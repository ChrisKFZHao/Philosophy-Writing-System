---
description: "Analyze moral-to-natural supervenience and Blackburn's challenge"
---

# /phil-moral-supervenience

Loads the `phil-moral-supervenience` skill to analyze moral-to-natural supervenience claims, the explanatory demand they generate, and the dialectical implications for metaethical positions.

## Usage

```
/phil-moral-supervenience [text]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) and a moral realism analysis (`/phil-moral-realism`) are strongly recommended.

## Behavior

1. Identifies supervenience claims in the argument — explicit ("moral properties supervene on natural properties") or implicit (patterns of covariation that require explanation)
2. Formally characterizes the supervenience relation: strong vs. weak, global vs. local, logical vs. metaphysical vs. nomological necessity
3. Applies Blackburn's supervenience challenge: if moral properties supervene on natural properties with conceptual or metaphysical necessity, what explains this covariation? Realists owe an explanation; anti-realists can treat it as a constraint on consistent moralizing
4. Evaluates the argument's response to the challenge — does it provide an explanation, treat supervenience as brute, or deny the explanatory demand?
5. Maps the dialectical implications: which metaethical positions face the strongest supervenience-incurred explanatory burden, and which can discharge it most easily?
6. Tests whether the argument's supervenience stance generalizes to other domains (normative, aesthetic) or is ad hoc to morality
7. Outputs the moral supervenience analysis report

## Notes

- References: `metaethical-distinctions.md`, `glossary-metaethics.md`
- Cross-domain: Builds on `phil-grounding-check` (supervenience as a dependence relation) and `phil-moral-realism` (explanatory burden varies by realist stance); connected to `phil-normativity` (normative supervenience generalization)
- Core dialectical test: does the argument treat moral supervenience as a metaphysical phenomenon requiring explanation or a conceptual constraint on the practice of moral judgment?
