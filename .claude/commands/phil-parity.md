---
description: "Check parity/relevant-similarity claims in arguments"
---

# /phil-parity

Loads the `phil-parity` skill to evaluate parity arguments and relevant-similarity claims, including "companions in guilt" strategies, by systematically testing whether alleged similarities withstand differential scrutiny.

## Usage

```
/phil-parity [argument-text or parity claim]
```

Prerequisite: It is recommended to first run `/phil-reconstruct` to isolate the parity premise. An existing `/phil-concepts` report can clarify the respect-of-comparison concept.

## Behavior

1. Extracts the parity relation: identifies what is being compared (A and B) and the claimed respect of similarity R
2. Enumerates the respect of comparison precisely, distinguishing between features that are explicit in the argument and those that are implicitly assumed relevant
3. Inventories all relevant differences between A and B across ontological, epistemic, normative, and functional dimensions
4. Tests whether each difference is relevant to R by evaluating whether it breaks the inference from "X applies to A" to "X should apply to B"
5. Assesses the parity chain: if the argument deploys multiple parity links, checks whether parity is transitive across the chain or degrades at each step

## Notes

- References: `fallacy-catalog.md` for false equivalence detection and relevant-difference criteria, `companions-in-guilt.md` argument form for the canonical parity-argument structure
- Primary use case: "companions in guilt" arguments in metaethics (e.g., moral facts are no more problematic than mathematical facts), but applies to any parity-reasoning across philosophical domains
- Sibling to `phil-analogy`: parity arguments are a special case of analogical reasoning where the inference is specifically "treat A and B the same way"; `/phil-analogy` covers the broader class
