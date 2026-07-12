---
description: Thought experiment analysis — deconstructing the structure, intuition mechanisms, and argumentative force of philosophical thought experiments
name: phil-thought-experiment
domain: general
version: 1.0.0
---

# Thought Experiment Analysis

## Overview

The thought experiment is one of the most important methodological tools in analytic philosophy. From Putnam's brain-in-a-vat to Thomson's violinist, from Chalmers's zombie to Parfit's fission case, thought experiments form the argumentative bedrock of analytic philosophy.

This Skill systematically deconstructs the logical structure of thought experiments, analyzes their intuition-triggering mechanisms, and evaluates their argumentative force. It answers:

- How is the thought experiment's scenario constructed? Which details carry argumentative function?
- What is the bridge from the scenario to the conclusion via intuition?
- Does the thought experiment implicitly rely on unwarranted presuppositions?
- Can the "typicality" of the thought experiment be challenged?
- Can the force of this thought experiment be transferred to a more ordinary case with fewer assumptions?

## Input

- A description of a philosophical thought experiment (full paragraph / paper excerpt)
- Optional:
  - The corresponding argument reconstruction (from `phil-argument-reconstruct`)

## Output

A structured **Thought Experiment Analysis Report**, containing:
- Scenario decomposition (setting, actors, events, key details)
- Intuition-triggering mechanism analysis
- Conclusion derivation pathway
- Presupposition audit (hidden assumptions)
- Alternative-case test (can an equivalent case be constructed that removes this presupposition?)
- Force assessment

## Methodological Foundations

1. **The Logic of Thought Experiments**: Thought experiments are not arbitrary imaginings — their logical structure is "a chain of reasoning from possible worlds" (Sorensen, 1992; Brown, 1991)
2. **The Role of Intuition in Philosophy**: Are intuitions the "basic data" of philosophical argumentation or biases that need to be interrogated? Experimental philosophy challenges the universality of intuitions (Weinberg, Nichols & Stich, 2001; Machery et al., 2004)
3. **Method of Cases**: Thought experiments are a "limit version" of the method — deriving conclusions about complex cases from intuitively compelling simple cases (Williamson, 2007, methodological critique)
4. **Imaginative Resistance**: Some thought experiments are "hard to enter" — not due to logical defects, but because of imaginative resistance (Gendler, 2000)

## Steps

### Step 1: Scenario Parsing

Parse the constituent elements of the thought experiment:

- **Setting**: Time, place, historical background (or counterfactual setup)
- **Actors**: How many participants? What properties do they have?
- **Events** (chain of events): What happens? In what order?
- **Key Detail**: Which details carry "driving" argumentative force? Which are merely "ornamental"?
- **Counterfactual Hinge**: Which part is counterfactual — i.e., at which step does the scenario depart from the actual world?

**Output**: Five-element scenario decomposition.

### Step 2: Intuition-Triggering Mechanism Analysis

Thought experiments are not deductive proofs — they rely on intuition. Analyze the source of the intuition:

- Does the intuition derive from a **generalization of everyday experience**? (e.g., "unfair treatment elicits anger")
- Does the intuition derive from a **conceptual convention**? (e.g., "this is a bachelor")
- Does the intuition derive from **moral/aesthetic perception**? (e.g., "this is manifestly unjust/ugly")

Assessment of the intuition source:
- Is this intuition source reliable? (Generalizations from everyday experience are typically reliable; conceptual conventions may be circular; moral perception exhibits cultural variation)
- Could there be a contrary intuition?

**Output**: Intuition source analysis + reliability assessment.

### Step 3: Conclusion Derivation Pathway

Map the argumentative chain from the scenario to the conclusion:

```
Scenario description
  → Intuitive response: <description>
    → Generalization: <from specific case to general principle>
      → Conclusion: <the thesis ultimately supported by the thought experiment>
```

Examine each step:
- Does the intuitive response necessarily follow from the scenario description?
- Does generalizing from "in case C, we have intuition I" to "in all cases of type C, I holds" face a representativeness problem?
- Does the generalization step involve a hidden universal leap?

**Output**: Derivation pathway + assessment of each step.

### Step 4: Presupposition Audit

Thought experiments always rest on certain unstated background presuppositions. Audit:

- **Alienation Presupposition**: Does the scenario contain counterfactual presuppositions unfamiliar to the reader? If the presuppositions are excessively alien, the intuition may be unreliable
- **Moral Disagreement Presupposition**: Does the scenario depend on a particular moral/value orientation that is philosophically contested?
- **Actuality Gap**: Is the departure from the actual world so great that "laboratory intuitions" are inapplicable?

**Output**: List of presuppositions, each annotated with its impact on the analysis.

### Step 5: Alternative-Case Test

Construct an equivalent case that removes a key presupposition, and test whether the thought experiment's conclusion still holds:

- If presupposition X is removed, can a scenario of equivalent strength still be constructed?
- If not, then presupposition X is a necessary component of the thought experiment — flag it
- If yes, then the presupposition is superfluous ornamentation

**Output**: Alternative case (if available) or explanation of the presupposition's non-removability.

### Step 6: Force Assessment

| Dimension | Assessment |
|-----------|------------|
| Scenario conceivability | High / Medium / Low |
| Intuition reliability | High / Medium / Low / Culturally variable |
| Derivational validity | Valid / Partially valid / Invalid |
| Presupposition transparency | Most presuppositions flagged / Significant hidden presuppositions |
| Contribution to the argument | Core argument / Supporting argument / Heuristic only |

### Step 7: Output the Analysis Report

```
## Thought Experiment Analysis Report

### Basic Information
- **Analysis ID**: THX-<xxx>
- **Thought Experiment Name**: <name or identifier>
- **Source**: <bibliographic reference>

### Scenario Decomposition
- Setting: ...
- Actors: ...
- Events: ...
- Key Detail: ...
- Counterfactual Hinge: ...

### Intuition-Triggering Mechanism
- Intuition source: <everyday experience / conceptual convention / moral perception / ...>
- Reliability: <assessment>
- Possible contrary intuition: <if any>

### Conclusion Derivation Pathway
<four-step analysis: scenario → intuition → generalization → conclusion>

### Presupposition Audit
<list>

### Alternative-Case Test
<if available>

### Force Assessment
<six-dimension table>
```

## Quality Criteria

1. **Do not conflate intuition with argument**: The intuition-triggering mechanism is the foundation of the thought experiment, but it is not an independent argument — flag the intuition source and its plausibility
2. **Presupposition transparency principle**: All scenario presuppositions must be explicitly listed
3. **Do not default to universality**: That an intuition holds in a specific case does not entail that it holds in all similar cases

## Relations to Other Skills

**Dependencies** (optional):
- `phil-argument-reconstruct`: Can provide a standardized reconstruction of the argument

**Dependents**:
- `phil-dialectical-map`: Thought experiments often serve as a key node within a dialectical tree

## Boundary Conditions

1. **Non-thought-experiment cases**: If the case in the text is a real case (rather than a thought experiment), redirect to `phil-counterexample` or `phil-conceptual-analysis`
2. **Multiple thought experiments**: A single text may contain multiple thought experiments; analyze each separately

## ARS Interface

- Thought experiment analysis reports may be passed to ARS `academic-paper` as methodological supplement
- Presupposition analysis of thought experiments may serve as citation-verification material for ARS `citation-check`
