# Causation Taxonomy

A Systematic Survey of Causal Theories for Philosophical Analysis

---

## 1. Introduction

Causation is a central concept in metaphysics, philosophy of science, and
philosophy of mind. It underwrites explanation, prediction, moral and legal
responsibility, and our sense of agency in the world. Philosophers have long
sought to analyze what it means for one event or fact to cause another, and
the resulting literature contains a rich array of competing theories, each
with characteristic strengths and characteristic difficulties.

This taxonomy organizes the major families of causal theories, identifying
their core commitments, principal variants, motivating insights, and the
key problems or counterexamples each family addresses (or fails to address).
It is designed to support systematic comparison across theories and to
highlight the dialectical pressures that have driven theoretical innovation.
The taxonomy is organized by theoretical family, with sub-variants enumerated
under each heading as appropriate, and concludes with a survey of special
topics that cut across multiple families.

---

## 2. Regularity Theories

### 2.1 Core Claim

Causation is reducible to regular succession: *c* causes *e* just in case
events of type C are regularly followed by events of type E. There is no
hidden "necessary connection" beyond the observed pattern.

### 2.2 Principal Variants

#### 2.2.1 Hume's Constant-Conjunction Account

David Hume (1739, 1748) argued that all we observe is the constant
conjunction of like events: the impression of one type of event is
regularly followed by the impression of another. The idea of necessary
connection is projected onto the world by the mind, a product of custom
and habit. Hume's analysis is:

- **Contiguity**: cause and effect must be spatially and temporally adjacent.
- **Temporal priority**: the cause precedes the effect.
- **Constant conjunction**: events of the causal type are always followed by
  events of the effect type.

#### 2.2.2 Mill's Method of Difference

John Stuart Mill (1843) systematized Hume's insight into canons of
inductive reasoning. The Method of Difference is the most directly
causal:

> If an instance in which the phenomenon under investigation occurs,
> and an instance in which it does not occur, have every circumstance
> in common save one (that one occurring only in the former), the
> circumstance in which alone the two instances differ is the effect,
> or the cause, or an indispensable part of the cause, of the phenomenon.

Mill also proposed the Method of Agreement, the Joint Method, the Method
of Residues, and the Method of Concomitant Variation, collectively forming
the backbone of early experimental inference.

#### 2.2.3 Mackie's INUS Conditions

J.L. Mackie (1965, 1974) refined the regularity approach by recognizing
that causes are rarely necessary or sufficient in isolation. His INUS
analysis:

> A cause is an **I**nsufficient but **N**ecessary part of an
> **U**nnecessary but **S**ufficient condition.

- A short-circuit (c) is neither necessary (a fire could start by other
  means) nor sufficient (oxygen and fuel are also needed) for a house fire.
- But c is a necessary member of *some* set of conditions (short-circuit +
  oxygen + fuel) that is jointly sufficient for the fire, and that set as a
  whole is unnecessary (other sufficient sets exist: arson + oxygen + fuel).
- Hence c is an INUS condition.

Mackie's account captures the "causal field" idea: causes operate against
a background of standing conditions that we take for granted.

### 2.3 Strengths

| Strength | Explanation |
|---|---|
| Metaphysical parsimony | Reduces causation to observable patterns; no commitment to unobservable necessary connections, powers, or possible worlds. |
| Empiricist motivation | Rooted in what can be known through experience; aligns with Humean strictures on knowledge. |
| Grounding in scientific practice | Mill's methods capture key patterns of experimental inference. |
| Causal pluralism | INUS conditions allow multiple sufficient constellations, capturing complex causal structures. |

### 2.4 Problems

| Problem | Description |
|---|---|
| Distinguishing causal from accidental regularities | Not every constant conjunction is causal (day follows night, but night does not cause day). Regularity theories struggle to distinguish nomological from merely accidental regularities without appealing to laws, which themselves need a causal basis on pain of circularity. |
| Preemption | When a backup cause is poised to bring about e but is preempted by the actual cause, regularity theories fail: the effect is not regularly preceded by the actual cause's type (the backup would have produced it anyway), nor is it counterfactually dependent on the actual cause. |
| Direction of causation | Mere succession does not distinguish cause from effect; symmetry objections arise. |
| Omissions and absences | It is unclear how an absence (a non-event) can stand in relations of constant conjunction with anything. |

---

## 3. Counterfactual Theories

### 3.1 Core Claim

Causation is analyzable in terms of counterfactual dependence: *c* causes
*e* just in case, had *c* not occurred, *e* would not have occurred.

### 3.2 Principal Variants

#### 3.2.1 Lewis (1973): Counterfactual Dependence

David Lewis's seminal analysis:

> Where *c* and *e* are two distinct actual events, *e* causally depends
> on *c* if and only if, if *c* had not occurred, *e* would not have
> occurred. Causation is the ancestral of causal dependence.

