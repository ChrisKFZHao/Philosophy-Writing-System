# Grounding Analysis Examples

> This document demonstrates the practical application of grounding/constitution analysis across different dependence relation types. Each example shows the complete input-to-output process.

---

## Example 1: Simple Grounding — Mental Supervenience on Physical (Kim)

### Input

> Mental properties strongly supervene on physical properties. For any mental property M, necessarily, if something has M, there exists a physical property P such that the thing has P, and necessarily, anything that has P has M. This supervenience relation captures the dependence of the mental on the physical: there can be no mental difference without a physical difference. The mental is therefore nothing over and above the physical — the physical facts determine all the mental facts.

### Output

```
## Grounding Relation Analysis Report

### Basic Information
- **Argument ID**: GEX001
- **Relation Types Detected**: Supervenience (claims grounding intent), Realization
- **Domain**: Philosophy of Mind
- **Source**: Hypothetical physicalist supervenience argument

### Relation Catalog

| ID | Ground | Grounded | Relation Type | Level Change | Confidence |
|----|--------|----------|---------------|--------------|------------|
| GR1 | Physical properties | Mental properties | Supervenience | Yes (physical→mental) | High |
| GR2 | Physical facts | Mental facts | Supervenience (author intends grounding) | Yes | High |

### Dependence Topology

[Fundamental Level (claimed)]
    Physical facts/properties (P1, P2, ..., Pn)
           |
           | (strong supervenience)
           v
[Derivative Level]
    Mental facts/properties (M1, M2, ..., Mn)

**Chain Structure**: Foundationalist (two-level)
**Well-Foundedness**: Fully well-founded within the argument's ontology

### Formal Properties Checklist

| Property | Expected | Result |
|----------|----------|--------|
| Irreflexivity | Physical does not supervene on itself as distinct mental | Pass |
| Asymmetry | Mental supervenes on physical, not vice versa | Pass |
| Transitivity | Not applicable (two-level only) | N/A |
| Hyperintensionality | Necessarily equivalent mental properties share supervenience base | Pass |

### Explanatory Adequacy Evaluation

**Critical Gap: Supervenience-to-Grounding Inference**: The author moves from "mental supervenes on physical" to "mental is nothing over and above the physical." This inference is invalid without additional premises. Supervenience is a modal covariance relation — it tells us that mental facts co-vary with physical facts, but not why. Grounding requires asymmetric explanation: the physical must explain the mental, not merely co-vary with it. The author needs a "because" argument — why does the physical explain the mental, not merely determine it modally?

**Modal Covariance Gap**: Strong supervenience as defined by Kim guarantees that within and across worlds, mental properties track physical properties. But this tracking relation is consistent with both physicalism (the physical explains the mental) and epiphenomenal dualism with necessary laws (the mental is distinct but necessarily co-occurs). Supervenience is too cheap to do the work the author wants it to do.

**Explanatory Power Score**: Adequate (supervenience correctly classified, but grounding claim not yet earned)

### Vulnerability and Recommendations

- **Primary Vulnerability**: The supervenience-to-grounding leap. A critic can accept the supervenience claim while rejecting the grounding claim (e.g., non-reductive physicalists accept supervenience but deny reduction/grounding; epiphenomenalists accept covariance but deny physical explanation).
- **Strengthening Recommendation**: Add a "because" argument: "Mental facts obtain in virtue of physical facts because [theory of realization/identity/functionalism]." Without this, the argument asserts covariance but claims explanation.
```

---

## Example 2: Constitutive Grounding — Wholes Grounded in Parts

### Input

> A table is nothing over and above its parts arranged table-wise. The existence and nature of the table are fully determined by the existence and arrangement of its constituent particles. There is no further "table-fact" beyond the facts about the particles and their organization. If you have listed all the facts about the particles — their positions, bonds, motions — you have listed everything there is to say about the table. The whole is grounded in its parts.

### Output

