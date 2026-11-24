#!/usr/bin/env python3
"""Normalize cross-runtime workflow policy values."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


COLLABORATION_ALIASES = {
    "user-led": ("user-led", False),
    "assistant-led": ("assistant-led", False),
    "claude-led": ("assistant-led", True),
    "codex-led": ("assistant-led", True),
}
ANALYSIS_LEVELS = {0.5, 1, 2, 3}
RECONSTRUCTION_LEVELS = {
    1: ("method.argument.argument-reconstruct",),
    2: (
        "method.argument.argument-reconstruct",
        "method.argument.charity-check",
        "method.argument.premise-detect",
    ),
    3: (
        "method.argument.argument-reconstruct",
        "method.argument.charity-check",
        "method.argument.premise-detect",
        "method.dialectic.contextualize",
        "method.dialectic.dialectical-map",
    ),
}
RECONSTRUCTION_FEATURES = {
    "conceptual": "method.concept.conceptual-analysis",
    "distinction": "method.concept.distinction-track",
    "modal": "method.metaphysics.modal-arg",
    "thought-experiment": "method.concept.thought-experiment",
    "intuition": "method.concept.intuition-pump",
    "ontology": "method.metaphysics.ontological-commitment",
    "identity": "method.metaphysics.identity-persistence",
    "grounding": "method.metaphysics.grounding-check",
    "conceivability": "method.metaphysics.conceivability-arg",
    "causation": "method.metaphysics.causation-analyze",
    "essence": "method.metaphysics.essence-detect",
    "natural-kind": "method.concept.natural-kind-analyze",
    "moral-disagreement": "method.metaethics.moral-disagreement",
    "moral-epistemology": "method.metaethics.moral-epistemology",
    "moral-psychology": "method.metaethics.moral-psychology",
    "moral-realism": "method.metaethics.moral-realism",
    "moral-semantics": "method.metaethics.moral-semantics",
    "moral-supervenience": "method.metaethics.moral-supervenience",
    "normativity": "method.metaethics.normativity",
}
EVALUATION_FEATURES = {
    "counterexample": "method.argument.counterexample",
    "dialectical": "method.dialectic.dialectical-map",
    "analogy": "method.argument.analogy-check",
    "parity": "method.argument.parity-check",
    "intuition": "method.concept.intuition-pump",
    "methodology": "method.dialectic.methodology",
}
EVALUATION_INTENTS = {
    "targeted": (),
    "stress-test": ("counterexample", "dialectical"),
    "comparison": ("analogy", "parity"),
    "framing": ("intuition",),
    "method": ("methodology",),
}
LIGHTWEIGHT_EVALUATION = ("inference-scan", "fallacy-scan")
COVERAGE_ALIASES = {
    "phil-analogy-check": "method.argument.analogy-check",
    "phil-argument-reconstruct": "method.argument.argument-reconstruct",
    "phil-causation-analyze": "method.metaphysics.causation-analyze",
    "phil-charity-check": "method.argument.charity-check",
    "phil-citation-extract": "method.dialectic.citation-extract",
    "phil-conceivability-arg": "method.metaphysics.conceivability-arg",
    "phil-conceptual-analysis": "method.concept.conceptual-analysis",
    "phil-contextualize": "method.dialectic.contextualize",
    "phil-counterexample": "method.argument.counterexample",
    "phil-dialectical-map": "method.dialectic.dialectical-map",
    "phil-distinction-track": "method.concept.distinction-track",
    "phil-essence-detect": "method.metaphysics.essence-detect",
    "phil-grounding-check": "method.metaphysics.grounding-check",
    "phil-identity-persistence": "method.metaphysics.identity-persistence",
    "phil-intuition-pump": "method.concept.intuition-pump",
    "phil-methodology": "method.dialectic.methodology",
    "phil-modal-arg": "method.metaphysics.modal-arg",
    "phil-moral-disagreement": "method.metaethics.moral-disagreement",
    "phil-moral-epistemology": "method.metaethics.moral-epistemology",
    "phil-moral-psychology": "method.metaethics.moral-psychology",
    "phil-moral-realism": "method.metaethics.moral-realism",
    "phil-moral-semantics": "method.metaethics.moral-semantics",
    "phil-moral-supervenience": "method.metaethics.moral-supervenience",
    "phil-natural-kind-analyze": "method.concept.natural-kind-analyze",
    "phil-normativity": "method.metaethics.normativity",
    "phil-ontological-commitment": "method.metaphysics.ontological-commitment",
    "phil-parity-check": "method.argument.parity-check",
    "phil-premise-detect": "method.argument.premise-detect",
    "phil-summarize": "method.dialectic.summarize",
    "phil-thought-experiment": "method.concept.thought-experiment",
    "contextualization": "method.dialectic.contextualize",
    "modal argument": "method.metaphysics.modal-arg",
    "ontological commitment": "method.metaphysics.ontological-commitment",
    "argument reconstruction": "method.argument.argument-reconstruct",
    "argument-reconstruct": "method.argument.argument-reconstruct",
    "charity audit": "method.argument.charity-check",
    "charity-check": "method.argument.charity-check",
    "implicit premises": "method.argument.premise-detect",
    "premise-detect": "method.argument.premise-detect",
    "conceptual analysis": "method.concept.conceptual-analysis",
    "conceptual-analysis": "method.concept.conceptual-analysis",
    "distinction tracking": "method.concept.distinction-track",
    "distinction-track": "method.concept.distinction-track",
    "modal-arg": "method.metaphysics.modal-arg",
    "thought-experiment": "method.concept.thought-experiment",
    "intuition-pump": "method.concept.intuition-pump",
    "ontological-commitment": "method.metaphysics.ontological-commitment",
    "contextualize": "method.dialectic.contextualize",
    "dialectical mapping": "method.dialectic.dialectical-map",
    "dialectical-map": "method.dialectic.dialectical-map",
    "counterexample": "method.argument.counterexample",
    "analogy-check": "method.argument.analogy-check",
    "parity-check": "method.argument.parity-check",
    "methodology": "method.dialectic.methodology",
}


def normalize_collaboration(value: str) -> dict:
    normalized = value.strip().lower()
    if normalized not in COLLABORATION_ALIASES:
        raise ValueError("collaboration must be user-led or assistant-led")
    canonical, deprecated = COLLABORATION_ALIASES[normalized]
    return {"input": normalized, "canonical": canonical, "deprecated_alias": deprecated}


def zotero_status(mcp: bool, local: bool) -> str:
    if mcp:
        return "full"
    if local:
        return "partial"
    return "skipped"


def zotero_plan(mcp: bool, local: bool, dry_run: bool = False) -> dict:
    status = zotero_status(mcp, local)
    return {
        "status": status,
        "step8": status,
        "write_allowed": status == "full" and not dry_run,
        "dry_run": dry_run,
    }


def refs_status(refs_path: Path, key: str) -> str:
    """Return ``registered``, ``rejected``, or ``absent`` for a KEY in refs.md."""
    if not refs_path.is_file():
        return "absent"
    statuses: list[str] = []
    for line in refs_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if "|" not in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        # A table row has KEY, role, and status cells; prose does not.
        if len(cells) >= 3 and cells[0] == key:
            statuses.append(cells[2].lower())
    if not statuses:
        return "absent"
    # Fail closed: a KEY marked rejected in any row, even with an annotation, stays rejected.
    return "rejected" if any("rejected" in status for status in statuses) else "registered"


def citation_gate(
    registered: bool,
    required_level: float,
    available_level: float | None = None,
    metadata: dict[str, object] | None = None,
    current_source_sha256: str | None = None,
    current_analysis_sha256: str | None = None,
    cited_key: str | None = None,
) -> dict:
    """Apply both Citation Gate hops using verified analysis metadata.

    ``available_level`` remains an optional compatibility input.  It can still
    establish an insufficient-level block, but it can never establish a pass.
    """
    if not _valid_level(required_level) or (
        available_level is not None and not _valid_level(available_level)
    ):
        return {"decision": "block", "hop": 2, "reason": "analysis-level-insufficient"}
    if not registered:
        return {"decision": "block", "hop": 1, "reason": "key-not-in-refs"}
    if available_level is not None and available_level < required_level:
        return {"decision": "block", "hop": 2, "reason": "analysis-level-insufficient"}
    if not isinstance(metadata, dict):
        return {"decision": "block", "hop": 2, "reason": "analysis-metadata-missing"}
    if (
        cited_key is not None
        and isinstance(metadata.get("bib_key"), str)
        and metadata["bib_key"] != cited_key
    ):
        return {"decision": "block", "hop": 2, "reason": "analysis-key-mismatch"}

    metadata_level = metadata.get("analysis_level")
    if not _has_required_level(metadata_level, required_level):
        return {"decision": "block", "hop": 2, "reason": "analysis-level-insufficient"}
    if metadata.get("verification_status") == "stale":
        return {"decision": "block", "hop": 2, "reason": "analysis-stale"}
    if metadata.get("verification_status") != "verified":
        return {"decision": "block", "hop": 2, "reason": "analysis-unverified"}
    if (
        not _matching_sha256(metadata.get("source_sha256"), current_source_sha256)
        or not _matching_sha256(metadata.get("analysis_sha256"), current_analysis_sha256)
    ):
        return {"decision": "block", "hop": 2, "reason": "analysis-stale"}
    return {"decision": "pass", "hop": 2, "reason": "verified"}


def _matching_sha256(recorded: object, current: str | None) -> bool:
    return (
        isinstance(recorded, str)
        and isinstance(current, str)
        and len(recorded) == 64
        and recorded == recorded.lower()
        and current == current.lower()
        and recorded == current
    )


def _valid_level(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and value in ANALYSIS_LEVELS
    )


def _has_required_level(value: object, required_level: object) -> bool:
    return _valid_level(value) and _valid_level(required_level) and value >= required_level


def _valid_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and value == value.lower()
        and all(character in "0123456789abcdef" for character in value)
    )


def _artifact_candidates(artifacts: object) -> list[dict[str, object]]:
    if isinstance(artifacts, dict):
        return [artifacts]
    if isinstance(artifacts, list):
        return [item for item in artifacts if isinstance(item, dict)]
    return []


def _canonical_coverage(values: list[object]) -> set[str]:
    return {
        COVERAGE_ALIASES.get(value, value)
        for value in values
        if isinstance(value, str)
    }


def _current_coverage(
    artifacts: object,
    source_sha256: str | None,
    analysis_sha256: str | None,
) -> tuple[set[str], list[str]]:
    """Return coverage reusable for the current source and an invalidation signal."""
    if source_sha256 is not None and not _valid_sha256(source_sha256):
        raise ValueError("source_sha256 must be a lowercase SHA-256 digest")
    if analysis_sha256 is not None and not _valid_sha256(analysis_sha256):
        raise ValueError("analysis_sha256 must be a lowercase SHA-256 digest")
    covered: set[str] = set()
    invalidations: set[str] = set()
    for artifact in _artifact_candidates(artifacts):
        recorded_hash = artifact.get("source_sha256")
        recorded_analysis_hash = artifact.get("analysis_sha256")
        coverage = artifact.get("coverage")
        if not isinstance(coverage, list) or not all(isinstance(item, str) for item in coverage):
            continue
        verification_status = artifact.get("verification_status")
        if verification_status != "verified":
            invalidations.add(
                "analysis-stale" if verification_status == "stale" else "analysis-unverified"
            )
            continue
        if source_sha256 is None or analysis_sha256 is None:
            invalidations.add("hash-required")
            continue
        if recorded_hash != source_sha256:
            invalidations.add("source-hash-changed")
            continue
        if recorded_analysis_hash != analysis_sha256:
            invalidations.add("analysis-hash-changed")
            continue
        covered.update(_canonical_coverage(coverage))
    return covered, sorted(invalidations)


def _plan_modules(
    workflow: str,
    requested: tuple[str, ...],
    artifacts: object,
    source_sha256: str | None,
    analysis_sha256: str | None,
    always_run: tuple[str, ...] = (),
    override: str = "none",
) -> dict:
    coverage, invalidations = _current_coverage(artifacts, source_sha256, analysis_sha256)
    run = list(always_run)
    reuse = []
    for module in requested:
        if module in always_run:
            continue
        if module in coverage:
            reuse.append(module)
        else:
            run.append(module)
    return {
        "workflow": workflow,
        "override": override,
        "source_changed": "source-hash-changed" in invalidations,
        "invalidation": invalidations,
        "run": run,
        "reuse": reuse,
        "required_coverage": list(requested),
    }


def _decision_ledger(
    plan: dict,
    universe: tuple[str, ...],
    selectors: dict[str, str],
    skip_reasons: dict[str, str],
) -> list[dict[str, str]]:
    run = set(plan["run"])
    reuse = set(plan["reuse"])
    invalidations = plan["invalidation"]
    invalidation_reason = invalidations[0] if invalidations else "coverage-missing"
    decisions = []
    for module in universe:
        selector = selectors.get(module, "not-selected")
        if module in reuse:
            action, reason = "reuse", "verified-hash-current"
        elif module in run:
            action = "run"
            reason = "mandatory-baseline" if module in LIGHTWEIGHT_EVALUATION else invalidation_reason
        else:
            action, reason = "skip", skip_reasons.get(module, "feature-or-intent-absent")
        decisions.append({
            "module": module,
            "action": action,
            "reason": reason,
            "selector": selector,
        })
    return decisions


def reconstruction_plan(
    level: int = 1,
    artifacts: object = None,
    source_sha256: str | None = None,
    analysis_sha256: str | None = None,
    features: object = (),
    full: bool = False,
    deep: bool = False,
) -> dict:
    """Plan only the analysis dimensions not covered by a hash-current artifact."""
    if level not in RECONSTRUCTION_LEVELS:
        raise ValueError("reconstruction level must be 1, 2, or 3")
    if not isinstance(features, (list, tuple, set)) or not all(isinstance(item, str) for item in features):
        raise ValueError("features must be a list of feature names")
    unknown = set(features) - set(RECONSTRUCTION_FEATURES)
    if unknown:
        raise ValueError("unknown reconstruction features: " + ", ".join(sorted(unknown)))
    effective_level = 3 if full or deep else level
    requested = list(RECONSTRUCTION_LEVELS[effective_level])
    requested.extend(RECONSTRUCTION_FEATURES[item] for item in features)
    requested = list(dict.fromkeys(requested))
    selectors = {
        module: f"level:{effective_level}"
        for module in RECONSTRUCTION_LEVELS[effective_level]
    }
    selectors.update({
        RECONSTRUCTION_FEATURES[feature]: f"feature:{feature}"
        for feature in features
    })
    plan = _plan_modules(
        "reconstruct",
        tuple(requested),
        artifacts,
        source_sha256,
        analysis_sha256,
        override="deep" if deep else "full" if full else "none",
    )
    plan["level"] = effective_level
    plan["features"] = sorted(set(features))
    universe = tuple(dict.fromkeys(
        (*RECONSTRUCTION_LEVELS[3], *RECONSTRUCTION_FEATURES.values())
    ))
    plan["decisions"] = _decision_ledger(
        plan,
        universe,
        selectors,
        {
            module: "above-target-level"
            for module in RECONSTRUCTION_LEVELS[3]
            if module not in RECONSTRUCTION_LEVELS[effective_level]
        },
    )
    return plan


def evaluation_plan(
    intent: str = "targeted",
    artifacts: object = None,
    source_sha256: str | None = None,
    analysis_sha256: str | None = None,
    features: object = (),
    full: bool = False,
    deep: bool = False,
) -> dict:
    """Plan critique dimensions while retaining fresh lightweight inference checks."""
    if intent not in EVALUATION_INTENTS:
        raise ValueError("unknown evaluation intent")
    if not isinstance(features, (list, tuple, set)) or not all(isinstance(item, str) for item in features):
        raise ValueError("features must be a list of feature names")
    unknown = set(features) - set(EVALUATION_FEATURES)
    if unknown:
        raise ValueError("unknown evaluation features: " + ", ".join(sorted(unknown)))
    selected = list(EVALUATION_INTENTS[intent]) + list(features)
    if full or deep:
        selected.append("counterexample")
    requested = list(LIGHTWEIGHT_EVALUATION)
    requested.extend(EVALUATION_FEATURES[item] for item in selected)
    requested = list(dict.fromkeys(requested))
    plan = _plan_modules(
        "evaluate",
        tuple(requested),
        artifacts,
        source_sha256,
        analysis_sha256,
        always_run=LIGHTWEIGHT_EVALUATION,
        override="deep" if deep else "full" if full else "none",
    )
    selectors = {module: "mandatory-baseline" for module in LIGHTWEIGHT_EVALUATION}
    selectors.update({EVALUATION_FEATURES[item]: f"intent:{intent}" for item in EVALUATION_INTENTS[intent]})
    selectors.update({EVALUATION_FEATURES[item]: f"feature:{item}" for item in features})
    if full or deep:
        selectors["method.argument.counterexample"] = "explicit-override"
    plan["intent"] = intent
    plan["features"] = sorted(set(features))
    universe = (*LIGHTWEIGHT_EVALUATION, *EVALUATION_FEATURES.values())
    plan["decisions"] = _decision_ledger(plan, universe, selectors, {})
    return plan


def sha256_file(path: Path) -> str:
    if path.suffix.lower() in {".txt", ".md", ".json", ".tex", ".bib"}:
        # Normalize line endings so a CRLF checkout keeps a recorded text hash valid.
        data = path.read_bytes().replace(b"\r\n", b"\n")
        return hashlib.sha256(data).hexdigest()
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def philosopher_claim_gate(
    support_status: str,
    evidence: list[dict[str, object]],
    registered_keys: set[str],
    required_level: float,
    verification_by_key: dict[str, dict[str, object]] | None = None,
) -> dict:
    """Route a philosopher claim through its bibliography evidence."""
    if support_status != "source-backed":
        return {"decision": "block", "hop": 0, "reason": "philosopher-claim-prompt-only"}
    if not evidence:
        return {"decision": "block", "hop": 0, "reason": "philosopher-claim-missing-evidence"}
    registered = [item for item in evidence if item.get("bib_key") in registered_keys]
    if not registered:
        return {"decision": "block", "hop": 1, "reason": "evidence-key-not-registered"}
    if not _valid_level(required_level):
        return {"decision": "block", "hop": 2, "reason": "analysis-level-insufficient"}
    eligible = sorted({
        str(item["bib_key"])
        for item in registered
        if _has_required_level(item.get("analysis_level"), required_level)
    })
    if not eligible:
        return {"decision": "block", "hop": 2, "reason": "analysis-level-insufficient"}

    if not isinstance(verification_by_key, dict):
        return {"decision": "block", "hop": 2, "reason": "analysis-metadata-missing"}

    verified = []
    has_metadata_missing = False
    has_unverified = False
    has_stale = False
    for key in eligible:
        item = verification_by_key.get(key)
        if not isinstance(item, dict):
            has_metadata_missing = True
            continue
        if item.get("verification_status") == "stale":
            has_stale = True
        elif item.get("verification_status") != "verified":
            has_unverified = True
        elif (
            item.get("source_hash_matches") is not True
            or item.get("analysis_hash_matches") is not True
        ):
            has_stale = True
        elif _has_required_level(item.get("analysis_level"), required_level):
            verified.append(key)

    if verified:
        return {
            "decision": "pass",
            "hop": 2,
            "reason": "source-evidence-sufficient",
            "eligible_keys": verified,
        }
    if has_metadata_missing:
        return {"decision": "block", "hop": 2, "reason": "analysis-metadata-missing"}
    if has_stale:
        return {"decision": "block", "hop": 2, "reason": "analysis-stale"}
    if has_unverified:
        return {"decision": "block", "hop": 2, "reason": "analysis-unverified"}
    return {"decision": "block", "hop": 2, "reason": "analysis-level-insufficient"}


def removed_entrypoint(command: str) -> dict:
    """Resolve a removed v0.6 command to its v0.7 replacement with an explicit message."""
    migration = json.loads(
        (Path(__file__).resolve().parent.parent / "Migration" / "migration-v0.7.json").read_text(encoding="utf-8")
    )
    table = migration["command_map"]
    entry = table.get(command)
    if entry is None:
        known = ", ".join(sorted(table))
        raise ValueError(f"unknown command: {command} (known: {known})")
    if entry["status"] == "retained":
        return {"command": command, "status": "retained", "message": f"{command} is unchanged in v0.7"}
    return {
        "command": command,
        "status": "removed",
        "replacement": entry["replacement"],
        "message": f"{command} was removed in 0.7.0-alpha. Use `{entry['replacement']}` instead. "
        "No alias or deprecation shim is retained.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    collaboration = subparsers.add_parser("collaboration")
    collaboration.add_argument("value")
    zotero = subparsers.add_parser("zotero")
    zotero.add_argument("--mcp", action="store_true")
    zotero.add_argument("--local", action="store_true")
    zotero.add_argument("--dry-run", action="store_true")
    citation = subparsers.add_parser("citation-gate")
    citation.add_argument("--registered", action="store_true")
    citation.add_argument("--key")
    citation.add_argument("--refs", type=Path)
    citation.add_argument("--required-level", type=float, required=True)
    citation.add_argument("--available-level", type=float)
    citation.add_argument("--metadata", type=Path)
    citation.add_argument("--source-path", type=Path)
    citation.add_argument("--analysis-path", type=Path)
    reconstruction = subparsers.add_parser("reconstruction-plan")
    reconstruction.add_argument("--level", type=int, choices=(1, 2, 3), default=1)
    reconstruction.add_argument("--artifacts", type=Path)
    reconstruction.add_argument("--source-sha256")
    reconstruction.add_argument("--source-path", type=Path)
    reconstruction.add_argument("--analysis-sha256")
    reconstruction.add_argument("--analysis-path", type=Path)
    reconstruction.add_argument("--feature", action="append", default=[])
    reconstruction.add_argument("--full", action="store_true")
    reconstruction.add_argument("--deep", action="store_true")
    evaluation = subparsers.add_parser("evaluation-plan")
    evaluation.add_argument("--intent", choices=sorted(EVALUATION_INTENTS), default="targeted")
    evaluation.add_argument("--artifacts", type=Path)
    evaluation.add_argument("--source-sha256")
    evaluation.add_argument("--source-path", type=Path)
    evaluation.add_argument("--analysis-sha256")
    evaluation.add_argument("--analysis-path", type=Path)
    evaluation.add_argument("--feature", action="append", default=[])
    evaluation.add_argument("--full", action="store_true")
    evaluation.add_argument("--deep", action="store_true")
    removed = subparsers.add_parser("removed-entrypoint")
    removed.add_argument("name")
    args = parser.parse_args()
    if args.command == "citation-gate" and args.refs is not None and args.key is None:
        parser.error("--refs requires --key")
    try:
        if args.command == "removed-entrypoint":
            result = removed_entrypoint(args.name)
        elif args.command == "collaboration":
            result = normalize_collaboration(args.value)
        elif args.command == "zotero":
            result = zotero_plan(args.mcp, args.local, args.dry_run)
        elif args.command == "citation-gate":
            metadata = None
            if args.metadata is not None:
                with args.metadata.open(encoding="utf-8") as handle:
                    metadata = json.load(handle)
            source_hash = sha256_file(args.source_path) if args.source_path else None
            analysis_hash = sha256_file(args.analysis_path) if args.analysis_path else None
            refs_result = refs_status(args.refs, args.key) if args.refs is not None else None
            if refs_result == "absent":
                result = {"decision": "block", "hop": 1, "reason": "key-not-in-refs"}
            elif refs_result == "rejected":
                result = {"decision": "block", "hop": 1, "reason": "key-rejected"}
            else:
                registered = args.registered if refs_result is None else True
                result = citation_gate(
                    registered,
                    args.required_level,
                    args.available_level,
                    metadata,
                    source_hash,
                    analysis_hash,
                    cited_key=args.key,
                )
        else:
            artifacts = None
            if args.artifacts is not None:
                with args.artifacts.open(encoding="utf-8") as handle:
                    artifacts = json.load(handle)
            if args.command == "reconstruction-plan":
                source_hash = sha256_file(args.source_path) if args.source_path else args.source_sha256
                analysis_hash = sha256_file(args.analysis_path) if args.analysis_path else args.analysis_sha256
                result = reconstruction_plan(
                    args.level,
                    artifacts,
                    source_hash,
                    analysis_hash,
                    args.feature,
                    args.full,
                    args.deep,
                )
            else:
                source_hash = sha256_file(args.source_path) if args.source_path else args.source_sha256
                analysis_hash = sha256_file(args.analysis_path) if args.analysis_path else args.analysis_sha256
                result = evaluation_plan(
                    args.intent,
                    artifacts,
                    source_hash,
                    analysis_hash,
                    args.feature,
                    args.full,
                    args.deep,
                )
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False))
    if args.command == "citation-gate" and result.get("decision") != "pass":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
