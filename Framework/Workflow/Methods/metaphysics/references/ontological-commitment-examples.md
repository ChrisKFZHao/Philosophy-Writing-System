# Ontological Commitment Detection — examples (conditional reference for method.metaphysics.ontological-commitment)

> Loaded only when the consuming mode's live ambiguity or the user's explicit request requires it; never loaded by default with the method file.

# Ontological Commitment Detection Examples

> This document demonstrates the practical application of ontological commitment detection across different argument types and commitment patterns. Each example shows the complete input-to-output process using Quinean criterion and ontological category taxonomy.

---

## Example 1: Simple Quinean Analysis — Mathematical Entities

### Input

> There are infinitely many prime numbers. Any arithmetic system that can represent basic arithmetic must quantify over numbers. Since our best scientific theories are formulated in mathematical language, we are committed to the existence of numbers — not as physical objects, but as abstract entities. Numbers are indispensable to science, so we must accept their existence.

This argument deploys the Quine-Putnam indispensability argument to commit its proponent to mathematical abstracta. The ontological commitment detection proceeds as follows:

### Output

```
## Ontological Commitment Report

### Basic Information
- **Argument ID**: OC-EX001
- **Argument Type**: Indispensability argument (abductive)
- **Source**: Composite — Quine/Putnam indispensability argument (reconstructed)
- **Date of Analysis**: 2026-07-11

---

### Section 1: Detected Commitments List

[OC1]
  entity_type:                Number (natural number, prime number, etc.)
  ontological_category:       abstract_object
  explicitness_level:         quantificational
  quinean_test_application:   Quantified statement: "There are infinitely many prime numbers."
                              Logical form: ∃x(Px ∧ x > 100) where domain is mathematical.
                              Bound variable: x ranges over numbers.
                              Required domain value: At least one number (in fact, infinitely many).
  controversiality_rating:    highly_controversial
  alternative_paraphrase:     Field's mathematical fictionalism — treat arithmetic statements as
                              useful fictions within a pretense. Cost: loss of literal truth for
                              mathematical claims; the argument's appeal to indispensability is
                              undermined if mathematical statements are not literally true.
  rejection_impact:           significant_weakening — the argument's conclusion directly asserts
                              existence of numbers; rejecting OC1 collapses the argument into
                              instrumentalism about mathematics.

[OC2]
  entity_type:                Set (the set of all prime numbers)
  ontological_category:       set
  explicitness_level:         quantificational
  quinean_test_application:   Quantified statement: Reference to "infinitely many" primes implies
                              quantification over the set or extension of prime numbers.
                              Logical form: ∃S∀x(x ∈ S ↔ Px)
                              Required domain value: An abstract set.
  controversiality_rating:    moderately_controversial
  alternative_paraphrase:     Plural quantification — "there are some things, the primes" — avoids
                              commitment to sets while preserving truth conditions. Cost: plural
                              logic is less standard but adequate for the argument's needs.
  rejection_impact:           minor_adjustment — the argument can be reformulated without sets
                              using plural quantification or second-order logic.

[OC3]
  entity_type:                Abstract entity (generic category of non-spatiotemporal existents)
  ontological_category:       abstract_object
  explicitness_level:         explicit
  quinean_test_application:   Explicit statement: "numbers are abstract entities." The argument
                              directly classifies numbers as abstracta, committing to the
                              existence of the category abstract_object itself.
  controversiality_rating:    highly_controversial
  alternative_paraphrase:     Carnapian framework-internal treatment — numbers "exist" only
                              internal to the mathematical framework, and the external question
                              of whether the framework itself exists is pragmatic. Cost: deflates
                              the argument's ontological force; the argument is supposed to be
                              about what really exists.
  rejection_impact:           fatal — the argument's conclusion is that abstract objects exist;
                              rejecting OC3 is rejecting the conclusion.

[OC4]
  entity_type:                Scientific theory (as a truth-bearing entity)
  ontological_category:       proposition
  explicitness_level:         presuppositional
  quinean_test_application:   Presuppositional: the argument presupposes that scientific theories
                              are truth-apt and that their truth commits us to the entities they
                              quantify over. Without this presupposition, the indispensability
                              premise has no ontological force.
  controversiality_rating:    moderately_controversial
  alternative_paraphrase:     Scientific instrumentalism — theories need not be true to be good;
                              they need only be empirically adequate. Cost: the indispensability
                              argument requires scientific realism about theories.
  rejection_impact:           fatal — if scientific theories carry no ontological commitment,
                              then indispensability to science is irrelevant to ontology.

---

### Section 2: Ontological Profile

**Overall Quinean Ontology Summary:**

This argument commits its proponent to a two-tier ontology: (i) concrete physical particulars
(implicitly, as the subject matter of scientific theories), and (ii) abstract mathematical objects
(numbers and sets). The concrete realm is presupposed but not argued for; the abstract realm is
the argument's explicit target. The argument's ontology is thus Platonistic about mathematics but
otherwise follows the Quinean strategy of reading ontology off our best scientific theories.

**Most Contentious Commitment:** OC1 (numbers as abstract objects). Nominalists of all stripes
(Field, Azzouni, Yablo) deny that quantification over numbers carries genuine ontological
commitment. The indispensability argument's force depends on whether one accepts that scientific
indispensability is a guide to ontology — a premise that nominalists systematically resist.

**Parsimony Assessment:**
- Quantitative: 4 distinct entity types (numbers, sets, abstracta-category, propositions).
  This is qualitatively sparse — only two ontological categories are invoked.
- Qualitative: Abstract objects are qualitatively luxuriant (they belong to a category that
  nominalists reject wholesale). Compared to known positions: this is standard Platonism about
  mathematics, more parsimonious than full-blown Platonism (no universals, no possible worlds)
  but less parsimonious than nominalism or fictionalism.

**Category Breakdown:**
  abstract_object: 2 (numbers, abstract entity category)
  set:             1 (set of primes)
  proposition:     1 (scientific theories as truth-bearers)
```

