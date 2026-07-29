#!/usr/bin/env python3
"""Generate Claude Code and Codex adapters from Framework/Workflow."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = WORKFLOW_ROOT.parent.parent
MANIFEST_PATH = WORKFLOW_ROOT / "manifest.json"
GENERATED = "<!-- Generated from Framework/Workflow. Do not edit directly. -->"
ITEM_FIELDS = {
    "id",
    "kind",
    "source",
    "description",
    "dependencies",
    "role",
    "capabilities",
    "output_contract",
    "platforms",
}
KINDS = {"skill", "workflow", "role"}
PLATFORMS = {"claude", "codex"}
CAPABILITIES = {
    "read",
    "search",
    "write",
    "delegate",
    "pdf",
    "zotero-full",
    "zotero-local",
}


class ManifestError(ValueError):
    pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        return {}, text
    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata, match.group(2).lstrip("\n")


def frontmatter(name: str, description: str) -> str:
    return f"---\nname: {name}\ndescription: {yaml_string(description)}\n---\n"


def load_manifest() -> dict:
    data = json.loads(read_text(MANIFEST_PATH))
    if set(data) != {"schema_version", "items"}:
        raise ManifestError("manifest top level must contain only schema_version and items")
    if data["schema_version"] != 1 or not isinstance(data["items"], list):
        raise ManifestError("unsupported manifest schema")

    ids: dict[str, dict] = {}
    sources: set[str] = set()
    for item in data["items"]:
        if set(item) != ITEM_FIELDS:
            unknown = sorted(set(item) - ITEM_FIELDS)
            missing = sorted(ITEM_FIELDS - set(item))
            raise ManifestError(f"invalid fields for {item.get('id')}: unknown={unknown}, missing={missing}")
        item_id = item["id"]
        if not re.fullmatch(r"[a-z0-9-]+", item_id):
            raise ManifestError(f"invalid id: {item_id}")
        if item_id in ids:
            raise ManifestError(f"duplicate id: {item_id}")
        if item["kind"] not in KINDS:
            raise ManifestError(f"invalid kind for {item_id}")
        if not item["description"] or not isinstance(item["description"], str):
            raise ManifestError(f"missing description for {item_id}")
        item["description"] = item["description"].strip()
        if set(item["platforms"]) - PLATFORMS:
            raise ManifestError(f"unknown platform for {item_id}")
        if set(item["capabilities"]) - CAPABILITIES:
            raise ManifestError(f"unknown capability for {item_id}")
        if item["source"] in sources:
            raise ManifestError(f"duplicate source: {item['source']}")
        source = WORKFLOW_ROOT / item["source"]
        if not source.is_file():
            raise ManifestError(f"missing source for {item_id}: {item['source']}")
        sources.add(item["source"])
        ids[item_id] = item

    for item in data["items"]:
        for dependency in item["dependencies"]:
            if dependency not in ids:
                raise ManifestError(f"unknown dependency {dependency} in {item['id']}")
        role = item["role"]
        if role is not None and (role not in ids or ids[role]["kind"] != "role"):
            raise ManifestError(f"unknown role {role} in {item['id']}")

    counts = {kind: sum(i["kind"] == kind for i in data["items"]) for kind in KINDS}
    if counts != {"skill": 30, "workflow": 9, "role": 7}:
        raise ManifestError(f"unexpected inventory: {counts}")
    return data


def add_output(outputs: dict[Path, str | bytes], path: Path, content: str | bytes) -> None:
    if path in outputs:
        raise ManifestError(f"output collision: {path}")
    outputs[path] = content


def generated_markdown(text: str) -> str:
    return f"{GENERATED}\n{text.lstrip()}"


def codex_workflow_preamble(item: dict) -> str:
    role_line = ""
    if item["role"]:
        role_line = (
            f"- Read `Framework/Workflow/Roles/{item['role']}.md` completely and adopt that role "
            "before executing the workflow.\n"
        )
    delegation = ""
    if "delegate" in item["capabilities"]:
        delegation = (
            "- When delegation is available, parallelize only independent stages; otherwise execute the same "
            "dependency order serially.\n"
        )
    economic_delegation = (
        "- Apply the session-scoped cost-aware delegation policy in "
        "`Framework/Workflow/Rules/runtime-compatibility.md`. On the first eligible task in this session, "
        "ask once whether to use a lower-cost host candidate and which candidate to reuse; retain that choice "
        "only for this session. If the user revokes it, do not ask or delegate again in this session.\n"
        "- An eligible task is repeatable, independent, read-only, non-interactive, and returns only a "
        "discardable candidate artifact. The parent task must validate it before any artifact write or "
        "Citation Gate use.\n"
        "- Never delegate writing, review, Citation Gate work, bibliography or project changes, or workflow "
        "orchestration to the lower-cost candidate. If it is unavailable or insufficient, retain the current "
        "session model rather than selecting another candidate automatically. Do not claim a lower-cost "
        "candidate is optimal without host-provided evidence.\n"
    )
    return (
        "## Codex Runtime Adapter\n\n"
        f"- Treat `phil:{item['id']}` and `$source-command-{item['id']}` as the same public workflow.\n"
        "- Resolve project guidance in this order: `PROJECT.md`, `AGENTS.md`, then `CLAUDE.md`.\n"
        "- Normalize `claude-led` and `codex-led` to `assistant-led`, report the alias as deprecated, and use "
        "`[AI 补全]` for new disclosures.\n"
        f"{role_line}{delegation}{economic_delegation}"
        "- Apply the capability and Zotero degradation rules in `Framework/Workflow/Rules/runtime-compatibility.md`.\n"
    )


def render_root_guide(template: str, runtime: str) -> str:
    if runtime == "claude":
        guide_file = "CLAUDE.md"
        runtime_name = "Claude Code"
        adapter_note = (
            "Claude adapter: use `/phil:<name>` commands from `.claude/commands/`; generated skills and "
            "roles live under `.claude/`."
        )
    else:
        guide_file = "AGENTS.md"
        runtime_name = "Codex"
        adapter_note = (
            "Codex adapter: route `phil:<name>` to `$source-command-<name>` under `.agents/skills/`; "
            "atomic `phil-*` skills remain directly callable."
        )
    rendered = template.replace("{{GUIDE_FILE}}", guide_file).replace("{{RUNTIME_NAME}}", runtime_name)
    lines = rendered.splitlines()
    lines.insert(1, "")
    lines.insert(2, GENERATED)
    lines.insert(3, f"> {adapter_note}")
    return "\n".join(lines).rstrip() + "\n"


def render_outputs(manifest: dict) -> dict[Path, str | bytes]:
    outputs: dict[Path, str | bytes] = {}
    items = sorted(manifest["items"], key=lambda item: (item["kind"], item["id"]))

    for item in items:
        source = WORKFLOW_ROOT / item["source"]
        metadata, body = split_frontmatter(read_text(source))
        if item["kind"] == "skill":
            content = frontmatter(item["id"], item["description"]) + "\n" + GENERATED + "\n" + body
            for platform_root in (Path(".claude/skills"), Path(".agents/skills")):
                target_dir = platform_root / item["id"]
                add_output(outputs, target_dir / "SKILL.md", content)
                for extra in sorted(source.parent.rglob("*")):
                    if not extra.is_file() or extra.name == "SKILL.md":
                        continue
                    relative = extra.relative_to(source.parent)
                    raw = extra.read_bytes()
                    if extra.suffix.lower() == ".md":
                        raw = generated_markdown(raw.decode("utf-8")).encode("utf-8")
                    add_output(outputs, target_dir / relative, raw)
        elif item["kind"] == "workflow":
            claude_content = (
                f"---\ndescription: {yaml_string(item['description'])}\n---\n\n{GENERATED}\n{body}"
            )
            add_output(outputs, Path(".claude/commands") / f"{item['id']}.md", claude_content)
            codex_content = (
                frontmatter(f"source-command-{item['id']}", item["description"])
                + "\n"
                + GENERATED
                + "\n\n"
                + codex_workflow_preamble(item)
                + "\n"
                + body
            )
            add_output(
                outputs,
                Path(".agents/skills") / f"source-command-{item['id']}" / "SKILL.md",
                codex_content,
            )
        elif item["kind"] == "role":
            capabilities = set(item["capabilities"])
            tools = ["Read", "Grep", "Glob"]
            if "write" in capabilities:
                tools.extend(["Write", "Edit"])
            if "delegate" in capabilities:
                tools.append("Agent")
            role_frontmatter = (
                "---\n"
                f"description: {yaml_string(item['description'])}\n"
                "namespace: phil\n"
                f"tools: {', '.join(tools)}\n"
                "---\n"
            )
            add_output(
                outputs,
                Path(".claude/agents") / f"{item['id']}.md",
                role_frontmatter + "\n" + GENERATED + "\n" + body,
            )

    for rule in sorted((WORKFLOW_ROOT / "Rules").glob("*.md")):
        add_output(outputs, Path(".claude/rules") / rule.name, generated_markdown(read_text(rule)))

    root_template = read_text(WORKFLOW_ROOT / "Templates/Root/root-guidance.md")
    add_output(outputs, Path("CLAUDE.md"), render_root_guide(root_template, "claude"))
    add_output(outputs, Path("AGENTS.md"), render_root_guide(root_template, "codex"))
    render_project_bridges(outputs, manifest)
    return outputs


def bridge_body(target: str, runtime: str, kind: str, name: str | None = None, description: str | None = None) -> str:
    runtime_root = ".claude" if runtime == "claude" else ".agents/skills"
    metadata = ""
    if runtime == "codex":
        metadata = frontmatter(name or "nested-project-bridge", description or "Generated bridge to the outer workflow source") + "\n"
    return metadata + (
        f"{GENERATED}\n"
        "\n"
        "## External Workflow Bridge\n\n"
        "This is a generated bridge for a nested project repository. Do not treat the nested "
        "repository as a separate skill source and do not copy skill content here. Locate the "
        "nearest ancestor containing both `Framework/Workflow/` and the outer runtime adapter, "
        "then read the corresponding authoritative file below.\n\n"
        f"- Runtime: `{runtime}`\n"
        f"- Authoritative path: `<outer-root>/{runtime_root}/{target}`\n"
        f"- Artifact kind: `{kind}`\n\n"
        "If no such ancestor can be found, stop and report that the outer workflow root is unavailable; "
        "never silently fall back to a local copy.\n"
    )


def nested_root_guide(runtime: str) -> str:
    guide = "CLAUDE.md" if runtime == "claude" else "AGENTS.md"
    entry = "/phil:<name>" if runtime == "claude" else "$source-command-<name>"
    return (
        f"# Nested Project {runtime.title()} Adapter\n\n"
        f"{GENERATED}\n\n"
        "This repository is the private content layer and is not an independent workflow source. "
        "Read the nearest ancestor `PROJECT.md` first, then locate the nearest ancestor containing "
        "both `Framework/Workflow/` and the outer runtime adapters.\n\n"
        f"Route `phil:<name>` to the outer `{entry}` entry. If the outer workflow root cannot be found, "
        "stop with an explicit error instead of using a local copy.\n"
    )


def render_project_bridges(outputs: dict[Path, str | bytes], manifest: dict) -> None:
    """Generate thin bridges in the inner private repository when it exists."""
    private_root = REPO_ROOT / "Private"
    if not private_root.is_dir():
        return
    render_bridge_set(outputs, Path("Private"), manifest, include_root_guides=True)
    for project in sorted((private_root / "Projects").glob("*")):
        if project.is_dir() and (project / "PROJECT.md").is_file():
            render_bridge_set(
                outputs,
                project.relative_to(REPO_ROOT),
                manifest,
                include_root_guides=True,
            )


def render_bridge_set(
    outputs: dict[Path, str | bytes],
    prefix: Path,
    manifest: dict,
    include_root_guides: bool = False,
) -> None:
    if include_root_guides:
        add_output(outputs, prefix / "AGENTS.md", nested_root_guide("codex"))
        # Preserve an existing project-specific CLAUDE.md; the bridge is generated
        # under .claude/commands and does not need to replace local guidance.
        if prefix == Path("Private"):
            add_output(outputs, prefix / "CLAUDE.md", nested_root_guide("claude"))
    for item in sorted(manifest["items"], key=lambda entry: (entry["kind"], entry["id"])):
        item_id = item["id"]
        if item["kind"] == "skill":
            add_output(outputs, prefix / ".agents/skills" / item_id / "SKILL.md", bridge_body(
                f"{item_id}/SKILL.md", "codex", "skill", item_id, item["description"]
            ))
            add_output(outputs, prefix / ".claude/skills" / item_id / "SKILL.md", bridge_body(
                f"{item_id}/SKILL.md", "claude", "skill", item_id, item["description"]
            ))
        elif item["kind"] == "workflow":
            add_output(outputs, prefix / ".agents/skills" / f"source-command-{item_id}" / "SKILL.md", bridge_body(
                f"source-command-{item_id}/SKILL.md", "codex", "workflow", f"source-command-{item_id}", item["description"]
            ))
            add_output(outputs, prefix / ".claude/commands" / f"{item_id}.md", bridge_body(
                f"commands/{item_id}.md", "claude", "workflow", item_id, item["description"]
            ))
        elif item["kind"] == "role":
            add_output(outputs, prefix / ".claude/agents" / f"{item_id}.md", bridge_body(
                f"agents/{item_id}.md", "claude", "role", item_id, item["description"]
            ))


def managed_roots() -> tuple[Path, ...]:
    return (
        Path(".claude/skills"),
        Path(".claude/commands"),
        Path(".claude/agents"),
        Path(".claude/rules"),
        Path(".agents/skills"),
    )


def actual_managed_files() -> set[Path]:
    files: set[Path] = {Path("CLAUDE.md"), Path("AGENTS.md")}
    for root in managed_roots():
        absolute = REPO_ROOT / root
        if absolute.exists():
            files.update(path.relative_to(REPO_ROOT) for path in absolute.rglob("*") if path.is_file())
    return files


def actual_project_bridge_files() -> set[Path]:
    private_root = REPO_ROOT / "Private"
    if not private_root.is_dir():
        return set()
    files: set[Path] = set()
    prefixes = [private_root]
    projects = private_root / "Projects"
    if projects.is_dir():
        prefixes.extend(path for path in projects.iterdir() if path.is_dir() and (path / "PROJECT.md").is_file())
    for prefix in prefixes:
        files.add((prefix / "AGENTS.md").relative_to(REPO_ROOT))
        if prefix == private_root:
            files.add((prefix / "CLAUDE.md").relative_to(REPO_ROOT))
        for root in (".claude/skills", ".claude/commands", ".claude/agents", ".agents/skills"):
            absolute = prefix / root
            if absolute.exists():
                files.update(path.relative_to(REPO_ROOT) for path in absolute.rglob("*") if path.is_file())
    return files


def check(outputs: dict[Path, str | bytes]) -> int:
    failures: list[str] = []
    expected_files = set(outputs)
    for relative, expected in outputs.items():
        path = REPO_ROOT / relative
        expected_bytes = expected.encode("utf-8") if isinstance(expected, str) else expected
        if not path.is_file():
            failures.append(f"missing {relative.as_posix()}")
        elif path.read_bytes().replace(b"\r\n", b"\n") != expected_bytes.replace(b"\r\n", b"\n"):
            failures.append(f"stale {relative.as_posix()}")
    for extra in sorted(actual_managed_files() - expected_files):
        failures.append(f"unexpected {extra.as_posix()}")
    for extra in sorted(actual_project_bridge_files() - expected_files):
        failures.append(f"unexpected {extra.as_posix()}")
    if failures:
        print("Adapter check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Adapter check passed: {len(outputs)} files are current.")
    return 0


def write(outputs: dict[Path, str | bytes]) -> None:
    for root in managed_roots():
        absolute = (REPO_ROOT / root).resolve()
        if REPO_ROOT.resolve() not in absolute.parents:
            raise RuntimeError(f"refusing to remove path outside repository: {absolute}")
        if absolute.exists():
            shutil.rmtree(absolute)
    private_root = REPO_ROOT / "Private"
    if private_root.is_dir():
        prefixes = [private_root]
        projects = private_root / "Projects"
        if projects.is_dir():
            prefixes.extend(path for path in projects.iterdir() if path.is_dir() and (path / "PROJECT.md").is_file())
        for prefix in prefixes:
            for root in (".claude/skills", ".claude/commands", ".claude/agents", ".agents/skills"):
                absolute = (prefix / root).resolve()
                if private_root.resolve() not in absolute.parents:
                    raise RuntimeError(f"refusing to remove path outside private repository: {absolute}")
                if absolute.exists():
                    shutil.rmtree(absolute)
    for relative, content in sorted(outputs.items(), key=lambda pair: pair[0].as_posix()):
        path = REPO_ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"Generated {len(outputs)} adapter files.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify generated adapters without writing")
    args = parser.parse_args()
    try:
        manifest = load_manifest()
        outputs = render_outputs(manifest)
    except (ManifestError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    if args.check:
        return check(outputs)
    write(outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
