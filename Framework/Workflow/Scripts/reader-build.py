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
# Footnote notes: split each footnote unit into single notes, then classify
# ---------------------------------------------------------------------------

# A note number is accepted only where it continues the running sequence
# (n+1 to n+3), so years and page numbers are never mistaken for note numbers.
NOTE_AT = re.compile(
    r"(^|[\s。．.;；])\[?(\d{1,3})\]?(?=[\s一-鿿A-Za-z‘“\"(*])")

LEAD_IN = re.compile(r"^(see also|see|cf\.?|e\.g\.,?|compare)\b", re.IGNORECASE)
FOR_LEAD_IN = re.compile(
    r"^for (?:further|more|other|a|an|the)?\s*[^,.;]{0,60}?,?\s*see( also)?\b",
    re.IGNORECASE)
STOCK_PHRASE = re.compile(
    r"emphasis (?:added|in original|mine)"
    r"|translation modified"
    r"|my translation"
    r"|trans(?:lated)? by"
    r"|quoted in"
    r"|all quotations (?:are )?from"
    r"|ibid\.?"
    r"|op\. cit\.?"
    r"|forthcoming"
    r"|unpublished manuscript",
    re.IGNORECASE)

CAP_NAME = r"[A-Z][A-Za-z’'\-]*"
NAME_SEQ = rf"{CAP_NAME}(?:(?:\s*,\s*|\s+)(?:and\s+|&\s+|et al\.?\s*)?{CAP_NAME})*"
YEAR = r"(?:\d{4}[a-z]?(?:/\d{4}[a-z]?)?|n\.d\.)"
CITATION_LOCATOR = (
    r"(?:,\s*(?:pp?\.\s*\d+(?:\s*[–-]\s*\d+)?|ch\.\s*\d+|sec\.\s*\d+"
    r"|§\s*\d+|[IVXL]+\.\d+|\d+:\d+|\d+(?:\s*,\s*\d+)*))?")
AUTHOR_YEAR = re.compile(rf"{NAME_SEQ}\s+{YEAR}{CITATION_LOCATOR}")

STOPWORDS = frozenset({"and", "also", "in", "the", "of", "for", "a", "an", "on"})
ACK_WORDS = ("thank", "grateful", "acknowledg")


def _note_hits(text: str, last: int) -> tuple[list[dict], int]:
    """Return accepted note numbers in ``text`` and the updated running number."""
    hits = []
    for match in NOTE_AT.finditer(text):
        number = int(match.group(2))
        if last < number <= last + 3:
            hits.append({"n": number,
                         "start": match.start() + len(match.group(1)),
                         "body": match.end()})
            last = number
    return hits, last


def _texts_by_number(text: str, hits: list[dict]) -> dict[int, str]:
    """Slice each note's text from its number to the next accepted number."""
    notes = {}
    for index, hit in enumerate(hits):
        end = hits[index + 1]["start"] if index + 1 < len(hits) else len(text)
        notes[hit["n"]] = text[hit["body"]:end].strip()
    return notes


def split_footnote_notes(footnotes: list[dict]) -> list[dict]:
    """Split footnote units into single notes, pairing EN with ZH by number."""
    last = {"en": 0, "zh": 0}
    parsed = []
    for unit in footnotes:
        per_language = {}
        for language in ("en", "zh"):
            text = unit.get(language) or ""
            hits, last[language] = _note_hits(text, last[language])
            per_language[language] = (text, _texts_by_number(text, hits))
        parsed.append((unit, per_language))

    notes = []
    for unit, per_language in parsed:
        en_text, en_notes = per_language["en"]
        zh_text, zh_notes = per_language["zh"]
        numbers = sorted(set(en_notes) | set(zh_notes))
        if not numbers:
            notes.append({"n": None, "page": unit["page"], "unit": unit["id"],
                          "en": en_text, "zh": zh_text})
            continue
        for number in numbers:
            notes.append({"n": str(number), "page": unit["page"], "unit": unit["id"],
                          "en": en_notes.get(number, ""), "zh": zh_notes.get(number, "")})
    return notes


def classify_note(text: str, number: int | None, overrides: dict) -> tuple[str, bool]:
    """Return ``(kind, override_applied)`` for one note, judged on its EN text."""
    if number is not None and str(number) in overrides:
        return overrides[str(number)], True

    text = (text or "").strip()
    if number is None:
        lowered = text.lower()
        if text.startswith("*") or any(word in lowered for word in ACK_WORDS):
            return "acknowledgement", False
        return "other", False

    # (a) reading-pointer lead-ins, repeatedly, then (b) stock phrases,
    # then (c) author-year citations.
    for _ in range(4):
        stripped = LEAD_IN.sub("", text)
        stripped = FOR_LEAD_IN.sub("", stripped)
        if stripped == text:
            break
        text = stripped
    text = STOCK_PHRASE.sub(" ", text)
    text = AUTHOR_YEAR.sub(" ", text)

    words = [word.lower() for word in re.findall(r"[A-Za-z]+", text)]
    count = sum(1 for word in words if word not in STOPWORDS and len(word) >= 3)
    return ("citation" if count <= 2 else "substantive"), False


def build_footnote_notes(footnotes: list[dict], overrides: dict) -> list[dict]:
    """Split, pair, and classify every note; ``overrides`` is keyed by number."""
    overrides = overrides or {}
    result = []
    for note in split_footnote_notes(footnotes):
        number = int(note["n"]) if note["n"] is not None else None
        kind, applied = classify_note(note["en"], number, overrides)
        record = {"n": note["n"], "page": note["page"], "unit": note["unit"],
                  "en": note["en"], "zh": note["zh"], "kind": kind}
        if applied:
            record["override"] = True
        result.append(record)
    return result


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
    footnote_kinds = overrides.get("footnote_kinds") or {}

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
    footnote_notes = build_footnote_notes(footnotes, footnote_kinds)
    data = {"meta": meta, "units": units, "footnotes": footnotes,
            "footnote_notes": footnote_notes,
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
        "footnote_notes": len(footnote_notes),
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
