---
description: "Analyze the source and structure of normativity"
---

# /phil-normativity

Loads the `phil-normativity` skill to analyze claims about the source, force, and structure of normative reasons and oughts in an argument.

## Usage

```
/phil-normativity [text]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) provides the standard-form normative claims for analysis.

## Behavior

1. Identifies all normative operators in the argument — "ought," "reason," "should," "must," "value," "normative," "justification"
2. Classifies each normative claim by domain: moral, prudential, epistemic, aesthetic, instrumental, rational
3. Determines the argument's stance on the source of normativity: constructivist, realist, expressivist, constitutivist, Humean, Kantian
4. Analyzes the logical structure of normative claims — categorical vs. hypothetical, pro tanto vs. all-things-considered, agent-relative vs. agent-neutral
5. Evaluates whether the argument provides or presupposes an account of normative force — what makes normative claims binding?
6. Maps the argument's position on internalism vs. externalism about normative reasons
7. Outputs the normativity analysis report

## Notes

- References: `normativity-taxonomy.md`, `glossary-metaethics.md`, `metaethical-distinctions.md`
- Cross-domain: Interfaces with `phil-moral-realism` (normative force as queerness component), `phil-moral-psychology` (motivational internalism), and `phil-grounding-check` (normative grounding)
- Distinguishes normative claims about what one ought to do from descriptive claims about what norms people actually accept
