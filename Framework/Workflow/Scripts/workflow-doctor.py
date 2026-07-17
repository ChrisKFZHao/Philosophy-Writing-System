#!/usr/bin/env python3
"""Validate the neutral workflow core and both generated adapters."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = WORKFLOW_ROOT.parent.parent
FRONTMATTER = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def check_json(failures: list[str]) -> None:
    for path in [WORKFLOW_ROOT / "manifest.json", *(WORKFLOW_ROOT / "Schemas").glob("*.json")]:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"invalid JSON {path.relative_to(REPO_ROOT)}: {exc}")


def check_skill_frontmatter(failures: list[str]) -> None:
    for root in (
        WORKFLOW_ROOT / "Skills",
        REPO_ROOT / ".claude/skills",
        REPO_ROOT / ".agents/skills",
    ):
        for path in sorted(root.glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
            match = FRONTMATTER.match(text)
            if not match:
                failures.append(f"missing frontmatter: {path.relative_to(REPO_ROOT)}")
                continue
            keys = {
                line.split(":", 1)[0].strip()
                for line in match.group(1).splitlines()
                if ":" in line
            }
            if keys != {"name", "description"}:
                failures.append(f"invalid skill metadata {path.relative_to(REPO_ROOT)}: {sorted(keys)}")
                continue
            metadata = {}
            for line in match.group(1).splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip().strip('"')
            name = metadata["name"]
            description = metadata["description"]
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
                failures.append(f"invalid skill name {path.relative_to(REPO_ROOT)}: {name}")
            if not description or len(description) > 1024 or "<" in description or ">" in description:
                failures.append(f"invalid skill description {path.relative_to(REPO_ROOT)}")


def check_forbidden(failures: list[str]) -> None:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode:
        failures.append(f"cannot enumerate repository files: {result.stderr.strip()}")
        return
    files = [REPO_ROOT / line for line in result.stdout.splitlines() if line]
    for path in files:
        if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".py", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = path.relative_to(REPO_ROOT)
        forbidden_root = ".Co" + "dex"
        if f"{forbidden_root}/" in text or f"{forbidden_root}\\" in text:
            failures.append(f"forbidden legacy Codex root reference: {relative}")
        windows_users = r"C:\\" + r"Users\\[^\\\s]+"
        unix_users = "/" + "Users/" + r"[^/\s]+"
        if re.search(windows_users, text, re.IGNORECASE):
            failures.append(f"machine-specific user path: {relative}")
        if re.search(unix_users, text):
            failures.append(f"machine-specific user path: {relative}")
        if re.search(r'ZOTERO_API_KEY\s*[=:]\s*["\']?[A-Za-z0-9]{16,}', text):
            failures.append(f"possible embedded Zotero secret: {relative}")
        if re.search(r"^model:\s*(?:opus|sonnet|haiku|gpt-[A-Za-z0-9.-]+)\s*$", text, re.MULTILINE):
            allowed_claude_role = relative.parts[:2] == (".claude", "agents")
            if not allowed_claude_role:
                failures.append(f"provider model in neutral or Codex content: {relative}")


def markdown_files() -> list[Path]:
    roots = [
        WORKFLOW_ROOT,
        REPO_ROOT / ".claude",
        REPO_ROOT / ".agents",
        REPO_ROOT / "Framework/Lessons",
        REPO_ROOT / "README.md",
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "CLAUDE.md",
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file() and root.suffix.lower() == ".md":
            files.append(root)
        elif root.is_dir():
            files.extend(path for path in root.rglob("*.md") if "worktrees" not in path.parts)
    return sorted(set(files))


def check_markdown_links(failures: list[str]) -> None:
    for path in markdown_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            target = unquote(target.split("#", 1)[0])
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if any(char in target for char in "{}*"):
                continue
            target_path = Path(*target.replace("\\", "/").split("/"))
            candidates = [path.parent / target_path, REPO_ROOT / target_path]
            if not any(candidate.exists() for candidate in candidates):
                failures.append(
                    f"broken local link {path.relative_to(REPO_ROOT)} -> {raw_target}"
                )


def check_inventory(failures: list[str]) -> None:
    counts = {
        "core_skills": len(list((WORKFLOW_ROOT / "Skills").glob("*/SKILL.md"))),
        "claude_skills": len(list((REPO_ROOT / ".claude/skills").glob("*/SKILL.md"))),
        "codex_atomic": len(
            [path for path in (REPO_ROOT / ".agents/skills").glob("*/SKILL.md") if not path.parent.name.startswith("source-command-")]
        ),
        "claude_workflows": len(list((REPO_ROOT / ".claude/commands").glob("*.md"))),
        "codex_workflows": len(list((REPO_ROOT / ".agents/skills").glob("source-command-*/SKILL.md"))),
        "claude_roles": len(list((REPO_ROOT / ".claude/agents").glob("*.md"))),
    }
    expected = {
        "core_skills": 30,
        "claude_skills": 30,
        "codex_atomic": 30,
        "claude_workflows": 8,
        "codex_workflows": 8,
        "claude_roles": 7,
    }
    if counts != expected:
        failures.append(f"inventory mismatch: expected={expected}, actual={counts}")


def check_adapters(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(WORKFLOW_ROOT / "Scripts/build-adapters.py"), "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode:
        failures.append(result.stdout.strip() or result.stderr.strip())


def main() -> int:
    failures: list[str] = []
    check_json(failures)
    check_skill_frontmatter(failures)
    check_inventory(failures)
    check_forbidden(failures)
    check_markdown_links(failures)
    check_adapters(failures)
    if failures:
        print("Workflow doctor failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Workflow doctor passed: core and adapters are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
