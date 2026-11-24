#!/usr/bin/env python3
"""Report bibliography PDFs that are not fully registered and summarized.

Only rows in the ``Reference Inventory`` table are authoritative.  The INDEX
also documents naming conventions and examples, so scanning its prose creates
false registrations.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CANONICAL = re.compile(r"^[^_]+_(?:\d{4}|nd)_.+\.pdf$")
PDF_REFERENCE = re.compile(r"(?:^|\s)PDF/([^\s|,]+\.pdf)", re.IGNORECASE)
SUMMARY_SUFFIXES = (".md", ".txt")  # .md is current; .txt is accepted for older libraries


def inventory_rows(index_text: str) -> list[dict[str, object]]:
    """Parse rows from the Reference Inventory table and nothing else."""
    lines = index_text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == "## Reference Inventory"), None)
    if start is None:
        # A few callers use a minimal table fixture predating the explicit
        # heading.  Preserve that narrow compatibility mode without scanning
        # a real INDEX document's prose.
        rows = []
        for line in lines:
            if not line.lstrip().startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            pdfs = PDF_REFERENCE.findall(line)
            if cells and pdfs:
                rows.append({"key": cells[0], "pdfs": pdfs, "analysis_level": None, "cells": cells})
        return rows
    header = next((i for i in range(start + 1, len(lines)) if lines[i].lstrip().startswith("| KEY |")), None)
    if header is None or header + 1 >= len(lines):
        return []
    return _table_rows(lines[header + 2:], len(_split_cells(lines[header])))


def _split_cells(line: str) -> list[str]:
    """Split a table row on unescaped pipes; ``\\|`` is a literal pipe."""
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|") and not text.endswith("\\|"):
        text = text[:-1]
    cells: list[str] = []
    current: list[str] = []
    index = 0
    while index < len(text):
        character = text[index]
        if character == "\\" and index + 1 < len(text) and text[index + 1] == "|":
            current.append("|")
            index += 2
            continue
        if character == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
        index += 1
    cells.append("".join(current).strip())
    return cells


def _table_rows(lines: list[str], expected_columns: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in lines:
        if not line.lstrip().startswith("|"):
            break
        cells = _split_cells(line)
        if len(cells) != expected_columns:
            # Never read a shifted row by position; report it instead.
            rows.append({
                "key": cells[0] if cells else "",
                "pdfs": [],
                "analysis_level": None,
                "cells": cells,
                "malformed": True,
            })
            continue
        if len(cells) < 6:
            continue
        pdfs = PDF_REFERENCE.findall(cells[3])
        level_match = re.search(r"\bLevel\s+([0-9]+(?:\.[0-9]+)?)\b", cells[5], re.IGNORECASE)
        rows.append({
            "key": cells[0],
            "pdfs": pdfs,
            "analysis_level": float(level_match.group(1)) if level_match else None,
            "cells": cells,
        })
    return rows


def scan(root: Path) -> dict:
    bibliography = root / "Private/Bibliography"
    pdf_dir = bibliography / "PDF"
    index_path = bibliography / "INDEX.md"
    summary_dir = bibliography / "Summaries"
    index_text = index_path.read_text(encoding="utf-8") if index_path.is_file() else ""
    rows = inventory_rows(index_text)
    registered = {pdf for row in rows for pdf in row["pdfs"]}
    disk_pdfs = {path.name for path in pdf_dir.glob("*.pdf")} if pdf_dir.is_dir() else set()
    unprocessed = []
    for pdf in sorted(disk_pdfs, key=str.casefold):
        reasons = []
        if not CANONICAL.fullmatch(pdf):
            reasons.append("noncanonical-name")
        if pdf not in registered:
            reasons.append("missing-index-row")
        stem = Path(pdf).stem
        if not any((summary_dir / f"{stem}.summary{suffix}").is_file() for suffix in SUMMARY_SUFFIXES):
            reasons.append("missing-summary")
        if reasons:
            unprocessed.append({"file": pdf, "reasons": reasons})
    return {
        "pdf_count": len(disk_pdfs),
        "registered_pdf_count": len(registered),
        "unprocessed_count": len(unprocessed),
        "unprocessed": unprocessed,
        "dangling_index_pdfs": sorted(registered - disk_pdfs, key=str.casefold),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="exit 1 when unprocessed PDFs exist")
    args = parser.parse_args()
    result = scan(args.root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Unprocessed PDFs: {result['unprocessed_count']}")
        for item in result["unprocessed"]:
            print(f"- {item['file']}: {', '.join(item['reasons'])}")
        for pdf in result["dangling_index_pdfs"]:
            print(f"- dangling INDEX PDF: {pdf}")
    return 1 if args.strict and (result["unprocessed_count"] or result["dangling_index_pdfs"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
