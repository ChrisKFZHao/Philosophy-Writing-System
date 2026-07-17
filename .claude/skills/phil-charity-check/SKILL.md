---
name: phil-charity-check
description: "Charity Check — verify that argument reconstruction has built the strongest version of the original text, detecting oversimplification, distortion, and uncharitable interpretation"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Charity Check

## Overview

Taking the output of argument reconstruction (an argument in standard form) as the baseline, check whether the original text has been interpreted with sufficient strength — i.e., whether the **Principle of Charity** has been followed.

This Skill does not produce a new argument reconstruction; rather, it **audits an existing reconstruction**. It asks:

- Is the reconstructed argument weaker than what the original text implies?
- Does a stronger, reasonably attributable version exist that was not adopted?
- If multiple reasonable reconstructions exist, was the one with highest priority selected?
- Has the reconstruction annotated its "distance" from the original text?

## Input

- **Required**: Argument reconstruction report (from `phil-argument-reconstruct`)
- **Strongly recommended**: The original text (for cross-checking whether the reconstruction distorts the original)
- **Optional**:
  - Known philosophical background of the author (for charitably determining the most reasonable interpretation)
  - Other related texts by the author (for consistency checking)

## Output

A structured **Charity Audit Report**, containing:
- Overall assessment (Pass / Partial Pass / Fail)
- Charity assessment for each premise
- Alternative interpretation proposals (if stronger versions exist)
- Interpretive distance annotations (how large a "charitable stretching" exists between the reconstructed version and the original text)
- Root-cause analysis (why was a given premise weakened?)
- Improvement recommendations (how to construct a stronger version)

## Methodological Foundations

1. **Principle of Charity**: In interpreting another's assertions, one should maximize their truth and rationality — so long as the interpretation does not contradict the original assertions (Quine, 1960; Davidson, 1973)
2. **Interpretationism**: In understanding another's utterances, charity is not "politeness" but a **methodological requirement** — without assuming that speakers are generally rational, understanding cannot proceed (Davidson, 1984; Dennett, 1987)
3. **Principle of Optimal Interpretation**: Among multiple reasonable interpretations, one should choose the one that makes the speaker most correct — this promotes the quality of philosophical debate (Lewis, 1975)
4. **Critical vs. Interpretive Charity**: The Principle of Charity has a dual meaning — (a) being charitable in **interpretation** (constructing the strongest version), and (b) being charitable in **criticism** (refuting the strongest version rather than a weakened one). This Skill focuses primarily on the former

## Steps

### Step 1: Extract the Comparison Baseline

From the argument reconstruction report, extract:
- The original text segment for each premise (if available)
- The premise as stated in the reconstructed version
- Any annotated "alternative interpretations"

**Output**: A binary comparison table (original-text version vs. reconstructed version for each premise).

### Step 2: Source-Based Strength Assessment

Inspect each premise individually:

**Detection A: Does a stronger reasonable interpretation exist?**

Question: "Are there ambiguities or underdeveloped passages in the original text that permit a stronger interpretation than the current reconstruction?"

- If ambiguity exists and the reconstruction chose the **weaker interpretation** → record as a charity violation
- If the original text explicitly indicates this interpretation → the current reconstruction is justified
- If ambiguity exists without explicit direction → the Principle of Charity requires selecting the stronger version

**Detection B: Does the reconstruction exclude reasonable qualifications that the author may have implied?**

Sometimes the original text is read too absolutely, omitting implicit qualifiers.

Example:
- Original: "Government intervention is usually inefficient"
- Reconstruction: [P1] All government intervention is inefficient ← dropped "usually," universalized the reading
- Charitable version: [P1] Under normal conditions, government intervention tends toward inefficiency ← preserved the original qualification

**Detection C: Is the reconstructed version one that the author has already refuted in their other texts?**

If the author has elsewhere denied a premise in the reconstructed version, the Principle of Charity requires adopting an interpretation consistent with the author's overall position.

