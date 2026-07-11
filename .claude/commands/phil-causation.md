---
description: "Identify theoretical affiliations of causal claims"
---

# /phil-causation

Loads the `phil-causation-analyze` skill to identify the theoretical commitments and structural features of causal claims in an argument.

## Usage

```
/phil-causation [text]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) provides the standard-form causal claims for analysis.

## Behavior

1. Scans for all causal locutions — "causes," "because" (causal), "brings about," "due to," "effect of," counterfactual conditionals with causal import
2. Classifies each causal claim against the major theories of causation: counterfactual (Lewis), regularity (Hume, Mackie), probabilistic (Suppes), process (Salmon, Dowe), interventionist (Woodward), mechanistic
3. Determines whether the argument presupposes a particular theory of causation or remains theoretically neutral
4. Analyzes the structural features of each causal claim: type/token, positive/negative, direct/mediated, deterministic/probabilistic, singular/general
5. Evaluates whether the causal relations invoked are consistent with the argument's broader metaphysical commitments
6. Outputs the causation analysis report

## Notes

- References: `causation-taxonomy.md`, `glossary-metaphysics.md`
- Cross-domain: Interfaces with `phil-grounding-check` (distinguishing causal from non-causal dependence) and `phil-moral-psychology` (causal vs. rationalizing explanations of moral judgment)
- Identifies where causal claims are doing work better done by grounding or constitutive explanation
