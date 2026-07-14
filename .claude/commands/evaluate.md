---
description: Simultaneous multi-angle critique of philosophical texts — runs counterexample generation, dialectical mapping, analogy assessment, parity checking, intuition pump detection, methodological reflection, and fallacy analysis in parallel
---

# /phil:evaluate

## Usage

```
/phil:evaluate <text or argument>
```

Or provide the text first, then trigger `/phil:evaluate`. Works best when given the output of `/phil:reconstruct` as input.

## Role

Simultaneous multi-angle critique of **others' existing texts**. Seven evaluative dimensions run in parallel, producing an integrated critical evaluation report.

## Orchestrated Skills

All 7 skills have no interdependencies and **run in parallel**:

| Skill | Function |
|------|------|
| `phil-counterexample` | Counterexample construction: 6 counterexample types + four-dimensional assessment + dialectical anticipation |
| `phil-dialectical-map` | Dialectical mapping: thesis-objection-response attack-defense tree |
| `phil-analogy-check` | Analogy assessment: source-target correspondence, relevance of shared properties, disanalogy detection |
| `phil-parity-check` | Parity checking: inferential parity, companions-in-guilt, false parity |
| `phil-intuition-pump` | Intuition pump analysis: intuition-to-judgment chains, framing effects, debunking susceptibility |
| `phil-methodology` | Methodological reflection: method classification, consistency checking, alternative methods |
| Fallacy detection | Fallacy scan based on `fallacy-catalog.md` |

## Output Format

Generate an integrated critical evaluation report containing the following sections:

1. **Executive summary**: the 3-5 most serious problems, overall assessment of argumentative force
2. **Counterexample inventory**: ranked by severity, with type, target premise, and dialectical anticipation
3. **Dialectical structure**: ASCII visualization of the attack-defense tree
4. **Analogy assessment**: mapping-adequacy score for each analogical argument
5. **Parity check**: verification results for parity claims
6. **Intuition pump analysis**: framing bias and debunking assessment
7. **Methodological audit**: method classification, consistency, alternatives
8. **Fallacy inventory**: detected logical leaps and fallacies
9. **Improvement recommendations**: the 3-5 key problems the author most needs to address

## Notes

- Write all output in Chinese
- The 7 skills run in parallel; each produces its output independently before the results are merged
- If output from `/phil:reconstruct` already exists, use it directly as input — no re-analysis needed. In that case do not re-run `phil-intuition-pump`; use the intuition pump analysis from reconstruct Stage 2 as input
- Difference from `/phil:review`: evaluate targets the argumentative quality of others' texts; review is peer review of one's own papers
