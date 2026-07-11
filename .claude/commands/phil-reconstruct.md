---
description: Argument Reconstruction — Convert arguments in philosophical texts into standard premise-conclusion form
---

# /phil-reconstruct

Loads the `phil-argument-reconstruct` skill to perform argument reconstruction on user-provided text.

## Usage

```
/phil-reconstruct <text>
```

Or provide text first, then trigger with `/phil-reconstruct`.

## Behavior

1. Follows the 7-step process defined in SKILL.md to reconstruct arguments in the input text
2. Outputs a standard argument reconstruction report (premise-conclusion structure, implicit premises, logical form, structural assessment)
3. If the text contains no reconstructable argument, outputs "No reconstructable argument detected"

## Notes

- Supports both Chinese and English input
- Supports all argument types: deductive, inductive, reductio, abductive, analogical, dilemma, etc.
- Recommended to follow up with `/phil-premises` (implicit premise detection) and `/phil-charity` (principle of charity check)
