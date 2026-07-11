---
description: "Evaluate conceivability-to-possibility arguments (zombie arguments etc.)"
---

# /phil-conceivability

Loads the `phil-conceivability-arg` skill to evaluate arguments that infer metaphysical possibility from conceivability, including zombie arguments, inverted spectrum arguments, and disembodiment arguments.

## Usage

```
/phil-conceivability [argument]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) and a modal analysis (`/phil-modal`) provide the structured input needed for precise evaluation.

## Behavior

1. Identifies the form of the conceivability argument — positive (conceivability-to-possibility) or negative (inconceivability-to-impossibility)
2. Classifies the type of conceivability invoked: prima facie, ideal negative, ideal positive, or secondary
3. Applies the Chalmers two-dimensional framework (primary vs. secondary intensions) to assess whether the inference is valid for the relevant kind of possibility
4. Audits for idealization failures, cognitive limitations, and hidden a posteriori necessities that could block the inference
5. Evaluates whether the argument's conceivability claim survives refinement into ideal conceivability
6. Outputs the conceivability argument evaluation report

## Notes

- References: `modal-logic-primer.md`, `glossary-metaphysics.md`
- Cross-domain: Builds on `phil-modal-arg` for modal scope and framework analysis; connects to `phil-identity-persistence` for zombie/consciousness identity questions
- Flags the distinction between conceivability as a guide to logical vs. metaphysical possibility
