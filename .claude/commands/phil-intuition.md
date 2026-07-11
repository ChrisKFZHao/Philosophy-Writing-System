---
description: "Analyze intuition pumps and the dialectical role of intuitions"
---

# /phil-intuition

Loads the `phil-intuition` skill to dissect intuition pumps and thought experiments, tracing the mechanism from scenario presentation through intuitive judgment to argumentative conclusion, while checking for framing effects and debunking susceptibility.

## Usage

```
/phil-intuition [thought-experiment or intuition-pump text]
```

Prerequisite: It is recommended to first run `/phil-thought` if the intuition is embedded in a full thought experiment. An existing `/phil-premises` report can identify background assumptions shaping the intuitive response.

## Behavior

1. Identifies the pump mechanism: isolates the scenario description, the intuition being elicited, and the judgment the argument needs the reader to form
2. Reconstructs the intuition-to-judgment chain, mapping each step from initial presentation through cognitive processing to the target claim
3. Classifies the intuition type using standard taxonomies: conceptual vs. empirical, immediate vs. reflective, expert vs. folk, positive vs. negative
4. Checks for framing and bias effects: evaluates whether alternative framings, ordering effects, or affect-laden descriptions are doing illicit persuasive work
5. Evaluates debunking susceptibility by testing whether the intuition survives genealogical, evolutionary, or cross-cultural challenge

## Notes

- References: `thought-experiment-templates.md` for structural patterns underlying intuition pumps (especially the "pump," "trap," and "reveal" templates)
- Bridges `phil-thought-experiment` (structural thought-experiment analysis) and `phil-methodology` (methodological role of intuitions in philosophical practice), covering the cognitive-psychological dimension that neither fully addresses
- Cross-domain: Feeds into `phil-moral-epistemology` when intuitions function as moral knowledge sources, and `phil-conceivability` when conceivability intuitions are deployed in modal arguments
