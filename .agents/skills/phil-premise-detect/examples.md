<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Implicit Premise Detection Examples

> Each example demonstrates: given an already reconstructed standard-form argument, systematically detect the unstated implicit premises within it.

---

## Example 1: Conceptual Bridge + Is-Ought Gap

### Input (from argument reconstruction)

```
[P1] All sentient beings can feel pain.
[P2] Animals are sentient beings.
───────
[C]  ∴ We ought not to eat animals.
```

### Output

```
## Implicit Premise Detection Report

### Basic Information
- **Detection ID**: IPD-EX001
- **Based on Argument**: ARG-01
- **Argument Type**: Implicit mixed deduction
- **Original Premises**: P1, P2 → C

### Logical Gap Analysis

1. **[P1+P2] → [C] gap**: The premises concern descriptive facts (animals feel pain); the conclusion involves a normative requirement (we ought not to do something). An Is-Ought gap is present.

### Detection Results

[IP1] Causing pain is morally wrong.
  - Type: Category Jump / Is-Ought Gap
  - Fill: [P1+P2] → [C]
  - Confidence: medium
  - Independently testable: yes — this principle can be assessed through metaethical theory
  - Textual clues: no explicit textual clues
  - If rejected: argument fails completely (premises entail no normative conclusion)

[IP2] "Ought not to eat animals" falls within the scope of the general rule "avoid causing pain."
  - Type: Conceptual Bridge
  - Fill: [IP1] → [C]
  - Confidence: medium
  - Independently testable: yes — one can ask about the scope conditions of "eating animals" and "causing pain"
  - Textual clues: no explicit textual clues
  - If rejected: argument can be restated — could be revised to "we ought not to cause animal suffering for pleasure" or a more refined version

### Overall Assessment

- Implicitness grade: **Medium** (2 implicit premises, 1 of which is a critical Is-Ought gap)
- Key vulnerability points:
  1. [IP1] — If the interlocutor is a moral skeptic or holds a deontological version that does not include this principle, the argument cannot proceed
  2. [IP2] — A weaker gap; after filling, the argument has moderate force
- Recommended testing order:
  1. First test IP1: Is the moral principle "causing pain is wrong" accepted?
  2. Then test IP2: If IP1 is accepted, does "eating animals" definitively fall within the scope of this principle?

### Detection Notes

- This is a simplified version of a typical "vegetarian argument." An expanded version could include:
  conditional exits ("if you have a choice"),
  scope limitations ("not including diets necessary for survival").
  For a full version, each expansion would require additional implicit premises or re-anchoring.
```

---

## Example 2: Missing Universal + Exclusivity Assumption

### Input

```
[P1] In this case, government intervention led to inefficiency.
[P2] This case is a typical case of government intervention.
───────
[C]  ∴ Government intervention always leads to inefficiency.
```

### Output

```
## Implicit Premise Detection Report

### Basic Information
- **Detection ID**: IPD-EX002
- **Based on Argument**: ARG-02
- **Argument Type**: Inductive generalization (from a single case to a universal conclusion)
- **Original Premises**: P1, P2 → C

### Logical Gap Analysis

1. **[P1] → [C] main gap**: From one case ("this case") a universal conclusion ("always") is inferred.
2. **[P2] → [C] auxiliary gap**: Even if P1 holds, "typicality" requires a stronger assumption to support universal generalization.

### Detection Results

[IP1] This case is representative of all cases of government intervention.
  - Type: Missing Universal / Part-Whole Jump
  - Fill: [P1+P2] → [C]
  - Confidence: low
  - Independently testable: yes — requires empirical data (all cases of government intervention) to test
  - Textual clues: P2 claims "typicality" but this has no empirical evidence base
  - If rejected: argument fails completely — one cannot induce from a single case to all cases

[IP2] There exists no government intervention that does not lead to inefficiency.
  - Type: Exclusivity Assumption
  - Fill: [P1] → [C]
  - Confidence: low
  - Independently testable: yes — can be tested through counterexamples (if any single case of efficient government intervention is found, the premise is out)
  - Textual clues: the original text does not discuss whether government intervention can possibly be efficient
  - If rejected: argument fails completely — the existence of a counterexample means induction cannot hold

### Overall Assessment

- Implicitness grade: **High** (2 low-confidence premises; rejecting either causes complete failure)
- Key vulnerability points:
  1. [IP1] — This is a classic inductive leap. It requires substantial empirical evidence to support.
  2. [IP2] — Even finding just one counterexample of efficient government intervention renders the argument untenable.
- Recommended testing order:
  1. First test IP2: search for counterexamples — do cases of efficient government intervention exist?
  2. Then test IP1: if no counterexample is found, one must still prove "typicality" — to support universal induction

### Detection Notes

- This argument infers a universal conclusion from a single case — a classic weakness of inductive logic.
  The conclusion could be downgraded to "government intervention tends to lead to inefficiency,"
  which would change the degree of the implicit premises without changing their number.
```