```
## Grounding Relation Analysis Report

### Basic Information
- **Argument ID**: GEX002
- **Relation Types Detected**: Grounding (full grounding, mereological)
- **Domain**: Metaphysics of Material Objects
- **Source**: Hypothetical mereological grounding argument

### Relation Catalog

| ID | Ground | Grounded | Relation Type | Level Change | Confidence |
|----|--------|----------|---------------|--------------|------------|
| GR1 | Particles arranged table-wise | The table (existence) | Full Grounding | Yes (micro→macro) | High |
| GR2 | Particles arranged table-wise | The table (properties) | Full Grounding | Yes | High |
| GR3 | Particle arrangement facts | All facts about the table | Full Grounding | Yes | High |

### Dependence Topology

[Fundamental Level]
    Particles and their arrangement (P1, P2, ..., Pn, arrangement R)
           |
           | (full grounding — "nothing over and above")
           v
[Level-1 Derivative]
    The table — existence, properties, facts

**Chain Structure**: Foundationalist (two-level, mereological)
**Well-Foundedness**: Fully well-founded

### Formal Properties Checklist

| Property | Expected | Result |
|----------|----------|--------|
| Irreflexivity | The table does not ground itself | Pass |
| Asymmetry | Particles ground table; table does not ground particles | Pass |
| Transitivity | Not applicable (two-level) | N/A |
| Hyperintensionality | Not applicable (no modal equivalents in play) | N/A |
| Non-monotonicity | Adding irrelevant particles preserves grounding | Pass |

### Explanatory Adequacy Evaluation

**The "In Virtue Of" Test**: The table exists in virtue of the particles being arranged table-wise. This is a paradigm case of mereological grounding. The grounding claim is explanatory: we understand why the table exists (because the particles are so arranged) and what its nature consists in (the arrangement). The explanation is complete — there is no residual "table-ness" left unexplained.

**Constitution vs. Identity Check**: The author claims grounding, not identity. This is important: the table is not identical to the particles (the particles can survive the table's destruction; the table can survive replacement of some particles). Grounding captures the dependence without asserting identity. This is the correct classification.

**Over-Determination Check**: The table has a single complete ground (the particles so arranged). No over-determination. The ground is not redundant — remove the particles and the table ceases to exist.

**Explanatory Power Score**: Excellent

### Vulnerability and Recommendations

- **Primary Vulnerability**: The argument assumes mereological nihilism is false — that there are composite objects at all. A nihilist would deny that the table exists, making grounding moot. The author should engage this challenge.
- **Secondary Issue**: "Arranged table-wise" is somewhat circular — it defines the table's ground partly in terms of the table. This may be acceptable if "table-wise" is independently characterizable (e.g., functionally), but the author should address circularity concerns.
- **Strengthening Recommendation**: Provide an independent characterization of "table-wise arrangement" — perhaps in terms of functional capacities — to avoid circularity.
```

---

## Example 3: Logical Grounding — Disjunctions Grounded in True Disjuncts

### Input

> The proposition "Socrates is wise or Socrates is foolish" is true. It is true in virtue of the fact that Socrates is wise — this one true disjunct fully grounds the truth of the disjunction. The disjunctive fact is not something over and above its true disjuncts. In general, every true disjunction is grounded in each of its true disjuncts. This is a paradigm of logical grounding: logically complex facts are grounded in the atomic facts that make them true.

### Output

