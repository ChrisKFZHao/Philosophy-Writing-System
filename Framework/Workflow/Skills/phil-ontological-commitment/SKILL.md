---
name: phil-ontological-commitment
description: "Ontological Commitment Detection — identify entity types and existence categories presupposed by arguments using Quinean criterion and category taxonomy"
---

# Ontological Commitment Detection

## Overview

This skill detects what an argument commits its proponent to believe exists — the entities, properties, facts, and categories that must be in the world for the argument to be true. It answers the question: "If someone sincerely asserts this argument, what must they be willing to admit into their ontology?"

The core method combines two pillars of analytic ontology. First, Quine's criterion of ontological commitment: "to be is to be the value of a bound variable." An argument commits its proponent to the existence of whatever must be admitted as the value of a variable for the argument's quantified statements to be true. Second, a systematic ontological category taxonomy that classifies each commitment into its proper place within the furniture of the world — concrete particulars, abstract objects, properties, facts, events, and so on.

Beyond mere detection, this skill reconstructs the argument's implicit ontology — the full picture of what the world must contain if the argument is sound — and provides a structured assessment of that ontology's parsimony and controversiality. It distinguishes explicit commitments (stated in premises) from implicit ones (required as truthmakers, presuppositions, or best explanations), and for each controversial commitment it explores whether paraphrastic strategies (fictionalism, instrumentalism, paraphrase nominalism) could allow the proponent to avoid the commitment while preserving the argument's force.

This skill is foundational within the metaphysics pipeline: before evaluating whether an argument's dependence relations hold (phil-grounding-check) or whether its identity claims are coherent (phil-identity-persistence), one must first understand what the argument claims exists at all.

## Input

**Required:**
- `argument-reconstruction report` (from `phil-argument-reconstruct`): Provides the argument in standard form with premises and conclusion, including quantified structure and logical form. This is the primary input against which ontological commitments are detected.

**Optional:**
- `original text`: The source material from which the argument was extracted. Useful for detecting implicit commitments that do not appear in the reconstruction's standard form but are presupposed in the surrounding discourse.
- `premise-audit report` (from `phil-premise-detect`): Hidden premises often contain the most significant ontological commitments. The premise audit identifies enthymematic premises that may introduce entities not mentioned in the explicit argument.

## Output

**Ontological Commitment Report** — structured per `ontological-commitment-schema.json`, containing the following sections:

### Section 1: Detected Commitments List

A numbered list (OC1, OC2, ..., OCn) with each entry containing:

| Field | Description |
|-------|-------------|
| `commitment_id` | Unique identifier: OC1, OC2, ..., OCn |
| `entity_type` | The kind of thing committed to (e.g., "electrons," "moral properties," "possible worlds," "propositions") |
| `ontological_category` | Classification from the ontological category taxonomy (see Methodological Foundations) |
| `explicitness_level` | One of: `explicit`, `quantificational`, `presuppositional`, `truthmaker-based`, `implicit` |
| `quinean_test_application` | How Quine's criterion is applied: the quantified statement, the bound variable, and the required domain value |
| `controversiality_rating` | One of: `uncontroversial`, `moderately_controversial`, `highly_controversial`, `radical` — assessed within the relevant philosophical context |
| `alternative_paraphrase` | Whether a paraphrastic strategy (fictionalism, instrumentalism, paraphrase nominalism) could avoid this commitment, and at what cost to the argument's plausibility |
| `rejection_impact` | What happens to the argument if this commitment is rejected: `fatal` (argument collapses), `significant_weakening`, `minor_adjustment`, or `independent` (argument survives intact) |

### Section 2: Ontological Profile

A summary-level analysis including:

- **Overall Quinean Ontology Summary**: A synthetic statement of the argument's total ontological commitments, organized by category (e.g., "This argument commits its proponent to: concrete physical particulars (electrons, tables), abstract objects (sets, numbers), and property instances (tropes), but remains neutral on possible worlds.")
- **Most Contentious Commitment**: The single commitment most likely to provoke ontological dissent, with justification for why it is contentious and which philosophical positions would reject it.
- **Parsimony Assessment**: Both quantitative (how many distinct ontological categories are invoked, how many entity types) and qualitative (whether the commitments are qualitatively luxuriant — e.g., possibilia, universals, abstracta — vs qualitatively sparse). Includes comparison to known ontological positions (nominalism, realism, actualism, possibilism).
- **Category Breakdown Counts**: A table showing how many commitments fall into each ontological category (concrete_particular: 3, abstract_object: 2, property: 1, etc.).

## Methodological Foundations

This skill is grounded in six canonical sources in analytic ontology:

