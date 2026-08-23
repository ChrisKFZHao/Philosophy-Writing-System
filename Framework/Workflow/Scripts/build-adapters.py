#!/usr/bin/env python3
"""Generate Claude Code and Codex adapters from the neutral framework layer (manifest v2).

Exposure rule: only `skill` items are generated as runtime skills (exactly the four
public skills in manifest.exposure.skills). `method`, `method_package`, and `service`
items never become runtime skills or adapters. Claude additionally receives thin
command wrappers (delegation only, never canonical definitions) for the commands in
manifest.exposure.claude_command_wrappers.
"""

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
KINDS = {"skill", "method_package", "method", "service", "command"}
PLATFORMS = {"claude", "codex"}
CAPABILITIES = {
    "read", "search", "write", "delegate", "pdf", "zotero-full", "zotero-local",
}
METHOD_ID_PATTERN = re.compile(r"^method\.[a-z0-9-]+\.[a-z0-9-]+$")


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
    if set(data) != {"schema_version", "exposure", "migration_map", "items"}:
        raise ManifestError("manifest top level must contain schema_version, exposure, migration_map, items")
    if data["schema_version"] != 2 or not isinstance(data["items"], list):
        raise ManifestError("unsupported manifest schema")

    exposure = data["exposure"]
    if set(exposure) != {"skills", "claude_command_wrappers"}:
        raise ManifestError("invalid exposure fields")

    ids: dict[str, dict] = {}
    sources: set[str] = set()
    for item in data["items"]:
        item_id = item.get("id")
        if not re.fullmatch(r"[a-z0-9.-]+", item_id or ""):
            raise ManifestError(f"invalid id: {item_id}")
        if item_id in ids:
            raise ManifestError(f"duplicate id: {item_id}")
        if item["kind"] not in KINDS:
            raise ManifestError(f"invalid kind for {item_id}")
        if not item.get("description") or not isinstance(item["description"], str):
            raise ManifestError(f"missing description for {item_id}")
        ids[item_id] = item

    for item in data["items"]:
        kind, item_id = item["kind"], item["id"]
        if kind == "skill":
            if set(item) != {"id", "kind", "source", "description", "modes", "capabilities", "platforms"}:
                raise ManifestError(f"invalid skill fields for {item_id}")
            if set(item["platforms"]) - PLATFORMS:
                raise ManifestError(f"unknown platform for {item_id}")
            if set(item["capabilities"]) - CAPABILITIES:
                raise ManifestError(f"unknown capability for {item_id}")
        elif kind == "method_package":
            if set(item) != {"id", "kind", "source", "description", "members"}:
                raise ManifestError(f"invalid method_package fields for {item_id}")
            if not item["source"].endswith("/"):
                raise ManifestError(f"method_package source must be a directory: {item_id}")
        elif kind == "method":
            required = {"id", "kind", "package", "source", "description", "legacy_ids", "label", "consumers", "selector", "inputs", "outputs", "side_effect_policy"}
            if set(item) != required:
                raise ManifestError(f"invalid method fields for {item_id}")
            if not METHOD_ID_PATTERN.match(item_id):
                raise ManifestError(f"method id must match method.<package>.<slug>: {item_id}")
        elif kind == "service":
            if set(item) != {"id", "kind", "source", "description", "consumers", "authority"}:
                raise ManifestError(f"invalid service fields for {item_id}")
        elif kind == "command":
            if set(item) != {"id", "kind", "source", "description", "modes", "stages", "consumers"}:
                raise ManifestError(f"invalid command fields for {item_id}")

    for item in data["items"]:
        kind, item_id = item["kind"], item["id"]
        if kind in {"skill", "method", "service", "command"}:
            source = WORKFLOW_ROOT / item["source"]
            if not source.is_file():
                raise ManifestError(f"missing source for {item_id}: {item['source']}")
            if item["source"] in sources:
                raise ManifestError(f"duplicate source: {item['source']}")
            sources.add(item["source"])
        else:
            directory = WORKFLOW_ROOT / item["source"]
            if not directory.is_dir():
                raise ManifestError(f"missing package directory for {item_id}: {item['source']}")

    for item in data["items"]:
        if item["kind"] == "method_package":
            for member in item["members"]:
                if member not in ids or ids[member]["kind"] != "method":
                    raise ManifestError(f"unknown member {member} in {item['id']}")
                if ids[member]["package"] != item["id"]:
                    raise ManifestError(f"member {member} declares package {ids[member]['package']}, not {item['id']}")
        if item["kind"] == "method":
            if item["package"] not in ids or ids[item["package"]]["kind"] != "method_package":
                raise ManifestError(f"unknown package {item['package']} in {item['id']}")
            if item["id"] not in ids[item["package"]]["members"]:
                raise ManifestError(f"method {item['id']} missing from its package member list")
            for legacy in item["legacy_ids"]:
                if not legacy.startswith("phil-"):
                    raise ManifestError(f"legacy id must be a v0.6 skill id: {legacy}")

    skill_ids = {i["id"] for i in data["items"] if i["kind"] == "skill"}
    if set(exposure["skills"]) != skill_ids:
        raise ManifestError(f"exposure.skills must list exactly the skill items: {sorted(skill_ids)}")
    command = [i for i in data["items"] if i["kind"] == "command"]
    if len(command) != 1:
        raise ManifestError("exactly one command item is expected")
    if set(command[0]["consumers"]) - skill_ids:
        raise ManifestError("command consumers must be skill ids")
    for item in data["items"]:
        for consumer in item.get("consumers", []):
            owner = consumer.split("/", 1)[0]
            if owner not in skill_ids and owner != command[0]["id"]:
                raise ManifestError(f"unknown consumer {consumer} in {item['id']}")

    migration = WORKFLOW_ROOT / data["migration_map"]
    if not migration.is_file():
        raise ManifestError(f"missing migration map: {data['migration_map']}")
    return data