---

## Example 3: Existential Presupposition + Background Framework (Srinivasan Anger Argument)

### Input (based on the previously reconstructed Srinivasan ARG-03)

```
[P1] Apt anger has intrinsic value (the conclusion of ARG-02).
[P2] Anger can simultaneously be prudentially irrational.
[P3] Prudential irrationality does not cancel the aptness or intrinsic value of anger.
[P4] Therefore, victims of injustice face a genuine normative conflict.
───────
[C]  ∴ This normative conflict constitutes a second-order injustice — "affective injustice."
```

### Output

```
## Implicit Premise Detection Report

### Basic Information
- **Detection ID**: IPD-EX003
- **Based on Argument**: SRINIVASAN-ARG-03
- **Argument Type**: Deductive (with normative claims)
- **Original Premises**: P1-P4 → C

### Logical Gap Analysis

1. **[P4] → [C] gap**: From "there exists a normative conflict" to "the normative conflict constitutes an injustice" — needs supplementation of a standard of injustice.
2. **[P2] → [P3] transition**: P3 claims that prudential irrationality does not cancel intrinsic value, requiring a value incommensurability premise.
3. **[P1] footing**: The assertion of intrinsic value itself depends on certain background presuppositions.

### Detection Results

[IP1] The relation between intrinsic value and prudential value is one of incommensurability — neither can override the other.
  - Type: Background Framework
  - Fill: [P2] → [P3]
  - Confidence: low (core point of contention)
  - Independently testable: yes — can be adjudicated through value theory
  - Textual clues: "prudential reason does not trump apt anger" [notes §2]
  - If rejected: argument severely weakened (if prudential value can override intrinsic value, the normative conflict does not exist)

[IP2] If a group is systematically and coercively placed in a harmful state, and that state stems from the group's subordinate position,
      then that state constitutes an injustice.
  - Type: Existential Presupposition / Normative Presupposition (standard of injustice)
  - Fill: [P4] → [C]
  - Confidence: medium
  - Independently testable: yes — can be assessed through standards of injustice in social/political philosophy
  - Textual clues: the concept of "second-order injustice" implicitly contains this standard
  - If rejected: argument fails completely (even if the normative conflict exists, it may be merely unfortunate rather than unjust)

[IP3] "Emotions" have intrinsic value — they are cognitive, not merely affective.
  - Type: Existential Presupposition / Background Framework
  - Fill: Foundation of [P1]
  - Confidence: low (this is a presupposition of cognitivist emotion theory)
  - Independently testable: partially — requires adjudication through philosophy of emotion
  - Textual clues: analogy to aesthetic experience (the similarity between beauty and anger)
  - If rejected: P1 does not hold → the starting point of the entire argument chain collapses

[IP4] The counterproductive effects of anger are products of social structure, not intrinsic features of anger itself.
  - Type: Background Framework
  - Fill: [P2] ↔ [P3]
  - Confidence: medium
  - Independently testable: partially — requires empirical analysis of social structures
  - Textual clues: "this may be a false dichotomy that maintains the status quo" [notes §7c]
  - If rejected: the argument can continue (counterproductive effects could still be intrinsic, but the normative conflict no longer "victimizes" the victim)

### Overall Assessment

- Implicitness grade: **High** (4 implicit premises, 3 of which have low confidence)
- Key vulnerability points:
  1. [IP3] — The intrinsic value of emotions is the core point of contention. If emotions lack intrinsic value, P1 and everything that follows lack foundation.
  2. [IP1] — Does incommensurability hold? This determines whether the normative conflict genuinely exists.
  3. [IP2] — Even if the first two steps hold, whether the normative conflict constitutes "injustice" requires an independent theory of injustice.
- Recommended testing order:
  1. First test IP3: Is there principled grounding for "emotions have intrinsic cognitive value"?
  2. Then test IP1: Assuming IP3 holds, can the incommensurability of intrinsic value and prudential value be argued?
  3. Then test IP2: If IP1 holds, does the normative conflict satisfy the standard of "injustice"?
  4. Finally test IP4: A supplementary rather than critical test
```

