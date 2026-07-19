---
name: source-command-evaluate
description: "Cost-aware critical evaluation of philosophical texts — always runs a lightweight inference and fallacy baseline, then selects only feature- or intent-relevant dimensions unless full coverage is requested"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->

## Codex Runtime Adapter

- Treat `phil:evaluate` and `$source-command-evaluate` as the same public workflow.
- Resolve project guidance in this order: `PROJECT.md`, `AGENTS.md`, then `CLAUDE.md`.
- Normalize `claude-led` and `codex-led` to `assistant-led`, report the alias as deprecated, and use `[AI 补全]` for new disclosures.
- When delegation is available, parallelize only independent stages; otherwise execute the same dependency order serially.
- Apply the capability and Zotero degradation rules in `Framework/Workflow/Rules/runtime-compatibility.md`.

# /phil:evaluate

## Usage

```
/phil:evaluate <text or argument>
/phil:evaluate --full <text or argument>
```

`--deep` is an alias for `--full`. The command works best with a valid `/phil:reconstruct` artifact, but it must not require a full reconstruction merely to identify ordinary inferential defects.

## Role

Critically evaluate another author's existing text in Chinese while avoiding an automatic seven-dimension critique. Produce a baseline inference/fallacy assessment first, then add only dimensions supported by the argument's features or the caller's stated evaluative purpose.

## Feature Classification, Deterministic Preplan, and Reuse

Before loading optional skill material, use the current execution model once to classify only the argument features needed by the evaluation table. Do not invoke an analysis skill or load examples/checklists for this classification. Pass those flags and the caller intent to `workflow-policy.py evaluation-plan`; the planner is deterministic given those inputs and does not interpret the text itself. Treat an ambiguous feature as present, and make the classification exhaustive for `--full` / `--deep`.

Report the planner's current input hash, current analysis-artifact hash when supplied, reconstruction coverage, detected features, caller intent, and each dimension's `reuse`, `run`, or `skip` decision, selector, and reason.

Use reconstruction findings only when their recorded source hash matches the current input hash, their recorded analysis hash matches the current analysis artifact, and their declared coverage is valid. A source or analysis hash mismatch makes those findings stale: do not reuse them, and do not silently treat an old report as a substitute for current analysis. Reuse only the specific valid sections needed by the chosen dimension; never rerun a reconstruct dimension merely because evaluate was called.

## Baseline: Always Run

Perform a lightweight inference and fallacy scan. Use a valid argument reconstruction when available; otherwise identify only the minimum thesis, premises, and inferential links needed to assess support. Check for material logical gaps, equivocation, circular support, illicit shifts in burden, and applicable entries from `fallacy-catalog.md`. This baseline is not a substitute for `phil-counterexample` or `phil-dialectical-map`.

## Targeted Dimensions

After the baseline, select dimensions independently. Selected dimensions with no interdependencies may run in parallel.

| Dimension | Skill | Run when |
|---|---|---|
| Counterexample testing | `phil-counterexample` | the caller asks for stress-testing, a contested premise is identifiable, or the baseline exposes a vulnerable generalization |
| Dialectical mapping | `phil-dialectical-map` | the text develops objections/responses, or the caller asks for dialectical structure |
| Analogy assessment | `phil-analogy-check` | the argument relies on a source-target analogy |
| Parity assessment | `phil-parity-check` | it claims parity, symmetry, or a companions-in-guilt move |
| Intuition-pump analysis | `phil-intuition-pump` | a thought experiment is intended to elicit a supporting judgment |
| Methodological audit | `phil-methodology` | methodology is explicit, contested, or material to the inference |

`--full` / `--deep` always adds counterexample stress-testing after the baseline and runs every other applicable detected dimension in the table. A dimension with no corresponding feature remains not applicable rather than receiving a generic boilerplate section.

## Skill Material Loading

Read a selected skill's operational instructions before use. Keep examples, long checklists, historical surveys, and reference documents unloaded unless they are necessary to assess a live feature, resolve a classification ambiguity, or were explicitly requested. Do not load a skill merely to confirm that a preplan has skipped it.

## Output Format

Generate an integrated Chinese evaluation report containing:

1. Preplan: input/artifact validity, detected features, caller intent, and `reuse`/`run`/`skip` decisions.
2. Inference and fallacy baseline, ranked by seriousness.
3. One labeled section for each selected or reused targeted dimension.
4. A short list of the 3-5 highest-priority revisions, tied to the relevant baseline or selected-dimension finding.
5. Explicit coverage gaps and not-applicable dimensions.

Do not emit empty analogy, parity, intuition, methodology, counterexample, or dialectical sections solely to preserve a fixed report shape.

## Notes

- Write all output in Chinese.
- `/phil:evaluate` assesses the argumentative quality of others' texts; `/phil:review` is peer review of one's own paper.
- A valid reconstruct result may be reused selectively, including its intuition-pump finding; stale results may not be reused.