def inventory(manifest: dict) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in manifest["items"]:
        counts[item["kind"]] = counts.get(item["kind"], 0) + 1
    return counts


def add_output(outputs: dict[Path, str | bytes], path: Path, content: str | bytes) -> None:
    if path in outputs:
        raise ManifestError(f"output collision: {path}")
    outputs[path] = content


def generated_markdown(text: str) -> str:
    return f"{GENERATED}\n{text.lstrip()}"


CLAUDE_WRAPPERS = {
    "research": ("phil-research", "Route to the `phil-research` skill with the requested mode (ingest / reconstruct / evaluate / comment / philosophers)."),
    "tutor": ("phil-tutor", "Route to the `phil-tutor` skill (reading / incubating)."),
    "write": ("phil-write", "Route to the `phil-write` skill (outline / draft / revision)."),
    "review": ("phil-review", "Route to the `phil-review` skill (full / targeted / re-review)."),
    "full": (None, "Read `Framework/Workflow/Commands/phil-full.md` and execute the pipeline state machine (start / status / resume)."),
}


def render_claude_wrapper(name: str) -> str:
    skill, instruction = CLAUDE_WRAPPERS[name]
    body = (
        f"## Delegation only\n\n"
        f"{instruction}\n\n"
        "This wrapper is not a canonical definition. The authoritative contract is "
        + (
            f"`Framework/Workflow/Skills/{skill}/SKILL.md`."
            if skill
            else "`Framework/Workflow/Commands/phil-full.md`."
        )
        + " Do not copy or specialize its content here.\n"
    )
    return (
        f"---\ndescription: {yaml_string('phil:' + name + ' — thin delegation wrapper')}\n---\n\n"
        + GENERATED + "\n" + body
    )


def render_root_guide(template: str, runtime: str, manifest: dict) -> str:
    if runtime == "claude":
        guide_file = "CLAUDE.md"
        runtime_name = "Claude Code"
        adapter_note = (
            "Claude adapter: `/phil:<name>` maps to the thin command wrappers in `.claude/commands/` "
            "(research, tutor, write, review, full), which delegate to the four generated skills under `.claude/skills/`."
        )
    else:
        guide_file = "AGENTS.md"
        runtime_name = "Codex"
        adapter_note = (
            "Codex adapter: route `phil:<name>` to the matching generated skill under `.agents/skills/` "
            "(phil-research, phil-tutor, phil-write, phil-review); `phil:full` executes the command "
            "specification `Framework/Workflow/Commands/phil-full.md`."
        )
    rendered = template.replace("{{GUIDE_FILE}}", guide_file).replace("{{RUNTIME_NAME}}", runtime_name)
    lines = rendered.splitlines()
    lines.insert(1, "")
    lines.insert(2, GENERATED)
    lines.insert(3, f"> {adapter_note}")
    return "\n".join(lines).rstrip() + "\n"