1. **Quine (1948) "On What There Is"** — The criterion of ontological commitment via bound variables. Quine argues that we are ontologically committed to whatever must be among the values of our bound variables for our assertions to be true. The slogan "to be is to be the value of a variable" is the operational core of this skill. Importantly, Quine distinguishes the question of what a theory says exists (its ontological commitments) from the question of what actually exists (ontology proper).

2. **van Inwagen (2014) "Metaphysics"** — The five fundamental questions of ontology: (i) What is the relation between particulars and properties? (ii) What is the relation between the mental and the physical? (iii) What are the ultimate constituents of material objects? (iv) Are there non-physical things? (v) Are there necessary beings? These questions structure the investigation and guide the controversiality assessment.

3. **Hirsch (2011) "Quantifier Variance and Realism"** — The thesis that different ontological frameworks may use different quantifier meanings, such that what "exists" according to one framework differs from what "exists" according to another, without either being wrong. This is essential for assessing whether a detected commitment is a genuine ontological commitment or merely an artifact of the quantifier chosen. Hirsch's deflationism provides the theoretical basis for the "alternative paraphrase possibility" assessment.

4. **Schaffer (2009) "On What Grounds What"** — The distinction between a permissive ontology (many things exist, including arbitrary mereological sums) and an austere ontology (fewer things exist, only those that are fundamental). Schaffer's distinction between existence questions and fundamentality questions informs the ontological profile: an argument may have a permissive ontology of existence but a sparse ontology of fundamentality.

5. **Lewis (1983) "New Work for a Theory of Universals"** — The distinction between sparse natural properties (those that "carve nature at the joints") and abundant properties (any set of possibilia). This informs whether property commitments are genuinely ontologically committing or merely logically trivial.

6. **Carnap (1950) "Empiricism, Semantics, and Ontology"** — The distinction between internal questions (questions about the existence of entities within a linguistic framework, answerable by empirical or logical methods) and external questions (questions about the existence of the framework itself, which are pragmatic rather than factual). This distinction is crucial for assessing whether an ontological commitment is a substantive metaphysical claim or a pragmatic choice of framework.

## Steps

### Step 1: Extract Quantified Statements

Identify all existential quantifier patterns and universal quantifier patterns in the reconstructed argument's premises and conclusion.

**Existential patterns to detect:**
- Formal: `∃x`, `∃x∃y`, `∃x∀y`
- Natural language: "there is," "there exists," "some," "at least one," "a certain," "something"
- Implicit existential import: definite descriptions in subject position often carry existential commitment
- Predicative commitment: "a is F" may commit to the existence of the property F-ness

**Universal patterns to detect:**
- Formal: `∀x`, `∀x∃y`
- Natural language: "all," "every," "any," "each," "whatever"

**Important nuance:** Universal quantification alone does not carry existential commitment (on standard modern logic). "All unicorns are white" does not commit one to the existence of unicorns. However, universal quantification combined with existential quantification may carry derivative commitments.

For each quantified statement, extract:
- The statement in its original form
- Its logical form (first-order or higher-order)
- The domain of quantification (explicit or implicit)
- The binding structure (which variables are bound, which are free)

Record predicate commitments separately: does the argument invoke predicates that, if taken as referring to properties or universals, would generate additional commitments?

### Step 2: Apply Quinean Test

For each quantified statement identified in Step 1, apply Quine's criterion systematically:

1. **Identify the quantified statement** in logical form.
2. **Determine the domain of quantification**: What kind of things must the variables range over? Is the domain unrestricted (everything that exists) or restricted (e.g., physical objects, mathematical entities, events)?
3. **Determine the truth conditions**: Under what assignment of values to bound variables is the statement true?
4. **Extract the commitment**: The entities that must be in the domain to satisfy the truth conditions are the ontological commitments of that statement.

**Binding structure record:** For each commitment, document:
- Which quantified statement generates it
- The quantifier type (existential, universal with existential import)
- The variable(s) bound
- The required value(s) in the domain

**Special cases:**
- **Higher-order quantification:** If the argument quantifies over predicates (second-order or higher), apply the Quinean test at the appropriate order. A commitment to properties, for instance, may arise from second-order quantification.
- **Substitutional quantification:** If the quantifier is interpreted substitutionally rather than objectually, it may carry no ontological commitment. Flag this interpretive ambiguity.
- **Plural quantification:** Plural quantifiers ("there are some things such that...") may commit to pluralities without committing to sets. Handle with care.

### Step 3: Classify by Category

Map each detected commitment to the ontological category taxonomy from `ontological-categories.md`. The standard taxonomy includes:

