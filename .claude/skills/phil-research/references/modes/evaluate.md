<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Mode contract: evaluate

Read-only targeted critique of another author's text. Cost-aware: a lightweight inference/fallacy baseline always runs; deeper dimensions are selected by the argument's features or the caller's stated intent, not by a fixed bundle.

## Usage

```
phil:research evaluate <text or argument>
phil:research evaluate --full <text or argument>    # --deep is an alias
```

Works best with a valid reconstruct artifact but must not require full reconstruction merely to identify ordinary inferential defects.

## Deterministic preplan

Classify only the argument features needed by the selection table below (no method invocation, no example loading for this). Pass flags and caller intent to:

```bash
python "Framework/Workflow/Scripts/workflow-policy.py" evaluation-plan --intent <i> --feature <f>... [--artifacts ...] [--full]
```

Treat an ambiguous feature as present; exhaustive for `--full`/`--deep`. Report the planner's input hash, current artifact hash when supplied, reconstruction coverage, detected features, caller intent, and each dimension's `run`/`reuse`/`skip` decision, selector, and reason.

Reuse reconstruct findings only when their recorded source hash matches the current input hash, their recorded analysis hash matches the current artifact, and their declared coverage is valid. A mismatch makes findings stale: do not reuse and do not silently substitute an old report. Reuse only the specific valid sections needed; never rerun a reconstruct dimension merely because evaluate was called.

## Baseline (always run)

A lightweight inference and fallacy scan: with a valid reconstruction when available, otherwise identify only the minimum thesis, premises, and inferential links needed to assess support. Check material logical gaps, equivocation, circular support, illicit burden shifts, and applicable `References/fallacy-catalog.md` entries. The baseline is not a substitute for `method.argument.counterexample` or `method.dialectic.dialectical-map`.

## Targeted dimensions (selected independently; independent selections may run in parallel)

| Dimension | Method | Run when |
|---|---|---|
| Counterexample testing | `method.argument.counterexample` | caller asks for stress-testing, a contested premise is identifiable, or the baseline exposes a vulnerable generalization |
| Dialectical mapping | `method.dialectic.dialectical-map` | the text develops objections/responses, or the caller asks for dialectical structure |
| Analogy assessment | `method.argument.analogy-check` | the argument relies on a source-target analogy |
| Parity assessment | `method.argument.parity-check` | it claims parity, symmetry, or a companions-in-guilt move |
| Intuition-pump analysis | `method.concept.intuition-pump` | a thought experiment is intended to elicit a supporting judgment |
| Methodological audit | `method.dialectic.methodology` | methodology is explicit, contested, or material to the inference |

`--full`/`--deep` always adds counterexample stress-testing after the baseline and runs every other applicable detected dimension. A dimension with no corresponding feature stays not applicable — no generic boilerplate sections.

## Loading

Read a selected method's operational instructions before use; keep examples, long checklists, and reference documents unloaded unless needed for a live feature, a classification ambiguity, or an explicit request. Do not load a method merely to confirm the preplan skipped it.

## Output

Integrated Chinese evaluation report: (1) preplan — input/artifact validity, detected features, intent, decisions; (2) inference and fallacy baseline ranked by seriousness; (3) one labeled section per selected or reused dimension; (4) the 3–5 highest-priority revisions tied to the findings; (5) explicit coverage gaps and not-applicable dimensions. Never emit empty dimension sections to preserve a fixed report shape.

`evaluate` assesses others' texts; `phil:review` is peer review of one's own manuscript.
