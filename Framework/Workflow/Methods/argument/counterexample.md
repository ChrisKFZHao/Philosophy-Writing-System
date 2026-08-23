---
id: method.argument.counterexample
package: argument
legacy_ids: [phil-counterexample]
label: Counterexample Generation and Evaluation
consumers: [phil-research/evaluate, phil-write, phil-review]
selector: feature-detected
side_effects: read-only
---

# Counterexample Generation and Evaluation (method.argument.counterexample)

> Internal method module — not a registered runtime skill. Loaded on demand by the consuming skill's mode contract through the manifest resolver; never loaded wholesale.

# Counterexample Generation & Evaluation

## Overview

Using an argument reconstruction report (from `method.argument.argument-reconstruct`) as a blueprint, systematically construct, classify, and evaluate counterexamples. This is the sharpest methodological tool in analytic philosophy — a well-constructed counterexample can dismantle an entire argument in a single stroke.

This Skill handles three types of operations:

- **Counterexamples targeting premises**: Construct a case in which the premise is false
- **Counterexamples targeting inferential chains**: Construct a case that satisfies the premises but does not entail the conclusion
- **Counterexamples targeting conceptual boundaries**: Construct a case that breaks the necessary/sufficient conditions of a concept (Gettier-style)
- For each counterexample, evaluate: intuitive force, conceivability, and impact on the argument

This Skill depends on the output of `method.argument.argument-reconstruct` (standard form) and may optionally draw on the output of `method.argument.premise-detect` (known weak points).

## Input

- **Required**: Argument reconstruction report (from `method.argument.argument-reconstruct`) — containing numbered premises and conclusion
- **Strongly recommended**: Implicit premise detection report (from `method.argument.premise-detect`) — flagging vulnerable points
- **Optional**:
  - Target premise number(s) (user-specified attack points)
  - Background knowledge / domain constraints

## Output

A structured **Counterexample Construction & Evaluation Report**, containing:
- Description of each counterexample (scenario/case)
- Counterexample type classification
- Target (which premise/inferential step)
- Impact assessment on the argument (fatal/severe/moderate/weak)
- Conceivability assessment of the counterexample
- Anticipated rebuttals and responses (dialectical anticipation)

## Methodological Foundations

1. **The Gettier Method** (Gettier, 1963): Construct cases that satisfy the analytic conditions yet elicit intuitive rejection of the conclusion — the most celebrated paradigm of counterexample construction
2. **Method of Possible Cases**: Test necessary and sufficient conditions by constructing logically possible cases (Chalmers, 2002; Williamson, 2007)
3. **Intuition Pump Method**: Counterexamples are a species of intuition pump — they expose problems in conceptual analysis by eliciting intuitions (Dennett, 1984/2013)
4. **Dialectical Counterexample**: Not merely "find a case where the premise is false," but construct a case that also holds within the opponent's conceptual framework, forcing a response (Lakatos, 1976)

## Steps

### Step 1: Receive the Argument and Identify Attack Points

Extract from the argument reconstruction report:

- All explicit premises [P1]...[Pn] and the conclusion [C]
- Implicit premises [IP1]...[IPn] (if available, from `method.argument.premise-detect`)
- The role and degree of certainty for each premise

**Determine attack priority**:
1. The most vulnerable premise (lowest certainty)
2. The premise with the greatest impact on the conclusion (if a counterexample succeeds, the conclusion collapses entirely)
3. Implicit premises (typically the most vulnerable and highest-impact)

**Output**: Attack priority list.

### Step 2: Construct Counterexamples

For each target premise/inferential chain, construct a counterexample. Counterexamples may be:

| Type | Structure | Example |
|------|-----------|---------|
| **Factual Counterexample** | Construct a real-world case where the premise does not hold | "The premise claims all X have Y, but there exists X* without Y" |
| **Thought Experiment Counterexample** | Construct a possible-world case where the premise does not hold | Gettier's ten-coins case |
| **Logical Counterexample** | Demonstrate that the premise entails a contradiction, or that the conceptual analysis is insufficient | "If P2 holds, then Q follows; but ¬Q is more reasonable" |
| **Analogical Counterexample** | Construct a case similar in relevant dimensions, but whose conclusion is absurd | "If this works for A, it should also work for A*; but it does not work for A*" |
| **Borderline Counterexample** | Demonstrate that the concept collapses at the boundary (applicable to cluster concepts) | Wittgenstein's "game" cases |
| **Vagueness Counterexample** | Demonstrate a sorites chain — the boundary cannot be determined | "One grain is not a heap, two grains are not a heap → n grains → ..." |