```
## Grounding Relation Analysis Report

### Basic Information
- **Argument ID**: GEX003
- **Relation Types Detected**: Grounding (full grounding, logical grounding)
- **Domain**: Metaphysics of Logic / Logical Grounding
- **Source**: Hypothetical logical grounding argument

### Relation Catalog

| ID | Ground | Grounded | Relation Type | Level Change | Confidence |
|----|--------|----------|---------------|--------------|------------|
| GR1 | Socrates is wise | Socrates is wise or Socrates is foolish | Full Grounding (logical) | No (same level) | High |
| GR2 | Each true disjunct | The corresponding true disjunction | Full Grounding (general claim) | No | High |

### Dependence Topology

[Fundamental Level — Atomic Facts]
    Socrates is wise (atomic fact)
           |
           | (logical grounding)
           v
[Level-1 Derivative — Logically Complex Facts]
    Socrates is wise or Socrates is foolish (disjunctive fact)

**Chain Structure**: Foundationalist (two-level)
**Well-Foundedness**: Fully well-founded — atomic facts are bedrock within this ontology

### Formal Properties Checklist

| Property | Expected | Result |
|----------|----------|--------|
| Irreflexivity | Disjunction does not ground itself | Pass |
| Asymmetry | True disjunct grounds disjunction; disjunction does not ground true disjunct | Pass |
| Transitivity | Not applicable (two-level) | N/A |
| Hyperintensionality | Necessarily equivalent disjunctions may have different grounds | Not tested |
| Non-monotonicity | Adding irrelevant conjuncts to ground does not destroy grounding | Pass |

### Explanatory Adequacy Evaluation

**The "In Virtue Of" Test**: "In virtue of what is the disjunction 'P or Q' true?" Answer: "In virtue of P being true." This is maximally explanatory — the truth of the disjunction is wholly accounted for by the truth of a disjunct. No residual mystery.

**Vacuous Grounding Check**: Logical grounding is one of the least controversial forms of grounding precisely because the explanatory connection is transparent. The disjunction "contains" the grounded fact in a recognizable sense. No risk of vacuity.

**Over-Determination Check**: When BOTH P and Q are true, the disjunction "P or Q" has two full grounds (P and Q separately). This is a benign case of over-determination — each true disjunct is individually sufficient. The author acknowledges this implicitly but should note the over-determination explicitly.

**Relevance Check**: The ground (Socrates is wise) is clearly relevant to the grounded (the disjunction that includes it as a disjunct). The relevance is conceptual, not causal.

**Explanatory Power Score**: Excellent

### Vulnerability and Recommendations

- **Primary Vulnerability**: Minimal. Logical grounding of disjunctions in true disjuncts is widely accepted as a paradigm of grounding. The main challenge comes from identity theorists who might deny that logical complexity involves genuine grounding (the disjunctive fact just is the collection of true disjunct facts), but this is a debate about the relata, not the relation.
- **Secondary Issue**: The author generalizes to "every true disjunction is grounded in each of its true disjuncts." For infinite disjunctions or disjunctions involving vague predicates, this claim requires qualification.
- **Strengthening Recommendation**: Address the over-determination case explicitly — when multiple disjuncts are true, the disjunction has multiple distinct full grounds. This is benign but should be noted for completeness.
```

---

## Example 4: Multiple Determination — One Grounded Entity, Multiple Grounds

### Input

> The fact that this action is morally wrong may be grounded in several distinct features of the action: it causes unnecessary suffering; it violates a freely undertaken promise; it treats another person merely as a means. Each of these features, individually, would suffice to make the action wrong. But the action's wrongness is not over-determined in a problematic sense — each ground provides a complete explanation of why the action is wrong. The wrongness of this particular action is multiply realizable in the sense that different configurations of wrong-making features can ground it.

### Output

```
## Grounding Relation Analysis Report

### Basic Information
- **Argument ID**: GEX004
- **Relation Types Detected**: Full Grounding (multiple full grounds — over-determination)
- **Domain**: Metaethics (normative grounding)
- **Source**: Hypothetical moral grounding argument

### Relation Catalog

| ID | Ground | Grounded | Relation Type | Level Change | Confidence |
|----|--------|----------|---------------|--------------|------------|
| GR1 | Action causes unnecessary suffering | Action is morally wrong | Full Grounding | Yes (natural→normative) | High |
| GR2 | Action violates a freely undertaken promise | Action is morally wrong | Full Grounding | Yes | High |
| GR3 | Action treats person merely as a means | Action is morally wrong | Full Grounding | Yes | High |

### Dependence Topology

[Fundamental Level]
    Natural facts: suffering caused (F1), promise violated (F2), person used as means (F3)
      |              |              |
      | (grounds)    | (grounds)    | (grounds)
      v              v              v
[Level-1 Derivative]
    Normative fact: The action is morally wrong (N1)
    ─── Multiple Determination ───

**Chain Structure**: Foundationalist (two-level, convergent — multiple grounds converge on single grounded entity)
**Well-Foundedness**: Fully well-founded

### Formal Properties Checklist

| Property | Expected | Result |
|----------|----------|--------|
| Irreflexivity | Wrongness does not ground itself | Pass |
| Asymmetry | Natural facts ground wrongness; wrongness does not ground natural facts | Pass |
| Transitivity | Not applicable (two-level) | N/A |
| Non-monotonicity | Adding an irrelevant fact to a ground preserves grounding | Pass |

### Explanatory Adequacy Evaluation

**Multiple Grounds / Over-Determination Analysis**: This is a central case requiring careful handling. The action's wrongness has three distinct full grounds (GR1, GR2, GR3). Each is claimed to be individually sufficient. This constitutes metaphysical over-determination of the grounded fact.

The author argues this over-determination is benign: each ground provides a complete moral explanation of the wrongness. This is plausible if we accept that moral wrongness is a "multiply realizable" property — it can be grounded in different configurations of wrong-making features without redundancy.

However, multiple full grounds raise questions: if GR1 alone fully grounds the wrongness, what explanatory work do GR2 and GR3 do? Are they alternative grounds or partial grounds of an over-arching ground? The author needs to clarify the relationship between the multiple grounds — are they independent, complementary, or redundant?

**Relevance Check**: Each ground (suffering, promise-breaking, using-as-means) is clearly relevant to wrongness. No issue.

**Explanatory Power Score**: Good (grounds are relevant and individually explanatory, but over-determination requires further analysis)

### Vulnerability and Recommendations

- **Primary Vulnerability**: The over-determination structure. A critic might argue that if GR1 alone fully grounds the wrongness, GR2 and GR3 are superfluous — they do not add to the explanation. Alternatively: the wrongness is grounded in a disjunctive property (suffering OR promise-breaking OR using-as-means) rather than in each individually. The author should address which structure is intended.
- **Secondary Issue**: The natural-to-normative level change requires bridging the is-ought gap. The author assumes that natural facts can ground normative facts without providing a theory of normative grounding. This is a metaethical commitment, not a logical given.
- **Strengthening Recommendation**: Either (a) argue that the grounds are partial grounds jointly constituting a single full ground, or (b) defend the claim that multiple full grounds are metaphysically acceptable for normative properties specifically.
```

