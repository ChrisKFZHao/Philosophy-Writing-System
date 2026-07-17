---
name: phil-premise-detect
description: "Implicit premise detection — systematically detecting unstated assumptions, hidden conditions, and framework presuppositions in philosophical arguments; classifying and evaluating all gaps that constitute implicit obstacles to an argument's validity"
---

# Implicit Premise Detection

## Overview

Taking the standard form of a reconstructed argument (numbered premise list → conclusion) as input, systematically detect the **unstated premises** within the argument. This capability is the "X-ray machine" of analytic philosophy — it reveals what assumptions lie hidden beneath the surface premises of an argument, supporting the inference, and whether those assumptions withstand scrutiny.

This Skill does not detect whether an argument succeeds (that is the work of structural assessment); rather, it detects **how much has been left unsaid**. In philosophical writing, finding an opponent's hidden premises is a prerequisite step for rebuttal; finding one's own hidden premises is a demand of intellectual rigor.

## Input

- **Required**: A standard-form argument produced by `phil-argument-reconstruct` (numbered premises [P1]...[Pn], conclusion [C])
- **Optional**:
  - The source text (for textual clue analysis)
  - The author's known philosophical positions (for detecting framework presuppositions)
  - An exclusion list (premises already known to the user, not needing re-detection)

## Output

A structured **implicit premise detection report** conforming to the `premise-audit-schema.json` specification, containing:
- Each detected implicit premise: [IP1], [IP2]...
- Type classification for each implicit premise
- Fill location (between which premise and conclusion / other premise)
- Confidence assessment (high / medium / low)
- Textual clues (if suggested in the source text)
- Impact on the argument if the premise is rejected
- Rationale / response summary (optional challenge and reply pathways)
- Overall implicitness overview (to what extent the argument depends on unstated assumptions)

## Methodological Foundations

1. **Enthymeme Theory**: Aristotle first discovered that everyday arguments always contain implicit premises (Aristotle, *Rhetoric*, I.2.1358a). Modern literature (Walton, 2008; Hitchcock, 2016) has developed rigorous methods for identifying enthymematic premises.
2. **Defeasible Reasoning**: Most philosophical arguments are defeasible rather than deductive — detecting implicit premises serves to determine under what conditions the argument fails (Pollock, 1987; Toulmin, 1958).
3. **Conceptual Analysis Tradition**: Many implicit premises originate from the lack of explicit connections between concepts — this is precisely the entry point for conceptual analysis (see `phil-conceptual-analysis`).
4. **Presupposition Theory**: Certain propositions are not "premises" but "presuppositions" — they must hold for the assertion itself to be meaningful (Strawson, 1950; Stalnaker, 1974).
5. **Principle of Charity and Fidelity**: When detecting implicit premises, assume the best interpretation of the author's intent within reasonable bounds, but annotate the distance from the source text (Quine, 1960; Davidson, 1973).

## Steps

### Step 1: Receive and Confirm Input Structure

Determine whether the input argument structure is complete. Confirm:
- Whether the explicit premises [P1]...[Pn] are independent, complete statements
- Whether the conclusion [C] is clearly stated
- Whether the argument type (deductive/inductive/abductive, etc.) has been annotated

If the input is incomplete, return a request for supplementation — implicit premises cannot be detected without a complete argument structure.

**Output**: Confirmed input structure (premise numbers and conclusion, ready for reuse).

### Step 2: Logical Gap Analysis

Examine the inference path from premises to conclusion one step at a time, locating gaps that need filling.

For a deductive argument:
- Check the **premise-conclusion gap**: Does the premise set {P1, ..., Pn} entail C?
  - If yes → no implicit premises needed (this is the rare ideal case)
  - If no → premises need to be supplied to establish the entailment relation

For an inductive argument:
- Check the **leap magnitude**: How large is the inductive leap from sample to population?
  → The implicit premise is often "the sample is representative and random"

For an abductive argument:
- Check the **competing hypothesis space**: Have all competing hypotheses been ruled out?
  → The implicit premise is often "there is no better explanation besides this one"

**Output**: Annotate the start and end points of each gap (e.g., "gap from P1, P2 to C," "leap from P3 to P4").

### Step 3: Detect Implicit Premises by Type

Fill each gap one by one, detecting according to the following classification system:

#### 3.1 Missing Universal / Missing Generalization

The missing step of generalization when moving from "a particular case has property F" to "all cases have property F."

