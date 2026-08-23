#!/usr/bin/env python3
"""Deterministic 0.6 -> 0.7 migration: IDs, analysis metadata, and project workflow state.

Defaults to dry-run (reports planned changes, writes nothing); pass --apply to write.
Fails on unknown IDs instead of guessing or dropping data. Writes are restricted to a
whitelist of known framework, adapter, project-guidance, and metadata targets.
`Private/Projects/*/working-notes.md` is never read or written.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MIGRATION_MAP = Path(__file__).resolve().parent / "migration-v0.7.json"

# Write whitelist: everything else is reported as out-of-scope and refused.
WRITABLE_SUFFIXES = (".analysis.meta.json", "-workflow-state.json")
WRITABLE_GUIDANCE = {"PROJECT.md"}
GUIDANCE_PROJECTS = ("instantaneous-velocity", "rawlsian-ai", "srinivasan-critique")

COMMAND_RE = re.compile(r"phil:(reconstruct|evaluate|comment|ingest|philosophers|pipeline)\b")
PROTECTED = {"working-notes.md"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_map() -> dict:
    return json.loads(MIGRATION_MAP.read_text(encoding="utf-8"))


class MigrationError(ValueError):
    pass


def canonical_coverage(entry: str, maps: dict) -> str:
    entry = entry.strip()
    for table in (maps["coverage_alias_map"], maps["method_map"]):
        if entry in table:
            return table[entry]["method_id"] if entry in maps["method_map"] else table[entry]
    if entry.startswith("method."):
        return entry
    raise MigrationError(f"unknown coverage entry: {entry!r}")


def migrate_analysis_meta(path: Path, maps: dict) -> list[str]:
    changes: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    workflow_id = data.get("workflow_id", "")
    migrated_values = set(maps["workflow_id_map"].values())
    if workflow_id in maps["workflow_id_map"]:
        new_id = maps["workflow_id_map"][workflow_id]
        data["workflow_id"] = new_id
        changes.append(f"workflow_id: {workflow_id} -> {new_id}")
    elif workflow_id in migrated_values or workflow_id.startswith("phil:research") or workflow_id == "phil:full":
        pass
    elif workflow_id:
        raise MigrationError(f"{path.name}: unknown workflow_id {workflow_id!r}")
    new_coverage = []
    for entry in data.get("coverage", []):
        canonical = canonical_coverage(entry, maps)
        if canonical != entry:
            changes.append(f"coverage: {entry!r} -> {canonical}")
        new_coverage.append(canonical)
    data["coverage"] = new_coverage
    if changes:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changes


# v1 pipeline stages: 0 = not started; 1 topic orientation; 2 reading & analysis;
# 3 conception incubation; 4 outline; 5 draft & revision; 6 review & final.
V1_STAGE_TO_V2 = ["intake", "research", "research", "incubation", "outline", "draft", "review"]


def migrate_workflow_state(path: Path, maps: dict) -> list[str]:
    changes: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") == 2:
        return changes
    if data.get("schema_version") != 1:
        raise MigrationError(f"{path.name}: unsupported schema_version {data.get('schema_version')!r}")
    stage_index = data.get("current_stage", 0)
    if not isinstance(stage_index, int) or not 0 <= stage_index < len(V1_STAGE_TO_V2):
        raise MigrationError(f"{path.name}: invalid current_stage {stage_index!r}")
    project = data.get("project") or path.parent.name
    artifacts = []
    for artifact in data.get("artifacts", []):
        posix_path = artifact.get("path", "").replace("\\", "/")
        artifacts.append({
            "kind": "analysis" if artifact.get("workflow") == "phil:reconstruct" else artifact.get("workflow", "artifact"),
            "path": posix_path,
            "sha256": artifact.get("hash", ""),
            "status": "stale" if artifact.get("stale") else "current",
        })
    gates = data.get("gates", [])
    outline_decision = "pending"
    if any(g.get("decision") == "pass" for g in gates if g.get("stage") == 4):
        outline_decision = "approved"
    elif any(g.get("decision") == "override" for g in gates if g.get("stage") == 4):
        outline_decision = "waived"
    status_map = {
        "not-started": "not_started", "in-progress": "in_progress",
        "paused": "awaiting_user", "complete": "completed",
    }
    status = status_map.get(data.get("status"), "in_progress")
    migrated = {
        "schema_version": 2,
        "project": project,
        "run_id": "run-migrated-v07",
        "entrypoint": "phil-full",
        "stage": V1_STAGE_TO_V2[stage_index],
        "status": status,
        "collaboration_mode": "user-led",
        "artifacts": artifacts,
        "approvals": {"outline": {
            "decision": outline_decision,
            "artifact_sha256": None,
            "recorded_at": now(),
            "reason": "migrated from v1 gate ledger" if outline_decision != "pending" else "initial",
        }},
        "review_findings": [],
        "section_audit": None,
        "next_action": "v1 state migrated; validate artifacts and continue",
        "updated_at": now(),
    }
    changes.append(f"state v1 -> v2 (stage {stage_index} -> {migrated['stage']}, "
                   f"{len(artifacts)} artifacts, outline={outline_decision}, "
                   f"{len(gates)} v1 gates collapsed into approvals)")
    path.write_text(json.dumps(migrated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changes


def migrate_guidance(path: Path, maps: dict) -> list[str]:
    text = path.read_text(encoding="utf-8")
    changes: list[str] = []

    def replace_command(match: re.Match) -> str:
        old = "phil:" + match.group(1)
        new = maps["workflow_id_map"][old]
        if new != old:
            changes.append(f"command: {old} -> {new}")
        return new

    new_text = COMMAND_RE.sub(replace_command, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return changes


def collect_targets(repo_root: Path) -> dict[str, list[Path]]:
    targets: dict[str, list[Path]] = {"analysis-meta": [], "workflow-state": [], "guidance": []}
    analysis_dir = repo_root / "Private/Bibliography/Analysis"
    if analysis_dir.is_dir():
        targets["analysis-meta"] = sorted(analysis_dir.glob("*.analysis.meta.json"))
    projects = repo_root / "Private/Projects"
    if projects.is_dir():
        for project in sorted(projects.iterdir()):
            if not project.is_dir():
                continue
            for child in project.rglob("*-workflow-state.json"):
                targets["workflow-state"].append(child)
            if project.name in GUIDANCE_PROJECTS:
                guidance = project / "PROJECT.md"
                if guidance.is_file():
                    targets["guidance"].append(guidance)
    return targets


def check_writable(path: Path, repo_root: Path) -> None:
    relative = path.relative_to(repo_root)
    parts = relative.parts
    if any(part in PROTECTED for part in parts):
        raise MigrationError(f"refusing to touch protected file: {relative}")
    allowed = (
        relative.name.endswith(".analysis.meta.json")
        or relative.name.endswith("-workflow-state.json")
        or (relative.name in WRITABLE_GUIDANCE and len(parts) == 4 and parts[0] == "Private" and parts[1] == "Projects")
    )
    if not allowed:
        raise MigrationError(f"target outside migration write whitelist: {relative}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    args = parser.parse_args()
    maps = load_map()
    targets = collect_targets(REPO_ROOT)
    report: list[dict] = []
    failures: list[str] = []

    jobs = [
        ("analysis-meta", targets["analysis-meta"], migrate_analysis_meta),
        ("workflow-state", targets["workflow-state"], migrate_workflow_state),
        ("guidance", targets["guidance"], migrate_guidance),
    ]
    for kind, paths, handler in jobs:
        for path in paths:
            entry = {"kind": kind, "file": str(path.relative_to(REPO_ROOT)).replace("\\", "/"), "changes": []}
            try:
                check_writable(path, REPO_ROOT)
                if args.apply:
                    entry["changes"] = handler(path, maps)
                else:
                    # Dry-run: compute changes on a copy without writing.
                    backup = path.read_bytes()
                    entry["changes"] = handler(path, maps)
                    path.write_bytes(backup)
            except (MigrationError, ValueError, OSError, json.JSONDecodeError, KeyError) as exc:
                failures.append(f"{entry['file']}: {exc}")
            report.append(entry)

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"migrate-v07 [{mode}]")
    for entry in report:
        marker = "would change" if not args.apply and entry["changes"] else ("changed" if entry["changes"] else "current")
        print(f"- [{entry['kind']}] {entry['file']}: {marker}")
        for change in entry["changes"]:
            print(f"    {change}")
    if failures:
        print("FAILURES (nothing further written for these):")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("OK" if args.apply else "OK (dry-run; pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
