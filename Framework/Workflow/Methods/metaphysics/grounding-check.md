---
id: method.metaphysics.grounding-check
package: metaphysics
legacy_ids: [phil-grounding-check]
label: Grounding/Constitution Analysis
consumers: [phil-research/reconstruct, phil-write]
selector: feature-detected
side_effects: read-only
---

# Grounding/Constitution Analysis (method.metaphysics.grounding-check)

> Internal method module — not a registered runtime skill. Loaded on demand by the consuming skill's mode contract through the manifest resolver; never loaded wholesale.

# Grounding/Constitution Analysis

## Overview

This skill identifies and analyzes relations of metaphysical dependence — grounding, supervenience, realization, constitution — that structure an argument's ontological commitments. It maps the "dependence topology": which entities are fundamental and which are derivative, forming a directed structure. Beyond detection, it evaluates whether dependence claims satisfy formal constraints (irreflexivity, asymmetry, transitivity) and provide genuine metaphysical explanation rather than merely tracking modal covariance.

The core insight driving this skill is that not all "depends on" relations are equal. A supervenience relation merely tracks covariance across possible worlds — property A supervenes on property B if no change in A without a change in B. But supervenience is symmetric in its modal structure and says nothing about what explains what. Grounding, by contrast, is an asymmetric, explanatory relation: the mental is grounded in the physical not merely because they covary, but because physical facts explain mental facts. This skill draws those distinctions sharply and systematically, providing a rigorous typology that prevents the conflation of covariance with explanation — one of the most common errors in metaphysical argumentation.

The skill operates on the output of a prior argument-reconstruction, using that structured analysis to locate and classify every dependence claim in the target text. It then builds a topological map of what is fundamental and what is derivative, evaluates whether the dependence chain bottoms out appropriately (well-foundedness), and assesses whether the author's grounding claims genuinely explain rather than simply track covariation. The analysis is both diagnostic (identifying what the argument claims about dependence) and evaluative (assessing whether those claims succeed as metaphysical explanation).

This skill is especially valuable for arguments in philosophy of mind (where realization and supervenience claims are ubiquitous), metaethics (where moral facts are often claimed to supervene on or be grounded in natural facts), metaphysics of material objects (constitution vs. identity), and any argument that invokes levels of reality or fundamentality. The grounding turn in 21st-century analytic metaphysics — led by Kit Fine, Jonathan Schaffer, and others — has made dependence analysis a central methodological tool, and this skill operationalizes that methodology for systematic argument evaluation.

## Input

**Required:**
- `argument-reconstruction report` (from `method.argument.argument-reconstruct`): Provides the premises and conclusion in standard form, with inference patterns and logical structure identified. All dependence claims must be located within the argument's architecture to determine their dialectical role — whether grounding is asserted as a premise, derived as a conclusion, or presupposed as a background commitment. Without this structured input, there is no systematic basis for locating and classifying dependence claims.

**Optional:**
- `ontological-commitment report` (from `method.metaphysics.ontological-commitment`): The entity inventory enriches the analysis by cataloguing what the argument commits to existing. Knowing the ontological furniture enables a richer dependence topology: which of these entities are fundamental, and which are grounded in others? Without it, the dependence analysis builds its entity inventory from scratch using only entities explicitly mentioned in the argument text.
- `original text`: The source material. Grounding language is often subtle — "in virtue of," "nothing over and above," "consists in" — and may be more visible in the original prose than in the formalized reconstruction. Direct access to the original text also enables verification of quoted evidence.

## Output

**Grounding Relation Analysis Report** — structured per `grounding-relation-schema.json`, containing:

### Section 1: Relation Catalog

A comprehensive table of all dependence relations detected, each with:

| Field | Description |
|-------|-------------|
| `relation_id` | Unique identifier: GR1, GR2, ..., GRn |
| `ground` | The grounding entity, fact, or property (the more fundamental relatum) |
| `grounded` | The grounded entity, fact, or property (the derivative relatum) |
| `relation_type` | One of: `full_grounding`, `partial_grounding`, `supervenience`, `realization`, `constitution`, `identity`, `causation`, `other` |
| `direction` | `upward` (derivative depends on fundamental), `downward` (fundamental depends on derivative — unusual, flag), `lateral` (same level) |
| `level_change` | Whether the relation crosses ontological levels (e.g., mental-to-physical, social-to-psychological) |
| `formal_properties` | Assessment of irreflexivity, asymmetry, transitivity for this specific relation |
| `textual_evidence` | Quotation or precise reference to the source text |
| `classification_confidence` | High / Medium / Low |

