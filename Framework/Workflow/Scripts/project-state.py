#!/usr/bin/env python3
"""Maintain project workflow state (schema v2): runs, stages, approvals, findings, freshness."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 2
STATUSES = {"not_started", "in_progress", "awaiting_user", "blocked", "stale", "completed"}
STAGES = [
    "intake", "research", "incubation", "outline", "section_brief", "draft",
    "section_audit", "review", "revision", "citation_closure", "complete",
]
ENTRYPOINTS = {"phil-research", "phil-tutor", "phil-write", "phil-review", "phil-full"}
COLLABORATION_MODES = {"user-led", "assistant-led"}
OUTLINE_DECISIONS = {"pending", "approved", "rejected", "waived"}
CONCEPTION_DECISIONS = {"pending", "accepted", "waived"}
REVIEW_DECISIONS = {"pending", "accept", "minor", "major", "reject"}
CLOSURE_RESULTS = {"pending", "pass"}
FINDING_STATUSES = {"open", "accepted", "rejected", "resolved", "deferred"}
SEVERITIES = {"high", "medium", "low"}
AUDIT_VERDICTS = {"pass", "advisory", "block"}

# Artifact kinds that own a stage; a stale artifact of that kind rewinds resume to it.
STAGE_OF_KIND = {
    "conception": "incubation",
    "analysis": "research",
    "outline": "outline",
    "section-brief": "section_brief",
    "draft-section": "draft",
    "section-audit-report": "section_audit",
    "review-report": "review",
    "revision-log": "revision",
    "closure-report": "citation_closure",
}
SHA_PATTERN = re.compile(r"^[a-f0-9]{64}$")


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


_RUN_COUNTER = itertools.count(1)


def new_run_id() -> str:
    return "run-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"-{next(_RUN_COUNTER):04d}"


def empty_state(project_dir: Path) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "project": project_name(project_dir),
        "run_id": new_run_id(),
        "entrypoint": "phil-full",
        "stage": "intake",
        "status": "not_started",
        "collaboration_mode": "user-led",
        "artifacts": [],
        "approvals": {"outline": outline_approval("pending", None, "initial")},
        "review_findings": [],
        "section_audit": None,
        "next_action": "resolve intake: deliverable, sources, collaboration mode",
        "updated_at": now(),
    }


def outline_approval(decision: str, artifact_sha256: str | None, reason: str) -> dict:
    return {
        "decision": decision,
        "artifact_sha256": artifact_sha256,
        "recorded_at": now(),
        "reason": reason,
    }


def load(project_dir: Path) -> dict:
    path = state_path(project_dir)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else empty_state(project_dir)


def save(project_dir: Path, state: dict) -> None:
    errors = validate(state, project_name(project_dir))
    if errors:
        raise ValueError("invalid workflow state: " + "; ".join(errors))
    project_dir.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = now()
    state_path(project_dir).write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def is_safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and "\\" not in value
        and path.as_posix() == value
    )


def validate(state: dict, expected_project: str | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(state, dict):
        return ["state must be an object"]
    required_top = {
        "schema_version", "project", "run_id", "entrypoint", "stage", "status",
        "collaboration_mode", "artifacts", "approvals", "review_findings",
        "section_audit", "next_action", "updated_at",
    }
    if set(state) != required_top:
        errors.append("invalid state fields")
    if state.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if not isinstance(state.get("project"), str) or not state.get("project"):
        errors.append("project is required")
    if expected_project and state.get("project") != expected_project:
        errors.append("project does not match directory")
    if state.get("entrypoint") not in ENTRYPOINTS:
        errors.append("invalid entrypoint")
    if state.get("stage") not in STAGES:
        errors.append("invalid stage")
    if state.get("status") not in STATUSES:
        errors.append("invalid status")
    if state.get("collaboration_mode") not in COLLABORATION_MODES:
        errors.append("invalid collaboration_mode")
    if not isinstance(state.get("run_id"), str) or not state.get("run_id"):
        errors.append("run_id is required")

    seen_paths: set[str] = set()
    for artifact in state.get("artifacts") or []:
        if not isinstance(artifact, dict) or set(artifact) != {"kind", "path", "sha256", "status"}:
            errors.append("invalid artifact fields")
            continue
        if not isinstance(artifact["kind"], str) or not artifact["kind"]:
            errors.append("artifact kind required")
        if not is_safe_relative_path(artifact["path"]):
            errors.append(f"artifact path must be POSIX-relative: {artifact.get('path')!r}")
        elif artifact["path"] in seen_paths:
            errors.append(f"duplicate artifact path: {artifact['path']}")
        else:
            seen_paths.add(artifact["path"])
        if not isinstance(artifact["sha256"], str) or not SHA_PATTERN.match(artifact["sha256"]):
            errors.append("artifact sha256 malformed")
        if artifact["status"] not in {"current", "stale"}:
            errors.append("artifact status must be current or stale")

    approvals = state.get("approvals")
    if not isinstance(approvals, dict) or "outline" not in approvals:
        errors.append("approvals.outline is required")
    else:
        if set(approvals) - {"conception", "outline", "review", "citation_closure"}:
            errors.append("unknown approval gates")
        outline = approvals.get("outline")
        if not isinstance(outline, dict) or outline.get("decision") not in OUTLINE_DECISIONS:
            errors.append("invalid outline decision")
        elif outline["decision"] == "waived" and not str(outline.get("reason", "")).strip():
            errors.append("outline waiver requires a recorded reason")
        conception = approvals.get("conception")
        if conception is not None and (not isinstance(conception, dict)
                                       or conception.get("decision") not in CONCEPTION_DECISIONS):
            errors.append("invalid conception decision")
        review = approvals.get("review")
        if review is not None and (not isinstance(review, dict)
                                   or review.get("decision") not in REVIEW_DECISIONS):
            errors.append("invalid review decision")
        closure = approvals.get("citation_closure")
        if closure is not None and (not isinstance(closure, dict)
                                    or closure.get("integrity_result") not in CLOSURE_RESULTS):
            errors.append("invalid citation_closure integrity result")

    seen_ids: set[str] = set()
    for finding in state.get("review_findings") or []:
        if not isinstance(finding, dict) or set(finding) - {
            "id", "severity", "target", "status", "source_review_sha256", "note",
        }:
            errors.append("invalid finding fields")
            continue
        if not isinstance(finding.get("id"), str) or not finding["id"]:
            errors.append("finding id required")
        elif finding["id"] in seen_ids:
            errors.append(f"duplicate finding id: {finding['id']}")
        else:
            seen_ids.add(finding["id"])
        if finding.get("severity") not in SEVERITIES:
            errors.append("invalid finding severity")
        if finding.get("status") not in FINDING_STATUSES:
            errors.append("invalid finding status")
        if not isinstance(finding.get("source_review_sha256"), str) or not SHA_PATTERN.match(finding["source_review_sha256"]):
            errors.append("finding source_review_sha256 malformed")

    audit = state.get("section_audit")
    if audit is not None:
        if not isinstance(audit, dict) or set(audit) != {"report_sha256", "unresolved_high", "verdict"}:
            errors.append("invalid section_audit fields")
        else:
            if not SHA_PATTERN.match(str(audit["report_sha256"])):
                errors.append("section_audit report_sha256 malformed")
            if not isinstance(audit["unresolved_high"], int) or isinstance(audit["unresolved_high"], bool) or audit["unresolved_high"] < 0:
                errors.append("section_audit unresolved_high must be a non-negative integer")
            if audit["verdict"] not in AUDIT_VERDICTS:
                errors.append("invalid section_audit verdict")
    return errors


def refresh_artifacts(project_dir: Path, state: dict) -> bool:
    changed = False
    for artifact in state["artifacts"]:
        if not is_safe_relative_path(artifact.get("path")):
            if artifact.get("status") != "stale":
                artifact["status"] = "stale"
                changed = True
            continue
        path = project_dir / artifact["path"]
        stale = not path.is_file() or sha256(path) != artifact["sha256"]
        fresh_status = "stale" if stale else "current"
        if artifact.get("status") != fresh_status:
            artifact["status"] = fresh_status
            changed = True
    return changed


def earliest_affected_stage(state: dict) -> str | None:
    stages = [STAGE_OF_KIND.get(a["kind"]) for a in state["artifacts"] if a.get("status") == "stale"]
    stages = [s for s in stages if s]
    if not stages:
        return None
    return min(stages, key=STAGES.index)


def derive_next_action(state: dict) -> str | None:
    if state["status"] == "completed":
        return None
    if state["status"] == "stale":
        rewind = earliest_affected_stage(state) or state["stage"]
        return f"artifact hashes changed: renewed confirmation required at stage '{rewind}'"
    stage = state["stage"]
    outline = state["approvals"]["outline"]["decision"]
    if stage in {"intake", "research"}:
        return f"complete stage '{stage}' before advancing"
    if stage == "incubation":
        conception = (state["approvals"].get("conception") or {}).get("decision", "pending")
        return "accept or waive the conception artifact" if conception == "pending" else "advance after conception decision"
    if stage == "outline":
        return "await outline approval" if outline == "pending" else f"outline {outline}; proceed to section briefs"
    if stage in {"section_brief", "draft"}:
        if outline not in {"approved", "waived"}:
            return "outline approval required before drafting"
        return f"complete stage '{stage}'"
    if stage == "section_audit":
        audit = state["section_audit"]
        if audit is None:
            return "run the section audit"
        if audit["unresolved_high"] > 0 and audit["verdict"] != "pass":
            return "resolve or explicitly defer unresolved high-severity audit findings"
        return "advance to review"
    if stage == "review":
        review = state["approvals"].get("review")
        if not review or review["decision"] == "pending":
            return "record the editorial decision on the review report"
        return "advance to revision"
    if stage == "revision":
        open_high = [f for f in state["review_findings"] if f["severity"] == "high" and f["status"] in {"open", "accepted"}]
        return "resolve outstanding review findings (high severity open)" if open_high else "advance to citation closure"
    if stage == "citation_closure":
        closure = state["approvals"].get("citation_closure")
        if not closure or closure["integrity_result"] != "pass":
            return "run citation closure (machine check cannot be waived)"
        if not closure.get("acknowledged_at"):
            return "await user acknowledgement of the closure report"
        return "advance to complete"
    return None


def completion_blocked(state: dict) -> str | None:
    outline = state["approvals"]["outline"]["decision"]
    if outline not in {"approved", "waived"}:
        return f"outline decision is '{outline}'"
    audit = state["section_audit"]
    if audit and audit["unresolved_high"] > 0 and audit["verdict"] != "pass":
        return "unresolved high-severity section-audit findings"
    open_high = [f for f in state["review_findings"] if f["severity"] == "high" and f["status"] in {"open", "accepted"}]
    if open_high:
        return "unresolved high-severity review findings: " + ", ".join(f["id"] for f in open_high)
    closure = state["approvals"].get("citation_closure")
    if not closure or closure.get("integrity_result") != "pass":
        return "citation closure has not passed"
    if not closure.get("acknowledged_at"):
        return "citation closure not acknowledged by the user"
    return None


def cmd_init(project_dir: Path, args: argparse.Namespace) -> dict:
    state = load(project_dir)
    if state_path(project_dir).exists() and state.get("status") != "completed":
        return {
            "action": "refused",
            "reason": "an unfinished run exists; use resume",
            "existing_run": state["run_id"],
            "stage": state["stage"],
            "status": state["status"],
        }
    state = empty_state(project_dir)
    state["entrypoint"] = args.entrypoint
    if args.collaboration:
        state["collaboration_mode"] = args.collaboration
    state["status"] = "in_progress"
    state["next_action"] = derive_next_action(state)
    save(project_dir, state)
    return {"action": "started", "run_id": state["run_id"], "entrypoint": state["entrypoint"],
            "collaboration_mode": state["collaboration_mode"]}


def cmd_status(project_dir: Path, args: argparse.Namespace) -> dict:
    state = load(project_dir)
    changed = refresh_artifacts(project_dir, state)
    if changed and state_path(project_dir).exists():
        if any(a["status"] == "stale" for a in state["artifacts"]) and state["status"] != "completed":
            state["status"] = "stale"
        state["next_action"] = derive_next_action(state)
        save(project_dir, state)
    derived = derive_next_action(state)
    return {
        "run_id": state["run_id"], "entrypoint": state["entrypoint"], "stage": state["stage"],
        "status": state["status"], "collaboration_mode": state["collaboration_mode"],
        "artifacts": [{"kind": a["kind"], "path": a["path"], "status": a["status"]} for a in state["artifacts"]],
        "outline_decision": state["approvals"]["outline"]["decision"],
        "open_high_findings": [f["id"] for f in state["review_findings"]
                               if f["severity"] == "high" and f["status"] in {"open", "accepted"}],
        "next_action": derived,
        "refreshed": changed,
    }


def cmd_resume(project_dir: Path, args: argparse.Namespace) -> dict:
    state = load(project_dir)
    if not state_path(project_dir).exists():
        return {"action": "none", "reason": "no state file; use init"}
    refresh_artifacts(project_dir, state)
    stale = [a for a in state["artifacts"] if a["status"] == "stale"]
    if stale and state["status"] != "completed":
        state["status"] = "stale"
        rewind = earliest_affected_stage(state)
        if rewind:
            state["stage"] = rewind
        state["next_action"] = derive_next_action(state)
        save(project_dir, state)
        return {
            "action": "stale", "rewound_to": state["stage"],
            "stale_artifacts": [{"kind": a["kind"], "path": a["path"]} for a in stale],
            "request": "renewed user confirmation required before reusing outputs",
        }
    if state["status"] in {"stale", "blocked"}:
        state["status"] = "in_progress"
    state["next_action"] = derive_next_action(state)
    save(project_dir, state)
    return {"action": "resumed", "stage": state["stage"], "status": state["status"],
            "next_action": state["next_action"]}


def cmd_artifact(project_dir: Path, args: argparse.Namespace) -> dict:
    state = load(project_dir)
    if not is_safe_relative_path(args.path):
        raise ValueError(f"artifact path must be POSIX-relative: {args.path!r}")
    path = project_dir / args.path
    if not path.is_file():
        raise ValueError(f"artifact file not found: {args.path}")
    digest = sha256(path)
    for artifact in state["artifacts"]:
        if artifact["path"] == args.path:
            artifact.update(kind=args.kind, sha256=digest, status="current")
            break
    else:
        state["artifacts"].append({"kind": args.kind, "path": args.path, "sha256": digest, "status": "current"})
    state["next_action"] = derive_next_action(state)
    save(project_dir, state)
    return {"action": "recorded", "kind": args.kind, "path": args.path, "sha256": digest}


def cmd_advance(project_dir: Path, args: argparse.Namespace) -> dict:
    state = load(project_dir)
    if args.stage not in STAGES:
        raise ValueError(f"unknown stage: {args.stage}")
    if args.stage == "complete":
        blocked = completion_blocked(state)
        if blocked:
            return {"action": "refused", "reason": f"completion blocked: {blocked}"}
        state["stage"] = "complete"
        state["status"] = "completed"
        state["next_action"] = None
    else:
        if args.stage != state["stage"] and STAGES.index(args.stage) <= STAGES.index(state["stage"]):
            return {"action": "refused",
                    "reason": "cannot advance backwards from '" + state["stage"] + "' to '"
                              + args.stage + "' (resume handles rewinds)"}
        state["stage"] = args.stage
        if state["status"] in {"not_started", "awaiting_user", "blocked", "stale"}:
            state["status"] = "in_progress"
        state["next_action"] = derive_next_action(state)
    save(project_dir, state)
    return {"action": "advanced", "stage": state["stage"], "status": state["status"], "next_action": state["next_action"]}


def _gate_artifact_sha(project_dir: Path, relative: str | None) -> str | None:
    if not relative:
        return None
    target = project_dir / relative
    if not is_safe_relative_path(relative) or not target.is_file():
        raise ValueError(f"artifact not found: {relative}")
    return sha256(target)


def cmd_approve(project_dir: Path, args: argparse.Namespace) -> dict:
    state = load(project_dir)
    gate, decision = args.gate, args.decision
    if gate == "outline":
        if decision not in OUTLINE_DECISIONS:
            raise ValueError("outline decision must be pending/approved/rejected/waived")
        if decision == "waived" and not (args.reason or "").strip():
            raise ValueError("outline waiver requires the authorizing user instruction")
        state["approvals"]["outline"] = {
            "decision": decision,
            "artifact_sha256": _gate_artifact_sha(project_dir, args.artifact_path),
            "recorded_at": now(),
            "reason": args.reason or "",
        }
    elif gate == "conception":
        if decision not in CONCEPTION_DECISIONS:
            raise ValueError("conception decision must be pending/accepted/waived")
        if decision == "waived" and not (args.reason or "").strip():
            raise ValueError("conception waiver requires an explicit user instruction")
        state["approvals"]["conception"] = {
            "decision": decision,
            "artifact_sha256": _gate_artifact_sha(project_dir, args.artifact_path),
            "recorded_at": now(),
            "reason": args.reason or "",
        }
    elif gate == "review":
        if decision not in REVIEW_DECISIONS:
            raise ValueError("review decision must be pending/accept/minor/major/reject")
        state["approvals"]["review"] = {
            "decision": decision,
            "review_sha256": _gate_artifact_sha(project_dir, args.artifact_path),
            "recorded_at": now(),
            "reason": args.reason or "",
        }
    elif gate == "citation_closure":
        if decision == "acknowledge":
            closure = state["approvals"].get("citation_closure")
            if not closure or closure.get("integrity_result") != "pass":
                raise ValueError("citation closure cannot be acknowledged before a machine PASS")
            closure["acknowledged_at"] = now()
        elif decision == "pass":
            state["approvals"]["citation_closure"] = {
                "integrity_result": "pass",
                "report_sha256": _gate_artifact_sha(project_dir, args.artifact_path),
                "acknowledged_at": None,
                "recorded_at": now(),
            }
        else:
            raise ValueError("citation_closure decision must be pass or acknowledge")
    else:
        raise ValueError(f"unknown gate: {gate}")
    state["next_action"] = derive_next_action(state)
    save(project_dir, state)
    return {"action": "recorded", "gate": gate, "decision": decision}


def cmd_finding(project_dir: Path, args: argparse.Namespace) -> dict:
    state = load(project_dir)
    if args.severity not in SEVERITIES:
        raise ValueError("severity must be high/medium/low")
    if args.status not in FINDING_STATUSES:
        raise ValueError("finding status must be open/accepted/rejected/resolved/deferred")
    if args.status in {"deferred", "resolved"} and not (args.note or "").strip():
        raise ValueError(f"{args.status} requires a recorded reason/evidence in --note")
    review_sha = args.review_sha256 or ""
    if review_sha and not SHA_PATTERN.match(review_sha):
        raise ValueError("review_sha256 malformed")
    for finding in state["review_findings"]:
        if finding["id"] == args.id:
            finding.update(severity=args.severity, target=args.target, status=args.status,
                           source_review_sha256=review_sha or finding["source_review_sha256"],
                           note=args.note or finding.get("note", ""))
            break
    else:
        if not review_sha:
            raise ValueError("a new finding requires --review-sha256")
        state["review_findings"].append({
            "id": args.id, "severity": args.severity, "target": args.target,
            "status": args.status, "source_review_sha256": review_sha, "note": args.note or "",
        })
    state["next_action"] = derive_next_action(state)
    save(project_dir, state)
    return {"action": "recorded", "id": args.id, "status": args.status}


def cmd_audit(project_dir: Path, args: argparse.Namespace) -> dict:
    state = load(project_dir)
    if args.verdict not in AUDIT_VERDICTS:
        raise ValueError("verdict must be pass/advisory/block")
    if not is_safe_relative_path(args.report):
        raise ValueError(f"report path must be POSIX-relative: {args.report!r}")
    target = project_dir / args.report
    if not target.is_file():
        raise ValueError(f"audit report not found: {args.report}")
    state["section_audit"] = {
        "report_sha256": sha256(target),
        "unresolved_high": args.unresolved_high,
        "verdict": args.verdict,
    }
    state["next_action"] = derive_next_action(state)
    save(project_dir, state)
    return {"action": "recorded", "verdict": args.verdict, "unresolved_high": args.unresolved_high}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=None,
                        help="project directory (default: cwd)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init")
    init.add_argument("--entrypoint", choices=sorted(ENTRYPOINTS), default="phil-full")
    init.add_argument("--collaboration", choices=sorted(COLLABORATION_MODES))

    subparsers.add_parser("status")
    subparsers.add_parser("resume")

    artifact = subparsers.add_parser("artifact")
    artifact.add_argument("--kind", required=True)
    artifact.add_argument("--path", required=True)

    advance = subparsers.add_parser("advance")
    advance.add_argument("--stage", required=True)

    approve = subparsers.add_parser("approve")
    approve.add_argument("--gate", required=True,
                         choices=["conception", "outline", "review", "citation_closure"])
    approve.add_argument("--decision", required=True)
    approve.add_argument("--reason", default="")
    approve.add_argument("--artifact-path", default=None)

    finding = subparsers.add_parser("finding")
    finding.add_argument("--id", required=True)
    finding.add_argument("--severity", required=True)
    finding.add_argument("--target", required=True)
    finding.add_argument("--status", required=True)
    finding.add_argument("--review-sha256", default="")
    finding.add_argument("--note", default="")

    audit = subparsers.add_parser("audit")
    audit.add_argument("--report", required=True)
    audit.add_argument("--verdict", required=True)
    audit.add_argument("--unresolved-high", type=int, required=True)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_dir = (args.project or Path.cwd()).resolve()
    handlers = {
        "init": cmd_init, "status": cmd_status, "resume": cmd_resume, "artifact": cmd_artifact,
        "advance": cmd_advance, "approve": cmd_approve, "finding": cmd_finding, "audit": cmd_audit,
    }
    try:
        result = handlers[args.command](project_dir, args)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
