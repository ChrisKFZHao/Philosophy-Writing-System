---
description: Modal Argument Analysis — Evaluate the logical structure and inferential validity of possibility and necessity claims
---

# /phil-modal

Loads the `phil-modal-arg` skill to analyze modal claims in arguments.

## Usage

```
/phil-modal
```

Prerequisite: Must have obtained an argument reconstruction report via `/phil-reconstruct`.

## Behavior

1. Scans for all modal operators (possibly/necessarily/conceivably, etc.)
2. Detects modal scope ambiguity (De dicto / De re)
3. Evaluates the implicit modal framework
4. Assesses the conceivability → possibility inference chain
5. Outputs a modal argument analysis report
