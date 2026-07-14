---
description: Tutor-style dialogue on the literature — asks about your thinking, probes your understanding, surfaces blind spots, recommends readings, and plans next steps
---

# /phil:tutor

## Usage

```
/phil:tutor
```

Just trigger it directly. The agent will greet you and start the conversation on its own.

If you already have a specific question or a text to discuss, you can say it directly:

```
/phil:tutor I'm reading Srinivasan's "Anger", but I'm not sure what the implicit premise in her argument is
```

## Positioning

A **tutor-dialogue** tool for when you are reading the literature. phil:tutor is not an analysis engine (that is phil:reconstruct's job) but a conversation partner — it helps you clarify your thinking, surface blind spots, and decide what to read next.

Relation to phil:reconstruct:
- **reconstruct** does mechanical analysis → decomposes a text into its argumentative structure
- **tutor** does dialogic guidance → helps you understand what that structure means
- Suggested order: read the text first → then discuss with tutor → then analyze in depth with reconstruct

## Agent Used

This command launches the `phil-tutor` agent (defined in `.claude/agents/phil-tutor.md`).

The agent may internally invoke the following skill when needed:
- `phil-citation-extract` — extract citations from the current text for recommendation purposes

## Dialogue Flow

The agent guides the conversation through the following four phases:

| Phase | What the agent does | What you do |
|------|-------------|---------|
| 1: Orientation | Asks what you are reading and what stage you are at | Describe your current reading or question |
| 2: Probing | Socratic questioning to test the depth of your understanding | Answer, reflect, expose blind spots |
| 3: Recommendation | Recommends literature based on the conversation | Assess whether the recommendations fit |
| 4: Planning | Proposes a reading plan and tool suggestions | Confirm or adjust the plan |

You can also skip any phase at any time and ask a specific question directly.

## Notes

- The agent converses in Chinese (project convention); citation metadata remains in English
- Follows the citation integrity rule (Rule 2): no fabricated bibliographic information
- If phil:reconstruct has already been run, tell the agent — it will draw on the analysis results in its probing
- The agent's knowledge sources: Philosophers-DB/ (49 philosophers), argument-forms/ (26 argument forms), Private/Bibliography/INDEX.md (project bibliography)