---

## Example 4: Hidden Exclusivity Assumption — Empiricist Argument

### Input

```
[P1] All human knowledge comes from sensory experience.
[P2] Mathematical truths do not come from sensory experience.
───────
[C]  ∴ Mathematical truths are not knowledge.
```

### Output

```
## Implicit Premise Detection Report

### Basic Information
- **Detection ID**: IPD-EX004
- **Based on Argument**: ARG-04
- **Argument Type**: Deductive (Barbara form)
- **Original Premises**: P1, P2 → C

### Logical Gap Analysis

1. **[P1] → [C] main gap**: The argument assumes that "coming from sensory experience" in P1 is a necessary condition for "knowledge" — but could the intension/extension of "knowledge" admit other possibilities?

### Detection Results

[IP1] The sole source of knowledge is sensory experience.
  - Type: Exclusivity Assumption + Background Framework
  - Fill: [P1] → [C]
  - Confidence: low (precisely the fundamental dispute between empiricism and rationalism)
  - Independently testable: yes — one can ask: are there non-empirical sources of knowledge? (a priori knowledge, conceptual truths)
  - Textual clues: Premise P1 is itself the core assertion of empiricism, but it is treated as the only option
  - If rejected: argument fails completely — if non-empirical sources of knowledge exist (rationalism), C does not follow

[IP2] The conceptual nature of mathematical truths is not a derivative of "sensory experience."
  - Type: Conceptual Bridge (reverse direction)
  - Fill: Internal to [P2]
  - Confidence: medium
  - Independently testable: yes — can be tested through epistemology/philosophy of mathematics (e.g., intuitionism vs. empiricist philosophy of mathematics)
  - Textual clues: no explicit textual clues
  - If rejected: the argument needs restatement — if mathematical truths are derived from experience, the premise is negated

### Overall Assessment

- Implicitness grade: **Medium** (2 implicit premises, but the most central is IP1)
- Key vulnerability points:
  1. [IP1] — Exclusivity assumption: do non-sensory sources of knowledge exist?
  For a rationalist, this premise begs the question at the crucial point.
- Recommended testing order:
  1. First test IP1: Does rationalism provide a viable path to non-empirical sources of knowledge?
  2. Then test IP2: If IP1 is rejected, IP2 need not be tested (the argument has already failed)

### Detection Notes

- This argument is itself valid (as a deduction), but it is deeper than it appears on the surface.
  It effectively presupposes its conclusion in the core battlefield of "empiricism vs. rationalism" —
  the argument's validity depends on whether the reader has already accepted the empiricist framework (IP1).
  For a reader who has not accepted that framework, the argument's premises already contain part of the conclusion.
```

---

## Example 5: Full Detection Suite — Plato's *Euthyphro* Divine Command Theory