### Section 2: Dependence Topology Map

A text-based directed graph showing the full dependence structure:
- **Fundamental level**: Entities/facts that are ungrounded within the argument's ontology — the ontological bedrock.
- **Derivative levels**: Stratified into layers (level-1 derivative directly grounded in fundamental; level-2 derivative grounded in level-1 derivative, etc.).
- **Chain structure**: Classification as foundationalist (chains terminate), infinitist (chains do not terminate), or coherentist (circular dependencies — problematic).
- **Well-foundedness assessment**: Whether every non-fundamental entity has a grounding chain that terminates in the fundamental. Fully well-founded, partially well-founded, not well-founded, or undetermined.
- **Text-based topology diagram**: ASCII-art visualization of the directed acyclic graph of dependence relations, with relation types distinguished (e.g., solid arrows for grounding, dashed for supervenience).

### Section 3: Explanatory Adequacy Evaluation

- **Genuine Explanation Check**: Does each grounding relation answer "in virtue of what does X obtain?" without circularity, infinite regress, or triviality?
- **Modal Covariance Gap**: Where supervenience is claimed, does the author recognize that supervenience alone does not constitute grounding? If not, flag this as a gap.
- **Fundamentality Assessment**: Is the claim of fundamentality non-trivial — does it pick out a genuine ontological distinction rather than merely re-labeling something as "fundamental" without explanatory work?
- **Over-Determination Check**: Are there cases where multiple distinct grounds are claimed for the same grounded entity? If so, is this over-determination handled or acknowledged?
- **Explanatory Power Score**: Summary rating — Excellent / Good / Adequate / Weak / Inadequate.

### Section 4: Formal Properties Checklist

A systematic checklist applied to each grounding-typed relation:

| Property | Expected | Verification Method | Result |
|----------|----------|---------------------|--------|
| Irreflexivity | Nothing grounds itself | Check if any entity appears as both ground and grounded in the same relation | Pass / Fail / Undetermined |
| Asymmetry | If A grounds B, B does not ground A | Scan for mutual grounding pairs or bidirectional chains | Pass / Fail / Undetermined |
| Transitivity | If A grounds B and B grounds C, A grounds C | Check all chains of length >= 2; verify transitivity holds or is explicitly denied | Pass / Fail / Denied by Author |
| Hyperintensionality | Necessarily equivalent grounds are not interchangeable | Check for cases where necessarily equivalent facts are treated as having identical grounding profiles | Pass / Fail / Not Applicable |
| Non-monotonicity | Adding conjuncts to ground may not preserve grounding | Check for cases where X grounds Y but X+Z is claimed not to ground Y | Pass / Flagged / Not Applicable |

For supervenience relations specifically, an additional check is applied: "Does the argument mistakenly treat supervenience as grounding?" Supervenience is reflexive, symmetric in its failure conditions, and does not entail explanation. Moving from "B supervenes on A" to "A grounds/explains B" without additional premises is a formal error that the checklist flags explicitly.

### Section 5: Vulnerability and Recommendations

- **Dependence Vulnerabilities**: Which dependence relations are most likely to be challenged by critics? Which rest on contested inferences (e.g., moving from supervenience to grounding without additional premises)? Which depend on controversial formal claims (e.g., denying transitivity)?
- **Alternative Topologies**: Are there alternative dependence structures that would better support the argument's conclusion? Could the argument be reformulated with a different fundamentality thesis?
- **Strengthening Recommendations**: If weak, can weak supervenience be upgraded to grounding by adding a "because" argument? Can implicit grounding be made explicit? Can circular dependencies be restructured?

## Methodological Foundations

This skill synthesizes the grounding literature that has reshaped analytic metaphysics since the early 2000s:

1. **Fine, Kit (2012). "Guide to Ground."** In *Metaphysical Grounding: Understanding the Structure of Reality*, edited by Fabrice Correia and Benjamin Schnieder. Cambridge University Press. — The canonical statement of grounding as a distinctive metaphysical relation with its own logic. Fine distinguishes the logic of ground from the logic of essence, establishing that grounding is a relation between facts with a distinctive grammatical form: "P because Q" where the "because" is metaphysical rather than causal. His framework provides the logical apparatus for formal property checks (irreflexivity, asymmetry, transitivity) and the "in virtue of" test for explanatory adequacy. Fine's distinction between strict and weak ground informs the classification of full vs. partial grounding.

