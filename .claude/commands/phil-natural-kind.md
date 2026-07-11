---
description: "Analyze natural kind classification arguments"
---

# /phil-natural-kind

Loads the `phil-natural-kind-analyze` skill to evaluate arguments about natural kind membership, kind essences, and the realism/conventionalism debate about kinds.

## Usage

```
/phil-natural-kind [text]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) and an ontological commitment report (`/phil-ontology`) provide the structured input for kind analysis.

## Behavior

1. Identifies all kind terms and classification claims in the argument — natural kinds, social kinds, artifactual kinds, biological taxa
2. Classifies each kind claim against the major theories: Kripke-Putnam causal reference, Boyd's homeostatic property cluster theory, Dupré's promiscuous realism, conventionalism about kinds
3. Determines the argument's stance on kind realism vs. conventionalism and essentialism vs. anti-essentialism about each kind invoked
4. Tests whether kind membership conditions are adequately specified — are they epistemically accessible? Do they support induction and explanation?
5. Evaluates whether the argument's use of kinds is consistent across different domains (physical, biological, psychological, social)
6. Outputs the natural kind analysis report

## Notes

- References: `ontological-categories.md`, `glossary-metaphysics.md`
- Cross-domain: Depends on `phil-ontological-commitment` for identifying which commitments are to kinds; interfaces with `phil-essence-detect` for kind essentialism claims
- Distinguishes natural kind classification from merely conventional or pragmatic grouping