### Input

```
[P1] An action is pious if and only if it is loved by the gods.
[P2] The gods love certain actions (e.g., worshipping the gods).
[P3] The gods do not love certain other actions (e.g., murder).
───────
[C]  ∴ Murder is impious.
```

### Output

```
## Implicit Premise Detection Report

### Basic Information
- **Detection ID**: IPD-EX005
- **Based on Argument**: ARG-05 (Euthyphro definitional argument)
- **Argument Type**: Deductive / Definitional
- **Original Premises**: P1-P3 → C

### Logical Gap Analysis

1. **[P1+P3] → [C] gap**: Needs supplementation of the inference chain from "not loved" to "impious."
2. **P1 footing problem**: P1 defines "pious" as "loved by the gods" — but is this the correct definition?
   (Socrates himself questions this in the dialogue)
3. **Implicit entity presupposition**: The argument presupposes the existence of the gods — but this is not stated.

### Detection Results

[IP1] If an action is not loved by the gods, then it is not an instance of "being loved by the gods"; therefore that action is not pious (according to P1).
  - Type: Conceptual Bridge
  - Fill: [P3] → [C]
  - Confidence: high (within the scope of P1's definition, this inference is strong)
  - Independently testable: no — depends solely on P1's definition
  - Textual clues: direct logical derivation
  - If rejected: C can still be derived from P1+P3 (negating IP1 would only be meaningful under a negation of P1)

[IP2] One or more gods exist, and the love and hatred of these gods are morally relevant.
  - Type: Existential Presupposition
  - Fill: Makes the entire argument meaningful
  - Confidence: low (concerning the theism vs. atheism dispute)
  - Independently testable: partially — the entire philosophical debate between theism and atheism unfolds here
  - Textual clues: the predicate "loved by the gods" presupposes the existence of gods
  - If rejected: argument fails completely — without gods, P1-P3 all lose their anchor

[IP3] The love and hatred of the gods toward actions are constant and non-contradictory.
  - Type: Background Framework
  - Fill: Coherence of [P2] + [P3]
  - Confidence: medium
  - Independently testable: partially — if theologically the gods may love different actions in different cultures,
    then IP3 does not hold and the argument is difficult to generalize
  - Textual clues: P2 and P3 implicitly assume that the gods' love and hatred are determinate
  - If rejected: argument severely weakened — if divine love is contradictory, P2 and P3 cannot both be true

[IP4] The definition of "pious" in P1 exhausts all aspects of the concept — piety has no content beyond "being loved by the gods."
  - Type: Exclusivity Assumption
  - Fill: [P1] itself
  - Confidence: low (precisely the core of what Socrates challenges in the dialogue)
  - Independently testable: yes — can be tested through conceptual analysis
  - Textual clues: the definition of P1 itself
  - If rejected: argument fails completely — if P1 does not hold, the definitional foundation disappears

### Overall Assessment

- Implicitness grade: **High** (4 implicit premises, 2 of which have low confidence, 1 medium)
- Key vulnerability points:
  1. [IP2] — The most basic entity presupposition: if there are no gods, the entire argument is meaningless
  2. [IP4] — The core of conceptual analysis: does the definition exhaust? This is precisely what Socrates reveals in the dialogue
  3. [IP3] — An auxiliary problem; but if both IP2 and IP4 pass, IP3 can still pose a challenge
- Recommended testing order:
  1. First test IP2: Do gods exist? If so, what properties do they have?
  2. Then test IP4: If P1 passes, is "pious" genuinely equivalent to "loved by the gods"?
  3. If the first two steps both pass, then test IP3: the constancy of divine love

### Detection Notes

- This is one of the earliest and most famous cases of implicit premise detection in the history of analytic philosophy.
  Socrates in the dialogue is not negating P1; rather he is asking:
  "Is the pious loved by the gods because it is pious, or is it pious because it is loved by the gods?"
  This is precisely a detection targeting IP4's exclusivity assumption.
```
