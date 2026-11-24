---
name: review
description: "Peer review your own philosophy manuscript: a full eight-dimension review, a targeted review, or a re-review of earlier findings. Read-only; revision is handed to phil:write revision. Use for 审稿、复审."
---

# phil-review

> **Paths.** `<root>` is the nearest ancestor of the working directory containing `Framework/Workflow/manifest.json`; if there is none, stop and report it. `Framework/…` and `Private/…` paths resolve from `<root>`. Bare `Methods/`, `Services/`, `Rules/`, `Schemas/`, `Scripts/`, `Contracts/`, `Commands/`, `References/`, and `Templates/` paths resolve from `<root>/Framework/Workflow/`. Run scripts with `<root>` as the working directory.

A domain-specific peer reviewer for **one's own writing**: simulated peer review assessing argument validity, conceptual clarity, modal rigor, dialectical charity, and counterexample resilience from configurable philosophical perspectives. Constructive, remediation-oriented, evidence-based — and **read-only toward the manuscript**: this skill never edits the draft. Revision is `phil:write revision`'s job; when the user explicitly requests revision alongside review, hand the findings to that mode rather than applying edits here.

## Usage

```
phil:review <manuscript>                    # full review
phil:review targeted <dimension|section>    # targeted review
phil:review re-review [prior report]        # verify prior findings' resolution
```

Routing: explicit mode wins; clean natural-language mapping routes directly; material ambiguity gets one focused question. Difference from `phil:research evaluate`: review targets one's own manuscript and produces constructive revision recommendations; evaluate critically analyzes others' texts.

## Modes

- **full** — all eight dimensions over the whole manuscript, major/minor issue ranking, prioritized revision recommendations.
- **targeted** — only the named dimensions or sections (e.g. modal rigor in §3); the same standards, scoped.
- **re-review** — load the prior review report and the current draft; for each finding verify resolution with evidence; report resolved / partially resolved / unresolved / regressed. Never mark a finding resolved without pointing at the passage that resolves it.

## Eight dimensions

1. **Argument validity and soundness** (`method.argument.argument-reconstruct`, `method.argument.premise-detect`) — do conclusions follow from premises; are premises defended or flagged as assumptions; any inferential gaps disguised by elegant prose.
2. **Charity to opposing views** (`method.argument.charity-check`) — strongest versions; would a holder of the opposing view recognize their position.
3. **Conceptual clarity and distinction precision** (`method.concept.conceptual-analysis`, `method.concept.distinction-track`) — defined-before-use; senses fixed; distinctions maintained.
4. **Modal rigor** (`method.metaphysics.modal-arg`) — necessity strength qualified; de dicto/de re; no epistemic-to-metaphysical slides.
5. **Counterexample resilience** (`method.argument.counterexample`) — generalizations qualified; obvious counterexamples addressed; vulnerabilities acknowledged.
6. **Dialectical completeness** (`method.dialectic.dialectical-map`) — positions engaged in order; objections anticipated; no blind spots on key objections.
7. **Ontological commitment transparency** (`method.metaphysics.ontological-commitment`) — quantificational commitments explicit; costs noted.
8. **Methodological consistency** (`method.dialectic.methodology`) — method matches execution; meta-philosophical choices coherent.

Load only the methods a dimension actually needs (manifest-resolved, per the shared loading contract); a targeted review loads fewer methods than a full one.

## Perspective simulation (optional)

Review additionally from a named perspective — Quinean / Lewisian / Kripkean / Williamsonian / Parfitian: what would that philosopher press on? Perspective biases are declared in the report, never hidden. A simulated perspective is a heuristic, not evidence of what the philosopher held: any attribution to them must route to a source-backed claim or be marked `[source unverified]`.

## Output

Standard review report in Chinese: (1) overall assessment; (2) dimension-by-dimension scores and comments; (3) major issues ranked by severity; (4) minor issues; (5) revision recommendations ranked by priority. Each finding is discrete and locatable (section + passage), enabling the finding ledger.

## Finding ledger

When workflow state is active (recognized project), record findings into `{topic}-workflow-state.json` via `Scripts/project-state.py finding` — stable ID, severity (`high`/`medium`/`low`), target, status (`open`/`accepted`/`rejected`/`resolved`/`deferred`), and source review hash. Findings drive `phil:write revision`; nothing is silently deleted, collapsed, or resolved without evidence. The editorial decision (`accept`/`minor`/`major`/`reject`) is recorded as `approvals.review` — the user's, never the reviewer's own.

## Quality standards

Constructive criticism over verdicts; perspective transparency; dimension completeness in full mode (report N/A explicitly rather than skipping silently); evidence-based assessment (every issue points at a passage); remediation orientation; charity to the reviewed work. Reports in Chinese; technical terms and citations in English where conventional.