---

## Example 2: Higher-Order Quantification — Commitment to Properties

### Input

> Electrons all have negative charge. Protons all have positive charge. But negative charge and positive charge have something in common — they are both instances of the property of having charge. Indeed, there is a determinable property, charge, of which negative charge and positive charge are determinates. Since there are such determinable properties, and since quantification over properties is indispensable to physical theory, we are committed to the existence of properties as entities in their own right.

This argument deploys second-order quantification (quantification into predicate position) to commit to universals or property-types. The detection must handle higher-order Quinean application.

### Output

```
## Ontological Commitment Report

### Basic Information
- **Argument ID**: OC-EX002
- **Argument Type**: Definitional/Abductive hybrid
- **Source**: Composite — determinable/determinate property argument (reconstructed)
- **Date of Analysis**: 2026-07-11

---

### Section 1: Detected Commitments List

[OC1]
  entity_type:                Determinable property (charge)
  ontological_category:       universal
  explicitness_level:         quantificational (second-order)
  quinean_test_application:   Quantified statement: "There is a determinable property, charge."
                              Logical form: ∃X(DETERMINABLE(X) ∧ ∀Y(DETERMINATE(Y, X) → ...))
                              where X ranges over properties (second-order quantification).
                              Binding structure: Second-order existential quantifier binds a
                              predicate variable X; truth requires a property in the domain.
  controversiality_rating:    highly_controversial
  alternative_paraphrase:     Paraphrase nominalism — replace property quantification with
                              predicate-token quantification: "there are predicate tokens
                              '...is charged' that apply to electrons and protons." Cost:
                              loses the distinction between determinable and determinate
                              (predicates do not stand in determination relations naturally).
  rejection_impact:           fatal — the argument's conclusion is the existence of
                              determinable properties; rejecting OC1 rejects the conclusion.

[OC2]
  entity_type:                Determinate properties (negative charge, positive charge)
  ontological_category:       universal
  explicitness_level:         quantificational (second-order)
  quinean_test_application:   Quantified statement: "Negative charge and positive charge
                              are both instances of the property of having charge."
                              Logical form: ∃X∃Y(INSTANCE(X, C) ∧ INSTANCE(Y, C) ∧ X ≠ Y)
                              Second-order existential quantifiers bind X and Y over the
                              domain of properties.
  controversiality_rating:    highly_controversial
  alternative_paraphrase:     Trope theory — treat negative charge and positive charge as
                              particularized property instances (tropes) rather than universals.
                              The argument can be reformulated in trope-theoretic terms without
                              loss of its core claim about determinable/determinate structure.
                              Cost: requires accepting tropes, which are themselves controversial
                              (though less so than universals for some ontologists).
  rejection_impact:           significant_weakening — the determinable/determinate structure
                              can be preserved in a trope ontology, so the argument's core
                              insight survives, but the explicit commitment to universals
                              requires modification.

[OC3]
  entity_type:                Concrete particulars (electrons, protons)
  ontological_category:       concrete_particular
  explicitness_level:         explicit
  quinean_test_application:   Quantified statement: "Electrons all have negative charge."
                              Logical form: ∀x(ELECTRON(x) → NEGATIVE_CHARGE(x))
                              Universal quantification alone carries no commitment, but
                              the argument presupposes the existence of electrons and protons
                              as the bearers of charge properties.
  controversiality_rating:    uncontroversial
  alternative_paraphrase:     Not needed — the commitment to electrons and protons is
                              uncontroversial within the context of physical theory.
  rejection_impact:           independent — the property commitments (OC1, OC2) are the
                              argument's target; the concrete particular commitments are
                              background assumptions.

[OC4]
  entity_type:                Instantiation relation (the relation between property and bearer)
  ontological_category:       universal
  explicitness_level:         presuppositional
  quinean_test_application:   Presuppositional: the argument presupposes that there is a
                              relation of instantiation connecting properties to their bearers.
                              Without this relation, "electrons have charge" is not ontologically
                              analyzable as "electrons instantiate the property of charge."
  controversiality_rating:    moderately_controversial
  alternative_paraphrase:     Ostrich nominalism — refuse to analyze predication at all.
                              "Electrons have negative charge" does not require an instantiation
                              relation; it is a primitive predication. Cost: gives up on
                              analyzing the metaphysics of predication, which is the whole
                              point of the property-realist argument.
  rejection_impact:           significant_weakening — without the instantiation relation, the
                              argument's analysis of properties as entities collapses into
                              primitive predication.

---

### Section 2: Ontological Profile

**Overall Quinean Ontology Summary:**

This argument commits its proponent to three tiers of being: (i) concrete physical particulars
(electrons, protons), (ii) first-order properties as universals (charge, negative charge, positive
charge), and (iii) a relational universal (instantiation). This is a robustly realist ontology of
properties. The commitment to universals arises not from first-order quantification over
individuals but from second-order quantification over properties — a classic case where
Quinean commitment extends beyond the first-order domain.

**Most Contentious Commitment:** OC1/OC2 (universals). Nominalists of all varieties deny that
quantification into predicate position carries ontological commitment — they interpret it
substitutionally or as mere shorthand. Trope theorists accept properties but deny they are
universals. The argument's proponent must either defend second-order objectual quantification
or find an alternative route to property realism.

**Parsimony Assessment:**
- Quantitative: 4 entity types across 2 categories (concrete_particular, universal).
- Qualitative: Universals are among the most contested ontological categories. This ontology
  is comparable to Armstrong's immanent realism (universals exist only in their instances)
  or Lowe's four-category ontology. It is less luxuriant than full Platonism (no transcendent
  universals, no possible worlds).

**Category Breakdown:**
  concrete_particular: 1 (electrons/protons)
  universal:           3 (charge determinable, negative charge, positive charge, instantiation)
```

