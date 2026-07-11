---
description: Philosophy Reviewer — Domain-specific peer review with 8 review dimensions and configurable philosophical perspectives
---

# /phil-review

Loads the `phil-reviewer` agent to evaluate philosophical manuscripts against discipline-specific standards.

## Usage

```
/phil-review [mode: standard|perspective:<philosopher>] [manuscript]
```

## Behavior

1. Engages the phil-reviewer agent in the specified mode
2. **Standard mode** (`standard`): Evaluates the manuscript across all 8 review dimensions from a neutral stance. Produces a structured review report with severity-graded findings and a revision priority matrix.
3. **Perspective mode** (`perspective:<Quinean|Lewisian|Kripkean|...>`): Reviews from the specified philosophical stance, labeling each finding as perspective-dependent or perspective-neutral.
4. The 8 review dimensions: argument validity, principle of charity, conceptual clarity, modal rigor, counterexample resilience, dialectical completeness, ontological commitment transparency, methodological consistency.
5. Output: structured review report with overall assessment, strengths, dimension-by-dimension findings, revision priority matrix, and publication recommendation.

## Notes

- Can review manuscripts in Chinese or English
- Recommended to run `/phil-write draft` before review, and `/phil-write revision` after receiving the review report
- For a complete writing-review-revise cycle, consider using `/phil-pipeline`
