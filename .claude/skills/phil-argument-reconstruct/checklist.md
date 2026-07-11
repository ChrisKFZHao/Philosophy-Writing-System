# Argument Reconstruction Quality Checklist

> After each argument reconstruction, check each item. A fully checked list indicates a high-quality reconstruction.

---

## Structural Checks

- [ ] **Distinction between premises and conclusion**: Is it clear which statements are premises and which is the conclusion?
- [ ] **Premise independence**: Is each premise an independent, complete declarative sentence that does not depend on the interpretation of other premises?
- [ ] **No omissions**: Have all statements in the source text that bear inferential weight been covered?
- [ ] **No additions**: Have no statements been added that are not in the source text and are not implicit premises?
- [ ] **Conclusion location**: Has the position of the conclusion in the source text (at the beginning or end) been noted?

## Implicit Premise Checks

- [ ] **Necessity**: Is each implicit premise genuinely required for the argument to hold? (If the argument would still be valid without it, it is not a genuine implicit premise)
- [ ] **Textual clues**: Does each implicit premise have support from textual clues in the source (rather than being pure speculation)?
- [ ] **Confidence annotation**: Is the confidence level (high/medium/low) for each implicit premise reasonable?
- [ ] **Minimality principle**: Have no more implicit premises been added than are necessary?

## Principle of Charity Checks

- [ ] **Strongest version**: Is the reconstructed version the strongest version of the source argument?
- [ ] **Fidelity**: Does the reconstruction not distort or alter the direction of the source's claims?
- [ ] **Alternative interpretations**: If multiple reasonable reconstructions exist, have alternative interpretations been annotated?

## Argument Type Checks

- [ ] **Type determination**: Has the argument type been accurately determined?
- [ ] **Formal notation**: Does the logical form notation match the actual inferential structure?
- [ ] **Mixed types**: If the argument mixes multiple types, has the dominant type and auxiliary type(s) been annotated?

## Sub-argument Checks

- [ ] **Nested structure**: If sub-arguments exist, are the conclusions of sub-arguments correctly used as premises of the higher-level argument?
- [ ] **Clear hierarchy**: Does the nesting depth not exceed 5 levels? (Segment the reconstruction if it does)

## Language and Format Checks

- [ ] **Sentence completeness**: Is each premise and conclusion a complete declarative sentence (not a phrase or question)?
- [ ] **Consistent numbering**: Is the premise numbering format consistent, with no skipped or duplicate numbers?
- [ ] **Translation fidelity**: If reconstructing an English text in Chinese (or vice versa), does the expression accurately convey the original meaning?

## Boundary Checks

- [ ] **Unreconstructable cases**: If the source text is too vague to reconstruct, has a clear "Cannot reconstruct" explanation been provided?
- [ ] **Non-argumentative text**: If the text contains no argument (pure rhetoric/narrative), has it been annotated as "No argument detected" rather than having a structure imposed?
