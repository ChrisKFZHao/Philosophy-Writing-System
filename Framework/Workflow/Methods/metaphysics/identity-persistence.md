---
id: method.metaphysics.identity-persistence
package: metaphysics
legacy_ids: [phil-identity-persistence]
label: Identity and Persistence Analysis
consumers: [phil-research/reconstruct, phil-write]
selector: feature-detected
side_effects: read-only
---

# Identity and Persistence Analysis (method.metaphysics.identity-persistence)

> Internal method module — not a registered runtime skill. Loaded on demand by the consuming skill's mode contract through the manifest resolver; never loaded wholesale.

# Identity and Persistence Analysis

## Overview

When an argument makes or presupposes claims about identity over time ("this is the same ship that sailed into harbor") or across possible worlds ("if this table had been made of different wood, would it be the same table?"), this skill analyzes the identity conditions, evaluates whether the persistence framework (endurance, perdurance, or exdurantism) affects the argument's validity, and detects classic identity problems that may undermine the argument's conclusion.

Identity is not a univocal concept. Numerical identity (being one and the same thing) must be distinguished from qualitative similarity (being exactly alike), constitution (the statue is constituted by the clay but is not identical to it), and genidentity (the identity of a process through time). Furthermore, identity claims are always made under a sortal — "same ship," "same person," "same lump of clay" — and the sortal determines the persistence conditions.

This skill applies Leibniz's Law systematically: if A is identical to B, then A and B share all properties. In modal contexts, the modal variant applies: if A is necessarily identical to B, then any property A has necessarily, B has necessarily. The skill diagnoses the modal structure of identity statements — whether they are necessary (Kripke's thesis that identity is necessary if true), a posteriori necessary (identity claims discovered empirically), or contingent and thus suspect.

The central methodological move is a framework diagnosis. Different theories of persistence provide different semantics for cross-time and cross-world identity, and an argument may implicitly depend on one framework. By making this dependence explicit, the skill assesses whether the argument would survive a switch to a rival framework — a crucial dialectical metric.

## Input

**Required:**
- `argument-reconstruction report` (from `method.argument.argument-reconstruct`): Provides the argument in standard form, from which identity claims and persistence claims are extracted. The reconstruction's logical form is essential for identifying `=` relations and for determining whether identity is predicated of objects, events, or other ontological categories.