Lewis provides a possible-worlds semantics for counterfactuals:

- A counterfactual "If A were the case, C would be the case" is true
  (at the actual world) iff some world where A and C are both true is
  closer (more similar) to the actual world than any world where A is
  true and C is false.
- Similarity is governed by a system of weights: avoid big, widespread,
  diverse violations of law; maximize spatiotemporal region of perfect
  match; avoid small, localized, simple violations of law (in that
  priority order).

Key features of the 1973 account:
- Causation is transitive (ancestral of dependence).
- The analysis is reductive: causation is cashed out in non-causal terms
  (similarity of worlds, laws of nature).
- Events are fine-grained, occurring in specific regions of spacetime.

#### 3.2.2 Lewis (2000): Influence Account

Pushed by late preemption counterexamples, Lewis revised his analysis:

> *c* causes *e* iff there is a substantial pattern of counterfactual
> dependence—not necessarily of whether *e* occurs, but of *how*, *when*,
> and *in what manner* *e* occurs—on whether, how, when, and in what
> manner *c* occurs.

- "Influence" covers alterations in the time, place, and manner of the
  effect in response to small alterations of the cause.
- This handles late preemption: the preempted backup does not influence
  the effect because small changes to the backup alter nothing about the
  effect—the actual cause is already determining the effect.

#### 3.2.3 Other Counterfactual Approaches

- **Woodward's interventionist counterfactuals** (see Section 6 below):
  grafts counterfactuals onto an explicitly interventionist framework.
- **Yablo's proportionality constraint**: the cause must be proportional
  to the effect—neither too specific nor too general. This addresses some
  problems of causal selection.

### 3.3 Strengths

| Strength | Explanation |
|---|---|
| Handles prevention and omission | "The doctor's failure to administer antibiotics caused the patient's death" is analyzed as: if the doctor *had* administered antibiotics, the patient would not have died. Absences enter counterfactuals naturally. |
| Non-reductive treatment of laws | Counterfactual dependence does not require identifying causal laws in advance; it leverages similarity metrics that may be independently motivated. |
| Asymmetry | Counterfactual dependence is temporally asymmetric in typical worlds; the future depends on the past but not vice versa. |
| Formal rigor | Possible-worlds semantics provides a well-defined formal framework. |

### 3.4 Problems

