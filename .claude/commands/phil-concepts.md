---
description: Conceptual Analysis — Extract, clarify, and test the structure, conditions, and boundaries of philosophical concepts
---

# /phil-concepts

Loads the `phil-conceptual-analysis` skill to perform conceptual analysis on user-provided concepts or text.

## Usage

```
/phil-concepts <concept name or text passage containing concepts>
```

Or provide text first, then trigger with `/phil-concepts`.

## Behavior

1. Follows the 9-step process defined in SKILL.md to analyze the concept
2. Outputs a standard conceptual analysis report (candidate definitions, necessary/sufficient conditions, case testing, distinction mapping, structure typing, dimension analysis)
3. If the text contains no analyzable concept, outputs "No analyzable concept detected"

## Work Modes

- **Initial Analysis** (default): Comprehensive analysis of a new concept
- **Supplementary Analysis**: Add new cases, dimensions, or conditions to an existing concept analysis
- **Concept Engineering** (`/phil-concepts --engineer <concept>`): Propose concept revision based on analysis

## Notes

- Supports both Chinese and English input
- Independent of `/phil-reconstruct`; can be used standalone
- Recommended to use with `/phil-reconstruct` (argument reconstruction) and `/phil-distinctions` (distinction tracking)
