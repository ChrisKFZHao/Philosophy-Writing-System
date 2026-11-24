#!/usr/bin/env python3
"""Maintain the persistent, project-local idea ledger."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


EVENTS = {"new-evidence", "related-objection", "scope-change", "argument-stall", "defect-resolved", "alternative-failed", "user-request"}
STATUSES = {"active", "parked", "rejected", "superseded"}
PROVENANCE = {"user", "ai-completion", "joint"}
HISTORY_FIELDS = {"from_status", "to_status", "from_reason", "superseded_by", "at"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def project_name(project_dir: Path) -> str:
    return project_dir.resolve().name


def ledger_path(project_dir: Path) -> Path:
    return project_dir / f"{project_name(project_dir)}-idea-ledger.json"


def empty_ledger(project_dir: Path) -> dict:
    return {"schema_version": 1, "project": project_name(project_dir), "next_id": 1, "ideas": []}


def load(project_dir: Path) -> dict:
    path = ledger_path(project_dir)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else empty_ledger(project_dir)


def save(project_dir: Path, ledger: dict) -> None:
    errors = validate(ledger, project_name(project_dir))
    if errors:
        raise ValueError("invalid idea ledger: " + "; ".join(errors))
    project_dir.mkdir(parents=True, exist_ok=True)
    target = ledger_path(project_dir)
    temp = target.with_name(target.name + ".tmp")
    try:
        temp.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temp, target)
    except BaseException:
        temp.unlink(missing_ok=True)
        raise


def normalized(statement: str) -> str:
    return " ".join(statement.casefold().split())


def valid_strings(values: object, maximum: int | None = None) -> bool:
    if not isinstance(values, list):
        return False
    if maximum is not None and len(values) > maximum:
        return False
    return all(isinstance(value, str) and value.strip() for value in values)


def valid_triggers(triggers: object) -> bool:
    if not isinstance(triggers, list) or len(triggers) > 3:
        return False
    return all(
        isinstance(trigger, dict)
        and set(trigger) == {"event", "description"}
        and trigger.get("event") in EVENTS
        and isinstance(trigger.get("description"), str)
        and trigger["description"].strip()
        for trigger in triggers
    )


def validate(ledger: dict, expected_project: str | None = None) -> list[str]:
    errors = []
    if not isinstance(ledger, dict):
        return ["ledger must be an object"]
    required_top = {"schema_version", "project", "next_id", "ideas"}
    if set(ledger) != required_top:
        errors.append("invalid ledger fields")
    if ledger.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(ledger.get("project"), str) or not ledger.get("project"):
        errors.append("project is required")
    if expected_project and ledger.get("project") != expected_project:
        errors.append("project does not match directory")
    if not isinstance(ledger.get("next_id"), int) or ledger["next_id"] < 1:
        errors.append("next_id must be positive")
    ideas = ledger.get("ideas")
    if not isinstance(ideas, list):
        return errors + ["ideas must be a list"]
    ids = set()
    required_idea = {
        "id", "statement", "status", "provenance", "status_reason",
        "revival_triggers", "keywords", "related_bib_keys", "superseded_by",
        "created_at", "updated_at", "last_surfaced_at", "last_surfaced_reason",
    }
    allowed_idea = required_idea | {"status_history"}
    for idea in ideas:
        if not isinstance(idea, dict):
            errors.append("idea must be an object")
            continue
        if not required_idea <= set(idea) or not set(idea) <= allowed_idea:
            errors.append("invalid idea fields")
        identifier = idea.get("id", "")
        if (
            not isinstance(identifier, str)
            or not identifier.startswith("IDEA-")
            or len(identifier[5:]) < 3
            or not identifier[5:].isdigit()
        ):
            errors.append("invalid idea id")
        if identifier in ids:
            errors.append("duplicate idea id")
        ids.add(identifier)
        if not isinstance(idea.get("statement"), str) or not idea["statement"].strip():
            errors.append(f"{identifier}: statement is required")
        if idea.get("status") not in STATUSES:
            errors.append(f"{identifier}: invalid status")
        if idea.get("provenance") not in PROVENANCE:
            errors.append(f"{identifier}: invalid provenance")
        triggers = idea.get("revival_triggers", [])
        if not valid_triggers(triggers):
            errors.append(f"{identifier}: invalid revival triggers")
        if not valid_strings(idea.get("keywords"), 5):
            errors.append(f"{identifier}: invalid keywords")
        if not valid_strings(idea.get("related_bib_keys")):
            errors.append(f"{identifier}: invalid related_bib_keys")
        if not isinstance(idea.get("status_reason"), str):
            errors.append(f"{identifier}: invalid status_reason")
        for field in ("created_at", "updated_at"):
            if not isinstance(idea.get(field), str) or not idea[field]:
                errors.append(f"{identifier}: invalid {field}")
        for field in ("last_surfaced_at", "last_surfaced_reason"):
            if idea.get(field) is not None and not isinstance(idea[field], str):
                errors.append(f"{identifier}: invalid {field}")
        history = idea.get("status_history")
        if history is not None:
            if not isinstance(history, list):
                errors.append(f"{identifier}: invalid status_history")
            else:
                for entry in history:
                    if not isinstance(entry, dict) or set(entry) != HISTORY_FIELDS:
                        errors.append(f"{identifier}: invalid status_history entry")
                        continue
                    if entry["from_status"] not in STATUSES or entry["to_status"] not in STATUSES:
                        errors.append(f"{identifier}: invalid status_history entry")
                    if not isinstance(entry["from_reason"], str):
                        errors.append(f"{identifier}: invalid status_history entry")
                    if entry["superseded_by"] is not None and not isinstance(entry["superseded_by"], str):
                        errors.append(f"{identifier}: invalid status_history entry")
                    if not isinstance(entry["at"], str) or not entry["at"]:
                        errors.append(f"{identifier}: invalid status_history entry")
    # Permit a valid reference to an idea defined later in the ledger.
    for idea in ideas:
        if not isinstance(idea, dict):
            continue
        if idea.get("status") != "superseded":
            if idea.get("superseded_by") is not None:
                errors.append(f"{idea.get('id', '')}: superseded_by must be null outside superseded status")
            continue
        replacement = idea.get("superseded_by")
        if not isinstance(replacement, str) or replacement == idea.get("id") or replacement not in ids:
            errors.append(f"{idea.get('id', '')}: invalid superseded_by")
    return errors


def record(ledger: dict, statement: str, provenance: str, status: str, reason: str, keywords: list[str], bib_keys: list[str], triggers: list[dict], user_confirmed: bool = False) -> tuple[dict, bool]:
    if not isinstance(statement, str) or not statement.strip():
        raise ValueError("statement is required")
    if provenance not in PROVENANCE or status not in STATUSES:
        raise ValueError("invalid provenance or status")
    if status == "superseded":
        raise ValueError("an initial idea cannot be superseded")
    if status == "active" and not user_confirmed:
        raise ValueError("recording an active idea requires --user-confirmed")
    if not isinstance(reason, str):
        raise ValueError("reason must be a string")
    if not valid_strings(keywords, 5):
        raise ValueError("invalid keywords")
    if not valid_strings(bib_keys):
        raise ValueError("invalid bibliography keys")
    if not valid_triggers(triggers):
        raise ValueError("invalid revival triggers")
    wanted = normalized(statement)
    for idea in ledger["ideas"]:
        if normalized(idea["statement"]) == wanted:
            return idea, False
    timestamp = now()
    idea = {
        "id": f"IDEA-{ledger['next_id']:03d}",
        "statement": statement.strip(),
        "status": status,
        "provenance": provenance,
        "status_reason": reason,
        "revival_triggers": triggers,
        "keywords": keywords,
        "related_bib_keys": bib_keys,
        "superseded_by": None,
        "created_at": timestamp,
        "updated_at": timestamp,
        "last_surfaced_at": None,
        "last_surfaced_reason": None,
    }
    ledger["ideas"].append(idea)
    ledger["next_id"] += 1
    return idea, True


def transition(ledger: dict, identifier: str, status: str, reason: str, user_confirmed: bool, superseded_by: str | None) -> dict:
    if status not in STATUSES:
        raise ValueError("invalid status")
    if not isinstance(reason, str):
        raise ValueError("reason must be a string")
    if status == "active" and not user_confirmed:
        raise ValueError("transition to active requires --user-confirmed")
    idea = next((item for item in ledger["ideas"] if item["id"] == identifier), None)
    if not idea:
        raise ValueError("idea not found")
    if status == "superseded":
        known_ids = {item["id"] for item in ledger["ideas"]}
        if not isinstance(superseded_by, str) or superseded_by == identifier or superseded_by not in known_ids:
            raise ValueError("superseded_by must name a different existing idea")
    elif superseded_by is not None:
        raise ValueError("superseded_by is only valid for superseded status")
    timestamp = now()
    idea.setdefault("status_history", []).append({
        "from_status": idea["status"],
        "to_status": status,
        "from_reason": idea["status_reason"],
        "superseded_by": idea["superseded_by"],
        "at": timestamp,
    })
    idea["status"] = status
    idea["status_reason"] = reason
    idea["superseded_by"] = superseded_by if status == "superseded" else None
    idea["updated_at"] = timestamp
    return idea


def mark_surfaced(ledger: dict, identifier: str, reason: str) -> dict:
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("surface reason is required")
    idea = next((item for item in ledger["ideas"] if item["id"] == identifier), None)
    if not idea:
        raise ValueError("idea not found")
    timestamp = now()
    idea["last_surfaced_at"] = timestamp
    idea["last_surfaced_reason"] = reason
    idea["updated_at"] = timestamp
    return idea


def candidates(ledger: dict, event: str, keywords: list[str], bib_keys: list[str]) -> list[dict]:
    if event not in EVENTS:
        raise ValueError("invalid event")
    wanted_words = {normalized(item) for item in keywords}
    wanted_keys = {item.strip() for item in bib_keys}
    result = []
    for idea in ledger["ideas"]:
        if idea["status"] == "active":
            continue
        if event != "user-request" and not any(item["event"] == event for item in idea["revival_triggers"]):
            continue
        if idea["status"] == "rejected" and event not in {"defect-resolved", "user-request"}:
            continue
        if idea["status"] == "superseded" and event not in {"alternative-failed", "user-request"}:
            continue
        overlap = (
            wanted_words.intersection(normalized(item) for item in idea["keywords"])
            or wanted_keys.intersection(idea["related_bib_keys"])
        )
        if overlap:
            result.append(idea)
        if len(result) == 2:
            break
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True, type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    record_parser = sub.add_parser("record")
    record_parser.add_argument("--statement", required=True)
    record_parser.add_argument("--provenance", required=True, choices=sorted(PROVENANCE))
    record_parser.add_argument("--status", default="parked", choices=sorted(STATUSES))
    record_parser.add_argument("--reason", default="")
    record_parser.add_argument("--keyword", action="append", default=[])
    record_parser.add_argument("--bib-key", action="append", default=[])
    record_parser.add_argument("--trigger", action="append", default=[])
    record_parser.add_argument("--user-confirmed", action="store_true")
    transition_parser = sub.add_parser("transition")
    transition_parser.add_argument("id")
    transition_parser.add_argument("--status", required=True, choices=sorted(STATUSES))
    transition_parser.add_argument("--reason", required=True)
    transition_parser.add_argument("--superseded-by")
    transition_parser.add_argument("--user-confirmed", action="store_true")
    candidate_parser = sub.add_parser("candidates")
    candidate_parser.add_argument("--event", required=True, choices=sorted(EVENTS))
    candidate_parser.add_argument("--keyword", action="append", default=[])
    candidate_parser.add_argument("--bib-key", action="append", default=[])
    surfaced_parser = sub.add_parser("mark-surfaced")
    surfaced_parser.add_argument("id")
    surfaced_parser.add_argument("--reason", required=True)
    sub.add_parser("validate")
    args = parser.parse_args()
    try:
        ledger = load(args.project_dir)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    try:
        if args.command == "validate":
            errors = validate(ledger, project_name(args.project_dir))
            print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False))
            return 0 if not errors else 1
        errors = validate(ledger, project_name(args.project_dir))
        if errors:
            raise ValueError("invalid idea ledger: " + "; ".join(errors))
        if args.command == "record":
            triggers = []
            for value in args.trigger:
                event, separator, description = value.partition(":")
                if not separator:
                    raise ValueError("trigger must be EVENT:DESCRIPTION")
                triggers.append({"event": event, "description": description})
            result, changed = record(ledger, args.statement, args.provenance, args.status, args.reason, args.keyword, args.bib_key, triggers, args.user_confirmed)
            if changed:
                save(args.project_dir, ledger)
            print(json.dumps({"idea": result, "idempotent": not changed}, ensure_ascii=False))
        elif args.command == "transition":
            result = transition(ledger, args.id, args.status, args.reason, args.user_confirmed, args.superseded_by)
            save(args.project_dir, ledger)
            print(json.dumps(result, ensure_ascii=False))
        elif args.command == "candidates":
            print(json.dumps(candidates(ledger, args.event, args.keyword, args.bib_key), ensure_ascii=False))
        elif args.command == "mark-surfaced":
            result = mark_surfaced(ledger, args.id, args.reason)
            save(args.project_dir, ledger)
            print(json.dumps(result, ensure_ascii=False))
        else:
            counts = {status: sum(item["status"] == status for item in ledger["ideas"]) for status in sorted(STATUSES)}
            print(json.dumps({"path": str(ledger_path(args.project_dir)), "ideas": len(ledger["ideas"]), "by_status": counts}, ensure_ascii=False))
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
