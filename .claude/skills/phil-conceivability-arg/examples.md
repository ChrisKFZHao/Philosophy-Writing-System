# Conceivability Argument Analysis Examples

> This document demonstrates the practical application of conceivability argument analysis across different argument types and difficulty levels. Each example shows the complete input-to-output process.

---

## Example 1: Zombie Argument (Chalmers) — Positive Conceivability to Metaphysical Possibility

### Input

> Zombies are conceivable. A zombie is a being that is physically identical to a conscious human but lacks phenomenal consciousness — there is nothing it is like to be a zombie. I can coherently imagine a world physically identical to ours in which no one is conscious. Since zombies are conceivable, zombies are metaphysically possible. And if zombies are metaphysically possible, then physicalism is false — because physicalism requires that the physical facts metaphysically necessitate the phenomenal facts. Therefore, physicalism is false.

### Output

```
## Conceivability Argument Analysis Report

### Basic Information
- **Argument ID**: CEX001
- **Argument Type**: Conceivability Argument (anti-physicalist)
- **Logical Form**: ◇C(Z), C(Z)→◇Z, ◇Z→¬P ∴ ¬P
- **Source**: Chalmers-style zombie conceivability argument

### Chain Reconstruction

L1: Zombies (physical duplicates of conscious beings lacking phenomenal consciousness) are conceivable.
L2: If zombies are conceivable (in the relevant sense), then zombies are metaphysically possible.
L3: If zombies are metaphysically possible, then physicalism is false.
L4: Therefore, physicalism is false.

**Suppressed Premises**:
- SP1: Physicalism entails that the physical facts metaphysically necessitate the phenomenal facts (□(P→Q)).
- SP2: The conceivability of zombies is ideal positive conceivability (not merely prima facie).
- SP3: The primary-to-secondary possibility entailment holds for phenomenal-physical identities.

### Conceivability Type Assessment

**Claimed Type**: Ideal Positive Conceivability
**Evidence**: The argument claims zombies can be "coherently imagined" in a complete physical scenario. This is a positive conceivability claim.
**Type Appropriateness**: Ambiguous. The argument needs ideal positive conceivability to underwrite the move to metaphysical possibility (per Chalmers's framework). But the scenario description is schematic ("a world physically identical to ours") rather than fully specified. This falls between positive and ideal positive conceivability.
**Controversy**: Dennett and others deny that zombies are even positively conceivable — they argue the concept is incoherent because consciousness just is a functional-physical phenomenon.

### Link-by-Link Evaluation

| Link | Description | Rating | Key Issue |
|------|-------------|--------|-----------|
| L1 | Conceivability to Possibility | Questionable | Two-dimensional defense required but not fully provided; phenomenal concept strategy not engaged |
| L2 | Possibility to Conclusion | Adequate | Entailment holds given physicalism's supervenience requirement, but Type-B materialism not addressed |

**L1 Detailed Evaluation**:
- Kripke's Necessary A Posteriori Challenge: The argument must show that "consciousness is physical" is not a necessary a posteriori identity like "water is H2O." If phenomenal concepts are like water-concepts (revealing only contingent features), the conceivability of zombies is no more significant than the conceivability of water not being H2O. The argument does not adequately engage this challenge.
- Two-Dimensional Semantics Defense: Chalmers argues that ideal primary positive conceivability of zombies entails primary possibility, and given that phenomenal concepts are not "semantically neutral" (they reveal essence), primary possibility entails secondary possibility. This is a sophisticated defense, but the argument as presented here does not develop it — it relies on an intuitive conceivability claim without the semantic framework.
- Phenomenal Concept Strategy (Balog, Loar): The argument does not address the claim that the conceivability of zombies is an artifact of special phenomenal concepts, not a guide to metaphysical possibility. This is a significant omission.
- Completeness: Can a complete physical description be specified such that we can verify physical identity with the conscious counterpart? The schematic nature of the description ("physically identical") is a placeholder, not a full specification.

**L2 Detailed Evaluation**:
- The entailment from zombie possibility to physicalism's falsity is logically valid given physicalism's commitment to the metaphysical necessity of physical-to-phenomenal supervenience.
- However, Type-B materialists (Block, Stalnaker) accept the epistemic gap between physical and phenomenal but deny the ontological gap — they treat consciousness as a necessary a posteriori identity. The argument does not address Type-B materialism, which is a dialectical gap.

### Gap Analysis

**Gap Severity Ranking**:
1. **L1 Gap (Severity: Critical)**: The move from conceivable to possible is inadequately defended. The argument needs either (a) the full two-dimensional defense or (b) an alternative modal epistemology. Without it, the Kripkean challenge remains unanswered.
2. **Type-B Materialism Gap (Severity: High)**: Even if L1 is defended, L2 must engage Type-B materialism, which accepts the epistemic gap (and thus the conceivability) but denies the metaphysical gap.
3. **Completeness Gap (Severity: Medium)**: The zombie scenario is underdescribed, making the conceivability claim underdetermined.

**Cumulative Assessment**: The weaknesses compound. L1's failure to engage the phenomenal concept strategy interacts with L2's failure to address Type-B materialism — both target the same underlying issue (whether the epistemic conceivability tracks metaphysical possibility).

### Modal Framework Assessment

- **System Required**: S5 (universal accessibility) typically required for Chalmers-style arguments to collapse iterated modalities.
- **Framework Provided**: Implicit S5 — the argument moves from conceivability (in actual world) to metaphysical possibility (in some world) to necessity of physicalism's falsity (in all worlds if physicalism is necessarily true).
- **Framework Rating**: Implicit but reconstructable. S5 for metaphysical modality is controversial — the argument should address this.

### Overall Strength Rating: Weak

The argument's central inference (conceivability to metaphysical possibility) is inadequately defended. The Kripkean challenge (necessary a posteriori) and the phenomenal concept strategy are standard objections that the argument does not address. The two-dimensional semantic defense that could potentially bridge the gap is not developed. While the logical form is valid and the entailment link (L2) is structurally sound, the core link (L1) is Questionable. The argument has dialectical value as a challenge to physicalism but does not compel assent as presented. To reach Medium, the argument would need to engage the phenomenal concept strategy and develop the primary-to-secondary possibility entailment. To reach Strong, it would additionally need to defend S5 for metaphysical modality and provide a fully specified zombie scenario.
```

