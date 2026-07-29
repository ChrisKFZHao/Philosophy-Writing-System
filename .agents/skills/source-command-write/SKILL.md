---
name: source-command-write
description: "Philosophical writing — invokes the phil-writer agent with three modes: outline (structured outline), draft (section-by-section composition, with user-led/assistant-led collaboration modes), revision (review-driven revision)"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->

## Codex Runtime Adapter

- Treat `phil:write` and `$source-command-write` as the same public workflow.
- Resolve project guidance in this order: `PROJECT.md`, `AGENTS.md`, then `CLAUDE.md`.
- Normalize `claude-led` and `codex-led` to `assistant-led`, report the alias as deprecated, and use `[AI 补全]` for new disclosures.
- Read `Framework/Workflow/Roles/phil-writer.md` completely and adopt that role before executing the workflow.
- Apply the session-scoped cost-aware delegation policy in `Framework/Workflow/Rules/runtime-compatibility.md`. On the first eligible task in this session, ask once whether to use a lower-cost host candidate and which candidate to reuse; retain that choice only for this session. If the user revokes it, do not ask or delegate again in this session.
- An eligible task is repeatable, independent, read-only, non-interactive, and returns only a discardable candidate artifact. The parent task must validate it before any artifact write or Citation Gate use.
- Never delegate writing, review, Citation Gate work, bibliography or project changes, or workflow orchestration to the lower-cost candidate. If it is unavailable or insufficient, retain the current session model rather than selecting another candidate automatically. Do not claim a lower-cost candidate is optimal without host-provided evidence.
- Apply the capability and Zotero degradation rules in `Framework/Workflow/Rules/runtime-compatibility.md`.

# /phil:write

## Usage

```
/phil:write <mode: outline|draft|revision> [collaboration: user-led|assistant-led] [context]
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
- **Preferentially consumes `Private/Projects/{topic}/{topic}-conception.txt`** (the Stage 3 ideation output) when it exists — the writer refines the user's own thesis and argument sketch rather than inventing a replacement. Any substantive deviation from the conception file's thesis is flagged and justified to the user before proceeding. Absent a conception file, falls back to a user-supplied thesis or research question.
- Output: structured outline (thesis, section plan, distinction inventory, anticipated objections)

### Draft mode
- Input: approved outline + analysis outputs
- Output: complete manuscript sections, argument-first prose, Chinese academic conventions

**Collaboration Modes** (dual sub-modes):
- **`user-led`** (严肃学术论文 — serious academic papers): the user writes sections into `{topic}-draft.txt`; per section, the AI assistant gives Socratic feedback triggered only by a nameable defect (Rule 1 §Workflow Gates), offers gap-filling as `[AI 补全]`-disclosed suggestions, and polishes against the 7 prose standards below. The AI assistant edits the draft only to apply changes the user has explicitly accepted — never a silent rewrite.
- **`assistant-led`** (课程论文 — course papers): the AI assistant drafts section-by-section, with **default-on boundary interrogation** — 1–3 ownership questions posed to the user at each section boundary. Skips are recorded in the manuscript's Notes to Self.
- Selection: read the `collaboration:` key from the project's guidance file (PROJECT.md, falling back to AGENTS.md or CLAUDE.md); if absent, ask the user once and suggest recording it. The `[collaboration: user-led|assistant-led]` argument above overrides this for a single invocation.

### Revision mode
- Input: manuscript + reviewer feedback
- Output: revised draft + change log, prioritized by type (structure → concepts → dialectic → modality → style)
- **Collaboration-mode interaction**: in `user-led`, revision mode produces a prioritized change plan plus per-finding suggested edits, which the user implements. In `assistant-led`, current behavior applies, plus: findings that trace back to a user-authored or user-approved choice are asked about (lenient interrogation) before the AI assistant rewrites.

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
- The draft collaboration mode is recorded via a `collaboration:` key in the project-level CLAUDE.md; a per-invocation `[collaboration: ...]` argument overrides it for that call only
- Rule 1 §Workflow Gates (lenient interrogation) governs all boundary interrogation and Socratic feedback in draft and revision modes — a nameable defect triggers a challenge, otherwise gaps are charitably completed with `[AI 补全]` disclosure; gates never hard-block
- Optionally invoke ARS capabilities (citation-check, format-convert; requires the external ARS plugin) for final polishing
