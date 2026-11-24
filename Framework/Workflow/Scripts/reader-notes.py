#!/usr/bin/env python3
"""Summarize reading-page annotations and route them into the workflow.

``summary`` is read-only.  ``route`` writes only for annotations not yet
routed: ``idea`` notes go to the project idea ledger through
``idea-ledger.py``; ``cite`` notes become candidate rows/lines in the
project's ``refs.md``.  Routing state lives in ``notes-routed.json`` next to
the annotations, written atomically.

Only the Python standard library is required.
"""

from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
IDEA_LEDGER = SCRIPT_DIR / "idea-ledger.py"
PAGE_MARKER = re.compile(r"⟦p([^⟧]+)⟧")
QUOTE_LIMIT = 40
TAG_KINDS = ("idea", "cite")
ROUTE_TARGET = {"idea": "idea-ledger", "cite": "refs"}
KIND_LABELS = {
    "highlight": "高亮",
    "comment": "批注",
    "idea": "想法",
    "cite": "引用候选",
    "paragraph-comment": "段落批注",
}
CANDIDATE_SECTION = "## 阅读页引用候选"
CANDIDATE_WARNING = "译文仅供定位，引用前须按原文单元核对英文原句"


class NotesError(Exception):
    """A user-facing failure."""


# ---------------------------------------------------------------------------
# Loading shared parsers from reader-build.py
# ---------------------------------------------------------------------------

_READER_BUILD = None


def reader_build():
    """Load ``reader-build.py`` so its loading helpers are reused."""
    global _READER_BUILD
    if _READER_BUILD is None:
        path = SCRIPT_DIR / "reader-build.py"
        spec = importlib.util.spec_from_file_location("reader_build", path)
        if spec is None or spec.loader is None:
            raise NotesError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _READER_BUILD = module
    return _READER_BUILD


def find_root(start: Path | None = None) -> Path | None:
    directory = Path(start or SCRIPT_DIR).resolve()
    for parent in [directory, *directory.parents]:
        if (parent / "Framework/Workflow/manifest.json").is_file():
            return parent
    return None


def paths(root: Path, stem: str) -> dict[str, Path]:
    bibliography = root / "Private/Bibliography"
    reader = bibliography / "Reader" / stem
    return {
        "reader": reader,
        "notes": reader / "user-notes.json",
        "routed": reader / "notes-routed.json",
        "blocks": bibliography / "Extract" / stem / "blocks.jsonl",
        "index": bibliography / "INDEX.md",
    }


def read_json(path: Path):
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise NotesError(f"无法读取 {path}: {exc}")


def write_atomic(path: Path, text: str) -> None:
    temp = path.with_name(path.name + ".tmp")
    try:
        temp.write_text(text, encoding="utf-8")
        os.replace(temp, path)
    except BaseException:
        temp.unlink(missing_ok=True)
        raise


# ---------------------------------------------------------------------------
# KEY <-> stem and project files
# ---------------------------------------------------------------------------

def index_rows(root: Path) -> list[dict]:
    path = root / "Private/Bibliography/INDEX.md"
    if not path.is_file():
        return []
    return reader_build().bibliography_scan_module().inventory_rows(
        path.read_text(encoding="utf-8"))


def key_for_stem(root: Path, stem: str) -> str:
    row = reader_build().index_row(root, stem)
    return row.get("key") or stem


def stem_for_key(root: Path, key: str) -> str | None:
    for row in index_rows(root):
        if row.get("key") != key:
            continue
        for pdf in row.get("pdfs") or []:
            name = Path(pdf).name
            return name[:-4] if name.lower().endswith(".pdf") else name
    return None


def refs_keys(refs_path: Path) -> list[str]:
    """Return the KEY column of every table row, preserving order."""
    keys: list[str] = []
    if not refs_path.is_file():
        return keys
    for line in refs_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if "|" not in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 3 or not cells[0] or cells[0] == "KEY":
            continue
        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        if cells[0] not in keys:
            keys.append(cells[0])
    return keys


def has_table_row(refs_text: str, key: str) -> bool:
    for line in refs_text.splitlines():
        stripped = line.strip()
        if "|" not in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) >= 3 and cells[0] == key:
            return True
    return False


def project_directory(root: Path, topic: str) -> Path:
    project = root / "Private/Projects" / topic
    if not project.is_dir():
        raise NotesError(f"项目目录不存在：{project}")
    return project


