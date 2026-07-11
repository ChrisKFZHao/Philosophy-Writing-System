---
description: Implicit Premise Detection — Systematically detect unstated assumptions and hidden conditions in philosophical arguments
---

# /phil-premises

Loads the `phil-premise-detect` skill to detect implicit premises in the standardized form of a reconstructed argument.

## Usage

```
/phil-premises
```

**Prerequisite**: Must have obtained a premise-conclusion structure via `/phil-reconstruct`.
Can be used consecutively: `/phil-reconstruct <text>` then `/phil-premises`.

## Behavior

1. Takes a standard-form argument (numbered premises + conclusion)
2. Checks for gaps across all 7 implicit premise types
3. Outputs a complete detection report (type, gap filled, certainty, rejection impact for each implicit premise)
4. Provides overall assessment and recommended inspection order

## Notes

- Must run `/phil-reconstruct` first to obtain standard form
- Detection results can be passed directly to `/phil-counterexample` (counterexample generation)