| Category | Description | Examples |
|----------|-------------|----------|
| `concrete_particular` | Spatiotemporally located individual objects | Tables, electrons, persons, planets |
| `abstract_object` | Non-spatiotemporal objects | Numbers, sets, propositions, universals (Platonic) |
| `property` | Ways things are — properties, qualities, attributes | Mass, charge, redness, being-wise |
| `fact` | Truthmakers — states of affairs that make propositions true | The fact that snow is white, the obtaining of a state of affairs |
| `event` | Dated, located occurrences | The explosion, the lecture, the sunrise |
| `process` | Extended, continuous occurrences without clear boundaries | Erosion, evolution, thinking |
| `possible_world` | Maximal ways things could have been | Lewisian concrete worlds, Stalnakerian abstract worlds |
| `set` | Collections defined by their members | The set of prime numbers, the empty set |
| `kind` | Natural kinds or substantial sortals | Tiger, water, gold, electron |
| `trope` | Particularized properties — property instances | The redness of this apple, Socrates' wisdom |
| `universal` | Repeatable entities wholly present in multiple locations | Immanent universals (Aristotelian), transcendent universals (Platonic) |
| `proposition` | Abstract bearers of truth-values | The proposition that 2+2=4 |
| `truthmaker` | That in virtue of which a truth-bearer is true | Facts, tropes, objects |
| `other` | Entities not fitting the above categories | Specify and justify |

For each classification, provide a brief justification: why this category rather than alternative categories? For example, if an argument commits to "the property of being conscious," justify whether this should be classified as `property` (universal), `trope` (particularized), or `abstract_object` (Platonic form).

**Category overlap resolution:** Some entities may fit multiple categories. For example, a "state of affairs" might be classified as `fact` or `event`. In such cases, explain the ambiguity and select the most precise classification consistent with the argument's own metaphysical assumptions.

### Step 4: Assess Explicitness

Classify each commitment on the explictness scale:

| Level | Definition | Detection Strategy |
|-------|-----------|-------------------|
| `explicit` | Stated directly in a premise: "There are numbers." | Direct textual match |
| `quantificational` | Implied by quantifier structure: `∃xFx` commits to Fs without explicitly saying "Fs exist." | Quinean test application |
| `presuppositional` | Required as a background condition for the argument to get off the ground: "If knowledge requires justified true belief, there must be beliefs." | Counterfactual test: would the argument fail if this entity did not exist? |
| `truthmaker-based` | Required as truthmaker for a truth claimed in the argument: "If 'snow is white' is true, there must be a truthmaker." | Truthmaker principle application |
| `implicit` | Detected via inference to best explanation: the best explanation of the argument's commitments includes this entity even though it is not explicitly or quantificationally required. | IBE analysis — what must be in the ontology to make sense of the argument's other commitments? |

For each commitment, justify the explicitness classification with reference to the specific textual or logical feature that triggers it. Explicit and quantificational commitments are the most robust; truthmaker-based and implicit commitments are more contestable and should be flagged as such.

### Step 5: Evaluate Controversiality and Alternatives

For each commitment, conduct a three-part evaluation:

**Part A: Controversiality Assessment**

Rate the commitment on the scale: `uncontroversial`, `moderately_controversial`, `highly_controversial`, `radical`.

Factors that increase controversiality:
- The entity belongs to a category whose existence is denied by a major philosophical tradition (e.g., abstract objects denied by nominalists, possible worlds denied by actualists, universals denied by trope theorists)
- The entity is exotic or theoretically loaded (e.g., haecceities, bare particulars, non-natural moral properties)
- The entity is redundant given other entities in the ontology (violations of parsimony)
- The entity has been subject to sustained skeptical or eliminativist arguments

Factors that decrease controversiality:
- The entity is a concrete particular whose existence is uncontroversial in common sense and science
- The entity is a logical construction reducible to less controversial entities
- The entity is a theoretical posit with strong explanatory utility and broad acceptance

For each rating, cite the relevant philosophical positions that would reject the commitment and the strength of their case.

**Part B: Alternative Paraphrase Possibilities**

For each `moderately_controversial` or higher commitment, explore whether a paraphrastic strategy could eliminate the commitment:

| Strategy | Description | Application |
|----------|-------------|-------------|
| Fictionalism | Treat discourse about the entity as useful fiction — statements involving it are false if taken literally, but useful within a pretense | Numbers (Field's mathematical fictionalism), possible worlds (Rosen's modal fictionalism) |
| Instrumentalism | The entity is a useful instrument for prediction/organization but does not exist | Theoretical entities, unobservables |
| Paraphrase nominalism | Reformulate the statements to avoid quantification over the entity while preserving truth conditions | Properties (paraphrased as predicate-tokens), events (paraphrased as sentences about objects) |
| Reduction | The entity reduces to a less controversial ontology | Possible worlds reduced to maximal consistent sets of propositions (linguistic ersatzism) |
| Deflationism | The statements are true but do not carry ontological commitment in the way assumed | Hirsch-style quantifier variance, Carnapian framework-internal questions |

