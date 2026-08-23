# Mode contract: reconstruct

Read-only progressive comprehension of another author's text, with verification-aware coverage planning. Produces a Chinese analysis report and, when persisted, refreshed analysis metadata.

## Usage

```
phil:research reconstruct --level <1|2|3> <text>
phil:research reconstruct --full <text>      # --deep is an alias
```

A standalone legacy invocation without a level keeps full-comprehension behavior; report that full coverage was selected. Pipeline and Citation Gate upgrade calls must specify the lowest required `--level`.

## Deterministic preplan (before loading any method)

Use the current execution model once to classify only the features present in the supplied text or a valid reused reconstruction. Do not invoke a method or load examples/checklists for this classification. Pass the feature flags to:

```bash
python "Framework/Workflow/Scripts/workflow-policy.py" reconstruction-plan \
  --level <N> --feature <f>... [--artifacts <meta>] [--source-sha256 ...] [--analysis-sha256 ...] [--full]
```

Treat a genuinely ambiguous feature as present; for `--full`/`--deep`, make classification exhaustive. Report the preplan: requested target; current source SHA-256 and prior declared coverage when a persisted artifact exists; the feature scan; and each candidate dimension's `run`/`reuse`/`skip` decision, selector, and deterministic reason (above-target-level, source/analysis hash changed, verification failed, coverage missing, feature/intent absent, explicit override, or valid coverage reused).

New coverage entries use canonical method IDs. Legacy labels and `phil-*` skill IDs in old artifacts normalize on read (the planner does this); never write a new alias.

## Coverage levels

- **Level 1 — argument backbone**: `method.argument.argument-reconstruct` (thesis, numbered premise-conclusion chains, argument type, unresolved textual ambiguities).
- **Level 2 — interpretive and conceptual reliability**: Level 1 plus `method.argument.charity-check` (always), `method.argument.premise-detect` (always, after charity), `method.concept.conceptual-analysis` (a term carries argumentative weight), `method.concept.distinction-track` (the argument relies on a distinction). The two conceptual tasks may run in parallel after Level 1; no material concept/distinction → record an explicit `skip`, never an empty section.
- **Level 3 — contextual and domain coverage**: Levels 1–2 plus `method.dialectic.contextualize` (always), `method.dialectic.dialectical-map` (always), and feature-selected: `method.metaphysics.modal-arg` (modal operators matter), `method.concept.thought-experiment` (a hypothetical case does argumentative work), `method.concept.intuition-pump` (the case elicits a supporting judgment), `method.metaphysics.ontological-commitment`, `method.metaphysics.identity-persistence`, `method.metaphysics.grounding-check`, `method.metaphysics.conceivability-arg`, `method.metaphysics.causation-analyze`, `method.metaphysics.essence-detect`, `method.metaphysics.natural-kind-analyze`, and the metaethics package member whose feature is present (`moral-disagreement`, `moral-epistemology`, `moral-psychology`, `moral-realism`, `moral-semantics`, `moral-supervenience`, `normativity`).

`--full`/`--deep` runs every applicable detected dimension despite a missing efficiency trigger. It covers only detected dimensions — it does not invent a domain analysis where the text has no relevant claim; record those as not applicable.

## Evidence and reuse

Reuse is permitted only when prior metadata is `verified`, both recorded hashes equal the current hashes, and its coverage explicitly contains the needed canonical method. A changed hash invalidates the artifact: mark `stale`, rerun only the dimensions the new target requires. Quote passages as evidence units (`Services/evidence-retrieval.md`) with page/section provenance.

## Output

Integrated Chinese report containing: (1) preplan and coverage ledger; (2) executive summary and argument reconstruction; (3) only the Level 2/3 sections actually run or reused, each labeled with coverage status; (4) domain findings only where triggered or explicitly requested; (5) open questions and remaining coverage gaps. State which features triggered each optional dimension and why absent dimensions were skipped.

When persisting under `Private/Bibliography/Analysis/`: include `source_bib_key` and compact `philosopher_observations[]` (`Schemas/philosopher-observation-schema.json`); refresh the paired `.analysis.meta.json` per `Schemas/analysis-metadata-schema.json` — current source and analysis hashes, target level, canonical actual-coverage method IDs, workflow version (`phil:research reconstruct`), and verification status (`provisional` until the declared coverage is checked against the current source). Then record with `philosopher-db.py observe --analysis-level <INDEX level> --input <file>`. Ad-hoc reports do not update the queue.

The result is a primary input to `phil:research evaluate` and `phil:write` draft mode. Philosopher observations create private review candidates only; they never overwrite canonical claims.