---

## Example 3: Implicit and Presuppositional Commitments — Truthmaker-Based Detection

### Input

> The proposition that snow is white is true. If a proposition is true, there must be something in the world that makes it true — a truthmaker. The truthmaker for "snow is white" cannot be merely the fact that we believe snow is white, nor the fact that the predicate "is white" applies to snow in our language. It must be a mind-independent fact: the actual whiteness of snow. Therefore, there are mind-independent facts, and true propositions are made true by them.

This argument deploys the truthmaker principle to argue for the existence of facts. Detection must identify truthmaker-based commitments that arise not from quantification but from the truthmaker principle itself.

### Output

```
## Ontological Commitment Report

### Basic Information
- **Argument ID**: OC-EX003
- **Argument Type**: Truthmaker argument (metaphysical/transcendental hybrid)
- **Source**: Composite — truthmaker argument for facts (reconstructed)
- **Date of Analysis**: 2026-07-11

---

### Section 1: Detected Commitments List

[OC1]
  entity_type:                Proposition (the proposition that snow is white)
  ontological_category:       proposition
  explicitness_level:         explicit
  quinean_test_application:   Explicit statement: "The proposition that snow is white is true."
                              Quantified structure: ∃p(PROPOSITION(p) ∧ p = <snow is white> ∧ TRUE(p))
                              Bound variable p ranges over propositions.
  controversiality_rating:    moderately_controversial
  alternative_paraphrase:     Sentence nominalism — treat "true" as a predicate of sentence tokens
                              rather than abstract propositions. "Snow is white" is true in English.
                              Cost: truth becomes language-relative; mind-independence of truth is
                              harder to sustain; the argument's claim about mind-independent facts
                              is weakened if truth-bearers are language-dependent.
  rejection_impact:           significant_weakening — the argument can be reformulated with
                              sentence-truth instead of propositional truth, but some
                              philosophical force is lost.

[OC2]
  entity_type:                Fact (the fact that snow is white; the whiteness of snow)
  ontological_category:       fact
  explicitness_level:         truthmaker-based
  quinean_test_application:   This commitment does not arise from the bound variable of any
                              explicit quantified statement in the argument. It arises from
                              the truthmaker principle: "If a proposition is true, there must
                              be something in the world that makes it true." The truthmaker
                              principle is a metaphysical bridge principle — it takes us from
                              a truth (a semantic or propositional fact) to an entity (a
                              truthmaker) that is ontologically distinct.
  controversiality_rating:    highly_controversial
  alternative_paraphrase:     Truthmaker deflationism — reject the truthmaker principle as
                              a guide to ontology. Truth is a primitive property of propositions
                              that does not require a distinct entity as truthmaker. Cost:
                              the argument collapses entirely; its sole premise is the truthmaker
                              principle. Alternatively, truth supervenes on being (Lewis) —
                              truth is determined by what exists, but no individual facts are
                              needed as truthmakers.
  rejection_impact:           fatal — the argument's conclusion is the existence of facts;
                              without the truthmaker principle, nothing remains.

[OC3]
  entity_type:                Mind-independent world (the world as concrete reality)
  ontological_category:       concrete_particular
  explicitness_level:         presuppositional
  quinean_test_application:   Presuppositional: the argument presupposes that there is a
                              mind-independent world containing snow. This is not argued for
                              but is the background against which the truthmaker claim is made.
                              Counterfactual test: if there were no mind-independent world,
                              would the argument fail? Yes — there would be nothing for facts
                              to be about.
  controversiality_rating:    uncontroversial
  alternative_paraphrase:     Idealism — the "fact" is a mental construction; no mind-independent
                              truthmaker is needed. Cost: the argument explicitly argues against
                              this; it is designed to establish mind-independent facts.
  rejection_impact:           independent — the existence of the external world is not what is
                              at stake; it is the existence of facts as a distinct ontological
                              category.

[OC4]
  entity_type:                Truthmaker relation (the "makes true" relation between facts and propositions)
  ontological_category:       universal
  explicitness_level:         implicit
  quinean_test_application:   Implicit commitment detected via inference to best explanation:
                              the argument repeatedly invokes the truthmaker relation ("makes true")
                              and treats it as a genuine relation with relata (facts, propositions).
                              Without this relation in the ontology, the argument's causal-explanatory
                              language ("something...that makes it true") is mere metaphor.
  controversiality_rating:    moderately_controversial
  alternative_paraphrase:     Truthmaker as primitive metaphysical explanation — the relation is
                              a primitive grounding relation, not a further entity. Cost: minimal;
                              most truthmaker theorists already treat the truthmaker relation as
                              a primitive grounding or necessitation relation rather than as a
                              separately existing universal.
  rejection_impact:           minor_adjustment — reclassifying the truthmaker relation as primitive
                              does not affect the argument's conclusion about fact existence.

---

### Section 2: Ontological Profile

**Overall Quinean Ontology Summary:**

This argument commits its proponent to a proposition-fact ontology: concrete reality (snow, the
world), abstract propositions (truth-bearers), mind-independent facts (truthmakers), and a
truthmaking relation connecting them. The core ontological innovation is OC2 (facts) — this is
what the argument aims to establish. Unlike the first two examples, the core commitment here
is truthmaker-based rather than quantificational, making it methodologically distinctive.

**Most Contentious Commitment:** OC2 (facts). Deflationists about truth, proponents of truth
supervenes on being, and ontological minimalists all reject that truth requires distinct truthmaking
entities. The argument's success depends on establishing that the truthmaker principle is a
genuine ontological principle rather than a trivial conceptual truth.

**Parsimony Assessment:**
- Quantitative: 4 entity types across 4 categories. This is relatively sparse in entity count
  but qualitatively involves a contested category (facts).
- Qualitative: Commitment to facts is a substantive ontological position (Armstrong, Lowe).
  Rivals include: fact nominalism (no facts, only objects and properties), truthmaker minimalism
  (objects alone are truthmakers), and primitivism (truth is primitive).

**Category Breakdown:**
  proposition:        1 (the proposition that snow is white)
  fact:               1 (the fact that snow is white)
  concrete_particular: 1 (snow, the world)
  universal:          1 (truthmaker relation)
```