For each applicable strategy, assess:
- Can the argument be reformulated using this strategy without losing its dialectical force?
- What costs does the strategy impose (loss of explanatory power, increased complexity, departure from ordinary language)?
- Would the argument's proponent likely accept this paraphrase, or would they resist it?

**Part C: Alternative Ontologies**

For each commitment, identify which major ontological positions accept it and which reject it. Example mapping:

- Commitment to `universals` → Accepted by: Platonism, Aristotelian realism. Rejected by: Nominalism, trope theory, conceptualism.
- Commitment to `possible_worlds` → Accepted by: Modal realism (Lewis), abstract modal realism (Plantinga, Stalnaker). Rejected by: Actualism, modal fictionalism.
- Commitment to `abstract_objects` → Accepted by: Platonism in mathematics. Rejected by: Nominalism (Field, Azzouni).

### Step 6: Compile Report

Synthesize all findings into the structured Ontological Commitment Report.

**Report structure:**

1. **Header**: Argument identifier, source, date of analysis.
2. **Detected Commitments Table**: OC1 through OCn, with all fields from Section 1 above.
3. **Ontological Profile**:
   - Overall Quinean ontology summary (narrative paragraph)
   - Most contentious commitment (highlighted, with justification)
   - Parsimony assessment (quantitative: count of entities and categories; qualitative: comparison to known positions)
   - Category breakdown table
4. **Implicit Ontology Map**: A visual/textual representation of how commitments relate to each other — e.g., if commitment to events depends on commitment to objects, or if commitment to facts is foundational and other commitments are derivative.
5. **Dialectical Implications**: If this argument is advanced against an opponent who holds a different ontology, what is the dialectical situation? Is the opponent forced to accept these commitments to engage with the argument, or can they resist?
6. **Recommendations**: Optional — if certain commitments are especially vulnerable and likely to be challenged, suggest whether the argument can be strengthened by reducing or reclassifying those commitments.

## Quality Criteria

1. **Exhaustiveness**: Every quantifier in the argument is examined. No existential quantifier pattern is overlooked. The report accounts for all quantified statements identified in Step 1. If a quantifier is present but the resulting commitment is judged trivial, this judgment is documented rather than silently omitted.

2. **Category Precision**: Each commitment is correctly classified by ontological category according to the standard taxonomy. Classifications are justified with reference to the category definitions in `ontological-categories.md`. Borderline cases are acknowledged and explained rather than forced into an inappropriate category.

3. **Quinean Rigor**: The bound-variable criterion is correctly applied in every case. The logical form of quantified statements is respected. Higher-order quantification is handled at the appropriate order. The distinction between objectual and substitutional quantification is observed.

4. **Alternative Awareness**: For every controversial commitment, plausible paraphrase strategies are identified and assessed. The report does not assume that a commitment is unavoidable without first exploring whether paraphrastic resources exist. The costs of paraphrase are fairly assessed.

5. **Neutrality**: The report distinguishes detecting commitments from evaluating them. The detection of a commitment does not imply endorsement or rejection of that commitment. The report's tone is descriptive and analytical, not polemical. The controversiality assessment identifies which positions would reject the commitment without arguing that those positions are correct or incorrect.

6. **Implicit Commitment Sensitivity**: Beyond explicit and quantificational commitments, the report identifies presuppositional, truthmaker-based, and implicit commitments where they are genuinely required by the argument. False positives (detecting commitments that are not genuinely required) are as much an error as false negatives (missing genuine commitments). Implicit commitments are flagged as more contestable.

## Relations to Other Skills

**Depends on:**
- `phil-argument-reconstruct`: Provides the argument in standard form with quantified structure. Without a reconstruction, the Quinean test cannot be reliably applied. The quality of the ontological commitment report is bounded by the quality of the reconstruction.
- `phil-premise-detect`: Hidden premises — those required to make the argument valid or to fill logical gaps — often contain the most significant ontological commitments. The premise audit identifies enthymematic premises that may introduce entities not mentioned in the explicit argument. If a premise audit is available, cross-reference it against detected commitments.

**References (read-only):**
- `ontological-categories.md`: The canonical taxonomy of ontological categories used in Step 3.
- `glossary-metaphysics.md`: Definitions of technical terms (trope, universal, haecceity, quiddity, etc.) used in the report.

