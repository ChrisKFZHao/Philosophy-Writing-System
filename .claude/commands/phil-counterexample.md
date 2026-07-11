---
description: Counterexample Generation — Construct counterexamples targeting argument premises or inferential chains
---

# /phil-counterexample

Loads the `phil-counterexample` skill to construct counterexamples targeting an argument.

## Usage

```
/phil-counterexample
```

Prerequisite: Must have run `/phil-reconstruct` (and optionally `/phil-premises`).

## Behavior

1. Identifies attack priority (most vulnerable premise first)
2. Constructs targeted counterexamples (6 types)
3. Four-dimension evaluation of each counterexample
4. Anticipates and preempts rebuttals
5. Outputs a counterexample construction and evaluation report
