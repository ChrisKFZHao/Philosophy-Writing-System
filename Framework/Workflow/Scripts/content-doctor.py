#!/usr/bin/env python3
"""Check private-content integrity without changing private artifacts."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path


def _scanner():
    path = Path(__file__).with_name("bibliography-scan.py")
    spec = importlib.util.spec_from_file_location("bibliography_scan", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCAN = _scanner()


def _script_module(filename: str, name: str):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


IDEA_LEDGER = _script_module("idea-ledger.py", "idea_ledger")
PROJECT_STATE = _script_module("project-state.py", "project_state")
FENCED_JSON = re.compile(r"```json[ \t]*\r?\n(.*?)\r?\n```", re.DOTALL | re.IGNORECASE)
REF_KEY = re.compile(r"^\s*([A-Z0-9][A-Z0-9-]*)\s*\|", re.MULTILINE)


def sha256(path: Path) -> str:
    if path.suffix.lower() in {".txt", ".md", ".json", ".tex", ".bib"}:
        # Normalize line endings so a CRLF checkout keeps a recorded text hash valid.
        data = path.read_bytes().replace(b"\r\n", b"\n")
        return hashlib.sha256(data).hexdigest()
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_documents(directory: Path, suffix: str) -> list[tuple[Path, dict]]:
    documents = []
    if not directory.is_dir():
        return documents
    for path in directory.glob(suffix):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict):
            documents.append((path, data))
    return documents


def summary_keys(summary_dir: Path) -> tuple[dict[str, Path], list[str]]:
    found: dict[str, Path] = {}
    errors: list[str] = []
    if not summary_dir.is_dir():
        return found, errors
    for path in sorted(p for suffix in (".md", ".txt") for p in summary_dir.glob(f"*.summary{suffix}")):
        matches = FENCED_JSON.findall(path.read_text(encoding="utf-8"))
        if not matches:
            errors.append(f"summary-json-missing:{path.name}")
            continue
        valid = False
        for text in matches:
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict) and isinstance(payload.get("bib_key"), str):
                key = payload["bib_key"]
                if key in found:
                    errors.append(f"summary-bib-key-duplicate:{key}:{found[key].name}:{path.name}")
                else:
                    found[key] = path
                valid = True
        if not valid:
            errors.append(f"summary-json-invalid:{path.name}")
    return found, errors


def refs_keys(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    return set(REF_KEY.findall(path.read_text(encoding="utf-8")))


def validate_project_json(project: Path, name: str, validator, failures: list[str]) -> None:
    path = project / name
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        failures.append(f"invalid-json:{project.name}/{name}")
        return
    errors = validator(data, project.name)
    for error in errors:
        failures.append(f"invalid-{name}:{project.name}:{error}")


def check(root: Path) -> dict:
    private = root / "Private"
    result = {"status": "ok", "failures": [], "warnings": [], "checks": {}}
    failures: list[str] = result["failures"]
    warnings: list[str] = result["warnings"]
    if not private.is_dir():
        result.update({"status": "skipped", "reason": "private-directory-absent"})
        return result

    bibliography = private / "Bibliography"
    index = bibliography / "INDEX.md"
    rows = SCAN.inventory_rows(index.read_text(encoding="utf-8") if index.is_file() else "")
    if not index.is_file():
        failures.append("index-missing")
    for row in rows:
        if row.get("malformed"):
            failures.append(f"index-malformed-row:{row['key']}")
    pdf_dir = bibliography / "PDF"
    disk_pdfs = {path.name: path for path in pdf_dir.glob("*.pdf")} if pdf_dir.is_dir() else {}
    indexed_pdfs = {pdf for row in rows for pdf in row["pdfs"]}
    for pdf in sorted(set(disk_pdfs) - indexed_pdfs):
        failures.append(f"pdf-missing-index:{pdf}")
    for pdf in sorted(indexed_pdfs - set(disk_pdfs)):
        failures.append(f"index-dangling-pdf:{pdf}")
    for pdf in sorted(disk_pdfs):
        if not SCAN.CANONICAL.fullmatch(pdf):
            failures.append(f"pdf-noncanonical:{pdf}")

    summary_by_key, summary_errors = summary_keys(bibliography / "Summaries")
    failures.extend(summary_errors)
    keys = {str(row["key"]) for row in rows}
    for row in rows:
        key = str(row["key"])
        if row["analysis_level"] is not None and key not in summary_by_key:
            failures.append(f"summary-missing-or-key-mismatch:{key}")

    metadata_by_key: dict[str, tuple[Path, dict]] = {}
    for path, data in json_documents(bibliography / "Analysis", "*.analysis.meta.json"):
        key = data.get("bib_key")
        if isinstance(key, str):
            metadata_by_key[key] = (path, data)
        else:
            failures.append(f"analysis-metadata-bib-key-missing:{path.name}")
    for row in rows:
        level = row["analysis_level"]
        key = str(row["key"])
        if level is None or level < 1:
            continue
        item = metadata_by_key.get(key)
        if item is None:
            failures.append(f"analysis-metadata-missing:{key}")
            continue
        path, data = item
        if not isinstance(data.get("analysis_level"), (int, float)) or float(data["analysis_level"]) < level:
            failures.append(f"analysis-level-insufficient:{key}")
        if data.get("verification_status") != "verified":
            failures.append(f"analysis-unverified:{key}")
        pdf_names = list(row["pdfs"])
        pdf = disk_pdfs.get(pdf_names[0]) if pdf_names else None
        expected_pdf_hash = data.get("source_sha256", data.get("pdf_sha256"))
        if pdf is None:
            failures.append(f"analysis-pdf-missing:{key}")
        elif not isinstance(expected_pdf_hash, str) or sha256(pdf) != expected_pdf_hash:
            failures.append(f"analysis-pdf-hash-mismatch:{key}")
        analysis_name = data.get("analysis_path") or data.get("analysis_file") or path.name.removesuffix(".meta.json")
        analysis_path = Path(str(analysis_name))
        if not analysis_path.is_absolute():
            analysis_path = root / analysis_path if str(analysis_name).startswith("Private/") else bibliography / "Analysis" / analysis_path
        expected_analysis_hash = data.get("analysis_sha256")
        if not analysis_path.is_file():
            failures.append(f"analysis-file-missing:{key}")
        elif not isinstance(expected_analysis_hash, str) or sha256(analysis_path) != expected_analysis_hash:
            failures.append(f"analysis-hash-mismatch:{key}")

    projects = private / "Projects"
    if projects.is_dir():
        for project in sorted((path for path in projects.iterdir() if path.is_dir()), key=lambda p: p.name):
            for key in sorted(refs_keys(project / "refs.md") - keys):
                failures.append(f"project-ref-key-missing:{project.name}:{key}")
            if not (project / "PROJECT.md").is_file():
                warnings.append(f"project-guidance-missing:{project.name}:PROJECT.md")
            else:
                text = (project / "PROJECT.md").read_text(encoding="utf-8")
                if not re.search(r"^collaboration:\s*(?:user-led|assistant-led|claude-led|codex-led)\s*$", text, re.MULTILINE):
                    warnings.append(f"project-collaboration-missing:{project.name}")
            validate_project_json(project, f"{project.name}-idea-ledger.json", IDEA_LEDGER.validate, failures)
            validate_project_json(project, f"{project.name}-workflow-state.json", PROJECT_STATE.validate, failures)
    result["checks"] = {"index_rows": len(rows), "pdfs": len(disk_pdfs), "summaries": len(summary_by_key)}
    if failures:
        result["status"] = "fail"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = check(args.root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Content doctor: {result['status']}")
        for problem in result["failures"]:
            print(f"- failure: {problem}")
        for warning in result["warnings"]:
            print(f"- warning: {warning}")
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