**Dependents (skills that use this skill's output):**
- `phil-grounding-check`: Grounding and dependence relations operate on ontological commitments. Before determining what grounds what, one must know what the entities are that stand in grounding relations. The ontological commitment report provides the entity inventory against which dependence relations are mapped.
- `phil-natural-kind-analyze`: Natural kind analysis requires identifying which commitments are to kinds and whether those kinds are construed realistically or conventionally. The ontological commitment report identifies kind commitments and classifies them within the category taxonomy.

## Boundary Conditions

### 1. No Quantifiable Statements

If the argument contains no existential or universal quantification — e.g., it consists entirely of imperatives, questions, or purely logical tautologies — output:

> "No ontological commitments beyond trivial background assumptions detected."

Explain why: the argument's surface form does not trigger the Quinean test. Note that background assumptions (e.g., the existence of language, the existence of the arguer) are always present but are not attributably to the argument itself.

### 2. Ordinary Language

If the argument uses natural language without clear quantifier structure — common in continental philosophy, some ordinary language philosophy, or pre-Fregean texts — note the limitation explicitly:

> "This argument employs natural language without perspicuous quantifier structure. The following Quinean analysis represents a best-effort regimentation into first-order logic, but multiple regimentations are possible, and ontological commitment assessments may vary depending on regimentation choices."

Provide the best-effort analysis but flag that alternative formalizations could yield different commitment profiles. Where multiple regimentations are plausible, present the range of possible commitments.

### 3. Metaphysically Neutral Arguments

If the argument is carefully constructed to avoid ontological commitment — a common strategy in some areas of philosophy of science, meta-ethics, and deflationary metaphysics — acknowledge the neutrality strategy:

> "This argument appears to be constructed with ontological neutrality as a methodological goal. It avoids existential quantification over contested entities and does not presuppose controversial ontological categories. The following detected commitments represent only those that cannot be avoided without rendering the argument meaningless."

Do not invent commitments that the argument successfully avoids. Respect the proponent's methodological choices.

### 4. Pure Logic/Mathematics

Arguments in pure logic or mathematics may have only mathematical ontological commitments (sets, numbers, functions, logical forms). Classify these accordingly:

> "This argument's ontological commitments are confined to mathematical ontology: [list]. Whether mathematical ontology is itself ontologically committing is a further question (see the debate between mathematical Platonism and nominalism). This report takes no position on that question."

Do not conflate mathematical commitment with commitment to a broader ontology. The Quine-Putnam indispensability argument would extend mathematical commitment to physical ontology, but this is itself a substantive philosophical thesis that should not be assumed.

## ARS Interface

The ontological commitment report serves two primary functions within the broader Academic Research System (ARS).

**1. Academic Paper Integration**

The report can be passed to `ars academic-paper` as an "ontological presuppositions" section suitable for inclusion in the methodology chapter or introduction of a philosophy paper. The structured format (detected commitments list, ontological profile, category breakdown) maps naturally to academic prose. The section would typically read: "This argument presupposes the following ontological commitments: ... Of these, the most contentious is ... because ... Alternative paraphrasings, such as ..., could avoid this commitment but at the cost of ..."

**2. Deep Research Integration**

The report informs `ars deep-research` by identifying which ontological debates the paper engages. For example, if the report detects a commitment to abstract objects, the deep-research module knows to search for literature on nominalism, Platonism, and the indispensability argument. If it detects commitment to possible worlds, it searches for modal realism, ersatzism, and fictionalism. This enables targeted literature discovery rather than generic keyword searching.

**3. Revision Coach Integration**

When used with `ars revision-coach`, the ontological commitment report identifies vulnerabilities: commitments that opponents are likely to challenge. The revision coach can then suggest strategies for defending, reducing, or reclassifying those commitments, or for building paraphrase defenses into the argument preemptively.

**4. Cross-Skill Pipeline Integration**

The ontological commitment report is foundational within the metaphysics analysis pipeline. Before `phil-grounding-check` can determine which entities are fundamental and which are derivative, it needs the entity inventory provided by this skill. Before `phil-identity-persistence` can assess whether identity claims are coherent, it needs to know what kinds of things are being claimed to be identical. The report thus serves as the ontological baseline that all downstream analyses reference.

**5. Citation and Source Validation**

When passed to `ars citation-check`, the commitment report's classification of commitments by category and controversiality enables targeted verification: if the argument claims that a certain ontological category (e.g., tropes, possible worlds) is uncontroversial, the citation checker can verify whether the cited sources actually support that claim, or whether the argument misrepresents the state of the literature on the controversiality of that category.
