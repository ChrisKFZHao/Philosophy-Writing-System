---
description: Philosophy Writer — Generate outline, draft, or revision with argument integrity, conceptual precision, and Chinese academic conventions
---

# /phil-write

Loads the `phil-writer` agent to produce philosophical writing in three modes.

## Usage

```
/phil-write <mode: outline|draft|revision> [context]
```

## Behavior

1. Engages the phil-writer agent in the specified mode
2. **Outline mode** (`outline`): Expects a thesis or research question plus analysis context. Outputs a structured outline with thesis, section plan, distinction inventory, and anticipated objections.
3. **Draft mode** (`draft`): Expects an approved outline plus analysis outputs. Writes complete manuscript sections with argument-first prose, technical term precision, and Chinese academic conventions.
4. **Revision mode** (`revision`): Expects a manuscript plus reviewer feedback. Produces a revised manuscript with change log, prioritized by finding type (structural → conceptual → dialectical → modal → stylistic).
5. Output format: plain text (.txt) for manuscripts in `manuscript/`, LaTeX (.txt) for papers in `paper/`.

## Notes

- Writing in Chinese (per project convention)
- Recommended to run phil-* analysis skills before writing for comprehensive input
- The agent applies 7 philosophy-aware prose standards: argument transparency, conceptual precision, modal accuracy, dialectical positioning, distinction preservation, counterexample resilience, ontological explicitness
- Can optionally invoke ARS capabilities (citation-check, format-convert, disclosure) for final polishing