- **Form**: From `∃x(Fx)` to `∀x(Fx)`
- **Detection trigger**: Premises involve particular/existential statements; conclusion involves a universal statement
- **Implicit premise fill**: `[IP] All similar cases also have property F`

#### 3.2 Conceptual Bridge / Missing Conditional

The premises use concept A; the conclusion uses concept B, but the logical relation between A and B is not stated.

- **Form**: From "X is A" to "X is B" (or equivalently "X should have concept B applied to it")
- **Detection trigger**: The core predicate in the premises differs from the core predicate in the conclusion, with no explicit connection
- **Implicit premise fill**: `[IP] All A are also B` (or: "If something is A, then it falls under category B")

#### 3.3 Category Jump / Is-Ought Gap

Moving from descriptive premises to normative conclusions (or from possibility to actuality, from part to whole, etc.).

- **Common forms**:
  - Descriptive → Normative: `X operates in manner Y` → `We ought to support X` (Hume, *Treatise*, III.i.1)
  - Possible → Actual: `X could happen` → `X will / has happened`
  - Part → Whole: `A part of X has F` → `X has F` (fallacy of composition)
- **Detection trigger**: The type of premises does not correspond to the type of conclusion
- **Implicit premise fill**: `[IP] Descriptive facts entail normative conclusions` (or the corresponding principle for other jumps)

#### 3.4 Existential Presupposition

The argument tacitly presupposes the existence of certain entities, properties, states, or categories — without them, the premises or conclusion lose meaning.

- **Form**: Argument is meaningful → entity type T exists
- **Detection trigger**: The argument uses expressions like "X," "F," but does not prove the existence of X or F-instances
- **Implicit premise fill**: `[IP] Entities of type T exist` (e.g., "moral facts exist," "universals exist")

#### 3.5 Exclusivity Assumption / Closed World

The argument assumes no other possibilities exist — i.e., the options given are the only ones, but in philosophy there is often a third possibility.

- **Form**: The argument claims "either A or B" (and infers C from this), but does not prove ¬(A ∧ B), and does not prove that C does not exist
- **Detection trigger**: Occurrence of "either...or...," "there is no other option," "the only possible explanation is"
- **Implicit premise fill**: `[IP] There is no third, fourth, ... possibility`

#### 3.6 Background Framework / Paradigm Assumption

The argument depends on a large, undeclared philosophical presupposition that typically spans multiple subfields.

- **Form**: The argument operates within a certain philosophical framework, but does not declare the framework's threshold assumptions
- **Detection trigger**: The argument's conclusion presupposes a basic presupposition of some domain (e.g., "the physical world exists," "other minds exist," "causal determinism holds")
- **Implicit premise fill**: `[IP] The basic assumptions of framework F hold` and annotate the framework name

#### 3.7 Hidden Quantification Shift

The premises use vague quantifiers ("many," "most," "some"), and the conclusion treats them as having a determinate quantity.

- **Form**: From "F(X)" to "G(X)," where the quantificational scope of F is vague
- **Detection trigger**: Premises use vague vocabulary; the conclusion issues a precise assertion
- **Implicit premise fill**: `[IP] The scope of F is sufficient to support the conclusion's precise assertion`

**Output**: For each gap, a list of filled implicit premises, each annotated with type, form, textual location, and confidence.

### Step 4: Evaluate Each Implicit Premise

For each detected [IP], evaluate its properties:

#### 4.1 Confidence Assessment

| Level | Definition | Typical Case |
|-------|-----------|-------------|
| **High** | Most readers (including the author) would accept the premise; an opponent would seem unreasonable to reject it | Everyday background presuppositions, consensual frameworks |
| **Medium** | The author likely implicitly presupposes this premise, but philosophically reasonable disagreement exists | Contested but common assumptions |
| **Low** | The implicit premise carries high philosophical weight; most opponents would attack the argument at this point | Core, undefended assumptions |

#### 4.2 Independent Testability

Investigate: Can this [IP] be tested independently of the argument itself?

- **Independently testable**: The premise can be tested through empirical evidence, conceptual analysis, or more fundamental principles
- **Not independently testable**: The premise is meaningful only within the context of the argument (i.e., the argument is circular — premise and conclusion are bound together)

#### 4.3 Impact of Rejecting the Premise

Analyze: If an interlocutor rejects this implicit premise, how is the argument affected?

- **Complete failure**: The argument depends entirely on this premise; rejecting it means the conclusion does not follow
- **Severely weakened**: The argument can continue but its logical force drops substantially
- **Mildly diminished**: The argument can be reconstructed but needs alternative support

