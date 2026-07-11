---
description: "Check ontological commitments of an argument"
---

# /phil-ontology

Loads the `phil-ontological-commitment` skill to detect and classify the ontological commitments presupposed by an argument using Quine's criterion and a systematic category taxonomy.

## Usage

```
/phil-ontology [argument-text or reference to analysis]
```

Prerequisite: It is recommended to first run `/phil-reconstruct` to obtain a standard-form argument reconstruction. An existing `/phil-premises` report can enrich implicit commitment detection.

## Behavior

1. Extracts all quantified statements from the reconstructed argument and applies the Quinean bound-variable criterion
2. Classifies each detected commitment into the ontological category taxonomy (concrete particular, abstract object, property, fact, event, etc.)
3. Assesses each commitment by explicitness level, controversiality rating, and available paraphrastic escape strategies
4. Compiles a full ontological profile including parsimony assessment, category breakdown, and dialectical implications
5. Outputs the ontological commitment report

## Notes

- References: `ontological-categories.md`, `glossary-metaphysics.md`
- Cross-domain: Feeds into `phil-grounding-check` (grounding relations depend on ontological inventory) and `phil-natural-kind-analyze` (kind commitments require category classification)
- Also surfaces presuppositional and truthmaker-based commitments that go beyond explicit quantificational structure
