---
description: Philosophical writing — invokes the phil-writer agent with three modes: outline (structured outline), draft (section-by-section composition), revision (review-driven revision)
---

# /phil:write

## Usage

```
/phil:write <mode: outline|draft|revision> [context]
```

## Role

Philosophical paper writing. Invokes the `phil-writer` agent.

## Orchestration

| Component | Description |
|------|------|
| Agent | `phil-writer` |
| Modes | outline (structured outline) / draft (section-by-section composition) / revision (review-driven revision) |

### Outline mode
- Input: thesis or research question + analysis context
- Output: structured outline (thesis, section plan, distinction inventory, anticipated objections)

### Draft mode
- Input: approved outline + analysis outputs
- Output: complete manuscript sections, argument-first prose, Chinese academic conventions

### Revision mode
- Input: manuscript + reviewer feedback
- Output: revised draft + change log, prioritized by type (structure → concepts → dialectic → modality → style)

## 7 Standards of Philosophical Prose

1. Argumentative transparency
2. Conceptual precision
3. Modal accuracy
4. Dialectical positioning
5. Distinction preservation
6. Counterexample resilience
7. Ontological clarity

## Notes

- Write the writing output in Chinese
- Recommended: run the analysis skills (`/phil:reconstruct` + `/phil:evaluate`) before writing
- Optionally invoke ARS capabilities (citation-check, format-convert; requires the external ARS plugin) for final polishing
