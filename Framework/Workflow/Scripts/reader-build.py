#!/usr/bin/env python3
"""Build a self-contained bilingual reader page from evidence units.

Reads the evidence units for a source stem, its translation lines, optional
agent and user notes, and optional reader overrides; renders the package
template and writes ``reader.html`` plus a ``reader.check.json`` report.

Only the Python standard library is required.
"""

from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_REL = "Framework/Workflow/Templates/Reader/reader.html"
PLACEHOLDER = "__READER_DATA__"
PAGE_MARKER = re.compile(r"⟦p([^⟧]+)⟧")
QUOTED_TITLE = re.compile(r'["“](.+?)["”]')

_BIBLIOGRAPHY_SCAN = None


# ---------------------------------------------------------------------------
# Loading helpers
# ---------------------------------------------------------------------------

def find_root(start: Path | None = None) -> Path | None:
    """Walk up to the directory that contains Framework/Workflow/manifest.json."""
    directory = Path(start or SCRIPT_DIR).resolve()
    for parent in [directory, *directory.parents]:
        if (parent / "Framework/Workflow/manifest.json").is_file():
            return parent
    return None


def bibliography_scan_module():
    """Load ``bibliography-scan.py`` so its inventory parser is reused."""
    global _BIBLIOGRAPHY_SCAN
    if _BIBLIOGRAPHY_SCAN is None:
        path = SCRIPT_DIR / "bibliography-scan.py"
        spec = importlib.util.spec_from_file_location("bibliography_scan", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _BIBLIOGRAPHY_SCAN = module
    return _BIBLIOGRAPHY_SCAN


def read_jsonl(path: Path) -> list[dict]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def read_json(path: Path):
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_translations(reader_dir: Path) -> tuple[dict[str, dict], dict | None]:
    """Load translation lines in file-name order; later lines win."""
    translations: dict[str, dict] = {}
    first: dict | None = None
    for path in sorted(reader_dir.glob("translation*.jsonl"), key=lambda item: item.name):
        for record in read_jsonl(path):
            if first is None:
                first = record
            translations[record["unit_id"]] = record
    return translations, first


def index_row(root: Path, stem: str) -> dict:
    """Return the INDEX row whose PDF cell names ``PDF/STEM.pdf``."""
    path = root / "Private/Bibliography/INDEX.md"
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    target = f"{stem}.pdf"
    for row in bibliography_scan_module().inventory_rows(text):
        if target in (row.get("pdfs") or []):
            return row
    return {}


# ---------------------------------------------------------------------------
# Small parsers
# ---------------------------------------------------------------------------

def cell(row: dict, index: int) -> str:
    cells = row.get("cells") or []
    return cells[index] if index < len(cells) else ""


def display_author(value: str) -> str:
    """Turn ``Surname, Given`` into ``Given Surname``; keep ``&`` joins."""
    parts = []
    for part in value.split("&"):
        part = part.strip()
        if "," in part:
            surname, given = part.split(",", 1)
            part = f"{given.strip()} {surname.strip()}".strip()
        if part:
            parts.append(part)
    return " & ".join(parts)


def extract_title(value: str) -> str:
    """Return the first double-quoted span, else the whole cell."""
    match = QUOTED_TITLE.search(value)
    return match.group(1).strip() if match else value.strip()


def year_of(stem: str) -> str:
    segments = stem.split("_")
    return segments[1] if len(segments) > 1 else ""


def insert_page_markers(text: str, page_breaks: list[dict]) -> str:
    """Insert ⟦pLABEL⟧ at each offset, from the largest offset down."""
    for page_break in sorted(page_breaks, key=lambda item: int(item["offset"]), reverse=True):
        offset = int(page_break["offset"])
        text = text[:offset] + f"⟦p{page_break['page_label']}⟧" + text[offset:]
    return text


def marker_labels(text: str) -> list[str]:
    return PAGE_MARKER.findall(text)


def first_page(value: str) -> str:
    return value.split("-", 1)[0].strip()


def last_page(value: str) -> str:
    return value.rsplit("-", 1)[-1].strip()


def user_notes_of(raw) -> list:
    if isinstance(raw, dict):
        return raw.get("items") or []
    if isinstance(raw, list):
        return raw
    return []


class MissingInput(Exception):
    """A required input file is absent."""


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build(root: Path, stem: str, out_path: Path) -> tuple[dict, str | None]:
    """Return ``(report, html)``; raise MissingInput when a required input is gone."""
    errors: list[str] = []
    warnings: list[str] = []
    bibliography = root / "Private/Bibliography"
    blocks_path = bibliography / "Extract" / stem / "blocks.jsonl"
    reader_dir = bibliography / "Reader" / stem

    if not blocks_path.is_file():
        raise MissingInput(str(blocks_path))
    translations, first_translation = load_translations(reader_dir)
    if not translations:
        raise MissingInput(f"no translation*.jsonl in {reader_dir}")

    blocks = read_jsonl(blocks_path)
    by_id = {block["unit_id"]: block for block in blocks}
    overrides = read_json(reader_dir / "reader.json") or {}
    epigraph_ids = set(overrides.get("epigraph") or [])
    row = index_row(root, stem)

    units: list[dict] = []
    footnotes: list[dict] = []
    included_zh: dict[str, str] = {}
    included_pages: list[str] = []

    for block in blocks:
        unit_id = block["unit_id"]
        translation = translations.get(unit_id)
        if translation is None:
            continue
        if translation.get("unit_sha256") != block.get("unit_sha256"):
            errors.append(f"stale:{unit_id}")
            continue
        layout = block.get("layout") or {}
        kind = layout.get("kind") or "body"
        en = insert_page_markers(block.get("text_span") or "", layout.get("page_breaks") or [])
        zh = translation.get("zh") or ""
        page = (block.get("locator") or {}).get("value") or ""
        if marker_labels(zh) != marker_labels(en):
            errors.append(f"page-markers:{unit_id}")
        if kind == "footnote":
            footnotes.append({"id": unit_id, "page": page, "en": en, "zh": zh})
        else:
            units.append({"id": unit_id, "kind": kind, "page": page,
                          "en": en, "zh": zh, "epigraph": unit_id in epigraph_ids})
        included_zh[unit_id] = zh
        included_pages.append(page)

    for unit_id in sorted(set(translations) - set(by_id)):
        warnings.append(f"orphan-translation:{unit_id}")
    for block in blocks:
        if "(cid:" in (block.get("text_span") or ""):
            warnings.append(f"cid-glyphs:{block['unit_id']}")

    notes_data = read_json(reader_dir / "agent-notes.json") or {}
    notes = (notes_data.get("notes") or []) if isinstance(notes_data, dict) else []
    for note in notes:
        note_id = note.get("id") or ""
        unit_id = note.get("unit_id") or ""
        block = by_id.get(unit_id)
        included = unit_id in included_zh
        if not included:
            warnings.append(f"note-unit:{note_id}")
        anchor_en = note.get("anchor_en") or ""
        if block is not None and anchor_en and anchor_en not in (block.get("text_span") or ""):
            warnings.append(f"anchor-en:{note_id}")
        anchor_zh = note.get("anchor_zh") or ""
        if included and anchor_zh and anchor_zh not in included_zh[unit_id]:
            warnings.append(f"anchor-zh:{note_id}")

    user_notes = user_notes_of(read_json(reader_dir / "user-notes.json"))

    if included_pages:
        page_range = f"{first_page(included_pages[0])}–{last_page(included_pages[-1])}"
    else:
        page_range = ""
    model = (first_translation or {}).get("model") or ""
    glossary = (first_translation or {}).get("glossary") or ""
    today = datetime.date.today().isoformat()
    colophon = (f"据 PDF 第 {page_range} 页 · 译文：{model} · "
                f"术语表：{glossary} · 生成于 {today}")

    meta = {
        "key": overrides.get("key") or row.get("key") or stem,
        "stem": stem,
        "title": extract_title(cell(row, 2)),
        "author": display_author(cell(row, 1)),
        "year": year_of(stem),
        "venue": overrides.get("venue") or "",
        "title_zh": overrides.get("title_zh") or "",
        "author_zh": overrides.get("author_zh") or "",
        "section_label": overrides.get("section_label") or "",
        "footer": overrides.get("footer") or "",
        "colophon": colophon,
    }
    data = {"meta": meta, "units": units, "footnotes": footnotes,
            "notes": notes, "user_notes": user_notes}

    html: str | None = None
    template_path = root / TEMPLATE_REL
    if not template_path.is_file():
        errors.append("template-missing")
    else:
        template = template_path.read_text(encoding="utf-8")
        if PLACEHOLDER not in template:
            errors.append("template-placeholder-missing")
        else:
            html = template.replace(PLACEHOLDER, json_payload(data))

    report = {
        "stem": stem,
        "output": str(out_path) if html is not None else "",
        "units": len(units),
        "footnotes": len(footnotes),
        "notes": len(notes),
        "user_notes": len(user_notes),
        "errors": errors,
        "warnings": warnings,
    }
    return report, html


def json_payload(data: dict) -> str:
    """Serialize for an HTML script context without breaking the parser."""
    payload = json.dumps(data, ensure_ascii=False)
    payload = payload.replace("</", "<\\/")
    return payload.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    parser = argparse.ArgumentParser(description="Build a bilingual reader page.")
    parser.add_argument("stem", help="bibliography stem, e.g. Author_2018_Title")
    parser.add_argument("--root", type=Path, help="repository root")
    parser.add_argument("--out", type=Path, help="output reader.html path")
    args = parser.parse_args(argv)

    root = (args.root or find_root() or Path.cwd()).resolve()
    out_path = args.out or root / "Private/Bibliography/Reader" / args.stem / "reader.html"

    try:
        report, html = build(root, args.stem, out_path)
    except MissingInput as exc:
        print(f"missing input: {exc}", file=sys.stderr)
        return 2

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if html is not None:
        out_path.write_text(html, encoding="utf-8")
    check_path = out_path.parent / "reader.check.json"
    check_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not report["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