---

## Example 2: Descartes' Real Distinction Argument — Clear and Distinct Conceivability

### Input

> I know that I exist as a thinking thing. I can clearly and distinctly conceive of myself as a thinking thing existing without my body. Since God can bring about whatever I clearly and distinctly conceive, it follows that I am really distinct from my body and can exist without it. The mind is a substance whose whole essence is to think; the body is a substance whose essence is extension. Since I can conceive the one without the other, they must be distinct substances.

### Output

```
## Conceivability Argument Analysis Report

### Basic Information
- **Argument ID**: CEX002
- **Argument Type**: Conceivability Argument (substance dualist)
- **Logical Form**: CCD(M without B) → ◇(M without B) → M ≠ B
- **Source**: Descartes, Meditations on First Philosophy (Sixth Meditation)

### Chain Reconstruction

L1: I can clearly and distinctly conceive of myself (a thinking thing) existing without my body (an extended thing).
L2: If I can clearly and distinctly conceive of X existing without Y, then X can exist without Y (God can bring it about).
L3: If X can exist without Y, then X is really distinct from Y (they are different substances).
L4: Therefore, I (mind) am really distinct from my body.

**Suppressed Premises**:
- SP1: Clear and distinct conception is a reliable guide to metaphysical possibility (the "truth rule").
- SP2: God exists and is not a deceiver (established earlier in the Meditations).
- SP3: Real distinction between substances follows from the possibility of separate existence.

### Conceivability Type Assessment

**Claimed Type**: Clear and Distinct Conceivability (Descartes's own category, akin to ideal rational conceivability)
**Evidence**: Descartes claims "clear and distinct" perception, his highest epistemic standard — an idea is clear when "present and accessible to the attentive mind" and distinct when "so precise and different from all other objects that it contains within itself nothing but what is clear."
**Type Appropriateness**: Strong by Descartes's standards — clear and distinct perception purports to provide indubitable access to reality. However, by modern standards, clear and distinct perception is an epistemic operator, not a metaphysical one: it tells us about our concepts, not about modal reality.
**Historical Note**: Descartes lacks the conceptual resources of Kripke and the two-dimensional framework. This analysis applies modern categories retrospectively for evaluation while acknowledging the historical context.

### Link-by-Link Evaluation

| Link | Description | Rating | Key Issue |
|------|-------------|--------|-----------|
| L1 | Clear and distinct conception to possibility | Questionable | Cartesian "clear and distinct" perception conflated with genuine modal access |
| L2 | Possibility of separate existence to real distinction | Adequate | Valid given substance metaphysics, but depends on contested identity conditions |
| L3 | Real distinction to substance dualism | Adequate | Follows from L2 given Cartesian substance framework |

**L1 Detailed Evaluation**:
- The gap between "I can conceive of myself without a body" and "I can exist without a body" is the classic gap. Modern modal epistemology (Kripke) shows that conceivability can be an illusion of ignorance: I might conceive of water without H2O because I do not know water's essence. Similarly, I might conceive of myself without my body because I do not know my own essence.
- The Cartesian truth rule ("whatever I clearly and distinctly perceive is true") is defended by appeal to God's non-deceptive nature, which is itself established by an argument many find circular. Without God, the truth rule loses its foundation, and clear and distinct conception collapses to a psychological state with no modal guarantee.
- By modern standards: the argument achieves at best prima facie or negative conceivability. It does not demonstrate that the mind can exist without the body — only that the mental concept does not analytically entail the physical concept.

**L2 Detailed Evaluation**:
- Given a substance-attribute ontology, if two things can exist separately, they are distinct substances. This is definitional within Descartes's framework.
- However, this inference only works if the separate existence is genuinely possible. L2 inherits all the problems of L1.

### Gap Analysis

**Gap Severity Ranking**:
1. **L1 Gap (Severity: Critical)**: The move from conceivability to metaphysical possibility relies on the Cartesian truth rule, which is epistemically circular (requires God, whose existence is established by an argument that itself depends on clear and distinct perception). Without independent justification, L1 is Broken by modern standards.
2. **Essence Opacity Gap (Severity: High)**: Descartes assumes the mind's essence (thinking) is fully transparent to introspection, such that conceiving myself without a body reveals my essential nature. If my essence is partially opaque — if, for example, my essence involves embodiment in ways I do not introspectively grasp — the conceivability is an illusion.

**Bridgeability**: The L1 gap is unbridgeable within Descartes's framework without circularity. However, modern Cartesian dualists sometimes reformulate the argument without the truth-rule dependence, relying instead on direct modal intuition or conceivability under ideal conditions.

### Modal Framework Assessment

- **System**: Not formalized — pre-Kripkean, pre-possible-worlds semantics.
- **Accessibility**: Implicitly universal — what is conceivable is possible simpliciter.
- **Framework Rating**: Not applicable in modern terms. The argument operates with a pre-modal-logic conception of possibility.
- **Retrospective Note**: The argument would need substantial reconstruction to engage with modern modal epistemology.

### Overall Strength Rating: Weak (Retrospective: Broken by Modern Standards)

The argument's foundational move — from clear and distinct conception to metaphysical possibility — depends on the Cartesian truth rule, which is itself contested and arguably circular. By modern standards, the conceivability claim is at best negative conceivability, insufficient to establish metaphysical possibility. The Kripkean challenge (essence opacity) applies directly: Descartes assumes the mind's essence is transparent to introspection, but if embodiment is essential to personhood in ways not revealed by introspection, the conceivability is illusory. The argument is historically significant but fails by contemporary modal epistemological standards.
```

