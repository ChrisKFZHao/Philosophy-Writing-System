#!/usr/bin/env python3
"""Maintain project workflow state and artifact freshness."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


STATUSES = {"not-started", "in-progress", "paused", "complete"}
DECISIONS = {"pass", "block", "override"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def project_name(project_dir: Path) -> str:
    return project_dir.resolve().name


def state_path(project_dir: Path) -> Path:
    return project_dir / f"{project_name(project_dir)}-workflow-state.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def empty_state(project_dir: Path) -> dict:
    return {
        "schema_version": 1,
        "project": project_name(project_dir),
        "current_stage": 0,
        "status": "not-started",
        "artifacts": [],
        "gates": [],
        "next_action": None,
    }


def load(project_dir: Path) -> dict:
    path = state_path(project_dir)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else empty_state(project_dir)


def save(project_dir: Path, state: dict) -> None:
    errors = validate(state, project_name(project_dir))
    if errors:
        raise ValueError("invalid workflow state: " + "; ".join(errors))
    project_dir.mkdir(parents=True, exist_ok=True)
    state_path(project_dir).write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def is_safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts and path.as_posix() == value


def refresh_artifacts(project_dir: Path, state: dict) -> bool:
    changed = False
    for artifact in state["artifacts"]:
        if not is_safe_relative_path(artifact.get("path")):
            if artifact.get("stale") is not True:
                artifact["stale"] = True
                changed = True
            continue
        path = project_dir / artifact["path"]
        stale = not path.is_file() or sha256(path) != artifact["hash"]
        if artifact.get("stale") != stale:
            artifact["stale"] = stale
            changed = True
    return changed


def validate(state: dict, expected_project: str | None = None) -> list[str]:
    errors = []
    if not isinstance(state, dict):
        return ["state must be an object"]
    required_top = {"schema_version", "project", "current_stage", "status", "artifacts", "gates", "next_action"}
    if set(state) != required_top:
        errors.append("invalid state fields")
    if state.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(state.get("project"), str) or not state.get("project"):
        errors.append("project is required")
    if expected_project and state.get("project") != expected_project:
        errors.append("project does not match directory")
    if not isinstance(state.get("current_stage"), int) or not 0 <= state["current_stage"] <= 6:
        errors.append("current_stage must be 0 through 6")
    if state.get("status") not in STATUSES:
        errors.append("invalid status")
    if not isinstance(state.get("artifacts"), list):
        errors.append("artifacts must be a list")
    else:
        seen = set()
        for artifact in state["artifacts"]:
            if not isinstance(artifact, dict) or set(artifact) != {"path", "hash", "workflow", "version", "level", "stale"}:
                errors.append("invalid artifact fields")
                continue
            if artifact["path"] in seen:
                errors.append("duplicate artifact path")
            seen.add(artifact["path"])
            if not is_safe_relative_path(artifact["path"]):
                errors.append("invalid artifact path")
            if not isinstance(artifact["hash"], str) or len(artifact["hash"]) != 64 or any(char not in "0123456789abcdef" for char in artifact["hash"]):
                errors.append("invalid artifact hash")
            if not isinstance(artifact["workflow"], str) or not artifact["workflow"]:
                errors.append("invalid artifact workflow")
            if not isinstance(artifact["version"], str) or not artifact["version"]:
                errors.append("invalid artifact version")
            if artifact["level"] is not None and (not isinstance(artifact["level"], (int, float)) or isinstance(artifact["level"], bool) or artifact["level"] < 0):
                errors.append("invalid artifact level")
            if not isinstance(artifact["stale"], bool):
                errors.append("invalid artifact stale")
    gates = state.get("gates")
    if not isinstance(gates, list):
        errors.append("gates must be a list")
    else:
        for gate in gates:
            required_gate = {"stage", "decision", "reason", "recorded_at"}
            if not isinstance(gate, dict) or set(gate) != required_gate or gate.get("decision") not in DECISIONS or not isinstance(gate.get("stage"), int) or not 0 <= gate["stage"] <= 6 or not isinstance(gate.get("reason"), str) or not isinstance(gate.get("recorded_at"), str):
                errors.append("invalid gate")
    if state.get("next_action") is not None and not isinstance(state.get("next_action"), str):
        errors.append("invalid next_action")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True, type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    sub.add_parser("validate")
    update = sub.add_parser("update-stage")
    update.add_argument("--stage", required=True, type=int, choices=range(7))
    update.add_argument("--status", choices=sorted(STATUSES))
    update.add_argument("--next-action")
    gate = sub.add_parser("record-gate")
    gate.add_argument("--stage", required=True, type=int, choices=range(7))
    gate.add_argument("--decision", required=True, choices=sorted(DECISIONS))
    gate.add_argument("--reason", required=True)
    artifact = sub.add_parser("register-artifact")
    artifact.add_argument("--path", required=True)
    artifact.add_argument("--workflow", required=True)
    artifact.add_argument("--version", required=True)
    artifact.add_argument("--level", type=float)
    args = parser.parse_args()
    state = load(args.project_dir)
    try:
        if args.command == "validate":
            errors = validate(state, project_name(args.project_dir))
            print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False))
            return 0 if not errors else 1
        errors = validate(state, project_name(args.project_dir))
        if errors:
            raise ValueError("invalid workflow state: " + "; ".join(errors))
        changed = refresh_artifacts(args.project_dir, state)
        if args.command == "init":
            if not state_path(args.project_dir).exists():
                save(args.project_dir, state)
            print(json.dumps(state, ensure_ascii=False))
        elif args.command == "status":
            if changed:
                save(args.project_dir, state)
            print(json.dumps(state, ensure_ascii=False))
        elif args.command == "update-stage":
            state["current_stage"] = args.stage
            if args.status: state["status"] = args.status
            if args.next_action is not None: state["next_action"] = args.next_action
            save(args.project_dir, state)
            print(json.dumps(state, ensure_ascii=False))
        elif args.command == "record-gate":
            state["gates"].append({
                "stage": args.stage,
                "decision": args.decision,
                "reason": args.reason,
                "recorded_at": now(),
            })
            save(args.project_dir, state)
            print(json.dumps(state["gates"][-1], ensure_ascii=False))
        elif args.command == "register-artifact":
            relative = Path(args.path)
            if not is_safe_relative_path(args.path):
                raise ValueError("artifact path must be relative to project directory")
            target = args.project_dir / relative
            if not target.is_file():
                raise ValueError("artifact file does not exist")
            item = {
                "path": relative.as_posix(),
                "hash": sha256(target),
                "workflow": args.workflow,
                "version": args.version,
                "level": args.level,
                "stale": False,
            }
            state["artifacts"] = [
                existing for existing in state["artifacts"]
                if existing["path"] != item["path"]
            ] + [item]
            save(args.project_dir, state)
            print(json.dumps(item, ensure_ascii=False))
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
