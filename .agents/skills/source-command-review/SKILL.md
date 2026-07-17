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
