---
id: method.concept.conceptual-analysis
package: concept
legacy_ids: [phil-conceptual-analysis]
label: Conceptual Analysis
consumers: [phil-research/reconstruct, phil-write, phil-review]
selector: feature:conceptual / level:2
side_effects: read-only
---

# Conceptual Analysis (method.concept.conceptual-analysis)

> Internal method module — not a registered runtime skill. Loaded on demand by the consuming skill's mode contract through the manifest resolver; never loaded wholesale.

# Conceptual Analysis

## Overview

Clarify the meaning, conditions, and boundaries of philosophical concepts. This is the oldest and most central method of analytic philosophy — from Socrates asking "What is justice?" to contemporary conceptual engineering in analytic philosophy, conceptual analysis runs through the entire tradition.

This Skill handles questions including:
- What are the defining conditions of a concept? (Necessary conditions and sufficient conditions)
- Is the concept a "classical concept" or a "cluster concept"?
- How does this concept differ from adjacent concepts?
- Along what dimensions does this concept vary?
- Can an existing definition survive counterexample testing?

## Input

- A philosophical concept to be analyzed (Chinese or English)
- Optional:
  - The contextual passage in which the concept appears
  - A candidate definition proposed by the user
  - Specific disputed dimensions the user is concerned with
  - A need to distinguish the concept from adjacent concepts

## Output

A structured **conceptual analysis report** conforming to the `concept-map-schema.json` specification, containing:
- Concept positioning (domain, level, adjacent concepts)
- List of candidate definitions (if any)
- Necessary condition / sufficient condition matrix
- Case testing (positive cases / borderline cases / counterexamples)
- Distinction mapping (boundaries with adjacent concepts)
- Conceptual structure type determination (classical / cluster / prototype / stipulative)
- Conceptual engineering recommendations (if applicable)
- Dimensional analysis (along which axes does the concept vary)

## Methodological Foundations

The methodology of conceptual analysis derives from the following traditions:

1. **Socratic Definition Method**: Approaching the essence of a concept by asking "What is X?" and testing candidate definitions against counterexamples (Plato, *Euthyphro*, *Meno*)
2. **Classical Theory of Concepts**: Concepts are jointly defined by their necessary and sufficient conditions (Aristotle, *Categories*; Frege, 1884)
3. **Cluster Concept Theory**: Certain concepts have no single set of defining conditions; instead they are constituted by a set of "family resemblance" features (Wittgenstein, 1953; Putnam, 1975)
4. **Method of Cases**: Testing the adequacy of a conceptual definition through thought experiments and intuitive cases (Gettier, 1963; Thomson, 1971)
5. **Conceptual Engineering / Explication**: Deliberately revising concepts on the basis of analysis to serve specific theoretical or practical purposes (Carnap, 1950; Haslanger, 2000)
6. **Concept Mapping / Distinction Drawing**: Charting a concept's "logical geography" by comparing and contrasting it with adjacent concepts (Austin, 1956; Ryle, 1949)

## Steps

### Step 1: Extract and Position the Concept

Identify the target concept's location and mode of use within the text.

- Clarify the concept's mode of expression: is it an ordinary usage or a technical term?
- Determine the concept's domain: metaphysics, ethics, epistemology, philosophy of mind, philosophy of language, etc.
- Identify adjacent concepts: closely related terms that are easily confused with this concept

**Output**: Concept name, domain, preliminary positioning.

### Step 2: Reconstruct Candidate Definitions

If a definition of the concept already exists in the source text or context, extract it in explicit form.

Candidate definitions may be of several kinds:
- **Classical definition**: A = df. φ₁ ∧ φ₂ ∧ … ∧ φₙ (conjunction of necessary conditions)
- **Disjunctive definition**: A = df. φ₁ ∨ φ₂ ∨ … ∨ φₙ (disjunction of multiple ways)
- **Exemplar definition**: A ≈ sufficiently similar to paradigm x (prototype definition)
- **Anti-definitional**: A has no definition; it is understood solely through use (Wittgensteinian)
- **No candidate definition**: The concept is undefined — in this case, the task of this Skill is to propose candidate definitions

**Output**: List of candidate definitions (if any), or notation that no candidate definition exists.

### Step 3: Extract Necessary Conditions

