---
description: "Detect and evaluate essentialist claims"
---

# /phil-essence

Loads the `phil-essence-detect` skill to detect and evaluate claims about essential properties, real definitions, and what something must be to be what it is.

## Usage

```
/phil-essence [text]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) and a conceptual analysis (`/phil-concepts`) provide the structured input for identifying essentialist claims.

## Behavior

1. Scans for essentialist language — "essentially," "by its very nature," "in virtue of what it is to be," "constitutively," "real definition"
2. Classifies each essentialist claim by type: sortal essence, individual essence, dispositional essence, origin essentialism, kind essentialism
3. Applies Fine's modal/essential distinction — is the claim merely about what is necessary, or about what makes the thing what it is?
4. Tests essentialist claims against counterexamples: accidental necessities, converse essentialist attributions, trivializing cases
5. Maps the argument's essentialist commitments onto the modal profile of the entities involved
6. Outputs the essentialist claim analysis report

## Notes

- References: `metaphysical-distinctions.md`, `glossary-metaphysics.md`
- Cross-domain: Connects to `phil-modal-arg` (the modal profile of essential properties) and `phil-natural-kind-analyze` (kind essentialism about natural kinds)
- Distinguishes essentialist claims from merely definitional or conceptual claims per Fine (1994)
