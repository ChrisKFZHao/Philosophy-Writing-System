---
name: phil-argument-reconstruct
description: "Universal argument reconstruction framework — converting everyday language arguments into standard premise-conclusion form, supporting all argument types: deductive, inductive, reductio, abductive, inference to the best explanation, and more"
---

# Argument Reconstruction

## Overview

Transform arguments found in philosophical texts from everyday language into an **explicit, numbered premise-conclusion structure**. This is the most fundamental methodological tool in analytic philosophy — virtually all subsequent analysis (principle of charity checks, implicit premise detection, counterexample generation, modal analysis) takes the reconstructed standard form as input.

This Skill does not presuppose a specific argument type. **Deductive, inductive, reductio, abductive, inference to the best explanation, analogical, transcendental, dilemma, definitional arguments, and more** all use the same unified reconstruction framework.

## Input

- One or more paragraphs of philosophical text containing arguments (Chinese or English)
- Optional: user-annotated disputed passages, specific arguments to be analyzed

## Output

A structured **argument reconstruction report** conforming to the `analysis-report-schema.json` specification, containing:
- Argument type classification
- Numbered premise-conclusion chain
- Implicit premises (if any)
- Sub-argument structure (if any)
- Logical form notation
- Reconstruction notes (textual basis, alternative interpretations)

## Methodological Foundations

Argument reconstruction is the cornerstone method of analytic philosophy. Its norms derive from the following traditions:

1. **Standard Form Method**: Decomposing arguments into numbered premises and conclusions — the universal norm of analytic philosophy textbooks (Baronett, 2008; Weston, 2000; Vaughn, 2006)
2. **Logical Formalization**: Identifying the logical skeleton of an argument and notating its inference pattern with logical language (Sider, 2010; Smith, 2012)
3. **Principle of Charity**: Reconstructing the strongest version of the argument within reasonable bounds — but noting the distance from the original text (Quine, 1960; Davidson, 1973)
4. **Argument Mapping**: Visualizing argument structure as premise-conclusion diagrams (Walton, 1996; Reed & Walton, 2005)
5. **Enthymeme Theory**: Arguments often contain unstated premises; reconstruction must make them explicit and annotate them (Walton, 2008; Hitchcock, 2016)

## Steps

### Step 1: Identify Argument Scope

Locate the starting point and boundaries of the argument within the text. Distinguish between:
- The argument core — what the author is "claiming" and "inferring"
- Background information — definitions, context, conventions
- Rhetorical elements — emphasis, ornamentation, which bear no inferential function

**Output**: Argument-relevant passages extracted from the source text.

### Step 2: Extract the Conclusion

First identify the conclusion the author attempts to prove — this determines the direction of the reconstruction. Conclusions are typically signaled by indicator terms:
- "therefore," "hence," "thus," "consequently," "it follows that," "so," "we may conclude that"

**Note**: Sometimes the conclusion appears at the beginning (stated first, then argued), sometimes at the end (argued toward). In some texts, the conclusion must be inferred from context.

**Output**: A single-sentence statement of conclusion C.

### Step 3: Enumerate Explicit Premises

Identify all explicit statements offered in support of the conclusion. Number each premise:
- [P1], [P2], [P3] ...
- Each premise must be a **complete declarative sentence**
- Distinguish separate parts of the same premise (do not split a complex statement into multiple premises unless logic genuinely requires it)
- Distinguish distinct premises (do not merge multiple independent premises into one)

Premise indicators include:
- "because," "since," "as," "given that," "for," "inasmuch as," "owing to"

**Output**: A numbered list of explicit premises.

### Step 4: Identify Argument Type

Determine the argument type based on the premise-to-conclusion support relation:

| Type | Characteristic | Logical Form | Evaluative Criterion |
|------|---------------|-------------|---------------------|
| **Deductive** | If premises are true, conclusion must be true | ∀-elimination, modus ponens/tollens, categorical syllogism, etc. | Validity |
| **Inductive** | Premises support conclusion with some probability | Statistical generalization, enumerative induction | Strength |
| **Reductio** | Assume P → contradiction → ¬P | P → (Q ∧ ¬Q) ∴ ¬P | Necessity of the inference chain |
| **Abductive** | Observation O + explanation E → E is the best explanation | O, E ⇒ O, ¬∃E' better ∴ E | Explanatory power |
| **IBE** (Inference to the Best Explanation) | Among competing hypotheses, the one with greatest explanatory power is affirmed | Same as abduction, but explicitly comparative | Overall explanatory ranking |
| **Analogy** | A has properties F,G; B has F → B has G | A:F,G; B:F ∴ B:G | Relevance and strength of the analogy |
| **Transcendental** | X is a condition of the possibility of experience Y → X exists | ∀(Y → X) ∴ X | Necessity of the condition |
| **Definitional** | By the definition of X → X has property F | def(X) → F(X) | Adequacy of the definition |
| **Dilemma** | P ∨ Q; P → R; Q → R ∴ R | P∨Q, P→R, Q→R ∴ R | Completeness of the branches |
| **Practical Reasoning** | Goal G + means M → one ought to do M | Desire G, M → G ∴ Ought M | Sufficiency and necessity of the means |

> An argument may mix multiple types. In such cases, annotate as "primarily deductive, with an inductive sub-argument," etc.

**Output**: Argument type determination and rationale.

### Step 5: Identify Implicit Premises

Identify the **unstated assumptions** that are required for the argument to hold. This is the most crucial step in philosophical argument reconstruction.