# ---------------------------------------------------------------------------
# Annotation reading
# ---------------------------------------------------------------------------

def load_annotations(root: Path, stem: str) -> list[dict]:
    locations = paths(root, stem)
    if not locations["notes"].is_file():
        raise NotesError(f"没有阅读页批注：{locations['notes']}")
    raw = read_json(locations["notes"])
    return reader_build().user_notes_of(raw)


def load_context(root: Path, stem: str) -> tuple[dict, dict, dict]:
    """Return ``(translations, blocks_by_id, blocks)``, tolerating missing files."""
    locations = paths(root, stem)
    source = reader_build()
    translations: dict = {}
    if locations["reader"].is_dir():
        translations, _ = source.load_translations(locations["reader"])
    blocks = []
    if locations["blocks"].is_file():
        blocks = source.read_jsonl(locations["blocks"])
    return translations, {block["unit_id"]: block for block in blocks}, blocks


def body_values(annotation: dict, purpose: str) -> list[str]:
    values = []
    for body in annotation.get("body") or []:
        if isinstance(body, dict) and body.get("purpose") == purpose:
            value = body.get("value")
            if isinstance(value, str):
                values.append(value)
    return values


def quote_selector(annotation: dict) -> dict | None:
    for selector in (annotation.get("target") or {}).get("selector") or []:
        if isinstance(selector, dict) and selector.get("type") == "TextQuoteSelector":
            return selector
    return None


def position_start(annotation: dict) -> int | None:
    for selector in (annotation.get("target") or {}).get("selector") or []:
        if isinstance(selector, dict) and selector.get("type") == "TextPositionSelector":
            start = selector.get("start")
            if isinstance(start, int):
                return start
    return None


def kind_of(annotation: dict) -> str:
    tags = body_values(annotation, "tagging")
    if "idea" in tags:
        return "idea"
    if "cite" in tags:
        return "cite"
    comment = bool(body_values(annotation, "commenting"))
    if quote_selector(annotation) is None:
        return "paragraph-comment"
    return "comment" if comment else "highlight"


def clean_with_labels(zh: str) -> tuple[str, list[str]]:
    """Remove page markers and record the page label covering each character."""
    pieces: list[str] = []
    labels: list[str] = []
    current = ""
    last = 0
    for match in PAGE_MARKER.finditer(zh):
        segment = zh[last:match.start()]
        pieces.append(segment)
        labels.extend([current] * len(segment))
        current = match.group(1)
        last = match.end()
    segment = zh[last:]
    pieces.append(segment)
    labels.extend([current] * len(segment))
    return "".join(pieces), labels


def locate_quote(clean: str, selector: dict) -> int | None:
    exact = selector.get("exact") or ""
    if not exact:
        return None
    prefix = selector.get("prefix") or ""
    if prefix:
        index = clean.find(prefix + exact)
        if index >= 0:
            return index + len(prefix)
    index = clean.find(exact)
    return index if index >= 0 else None


def load_routed(root: Path, stem: str) -> dict:
    raw = read_json(paths(root, stem)["routed"])
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise NotesError(f"notes-routed.json 格式无效：{paths(root, stem)['routed']}")
    return raw


def start_page(locator: str) -> str:
    """Return the first printed page of a locator such as ``126-127`` or ``126–127``."""
    return re.split(r"\s*[-–—]\s*", locator, maxsplit=1)[0] if locator else locator


