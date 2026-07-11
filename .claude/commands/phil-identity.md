---
description: "Analyze identity conditions and persistence claims"
---

# /phil-identity

Loads the `phil-identity-persistence` skill to analyze claims about what makes something the same thing over time, across possible worlds, or under counterfactual change.

## Usage

```
/phil-identity [text or argument reference]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) is recommended to isolate the identity claims in standard form.

## Behavior

1. Identifies all identity claims and persistence conditions in the argument — diachronic, synchronic, and modal
2. Applies Leibniz's Law systematically to test for indiscernibility violations
3. Classifies each identity claim by type: numerical vs. qualitative, sortal-relative, strict vs. contingent, constitution vs. identity
4. Diagnoses the puzzle structure behind each claim — Theseus's ship, statue/lump, fission cases, personhood criteria
5. Evaluates the adequacy of proposed identity criteria against puzzle cases from the literature
6. Outputs the identity and persistence analysis report

## Notes

- References: `glossary-metaphysics.md`, `metaphysical-distinctions.md`
- Cross-domain: Interfaces with `phil-ontological-commitment` (identity claims presuppose ontological commitments to the entities identified) and `phil-modal-arg` (transworld identity involves modal reasoning)
- Distinguishes epistemic criteria for reidentification from metaphysical constitution of identity
