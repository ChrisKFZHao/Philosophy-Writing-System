---
description: "Analyze moral knowledge claims and justification pathways"
---

# /phil-moral-epistemology

Loads the `phil-moral-epistemology` skill to evaluate claims about how moral knowledge is possible, what justifies moral beliefs, and the epistemology of moral inquiry.

## Usage

```
/phil-moral-epistemology [text]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) and a moral realism analysis (`/phil-moral-realism`) provide context.

## Behavior

1. Identifies epistemic claims about moral knowledge — "we know that," "it is justifiable that," "we have reason to believe," appeals to moral intuition
2. Classifies the argument's epistemology: intuitionist, coherentist, foundationalist, reliabilist, constructivist, or skeptical
3. Evaluates the proposed justification pathway: perceptual model, rational intuition model, coherence model, reflective equilibrium, or evolutionary reliability
4. Analyzes the argument's response to canonical moral epistemology challenges: evolutionary debunking, disagreement as epistemic defeater, queerness as epistemic barrier, the regress problem for moral justification
5. Determines whether the argument's epistemology is consistent with its metaethical position — e.g., non-naturalism paired with perceptual epistemology is a mismatch
6. Outputs the moral epistemology analysis report

## Notes

- References: `glossary-metaethics.md`, `metaethical-distinctions.md`
- Cross-domain: Closely tied to `phil-moral-realism` (epistemic access constrains viable realism) and `phil-moral-disagreement` (disagreement as epistemic defeater)
- Distinguishes epistemic questions about how we know moral truths from metaphysical questions about what moral truths are