---

## Example 3: Kripke's Necessary A Posteriori — A Limit on Conceivability Arguments

### Input

> Consider the proposition "Water is not H2O." I can conceive of water — the clear, drinkable liquid — existing without being composed of H2O molecules. I can imagine a world where the liquid in the lakes and rivers has a different chemical composition but looks, tastes, and behaves exactly like water. This seems perfectly conceivable. Yet it is metaphysically impossible: given that water is H2O in the actual world, and "water" is a rigid designator, there is no possible world in which water is not H2O. My conceivability is an illusion — I am actually conceiving of something that is superficially like water but is not water. The necessary a posteriori shows that conceivability is not a reliable guide to possibility when the conceiving subject is ignorant of essential natures.

### Output

```
## Conceivability Argument Analysis Report

### Basic Information
- **Argument ID**: CEX003
- **Argument Type**: Meta-Level Analysis — Critique of Conceivability Arguments
- **Logical Form**: Demonstration that ◇C(P) does not entail ◇P when P involves a necessary a posteriori truth
- **Source**: Kripke, Naming and Necessity (1980)

### Chain Reconstruction

This is not a conceivability argument itself but a critical demonstration of the conceivability-to-possibility gap. The argument structure is:

L1: "Water is not H2O" is conceivable (I can imagine a superficially similar liquid in another possible world).
L2: "Water is not H2O" is metaphysically impossible (because water = H2O is necessary a posteriori).
L3: Therefore, conceivability does not entail metaphysical possibility for necessary a posteriori propositions.
L4: Therefore, any conceivability argument must address whether the target proposition involves a necessary a posteriori truth.

### Conceivability Type Assessment

**Type Demonstrated**: Positive Conceivability (of water without H2O)
**Significance**: The example demonstrates that even positive conceivability — coherently imagining a detailed scenario — can fail to track metaphysical possibility when the subject is ignorant of essential natures. The conceivability is genuine in the sense that the scenario is internally coherent, but it is about the wrong thing: I am conceiving of a water-like substance, not water.
**Critical Distinction**: The gap arises because conceivability operates at the level of "modes of presentation" or "superficial descriptions," while metaphysical possibility concerns the objects themselves (rigidly designated). This is the fundamental challenge to all conceivability arguments.

### Link-by-Link Evaluation

| Link | Description | Rating | Key Issue |
|------|-------------|--------|-----------|
| L1 | Water without H2O is conceivable | Solid | Universally accepted; even opponents concede the conceivability |
| L2 | Water without H2O is impossible | Solid | Established by Kripke's semantics of rigid designation and actual-world discovery |
| L3 | Conceivability fails as guide to possibility | Solid | L1 and L2 jointly establish that positive conceivability + ignorance of essence = modal illusion |

### Gap Analysis (Applied to General Conceivability Arguments)

**The Kripkean Filter**: Any conceivability argument must pass the "Kripkean filter": is the target proposition like "water is not H2O" — a case where our concepts give us only contingent modes of presentation of an essence we do not fully grasp?

**Application to Mind-Body Arguments**:
- The zombie argument claims "consciousness is physical" is not like "water is H2O" — phenomenal concepts reveal essence directly.
- The phenomenal concept strategy claims the opposite: phenomenal concepts are like water-concepts, presenting consciousness under a mode of presentation that conceals its physical essence.
- The entire dialectic turns on whether phenomenal concepts are "transparent" (revealing essence) or "opaque" (presenting a mode of presentation).

**Bridgeability**: The Kripkean challenge is bridgeable only if the proponent can argue that the target concept reveals essence directly. For phenomenal concepts, this is the central contested claim.

### Modal Framework Assessment

- **Framework**: Kripkean possible-worlds semantics with rigid designation.
- **Key Innovation**: Distinction between epistemic possibility (what is conceivable given our knowledge) and metaphysical possibility (what is genuinely possible given the nature of things).
- **Framework Rating**: Explicit and consistent — the framework is precisely what the example demonstrates. Solid.

### Overall Strength Rating: Strong (as a Critique)

As a meta-level critique of conceivability arguments, this argument is Strong. The water/H2O case is a decisive counterexample to the claim that conceivability simpliciter entails possibility. The burden of proof is now on any conceivability argument to demonstrate that its target proposition is not a "water/H2O case" — that the relevant concepts reveal essence rather than merely presenting modes of presentation. This is precisely the burden the zombie argument takes on, and the debate over whether it discharges this burden is the central dispute in modal epistemology of mind.
```

