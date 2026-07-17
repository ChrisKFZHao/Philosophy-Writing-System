#!/usr/bin/env python3
"""Report bibliography PDFs that are not fully registered and summarized."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CANONICAL = re.compile(r"^[^_]+_(?:\d{4}|nd)_.+\.pdf$")
REGISTERED = re.compile(r"PDF/([^ |,]+\.pdf)", re.IGNORECASE)


def scan(root: Path) -> dict:
    bibliography = root / "Private/Bibliography"
    pdf_dir = bibliography / "PDF"
    index_path = bibliography / "INDEX.md"
    summary_dir = bibliography / "Summaries"
    index_text = index_path.read_text(encoding="utf-8") if index_path.is_file() else ""
    registered = {match.group(1) for match in REGISTERED.finditer(index_text)}
    unprocessed = []
    for pdf in sorted(pdf_dir.glob("*.pdf"), key=lambda path: path.name.casefold()):
        reasons = []
        if not CANONICAL.fullmatch(pdf.name):
            reasons.append("noncanonical-name")
        if pdf.name not in registered:
            reasons.append("missing-index-row")
        if not (summary_dir / f"{pdf.stem}.summary.txt").is_file():
            reasons.append("missing-summary")
        if reasons:
            unprocessed.append({"file": pdf.name, "reasons": reasons})
    return {
        "pdf_count": len(list(pdf_dir.glob("*.pdf"))) if pdf_dir.is_dir() else 0,
        "registered_pdf_count": len(registered),
        "unprocessed_count": len(unprocessed),
        "unprocessed": unprocessed,
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
    return 1 if args.strict and result["unprocessed_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