| Problem | Description |
|---|---|
| Late preemption | Suzy and Billy both throw rocks at a bottle. Suzy's rock hits first, shattering it. Billy's rock would have shattered it had Suzy's missed. The shattering does *not* counterfactually depend on Suzy's throw (Billy's throw would have sufficed), yet Suzy's throw is clearly the cause. |
| Early preemption | Suzy throws her rock; Billy sees this and refrains. Had Suzy not thrown, Billy would have thrown. No counterfactual dependence, yet Suzy's throw is the cause. Lewis's influence account addresses late but arguably not all cases of early preemption. |
| Trumping | The sergeant and the major simultaneously order the soldiers to advance. The major's order "trumps" the sergeant's. Had the major not ordered, the soldiers would still have advanced (the sergeant's order suffices). Yet the major's order is the cause. Counterfactual dependence fails. |
| Overdetermination | Two assassins fire simultaneously; either bullet would have been fatal. Neither shot is counterfactually necessary, yet both are causes. |
| Symmetric overdetermination | As above, but symmetric: no principled way for counterfactual accounts to pick out one as the cause. |
| Transitivity | Lewis's ancestral account makes causation transitive, but there are plausible counterexamples (e.g., the dog-bite case: bite causes infection, infection causes death, but does the bite cause death? The infection might have been cured, but if it was not, transitivity seems to hold. The debate is live.) |

---

## 4. Probabilistic Theories

### 4.1 Core Claim

Causation is a matter of probability-raising: *c* causes *e* just in case
*c* raises the probability of *e* (relative to some appropriate background
conditions). The central insight is that causes make their effects more
likely, even when they do not necessitate them.

### 4.2 Principal Variants

#### 4.2.1 Suppes (1970): Prima Facie Causes

Patrick Suppes defines:

> *c* is a prima facie cause of *e* iff (i) *c* occurs before *e*,
> (ii) P(*e* | *c*) > P(*e*).

A *genuine* cause is a prima facie cause that is not screened off by
a more temporally proximate event. Screening off: *a* screens off *c*
from *e* if P(*e* | *c* & *a*) = P(*e* | *a*).

Suppes's theory was an early formalization of the idea that causal
relations are revealed by conditional probability inequalities.

#### 4.2.2 Cartwright (1989): Causal Capacities

Nancy Cartwright argues that probabilistic theories must be supplemented
by a metaphysics of *capacities*—stable, context-invariant tendencies of
objects or systems to produce certain outcomes:

- Mere probability-raising is insufficient; what causal claims assert is
  the operation of a capacity.
- Capacities are measured by probabilities, but not reducible to them.
- This moves away from pure Humean supervenience toward a more robustly
  realist metaphysics of causal powers.

#### 4.2.3 Eells (1991) and Skyrms (1980): Probabilistic Relevance

Ellery Eells and Brian Skyrms refine the probabilistic-relevance approach
by attending to the problem of *contextual unanimity*:

- A factor *c* is a positive causal factor for *e* iff, in every causally
  homogeneous background context, *c* raises the probability of *e*.
- A *causally homogeneous* context is one where all other causes of *e*
  are held fixed.

This handles Simpson's paradox: a drug may lower recovery probability in
each sub-population (men, women) while appearing to raise it in the aggregate
(if more men receive the drug and men recover more readily). Causation is
tied to probability-raising *within* homogeneous partitions.

#### 4.2.4 Causal Bayes Nets

Spirtes, Glymour, and Scheines (1993, 2000); Pearl (2000, 2009):

- Represent causal structure as a directed acyclic graph (DAG).
- Nodes = variables; edges = direct causal relations.
- The Markov condition: a variable is independent of its non-descendants
  given its parents.
- The Faithfulness condition: all independencies in the probability
  distribution are entailed by the Markov condition applied to the true
  causal graph.
- Causal discovery algorithms (PC, FCI) infer causal structure from
  patterns of conditional independence.
- Pearl's *do*-calculus formalizes the effect of interventions:
  P(*y* | *do*(*x*)) is distinct from P(*y* | *x*).

### 4.3 Strengths

| Strength | Explanation |
|---|---|
| Handles indeterministic causation | Probability-raising is defined even when causation is chancy; quantum mechanics and the special sciences fit naturally. |
| Captures degrees of causal contribution | Different causes can raise probability to different degrees; no forced binary of "cause or not." |
| Formal and algorithmic | Causal Bayes nets provide a computationally tractable framework for discovery and inference. |
| Intervention distinction | The *do*-calculus formalizes the difference between observing and intervening, a longstanding philosophical distinction. |

### 4.4 Problems

| Problem | Description |
|---|---|
| Spurious correlations | Barometer reading does not cause storms, though it raises their probability. Common causes produce probabilistic dependencies without direct causation. |
| Simpson's paradox | Aggregated probabilities can reverse conditional probabilities. Requires careful partitioning, which itself presupposes causal knowledge. |
| Singular causation | Probabilistic theories are primarily type-level; they say less about singular causal claims ("this rock's throw caused this window's shattering"). |
| Negative relevance | Some causes lower the probability of their effects (preventive causes). A vaccine lowers disease probability but is a cause of immunity. The simple probability-raising condition must be qualified. |
| The problem of priors | Probabilistic frameworks need a prior probability distribution, and the choice of prior can affect causal conclusions—yet there is rarely a uniquely rational prior. |

---

## 5. Process Theories

### 5.1 Core Claim

Causation is a physical process connecting cause to effect through a
spatiotemporally continuous sequence. The fundamental causal relation is
not regular succession or counterfactual dependence but the transmission
of a physical quantity or mark through space and time.

### 5.2 Principal Variants

#### 5.2.1 Salmon (1984): Mark-Transmission Account

Wesley Salmon's mark-transmission theory:

- A **causal process** is a physical process that is capable of
  transmitting a mark (a local modification of structure).
- A **pseudo-process** (e.g., a spot of light moving across a wall) cannot
  transmit a mark; if you modify the spot at one time, the modification is
  not carried forward—it is merely a succession of distinct events.
- The mark criterion: if a process is genuinely causal, a local
  modification introduced at one point (the mark) will persist and be
  transmitted to later stages of the process.
- **Causal interaction** occurs when two causal processes intersect and
  produce lasting modifications in each other.

Salmon later supplemented this with a conserved-quantity account (inspired
by Dowe).

#### 5.2.2 Dowe (1992, 2000): Conserved-Quantity Theory

Phil Dowe's conserved-quantity theory refines Salmon's account:

- A **causal process** is a world-line of an object that possesses a
  conserved quantity.
- A **causal interaction** is an intersection of world-lines involving
  exchange of a conserved quantity.
- Conserved quantities are those governed by conservation laws in physics:
  mass-energy, linear momentum, angular momentum, charge, etc.
- This eliminates the need for the counterfactually-loaded notion of
  "transmitting a mark."

Dowe's account is explicitly physicalist: causation is constituted by
the exchange of conserved quantities, and anything that does not involve
such exchange is not, strictly speaking, causation.

### 5.3 Strengths

| Strength | Explanation |
|---|---|
| Handles preemption | In both early and late preemption, the actual cause is connected to the effect by a continuous physical process; the preempted backup's process does not reach the effect. The physical connection picks out the right cause without reliance on counterfactuals. |
| Avoids "action at a distance" | Requires spatiotemporally continuous connection; rules out magical or purely counterfactual causation. |
| Physical grounding | Anchors causation in fundamental physics; avoids modal or epistemic primitives. |
| Distinguishes causal from pseudo-processes | The mark criterion and conserved-quantity criterion give objective grounds for the distinction. |

### 5.4 Problems

| Problem | Description |
|---|---|
| Omissions and absences | If causation requires a physical process, how can an absence (e.g., failure to water a plant) cause anything? There is no world-line of an omission, no conserved quantity exchanged. Yet omission-causation is central to legal, moral, and everyday reasoning. |
| Disconnections | Some putative causes involve disconnections rather than connections (e.g., cutting a rope causes the chandelier to fall). Dowe treats disconnections as interactions involving conserved quantities, but critics argue this stretches the notion of exchange. |
| Mental causation | If all causation is physical exchange of conserved quantities, mental events (thoughts, decisions) cannot cause physical effects—or must be identified with physical processes, inviting the exclusion problem. |
| Double prevention | If A prevents B from preventing C, does A cause C? Process theories struggle with nested preventions where no continuous physical link runs from A to C. |

---

## 6. Manipulationist / Interventionist Theories

### 6.1 Core Claim

Causation is fundamentally tied to the possibility of manipulation:
*X* causes *Y* just in case there is a possible intervention on *X*
(an idealized experimental manipulation) that would change *Y* (or the
probability distribution of *Y*).

### 6.2 Principal Variant: Woodward (2003)

James Woodward's *Making Things Happen* is the canonical statement:

> *X* causes *Y* if and only if there are circumstances such that, if
> some (single) intervention that changes the value of *X* (and no other
> variable except through *X*) were to occur, then *Y* (or the probability
> distribution of *Y*) would change.

Key concepts:

- **Intervention**: an exogenous causal process that sets the value of
  *X* independently of *X*'s other causes, breaking the normal causal
  arrows into *X* (surgical idealization).
- **Invariance**: a causal generalization is invariant under some range
  of interventions; it continues to hold when the cause variable is
  manipulated in specified ways.
- **Modularity**: causal systems are modular: one can intervene on one
  component (one equation in a structural model) without disrupting others.

Woodward's account is non-reductive about intervention (an intervention
is itself a causal notion), but it is not viciously circular: the aim is
not to eliminate causal concepts but to illuminate their interconnections.

### 6.3 Strengths

| Strength | Explanation |
|---|---|
| Unifies reasoning across sciences | The interventionist framework applies equally in physics, biology, economics, epidemiology, and psychology. |
| Practical relevance | Directly connects to experimental design, policy evaluation, and causal inference methods (instrumental variables, RCTs). |
| Handles type and token causation | Invariance and intervention apply at both the type level (generalizations) and the token level (singular causal claims relativized to a model). |
| Natural fit with causal Bayes nets | Woodward's framework integrates tightly with Pearl's structural causal models and *do*-calculus. |
| Proportionality and specificity | The interventionist framework naturally handles questions about how specific a cause is and at what level of description it operates. |

### 6.4 Problems

| Problem | Description |
|---|---|
| Anthropocentrism | Is the notion of intervention tied to human agency? Woodward argues that interventions are abstract, not necessarily human-performed, but critics charge that the *concept* of manipulation remains inherently tied to our experience as agents. |
| Circularity worry | An intervention is itself defined in causal terms (it must not be caused by variables in the system in the usual way). Is this a benign interdependence or a vicious circle? |
| What counts as an intervention? | The boundaries of "possible intervention" are vague. Some causal relations may hold in principle but be inaccessible to any physically possible intervention. |
| Fundamental physics | Does the interventionist framework apply to causal relations at the fundamental physical level, where variables may not be independently manipulable? |

---

## 7. Primitivist / Non-Reductive Theories

### 7.1 Core Claim

Causation cannot be reductively analyzed in non-causal terms. It is a
basic, irreducible feature of reality—a conceptual or metaphysical
primitive.

### 7.2 Principal Variants

#### 7.2.1 Anscombe (1971): Causation as Basic

G.E.M. Anscombe argued that the concept of causation is learned directly
from experience (e.g., pushing, pulling, cutting) and is not derived from
observed regularities, counterfactuals, or probabilities:

- We perceive causation directly in action; we do not infer it from constant
  conjunction.
- The Humean project of reducing causation to something else rests on a
  mistaken epistemology.
- Causal concepts are as fundamental as any we possess; they are not
  constructed out of simpler materials.

#### 7.2.2 Maudlin (2007): Causation as Primitive

Tim Maudlin, in *The Metaphysics Within Physics*, argues that:

- Laws of nature are primitive and irreducible.
- Causation is a primitive relation tied to the fundamental dynamical laws.
- Causal direction is built into the time-asymmetric structure of
  fundamental physics (the Second Law of Thermodynamics, the Past
  Hypothesis).
- Attempts to reduce causation to non-causal facts (Humean supervenience)
  fail because the needed non-causal facts do not exist: the mosaic of
  local matters of particular fact is insufficient to ground causal or
  nomological structure.

### 7.3 Strengths

| Strength | Explanation |
|---|---|
| Avoids reductionist failures | By refusing to reduce causation to something else, primitivism avoids all the counterexamples that bedevil reductive analyses. |
| Phenomenological support | We seem to experience causation directly (resistance, effort, collision); primitivism honors this phenomenology. |
| Fits fundamental physics | If physics is irreducibly causal/nomological, then the project of eliminating causation from fundamental ontology is misguided. |
| Conceptual economy | Taking causation as primitive avoids the need for an elaborate (and contested) reductive apparatus of possible worlds, counterfactuals, or probability spaces. |

### 7.4 Problems

| Problem | Description |
|---|---|
| Explanatory regress | If causation is primitive, we cannot explain *what* causation is. The theory is a refusal to give a theory, which may be unsatisfying. |
| Lack of analysis | Philosophical analysis aims at understanding; primitivism offers no illumination of the internal structure of causation. |
| Application to special sciences | Primitivism gives little guidance about how to discover or confirm causal claims in biology, economics, or epidemiology. |
| Distinguishing causal from non-causal | If causation is primitive, how do we distinguish causal relations from other relations (spatial, temporal, logical)? The criteria, if any, must come from elsewhere. |

---

## 8. Agent / Agency Theories

### 8.1 Core Claim

The concept of causation is derived from our experience as agents. We
understand what it is for one thing to cause another because we understand
what it is to *make* something happen through our own actions.

### 8.2 Principal Variants

#### 8.2.1 von Wright (1971): Action and Causation

Georg Henrik von Wright, in *Explanation and Understanding*, argued:

- The concept of causation is rooted in the concept of human action.
- We learn what it means for A to cause B by experiencing ourselves as
  bringing about changes through bodily movements.
- Experimental science extends this agentive understanding through
  controlled manipulation, generalizing the "making things happen"
  model to systems we cannot directly control.

#### 8.2.2 Price and Menzies (1993): Agency Theory

Huw Price and Peter Menzies develop an explicitly agent-centered account:

- *A* causes *B* iff, if an agent had the capacity to bring about *A*
  as a means to bringing about *B*, and the agent's bringing about *A*
  would be an effective means of bringing about *B*.
- The account uses the notion of an "ideal agent" with direct voluntary
  control over *A* (a free-action idealization).
- The truth-conditions of causal claims are tied to facts about what
  ideal agents could achieve.

### 8.3 Strengths

| Strength | Explanation |
|---|---|
| Explains epistemic access | Our knowledge of causation is anchored in our experience as agents; the agency theory explains *how* we come to know causal relations. |
| Connects to experimental practice | Controlled experiments are systematic extensions of the agentive model: we "intervene" to see what happens. |
| Handles omissions | Agents routinely bring things about by *not* doing something; omission-causation is natural within an agential framework. |
| Practical and moral relevance | Causal responsibility in law and morality is closely tied to agency. |

### 8.4 Problems

| Problem | Description |
|---|---|
| Anthropocentrism | The analysis is tied to human (or agential) capacities; causation in the early universe, in distant galaxies, or in non-agential systems becomes conceptually dependent on us, which is metaphysically suspect. |
| Circularity | The notion of "bringing about" or "making happen" is already causal. If an agent "makes A happen," the analysis presupposes the very causal relation it seeks to explain. |
| Ideal agent idealization | The agency account relies on a highly idealized notion of an agent with perfect voluntary control; it is unclear how to ground this idealization without circularity. |
| Non-agential causation | Much causation involves no agent at all (tectonic plates causing earthquakes). The agency theory must explain how such non-agential causation is conceptually linked to agency without making it parasitic in a problematic way. |

---

## 9. Dispositional / Powers Theories

### 9.1 Core Claim

Causation is the manifestation of powers, dispositions, or capacities.
Objects have intrinsic causal properties (powers), and causation occurs
when these powers are triggered or manifested in the right circumstances.

### 9.2 Principal Variants

#### 9.2.1 Mumford and Anjum (2011): Powers Manifestation

Stephen Mumford and Rani Lill Anjum, in *Getting Causes from Powers*:

- Causation is a vector: causes dispose toward effects without necessitating
  them.
- Powers can combine, and the result of composition is not always additive;
  mutual manifestation partners can produce emergent outcomes.
- Causation is intrinsic, singular, and productive—not reducible to
  regularities or counterfactuals.
- The causal relation is a polyadic relation involving multiple powers
  and their mutual manifestation.

#### 9.2.2 Bird (2007): Dispositional Essentialism

Alexander Bird, in *Nature's Metaphysics*:

- Fundamental properties have dispositional essences: the nature of a
  property is exhausted by the causal/nomological role it plays.
- Laws of nature are not contingent regularities but flow necessarily
  from the essences of properties.
- Causal relations are grounded in the dispositional essences of
  properties; causation is a manifestation of the fundamental causal
  structure of the world.

#### 9.2.3 Other Powers Approaches

- **Cartwright** (see Section 4.2.2): causal capacities as measured but
  not reducible to probabilities.
- **Chakravartty**: semirealism about causal properties.
- **Ellis**: scientific essentialism with causal powers at the fundamental
  level.
- **Martin and Heil**: two-sided (dispositional and qualitative) nature of
  properties; causation involves the manifestation of dispositions.

### 9.3 Strengths

| Strength | Explanation |
|---|---|
| Modal force explained | The necessity or "oomph" of causation is explained by the very nature of properties: they are *for* producing certain outcomes. |
| Unifies with metaphysics of properties | Causation is integrated with a broader metaphysical picture of what properties are, rather than treated in isolation. |
| Handles singular causation naturally | The manifestation of a power is a local, individuated event—not dependent on regularities or type-level patterns. |
| Vectors and thresholds | Mumford and Anjum's vector model captures the idea that causes can contribute without being sufficient, and that causation can involve threshold effects. |

### 9.4 Problems

| Problem | Description |
|---|---|
| Still developing formal framework | Compared with counterfactual or probabilistic theories, powers theories lack a well-developed formal apparatus for discovery and inference. |
| Omissions again | How can an absence trigger or manifest a power? If causation is always the manifestation of a positive disposition, omissions remain puzzling. |
| Composition of powers | How do multiple powers interact? The mereology and dynamics of power composition are not fully understood and may reintroduce regularity or counterfactual elements. |
| Epistemology | How do we know what a property's dispositional essence is? The epistemology of powers may collapse into the epistemology of laws or regularities. |

---

## 10. Comparison Across Major Families

### 10.1 Summary Table: Core Definitions

| Theory Family | Core Definition of "C causes E" |
|---|---|
| Regularity | Events of type C are regularly followed by events of type E; C is an INUS condition for E. |
| Counterfactual | Had C not occurred, E would not have occurred (or: C influences whether/how/when E occurs). |
| Probabilistic | C raises the probability of E in causally homogeneous background contexts. |
| Process | C and E are connected by a spatiotemporally continuous process transmitting a conserved quantity. |
| Interventionist | There is a possible intervention on C that changes E (or the probability distribution of E). |
| Primitivist | Causation is a basic, irreducible relation; no non-circular definition is possible. |
| Agency | An ideal agent could bring about E by bringing about C as a means. |
| Powers | C's powers/dispositions manifest to produce E. |

### 10.2 Summary Table: Problem Handling

| Problem | Regularity | Counterfactual | Probabilistic | Process | Interventionist | Powers |
|---|---|---|---|---|---|---|
| Early preemption | Poor | Fair (influence) | Fair | Good | Good | Fair |
| Late preemption | Poor | Good (influence) | Fair | Good | Good | Fair |
| Overdetermination | Fair | Poor | Fair | Fair | Fair | Fair |
| Trumping | Poor | Poor | Poor | Good | Fair | Fair |
| Omissions | Poor | Good | Fair | Poor | Good | Poor |
| Mental causation | Poor | Fair | Fair | Poor | Fair | Good |
| Spurious correlation | Poor | Fair | Good | Fair | Good | Fair |
| Simpson's paradox | Poor | Fair | Good | Fair | Good | Fair |
| Indeterministic causation | Poor | Fair | Good | Poor | Good | Good |
| Singular causation | Fair | Good | Poor | Good | Good | Good |

---

## 11. Special Topics

### 11.1 Mental Causation and the Exclusion Problem

Mental causation is the thesis that mental events (beliefs, desires,
intentions) cause physical events (bodily movements) and other mental
events. It faces the **exclusion problem** (Kim, 1998):

1. Every physical event has a sufficient physical cause (causal closure
   of the physical).
2. If a mental event M causes a physical event P, then P has both a mental
   cause M and a physical cause P*.
3. Unless M is identical to P* (reductive physicalism), we have causal
   overdetermination.
4. Systematic causal overdetermination is implausible.
5. Therefore, either mental causation is epiphenomenal (no genuine mental
   causation) or mental events reduce to physical events.

Responses include: identity theory, functionalism (mental causation via
functional role rather than intrinsic properties), counterfactual
dependence (Yablo's proportionality), interventionist accounts, and
powers-based emergentism (mental properties are emergent causal powers).
The exclusion problem is a stress test for any theory of causation that
aims to cover all domains.

### 11.2 Causation by Absence/Omission

Absences—things that do not happen—seem to cause events: the gardener's
failure to water the plant causes it to die; the omission of a safety
check causes an accident. Theories vary sharply in their ability to
accommodate absence causation:

- **Regularity theories**: struggle; absences are not events and cannot
  figure in constant conjunctions directly.
- **Counterfactual theories**: natural fit; "had the gardener watered the
  plant, it would not have died" is a standard counterfactual.
- **Process theories**: struggle severely; there is no physical process
  connecting a non-event to an event.
- **Interventionist theories**: can accommodate via counterfactuals about
  interventions on whether an event occurs.
- **Powers theories**: struggle; an absence does not seem to be a power
  or disposition (though some argue absences enable or fail to block the
  manifestation of other powers).

### 11.3 Causal Overdetermination

Overdetermination occurs when multiple causes each suffice for an effect.
Classic case: two assassins simultaneously shoot the victim; either shot
alone would have been fatal. Varieties:

- **Symmetric overdetermination**: two causally independent sufficient
  causes both operate.
- **Asymmetric overdetermination**: a sufficient cause operates while a
  backup sufficient cause is preempted (preemption cases are sometimes
  classified as overdetermination variants).
- **Constitutional overdetermination**: a whole and its parts are each
  causally relevant to the same effect.

Overdetermination is a problem for theories that require necessity (e.g.,
simple counterfactual dependence) because neither cause is necessary for
the effect. It also raises questions about whether overdetermination is
widespread in a way that threatens the plausibility of non-reductive
mental causation (see Section 11.1).

### 11.4 Transitivity of Causation

Is causation transitive? If *a* causes *b* and *b* causes *c*, does *a*
cause *c*?

- **Lewis**: built transitivity into the definition (causation = ancestral
  of causal dependence).
- **Intuitive counterexamples**: Hall's "double prevention" cases—a boulder
  tumbling toward a house is prevented by a hiker's ducking, but does the
  ducking cause the house to remain intact? Intuitions differ.
- **Formal approaches**: structural equation models can represent
  transitive and non-transitive causal chains and may allow counterexamples.
- **Relevance to exclusion**: if mental-to-physical causation is transitive,
  and every mental event that causes a physical event must itself be caused
  by a physical event, the threat of widespread causal overdetermination
  intensifies.

### 11.5 Causation in the Special Sciences

Causal claims in biology, psychology, economics, and sociology face
distinctive challenges:

- **Multiple realizability**: a single higher-level cause (e.g., pain)
  may be realized by many different physical states. Does "pain causes
  withdrawal behavior" pick out a genuine causal relation, or is all
  causation at the physical level?
- **Proportionality (Yablo)**: the cause should be specified at the right
  level of description—not too specific (this exact neural firing pattern)
  nor too general (some neural state or other). The "right" level is the
  one that makes a difference to the effect.
- **Causal relevance vs. causal mechanism**: in the special sciences, we
  often identify causes (smoking causes cancer) without identifying the
  complete physical mechanism. Must a full causal account include the
  mechanism?
- **Higher-level causation and exclusion**: if the physical realm is
  causally closed, and higher-level properties are not identical to
  physical properties, how do higher-level causes earn their keep?

Manipulationist and interventionist theories are particularly well-suited
to the special sciences because they tie causation to invariance under
intervention, which can be assessed at any level of description without
requiring full knowledge of underlying mechanisms.

---

## 12. Glossary of Key Terms

| Term | Definition |
|---|---|
| **Ancestral** | The ancestral of a relation R is the relation that holds between *a* and *b* iff there is a finite chain of R-steps from *a* to *b*. |
| **Causal Bayes net** | A directed acyclic graph representing causal relations, with edges indicating direct causation and conditional independence constraints encoded by the Markov condition. |
| **Causal dependence** | *e* counterfactually depends on *c* iff had *c* not occurred, *e* would not have occurred. |
| **Conserved quantity** | A physical quantity governed by a conservation law (mass-energy, momentum, charge, etc.); central to Dowe's process theory. |
| **Counterfactual** | A conditional of the form "If A were the case, C would be the case," evaluated by considering the closest possible worlds where A holds. |
| **Dispositional essence** | The thesis that a property's identity is exhausted by its causal or dispositional profile. |
| **Early preemption** | The backup cause is cut off before it can act; the actual cause preempts it early. |
| **Exclusion problem** | The problem that mental causation seems to be excluded by the causal closure of the physical domain, leading to overdetermination or epiphenomenalism. |
| **INUS condition** | An Insufficient but Necessary part of an Unnecessary but Sufficient condition (Mackie). |
| **Intervention** | An idealized exogenous manipulation that sets the value of a variable independently of its normal causes (Woodward). |
| **Invariance** | A generalization is invariant under interventions if it continues to hold when the cause variable is manipulated in the specified ways. |
| **Late preemption** | The actual cause and the backup cause both operate, but the actual cause reaches the effect first. |
| **Mark transmission** | Salmon's criterion: a causal process is one that can transmit a local modification (mark) to later stages. |
| **Markov condition** | In a causal DAG, every variable is conditionally independent of its non-descendants given its direct causes (parents). |
| **Multiple realizability** | The thesis that a higher-level property or kind can be realized by many different lower-level physical configurations. |
| **Omission** | A failure to act or the absence of an event, which is nonetheless cited as a cause. |
| **Overdetermination** | Multiple causes each suffice independently for an effect; the effect is "overdetermined." |
| **Preemption** | A backup process is poised to bring about an effect but is preempted by the actual cause. |
| **Proportionality** | The requirement that a cause be specified at the right level of generality—neither too specific nor too broad (Yablo). |
| **Screening off** | Variable *a* screens off *c* from *e* if conditioning on *a* renders *c* probabilistically irrelevant to *e*. |
| **Simpson's paradox** | A trend appearing in several groups of data reverses when the groups are combined; central challenge for probabilistic theories. |
| **Supervenience** | A set of properties A supervenes on B iff no two possible worlds differ in A without differing in B. Humean supervenience: all facts supervene on the mosaic of local particular facts. |
| **Trumping** | One cause overrides another in virtue of a higher-order rule (e.g., rank), not in virtue of preemption. |
| **Vector model** | Mumford and Anjum's model of causation as a vector-like contribution: causes dispose toward effects with varying strength and can compose in non-additive ways. |

---

## 13. Principal Sources and Further Reading

- Anscombe, G.E.M. (1971). *Causality and Determination*. Cambridge University Press.
- Bird, A. (2007). *Nature's Metaphysics: Laws and Properties*. Oxford University Press.
- Cartwright, N. (1989). *Nature's Capacities and Their Measurement*. Oxford University Press.
- Collins, J., Hall, N., & Paul, L.A. (eds.) (2004). *Causation and Counterfactuals*. MIT Press.
- Dowe, P. (2000). *Physical Causation*. Cambridge University Press.
- Eells, E. (1991). *Probabilistic Causality*. Cambridge University Press.
- Hall, N. (2004). "Two Concepts of Causation." In Collins, Hall, & Paul (2004).
- Hume, D. (1739). *A Treatise of Human Nature*.
- Hume, D. (1748). *An Enquiry Concerning Human Understanding*.
- Kim, J. (1998). *Mind in a Physical World*. MIT Press.
- Lewis, D. (1973). "Causation." *Journal of Philosophy* 70: 556-567.
- Lewis, D. (2000). "Causation as Influence." *Journal of Philosophy* 97: 182-197.
- Mackie, J.L. (1965). "Causes and Conditions." *American Philosophical Quarterly* 2: 245-264.
- Mackie, J.L. (1974). *The Cement of the Universe*. Oxford University Press.
- Maudlin, T. (2007). *The Metaphysics Within Physics*. Oxford University Press.
- Menzies, P. & Price, H. (1993). "Causation as a Secondary Quality." *British Journal for the Philosophy of Science* 44: 187-203.
- Mill, J.S. (1843). *A System of Logic*.
- Mumford, S. & Anjum, R.L. (2011). *Getting Causes from Powers*. Oxford University Press.
- Pearl, J. (2000). *Causality*. Cambridge University Press.
- Pearl, J. (2009). *Causality*, 2nd edition. Cambridge University Press.
- Salmon, W. (1984). *Scientific Explanation and the Causal Structure of the World*. Princeton University Press.
- Schaffer, J. (2005). "Contrastive Causation." *Philosophical Review* 114: 327-358.
- Skyrms, B. (1980). *Causal Necessity*. Yale University Press.
- Spirtes, P., Glymour, C., & Scheines, R. (1993). *Causation, Prediction, and Search*. Springer.
- Suppes, P. (1970). *A Probabilistic Theory of Causality*. North-Holland.
- von Wright, G.H. (1971). *Explanation and Understanding*. Cornell University Press.
- Woodward, J. (2003). *Making Things Happen: A Theory of Causal Explanation*. Oxford University Press.
- Yablo, S. (1992). "Mental Causation." *Philosophical Review* 101: 245-280.

---

*This taxonomy is maintained for use with phil-causation-analyze. Last updated: July 2026.*
