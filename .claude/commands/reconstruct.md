---
description: "Progressive, verification-aware comprehension of philosophical texts — plans the minimum Level 1, 2, or 3 coverage, reuses only verified hash-current analysis, and supports explicit full or deep coverage"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->
# /phil:reconstruct

## Usage

```
/phil:reconstruct --level <1|2|3> <text>
/phil:reconstruct --full <text>
```

`--deep` is an alias for `--full`. A standalone legacy invocation without a level keeps the former full-comprehension behaviour; report that full coverage was selected. Pipeline and Citation Gate upgrade calls must specify the lowest required `--level`.

## Role

Produce a Chinese argument-comprehension report for another author's text, with progressive coverage rather than a fixed all-skill bundle. The selected level is a minimum coverage target, not a reason to run dimensions already present in a valid artifact.

## Feature Classification and Deterministic Preplan

Before reading optional skill material or delegating analysis, use the current execution model once to classify only the features present in the supplied text or a valid reused reconstruction. Do not invoke an analysis skill or load examples/checklists for this classification. Pass the resulting feature flags to `workflow-policy.py reconstruction-plan`; this deterministic planner does not interpret philosophical text itself. When a feature is genuinely ambiguous, select it rather than risk omitting a relevant dimension. For `--full` / `--deep`, make this classification exhaustive.

Report the resulting preplan containing:

1. Requested target (`1`, `2`, `3`, or `full`) and any stated purpose.
2. Current source SHA-256, prior analysis metadata and declared coverage, when a persisted artifact exists.
3. A feature scan of the supplied text or valid Level 1 reconstruction: explicit argument, modal claims, thought experiments, analogies/parity claims, grounding/identity/essence/natural-kind/causation claims, and moral/normative claims.
4. For each candidate dimension, the planner's `reuse`, `run`, or `skip` decision, selector, and deterministic reason: above target level, source or analysis hash changed, verification failed, coverage missing, feature/intent absent, explicit override, or valid coverage reused.

New metadata coverage entries MUST use canonical `phil-*` skill IDs. When reading a legacy artifact, `workflow-policy.py` may normalize a documented legacy alias to its canonical ID; never write a new alias. Reuse is permitted only when the prior metadata is `verified`, both its recorded source and analysis hashes equal the current hashes, and its coverage explicitly contains the needed canonical dimension. A changed source or analysis hash invalidates the artifact for reuse; mark it `stale` and rerun only the dimensions required by the new target.

## Coverage Levels

### Level 1: Argument Backbone

Run `phil-argument-reconstruct` only when no valid reconstruction coverage can be reused. Produce the thesis, numbered premise-conclusion chains, argument type, and unresolved textual ambiguities.

### Level 2: Interpretive and Conceptual Reliability

Include Level 1, then run only missing coverage among:

| Skill | Trigger | Dependency |
|---|---|---|
| `phil-charity-check` | Always at Level 2 | Level 1 reconstruction |
| `phil-premise-detect` | Always at Level 2 | charitable reconstruction |
| `phil-conceptual-analysis` | a term carries argumentative weight | Level 1 reconstruction |
| `phil-distinction-track` | the argument relies on a conceptual distinction | Level 1 reconstruction |

Run charity before implicit-premise detection. The two conceptual tasks may run in parallel after Level 1. If the scan finds no material concept or distinction, record an explicit `skip` rather than generating an empty section.

### Level 3: Contextual and Domain Coverage

Include Levels 1-2, then run only missing coverage among:

| Skill or dimension | Trigger |
|---|---|
| `phil-contextualize` | Always at Level 3 |
| `phil-dialectical-map` | Always at Level 3 |
| `phil-modal-arg` | modal operators or modal inference matters to the conclusion |
| `phil-thought-experiment` | a hypothetical case does argumentative work |
| `phil-intuition-pump` | the case is used to elicit a judgment supporting an inference |
| `phil-ontological-commitment` | ontological commitment or category claims |
| `phil-identity-persistence` | identity across time or worlds |
| `phil-grounding-check` | grounding, realization, constitution, or supervenience |
| `phil-conceivability-arg` | conceivability-to-possibility reasoning |
| `phil-causation-analyze` | a substantive causal explanation or exclusion claim |
| `phil-essence-detect` | essence, necessity, or accidental-property reasoning |
| `phil-natural-kind-analyze` | natural-kind classification is inferentially important |
| metaethics skills | only the corresponding moral/normative/semantic/psychological/disagreement/epistemic/supervenience feature is present |

`--full` / `--deep` runs every applicable general and detected domain dimension despite a missing efficiency trigger. It only covers detected dimensions: it does not invent a domain analysis where the text contains no relevant claim, and records those dimensions as not applicable.

## Skill Material Loading

Load a selected skill's operational instructions before running it. Do not load its examples, extended checklists, historical surveys, or reference files during the preplan. Read those materials only when the selected dimension requires them to resolve an identified ambiguity, classify a live case, or meet a caller's explicit request. Reused coverage does not justify reopening the source or loading the corresponding skill materials.

## Output Format

Generate an integrated Chinese report with:

1. Preplan and coverage ledger: target, source/artifact status, and `reuse`/`run`/`skip` decisions.
2. Executive summary and argument reconstruction.
3. Only the Level 2 and Level 3 sections actually run or reused, each labeled with its coverage status.
4. Domain-specific findings only where triggered or explicitly requested.
5. Open questions and remaining coverage gaps.

When persisting under `Private/Bibliography/Analysis/`, include `source_bib_key` and compact `philosopher_observations[]` conforming to `philosopher-observation-schema.json`. Refresh the paired `.analysis.meta.json` according to `analysis-metadata-schema.json`: record the current source and analysis hashes, target level, canonical actual-coverage IDs, workflow version, and verification status. New or partially checked reports are `provisional`; set `verified` only after the declared coverage has been checked against the current source. Reuse valid contextualization rather than rereading the source to recreate unchanged metadata. Then record the artifact with `philosopher-db.py observe --analysis-level <current INDEX level> --input <analysis-file>`. Ad-hoc reports do not update the queue.

## Notes

- Write all output in Chinese.
- State which features triggered each optional dimension and why absent dimensions were skipped.
- The result is a primary input to `/phil:evaluate` and `/phil:write draft`.
- Philosopher observations create private review candidates only; they never overwrite canonical claims.
