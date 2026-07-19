#!/usr/bin/env python3
"""Normalize cross-runtime workflow policy values."""

from __future__ import annotations

import argparse
import json


COLLABORATION_ALIASES = {
    "user-led": ("user-led", False),
    "assistant-led": ("assistant-led", False),
    "claude-led": ("assistant-led", True),
    "codex-led": ("assistant-led", True),
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


def citation_gate(registered: bool, required_level: float, available_level: float) -> dict:
    if required_level < 0 or available_level < 0:
        raise ValueError("analysis levels must be non-negative")
    if not registered:
        return {"decision": "block", "hop": 1, "reason": "key-not-in-refs"}
    if available_level < required_level:
        return {"decision": "block", "hop": 2, "reason": "analysis-level-insufficient"}
    return {"decision": "pass", "hop": 2, "reason": "verified"}


def philosopher_claim_gate(
    support_status: str,
    evidence: list[dict[str, object]],
    registered_keys: set[str],
    required_level: float,
) -> dict:
    """Route a philosopher claim through its bibliography evidence."""
    if support_status != "source-backed":
        return {"decision": "block", "hop": 0, "reason": "philosopher-claim-prompt-only"}
    if not evidence:
        return {"decision": "block", "hop": 0, "reason": "philosopher-claim-missing-evidence"}
    registered = [item for item in evidence if item.get("bib_key") in registered_keys]
    if not registered:
        return {"decision": "block", "hop": 1, "reason": "evidence-key-not-registered"}
    eligible = sorted({
        str(item["bib_key"])
        for item in registered
        if float(item.get("analysis_level", 0)) >= required_level
    })
    if not eligible:
        return {"decision": "block", "hop": 2, "reason": "analysis-level-insufficient"}
    return {
        "decision": "pass",
        "hop": 2,
        "reason": "source-evidence-sufficient",
        "eligible_keys": eligible,
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
    citation.add_argument("--required-level", type=float, required=True)
    citation.add_argument("--available-level", type=float, required=True)
    args = parser.parse_args()
    try:
        if args.command == "collaboration":
            result = normalize_collaboration(args.value)
        elif args.command == "zotero":
            result = zotero_plan(args.mcp, args.local, args.dry_run)
        else:
            result = citation_gate(args.registered, args.required_level, args.available_level)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