2. **Schaffer, Jonathan (2009). "On What Grounds What."** In *Metametaphysics: New Essays on the Foundations of Ontology*, edited by David Chalmers, David Manley, and Ryan Wasserman. Oxford University Press. — Argues that grounding is the central notion of metaphysics, replacing Quinean existence questions with dependence questions. Schaffer's conception of grounding as metaphysical explanation and his defense of a sparse fundamental level inform the topology mapping and fundamentality assessment. His priority monism (the cosmos as the sole fundamental entity) is one pole of fundamentality; the report accommodates monist, pluralist, and nihilist answers.

3. **Kim, Jaegwon (1984). "Concepts of Supervenience."** *Philosophy and Phenomenological Research* 45(2): 153-176. — The classic taxonomy of supervenience varieties: weak, strong, and global supervenience. Kim's analysis of the formal structure of supervenience relations provides the criteria for distinguishing supervenience from grounding and for evaluating whether supervenience claims are explanatory or merely descriptive. His framework is essential for the critical classification step — preventing the conflation of supervenience (modal covariance) with grounding (metaphysical explanation).

4. **Wilson, Jessica (2014). "No Work for a Theory of Grounding."** *Inquiry* 57(5-6): 535-579. — A skeptical challenge to the grounding program, arguing that specific dependence relations (realization, constitution, set formation, etc.) do all the work and that "generic grounding" adds nothing. Wilson's dependence pluralism informs the skill's commitment to distinguishing grounding from supervenience, realization, and constitution rather than collapsing all into an undifferentiated "dependence" category. The relation typology is designed to be pluralist-sensitive.

5. **Bennett, Karen (2017).** *Making Things Up.* Oxford University Press. — A systematic treatment of "building relations" — grounding, composition, constitution, realization, causation — as a family of relations that share formal features (irreflexivity, asymmetry) while differing in their specific character. Bennett's framework provides the theoretical basis for treating these as distinct but related species of dependence and for the formal properties checklist that evaluates each relation type on its own terms.

6. **Rosen, Gideon (2010). "Metaphysical Dependence: Grounding and Reduction."** In *Modality: Metaphysics, Logic, and Epistemology*, edited by Bob Hale and Aviv Hoffmann. Oxford University Press. — Grounding as constitutive explanation, clarifying the relationship between grounding and reduction: reduction is one species of grounding (or grounding is what reduction aims at), but not all grounding is reductive. Rosen's work provides the framework for evaluating whether a dependence claim genuinely explains or merely redescribes.

7. **Bliss, Ricki and Kelly Trogdon (2021). "Metaphysical Grounding."** *Stanford Encyclopedia of Philosophy.* — The comprehensive survey of the grounding literature, providing the consensus framework: grounding is irreflexive, asymmetric, transitive (on most views), and hyperintensional. Serves as the reference point for the formal properties checklist and for situating anomalous cases (e.g., arguments that deny transitivity or embrace infinite descent) within the broader theoretical landscape.

8. **Dixon, T. Scott (2016). "What Is the Well-Foundedness of Grounding?"** *Mind* 125(498): 439-468. — Technical analysis of well-foundedness for grounding chains; informs the well-foundedness assessment in the topology mapping, particularly for distinguishing vicious from benign infinite descent.

9. **Dasgupta, Shamik (2014). "The Possibility of Physicalism."** *Journal of Philosophy* 111(9-10): 557-592. — Grounding formulation of physicalism as a key application area. The grounding analysis is particularly important for evaluating physicalism arguments, where the claim that "everything is grounded in the physical" is the central thesis.

10. **Leuenberger, Stephan (2014). "Grounding in Normative Ethics."** *Nous* 48(2): 227-251. — Application of grounding to normative domains, demonstrating how dependence analysis extends beyond pure metaphysics into ethics. Relevant for cross-domain applicability when the target argument involves normative grounding claims (e.g., moral facts grounded in natural facts, or normative reasons grounded in desires).

11. **Koslicki, Kathrin (2012). "Varieties of Ontological Dependence."** In *Metaphysical Grounding*. — Distinguishes between rigid and generic ontological dependence, and between existential and essential dependence. This finer-grained taxonomy informs the classification step when the argument's dependence claims are under-specified — the skill probes whether "depends on" means rigid dependence (the specific entity requires that specific ground) or generic dependence (the entity requires some ground of a certain type).

## Steps

### Step 1: Scan for Dependence Language

Search the reconstructed argument text for explicit dependence vocabulary. The following terms signal the presence of a dependence claim and should be noted with location and immediate context (2-3 sentences surrounding each hit):

