---
description: Dialectical Mapping — Construct thesis-objection-response dialectical trees to track argumentative evolution
---

# /phil-dialectic

Loads the `phil-dialectical-map` skill to map the dialectical structure of a philosophical debate.

## Usage

```
/phil-dialectic
```

Prerequisite: Arguments in the debate must have been reconstructed (`/phil-reconstruct`).

## Behavior

1. Identifies thesis node T
2. Maps objection chains (O1, O2, ...)
3. Maps response chains (R1, R2, ...)
4. Iterates counter-responses (if any)
5. Assigns dialectical states
6. Outputs a dialectical tree report
