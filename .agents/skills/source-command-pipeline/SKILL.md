---
name: source-command-pipeline
description: "One-command full pipeline — invokes the phil-orchestrator agent, 6 stages: topic orientation & reading plan → reading & analysis → conception incubation → outline → draft & iterative revision → review & final, with a lenient-interrogation quality gate at each stage"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->

## Codex Runtime Adapter

- Treat `phil:pipeline` and `$source-command-pipeline` as the same public workflow.
- Resolve project guidance in this order: `PROJECT.md`, `AGENTS.md`, then `CLAUDE.md`.
- Normalize `claude-led` and `codex-led` to `assistant-led`, report the alias as deprecated, and use `[AI 补全]` for new disclosures.
- Read `Framework/Workflow/Roles/phil-orchestrator.md` completely and adopt that role before executing the workflow.
- When delegation is available, parallelize only independent stages; otherwise execute the same dependency order serially.
- Apply the session-scoped cost-aware delegation policy in `Framework/Workflow/Rules/runtime-compatibility.md`. On the first eligible task in this session, ask once whether to use a lower-cost host candidate and which candidate to reuse; retain that choice only for this session. If the user revokes it, do not ask or delegate again in this session.
- An eligible task is repeatable, independent, read-only, non-interactive, and returns only a discardable candidate artifact. The parent task must validate it before any artifact write or Citation Gate use.
- Never delegate writing, review, Citation Gate work, bibliography or project changes, or workflow orchestration to the lower-cost candidate. If it is unavailable or insufficient, retain the current session model rather than selecting another candidate automatically. Do not claim a lower-cost candidate is optimal without host-provided evidence.
- Apply the capability and Zotero degradation rules in `Framework/Workflow/Rules/runtime-compatibility.md`.

# /phil:pipeline

## Usage

```
/phil:pipeline <research question or topic>
```

## Positioning

One-command, end-to-end philosophy paper production. Invokes the `phil-orchestrator` agent.

## Orchestration

| Component | Description |
|------|------|
| Agent | `phil-orchestrator` |

## 6-Stage Process

| Stage | Content | Quality Gate |
|------|------|--------|
| 1. Topic Orientation & Reading Plan | Scope the dispute + assemble a library-grounded reading plan | Topic is determinate enough to direct reading; reading list covers the debate's core positions |
| 2. Reading & Analysis | Ground the topic in the literature (`phil-tutor` reading mode + analysis skills) | User can state each core source's thesis and main argument in their own words |
| 3. Ideation / Conception Incubation (构思孵化) | Incubate the user's own thesis and argument sketch (`phil-tutor` incubating mode) → `{topic}-conception.txt` | User states their own thesis and argument line, positioned against named interlocutors |
| 4. Outline | Structure the paper's argument (`phil-writer` outline mode, consuming the conception file) | Argument flow is logically valid; user defends 1–2 structural choices |
| 5. Draft & Iterative Revision | Section-by-section production under the chosen collaboration mode (`phil-writer` draft mode) | 7 prose standards met; boundary-interrogation record complete |
| 6. Review & Final | Review-revision cycles to a polished manuscript (`phil-reviewer` + `phil-writer` revision mode) | Fatal findings resolved; user approves |

All gates are **dialogic lenient-interrogation gates**, not hard blocks: a nameable defect in the user's work triggers a challenge; a gap short of a defect is filled charitably with an explicit `[AI 补全]` disclosure; the user may always proceed, and any override or skip is recorded (see Rule 1 §Workflow Gates in `Framework/Workflow/Rules/socratic-engagement.md`). There is no "loop until the gate passes" hard requirement — the orchestrator recommends, the user decides.

## Notes

- **Resume cheaply**: At entry, query `{topic}-workflow-state.json` with `project-state.py status`. Reuse only hash-current registered artifacts; report stale artifacts and rerun only the stage that owns them.
- **Persist transitions**: After a gate decision or completed artifact, update the compact workflow state (stage, status, next action, gate decision, and artifact hash). This state is operational and never triggers a manuscript version cut.
- **Resurface cheaply and only on events**: Do not scan the idea ledger at stage entry, exit, or a quality gate. A named event (`new-evidence`, `related-objection`, `scope-change`, `argument-stall`, `defect-resolved`, `alternative-failed`, or `user-request`) may call `idea-ledger.py candidates` with the event's keywords and bibliography KEYs. Treat its at-most-two results as a deterministic prefilter; present only ideas the specialist judges would materially alter the present argument, then `mark-surfaced`. Preserve each idea's status; reactivation requires the user's explicit confirmation. Parked ideas follow their declared triggers; rejected ideas are eligible only for `defect-resolved` or explicit `user-request`, and superseded ideas only for `alternative-failed` or `user-request`.

- **Stage 0 prerequisite** (outside the pipeline): sources must already be ingested via `/phil:ingest` before the pipeline begins — the orchestrator directs the user there if a referenced source is missing from `Private/Bibliography/INDEX.md`.
- Stages internally invoke `/phil:reconstruct`, `/phil:evaluate`, `/phil:review`, `/phil:tutor` (reading and incubating modes), and `/phil:write` as needed
- **Stage 5 begins by selecting the collaboration mode**: the orchestrator reads the `collaboration:` key from the project's guidance file (PROJECT.md, falling back to AGENTS.md or CLAUDE.md), or asks the user once (`user-led` / `assistant-led`) — see `phil-writer`'s Draft mode.
- ARS capabilities may be invoked selectively (deep-research, citation-check, format-convert; requires the external ARS plugin)
- Write all output in Chinese (project convention)
