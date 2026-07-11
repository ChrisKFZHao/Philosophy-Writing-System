---
description: "Analyze analogical arguments and reasoning-by-analogy"
---

# /phil-analogy

Loads the `phil-analogy` skill to systematically analyze analogical arguments, mapping source/target domain correspondences, evaluating structural fit, detecting disanalogies, and grading argumentative force.

## Usage

```
/phil-analogy [argument-text or reference to analysis]
```

Prerequisite: It is recommended to first run `/phil-reconstruct` to obtain a standard-form argument reconstruction so that the analogical inference can be located within its dialectical context.

## Behavior

1. Identifies the source domain and target domain, then extracts the full set of asserted correspondences between them
2. Reconstructs the structural mapping: which features of the source are claimed to carry over to the target, and via what inferential path
3. Evaluates the relevance of each mapped feature to the conclusion, distinguishing accidental from essential correspondences
4. Detects disanalogies: features of source or target that resist mapping and may undermine the inference
5. Grades the argument's overall analogical force on a weak-to-strong spectrum, considering structural depth, relevance weight, and disanalogy impact

## Notes

- References: `analogy.md` argument form (source/target domain mapping with structural correspondence inference), `fallacy-catalog.md` for false analogy detection and weak-analogy assessment criteria
- Sibling to `phil-parity`: while `/phil-parity` evaluates relevant-similarity claims in parity arguments, `/phil-analogy` handles the broader class of analogical inferences including predictive and explanatory analogies
- Cross-domain: Feeds into `phil-thought-experiment` when analogies are embedded in thought experiments, and `phil-charity-check` when charitable reconstruction requires analogical strengthening