Common implicit premise types:
- **Conceptual Bridge**: A connecting assumption needed when the concepts used in the premises differ from those in the conclusion
- **Category Jump**: Moving from fact to value, from descriptive to normative, from possible to actual
- **Missing Universal**: Generalizing from "some X are Y" to "all X are Y"
- **Existential Presupposition**: Assuming the existence of a certain class of entities
- **Exclusivity Assumption**: Assuming there are no other possibilities
- **Background Framework**: Deep worldview presuppositions that underwrite the argument

For each implicit premise, annotate:
- Location (which gap between Pi and Pi+1 / C it fills)
- Confidence level (highly plausible / debatable / controversial)
- Textual clues (where in the source text the assumption is suggested)

**Output**: A numbered list of implicit premises [IP1], [IP2]..., each with its location and confidence level annotated.

### Step 6: Assess Structural Validity / Strength

Conduct an overall check of whether the argument succeeds:

- **Deductive argument**: Do the premises entail the conclusion? (If the premises are true, can the conclusion be false?)
- **Inductive argument**: How strong is the support the premises provide for the conclusion?
- **Reductio argument**: Is the derivation from assumption to contradiction valid?
- **Abductive / IBE argument**: Is this explanation genuinely the best among competing alternatives? Assessment criteria include explanatory power, simplicity, consistency, conservatism (Lipton, 2004; Harman, 1965)
- **Analogical argument**: Do the relevant similarities between A and B outweigh the irrelevant ones?

If structural problems exist, note them in the reconstruction notes.

**Output**: Structural assessment (valid / sound / strong / weak / fallacious, etc.).

### Step 7: Write the Reconstruction Report

Output the complete reconstruction in standard format:

```
## Argument Reconstruction Report

### Basic Information
- **Argument ID**: <unique identifier>
- **Argument Type**: <type determination>
- **Logical Form**: <notated logical form>
- **Source**: <passage citation>

### Premise-Conclusion Structure

[P1] <premise 1>
[P2] <premise 2>
[P3] <premise 3>
...
───────
[C]  ∴ <conclusion>

### Implicit Premises

[IP1] <implicit premise 1> (fills the gap [P2] → [C]) | Confidence: <high/medium/low>
[IP2] <implicit premise 2> | Confidence: <high/medium/low>

### Sub-argument Structure

<If nested arguments exist, display hierarchy with indentation here>

### Structural Assessment

- Argument type <...>, logical form <...>
- Structural determination: <valid / sound / strong / cogent / fallacious>
- Explanation: <brief justification of the determination>

### Reconstruction Notes

<Key points to note from the reconstruction process, e.g.:>
- <A passage in the source text is ambiguous; the reconstruction chooses interpretation A over B, with reasons>
- <Although the strongest version was constructed per the principle of charity, the original text may have had a weaker intent>
- <This argument shares premise P1 with argument X in another passage>
```

## Quality Criteria

1. **Premise Independence Principle**: Each premise should be an independent, complete declarative sentence that does not depend on the interpretation of other premises to be coherent.
2. **Conclusion-First Principle**: Identify the conclusion before the premises; avoid mistaking background information for premises.
3. **Minimal Implicit Premise Principle**: Supply only the implicit premises necessary for the argument to hold; do not over-supplement.
4. **Divergence-Annotation Principle**: If ambiguity in the source text allows multiple reasonable reconstructions, present all of them and annotate their priority.
5. **Principle of Charity**: Reconstruct the strongest version within reasonable bounds, but annotate the distance from the source text.
6. **Principle of Fidelity**: The reconstruction should not alter the source text's position or basic direction of reasoning.

## Relations to Other Skills

**Downstream (depend on this Skill's output)**:
- `phil-charity-check`: Takes the reconstructed standard form as input to assess whether the strongest version was built
- `phil-premise-detect`: Uses the reconstructed structure as a basis for deeper implicit premise detection
- `phil-counterexample`: Uses the standard form to construct counterexamples against specific premises
- `phil-modal-arg`: Requires the reconstructed modal premise structure
- `phil-ontological-commitment`: Requires explicit premise lists to extract existential commitments
- `phil-dialectical-map`: Uses multiple reconstructed arguments as nodes to build a dialectical tree

## Boundary Conditions

1. **Extremely Vague Text**: If the source text is too ambiguous to extract a clear premise-conclusion structure, output "Cannot reconstruct" with an explanation, rather than forcing a reconstruction.
2. **Purely Rhetorical or Narrative Text**: If the text is purely rhetorical or narrative and contains no argument (e.g., poetry, purely narrative prose), output "No reconstructable argument detected" rather than imposing a logical structure.
3. **Excessively Long Argument Chain**: If argument nesting exceeds 5 levels, recommend segmenting the reconstruction with independent numbering for each segment.
4. **Elliptical Arguments**: If the author relies on well-known suspended premises (e.g., "Humean causal skepticism" without restating the argument), annotate in [IP] and cite the corresponding argument-forms knowledge file.
5. **Multiple Conclusions**: If a text has multiple parallel conclusions, reconstruct each as an independent argument.

## ARS Interface

- Reconstruction reports can be directly passed to ARS `academic-paper` in the writing workflow, serving as appendices to argument analysis.
- Citation formats in the report are compatible with ARS `citation-check`.
- Reconstruction reports can serve as supplementary analytical material for ARS `academic-paper-reviewer`.
