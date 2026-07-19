---
description: "Tutor-style dialogue — two modes. reading (default): asks about your thinking, probes your understanding, surfaces blind spots, recommends readings, and plans next steps. incubating: conception incubation (构思孵化), helping you crystallize your own thesis and argument sketch"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->
# /phil:tutor

## Usage

```
/phil:tutor [mode: reading|incubating] [optional question or context]
```

`reading` is the default mode — just trigger `/phil:tutor` directly and the agent will greet you and start the conversation on its own.

If you already have a specific question or a text to discuss, you can say it directly:

```
/phil:tutor I'm reading Srinivasan's "Anger", but I'm not sure what the implicit premise in her argument is
```

To enter incubating mode explicitly:

```
/phil:tutor incubating
```

## Positioning

A **tutor-dialogue** tool with two purposes, distinguished by mode.

**reading mode** (default): for when you are reading the literature. phil:tutor is not an analysis engine (that is phil:reconstruct's job) but a conversation partner — it helps you clarify your thinking, surface blind spots, and decide what to read next. This is Stage 2 of the writing pipeline (`phil:pipeline`), but also stands alone for everyday literature dialogue outside any pipeline run.

Relation to phil:reconstruct:
- **reconstruct** does mechanical analysis → decomposes a text into its argumentative structure
- **tutor** does dialogic guidance → helps you understand what that structure means
- Suggested order: read the text first → then discuss with tutor → then analyze in depth with reconstruct

**incubating mode**: conception incubation (构思孵化) — Stage 3 of the writing pipeline, sitting between reading (Stage 2) and outline (Stage 4). Once the literature is grounded, incubating mode helps you crystallize your own thesis and argument sketch, in your own words, before any structural outlining begins. Output: `Private/Projects/{topic}/{topic}-conception.txt`, consumed preferentially by `phil:write outline`.

## Agent Used

This command adopts the `phil-tutor` role defined in `Framework/Workflow/Roles/phil-tutor.md`.

The agent may internally invoke the following skill when needed:
- `phil-citation-extract` — extract citations from the current text for recommendation purposes

## Dialogue Flow

### reading mode

The agent guides the conversation through the following four phases:

| Phase | What the agent does | What you do |
|------|-------------|---------|
| 1: Orientation | Asks what you are reading and what stage you are at | Describe your current reading or question |
| 2: Probing | Socratic questioning to test the depth of your understanding | Answer, reflect, expose blind spots |
| 3: Recommendation | Recommends literature based on the conversation | Assess whether the recommendations fit |
| 4: Planning | Proposes a reading plan and tool suggestions | Confirm or adjust the plan |

You can also skip any phase at any time and ask a specific question directly.

### incubating mode

A parallel four-phase arc, oriented toward crystallizing your own position rather than testing comprehension of someone else's:

| Phase | What the agent does | What you do |
|------|-------------|---------|
| 1: Landscape recall | Asks "How do your sources relate? Where do they agree, where do they clash?" | Map the terrain in your own words, drawing on refs.md and Stage 2 analyses |
| 2: Angle probing | Asks "Where do you disagree? What is your entry point?" — no comprehension-quizzing | Stake out a candidate thesis and entry angle |
| 3: Argument sketching | Sketches your main line at premise level, mapping each premise to a supporting refs.md KEY | Confirm, revise, or supply missing premises |
| 4: Conception consolidation | Writes/updates `{topic}-conception.txt`; records substantive parked, rejected, or superseded alternatives in `{topic}-idea-ledger.json` | Confirm the conception, or ask for another round |

Lenient interrogation (Rule 1 §Workflow Gates) governs this dialogue throughout: a nameable defect in the candidate thesis triggers a challenge; gaps short of a defect are filled charitably with an explicit `[AI 补全]` disclosure in the conception file, never silently.

## Notes

- The agent converses in Chinese (project convention); citation metadata remains in English
- In incubating mode, the conception file's content is written in Chinese (output layer), consistent with manuscript conventions
- Follows the citation integrity rule (Rule 2): no fabricated bibliographic information
- If phil:reconstruct has already been run, tell the agent — it will draw on the analysis results in its probing
- The agent's knowledge sources: Philosophers-DB v2 INDEX plus selected source-backed profiles, argument-forms/ (26 argument forms), Private/Bibliography/INDEX.md (project bibliography)
- `{topic}-conception.txt` is freely overwritten and never versioned (Rule 3)
- Do not silently delete a substantive candidate idea during incubation. Record it with `idea-ledger.py`; an idea may become `active` only after explicit user confirmation.
- Cross-stage resurfacing is event-driven, never a stage-boundary scan. Only these named events may query `idea-ledger.py candidates`: `new-evidence`, `related-objection`, `scope-change`, `argument-stall`, `defect-resolved`, `alternative-failed`, and `user-request`. Supply the event's concrete keywords and bibliography KEYs; its deterministic prefilter returns at most two candidates. Parked ideas follow their declared triggers; rejected ideas are eligible only for `defect-resolved` or explicit `user-request`, and superseded ideas only for `alternative-failed` or `user-request`. The model then judges only whether a candidate would materially change the current argument. Present qualifying ideas without changing their status, run `mark-surfaced` after presenting one, and reactivate only after the user explicitly confirms.
