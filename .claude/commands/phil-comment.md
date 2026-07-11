---
description: Philosophy Commentator — Critical engagement: uncover assumptions, identify alternative interpretations, map missing distinctions
---

# /phil-comment

Loads the `phil-commentator` agent to critically engage with a philosophical work.

## Usage

```
/phil-comment [mode: critical|response:<stance>|position] [work]
```

## Behavior

1. Engages the phil-commentator agent in the specified mode
2. **Critical Commentary** (`critical`): Comprehensive critical engagement identifying unexamined assumptions, missing distinctions, undefended inferences, hidden commitments, and dialectical blind spots. Outputs a structured commentary report.
3. **Response Paper** (`response:<stance>`): Writes a response from a specified philosophical position. Produces a reply article (2,000-5,000 characters in Chinese).
4. **Dialectical Positioning** (`position`): Situates the work within the broader philosophical debate landscape — identifies which debates it intervenes in, where it stands relative to major camps, and what its intellectual lineage is.
5. All modes operate on the principle of hermeneutic charity: understand before criticizing.

## Notes

- Works with published papers, manuscript drafts, or phil-* analysis outputs
- Distinct from `/phil-review`: commentary engages and extends; review assesses and grades
- Useful as a supplementary perspective during the writing pipeline (Stage 5 of `/phil-pipeline`)
