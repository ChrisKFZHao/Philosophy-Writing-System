---
description: Philosophy Writing Pipeline — End-to-end workflow: question formulation, literature review, outline, draft, and final manuscript
---

# /phil-pipeline

Loads the `phil-orchestrator` agent to coordinate the complete philosophical writing pipeline across five stages.

## Usage

```
/phil-pipeline [stage: 1|2|3|4|5] [context]
```

## Behavior

1. Engages the phil-orchestrator agent to manage the writing pipeline
2. If no stage is specified, starts from Stage 1 (Philosophical Question Formulation) or resumes from the last completed stage
3. The five stages:
   - **Stage 1 — 哲学提问**: Socratic clarification via metaphysician/metaethicist agents. Output: refined research question with scope.
   - **Stage 2 — 参考文献阅读与分析**: ars-deep-research + phil-* analysis skills + phil-contextualize. Output: literature and analysis package with dialectical map.
   - **Stage 3 — 打磨大纲**: phil-writer (outline mode) + optional phil-reviewer structural check. Output: approved detailed outline.
   - **Stage 4 — 生成初稿**: phil-writer (draft mode) with section-by-section quality checks. Output: complete manuscript draft.
   - **Stage 5 — 生成终稿**: phil-reviewer → phil-writer (revision) → loop until quality threshold met. Output: final manuscript + review reports + revision log.
4. Each stage has a quality gate — the orchestrator recommends advance/revise/return and the user decides
5. The pipeline can be entered at any stage if prior-stage outputs are already available

## Notes

- All writing in Chinese (per project convention)
- Output format: plain text (.txt) for manuscripts, LaTeX (.txt) for papers
- Optional ARS integration at each stage (deep-research, citation-check, format-convert, disclosure)
- To use individual agents directly: `/phil-write`, `/phil-review`, `/phil-comment`