---

## Example 4: Fictionalist Paraphrase Evaluation — Possible Worlds

### Input

> For any contingent proposition P, there is a possible world in which P is true and a possible world in which P is false. This is what it means for P to be contingent. Therefore, if there are contingent truths — and there obviously are — there must be possible worlds where those truths are false. Possible worlds exist.

This is a simplified version of a Lewisian argument for possible worlds. The detection must evaluate whether fictionalist paraphrase can avoid the commitment to possible worlds.

### Output

```
## Ontological Commitment Report

### Basic Information
- **Argument ID**: OC-EX004
- **Argument Type**: Definitional/Deductive
- **Source**: Composite — argument from contingency to possible worlds (reconstructed)
- **Date of Analysis**: 2026-07-11

---

### Section 1: Detected Commitments List

[OC1]
  entity_type:                Possible world
  ontological_category:       possible_world
  explicitness_level:         quantificational
  quinean_test_application:   Quantified statement: "There is a possible world in which P is true."
                              Logical form: ∀P(CONTINGENT(P) → ∃w(AT(w, P) ∧ ∃w'(AT(w', ¬P))))
                              where w ranges over possible worlds.
                              Bound variable: w; existential quantifier binds over the domain
                              of possible worlds.
  controversiality_rating:    highly_controversial
  alternative_paraphrase:     Rosen's modal fictionalism — statements about possible worlds are
                              true within the fiction of a plurality of worlds but are not
                              literally true. "There is a possible world where pigs fly" is
                              true according to the Lewisian fiction but false simpliciter.
                              Cost: the argument's conclusion "possible worlds exist" becomes
                              false (which is precisely what the fictionalist wants), but the
                              fictionalist can still use possible-worlds discourse as a useful
                              heuristic. The argument's force is neutralized.
  rejection_impact:           fatal if fictionalism is adopted — the argument's conclusion
                              is directly denied.

[OC2]
  entity_type:                Proposition
  ontological_category:       proposition
  explicitness_level:         quantificational
  quinean_test_application:   Quantified statement: "For any contingent proposition P..."
                              Logical form: ∀P(CONTINGENT(P) → ...)
                              Bound variable P ranges over propositions.
  controversiality_rating:    moderately_controversial
  alternative_paraphrase:     Sentence-based modality — replace quantification over propositions
                              with quantification over interpreted sentences. "For any contingent
                              sentence S..." Cost: modality becomes language-relative; the
                              argument's generality is limited to expressible propositions.
  rejection_impact:           significant_weakening — the argument's quantification over all
                              contingent propositions requires an ontology of propositions;
                              sentence-based approaches may not capture all contingent truths.

[OC3]
  entity_type:                Contingent truth (as a fact about the actual world)
  ontological_category:       fact
  explicitness_level:         explicit
  quinean_test_application:   Explicit statement: "There are contingent truths."
                              Logical form: ∃P(CONTINGENT(P) ∧ TRUE(P))
                              Commitment to at least one contingent truth.
  controversiality_rating:    uncontroversial
  alternative_paraphrase:     Not needed — the existence of some contingent truths is a
                              widely shared starting point across philosophical positions.
  rejection_impact:           fatal — if there are no contingent truths (necessitarianism),
                              the argument has no starting point. But rejecting OC3 would be
                              an extreme position (Spinozistic necessitarianism).

[OC4]
  entity_type:                The actual world (as one among many possible worlds)
  ontological_category:       possible_world
  explicitness_level:         presuppositional
  quinean_test_application:   Presuppositional: by treating possible worlds as an unrestricted
                              domain, the argument presupposes that the actual world is a member
                              of that domain — it is one possible world among many (the indexical
                              theory of actuality).
  controversiality_rating:    moderately_controversial
  alternative_paraphrase:     Actualist reduction — the actual world is not one world among
                              many; it is the only world. Other "possible worlds" are abstract
                              representations (maximal consistent sets of propositions, states
                              of affairs). Cost: the argument must be reformulated in actualist
                              terms; the quantification over worlds becomes quantification
                              over abstract representations.
  rejection_impact:           significant_weakening — the argument's elegant symmetry (one
                              quantifier over all worlds, actual and possible) is lost.

---

### Section 2: Ontological Profile

**Overall Quinean Ontology Summary:**

This argument commits its proponent to a modal realist ontology: propositions (as the bearers
of contingency), possible worlds (as the ontological ground of modal truth), and the actual
world (as an indexically distinguished member of the plurality of worlds). This is a distinctively
Lewisian ontology — it takes the quantifier at face value and refuses to paraphrase away the
commitment to possible worlds. The commitment is robustly Quinean: it arises directly from
existential quantification over worlds and cannot be eliminated without either paraphrasing the
quantifier or rejecting the argument's premise.

**Most Contentious Commitment:** OC1 (possible worlds). This is among the most contested
ontological commitments in all of metaphysics. Lewis's genuine modal realism — the thesis that
possible worlds are concrete entities of the same kind as the actual world — is accepted by a
small minority of philosophers. Even modal realists typically prefer ersatzist versions (worlds
as abstract entities). The argument as presented is vulnerable to multiple paraphrase strategies,
the most prominent being Rosen's modal fictionalism and Plantinga's actualist reduction.

**Parsimony Assessment:**
- Quantitative: 4 entity types across 3 categories. Numerically sparse.
- Qualitative: The commitment to possible worlds makes this ontology qualitatively luxuriant
  in the extreme — Lewis's pluriverse contains an enormous infinity of concrete worlds. Even
  ersatzist versions are less qualitatively profligate but still introduce a category (possible_world)
  that actualists reject. Compared to known positions: this is maximally non-parsimonious by
  actualist standards; Lewis would reply that qualitative parsimony is the wrong metric.

**Category Breakdown:**
  possible_world: 2 (possible worlds, actual world)
  proposition:    1 (propositions)
  fact:           1 (contingent truths as facts)

**Fictionalist Paraphrase Feasibility:** The strongest paraphrase strategy is Rosen's modal
fictionalism. The argument can be reconstructed as: "According to the fiction of a plurality
of worlds, there is a world where P and a world where not-P, for any contingent P. This is
what it means for P to be contingent." The fictionalist accepts the utility of possible-worlds
discourse without accepting the literal existence of possible worlds. The cost is that the
argument's conclusion "possible worlds exist" is false, but the fictionalist does not want that
conclusion — they want the explanatory power without the ontological commitment. The
arguer's dialectical opponent can accept the fictionalist paraphrase and thereby accept the
argument's premises while rejecting its ontological conclusion.
```