Conditions that are always presupposed when the concept is applied.

Propose and test each candidate necessary condition:

- **Necessary condition test**: Is there some case C such that C is an instance of concept X but does not satisfy condition φ? If so, φ is not a necessary condition.
- **Necessary conditions of a concept** typically include:
  - Categorical conditions (the highest category to which the concept belongs)
  - Attributive conditions (properties that distinguish the concept from others in the same category)
  - Relational conditions (relations between the concept and other concepts)

**Output**: List of necessary conditions (with test status).

### Step 4: Retrieve Sufficient Conditions

What set of conditions, when satisfied, always makes the concept applicable?

Propose and test each candidate sufficient condition set:

- **Sufficiency test**: Is there some case C such that C satisfies conditions φ₁, φ₂, …, φₙ but is not an instance of concept X? If so, that set of conditions is not sufficient.
- The classic "Gettier problem" is a sufficiency test — "justified true belief" is shown not to be sufficient for "knowledge."

**Output**: List of sufficient condition sets (with test status).

### Step 5: Case Testing

Construct three kinds of cases to test the conceptual analysis:

| Case Type | Definition | Function |
|-----------|-----------|----------|
| **Positive Case** | A typical instance that clearly belongs to the concept | Verifies whether the analysis covers core usage |
| **Borderline Case** | An instance where the concept's application at the boundary is disputed | Reveals the fuzzy boundaries of the definition |
| **Counterexample** | Satisfies the candidate definition but intuitively does not belong to the concept (or vice versa) | Falsification test — the most powerful testing tool |

For each case, annotate:
- Case source (classic case from the literature / self-constructed / from dialogue)
- The case's impact on the candidate definition (supports / challenges / neutral)
- The intuitive force of the case (strong / medium / weak)

Note: This step only **identifies and classifies cases** to test conceptual analysis; for constructing complete counterexamples and evaluating their impact on argument structure, see `method.argument.counterexample`.

**Output**: Case table (several of each: positive/borderline/counterexample), each annotated with source and function.

### Step 6: Distinction Mapping

Compare the concept with its adjacent concepts and draw a distinction map.

For each adjacent concept:
- What does it share with the target concept?
- What is the key difference from the target concept?
- Are these differences matters of degree (gradual, no sharp boundary) or matters of kind (sharp boundary)?

Common distinctions to map:
```
               ┌───────────────────┐
               │   Target Concept   │
               └────┬─────────┬────┘
                    │         │
          ┌─────────┴┐   ┌───┴──────────┐
          │ Adjacent A│   │ Adjacent B  │
          │ ─ key diff│   │ ─ key diff  │
          └───────────┘   └──────────────┘
```

**Output**: Distinction map (in textual description form).

### Step 7: Conceptual Structure Type Determination

Determine which structural type the concept belongs to:

| Type | Characteristic | Representative Theory | Typical Example |
|------|---------------|----------------------|-----------------|
| **Classical Concept** | Has determinate necessary + sufficient conditions | Aristotle, Frege | Bachelor (unmarried adult male) |
| **Cluster Concept** | A set of features; satisfying enough of them counts as an instance | Wittgenstein, Putnam | Game, language |
| **Prototype Concept** | Centered on a typical exemplar, with fuzzy boundaries | Rosch, Lakoff | Bird, furniture |
| **Decompositional Concept** | Composed from more basic concepts | Fodor, Jackendoff | Kill = cause to die |
| **Essentialist Concept** | Has a hidden essential structure | Kripke, Putnam | Water (H₂O), gold |
| **Stipulative Concept** | Artificially defined for theoretical purposes | Carnap | Theoretical terms |

**Output**: Structural type determination and its rationale.

### Step 8: Dimensional Analysis

Identify along which dimensions the concept varies — this is crucial in philosophical analysis because many conceptual confusions stem from conflating different dimensions.

Examples of common conceptual dimensions:
- Descriptive / Normative
- Intrinsic / Extrinsic
- Individual / Collective
- Objective / Subjective
- Gradable / Discrete
- Historical / Ahistorical

For each dimension, annotate:
- The dimension's relevance in the conceptual analysis
- Whether variation along this dimension changes the concept's application

**Output**: List of dimensions, each annotated with its role in the conceptual analysis.

