#!/usr/bin/env python3
"""Restore v0.6 per-skill examples.md/checklist.md as conditional method references."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

WF = Path(__file__).resolve().parent.parent
REPO = WF.parent.parent
OLD_COMMIT = "781ea76"


def convert_ids(text: str, id2new: dict[str, str]) -> str:
    pattern = re.compile(r"\b(" + "|".join(sorted(map(re.escape, id2new), key=len, reverse=True)) + r")\b")
    return pattern.sub(lambda m: id2new[m.group(0)], text)


def main() -> int:
    migration = json.loads((WF / "Migration/migration-v0.7.json").read_text(encoding="utf-8"))
    id2new = {old: entry["method_id"] for old, entry in migration["method_map"].items()}
    restored = 0
    missing: list[str] = []
    for old_id, entry in migration["method_map"].items():
        pkg, slug = entry["package"], entry["slug"]
        for extra in ("checklist.md", "examples.md"):
            result = subprocess.run(
                ["git", "show", f"{OLD_COMMIT}:Framework/Workflow/Skills/{old_id}/{extra}"],
                cwd=REPO, capture_output=True,
            )
            if result.returncode != 0:
                continue  # this skill had no such file
            text = result.stdout.decode("utf-8").replace("\r\n", "\n")
            body = re.sub(r"^---\n.*?\n---\n?", "", text, count=1, flags=re.DOTALL).lstrip()
            body = convert_ids(body, id2new)
            kind = extra.removesuffix(".md")
            header = (
                f"# {entry['label']} — {kind} (conditional reference for {entry['method_id']})\n\n"
                f"> Loaded only when the consuming mode's live ambiguity or the user's explicit request "
                f"requires it; never loaded by default with the method file.\n\n"
            )
            out = WF / "Methods" / pkg / "references" / f"{slug}-{kind}.md"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(header + body, encoding="utf-8", newline="\n")
            restored += 1

    # Point each method file at its conditional references.
    for old_id, entry in migration["method_map"].items():
        pkg, slug = entry["package"], entry["slug"]
        method_path = WF / "Methods" / pkg / f"{slug}.md"
        kinds = [k for k in ("checklist", "examples")
                 if (WF / "Methods" / pkg / "references" / f"{slug}-{k}.md").is_file()]
        if not kinds:
            missing.append(entry["method_id"])
            continue
        text = method_path.read_text(encoding="utf-8")
        if "Conditional references:" in text:
            continue
        lines = [f"`references/{slug}-{k}.md`" for k in kinds]
        block = (
            "\n## Conditional references\n\n"
            "Loaded only on a live ambiguity or an explicit request — never with this method by default: "
            + ", ".join(lines) + ".\n"
        )
        text = text.rstrip() + "\n" + block
        method_path.write_text(text, encoding="utf-8", newline="\n")

    print(f"restored {restored} reference files")
    if missing:
        print("methods without any restored reference:", len(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