**Optional:**
- `modal-argument analysis report` (from `method.metaphysics.modal-arg`): Essential for arguments involving possibility and necessity. The modal report provides the modal framework (S4, S5, accessibility relations, De dicto/De re distinctions) needed to analyze cross-world identity. Without this report, cross-world identity analysis is incomplete.
- `original text`: The source material. Identity problems are often more visible in narrative examples (Theseus's ship, fission cases) than in formalized reconstructions. The original text may contain the concrete scenario that motivates the identity analysis.

## Output

**Identity/Persistence Analysis Report** — structured as follows:

### Section 1: Identity Claims Inventory

A list of all identity claims detected in the argument, each with:
- `claim_id`: Unique identifier (ID1, ID2, ...)
- `statement`: The identity statement as it appears in the argument (or as reconstructed)
- `logical_form`: Formal representation (`a = b`, `a at t1 = a at t2`, `a in w1 = a in w2`)
- `sortal`: The sortal under which identity is claimed (if explicit or inferable)
- `location`: Where in the argument the claim appears (premise number, conclusion)
- `role`: How the identity claim functions in the argument (premise, intermediate conclusion, final conclusion, presupposition)

### Section 2: Persistence Framework Diagnosis

A determination of which theory of persistence the argument presupposes, whether explicitly or implicitly:

- **Endurantism (3D-ism):** Objects are wholly present at each moment they exist. Persistence through time is strict numerical identity: the object at t1 is literally the same object at t2. Identity criteria are synchronic (what makes this object the same object as itself right now) and diachronic (what makes the object at t1 the same as the object at t2). Problems: temporary intrinsics (how can the same object be both bent and straight?), coincidence (statue and clay — two objects in the same place at the same time).

- **Perdurantism (4D-ism, worm theory):** Objects are space-time worms — they have temporal parts at each moment, just as they have spatial parts at each region. Persistence is not identity but rather the having of distinct temporal parts at different times. The object at t1 is a temporal part of the same worm as the object at t2. Problems: modal properties of temporal parts, the "thinking parts" problem.

A perdurantist variant holds that persons are maximally continuous person-stages connected by psychological continuity relations.

- **Exdurantism (stage theory):** Only momentary stages (instantaneous temporal slices) exist. What we call "persistence" is actually a series of counterpart relations between stages at different times. The object at t1 is not identical to the object at t2; instead, the t2-stage is a temporal counterpart of the t1-stage.

The diagnosis includes:
- Textual evidence for the framework attribution
- Whether the argument explicitly adopts a framework or whether it is implicit
- Whether the framework matters to the argument's validity

### Section 3: Cross-World Identity Analysis

For arguments involving modality (possibility, necessity, counterfactuals), analyze how identity is tracked across possible worlds:

| Framework | Claim | Key Proponent |
|-----------|-------|---------------|
| Transworld identity | A single individual exists in multiple possible worlds. Identity across worlds is strict numerical identity. | Kripke (1980), Plantinga |
| Counterpart theory | No individual exists in more than one possible world. Instead, individuals in other worlds are counterparts — similar in contextually specified respects. No strict transworld identity. | Lewis (1968, 1986) |
| Haecceitism | Individuals have thisnesses (haecceities) — non-qualitative essences that ground transworld identity. | Plantinga, Adams |

The analysis covers:
- Which framework the argument presupposes (or whether both are compatible)
- Whether counterpart relations reduce modal commitment to de dicto (avoiding de re modality)
- Whether the argument requires rigid designation (Kripke) or can function with counterpart relations
- The modal strength of identity claims: necessary identity (true in all worlds where the objects exist), contingent identity (claimed identity that is false in some possible world — highly suspect post-Kripke)

### Section 4: Identity Problem Detection

A systematic check for classic identity problems that may affect the argument:

| Problem | Description | Diagnostic Question |
|---------|-------------|---------------------|
| Fission | One object becomes two (e.g., an amoeba divides, brain hemispheres are transplanted to two bodies). Which, if either, is identical to the original? | Does the argument assume uniqueness of successor? If so, fission scenarios challenge this. |
| Fusion | Two objects become one (e.g., two rivers merge). Which, if either, is the resulting object identical to? | Does the argument assume a unique predecessor? If so, fusion scenarios challenge this. |
| Theseus's Ship | Gradual replacement of all parts over time. Is the ship at the end identical to the ship at the start? | Does the argument rely on a criterion of identity over time (spatiotemporal continuity, functional continuity, same-matter) that the Theseus scenario challenges? |
| Vague Identity | Can it be indeterminate whether A = B? Evans's argument: if it is indeterminate whether A = B, then B has the property "being such that it is indeterminate whether A = it," but A lacks this property (it is determinate that A = A). By Leibniz's Law, A ≠ B — so indeterminate identity collapses into determinate non-identity. | Does the argument involve borderline cases where identity seems indeterminate? If so, Evans's argument may apply. |
| Contingent Identity | Claims of the form "A = B, but it is possible that A ≠ B." Post-Kripke, this is widely rejected: true identity is necessary (by the necessity of identity: if □(x)(x = x), and a = b, then any property of a is a property of b, including the property □(x = a), so □(a = b)). | Does the argument claim or presuppose that an identity statement could be contingent? If so, this violates the necessity of identity. |
| Coincidence / Constitution | A statue is made of a lump of clay. Are they identical (one object) or distinct (two objects coinciding)? If distinct, how can two material objects occupy the same place at the same time? | Does the argument involve materially coinciding objects? If so, does it assume they are identical or distinct? |
| Arbitrary Undetached Parts | Does the argument presuppose that for any object and any subregion it occupies, there is an object that exactly occupies that subregion (the doctrine of arbitrary undetached parts)? | Does the argument implicitly invoke AUP? If so, this is a substantive and contestable commitment. |

For each problem detected, the report describes:
- How the problem manifests in the argument
- Whether the problem is fatal to the argument or merely creates a dialectical burden
- What responses are available (e.g., "only one survives" thesis, non-branching psychological continuity, four-dimensionalism dissolves the ship problem)

### Section 5: Framework Sensitivity Assessment

The critical question: **would switching persistence frameworks affect the argument's validity or soundness?**

- **Framework-independent arguments**: If the argument's validity does not depend on any particular persistence framework, note this as a strength. The argument works regardless of whether one is an endurantist or perdurantist.
- **Framework-dependent arguments**: If the argument presupposes endurantism and would fail under perdurantism (or vice versa), note this as a dialectical vulnerability. An opponent who rejects the presupposed framework can reject the argument without engaging its substance.
- **Framework-ambiguous arguments**: If the argument employs concepts that are ambiguous between frameworks, note the ambiguity and assess whether disambiguation affects the argument.

**Sensitivity Matrix** — a compact table showing for each identity claim how it would be interpreted under each persistence framework and whether the interpretation would affect the argument's validity.

## Methodological Foundations

This skill is grounded in seven canonical sources spanning the metaphysics of identity, modality, and persistence:

1. **Leibniz's Law (the Indiscernibility of Identicals)** — The foundational principle: if a = b, then for any property P, P(a) iff P(b). Equivalently: there is no property that a has and b lacks. The modal variant: necessarily, if a = b, then for any property P, □P(a) iff □P(b). This principle is the primary tool for testing identity claims in Steps 1 and 4. Violations of Leibniz's Law indicate either a failure of identity or an intensional context.

2. **Kripke (1980) "Naming and Necessity"** — The thesis of rigid designation (proper names designate the same object in all possible worlds) and the necessity of identity. Kripke's argument that true identity statements, if true, are necessarily true, even when discovered a posteriori. This constrains Step 3 (cross-world identity analysis) and Step 4 (contingent identity detection).

3. **Lewis (1986) "On the Plurality of Worlds"** — Counterpart theory as an alternative to transworld identity. Modal properties are analyzed via counterparts: "I could have been a plumber" means I have a counterpart in some possible world who is a plumber. This framework is essential for Step 3 (cross-world identity analysis) and Step 5 (framework sensitivity), especially when the argument's modal claims are more naturally expressed in counterpart-theoretic terms.

4. **Parfit (1984) "Reasons and Persons"** — The fission argument against the importance of identity. Parfit argues that what matters in survival is not numerical identity but psychological continuity and connectedness, which can obtain in branching (fission) cases where identity cannot. This is central to Step 4 (fission problem detection) and to the framework sensitivity assessment when personal identity is at issue.

5. **Sider (2001) "Four-Dimensionalism"** — The argument from vagueness for perdurantism. If composition is unrestricted but it is vague when composition occurs, then there must be temporal parts to avoid vague existence. Sider's framework provides the canonical defense of four-dimensionalism and is essential for understanding the perdurantist framework in Step 2.

6. **van Inwagen (1990) "Material Beings"** — The Special Composition Question (SCQ): under what conditions do some things compose something? Van Inwagen's answer (nihilism: only simples and living organisms exist) is one extreme; universalism (any things compose something) is the other. The SCQ is the backdrop against which constitution puzzles (statue/clay) and Theseus problems are assessed in Step 4.

7. **Wiggins (2001) "Sameness and Substance Renewed"** — Sortal essentialism: identity is always identity under a sortal concept. The sortal provides the persistence conditions. "Same F" is the canonical form of an identity claim, and different sortals may deliver different verdicts about whether an object persists through a change. This is the guiding principle for Step 1's sortal extraction.

## Steps

### Step 1: Identify Identity Claims

Extract all identity statements from the argument's premises and conclusion.

**What to extract:**
- Explicit identity claims using "is identical to," "is the same as," "=," "one and the same"
- Implicit identity claims: definite descriptions in anaphoric chains ("John entered the room. He sat down." presupposes that the "he" is identical to John)
- Persistence claims: "this is the same ship as the one that sailed yesterday"
- Constitution claims: "the statue is made of clay" — is this an identity claim? Or is constitution distinct from identity? Flag the ambiguity.
- Counting claims: "there are exactly three Fs" presupposes identity conditions for Fs

**For each identity claim, determine:**
1. The logical form: `a = b`, `a at t1 = a at t2`, `∃x(x = a)`, or modal: `a in w1 = a in w2`, `∃w(a in w = b in w)`
2. The terms: are they proper names, definite descriptions, indexicals, variables?
3. The sortal: under what sortal is identity claimed? If no sortal is explicit, what is the most natural sortal given context? For example, "this is the same [lump of clay]" vs "this is the same [statue]" yield different identity verdicts in the statue/clay case.
4. The argument role: premise, intermediate conclusion, final conclusion, suppressed premise, or presupposition?

**Distinguish numerical identity from weaker relations:**
- Numerical identity: a = b (one and the same thing)
- Qualitative identity (exact similarity): a and b share all intrinsic properties but are distinct
- Constitution: the clay constitutes the statue (distinct but coincident)
- Composition: the planks compose the ship (distinct but the ship is not identical to any one plank)
- Genidentity: identity of a process (this continuous erosion event = that erosion event)
- Psychological continuity: the later person is psychologically continuous with the earlier person (Parfit: this is what matters, not identity)

### Step 2: Diagnose Persistence Framework

Determine which theory of persistence the argument presupposes.

**Diagnostic questions:**

1. Does the argument treat objects as having temporal extent (existing through time as a whole from a tenseless perspective) or as existing wholly at each moment?

2. Does the argument treat "object at t1" and "object at t2" as the very same entity (endurantism) or as distinct temporal parts of a four-dimensional worm (perdurantism) or as distinct stages linked by counterpart relations (exdurantism)?

3. Does the argument encounter the problem of temporary intrinsics? If an object is A at t1 and ~A at t2, is the object the same object having incompatible properties (problematic for endurantism), or are different temporal parts having different properties (unproblematic for perdurantism)?

4. Does the argument involve coincident objects (statue and clay, person and body)? If so, does it treat them as one or two? Endurantism struggles with coincidence (two material objects in the same place); perdurantism handles it via temporal parts (the statue-worm and clay-worm share some temporal parts but diverge).

5. Does the argument use tensed or tenseless language about persistence?

**Framework classification:**
- `endurantism` (classic 3D-ism)
- `perdurantism` (4D-ism, worm theory)
- `exdurantism` (stage theory)
- `neutral`: The argument does not presuppose any particular framework.
- `ambiguous`: The argument uses language compatible with multiple frameworks.
- `mixed`: The argument uses different frameworks for different kinds of entities.

Provide textual evidence for the classification, citing specific passages or logical features.

### Step 3: Analyze Cross-World Identity

For arguments involving possibility, necessity, counterfactuals, or modal operators of any kind, analyze how identity is tracked across possible worlds.

**Analysis dimensions:**

1. **Does the argument involve de re modality about individuals?**
   - "John necessarily has his parents" — this requires tracking John across possible worlds.
   - "Necessarily, the winner of the race is the winner of the race" — this is de dicto and does not require cross-world identity.

2. **Which framework does the argument presuppose?**
   - **Transworld identity** (Kripke): Same individual exists in multiple worlds. Requires rigid designation — the name "Aristotle" refers to the same individual in every world where it refers. Modal properties are properties of the individual simpliciter.
   - **Counterpart theory** (Lewis): No individual exists in more than one world. Modal properties are analyzed via counterparts. "Aristotle could have been a playwright" means: Aristotle has a counterpart (in some world) who is a playwright, where counterpart relations are determined by similarity in contextually specified respects.
   - **Alternative frameworks**: Haecceitism (individual essences ground transworld identity), combinatiorialism (worlds are maximal combinations of simple elements).

3. **Modal strength of the identity claim:**
   - **Necessary identity**: If a = b, then necessarily a = b (in all worlds where a and b exist). Standard post-Kripke.
   - **Contingent identity**: Claim that a = b in the actual world but a ≠ b in some possible world. Highly suspect — flag as a likely error.
   - **Necessarily distinct**: If a ≠ b, then necessarily a ≠ b (in all worlds where a and b exist). The converse of necessary identity.

4. **Quantified modal logic required**: Is S5 needed (□◇P scenarios, accessibility is universal)? Or does the argument work in S4 or weaker systems?

### Step 4: Detect Identity Problems

Systematically check for identity problems that could affect the argument.

**Fission/fusion:**
- Does the argument assume that if X at t1 is the same F as Y at t2 and as Z at t2, then Y = Z? (This is the transitivity of identity conjoined with uniqueness of successor.)
- In fission, one object gives rise to two. Which is the original? The argument may assume uniqueness of successor or the "only X survives" thesis — both are substantive and can be challenged.

**Theseus's ship:**
- Does the argument rely on a criterion of identity over time that the Theseus scenario challenges?
- Is the criterion material (same parts), formal (same structure/function), spatiotemporal (continuous trajectory), or historical (causal continuity)?
- Does the argument need to answer the Theseus problem, or is it orthogonal?

**Vague identity:**
- Does the argument involve borderline cases of identity?
- If so, does Evans's argument apply, forcing the conclusion that there is no vagueness in the world (only semantic vagueness)?

**Contingent identity:**
- Does the argument claim or presuppose that two things are identical but could have been distinct?
- If so, does this violate the necessity of identity? Is there a defense (e.g., Gibbard's contingent identity of Lumpl and Goliath)?

**Constitution coincidence:**
- Does the argument distinguish constitution from identity?
- Statue = Lumpl? Or Statue ≠ Lumpl but they coincide materially?
- What are the persistence conditions for constituted objects?

### Step 5: Assess Framework Sensitivity

Evaluate whether switching persistence frameworks or cross-world identity frameworks would affect the argument.

**Method:** For each identity claim in the argument, ask:
1. Would an endurantist interpret this claim differently from a perdurantist?
2. If differently, does the difference affect the truth-value of the claim?
3. If the truth-value changes, does this affect the validity of the overall argument?

**Sensitivity classification:**
- `robust`: The argument is valid and sound under all major persistence frameworks. Its identity claims are framework-neutral or can be translated without loss.
- `sensitive_but_defensible`: The argument works under one framework but would require modification under another. The modifications are feasible and preserve the argument's force.
- `framework_dependent`: The argument's validity or soundness depends on adopting a specific persistence framework. An opponent who rejects that framework can dismiss the argument. This is a significant dialectical vulnerability.

### Step 6: Compile Report

Synthesize into the structured Identity/Persistence Analysis Report:

1. **Identity Claims Inventory** (table)
2. **Persistence Framework Diagnosis** (narrative with evidence)
3. **Cross-World Identity Analysis** (if applicable)
4. **Problem Detection Summary** (list of problems found, severity, responses)
5. **Framework Sensitivity Assessment** (with sensitivity matrix)
6. **Overall Assessment**: A summary statement about how identity and persistence considerations affect the argument's strength.

## Quality Criteria

1. **Leibniz's Law Precision**: The indiscernibility of identicals is correctly applied, including in modal and intensional contexts. The report does not mistakenly apply Leibniz's Law across intensional operators (where it can fail) without noting the intensional context. The modal variant is correctly distinguished from the non-modal.

2. **Framework Transparency**: The persistence framework is explicitly diagnosed with textual evidence from the argument. If the framework is ambiguous, the ambiguity is acknowledged and both interpretations are explored. The diagnosis does not overattribute — "the argument uses a word associated with endurantism" is not sufficient for "the argument presupposes endurantism."

3. **Problem Detection Sensitivity**: All identity puzzles relevant to the argument are identified. False positives (detecting problems that do not actually arise) are avoided. The severity of each problem is assessed relative to the argument's structure — a problem that is tangential to the argument's main line should be noted but not treated as fatal.

4. **Framework Neutrality**: The report does not advocate for a persistence framework. It diagnoses what the argument presupposes and assesses the consequences of framework choice, but it does not argue that endurantism is correct and perdurantism wrong, or vice versa. The report's voice is analytical, not partisan.

5. **Sortal Awareness**: Identity is always analyzed as identity under a sortal (following Wiggins). The report explicitly identifies the relevant sortal for each identity claim. When the sortal is ambiguous or underdescribed, this is noted as a potential source of confusion.

## Relations to Other Skills

**Depends on:**
- `method.argument.argument-reconstruct`: Provides the argument in standard form, from which identity claims are extracted and logical form is derived. The reconstruction's handling of identity predicates (=) and temporal/modal operators is essential for all subsequent analysis.
- `method.metaphysics.modal-arg`: Provides the modal framework analysis (S4/S5 determination, De dicto/De re distinctions, accessibility relations) required for Step 3 (cross-world identity analysis). Without this, the modal dimension of identity cannot be reliably assessed.

**References (read-only):**
- `modal-logic-primer.md`: Technical reference for modal operators, accessibility relations, and quantified modal logic systems (S4, S5) relevant to cross-world identity analysis.
- `metaphysical-distinctions.md`: Taxonomies of persistence theories, identity conditions, and constitution puzzles used throughout the skill.

**Dependents (skills that use this skill's output):**
- None direct at the P1 level. At later stages, identity analysis informs:
  - `method.metaphysics.essence-detect`: Essence constrains identity conditions — what is essential to an entity determines what changes it can survive and what makes it the entity it is. The identity/persistence report provides the identity framework within which essentialist claims are evaluated.

**Complements:**
- `method.metaphysics.grounding-check`: If an entity is grounded in or supervenes on another, this may affect identity claims involving those entities. Conversely, identity claims may structure dependence relations.

## Boundary Conditions

### 1. No Identity Claims

If the argument contains no identity statements and makes no persistence claims:

> "No identity claims detected; persistence analysis not applicable."

Explain: the argument is purely qualitative (all terms are general), or it makes no claims about what survives what changes, or it is purely synchronic. Note that this is relatively rare in substantive philosophical arguments — most arguments invoke persisting objects at some level.

### 2. Purely Extensional Argument

If the argument uses no modal operators, no counterfactuals, and makes no cross-time claims:

> "This argument is purely extensional and synchronic. Cross-world and cross-time identity analyses are not applicable. The following identity claims (if any) are purely extensional and do not require persistence framework analysis."

Skip Step 3 (cross-world identity) and note the limitation. Step 2 (persistence framework) may still apply if identity over time is implicit.

### 3. Personal Identity

If the argument concerns personal identity rather than object identity in general, the analysis must be adapted to include the specific frameworks developed for personal identity:

- **Psychological continuity theory** (Parfit, Shoemaker): What matters is psychological connectedness and continuity, which can be one-many (fission). Personal identity in the strict numerical sense is not what matters.
- **Biological continuity theory** (Olson, animalism): Personal identity is biological continuity of the human organism. The person is the animal.
- **Narrative theory** (Schechtman): Personal identity is constituted by self-narrative and practical concerns.
- **Simple view** (Chisholm, Swinburne): Personal identity is primitive and unanalyzable; persons are simple substances (Cartesian egos or souls).

The report should note which framework the argument presupposes and whether rival frameworks challenge it.

### 4. Trivial Identities

Logical truths of the form `a = a` or `∀x(x = x)`:

> "The argument contains trivial identity claims (reflexivity of identity: a = a). These are logical truths that carry no substantive ontological weight. They are noted for completeness but not analyzed at length."

Do not waste analysis on tautological identities. Focus on substantive identity claims where the identity is informative or contested.

## ARS Interface

**Academic Paper Integration:** The identity/persistence analysis report provides the metaphysical architecture section for `ars academic-paper` when the paper engages with personal identity, material constitution, or modal identity debates. The report can be translated into a methodology section discussing the persistence framework adopted (or assumed) and the relevant identity problems that the paper's argument must navigate.

**Reviewer Integration:** When used with `ars academic-paper-reviewer`, the framework sensitivity assessment is especially valuable: if the paper's argument depends on a specific persistence framework without acknowledging it, the reviewer can flag this as a methodological gap. The reviewer can recommend that the paper either defend its framework choice or show that its argument is framework-independent.

**Cross-Domain Utility:** Identity/persistence analysis is relevant beyond pure metaphysics. The same structures appear in philosophy of mind (personal identity), ethics (the identity of persons across time as a precondition for desert and responsibility), and philosophy of science (the identity of scientific entities across theory change, the persistence of species and ecosystems).