---

## Example 5: Grounding vs. Causation — A Systematic Distinction

### Input

> The window's being shattered depends on the rock's striking it. This dependence is causal — it involves a temporal sequence: first the rock strikes, then the window shatters. But there is also a metaphysical dependence: the fact that the window is shattered at time t is grounded in the fact that its constituent molecules are arranged shattered-wise at t. This grounding relation is synchronic — it holds at a time between the macro-state and micro-state, not across times. Both relations are "dependence" relations, but they are fundamentally different in kind: one is diachronic and causal, the other is synchronic and constitutive.

### Output

```
## Grounding Relation Analysis Report

### Basic Information
- **Argument ID**: GEX005
- **Relation Types Detected**: Causation and Grounding (distinguished explicitly)
- **Domain**: Metaphysics of Causation and Grounding
- **Source**: Hypothetical causation-grounding distinction argument

### Relation Catalog

| ID | Ground | Grounded | Relation Type | Level Change | Confidence |
|----|--------|----------|---------------|--------------|------------|
| GR1 | Rock striking window at t1 | Window shattering at t2 | Causation | No | High |
| GR2 | Molecules arranged shattered-wise at t | Window is shattered at t | Full Grounding | Yes (micro→macro) | High |

### Dependence Topology

Causal (diachronic):
    Rock strikes at t1 ──(causes)──> Window shatters at t2

Grounding (synchronic):
    Molecules arranged shattered-wise at t
           |
           | (grounds)
           v
    Window is shattered at t

**Chain Structure**: Foundationalist for grounding; causal chain is separate
**Well-Foundedness**: Grounding is fully well-founded; causation is not evaluated here

### Formal Properties Checklist

| Property | Expected (Grounding) | Expected (Causation) | Result |
|----------|---------------------|---------------------|--------|
| Irreflexivity | Yes | Yes | Both Pass |
| Asymmetry | Yes | Yes (controversial) | Both Pass (causation asymmetry is accepted here) |
| Transitivity | Yes (typically) | Often accepted | Grounding: Pass; Causation: not evaluated |
| Temporality | Synchronic (intra-temporal) | Diachronic (inter-temporal) | Correctly distinguished |

### Explanatory Adequacy Evaluation

**The Causation-Grounding Distinction**: This example is primarily analytical — the author is not making a grounding claim but rather distinguishing grounding from causation. The analysis evaluates the distinction the author draws.

**Criteria for the Distinction**:
1. **Temporality**: Causation is diachronic (cause before effect); grounding is synchronic (ground and grounded co-temporal). ✓ Correctly applied.
2. **Explanation Type**: Causation explains "why did X happen?" (event explanation); grounding explains "in virtue of what does X obtain?" (constitutive explanation). ✓ Correctly distinguished.
3. **Relata**: Causation relates events across time; grounding relates facts at a time. ✓ Correctly noted, though some philosophers (Schaffer) argue causation is a species of grounding.

**The Boundary**: The author correctly identifies the glass's shattered state as both (a) caused by the rock and (b) grounded in molecular arrangement at the time of shattering. These are compatible, not competing. The causal explanation answers "how did it come to be shattered?"; the grounding explanation answers "what does being shattered consist in?"

**Explanatory Power Score**: Excellent (distinction correctly drawn and defended)

### Vulnerability and Recommendations

- **Primary Vulnerability**: Some philosophers (Schaffer, Wilson) argue causation is a species of grounding, blurring the distinction. The author might engage this view.
- **Secondary Issue**: The "at a time" specification for grounding needs refinement — grounding relations may hold tenselessly or across times in some frameworks.
- **Strengthening Recommendation**: Add a discussion of whether causation and grounding can interact — e.g., does the causal fact (rock striking caused shattering) itself have a grounding structure? This cross-relation analysis would strengthen the taxonomy.
```

