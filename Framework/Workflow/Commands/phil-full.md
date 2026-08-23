---
name: phil-full
description: "Full-pipeline state machine — start, status, resume. Orchestrates the four skills through persisted v2 workflow state from intake to citation closure."
kind: command
---

# phil:full

One-command, end-to-end philosophy paper production as a **state machine**, not a fifth skill. This specification references the four skills' contracts and never duplicates their protocols. It owns: stage sequencing, approval gates, artifact-state persistence, and resume semantics. Requires an existing writing project (`Private/Projects/{topic}/`).

## Usage

```
phil:full start <research question or topic>
phil:full status
phil:full resume
```

## Stages

`intake -> research -> [incubation] -> outline -> section_brief -> draft -> section_audit -> review -> revision -> citation_closure -> complete`

| Stage | Delegates to | Gate to advance |
|---|---|---|
| `intake` | this command | deliverable + collaboration mode resolved and recorded |
| `research` | `phil:research reconstruct` (+ `evaluate` as needed) | user can state each core source's thesis and main argument in their own words |
| `incubation` (conditional) | `phil:tutor incubating` | `approvals.conception = accepted` (or explicitly `waived`) |
| `outline` | `phil:write outline` | `approvals.outline = approved` (or `waived` with recorded user instruction) |
| `section_brief` | `phil:write draft` (brief phase) | every section has a brief |
| `draft` | `phil:write draft` | all sections drafted; boundary interrogation complete |
| `section_audit` | `phil:write` audit step | machine verdict recorded; unresolved high-severity findings block `complete` until resolved or explicitly deferred with reason |
| `review` | `phil:review` | review report produced; `approvals.review` records the user's editorial decision |
| `revision` | `phil:write revision` | finding ledger driven; no finding silently resolved |
| `citation_closure` | `phil:write` closure step + `Services/citation-gate.md` | machine PASS + user acknowledgement (`approvals.citation_closure`) — **cannot be waived** |
| `complete` | — | run complete |

All dialogue gates are **lenient-interrogation gates** (Rule 1 §Workflow Gates), not hard blocks: a nameable defect triggers a challenge; a gap short of a defect is filled charitably with `[AI 补全]` disclosure; the user may always proceed, and any override or skip is recorded. The orchestrator recommends; the user decides.

## Stage notes

- **Prerequisite (outside the state machine)**: sources must already be ingested (`phil:research ingest`) before `research` begins; direct the user there if a referenced source is missing from `Private/Bibliography/INDEX.md`.
- **`incubation` is conditional**: if intake finds no current conception artifact, invoke `phil:tutor incubating`, record the returned conception artifact and hash, enter `awaiting_user`, and proceed only after `approvals.conception = accepted`. A valid current conception is reused; an explicit skip records `waived` (requires an explicit user instruction). Standalone incubating and the pipeline use the same skill contract — this command consumes its artifact and never duplicates the dialogue protocol.
- **`research`** internally invokes `phil:research reconstruct`/`evaluate` and may use `phil:tutor` reading mode; it follows those skills' contracts.
- **`draft` begins by resolving the collaboration mode**: explicit user instruction → `PROJECT.md` → `user-led` (recorded in state; a later change needs explicit authorization and a recorded transition). Both modes share identical quality gates; they differ only in authorship identity and modification authority.

## State (schema v2)

Persisted in `{topic}-workflow-state.json` (`Contracts/workflow-state.schema.json`, maintained via `Scripts/project-state.py`). Fields: `schema_version`, `project`, `run_id`, `entrypoint`, `stage`, `status`, `collaboration_mode`, `artifacts[]` (kind, POSIX-relative path, SHA-256, status), `approvals` (`conception?`, `outline`, `review?`, `citation_closure?`), `review_findings[]`, `section_audit?`, `next_action`, `updated_at`.

**Status values**: `not_started`, `in_progress`, `awaiting_user`, `blocked`, `stale`, `completed`. **Outline decisions**: `pending`, `approved`, `rejected`, `waived`. **Conception decisions**: `pending`, `accepted`, `waived` (waiver requires an explicit user instruction; a rejected conception returns to incubation dialogue, recorded as continued `pending`). **Review decisions**: `pending`, `accept`, `minor`, `major`, `reject`. **Finding states**: `open`, `accepted`, `rejected`, `resolved`, `deferred`.

Rules:

- `status` is read-only and reports the next valid action; it is derived, never hand-set.
- **`start` must not overwrite an unfinished run**: report the existing state and direct the user to `resume`. A completed run may start a new `run_id`.
- **`resume` validates artifact hashes before reusing outputs.** A mismatch marks affected artifacts `stale` and the run `stale`, returns to the **earliest affected stage**, and requests renewed confirmation. Reuse only hash-current registered artifacts; report stale ones and rerun only the stage that owns them.
- Transition persistence: after every gate decision or completed artifact, update the compact state (stage, status, next action, decision, artifact hash). This state is operational and never triggers a manuscript version cut.

## Event-driven idea resurfacing

Do not scan the idea ledger at stage entry, exit, or gates. A named event (`new-evidence`, `related-objection`, `scope-change`, `argument-stall`, `defect-resolved`, `alternative-failed`, `user-request`) may call `idea-ledger.py candidates` with the event's keywords and bibliography KEYs; treat the at-most-two results as a deterministic prefilter, present only ideas a specialist judge would materially alter the present argument with, then `mark-surfaced`. Preserve each idea's status; reactivation requires explicit user confirmation. Parked ideas follow their declared triggers; rejected resurface only on `defect-resolved`/`user-request`; superseded only on `alternative-failed`/`user-request`.

## Cost-aware delegation

Session-scoped policy per `Rules/runtime-compatibility.md`: on the first eligible task, ask once whether a lower-cost host candidate may be reused this session; the user may revoke at any time. Eligible work is repeatable, independent, read-only, non-interactive, discardable-candidate work validated by the parent before any write or Citation Gate use. Never delegate writing, review, Citation Gate decisions, bibliography/project changes, user dialogue, or orchestration. If the candidate is unavailable or insufficient, retain the current model.

## Output

All stage output in Chinese (project convention). Each stage reports: what was delegated to which skill, the gate decision and its record, artifact hashes, and `next_action`.