def note_records(root: Path, stem: str, key: str | None = None) -> tuple[list[dict], dict]:
    """Return ``(records, routed)`` in document order before question sorting."""
    key = key or key_for_stem(root, stem)
    annotations = load_annotations(root, stem)
    translations, blocks_by_id, blocks = load_context(root, stem)
    routed = load_routed(root, stem)
    order = {block["unit_id"]: index for index, block in enumerate(blocks)}
    records = []
    for annotation in annotations:
        if not isinstance(annotation, dict) or not annotation.get("id"):
            continue
        target = annotation.get("target") or {}
        unit_id = target.get("source") or ""
        block = blocks_by_id.get(unit_id) or {}
        locator = (block.get("locator") or {}).get("value") or ""
        zh = (translations.get(unit_id) or {}).get("zh") or ""
        clean, labels = clean_with_labels(zh)
        selector = quote_selector(annotation)
        comment = "\n".join(body_values(annotation, "commenting")).strip()
        kind = kind_of(annotation)
        if selector is not None:
            quote = selector.get("exact") or ""
            index = locate_quote(clean, selector)
            # Before the unit's first page marker the quote sits on the page where the unit
            # starts: the first label of a range such as "126-127".
            page = labels[index] if index is not None and labels[index] else start_page(locator)
            fallback = position_start(annotation)
            start = index if index is not None else (fallback if fallback is not None else -1)
        else:
            joined = " ".join(clean.split())
            quote = joined[:QUOTE_LIMIT]
            if len(joined) > QUOTE_LIMIT:
                quote += "…"
            page = locator
            start = -1
        records.append({
            "id": annotation["id"],
            "kind": kind,
            "key": key,
            "stem": stem,
            "unit_id": unit_id,
            "page": page,
            "quote": quote,
            "comment": comment,
            "created": annotation.get("created") or "",
            "modified": annotation.get("modified") or annotation.get("created") or "",
            "question": "?" in comment or "？" in comment,
            "routed": routed.get(annotation["id"]),
            "start": start,
            "order": order.get(unit_id, len(order)),
        })
    return records, routed


def sort_records(records: list[dict]) -> list[dict]:
    """Questions first within a source, then document order."""
    return sorted(records, key=lambda record: (
        0 if record["question"] else 1,
        record["order"],
        record["start"],
        record["created"],
    ))


def source_summary(root: Path, stems: list[tuple[str, str]]) -> list[dict]:
    sources = []
    for stem, key in stems:
        records, _ = note_records(root, stem, key)
        records = sort_records(records)
        sources.append({
            "stem": stem,
            "key": key,
            "notes": [{field: value for field, value in record.items()
                       if field not in {"start", "order"}} for record in records],
        })
    return sources


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def one_line(value: str) -> str:
    return " ".join((value or "").split())


def format_summary(sources: list[dict]) -> str:
    lines: list[str] = []
    for source in sources:
        notes = source["notes"]
        if not notes:
            lines.append(f"{source['key']}  {source['stem']}  （无批注）")
            continue
        lines.append(f"{source['key']}  {source['stem']}  {len(notes)} 条")
        for note in notes:
            state = "未归档"
            routed = note.get("routed") or {}
            if routed:
                state = "已归档→" + (routed.get("to") or "")
            prefix = "问  " if note["question"] else "    "
            line = f"  {prefix}p. {note['page'] or '?'}  {KIND_LABELS.get(note['kind'], note['kind'])}"
            if note["quote"]:
                line += f"「{one_line(note['quote'])}」"
            if note["comment"]:
                line += f" — {one_line(note['comment'])}"
            line += f"  [{state}]  {note['id']}"
            if note.get("created"):
                line += f"  {note['created'][:10]}"
            lines.append(line)
    if not sources:
        lines.append("无阅读页批注。")
    return "\n".join(lines)


def summary_json(sources: list[dict]) -> dict:
    return {
        "sources": sources,
        "counts": {
            "notes": sum(len(source["notes"]) for source in sources),
            "unrouted": sum(1 for source in sources for note in source["notes"]
                            if not note.get("routed")),
        },
    }


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def idea_command(project: Path, note: dict) -> tuple[list[str], str]:
    """Return ``(argv, statement)`` for one idea note."""
    quote = one_line(note["quote"]) or "（整段）"
    statement = note["comment"].strip() or f"阅读时标为想法：「{quote}」"
    reason = f"阅读页批注 {note['id']}，{note['key']} p. {note['page'] or '?'}"
    trigger = "user-request:" + f"用户重读 {note['key']} 或重访该想法时重新评估"
    argv = [
        sys.executable, str(IDEA_LEDGER), "--project-dir", str(project),
        "record", "--statement", statement,
        "--provenance", "user", "--status", "parked",
        "--bib-key", note["key"],
        "--reason", reason,
        "--trigger", trigger,
    ]
    return argv, statement


def cite_line(note: dict) -> str:
    line = (f"- `{note['key']}` p. {note['page'] or '?'}（unit `{note['unit_id']}`）："
            f"“{one_line(note['quote'])}”——{CANDIDATE_WARNING}。")
    if note["comment"]:
        line += f"用户批注：{one_line(note['comment'])} "
    return line + f"<!-- note:{note['id']} -->"


