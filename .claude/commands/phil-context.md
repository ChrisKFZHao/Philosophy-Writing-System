---
description: "Situate arguments in debate traditions and intellectual landscapes"
---

# /phil-context

Loads the `phil-context` skill to situate philosophical arguments within their broader debate traditions, mapping rival positions, tracing conceptual genealogies, and assessing the dialectical stakes of the intervention.

## Usage

```
/phil-context [argument text]
```

Prerequisite: It is recommended to first run `/phil-reconstruct` to isolate the core argument. An existing `/phil-dialectic` report provides the internal dialectical structure that `/phil-context` situates within the external landscape.

## Behavior

1. Identifies the argument's explicit targets: authors, positions, schools, or traditions that the argument directly engages or responds to
2. Reconstructs the debate tradition: traces the lineage of the central question, identifying canonical contributions, key turning points, and the current state of play
3. Maps rival positions on the central issue, locating the argument's thesis relative to nearby, contrasting, and opposing views along the relevant spectrum
4. Traces the conceptual history of the key terms deployed in the argument, noting semantic shifts and contested definitions across the tradition
5. Assesses dialectical stakes: what hangs on this argument succeeding or failing, who must revise their view if it stands, and what downstream debates it affects

## Notes

- Distinguished from `/phil-dialectic`: `/phil-dialectic` tracks thesis/objection/reply chains internal to a single argument or exchange; `/phil-context` maps the broader debate landscape, including historical development, institutional context, and inter-school dynamics
- References: `philosophers-db` for biographical and doctrinal information on figures cited or alluded to in the argument
- Cross-domain: Feeds into `phil-charity-check` when historical context affects interpretative charity, and `phil-methodology` when methodological traditions shape debate structure