---

## Example 4: Primary vs. Secondary Conceivability — The Two-Dimensional Distinction

### Input

> Consider the proposition "water is not H2O" again. In one sense, it is conceivable. In another sense, it is not. The distinction is between primary and secondary conceivability. Primary conceivability is conceivability under a description: if we consider "the actual watery stuff" rather than "water" rigidly, "the actual watery stuff is not H2O" is primarily conceivable — there are worlds where the watery stuff is XYZ. Secondary conceivability is conceivability with rigid designation held constant: "water is not H2O" is secondarily inconceivable because, holding "water" rigid to its actual-world referent (H2O), there is no coherent scenario where that stuff is not H2O. The key question for any conceivability argument is whether primary conceivability entails secondary possibility — and this depends on whether the relevant terms are semantically neutral (like "water") or not (like "consciousness," Chalmers argues).

### Output

```
## Conceivability Argument Analysis Report

### Basic Information
- **Argument ID**: CEX004
- **Argument Type**: Conceptual Distinction (Two-Dimensional Framework)
- **Logical Form**: Distinction between ◇C_primary(P) and ◇C_secondary(P); primary possibility entailment conditions
- **Source**: Chalmers, "Does Conceivability Entail Possibility?" (2002); Jackson, From Metaphysics to Ethics (1998)

### Chain Reconstruction

This is a conceptual framework for evaluating conceivability arguments, not an argument itself. The distinction enables more precise chain construction:

For any proposition P:
- L1_primary: Ideal primary positive conceivability of P → primary possibility of P. (Generally accepted within the framework.)
- L1_secondary: Primary possibility of P → secondary (metaphysical) possibility of P. (Contested; holds only when relevant terms are semantically neutral in the right way.)
- The key question: Are the terms in P semantically neutral (like "water") or not neutral (like "consciousness")?

### Conceivability Type Assessment

**Types Distinguished**:

| Conceivability Type | What It Tracks | Modal Correlate | Example |
|--------------------|----------------|-----------------|---------|
| Primary Conceivability | Conceivability under a description (epistemic) | Primary Possibility (conceptual) | "The watery stuff is not H2O" |
| Secondary Conceivability | Conceivability with rigid designation fixed | Secondary Possibility (metaphysical) | "Water is not H2O" (inconceivable) |
| Ideal Primary Conceivability | Primary conceivability under ideal rational reflection | Entails primary possibility | Chalmers's gold standard |

**The Bridge Problem**: The critical methodological point is that even ideal primary conceivability guarantees only primary possibility. Moving from primary possibility to secondary (metaphysical) possibility requires an additional argument about the semantic status of the terms involved.

**For Zombie Arguments**:
- Chalmers argues that phenomenal concepts are NOT semantically neutral — they pick out phenomenal properties directly, without a contingent mode of presentation. Therefore, primary conceivability of zombies entails primary possibility, which entails secondary possibility (because the terms are not neutral).
- Critics argue phenomenal concepts ARE semantically neutral in the relevant respect — they present consciousness under a contingent mode of presentation, like "water" does.

### Link-by-Link Evaluation (Framework Assessment)

| Link | Description | Rating | Key Issue |
|------|-------------|--------|-----------|
| Ideal Primary → Primary Possibility | Standard granted within the framework | Solid | Assumes ideal rationality is achievable |
| Primary → Secondary Possibility | Depends on semantic neutrality of terms | Contested | Central dispute for mind-body arguments |

### Modal Framework Assessment

- **Framework**: Two-dimensional semantics with primary/secondary intension distinction.
- **Logical System**: S5 assumed for primary modality; S5 for secondary modality is more controversial.
- **Key Innovation**: Separates epistemic and metaphysical modalities while providing conditions for their alignment.
- **Framework Rating**: Explicit and well-developed. The framework is the standard for sophisticated conceivability arguments.

### Overall Strength Rating: N/A (Framework Analysis)

This is a framework analysis, not an argument evaluation. The two-dimensional framework is the most sophisticated defense of conceivability-to-possibility inferences. Its strength as a tool is that it identifies precisely where the dispute lies: not at the level of "conceivability to possibility" generally, but at the specific question of whether primary possibility entails secondary possibility for the target domain. This transforms the debate from a crude "conceivability good / conceivability bad" into a nuanced discussion of the semantic properties of specific concepts.
```