def insert_candidate_row(lines: list[str], key: str) -> None:
    """Insert a candidate row into the first refs table."""
    row = f"| {key} | background | candidate | 来自阅读页批注 |\n"
    header = next((index for index, line in enumerate(lines)
                   if line.lstrip().startswith("| KEY")), None)
    if header is None:
        lines.append(row)
        return
    last = header
    index = header + 1
    while index < len(lines) and lines[index].lstrip().startswith("|"):
        last = index
        index += 1
    lines.insert(last + 1, row)


def append_candidate_lines(lines: list[str], new_lines: list[str]) -> None:
    """Append lines under the candidate section, creating it at the end if absent."""
    heading = next((index for index, line in enumerate(lines)
                    if line.strip() == CANDIDATE_SECTION), None)
    if heading is None:
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        if lines and lines[-1].strip():
            lines.append("\n")
        lines.append(CANDIDATE_SECTION + "\n\n")
        lines.extend(new_lines)
        return
    insert = heading + 1
    while insert < len(lines) and not lines[insert].startswith("## "):
        insert += 1
    if insert > heading + 1 and lines[insert - 1].strip():
        new_lines = ["\n"] + new_lines
    elif insert == len(lines) and lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    lines[insert:insert] = new_lines


def read_refs(refs_path: Path) -> tuple[str, list[str]]:
    with refs_path.open("r", encoding="utf-8", newline="") as handle:
        text = handle.read()
    return text, text.splitlines(keepends=True)


def write_refs(refs_path: Path, lines: list[str]) -> None:
    text = "".join(lines)
    if text and not text.endswith("\n"):
        text += "\n"
    write_atomic(refs_path, text)


