#!/usr/bin/env python3
"""Regenerate manifest.json (v2) from the method files, services, skills, and migration map."""

from __future__ import annotations

import json
import re
from pathlib import Path

WF = Path(__file__).resolve().parent.parent
MIG = WF / "Migration/migration-v0.7.json"


def parse_method_header(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta


def build() -> dict:
    mig = json.loads(MIG.read_text(encoding="utf-8"))
    items = []

    skills = [
        ("phil-research", "Skills/phil-research/SKILL.md",
         "Shared evidence and provenance kernel for philosophical research — five isolated modes: ingest (library intake), reconstruct (progressive source comprehension), evaluate (targeted critique), comment (argumentative detail), philosophers (source-backed philosopher database)",
         ["ingest", "reconstruct", "evaluate", "comment", "philosophers"],
         ["read", "search", "write", "pdf", "zotero-full", "zotero-local", "delegate"]),
        ("phil-tutor", "Skills/phil-tutor/SKILL.md",
         "Tutor-style dialogue in two modes — reading (default): Socratic literature dialogue, probing understanding, recommending sources, planning next steps; incubating: conception incubation (构思孵化) helping crystallize your own thesis and argument sketch",
         ["reading", "incubating"], ["read", "search", "write"]),
        ("phil-write", "Skills/phil-write/SKILL.md",
         "Philosophical manuscript writing in three modes — outline (structured outline from your conception), draft (section-by-section composition with user-led/assistant-led collaboration), revision (review-driven revision)",
         ["outline", "draft", "revision"], ["read", "search", "write"]),
        ("phil-review", "Skills/phil-review/SKILL.md",
         "Peer review of your own manuscript in three modes — full (whole-paper 8-dimension review), targeted (specific dimensions or sections), re-review (verify prior findings were resolved). Read-only unless revision is explicitly requested.",
         ["full", "targeted", "re-review"], ["read", "search"]),
    ]
    for sid, src, desc, modes, caps in skills:
        items.append({"id": sid, "kind": "skill", "source": src, "description": desc,
                      "modes": modes, "capabilities": caps, "platforms": ["claude", "codex"]})

    packages: dict[str, list[dict]] = {}
    for old, m in mig["method_map"].items():
        packages.setdefault(m["package"], []).append(m)
    pkg_contracts = {
        "argument": "Argument-form methods: reconstruction, charity, implicit premises, counterexamples, analogy, parity.",
        "concept": "Conceptual methods: conceptual analysis, distinction tracking, intuition pumps, thought experiments, natural kinds.",
        "dialectic": "Dialectical methods: citation extraction, contextualization, dialectical mapping, methodology, summarization.",
        "metaphysics": "Metaphysics-domain methods: causation, conceivability, essence, grounding, identity, modality, ontological commitment.",
        "metaethics": "Metaethics-domain methods: disagreement, epistemology, psychology, realism, semantics, supervenience, normativity.",
    }
    for pkg in sorted(packages):
        items.append({"id": f"package.{pkg}", "kind": "method_package", "source": f"Methods/{pkg}/",
                      "description": pkg_contracts[pkg],
                      "members": sorted(m["method_id"] for m in packages[pkg])})

    input_output = {
        "argument.argument-reconstruct": ("text or source excerpt", "standard-form reconstruction report"),
        "argument.charity-check": ("reconstruction report + original text", "charity audit report"),
        "argument.premise-detect": ("charitable reconstruction", "implicit-premise audit report"),
        "argument.counterexample": ("reconstruction report", "counterexample set with evaluation"),
        "argument.analogy-check": ("argument containing an analogy", "analogy assessment report"),
        "argument.parity-check": ("argument containing a parity claim", "parity assessment report"),
        "concept.conceptual-analysis": ("text or reconstruction", "concept map / N-S condition analysis"),
        "concept.distinction-track": ("text or reconstruction", "distinction index and function test"),
        "concept.intuition-pump": ("thought-experiment passage", "intuition-pump analysis"),
        "concept.natural-kind-analyze": ("kind-classification claims", "natural kind analysis"),
        "concept.thought-experiment": ("thought-experiment passage", "thought-experiment deconstruction"),
        "dialectic.citation-extract": ("manuscript or text", "citation table with roles and cross-reference (citation-extract-schema.json)"),
        "dialectic.contextualize": ("argument + source", "contextualization report"),
        "dialectic.dialectical-map": ("text or debate corpus", "dialectical tree (dialectical-tree-schema.json)"),
        "dialectic.methodology": ("argument", "methodological-commitment analysis"),
        "dialectic.summarize": ("extracted source text + verified metadata", "Level 0.5 summary file (summary-schema.json)"),
        "metaphysics.modal-arg": ("modal claims in text", "modal argument analysis"),
        "metaphysics.conceivability-arg": ("conceivability reasoning", "conceivability-chain analysis"),
        "metaphysics.ontological-commitment": ("quantified claims", "commitment inventory (ontological-commitment-schema.json)"),
        "metaphysics.grounding-check": ("dependence claims", "grounding topology analysis"),
        "metaphysics.identity-persistence": ("identity claims", "identity-conditions analysis"),
        "metaphysics.causation-analyze": ("causal claims", "causal affiliation and exclusion analysis"),
        "metaphysics.essence-detect": ("essence/accident usage", "essentialist-claim analysis"),
        "metaethics.moral-realism": ("realism-spectrum argument", "moral realism analysis (moral-realism-schema.json)"),
        "metaethics.normativity": ("normative-source claims", "normativity analysis (normativity-schema.json)"),
        "metaethics.moral-semantics": ("moral-language claims", "moral semantics analysis (moral-semantics-schema.json)"),
        "metaethics.moral-psychology": ("judgment-motivation claims", "moral psychology analysis (moral-psychology-schema.json)"),
        "metaethics.moral-disagreement": ("disagreement-based argument", "moral disagreement analysis"),
        "metaethics.moral-epistemology": ("moral-knowledge claims", "moral epistemology analysis"),
        "metaethics.moral-supervenience": ("supervenience claims", "moral supervenience analysis"),
    }
    for pkg in sorted(packages):
        for m in sorted(packages[pkg], key=lambda x: x["slug"]):
            meta = parse_method_header(WF / "Methods" / pkg / (m["slug"] + ".md"))
            io = input_output.get(f'{pkg}.{m["slug"]}', ("text", "analysis report"))
            items.append({
                "id": m["method_id"], "kind": "method", "package": f"package.{pkg}",
                "source": f'Methods/{pkg}/{m["slug"]}.md',
                "description": m["label"] + " — internal method; input: " + io[0] + "; output: " + io[1] + ".",
                "legacy_ids": [k for k, v in mig["method_map"].items() if v["method_id"] == m["method_id"]],
                "label": m["label"],
                "consumers": [c.strip() for c in meta["consumers"].strip("[]").split(",")],
                "selector": meta["selector"],
                "inputs": io[0], "outputs": io[1],
                "side_effect_policy": "read-only",
            })

    services = [
        ("service.source-intake", "Services/source-intake.md",
         "Library intake pipeline: deterministic scan, title-page extraction, canonical rename, INDEX registration, Level 0.5 summaries, philosopher observations, recommendation trigger 1.",
         ["phil-research/ingest"], "write (library, queue; never projects)"),
        ("service.zotero-registration", "Services/zotero-registration.md",
         "Identifier-gated Zotero registration with linked-file attachment (DOI to ISBN to bibtex cascade).",
         ["phil-research/ingest"], "write (external cloud; identifier-gated)"),
        ("service.citation-gate", "Services/citation-gate.md",
         "Two-hop Citation Gate: refs.md registration + verified hash-current analysis verification.",
         ["phil-write", "phil-review", "phil-full", "phil-research/reconstruct"], "read + block"),
        ("service.philosopher-db", "Services/philosopher-db.md",
         "Philosopher database maintenance: queue, review, explicit approval, lazy audit, rebuild.",
         ["phil-research/philosophers", "phil-research/ingest"], "write (queue, profiles; approval explicit)"),
        ("service.evidence-retrieval", "Services/evidence-retrieval.md",
         "Evidence-unit location, quotation, and hash-current reuse without full-PDF context loads (0.7.0: local deterministic + cache contract).",
         ["phil-research/reconstruct", "phil-research/evaluate", "phil-tutor", "phil-write", "phil-review"], "read"),
    ]
    for sid, src, desc, consumers, authority in services:
        items.append({"id": sid, "kind": "service", "source": src, "description": desc,
                      "consumers": consumers, "authority": authority})

    items.append({
        "id": "phil-full", "kind": "command", "source": "Commands/phil-full.md",
        "description": "Full-pipeline state machine — start, status, resume; orchestrates the four skills through persisted v2 workflow state.",
        "modes": ["start", "status", "resume"],
        "stages": ["intake", "research", "incubation", "outline", "section_brief", "draft",
                   "section_audit", "review", "revision", "citation_closure", "complete"],
        "consumers": ["phil-research", "phil-tutor", "phil-write", "phil-review"],
    })

    return {
        "schema_version": 2,
        "exposure": {
            "skills": ["phil-research", "phil-tutor", "phil-write", "phil-review"],
            "claude_command_wrappers": ["research", "tutor", "write", "review", "full"],
        },
        "migration_map": "Migration/migration-v0.7.json",
        "items": items,
    }


if __name__ == "__main__":
    manifest = build()
    (WF / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    kinds: dict[str, int] = {}
    for item in manifest["items"]:
        kinds[item["kind"]] = kinds.get(item["kind"], 0) + 1
    print("manifest v2 items:", kinds)
