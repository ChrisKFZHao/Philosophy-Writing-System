---
description: "Analyze grounding, supervenience, and dependence relations"
---

# /phil-grounding

Loads the `phil-grounding-check` skill to analyze claims about what grounds what, supervenience relations, and ontological dependence structures in an argument.

## Usage

```
/phil-grounding [text]
```

Prerequisite: An ontological commitment report (`/phil-ontology`) is strongly recommended to establish the entity inventory before mapping dependence relations.

## Behavior

1. Scans the argument for grounding claims — explicit ("in virtue of," "because," "makes it the case that") and implicit dependence relations
2. Classifies each dependence relation by type: full grounding, partial grounding, supervenience, ontological dependence, conceptual dependence
3. Traces grounding chains to identify fundamental entities and detect circular or infinite grounding regresses
4. Evaluates whether supervenience claims are adequately explained or left as brute
5. Maps the argument's grounding architecture — a directed graph of what depends on what, with fundamentality assignments
6. Outputs the grounding and dependence analysis report

## Notes

- References: `metaphysical-distinctions.md`, `glossary-metaphysics.md`
- Cross-domain: Depends on `phil-ontological-commitment` for entity inventory; feeds into `phil-moral-supervenience` for the moral-to-natural supervenience special case
- Distinguishes metaphysical grounding from epistemic justification and causal explanation