def route(root: Path, stem: str, topic: str, dry_run: bool = False,
          only: str | None = None, ids: list[str] | None = None) -> list[dict]:
    """Route pending notes; return one change record per note."""
    project = project_directory(root, topic)
    refs_path = project / "refs.md"
    if not refs_path.is_file():
        raise NotesError(f"项目没有 refs.md：{refs_path}")
    records, routed = note_records(root, stem)
    wanted = [only] if only else list(TAG_KINDS)
    if ids:
        known = {record["id"] for record in records}
        unknown = [identifier for identifier in ids if identifier not in known]
        if unknown:
            raise NotesError("找不到批注：" + ", ".join(unknown))
    selected = []
    for record in sort_records(records):
        if record["kind"] not in wanted:
            continue
        if ids and record["id"] not in ids:
            continue
        target = ROUTE_TARGET[record["kind"]]
        if (record.get("routed") or {}).get("to") == target:
            continue
        selected.append(record)
    if not selected:
        print("没有待归档的批注。")
        return []

    refs_text, refs_lines = read_refs(refs_path)
    today = datetime.date.today().isoformat()
    changes: list[dict] = []
    refs_new_lines: list[str] = []
    refs_row_needed = False
    row_announced = False

    for note in selected:
        target = ROUTE_TARGET[note["kind"]]
        entry = {"to": target, "project": topic, "date": today}
        if target == "idea-ledger":
            argv, statement = idea_command(project, note)
            change = {"id": note["id"], "kind": note["kind"], "target": target,
                      "page": note["page"], "statement": statement,
                      "argv": argv, "entry": entry}
            if dry_run:
                print(f"idea  {note['id']}  {note['key']} p. {note['page'] or '?'}")
                print(f"  statement: {statement}")
                print(f"  reason: 阅读页批注 {note['id']}，{note['key']} p. {note['page'] or '?'}")
                print(f"  trigger: {argv[-1]}")
                print(f"  routed: {json.dumps({note['id']: entry}, ensure_ascii=False)}")
            else:
                completed = subprocess.run(
                    argv, capture_output=True, text=True, encoding="utf-8",
                    env={**os.environ, "PYTHONIOENCODING": "utf-8"})
                if completed.returncode != 0:
                    raise NotesError(
                        f"idea-ledger 失败：{completed.stderr.strip() or completed.stdout.strip()}")
                payload = json.loads(completed.stdout or "{}")
                ledger_id = (payload.get("idea") or {}).get("id")
                if ledger_id:
                    entry["ledger_id"] = ledger_id
                change["entry"] = entry
                print(f"idea  {note['id']} → {ledger_id or 'idea-ledger'}")
            routed[note["id"]] = entry
        else:
            line = cite_line(note)
            marker = f"<!-- note:{note['id']} -->"
            change = {"id": note["id"], "kind": note["kind"], "target": target,
                      "page": note["page"], "line": line, "entry": entry}
            if not has_table_row(refs_text, note["key"]):
                refs_row_needed = True
            if marker not in refs_text and line not in refs_new_lines:
                refs_new_lines.append(line + "\n")
            if dry_run:
                print(f"refs  {note['id']}  {note['key']} p. {note['page'] or '?'}")
                if refs_row_needed and not row_announced:
                    row_announced = True
                    print(f"  row: | {note['key']} | background | candidate | 来自阅读页批注 |")
                print(f"  line: {line}")
                print(f"  routed: {json.dumps({note['id']: entry}, ensure_ascii=False)}")
            else:
                print(f"refs  {note['id']} → {note['key']} p. {note['page'] or '?'}")
            routed[note["id"]] = entry
        changes.append(change)

    if dry_run:
        print("（--dry-run：未写入任何文件）")
        return changes

    if refs_new_lines or refs_row_needed:
        if refs_row_needed:
            insert_candidate_row(refs_lines, selected[0]["key"])
        if refs_new_lines:
            append_candidate_lines(refs_lines, refs_new_lines)
        write_refs(refs_path, refs_lines)
    write_atomic(paths(root, stem)["routed"],
                 json.dumps(routed, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return changes


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def resolve_project_sources(root: Path, topic: str) -> list[tuple[str, str]]:
    project = project_directory(root, topic)
    refs_path = project / "refs.md"
    if not refs_path.is_file():
        raise NotesError(f"项目没有 refs.md：{refs_path}")
    sources = []
    for key in refs_keys(refs_path):
        stem = stem_for_key(root, key)
        if not stem:
            continue
        if paths(root, stem)["notes"].is_file():
            sources.append((stem, key))
    return sources


def command_summary(args) -> int:
    root = (args.root or find_root() or Path.cwd()).resolve()
    if bool(args.stem) == bool(args.project):
        raise NotesError("summary 需要 STEM 或 --project TOPIC（二选一）")
    if args.project:
        stems = resolve_project_sources(root, args.project)
    else:
        locations = paths(root, args.stem)
        if not locations["notes"].is_file():
            raise NotesError(f"没有阅读页批注：{locations['notes']}")
        stems = [(args.stem, key_for_stem(root, args.stem))]
    sources = source_summary(root, stems)
    if args.new:
        for source in sources:
            source["notes"] = [note for note in source["notes"] if not note.get("routed")]
        sources = [source for source in sources if source["notes"]]
    if args.json:
        print(json.dumps(summary_json(sources), ensure_ascii=False, indent=2))
    else:
        print(format_summary(sources))
    return 0


def command_route(args) -> int:
    root = (args.root or find_root() or Path.cwd()).resolve()
    route(root, args.stem, args.project, args.dry_run, args.only, args.ids)
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    parser = argparse.ArgumentParser(
        description="Summarize or route reading-page annotations.")
    sub = parser.add_subparsers(dest="command", required=True)

    summary_parser = sub.add_parser("summary", help="list annotations (read-only)")
    summary_parser.add_argument("stem", nargs="?", help="bibliography stem")
    summary_parser.add_argument("--project", help="list every registered KEY with notes")
    summary_parser.add_argument("--root", type=Path, help="repository root")
    summary_parser.add_argument("--new", action="store_true", help="only unrouted notes")
    summary_parser.add_argument("--json", action="store_true", help="machine-readable output")

    route_parser = sub.add_parser("route", help="route idea/cite annotations")
    route_parser.add_argument("stem", help="bibliography stem")
    route_parser.add_argument("--project", required=True, help="project topic")
    route_parser.add_argument("--root", type=Path, help="repository root")
    route_parser.add_argument("--dry-run", action="store_true", help="print without writing")
    route_parser.add_argument("--only", choices=TAG_KINDS, help="route one kind only")
    route_parser.add_argument("--ids", nargs="+", help="route only these annotation ids")

    args = parser.parse_args(argv)
    try:
        if args.command == "summary":
            return command_summary(args)
        return command_route(args)
    except NotesError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
