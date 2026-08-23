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
    philosopher_root = REPO_ROOT / "Shared/Philosophers-DB"
    paths = [
        WORKFLOW_ROOT / "manifest.json",
        *(WORKFLOW_ROOT / "Schemas").glob("*.json"),
        *(WORKFLOW_ROOT / "Contracts").glob("*.json"),
        *(WORKFLOW_ROOT / "Migration").glob("*.json"),
        *(philosopher_root / "Profiles").glob("*.json"),
        philosopher_root / "Domains/registry.json",
    ]
    for path in paths:
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
        if re.search(r"^model:\s*", text, re.MULTILINE):
            failures.append(f"role-level model selection is forbidden: {relative}")


def markdown_files() -> list[Path]:
    roots = [
        WORKFLOW_ROOT,
        REPO_ROOT / ".claude",
        REPO_ROOT / ".agents",
        REPO_ROOT / "Framework/Lessons",
        REPO_ROOT / "Shared/Philosophers-DB",
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


def load_manifest(failures: list[str]) -> dict:
    try:
        return json.loads((WORKFLOW_ROOT / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"cannot read manifest: {exc}")
        return {}


def check_inventory(failures: list[str]) -> None:
    """Derive every inventory expectation from the manifest; no hard-coded counts."""
    manifest = load_manifest(failures)
    if not manifest:
        return
    items = manifest.get("items", [])
    skills = sorted(i["id"] for i in items if i.get("kind") == "skill")
    methods = {i["id"]: i for i in items if i.get("kind") == "method"}
    services = sorted(i["id"] for i in items if i.get("kind") == "service")
    commands = sorted(i["id"] for i in items if i.get("kind") == "command")

    core_skills = sorted(p.parent.name for p in (WORKFLOW_ROOT / "Skills").glob("*/SKILL.md"))
    claude_skills = sorted(p.parent.name for p in (REPO_ROOT / ".claude/skills").glob("*/SKILL.md"))
    codex_skills = sorted(p.parent.name for p in (REPO_ROOT / ".agents/skills").glob("*/SKILL.md"))
    if core_skills != skills:
        failures.append(f"core skill dirs {core_skills} do not match manifest skills {skills}")
    if claude_skills != skills:
        failures.append(f"claude skills {claude_skills} do not match manifest skills {skills}")
    if codex_skills != skills:
        failures.append(f"codex skills {codex_skills} do not match manifest skills {skills}")

    exposure = manifest.get("exposure", {})
    wrappers = sorted(p.stem for p in (REPO_ROOT / ".claude/commands").glob("*.md"))
    if wrappers != sorted(exposure.get("claude_command_wrappers", [])):
        failures.append(f"claude wrappers {wrappers} do not match exposure {exposure.get('claude_command_wrappers')}")

    if (REPO_ROOT / ".claude/agents").exists():
        failures.append(".claude/agents still exists; roles were removed in 0.7.0-alpha")
    leftover = sorted(p.parent.name for p in (REPO_ROOT / ".agents/skills").glob("source-command-*/SKILL.md"))
    if leftover:
        failures.append(f"source-command-* adapters remain: {leftover}")

    method_files = {p.relative_to(WORKFLOW_ROOT).as_posix() for p in (WORKFLOW_ROOT / "Methods").rglob("*.md")
                    if "references" not in p.parts}
    expected = {i["source"] for i in methods.values()}
    if method_files != expected:
        failures.append(f"Methods/ tree does not match manifest methods: extra={sorted(method_files - expected)}, missing={sorted(expected - method_files)}")
    method_slugs = {i["source"].rsplit("/", 1)[-1][:-3] for i in methods.values()}
    for reference in (WORKFLOW_ROOT / "Methods").glob("*/references/*.md"):
        stem = reference.stem
        if not any(stem == slug or stem.startswith(slug + "-") for slug in method_slugs):
            failures.append(f"orphan method reference: {reference.relative_to(REPO_ROOT)}")
    for service in (i for i in items if i.get("kind") == "service"):
        if not (WORKFLOW_ROOT / service["source"]).is_file():
            failures.append(f"missing service source: {service['id']}")
    for command in commands:
        if not (WORKFLOW_ROOT / "Commands").is_dir():
            failures.append("missing Commands/ directory")
    if sorted(exposure.get("skills", [])) != skills:
        failures.append("exposure.skills must list exactly the skill items")


STALE_PHRASES = (
    "30 skills", "9 workflows", "7 roles", "39 skills", "28 skills",
    "source-command-", "28 phil-*",
)


def check_stale_phrases(failures: list[str]) -> None:
    """Historical records (changelog, Lessons, Plans) are exempt; living definitions are not."""
    roots = [WORKFLOW_ROOT / "Skills", WORKFLOW_ROOT / "Methods", WORKFLOW_ROOT / "Services",
             WORKFLOW_ROOT / "Contracts", WORKFLOW_ROOT / "Commands", WORKFLOW_ROOT / "Rules",
             WORKFLOW_ROOT / "Templates", REPO_ROOT / ".claude", REPO_ROOT / ".agents",
             REPO_ROOT / "AGENTS.md", REPO_ROOT / "CLAUDE.md", REPO_ROOT / "README.md"]
    for root in roots:
        paths = [root] if root.is_file() else sorted(root.rglob("*.md")) if root.is_dir() else []
        for path in paths:
            if "worktrees" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for phrase in STALE_PHRASES:
                if phrase in text:
                    failures.append(
                        f"stale phrase '{phrase}' in {path.relative_to(REPO_ROOT)}"
                    )
                    break


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


def check_nested_project_bridges(failures: list[str]) -> None:
    private = REPO_ROOT / "Private"
    if not private.is_dir():
        return
    prefixes = [private]
    projects = private / "Projects"
    if projects.is_dir():
        prefixes.extend(path for path in projects.iterdir() if path.is_dir() and (path / "PROJECT.md").is_file())
    for prefix in prefixes:
        names = ("AGENTS.md", "CLAUDE.md") if prefix == private else ("AGENTS.md",)
        for name in names:
            path = prefix / name
            label = path.relative_to(REPO_ROOT)
            if not path.is_file():
                failures.append(f"missing nested project adapter: {label}")
            elif "not an independent workflow source" not in path.read_text(encoding="utf-8", errors="replace"):
                failures.append(f"invalid nested project adapter: {label}")
        _check_bridge_prefix(prefix, private, failures)


def _check_bridge_prefix(prefix: Path, private: Path, failures: list[str]) -> None:
    manifest = load_manifest(failures)
    if not manifest:
        return
    for item in manifest.get("items", []):
        item_id = item.get("id")
        if item.get("kind") == "skill":
            targets = [
                prefix / ".agents/skills" / item_id / "SKILL.md",
                prefix / ".claude/skills" / item_id / "SKILL.md",
            ]
        elif item.get("kind") == "command":
            targets = [prefix / ".claude/commands" / "full.md"]
        else:
            continue  # methods, packages, and services are never bridged
        for path in targets:
            label = path.relative_to(REPO_ROOT)
            if not path.is_file():
                failures.append(f"missing nested bridge: {label}")
            else:
                text = path.read_text(encoding="utf-8", errors="replace")
                if "External Workflow Bridge" not in text or "nearest ancestor" not in text:
                    failures.append(f"invalid nested bridge: {label}")


def check_philosopher_database(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(WORKFLOW_ROOT / "Scripts/philosopher-db.py"), "validate"],
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
    check_stale_phrases(failures)
    check_forbidden(failures)
    check_markdown_links(failures)
    check_philosopher_database(failures)
    check_adapters(failures)
    check_nested_project_bridges(failures)
    if failures:
        print("Workflow doctor failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Workflow doctor passed: core and adapters are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