---

## Example 5: Conceivability Chain Breakdown — When a Link Does Not Hold

### Input

> I can conceive of a world where time is circular rather than linear. In circular time, events loop back on themselves — what appears to be the future eventually becomes the past. I can describe this consistently: the event E that occurs "later" than E' is also "earlier" than E' when we trace the circle. Since I can conceive of circular time without contradiction, circular time must be metaphysically possible. And if circular time is possible, then the standard view of time as necessarily linear is false.

### Output

```
## Conceivability Argument Analysis Report

### Basic Information
- **Argument ID**: CEX005
- **Argument Type**: Conceivability Argument (about the metaphysics of time)
- **Logical Form**: ◇C(circular time) → ◇(circular time) → ¬□(linear time)
- **Source**: Hypothetical circular time conceivability argument

### Chain Reconstruction

L1: Circular time is conceivable (I can describe it consistently without contradiction).
L2: If circular time is conceivable, circular time is metaphysically possible.
L3: If circular time is metaphysically possible, then time is not necessarily linear.
L4: Therefore, time is not necessarily linear.

### Conceivability Type Assessment

**Claimed Type**: Negative Conceivability (cannot detect contradiction in circular time).
**Actual Type**: At best Negative Conceivability — the argument claims only that no contradiction has been detected, not that a full positive scenario has been constructed.
**Type Mismatch**: The argument claims a metaphysical possibility conclusion (L2) from negative conceivability evidence. Negative conceivability is the weakest type — inability to detect contradiction reflects our current conceptual resources, not the modal structure of reality. This is a classic type-mismatch problem.

### Link-by-Link Evaluation

| Link | Description | Rating | Key Issue |
|------|-------------|--------|-----------|
| L1 | Conceivability to Possibility | Broken | Negative conceivability insufficient for metaphysical possibility |
| L2 | Possibility to Conclusion | Adequate | Entailment valid, but moot given L1 failure |
| L3 | Overall Conclusion | Broken | Inherits L1 failure |

**L1 Detailed Evaluation**:
- The conceivability claim is merely negative: "I can describe it consistently." This does not provide positive evidence for possibility. Many impossible things are negatively conceivable — given finite rational capacities, I cannot exhaustively check for all hidden contradictions.
- Is the scenario fully specified? "Events loop back" is a schematic description, not a complete specification. What are the temporal relations? Does the B-theoretic description (earlier/later relations on a circle) capture all temporal phenomena, or does the A-theoretic passage of time resist circular modeling?
- The Kripkean Challenge: If time has a hidden essential nature (as some essentialists about time argue), the conceivability of circular time may be an illusion of ignorance — I conceive of a structure that satisfies some descriptions of time but fails to instantiate the essential nature of time.
- There is no two-dimensional defense, no engagement with the Kripkean challenge, and no positive scenario construction beyond a sketch.

**Factors Contributing to Breakdown**:
1. **Insufficient conceivability type**: Negative conceivability is too weak.
2. **Underdescribed scenario**: "Events loop back" is schematic, not fully specified.
3. **Unaddressed Kripkean challenge**: If time has an essential nature, the conceivability may be illusory.
4. **No modal epistemology**: The argument provides no theory of why conceivability would be a reliable guide in this domain.

### Gap Analysis

**Gap Severity Ranking**:
1. **L1 Gap (Severity: Fatal — Unbridgeable)**: The argument claims metaphysical possibility from negative conceivability. This inference is not merely unsupported — it is invalid. Negative conceivability establishes at most epistemic possibility (for all I know, circular time is possible). The gap is unbridgeable without fundamentally restructuring the argument to engage with modal epistemology.
2. **Completeness Gap (Severity: High)**: The scenario is underdescribed. Even if we upgrade to positive conceivability, the sketch would need substantial development.

**Cumulative Assessment**: The argument is Broken at L1. Even a charitable reconstruction cannot salvage the inference from negative conceivability to metaphysical possibility without adding substantial premises that the argument does not contain.

### Modal Framework Assessment

- **System**: Unspecified. The argument uses "possible" without specifying logical, conceptual, metaphysical, or physical modality.
- **Accessibility**: Implicitly universal — no accessibility relation specified.
- **Framework Rating**: Missing. The complete absence of a modal framework makes rigorous evaluation impossible. The argument needs to specify what kind of possibility is claimed.

### Overall Strength Rating: Broken

The argument fails at its first and most critical step. The inference from "I cannot detect a contradiction in circular time" to "circular time is metaphysically possible" is invalid without a defended modal epistemology. Negative conceivability supports only epistemic possibility — not metaphysical possibility. The Kripkean challenge is not addressed; the scenario is underdescribed; the modal framework is unspecified. The argument offers no resources for repair — it would need to be fundamentally restructured, replacing negative conceivability with at least positive conceivability, defending a modal epistemology, specifying the modal framework, and engaging the Kripkean challenge. As presented, it is not salvageable.
```
