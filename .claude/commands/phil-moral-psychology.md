---
description: "Analyze moral judgment–motivation relations"
---

# /phil-moral-psychology

Loads the `phil-moral-psychology` skill to analyze claims about the relationship between moral judgment and motivation, internalism vs. externalism, and the psychology of moral agency.

## Usage

```
/phil-moral-psychology [text]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) is recommended to isolate the relevant psychological claims.

## Behavior

1. Identifies psychological claims about moral judgment — what kind of mental state is a moral judgment? Belief, desire, emotion, plan, or hybrid?
2. Classifies the argument's stance on motivational internalism vs. externalism: does moral judgment necessarily motivate, or only contingently?
3. Analyzes the argument's account of the direction of fit for moral judgments — world-to-mind (desire-like) or mind-to-world (belief-like)?
4. Evaluates the argument's treatment of amoralism (the possibility of sincere moral judgment without motivation) as an internalism/externalism diagnostic
5. Maps the argument's implicit moral psychology onto the Humean, Kantian, Aristotelian, or sentimentalist tradition
6. Assesses whether the argument's psychological commitments are empirically plausible or in tension with relevant findings in moral psychology
7. Outputs the moral psychology analysis report

## Notes

- References: `glossary-metaethics.md`, `metaethical-distinctions.md`
- Cross-domain: Interfaces with `phil-moral-realism` (internalism/externalism constraints on realism), `phil-moral-semantics` (psychological vs. semantic expressivism), and `phil-normativity` (motivational vs. normative reasons)
- Distinguishes conceptual claims about the nature of moral judgment from empirical claims about actual human psychology