**Output**: For each [IP], its confidence level, independence assessment, and rejection impact.

### Step 5: Overall Implicitness Assessment

Calculate overall implicitness — i.e., to what extent the argument depends on unstated assumptions.

- **Low implicitness** (0-2 implicit premises, and confidence ≥ medium) → The argument is largely explicit; it mainly relies on consensual premises
- **Medium implicitness** (3-5 implicit premises, or at least 1 low-confidence premise) → The argument has gaps; viable space for rebuttal exists
- **High implicitness** (≥ 6 implicit premises, or at least 3 low-confidence premises) → The argument relies heavily on undefended assumptions

These grades help the user determine: against this argument, where should one direct one's efforts in rebuttal? Which implicit premise is the most vulnerable (lowest confidence + greatest impact if rejected)?

**Output**: Overall assessment grade and recommended priority target for attack.

### Step 6: Write the Detection Report

Output the complete detection report in standard format:

```
## Implicit Premise Detection Report

### Basic Information
- **Detection ID**: <unique identifier>
- **Based on Argument**: <cite ARG number or self-defined>
- **Argument Type**: <copy from input>
- **Original Premises**: <brief summary>

### Logical Gap Analysis

1. Gap from [Px] to [Py]: <description>
2. Gap from [Px] to [C]: <description>
...

### Detection Results

[IP1] <full statement of the implicit premise>
  - Type: <missing universal / conceptual bridge / category jump / exclusivity assumption / background framework / existential presupposition / hidden quantification shift>
  - Fill: [Px] → [Py/C]
  - Confidence: <high / medium / low>
  - Independently testable: <yes / no>
  - Textual clues: <text in the source that suggests this premise, or "no textual clues">
  - If rejected: <complete failure / severely weakened / mildly diminished>

[IP2] ...

### Overall Assessment

- Implicitness grade: <low / medium / high>
- Key vulnerability point: <the [IP] with lowest confidence + greatest impact if rejected>
- Recommended testing order:
  1. First test [IPx] (lowest confidence; if rejected, argument fails completely)
  2. Then test [IPy] (medium confidence, but highly independently testable; resolvable through empirical/conceptual methods)
  ...

### Detection Notes

<Key points to note from the operational process>
```

## Quality Criteria

1. **Completeness Principle**: Detect all logical gaps — do not detect only the obvious ones.
2. **Fill-the-Strongest Principle**: The filled implicit premise should be the minimal supplementation needed to make the argument hold — do not construct an assumption stronger than necessary.
3. **Discriminability Principle**: Different gaps should use different types — if two [IP]s have the same type, check whether they are duplicate detections.
4. **Independence Principle**: Each implicit premise should be an independent statement — not duplicating explicit premises or other implicit premises.
5. **Principle of Charity**: Assume the best interpretation of the author's intent within reasonable bounds — but if an unreasonably strong assumption must be constructed to salvage the argument, annotate this honestly.

## Relations to Other Skills

**Upstream (input sources for this Skill)**:
- `phil-argument-reconstruct`: Provides the standard-form argument (required)

**Downstream (skills that use this Skill's output)**:
- `phil-counterexample`: Constructs counterexamples targeting detected vulnerable implicit premises
- `phil-charity-check`: Uses detection results to assess whether the principle of charity has been satisfied (detecting implicit premises is part of charitable reconstruction)
- `phil-ontological-commitment`: Takes existential-presupposition-type implicit premises as input for further analysis of ontological commitments

## Boundary Conditions

1. **Perfect argument (no gaps)**: If the premises genuinely entail the conclusion, output "No implicit premises detected" rather than forcing a fill.
2. **Over-detection**: Do not detect every possible premise; only detect premises **necessary** for the argument to hold — if a gap can remain unfilled and the argument might still be valid, it is not considered an implicit premise.
3. **Argument invalid**: If the argument is logically invalid and cannot be repaired through reasonable implicit premises, output "Argument does not hold; implicit premises cannot repair it" with an explanation.
4. **Nested implicit premises**: If one implicit premise requires another implicit premise to support it (IP1 depends on IP2), annotate the hierarchy.
5. **Linguistic/textual ambiguity**: If the source text is too ambiguous to determine where the gap lies, annotate the uncertainty and offer possible dual analyses.

## ARS Interface

- Detection reports can be directly passed to ARS `academic-paper` for the "methodological limitations" or "implicit assumptions" section of a paper.
- Detection findings can serve as critical grounds for ARS `academic-paper-reviewer`.
