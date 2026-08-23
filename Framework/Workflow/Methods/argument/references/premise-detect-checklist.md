# Implicit Premise Detection — checklist (conditional reference for method.argument.premise-detect)

> Loaded only when the consuming mode's live ambiguity or the user's explicit request requires it; never loaded by default with the method file.

# Implicit Premise Detection Quality Checklist

> After each implicit premise detection, check each item.

---

## Input Completeness Checks

- [ ] **Argument structure is complete**: Does the input standard-form argument have clear premise numbers and conclusion?
- [ ] **Premise independence**: Is each explicit premise an independent statement, not a merger of multiple statements?
- [ ] **Argument type annotated**: Has the argument type been clearly specified (deductive/inductive/abductive, etc.)?

## Coverage Checks

- [ ] **No omissions**: Have all meaningful logical gaps in the argument been examined?
- [ ] **Type mapping**: Does each detected implicit premise have a clear type classification?
- [ ] **Location annotation**: Has the fill location of each implicit premise (Px → Py or Px → C) been annotated?
- [ ] **Fill is sufficient but not excessive**: Is the fill for each gap the most economical and adequate supplementation — neither too much nor too little?

## Quality Checks

- [ ] **Confidence assessment is reasonable**: Does each implicit premise's confidence (high/medium/low) have adequate justification?
- [ ] **Independence is distinguished**: Is each implicit premise an independent statement — not duplicating other implicit premises or explicit premises?
- [ ] **Charitable repair**: Are the constructed implicit premises the most reasonable version that makes the argument hold (neither over-strengthened nor under-strengthened)?
- [ ] **Testing information is sufficient**: Has each implicit premise been evaluated for the consequences if rejected?

## Boundary Checks

- [ ] **Over-detection**: Have only premises necessary for the argument been detected — not all logically possible premises?
- [ ] **Argument-invalid cases**: If the argument cannot be repaired through implicit premises, has this been annotated rather than forcing a fill?
- [ ] **Nested implicit premises**: If implicit premises are mutually dependent, has this been annotated?
- [ ] **Textual clues**: Those with textual clues from the source have been annotated; those without have also been marked "no textual clues"?