**Output**: A charity assessment for each premise (Sufficiently Charitable / Under-charitable / Requires Re-evaluation).

### Step 3: Holistic Structural Charity Assessment

Check not only each independent premise but also the **charity of the overall argument structure**:

- Does the argument structure reflect the author's intended reasoning path?
- If multiple attributable structural paths exist, was the strongest one selected?
- Is there any conflation that should have been split into multiple sub-arguments in a charitable reconstruction?

**Output**: Holistic structural assessment.

### Step 4: Alternative Interpretation Generation

For premises judged "Under-charitable," generate at least one alternative version:

- **Weak alternative**: Still stronger than the current version but closer to the original text
- **Strong alternative**: The strongest possible interpretation within the scope of the current text
- **Annotate "distance"**: The distance between the alternative version and the original text (Small / Medium / Large)

**Output**: A list of alternative versions for each problematic premise.

### Step 5: Write the Audit Report

Output in standard format:

```
## Charity Audit Report

### Basic Information
- **Audit ID**: CHAR-<xxx>
- **Audited Argument**: <ARG identifier>
- **Original Text Source**: <citation>
- **Audit Status**: Pass / Partial Pass / Fail

### Premise-Level Charity Assessment

| Premise | Original Expression | Reconstructed Version | Charity | Issue Description |
|---------|--------------------|-----------------------|---------|-------------------|
| [P1] | <original> | <reconstructed> | Sufficiently Charitable / Under-charitable | <description> |
| ... | | | | |

### Violation Details

#### Violation 1: [Px] Weakened Interpretation

- **Location**: Premise number [Px], step where it appears
- **Original Expression**: <excerpt from original text>
- **Reconstructed Version**: <current version>
- **Problem**: <why this interpretation is unfair to the interlocutor>
- **Alternative Interpretations**:
  - Weak alternative: <stronger but still conservative version> (Distance: Small / Medium / Large)
  - Strong alternative: <strongest possible version> (Distance: Small / Medium / Large)
- **Impact of Substitution**: <how the argument's strength changes if the alternative version is adopted>

### Holistic Structural Charity

- Argument structure reflects authorial intent: Yes / Partial / No
- Explanation: <specific explanation>

### Summary

- Charity violation count: <number>
- Key issues: <most important violations>
- Recommendations: <directions for improvement>
```

## Quality Criteria

1. **Evidence-Driven Principle**: Every judgment must be supported by original-text evidence — charity cannot be denied based on intuition or preference
2. **Author-Tendency Principle**: If the author has more precise formulations elsewhere, prioritize them as the baseline
3. **Alternative Measurability Principle**: Every alternative interpretation must be more reasonable than the current version — do not construct a "super-strong version" that no text supports
4. **Distance Transparency Principle**: If an alternative version requires "stretching" the original text, annotate the distance and provide justification

## Relations to Other Skills

**Dependencies (input sources for this Skill)**:
- `phil-argument-reconstruct`: provides the standard-form argument (required)

**Dependents (downstream consumers of this Skill's output)**:
- `phil-counterexample`: constructs counterexamples against the charitably revised argument, not against the weakened version

## Boundary Conditions

1. **Unimprovable reconstruction**: If the reconstructed version is already the strongest reasonable version → output "Pass," no changes needed
2. **Excessively vague original text**: If it is impossible to confidently determine whether a stronger version exists → note the uncertainty
3. **Charity is not unprincipled concession**: The Principle of Charity does not require turning a bad argument into a good one — if the original text's fundamental defect cannot be remedied through charitable revision, note this honestly
4. **Overall authorial consistency**: If the author's views in two texts are contradictory, note the conflict rather than forcing consistency

## ARS Interface

- Charity audit results can be passed to ARS `academic-paper-reviewer` as a fairness basis for review
- Alternative interpretations can serve as important input for ARS `academic-paper revision` — revising a paper to respond to charitable criticism