### Step 9: Write the Analysis Report

Output the complete conceptual analysis report in standard format:

```yaml
## Conceptual Analysis Report

### Basic Information
- **Concept**: <name>
- **Domain**: <philosophical domain>
- **Analysis Version**: <version number>
- **Analysis Type**: <initial analysis / supplementary analysis / conceptual engineering>

### Candidate Definitions

<If candidate definitions exist, list and number them here>

### Necessary Conditions

NC1: <condition 1> — Test: <passed / disputed / failed>
NC2: <condition 2> — Test: <passed / disputed / failed>
...

### Sufficiency Test

SC: <condition set> — Test: <passed / failed>
Explanation: <why it passed / failed>

### Case Testing

#### Positive Cases
PC1: <description> — Source: <classic / constructed> — Function: <supports the analysis>

#### Borderline Cases
BC1: <description> — Source: <classic / constructed> — Fuzzy area revealed: <explanation>

#### Counterexamples
CC1: <description> — Source: <classic / constructed> — Impact on candidate definition: <explanation>

### Distinction Mapping

| Adjacent Concept | Commonality | Key Difference | Boundary Type |
|-----------------|-------------|----------------|---------------|
| <concept A> | <shared features> | <distinguishing features> | degree / kind |

### Conceptual Structure Type

- Determination: <classical / cluster / prototype / decompositional / essentialist / stipulative>
- Rationale: <justification>

### Dimensional Analysis

| Dimension | Role in the Concept | Does variation change application? |
|-----------|---------------------|-------------------------------------|
| <dimension 1> | <explanation> | yes / no / sometimes |

### Reconstruction Notes and Technical Details

<Technical notes from the analysis process, e.g.:>
- <Do the cases used in this analysis depend on a particular philosophical tradition?>
- <If multiple viable paths of conceptual analysis exist, annotate them>
- <Possible sources of controversy for the concept>
- <If conceptual engineering is called for (revising the concept to serve theoretical purposes), annotate recommendations>
```

## Quality Criteria

1. **Reproducibility Principle**: The results of analysis should be independent of the user's intuitions — different users inputting the same concept should obtain a consistent analytical structure.
2. **Distinction-Testing Principle**: Each necessary condition must pass a conceivable counterexample test — if no case can be constructed that satisfies the condition but is not an instance, the condition may be vacuous.
3. **Sufficiency Principle**: The sufficient condition set must intuitively cover all typical instances — if a classic instance is not covered, the sufficient condition set is too narrow.
4. **Fidelity Principle**: The analysis should be faithful to the concept's actual use in the text/dialogue — unless explicitly declared to be doing "conceptual engineering."

## Relations to Other Skills

**Downstream (depend on this Skill's output)**:
- `method.concept.distinction-track`: Takes the distinction map from conceptual analysis as input to systematically track all key distinctions in the text
- `method.metaphysics.essence-detect`: Needs the results of conceptual analysis to determine whether a claim concerns essence or accident
- `method.concept.natural-kind-analyze`: Needs conceptual analysis to determine the defining features of natural kinds

**Upstream (this Skill depends on)**:
- This Skill is independent (does not depend on other analytical Skills)

## Boundary Conditions

1. **Concept undefined in the text**: If the concept is not constrained by any candidate definition, construct "the most reasonable default candidate definition" and annotate it as IP.
2. **Theory-embedded concepts**: The definition of certain concepts is fully embedded within a specific theoretical framework (e.g., "force" in physics); in such cases the concept cannot be analyzed in isolation from the theoretical context.
3. **Ordinary concepts vs. technical concepts**: Analysis of ordinary concepts should use ordinary intuitions; analysis of technical concepts should use the theoretical standards of the relevant field.
4. **Polysemy**: If a word has multiple completely unrelated meanings (e.g., "bank"), perform independent analyses for each rather than attempting to unify them.
5. **Political / contested concepts**: The definition of certain concepts is itself politically contested (e.g., "race," "gender"). When analyzing, annotate the political presuppositions of different definitions.

## ARS Interface

- Conceptual analysis reports can be passed to ARS `academic-paper` during the writing phase for the concept clarification section of a paper.
- Cases used in conceptual analysis can be passed to ARS `citation-check` to verify citation accuracy.