---

## Example 5: Cross-Domain — Metaethical Commitment to Moral Properties

### Input

> Some actions are morally wrong. If an action is morally wrong, there must be something about that action that makes it wrong. This "something" cannot be reduced to natural properties — for any natural property N, it is an open question whether an action with N is wrong (Moore's Open Question Argument). Therefore, the property of wrongness is a non-natural property, and we are committed to the existence of non-natural moral properties.

This is a metaethical argument that generates ontological commitments in the moral domain. The detection must handle both moral and metaphysical categorization simultaneously.

### Output

```
## Ontological Commitment Report

### Basic Information
- **Argument ID**: OC-EX005
- **Argument Type**: Hybrid — Open Question Argument (semantic) + truthmaker (metaphysical)
- **Source**: Composite — Moorean argument for non-natural moral properties (reconstructed)
- **Date of Analysis**: 2026-07-11

---

### Section 1: Detected Commitments List

[OC1]
  entity_type:                Moral property (wrongness, rightness)
  ontological_category:       property
  explicitness_level:         explicit
  quinean_test_application:   Explicit statement: "Some actions are morally wrong."
                              Logical form: ∃x(ACTION(x) ∧ WRONG(x))
                              Predicative commitment: the predicate "...is wrong" may carry
                              ontological commitment to the property wrongness if properties
                              are what predicates refer to (the "Fido"-Fido theory of meaning,
                              rejected by Quine but active in Moore's argument).
  controversiality_rating:    highly_controversial
  alternative_paraphrase:     Expressivism — "Some actions are morally wrong" does not ascribe
                              a property to actions; it expresses a con-attitude toward them.
                              The quantifier "some" is not objectually committing. Cost: the
                              argument's entire framework (properties, truthmakers, reduction)
                              presupposes cognitivism; the expressivist rejects the starting point.
  rejection_impact:           fatal — if expressivism is true, the argument never gets off
                              the ground because moral sentences do not purport to describe
                              properties.

[OC2]
  entity_type:                Non-natural property (sui generis moral property)
  ontological_category:       property
  explicitness_level:         explicit (conclusion)
  quinean_test_application:   Concluding statement: "The property of wrongness is a non-natural
                              property." Quantified form: ∃P(NON_NATURAL(P) ∧ MORAL(P)).
                              The commitment to non-naturalness is the argument's distinctive
                              contribution — it is not merely that moral properties exist, but
                              that they are of a special, irreducible kind.
  controversiality_rating:    radical
  alternative_paraphrase:     Naturalist reduction — wrongness is identical to some natural
                              property (e.g., failing to maximize utility). Cost: the Open
                              Question Argument is designed precisely to block this; accepting
                              naturalist reduction requires rejecting Moore's semantic premise.
                              Alternatively, error theory — there are no moral properties;
                              "Some actions are wrong" is systematically false. Cost: the
                              argument's first premise is denied.
  rejection_impact:           fatal — the argument's conclusion is the existence of non-natural
                              moral properties; rejecting OC2 is rejecting the conclusion.

[OC3]
  entity_type:                Natural property (as the baseline for comparison)
  ontological_category:       property
  explicitness_level:         presuppositional
  quinean_test_application:   Presuppositional: the Open Question Argument presupposes that
                              natural properties exist and are well-understood, so that the
                              contrast between natural and non-natural can be drawn. The argument
                              contrasts wrongness with natural properties, implying that the
                              latter are less ontologically problematic.
  controversiality_rating:    uncontroversial
  alternative_paraphrase:     Not needed — natural properties are widely accepted. However,
                              a radical nominalist might challenge property-talk in both the
                              natural and moral domains. Cost: the argument loses its contrast
                              class if neither natural nor non-natural properties exist.
  rejection_impact:           independent — the existence of natural properties is not what is
                              at stake; it is the existence of non-natural properties beyond them.

[OC4]
  entity_type:                Action (as the bearer of moral properties)
  ontological_category:       event
  explicitness_level:         explicit
  quinean_test_application:   Quantified statement: "Some actions are morally wrong."
                              First-order existential quantifier binds variable over actions.
  controversiality_rating:    uncontroversial
  alternative_paraphrase:     Not needed.
  rejection_impact:           independent — the argument is about moral properties, not about
                              actions; the existence of actions is a background assumption.

[OC5]
  entity_type:                Open question relation (the conceptual relation between a moral
                              term and natural terms)
  ontological_category:       proposition
  explicitness_level:         implicit
  quinean_test_application:   Implicit: the Open Question Argument relies on a semantic-epistemic
                              fact — that for any natural property N, it is an open question
                              whether an action with N is wrong. This is an implicit commitment
                              to the proposition that the open question test is a reliable
                              guide to property non-identity.
  controversiality_rating:    moderately_controversial
  alternative_paraphrase:     The open question test is methodological, not ontological — it
                              does not introduce a new entity but structures our inquiry. The
                              test can be rejected without ontological cost (as the Canberra
                              Plan and analytic functionalists do).
  rejection_impact:           fatal — the Open Question Argument relies on this methodological
                              principle; rejecting it undermines the argument's inference from
                              semantic open-ness to metaphysical distinctness.

---

### Section 2: Ontological Profile

**Overall Quinean Ontology Summary:**

This argument commits its proponent to a layered moral ontology: concrete events (actions),
natural properties (as the contrast class), non-natural moral properties (the target commitment),
and a semantic-epistemic relation (the open question test) linking the moral to the natural.
This is a paradigmatic non-naturalist realist ontology in metaethics — moral properties exist,
they are irreducible to natural properties, and their irreducibility is established by semantic
analysis. This ontology is comparable to Moore's and, in contemporary metaethics, to the
positions of Parfit (non-naturalist realism) and Enoch (robust realism).

**Most Contentious Commitment:** OC2 (non-natural moral properties). This is among the most
contested commitments in metaethics. Naturalists (Railton, Boyd, Jackson) reject it by arguing
that moral properties are identical to natural properties despite the open question intuition.
Expressivists (Blackburn, Gibbard) reject it by denying that moral language is assertoric.
Error theorists (Mackie, Joyce) reject it by denying that any moral properties exist. The
non-naturalist must defend against all three camps simultaneously.

**Parsimony Assessment:**
- Quantitative: 5 entity types across 3 categories (property, event, proposition).
- Qualitative: Non-natural properties are qualitatively luxuriant — they add a sui generis
  category of entity to the ontology. Mackie's argument from queerness targets precisely
  this: non-natural properties would be "utterly different from anything else in the universe."
  Compared to known positions: less parsimonious than naturalist realism (which identifies
  moral properties with natural ones), equally parsimonious as non-naturalist realism, and
  more parsimonious than theistic moral realism (which adds divine commands).

**Category Breakdown:**
  property:    3 (wrongness, non-natural moral properties, natural properties)
  event:       1 (actions)
  proposition: 1 (open question test as propositional commitment)

**Cross-Domain Note:** This example illustrates the cross-domain applicability of ontological
commitment detection. The Quinean criterion operates identically whether the domain is
mathematics (Example 1), fundamental physics (Example 2), modality (Example 4), or metaethics
(this example). What varies is which philosophical positions reject which commitments, and
which paraphrase strategies are available. The detection machinery is domain-neutral; the
dialectical analysis is domain-specific.
```

---

## Example 6: Mixed Commitment Pattern — Ontological Neutrality Strategy

### Input

> We shall remain ontologically neutral. We do not claim that numbers exist. We claim only that our best scientific theories are most elegantly formulated when they use mathematical language. Whether this mathematical language carries ontological commitment is a further question, which we do not settle. Our argument is: the predictive success of mathematized science is best explained by the hypothesis that the mathematical structures we employ correspond to real structural features of the world. This is a claim about structural correspondence, not about the existence of abstract objects.

This argument attempts to remain ontologically neutral while invoking mathematical entities. The detection must identify the neutrality strategy and assess whether the argument successfully avoids commitment.

### Output

```
## Ontological Commitment Report

### Basic Information
- **Argument ID**: OC-EX006
- **Argument Type**: Abductive (IBE) with ontology-avoidance strategy
- **Source**: Composite — ontologically neutral structuralist argument (reconstructed)
- **Date of Analysis**: 2026-07-11

---

### Boundary Condition Triggered: Metaphysically Neutral Arguments

**Assessment:** "This argument appears to be constructed with ontological neutrality as a
methodological goal. It avoids existential quantification over contested entities and does not
presuppose controversial ontological categories. The following detected commitments represent
only those that cannot be avoided without rendering the argument meaningless."

---

### Section 1: Detected Commitments List

[OC1]
  entity_type:                Structural feature (of the world)
  ontological_category:       property
  explicitness_level:         explicit
  quinean_test_application:   Explicit statement: "...correspond to real structural features of
                              the world." The argument commits to the existence of "structural
                              features" — which, if structural features are properties or relations
                              of the world, carries property-commitment.
                              Logical form: ∃S(STRUCTURAL_FEATURE(S) ∧ CORRESPONDS(math_struct, S))
  controversiality_rating:    moderately_controversial
  alternative_paraphrase:     Structuralism without objects (Ladyman, French) — structural
                              features are ontologically primitive; they are not properties
                              of objects because there are no objects, only structures. Cost:
                              radical metaphysical revision; most philosophers treat structural
                              features as parasitic on an ontology of objects and properties.
  rejection_impact:           significant_weakening — the argument's positive claim is that
                              structural features explain predictive success; rejecting OC1
                              leaves the predictive success unexplained by the argument.

[OC2]
  entity_type:                Mathematical structure
  ontological_category:       abstract_object
  explicitness_level:         quantificational (disputed)
  quinean_test_application:   Quantified statement: "The mathematical structures we employ."
                              This appears to quantify over mathematical structures. However,
                              the argument's proponent explicitly disavows commitment to
                              abstract objects. Resolution: the quantifier may be interpreted
                              substitutionally (structures as linguistic entities) or the
                              argument may treat "mathematical structures" as a façon de parler.
  controversiality_rating:    moderately_controversial
  alternative_paraphrase:     Substitutional quantification — "mathematical structures" are
                              not entities over which we quantify; they are placeholders in
                              our linguistic framework. The quantifier is substitutional rather
                              than objectual. Cost: the correspondence relation (between
                              mathematical structures and structural features) becomes harder
                              to analyze; substitutional quantification does not easily support
                              correspondence claims.
  rejection_impact:           minor_adjustment — the argument's proponent can clarify that
                              their quantification is substitutional and avoid the commitment.

[OC3]
  entity_type:                Correspondence relation (between mathematical structure and world)
  ontological_category:       universal
  explicitness_level:         implicit
  quinean_test_application:   Implicit: the argument invokes "correspondence" as a substantive
                              relation between two relata (mathematical structures and structural
                              features). This relation must exist in the ontology for the
                              correspondence claim to be true.
  controversiality_rating:    moderately_controversial
  alternative_paraphrase:     Deflationary correspondence — "correspondence" is not a substantive
                              relation but a disquotational device. "The mathematical structure
                              corresponds to structural features" means no more than "the
                              mathematical structure adequately models the structural features."
                              Cost: the argument's explanatory force is reduced; it becomes a
                              claim about modeling adequacy rather than ontological correspondence.
  rejection_impact:           significant_weakening — the argument's abductive force depends
                              on correspondence being a genuine explanatory relation; deflationary
                              correspondence may not carry explanatory weight.

[OC4]
  entity_type:                Scientific theory
  ontological_category:       proposition
  explicitness_level:         presuppositional
  quinean_test_application:   Presuppositional: the argument presupposes the existence of
                              scientific theories as entities that can be "formulated" and
                              that have "predictive success."
  controversiality_rating:    uncontroversial
  alternative_paraphrase:     Not needed.
  rejection_impact:           independent — the ontological status of theories themselves is
                              not at issue.

---

### Section 2: Ontological Profile

**Overall Quinean Ontology Summary:**

This argument attempts ontological neutrality with partial success. It avoids explicit commitment
to abstract objects (numbers, sets, possible worlds) and to non-natural properties. However, it
cannot avoid all commitment: structural features (as real features of the world), a correspondence
relation, and a background ontology of scientific theories are all required for the argument to
function. The argument's proponent would characterize these as "minimal" or "uncontroversial"
commitments, but a thoroughgoing nominalist would still object to structural features and
correspondence as illicit property-talk.

**Most Contentious Commitment:** OC1 (structural features). A radical nominalist who rejects
all properties and relations would find this commitment objectionable. However, structural
features are significantly less controversial than the abstract objects the argument explicitly
disavows. The argument succeeds in being more ontologically parsimonious than full Platonism
while retaining explanatory power.

**Neutrality Strategy Assessment:**

The argument employs a two-part neutrality strategy: (i) it explicitly disavows commitment to
the most controversial ontological category (abstract objects), and (ii) it shifts the ontological
weight to less controversial categories (structural features, correspondence). The strategy is
partially successful but not fully neutral — the commitments to OC1, OC2, and OC3 are genuine
ontological commitments even if less controversial. A thoroughgoing deflationist (Carnapian,
Hirschian) would argue that even these commitments are framework-internal rather than
substantively ontological. The argument's proponent can use quantifier variance to argue that
their "structural features" are internal to a pragmatic framework, but this would further weaken
the argument's explanatory ambitions.

**Parsimony Assessment:**
- Quantitative: 4 entity types across 3 categories. Numerically comparable to the other examples.
- Qualitative: This is the most qualitatively sparse of all examples — no abstracta (by explicit
  disavowal), no possible worlds, no non-natural properties. Compared to known positions: this
  is closest to structural realism (Ladyman, French) or ontic structural realism, which accepts
  structures but rejects objects.

**Category Breakdown:**
  property:    2 (structural features, correspondence relation)
  abstract_object: 1 (mathematical structure — disputed, may be eliminable)
  proposition: 1 (scientific theories)
```
