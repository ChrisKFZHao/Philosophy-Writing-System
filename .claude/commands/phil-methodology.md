---
description: "Identify and evaluate philosophical methodology commitments"
---

# /phil-methodology

Loads the `phil-methodology` skill to detect and evaluate the methodological commitments underlying philosophical arguments, classifying methods using a standard taxonomy and checking for consistency between declared and actual methodology.

## Usage

```
/phil-methodology [argument or text]
```

Prerequisite: It is recommended to first run `/phil-reconstruct` to obtain the argument in standard form, so that methodological signals can be traced to specific argumentative moves.

## Behavior

1. Detects explicit methodological signals: scans for meta-level statements about the author's method, approach, or style of argumentation
2. Identifies implicit methodological commitments by analyzing argument structure: what the author does methodologically, not just what they say they do
3. Classifies each detected method using the standard taxonomy: conceptual analysis, reflective equilibrium, experimental philosophy, genealogy, phenomenology, ordinary language philosophy, transcendental method, formal modeling
4. Checks for methodological consistency: flags tensions between declared and actual methods, or between methods used at different stages of the argument
5. Evaluates method-argument fit: assesses whether the chosen method is well-suited to the argument's target conclusion, given standard methodological norms

## Notes

- Meta-level skill: operates on the methods other skills employ and the methodological choices embedded in arguments, making it a reflective tool for the entire skills ecosystem
- Covers: conceptual analysis, reflective equilibrium, experimental philosophy (x-phi), genealogical method (Nietzschean/Foucauldian), phenomenological method, ordinary language philosophy, transcendental arguments, formal/philosophical-logic modeling
- Cross-domain: Feeds into `phil-charity-check` when methodological assumptions affect interpretative charity, and `phil-dialectic` when methodological disputes between traditions shape dialectical structure