**Core grounding vocabulary:**
- "grounds," "grounded in," "grounding relation"
- "in virtue of" (the canonical grounding phrase — Fine's litmus test)
- "because" used non-causally (metaphysical "because" vs. causal "because")
- "depends on," "dependent upon," "dependence relation"
- "nothing over and above" (the deflationary grounding claim)
- "consists in," "consists of nothing but"
- "reduces to," "reducible to"
- "obtains solely in virtue of"

**Supervenience vocabulary:**
- "supervenes on," "supervenience base," "supervenient"
- "covaries with," "no difference without a difference in"
- "fixes," "determines" (when modal rather than causal)

**Realization vocabulary:**
- "realized by," "realization," "realizer," "multiply realizable"
- "implemented by," "physical realization of"

**Constitution vocabulary:**
- "constituted by," "constitution relation," "constitutively"
- "made of," "composed of" (when non-mereological metaphysical constitution)

**Other dependence vocabulary:**
- "fundamental," "derivative," "ontologically prior," "more fundamental than"
- "emerges from" (when not causal emergence — flag for ambiguity)
- "obtains in virtue of the nature of"

For each hit, record the surrounding text, the entities related, and a preliminary type guess. Apply the causality test: if the relation involves temporal succession or counterfactual dependence across time, it is causal — route to `method.metaphysics.causation-analyze`. If it involves synchronic metaphysical explanation, it is grounding. If no dependence language is found at all, the analysis terminates at this step with a note that the argument does not invoke metaphysical dependence.

### Step 2: Classify Each Relation

For each dependence relation detected in Step 1, determine its precise type and document the evidence:

**Full Grounding:** X fully grounds Y. Y is wholly explained by X — there is nothing about Y left unexplained by X. The canonical test: "Y obtains in virtue of X" without needing to add anything else. Example: The fact that the rose is scarlet fully grounds the fact that the rose is red.

**Partial Grounding:** X is part of what grounds Y. Multiple grounds jointly fully ground Y, and X is one of them. The canonical test: "Y obtains partly in virtue of X." Example: The fact that Mary believes p and the fact that p is true together partially ground the fact that Mary knows p.

**Supervenience:** X supervenes on Y if there can be no change in X without a change in Y. This is a modal covariance relation, not necessarily explanatory. Sub-classify: weak supervenience (within a world), strong supervenience (across worlds), global supervenience (world-to-world). **Critical:** Supervenience claims are often mistaken for grounding claims. The author who claims "A supervenes on B" has made a modal claim; they have not yet made a grounding claim unless they additionally argue that B explains A. Flag this gap explicitly.

**Realization:** A functional or higher-level property is realized by a lower-level property that plays the specified causal/functional role. Standard in philosophy of mind: mental properties are realized by physical properties. Realization typically involves multiple realizability — the same higher-level property can be realized by different lower-level properties. Distinguish realization from grounding: realization is a specific dependence type; whether it counts as grounding depends on broader theoretical commitments.

**Constitution:** Material constitution without identity. The statue is constituted by the lump of clay, but the statue and the lump have different modal profiles (the statue would not survive squashing; the lump would). Constitution is a dependence relation without identity. Flag cases where constitution might be mistaken for identity or vice versa.

**Identity:** X is identical with Y. This is NOT a dependence relation — identity is symmetric and reflexive. If the author treats identity as grounding (e.g., "X is grounded in Y because X just is Y"), this is a category error. Flag such cases.

**Causation:** X causes Y. Diachronic and temporal, not synchronic metaphysical dependence. Flag causal claims being used where grounding claims are needed. Note: some philosophers (Schaffer) argue causation is a species of grounding; if the text explicitly adopts this view, note it but classify separately.

**Other:** Any dependence relation not fitting the above types. Document and describe.

For each classification, record: (a) textual evidence for the type, (b) alternatives considered and why rejected, (c) confidence level: High / Medium / Low.

### Step 3: Map Dependence Topology

Build the directed graph of dependence relations and analyze its structure:

**Identify fundamental entities:** Those that appear as "ground" but never as "grounded" in any detected relation. These are ungrounded within the argument's ontology — the ontological bedrock. Note: "fundamental within the argument" does not mean "absolutely fundamental in reality" — an argument may treat physical objects as fundamental even if a deeper metaphysics would ground them further.

**Identify derivative entities:** All entities that appear as "grounded." Stratify into levels:
- Level-1 derivative: grounded directly in fundamental entities.
- Level-2 derivative: grounded in level-1 derivative entities, with no shorter chain to the fundamental.
- Continue for deeper levels as needed.

**Classify chain structure:**
- **Foundationalist:** All chains terminate in fundamental entities. The most common and typically preferred structure. Well-founded in the strict sense.
- **Infinitist:** Chains do not terminate — every ground is itself grounded, ad infinitum. Does the author acknowledge this? Some metaphysical infinitists defend it as coherent.
- **Coherentist:** Cycles in the dependence graph (A grounds B, B grounds A, or longer cycles). Generally considered problematic because grounding is asymmetric. Flag as formal violation.
- **Mixed:** Different domains exhibit different structures (e.g., physical domain foundationalist, normative domain infinitist). Note domain-specific structure.

**Well-foundedness assessment:** Evaluate whether every dependence chain terminates in ungrounded entities:
- Fully well-founded: every chain terminates.
- Partially well-founded: some chains terminate, others do not.
- Not well-founded: no chains terminate, or cycles present.
- Undetermined: insufficient information in the text.

**Construct text-based topology diagram** using ASCII art. Distinguish relation types visually (e.g., solid lines for grounding, dashed for supervenience, dotted for realization). Example:
```
[Fundamental Level]
    Physical facts (P1, P2, ...)
           |
           | (grounds)
           v
[Level 1 — Biological]
    Biological facts (B1, B2, ...)
           |
           | (realizes)
           v
[Level 2 — Mental]
    Mental facts (M1, M2, ...)
```

### Step 4: Check Formal Properties

Evaluate the formal properties standardly attributed to grounding:

**Irreflexivity:** Nothing grounds itself. For every entity X, X is not grounded in X. Scan for self-grounding claims (e.g., "X grounds itself" or where ground and grounded are indistinguishable). Violations: flag if any entity appears as both ground and grounded in the same relation.

**Asymmetry:** If A grounds B, then B does not ground A. Scan for mutual grounding (A grounds B and B grounds A). This is a serious violation — asymmetric structure is definitional for grounding. Violations: flag and note whether the author might be using a non-standard conception.

**Transitivity:** If A grounds B and B grounds C, then A grounds C. Typically accepted but contested (Schaffer questions full transitivity for partial grounding). Check: does the dependence chain respect transitivity? For each chain A to B to C: (a) is A to C explicitly claimed? (b) If not, is it implied? (c) If A to C is explicitly denied, note this as a non-standard position.

**Non-monotonicity:** Grounding is generally non-monotonic — adding more ground does not necessarily preserve the grounding relation. Check for cases where X grounds Y but X+Z is said not to ground Y, or vice versa.

**Hyperintensionality:** Grounding is hyperintensional — necessarily equivalent propositions need not have the same grounds. Check for cases where the author treats necessary equivalents as having the same grounds (the "intensional fallacy" about grounding). For example, [P] and [P and (Q or not-Q)] are necessarily equivalent, but they may differ in what they ground.

**Supervenience-specific checks:**
- Does the argument move from supervenience to grounding? "B supervenes on A, therefore A grounds/explains B" — this inference is invalid without additional premises. Flag the gap.
- Does the argument move from supervenience to reduction or identity? Similarly requires additional premises.

For each property, produce a checklist: property, whether satisfied, whether explicitly assumed by the author, and any violations or anomalies.

### Step 5: Evaluate Explanatory Adequacy

Go beyond formal properties to assess whether the grounding claims genuinely explain:

**The "In Virtue Of" Test:** For each grounding claim, ask whether it plausibly answers "In virtue of what does the grounded entity or fact obtain?" A genuine grounding explanation should make the grounded fact intelligible in terms of the ground — not merely correlate with it. If the ground seems insufficient or irrelevant, the explanation is inadequate.

**The Modal Covariance Gap (Supervenience vs. Grounding):** Where supervenience claims are made: (a) Does the author recognize that supervenience is a purely modal relation? (b) Does the author attempt to bridge from supervenience to grounding, and if so, is the bridge plausible? (c) If the author treats supervenience as sufficient for grounding, flag this as an error. Supervenience is cheap — almost everything supervenes on itself. Grounding requires asymmetry and explanation.

**Vacuous Grounding Check:** If the ground is a necessary truth and the grounded is also necessary, then (on some accounts) anything grounds anything — this trivializes grounding. If the argument's grounding relations all involve necessary truths, flag the risk of vacuity.

**Fundamentality Non-Triviality:** Is the claim that certain entities are "fundamental" doing genuine explanatory work? Check: (a) Are there specific criteria for fundamentality? (b) Do fundamental entities play an explanatory role, or are they merely labeled "fundamental" as a placeholder? (c) Is the fundamentality claim consistent with the rest of the ontology?

**Over-Determination Check:** Count how many distinct full grounds are claimed for each grounded entity. Multiple full grounds constitute metaphysical over-determination. If detected: (a) Is it acknowledged? (b) Is there a principled reason to accept it? (c) Does it weaken explanatory force?

**Relevance Check:** Is the ground relevant to the grounded? "The fact that 2+2=4 grounds the fact that grass is green" — if the argument contains such apparently irrelevant grounding claims, flag them.

**Circularity Check:** Do any grounding chains loop? If A grounds B, B grounds C, and C (directly or indirectly) grounds A, this is circular and fails as explanation. Even wide circles (long chains) are problematic.

**Regress Check:** Do grounding chains extend infinitely downward without terminating? If so: (a) Does the author embrace metaphysical infinitism? (b) If not, is the regress vicious (undermining explanation) or benign (merely a consequence of open-ended ontology)?

**Explanatory Power Score:** Synthesize into a summary rating:
- **Excellent:** Grounding claims are precise, non-circular, well-founded, genuinely explanatory, and avoid conflating grounding with supervenience.
- **Good:** Minor issues (e.g., one supervenience conflation, one unacknowledged over-determination case) but overall robust.
- **Adequate:** Some relations are explanatory; others are merely asserted or confused with modal covariance.
- **Weak:** Most relations are under-described; grounding claims are largely gestural.
- **Inadequate:** Grounding claims are confused (e.g., symmetric grounding), circular, or entirely missing explanatory force.

### Step 6: Compile Report

Synthesize all findings into the final Grounding Relation Analysis Report:

1. **Header**: Title, target argument identifier, date of analysis, skill version.
2. **Executive Summary**: One paragraph overview — how many relations detected, what types, overall topology, key strengths and weaknesses.
3. **Relation Catalog**: Full table from Step 2, organized by type or by level in the dependence hierarchy.
4. **Dependence Topology Map**: From Step 3, including the text-based diagram, chain structure classification, and well-foundedness verdict.
5. **Formal Properties Checklist**: From Step 4, presented as a table.
6. **Explanatory Adequacy Evaluation**: From Step 5, with the Explanatory Power Score prominently displayed.
7. **Critical Observations**: The 2-4 most important issues for the author or reviewer to address — gaps, conflations, or formal violations.
8. **Vulnerability Analysis**: Which dependence relations are most likely to be challenged? Which rest on contested inferences (e.g., supervenience to grounding)? Are there alternative dependence structures that would better support the argument?
9. **Recommendations**: If the dependence structure is weak, can it be strengthened? Can weak supervenience be upgraded to grounding by adding a "because" argument?

Ensure the report is ready for consumption by downstream skills (e.g., `method.metaethics.moral-supervenience` for metaethics arguments) and by the ARS system.

## Quality Criteria

1. **Relation Precision with Justification:** Every dependence relation classified has explicit textual evidence and a justification for why it is classified as grounding, supervenience, realization, constitution, or other. The skill does not collapse distinct relations into an undifferentiated "dependence" category. Each classification is defended with reference to the definitions in Step 2.

2. **Topology Completeness:** The full dependence structure is mapped. All relata are accounted for. The chain structure (fundamental, derivative, intermediate) is explicit. The text-based diagram correctly represents the directed edges. Gaps in the topology (entities whose dependence status cannot be determined from the text) are explicitly noted.

3. **Formal Correctness:** Formal property violations (irreflexivity failures, asymmetry failures, unexplained transitivity denials) are flagged and explained. The formal checklist is complete — no property is omitted. The skill does not assume all published arguments respect the formal properties of grounding; it is diagnostic, not normalizing.

4. **Explanatory Assessment (Not Just Covariance):** The analysis goes beyond merely cataloguing dependence claims to evaluate whether they succeed as metaphysical explanations. The supervenience/grounding distinction is applied rigorously. The "in virtue of" test is applied to every grounding claim. Vacuous grounding is flagged.

5. **Pluralism Awareness:** The analysis respects the diversity of dependence relations. It does not collapse realization, constitution, supervenience, and causation into "grounding" without argument. Where the author uses a generic "depends on," the analysis probes which specific dependence relation is at work.

6. **Textual Grounding:** All classifications are anchored in specific textual evidence (quotations or precise references). The analysis does not attribute dependence claims to the author that are not present in the text.

7. **Dialectical Fairness:** When the author's dependence claims are ambiguous or incomplete, the analysis presents the most charitable interpretation before critiquing. The goal is to reconstruct the dependence structure as the author intended it, then evaluate it.

8. **Diagram Clarity:** The text-based topology diagram is visually parseable, correctly represents the directed structure, and distinguishes relation types (e.g., solid arrows for grounding, dashed for supervenience, dotted for realization).

9. **Cause/Metaphysical Distinction:** The distinction between causal dependence (temporal, diachronic, counterfactual) and metaphysical dependence (synchronic, explanatory, constitutive) is rigorously maintained. Causal dependence claims are flagged and routed, not confused with grounding.

## Relations to Other Skills

### Dependencies (Required Inputs)
- **`method.argument.argument-reconstruct`** (strong dependency): The grounding analysis requires a prior reconstruction of the argument's structure — premises, conclusions, and inferences. Without this, there is no systematic basis for locating and classifying dependence claims. The argument reconstruction provides the skeleton onto which the dependence topology is mapped. The reconstruction's logical form is essential for distinguishing different types of dependence — e.g., supervenience claims have a characteristic modal structure, grounding claims have a characteristic explanatory structure.
- **`method.metaphysics.ontological-commitment`** (weak dependency, optional but recommended): An ontological commitment report enriches the analysis by supplying an inventory of entities before dependence relations are examined. Without it, the dependence topology must build its entity inventory from scratch, which is more error-prone.

### References (Read-Only Knowledge Resources)
- **`glossary-metaphysics.md`**: Definitions of key terms (grounding, supervenience, realization, constitution, fundamentality, well-foundedness, etc.). Consult for terminological precision and to ensure definitions are applied consistently with the broader skill ecosystem.
- **`ontological-categories.md`**: The category system (substance, property, fact, event, etc.) that structures the ontological inventory. Useful for determining whether dependence relations cross category boundaries and for ensuring the relata are categorized correctly.
- **`modal-logic-primer.md`**: Reference for modal logic needed to analyze supervenience claims (S4, S5, accessibility relations). Relevant when evaluating the formal structure of supervenience and distinguishing weak/strong/global varieties.

### Dependents (Skills That Use This Output)
- **`method.metaethics.moral-supervenience`** (cross-domain dependent): When the argument involves moral facts and natural facts, the grounding analysis feeds into the moral supervenience analysis, which evaluates the specific claim that moral properties supervene on natural properties. The grounding typology (especially the supervenience/grounding distinction) is directly applied.
- **`phil-reduction-analyze`**: Reduction claims often involve grounding — if X reduces to Y, does Y ground X? The grounding analysis provides the dependence structure that the reduction analysis needs to evaluate whether reduction claims are genuinely reductive.
- **`method.metaphysics.essence-detect`**: Essentialist claims (what it is to be X) often interact with grounding claims (the essence of X grounds certain necessary truths about X). The grounding analysis informs essence detection by clarifying which truths are grounded in essence and which are merely necessary.

### Coordination Notes
- When run after `method.argument.argument-reconstruct`, use the reconstructed argument's numbering scheme for consistent cross-referencing throughout the report.
- When run before `method.metaethics.moral-supervenience`, flag all supervenience relations (especially global supervenience) for downstream analysis in the moral domain.
- If the argument involves both grounding and causation, coordinate with `method.metaphysics.causation-analyze` to ensure the metaphysical/causal distinction is drawn consistently across both analyses.

## Boundary Conditions

### When to Skip
- **No dependence language detected:** If Step 1 finds no grounding, supervenience, realization, constitution, or other dependence vocabulary, the analysis terminates with a brief report noting the absence of metaphysical dependence claims. Do not invent dependence where none is claimed. Note that absence of dependence claims is itself a metaphysically interesting feature — the argument is ontologically "flat" without a fundamentality hierarchy.
- **Pure causal claims:** If all "depends on" claims are clearly causal (temporal, diachronic, cause-effect), route to `method.metaphysics.causation-analyze` rather than performing a grounding analysis. Summarize the causal claims for reference but do not analyze them as grounding.
- **Purely formal or logical argument:** If the argument is purely logical (e.g., a proof in propositional logic) with no mention of entities, properties, or dependence, there is nothing to analyze. Terminate.

### When to Adjust Scope
- **Implicit grounding** (no explicit dependence language, but structure implies it): If the argument's conclusion is that "X must exist because Y exists" without explicit "grounds" language, flag as implicit grounding. Perform a limited analysis — note the implicit claim but do not classify with the same confidence as explicit claims. Mark confidence as "Low." State what is claimed to ground what, provide textual evidence for the attribution, and assess whether the argument's proponent would accept or reject the attribution.
- **Metaphysical neutrality:** If the author explicitly disavows metaphysical dependence claims (e.g., "I make no claims about grounding; this is purely an epistemic argument"), respect this. Note the disavowal but also note any structural features that look like dependence claims. The analysis becomes a "potential grounding structure" rather than an actual grounding claim analysis. Acknowledge this as a legitimate methodological choice rather than a deficiency.
- **Historical text (pre-2000):** Earlier literature may use "supervenience" broadly to cover what we now call "grounding." Adjust classification to reflect historical usage while noting the anachronism. Do not penalize the author for not having access to the contemporary grounding literature, but note the distinction for modern readers.

### Domain-Specific Guidance
- **Philosophy of Mind:** Expect realization and supervenience claims. The realization relation is central — be precise about multiple realizability and whether the author treats realization as grounding or as a separate dependence type. Physicalism arguments often turn on whether realization is a kind of grounding.
- **Metaethics:** Expect supervenience of the normative on the natural. Check whether the author treats moral supervenience as grounding or merely as modal covariance. The grounding of particular moral facts in natural facts is a key locus of analysis.
- **Metaphysics of Material Objects:** Expect constitution claims and identity/dependence confusion. The statue/lump distinction is the canonical case — check whether the author conflates constitution with identity.
- **Social Ontology:** Expect constitution claims (social facts constituted by psychological and physical facts). The grounding of institutional facts in collective intentionality is a common structure (Searle).

### Edge Cases
- **"Zero-grounding":** Some facts may be said to be grounded in nothing (they are "zero-grounded"). This is a special case of fundamentality — the fact exists but has no ground, not even itself. Treat as a fundamental fact with a special annotation.
- **Grounding of grounding facts:** If the argument addresses "what grounds the grounding relation itself?", note as a meta-grounding claim and flag for conceptual analysis beyond the scope of this skill.
- **Cross-world grounding:** If grounding claims span possible worlds (A in world w1 grounds B in world w2), flag as unusual and note that standard grounding is intra-world.
- **Tense and grounding:** If grounding claims are tensed ("X grounded Y at time t but not at time t'"), flag the temporal dimension as potentially conflating metaphysical dependence with causation.

## ARS Interface

### Role in ARS
This skill provides the **metaphysical architecture** for the methodology section of an ARS (Academic Review System) analysis. When ARS evaluates whether an argument's dependence claims are coherent and explanatory, it draws on the grounding analysis produced by this skill. The dependence structure report informs ARS's assessment of the argument's ontological foundations.

### Information Provided to ARS
1. **Dependence Structure Summary:** A concise statement of what is fundamental and what is derivative, which ARS can use to assess whether the argument's conclusions are consistent with its own ontological commitments.
2. **Critical Gaps:** Identification of where the author conflates supervenience with grounding, makes circular dependence claims, or fails to provide genuine explanation — these become ARS critique points.
3. **Formal Violations:** Any violations of irreflexivity, asymmetry, or other formal properties flagged as high-priority issues for ARS review.
4. **Explanatory Power Score:** A summary metric that ARS can use in its overall assessment of the argument's strength.

### How ARS Uses This Output
- **Methodology Section:** The dependence topology and chain structure become part of the methodological architecture that ARS reports.
- **Critique Generation:** Violations, gaps, and conflations identified become specific critique items in the ARS review.
- **Comparative Assessment:** When ARS compares multiple arguments (e.g., in a literature review), dependence structures can be compared — e.g., "Argument A is foundationalist and well-founded; Argument B is silent on well-foundedness, raising questions about ontological completeness."
- **Interdisciplinary Flagging:** ARS may flag arguments where dependence claims cross disciplinary boundaries for specialized review.
- **Revision Coaching:** The vulnerability analysis directly informs revision recommendations — showing the author exactly which dependence claims need strengthening or clarification.

### Information Received from ARS (Feedback Loop)
- **Contextual Adjustments:** If ARS provides context about the target journal, audience, or debate, the grounding analysis may adjust its explanatory standards. A metaphysics journal (e.g., *Nous*, *Mind*) demands more rigorous grounding analysis with explicit formal property checks; a general philosophy journal may accept looser dependence language.
- **Domain Expertise:** ARS may supply domain-specific dependence schemas (e.g., the standard grounding structure for the moral realism debate, or the canonical dependence topology for the physicalism literature) that this skill can use as comparison benchmarks.
- **Revision Targeting:** If ARS identifies that the author's grounding claims are a key weakness, this skill can be re-run with tighter criteria to provide more detailed critique for revision. For example, if ARS flags that the author conflates supervenience with grounding in the methodology section, the re-run focuses specifically on detecting and documenting that conflation.