---

## Example 6: Supervenience Without Grounding — The Explanatory Gap

### Input

> Aesthetic properties supervene on physical properties: two paintings that are physically identical cannot differ in beauty. If painting A is beautiful and painting B is physically identical, B must also be beautiful. But this supervenience does not explain why A is beautiful — it merely asserts a modal co-variance constraint. To say that beauty supervenes on the physical is to say that the physical facts fix the aesthetic facts. But it does not tell us what makes something beautiful, or in virtue of what a particular painting is beautiful. Supervenience is a necessary condition for grounding but not sufficient.

### Output

```
## Grounding Relation Analysis Report

### Basic Information
- **Argument ID**: GEX006
- **Relation Types Detected**: Supervenience (explicitly distinguished from grounding)
- **Domain**: Aesthetics / Metaphysics
- **Source**: Hypothetical aesthetic supervenience argument

### Relation Catalog

| ID | Ground | Grounded | Relation Type | Level Change | Confidence |
|----|--------|----------|---------------|--------------|------------|
| GR1 | Physical properties of painting | Aesthetic properties (beauty) | Supervenience | Yes (physical→aesthetic) | High |

### Dependence Topology

[Fundamental Level]
    Physical properties of painting A (P1, P2, ..., Pn)
           |
           | (supervenience — modal co-variance, NOT grounding)
           v
[Derivative Level]
    Aesthetic properties: beauty, elegance, etc.
    ⚠ Gap: Supervenience established; grounding NOT established

**Chain Structure**: Foundationalist in form but incomplete in substance (supervenience without grounding)
**Well-Foundedness**: Partially well-founded — the modal covariance structure is mapped, but the explanatory structure is absent

### Formal Properties Checklist

| Property | Expected | Result |
|----------|----------|--------|
| Irreflexivity | Beauty does not supervene on itself as distinct physical | Pass |
| Asymmetry | Aesthetic supervenes on physical but not vice versa | Pass (stipulated) |
| Supervenience vs. Grounding | Supervenience is symmetric in failure conditions (no A-diff without B-diff ≡ no B-diff without A-diff); grounding is asymmetric | Explicitly noted |

### Explanatory Adequacy Evaluation

**The Supervenience-Only Case**: The author correctly identifies that supervenience falls short of grounding. The supervenience claim tells us that aesthetic facts are not "free-floating" — they are constrained by physical facts. But it does not answer the constitutive question: in virtue of what is this painting beautiful?

**The Explanatory Gap**: The gap is between modal co-variance (supervenience) and constitutive explanation (grounding). The author acknowledges this gap explicitly rather than conflating the two. This is methodologically correct — supervenience is presented as a constraint on aesthetic properties, not as an explanation of them.

**The "Because" Missing**: Without a theory of what makes things beautiful (e.g., formal properties, emotional responses, historical context), the supervenience claim is empty of explanatory content. It says "if you change the physical, you change the aesthetic" but does not say which physical changes produce which aesthetic changes.

**Explanatory Power Score**: Good (for diagnostic purposes — correctly identifies the supervenience/grounding gap)

### Vulnerability and Recommendations

- **Primary Issue**: The argument correctly diagnoses the gap but does not attempt to bridge it. This is acceptable if the purpose is diagnostic rather than constructive.
- **Secondary Issue**: Global supervenience (world-to-world) may be even weaker than claimed — two worlds with identical physical distributions could differ aesthetically if aesthetic properties are response-dependent or culturally constituted.
- **Strengthening Recommendation**: If the goal is to bridge from supervenience to grounding, the author needs a theory of aesthetic value that explains which physical properties ground which aesthetic properties. Without this, supervenience is merely a constraint on an unknown grounding relation.
```
