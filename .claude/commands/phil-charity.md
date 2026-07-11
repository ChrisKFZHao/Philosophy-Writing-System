---
description: Principle of Charity Check — Verify that argument reconstruction has built the strongest version of the original text
---

# /phil-charity

Loads the `phil-charity-check` skill to audit the charitability of an argument reconstruction.

## Usage

```
/phil-charity
```

Prerequisite: Must have obtained an argument reconstruction report via `/phil-reconstruct`.

## Behavior

1. Compares each reconstructed premise against the original text
2. Detects whether a stronger reasonable interpretation exists
3. Generates alternative versions for under-charitable premises
4. Outputs a principle of charity audit report
