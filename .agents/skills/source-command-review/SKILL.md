---
name: source-command-review
description: "Peer review of philosophical papers — invokes the phil-reviewer agent, 8-dimension review + perspective simulation (Quinean/Lewisian/Kripkean etc.)"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->

## Codex Runtime Adapter

- Treat `phil:review` and `$source-command-review` as the same public workflow.
- Resolve project guidance in this order: `PROJECT.md`, `AGENTS.md`, then `CLAUDE.md`.
- Normalize `claude-led` and `codex-led` to `assistant-led`, report the alias as deprecated, and use `[AI 补全]` for new disclosures.
- Read `Framework/Workflow/Roles/phil-reviewer.md` completely and adopt that role before executing the workflow.
- Apply the session-scoped cost-aware delegation policy in `Framework/Workflow/Rules/runtime-compatibility.md`. On the first eligible task in this session, ask once whether to use a lower-cost host candidate and which candidate to reuse; retain that choice only for this session. If the user revokes it, do not ask or delegate again in this session.
- An eligible task is repeatable, independent, read-only, non-interactive, and returns only a discardable candidate artifact. The parent task must validate it before any artifact write or Citation Gate use.
- Never delegate writing, review, Citation Gate work, bibliography or project changes, or workflow orchestration to the lower-cost candidate. If it is unavailable or insufficient, retain the current session model rather than selecting another candidate automatically. Do not claim a lower-cost candidate is optimal without host-provided evidence.
- Apply the capability and Zotero degradation rules in `Framework/Workflow/Rules/runtime-compatibility.md`.

# /phil:review

## Usage

```
/phil:review <manuscript>
```

## Role

Reviewing **one's own writing**. Invokes the `phil-reviewer` agent to provide a simulated peer-review experience.

## Orchestration

| Component | Description |
|------|------|
| Agent | `phil-reviewer` |
| Review dimensions | 8: argumentative integrity, conceptual precision, dialectical awareness, modal accuracy, distinction preservation, counterexample resilience, ontological clarity, methodological appropriateness |
| Perspective simulation | Optional: review from a specific philosopher's perspective (Quinean / Lewisian / Kripkean / Williamsonian / Parfitian) |

## Output Format

Standard review report containing:
1. Overall assessment
2. Dimension-by-dimension scores and comments
3. Major issues (ranked by severity)
4. Minor issues
5. Revision recommendations (ranked by priority)

## Notes

- Difference from `/phil:evaluate`: review targets one's own manuscript and provides constructive revision suggestions; evaluate targets others' texts and provides critical analysis
- Difference from `/phil:comment`: review is whole-paper review; comment focuses on argument details and conceptual clarification
- Write all output in Chinese (project convention)
- Output format follows the review report template in `Framework/Workflow/Templates/`