Each counterexample description includes:
- Scenario/case description
- Why it constitutes a counterexample
- The specific premise/inferential step targeted

**Output**: At least one counterexample per attack point.

### Step 3: Evaluate Counterexample Validity

Each counterexample is assessed along the following dimensions:

| Dimension | Assessment Question | Rating |
|-----------|---------------------|--------|
| Intuitive Force | Does this counterexample elicit widespread intuitive agreement? | Strong / Moderate / Weak |
| Conceivability | Is this counterexample logically/metaphysically coherent? | High / Medium / Low / Disputed |
| Isolation | Does the counterexample challenge only the target premise, without collaterally challenging other accepted premises? | Good / Fair / Poor |
| Independence | Does the counterexample not depend on a specific philosophical stance? | Yes / Partial / No |

**Output**: Four-dimension evaluation for each counterexample.

### Step 4: Dialectical Anticipation — Anticipated Rebuttals and Responses

For each counterexample, anticipate possible responses from the opponent:

- **Reject the intuition**: "The intuition elicited by this counterexample is unreliable / should not be adopted"
- **Redefine the concept**: "The counterexample does not fall within the scope of this concept"
- **Distinction strategy**: "A finer-grained distinction is needed to exclude the counterexample"
- **Accept but downgrade**: "The counterexample succeeds but only affects the strength of the argument, not its demise"
- **Crushing response**: The counterexample is accepted as fatal

For each anticipated response, provide a preliminary assessment:
- Is the response reasonable?
- If the response succeeds, how does the counterexample's impact change?

**Output**: Dialectical anticipation for each counterexample.

### Step 5: Write the Counterexample Report

```
## Counterexample Construction & Evaluation Report

### Basic Information
- **Report ID**: CX-<xxx>
- **Based on Argument**: <ARG identifier>
- **Attack Priority**: <premise ordering>

### Counterexample 1: <name>

- **Type**: Factual / Thought Experiment / Logical / Analogical / Borderline / Vagueness
- **Target**: [P3] or the inferential chain [P1+P2 → C]
- **Scenario Description**: <detailed description>

- **Intuitive Force**: Strong / Moderate / Weak
- **Conceivability**: High / Medium / Low
- **Isolation**: Good / Fair / Poor
- **Independence**: Yes / Partial / No

- **Anticipated Rebuttal**: <possible opponent response>
- **Preliminary Assessment**: <whether the response is reasonable; if not, why not>

### Counterexample 2: ...

### Overall Assessment

- Most effective counterexample: <CX-number>
- Overall impact on the argument: Fatal / Severe / Moderate / Weak
```

## Quality Criteria

1. **Precision Principle**: Counterexamples must precisely target the target premise or inferential step — they must not be globalized
2. **Independence Principle**: Counterexamples should, as far as possible, not depend on a specific philosophical stance
3. **Dialectical Principle**: Every counterexample must have anticipated rebuttals and responses — do not assume the opponent will automatically concede
4. **Logical Consistency Principle**: The logical structure of the counterexample itself must be consistent

## Relations to Other Skills

**Dependencies**:
- `method.argument.argument-reconstruct`: Provides standard-form argument (required)
- `method.argument.premise-detect`: Provides list of vulnerable premises (strongly recommended)

## Boundary Conditions

1. **Unconstructable counterexample**: If the argument is entirely sound, do not forcibly fabricate a counterexample — output "No valid counterexample found"
2. **Disputed counterexample**: If the validity of the counterexample depends heavily on specific philosophical intuitions, flag its disputed status

## ARS Interface

- Counterexample reports may be passed to ARS `academic-paper-reviewer` as critical material
- Dialectical analysis of anticipated rebuttals may serve as input to the ARS `revision` stage

## Conditional references

Loaded only on a live ambiguity or an explicit request — never with this method by default: `references/counterexample-checklist.md`, `references/counterexample-examples.md`.
