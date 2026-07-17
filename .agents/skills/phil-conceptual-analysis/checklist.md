<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Conceptual Analysis Quality Checklist

> After each conceptual analysis, check each item. A fully checked list indicates a high-quality analysis.

---

## Basic Structure Checks

- [ ] **Concept clarity**: Is the analyzed concept's name clear and unambiguous? (If ambiguous, have multiple meanings been annotated?)
- [ ] **Domain annotation**: Has the philosophical domain to which the concept belongs been accurately annotated?
- [ ] **Candidate definitions**: If the source text contains candidate definitions, have they been explicitly reconstructed as a numbered list?

## Necessary Condition Checks

- [ ] **Necessity of each necessary condition**: Has it been confirmed that removing it would not make instances of the concept cease to exist?
- [ ] **Adequate testing**: Has each necessary condition passed at least one positive case test and one borderline case test?
- [ ] **No omissions**: Have no important necessary conditions been skipped (e.g., lacking annotation of categorical conditions)?

## Sufficiency Checks

- [ ] **Classical concepts have sufficiency tested**: If it is a classical concept structure, has the sufficient condition set been tested?
- [ ] **Counterexample identification**: If sufficiency failed, has a typical case been found or constructed?
- [ ] **Philosophical force of cases**: Are the counterexamples sufficiently strong (not merely rare edge cases)?

## Case Testing Checks

- [ ] **At least 2-3 positive cases**: Ensure the analysis covers the core use cases of the concept
- [ ] **At least 1 borderline case**: Reveals the fuzzy regions of the concept
- [ ] **Counterexample sources**: Have the sources of counterexamples been annotated (classic literature / self-constructed / discovered in discussion)?
- [ ] **Cases ≠ argument analysis**: This step only identifies and classifies cases to test conceptual analysis; constructing full counterexamples to evaluate argument structure should use `phil-counterexample`

## Distinction Mapping Checks

- [ ] **At least 2 adjacent concepts**: Demonstrate differences between concepts
- [ ] **Boundary type annotation**: Has it been explained whether the distinction is one of degree or kind?
- [ ] **No conflation of similar concepts**: Have common sources of confusion been analyzed?

## Structural Type Checks

- [ ] **Structural determination has rationale**: Why classical/cluster/prototype/other? The rationale must be explicit
- [ ] **Impact of type on subsequent analysis**: Has the impact of the conceptual structure type on subsequent philosophical analysis been annotated? (e.g., a typical cluster concept is unsuited for classical definition testing)

## Dimensional Analysis Checks

- [ ] **At least 2 dimensions**: Demonstrate the axes of variation for the concept
- [ ] **Each dimension has a role explanation**: What function does the dimension serve in the conceptual analysis?
- [ ] **Variation boundaries**: Has it been annotated whether variation along this dimension changes the application of the concept?

## Boundary Checks

- [ ] **Polysemy handling**: If a word has multiple unrelated meanings, have they been analyzed separately?
- [ ] **Theory dependence**: If the analysis depends on a specific theoretical framework, has this been annotated?
- [ ] **Contested concepts**: If the concept itself is politically/philosophically contested, have the analytical differences across different positions been annotated?
