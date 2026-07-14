---
description: One-command full pipeline — invokes the phil-orchestrator agent, 5 stages: philosophical question → literature review → outline → first draft → final draft, with a quality gate at each stage
---

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

## 5-Stage Process

| Stage | Content | Quality Gate |
|------|------|--------|
| 1 | Philosophical question clarification + position specification | Thesis clarity check |
| 2 | Literature review + analysis | Citation integrity check |
| 3 | Structured outline | Argument logic check |
| 4 | Section-by-section first draft | 7 philosophical prose standards check |
| 5 | Review + revision → final draft | 8-dimension review |

Each stage must pass its quality gate before advancing to the next. On failure, loop through revision until the gate passes or the user manually skips it.

## Notes

- Stages internally invoke `/phil:reconstruct`, `/phil:evaluate`, `/phil:review`, and `/phil:write` as needed
- ARS capabilities may be invoked selectively (deep-research, citation-check, format-convert; requires the external ARS plugin)
- Write all output in Chinese (project convention)
