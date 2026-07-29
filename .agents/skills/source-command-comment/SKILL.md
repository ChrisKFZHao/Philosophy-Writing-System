---
name: source-command-comment
description: "In-depth philosophical commentary — invokes the phil-commentator agent, focusing on argumentative detail: unstated assumptions, alternative readings, missing distinctions, hidden commitments, dialectical blind spots"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->

## Codex Runtime Adapter

- Treat `phil:comment` and `$source-command-comment` as the same public workflow.
- Resolve project guidance in this order: `PROJECT.md`, `AGENTS.md`, then `CLAUDE.md`.
- Normalize `claude-led` and `codex-led` to `assistant-led`, report the alias as deprecated, and use `[AI 补全]` for new disclosures.
- Read `Framework/Workflow/Roles/phil-commentator.md` completely and adopt that role before executing the workflow.
- Apply the session-scoped cost-aware delegation policy in `Framework/Workflow/Rules/runtime-compatibility.md`. On the first eligible task in this session, ask once whether to use a lower-cost host candidate and which candidate to reuse; retain that choice only for this session. If the user revokes it, do not ask or delegate again in this session.
- An eligible task is repeatable, independent, read-only, non-interactive, and returns only a discardable candidate artifact. The parent task must validate it before any artifact write or Citation Gate use.
- Never delegate writing, review, Citation Gate work, bibliography or project changes, or workflow orchestration to the lower-cost candidate. If it is unavailable or insufficient, retain the current session model rather than selecting another candidate automatically. Do not claim a lower-cost candidate is optimal without host-provided evidence.
- Apply the capability and Zotero degradation rules in `Framework/Workflow/Rules/runtime-compatibility.md`.

# /phil:comment

## Usage

```
/phil:comment <argument or text>
```

## Positioning

Deep critical engagement, focused on **argumentative detail and conceptual clarification**.

## Orchestration

| Component | Description |
|------|------|
| Agent | `phil-commentator` |

## Dimensions the Agent Attends To

1. **Unstated assumptions**: Which unstated premises does the argument depend on?
2. **Alternative readings**: Are there other readings that are equally plausible, or even stronger?
3. **Missing distinctions**: Which conceptual distinctions would change the force of the argument but were not considered by the author?
4. **Undefended steps**: Which inferential steps lack adequate support?
5. **Hidden commitments**: Which undeclared philosophical commitments (ontological, semantic, methodological) does the argument presuppose?
6. **Dialectical blind spots**: What are the key objections the author failed to anticipate?

## Output Format

Standard commentary report, containing:
1. Overall impression
2. Dimension-by-dimension analysis
3. Constructive suggestions
4. Directions for further inquiry

## Notes

- Difference from `/phil:review`: comment focuses on argumentative detail and conceptual clarification; review is whole-paper peer review
- Difference from `/phil:evaluate`: comment is deep qualitative analysis; evaluate is multi-dimensional parallel quantitative assessment
- Write all output in Chinese (project convention)