def render_outputs(manifest: dict) -> dict[Path, str | bytes]:
    outputs: dict[Path, str | bytes] = {}
    skills = {item["id"]: item for item in manifest["items"] if item["kind"] == "skill"}

    for item_id in sorted(skills):
        item = skills[item_id]
        source = WORKFLOW_ROOT / item["source"]
        _, body = split_frontmatter(read_text(source))
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

    for name in manifest["exposure"]["claude_command_wrappers"]:
        if name not in CLAUDE_WRAPPERS:
            raise ManifestError(f"unknown claude wrapper: {name}")
        add_output(outputs, Path(".claude/commands") / f"{name}.md", render_claude_wrapper(name))

    for rule in sorted((WORKFLOW_ROOT / "Rules").glob("*.md")):
        add_output(outputs, Path(".claude/rules") / rule.name, generated_markdown(read_text(rule)))

    root_template = read_text(WORKFLOW_ROOT / "Templates/Root/root-guidance.md")
    add_output(outputs, Path("CLAUDE.md"), render_root_guide(root_template, "claude", manifest))
    add_output(outputs, Path("AGENTS.md"), render_root_guide(root_template, "codex", manifest))
    render_project_bridges(outputs, manifest)
    return outputs


def bridge_body(target: str, runtime: str, kind: str, name: str | None = None, description: str | None = None) -> str:
    runtime_root = ".claude/skills" if runtime == "claude" else ".agents/skills"
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
    if runtime == "claude":
        entry = "the outer `/phil:<name>` command wrapper in `.claude/commands/`"
    else:
        entry = "the outer generated skill under `.agents/skills/` (`phil-research`, `phil-tutor`, `phil-write`, `phil-review`)"
    return (
        f"# Nested Project {runtime.title()} Adapter\n\n"
        f"{GENERATED}\n\n"
        "This repository is the private content layer and is not an independent workflow source. "
        "Read the nearest ancestor `PROJECT.md` first, then locate the nearest ancestor containing "
        "both `Framework/Workflow/` and the outer runtime adapters.\n\n"
        f"Route `phil:<name>` to {entry}; `phil:full` executes the outer "
        "`Framework/Workflow/Commands/phil-full.md` specification. If the outer workflow root cannot "
        "be found, stop with an explicit error instead of using a local copy.\n"
    )


def render_project_bridges(outputs: dict[Path, str | bytes], manifest: dict) -> None:
    """Generate thin bridges in the inner private repository when it exists."""
    private_root = REPO_ROOT / "Private"
    if not private_root.is_dir():
        return
    render_bridge_set(outputs, Path("Private"), manifest, include_root_guides=True)
    for project in sorted((private_root / "Projects").glob("*")):
        if project.is_dir() and (project / "PROJECT.md").is_file():
            render_bridge_set(outputs, project.relative_to(REPO_ROOT), manifest, include_root_guides=True)


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
    skills = [item for item in manifest["items"] if item["kind"] == "skill"]
    for item in sorted(skills, key=lambda entry: entry["id"]):
        item_id = item["id"]
        add_output(outputs, prefix / ".agents/skills" / item_id / "SKILL.md", bridge_body(
            f"{item_id}/SKILL.md", "codex", "skill", item_id, item["description"]
        ))
        add_output(outputs, prefix / ".claude/skills" / item_id / "SKILL.md", bridge_body(
            f"{item_id}/SKILL.md", "claude", "skill", item_id, item["description"]
        ))
    command = next(item for item in manifest["items"] if item["kind"] == "command")
    add_output(outputs, prefix / ".claude/commands" / "full.md", bridge_body(
        "commands/full.md", "claude", "command", "full", command["description"]
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
    print("Inventory derived from manifest: " + json.dumps(inventory(manifest), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
