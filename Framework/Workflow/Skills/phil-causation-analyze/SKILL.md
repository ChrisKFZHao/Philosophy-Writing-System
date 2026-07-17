---
name: phil-causation-analyze
description: "Causal Claim Analysis — identify theoretical affiliations of causal claims; evaluate Humean vs anti-Humean readings; detect causal exclusion and overdetermination problems"
---

# Causal Claim Analysis

## Overview

Causal claims in philosophical arguments are theory-laden — they presuppose a particular theory of causation whether the author acknowledges it or not. An argument that relies on the claim "smoking causes cancer" may implicitly presuppose a regularity theory (smoking is regularly followed by cancer), a counterfactual theory (if one hadn't smoked, one wouldn't have developed cancer), a probabilistic theory (smoking raises the probability of cancer), a process theory (there is a spatiotemporally continuous causal process connecting smoking to cancer), or a powers-based theory (nicotine has the causal power to induce carcinogenic changes). The truth-conditions, inferential implications, and dialectical force of the argument shift depending on which theory of causation is presupposed.

This skill identifies the implicit causal theory underlying an argument's causal claims, diagnoses its adequacy for the argument's purposes, detects classic causal problems (exclusion, overdetermination, preemption, absence causation, causal transitivity failures), and evaluates whether alternative causal theories would undermine or strengthen the argument. It answers the question: "When the argument claims that A causes B, what does 'causes' mean here, and does that meaning support the work the argument demands of it?"

The skill is essential within the metaphysics pipeline because causation is not a univocal concept — it admits of radically different analyses with different logical properties. An argument that succeeds under a regularity theory of causation may collapse under a counterfactual theory, and vice versa. Detecting the theoretical commitments latent in causal language is therefore a prerequisite for evaluating any argument that draws causal inferences.

## Input

**Required:**
- `argument-reconstruction report` (from `phil-argument-reconstruct`): Provides the argument in standard premise-conclusion form, including the logical structure of causal premises and the inferential role that causal claims play within the argument. The reconstruction report identifies where causal claims appear and how they function in the argument's inferential structure.

**Optional:**
- `original text`: The source material from which the argument was extracted. Particularly useful when causal language is embedded in background context that does not survive standard-form reconstruction — e.g., hedging language ("tends to cause," "contributes to"), scope qualifiers ("in normal conditions," "other things being equal"), and implicit causal metaphors ("drives," "produces," "brings about").
- `ontological-commitment report` (from `phil-ontological-commitment`): Causal claims interact with ontological commitments. If the argument commits to events as causal relata, it imposes constraints on which causal theories are viable. Conversely, if the argument presupposes a causal theory that requires a specific ontology of relata (e.g., trope causation requires tropes), the ontological commitment report reveals whether the argument's ontology can support the causal theory.

## Output

**Causal Claim Analysis Report** — structured analysis containing the following sections:

### Section 1: Causal Claim Catalog

A numbered list (CC1, CC2, ..., CCn) cataloging every causal claim in the argument. Each entry contains:

| Field | Description |
|-------|-------------|
| `claim_id` | Unique identifier: CC1, CC2, ..., CCn |
| `causal_locution` | The exact causal language used in the source: "causes," "produces," "brings about," "leads to," "is responsible for," "because" (causal sense), "due to," "owing to," "makes it the case that" |
| `cause_relatum` | The entity designated as cause: its type (event, fact, property, object, omission, process, state, agent) and its specification as it appears in the argument |
| `effect_relatum` | The entity designated as effect: same type specification |
| `relata_type_diagnosis` | Classification of both relata according to the taxonomy (event, fact, property, object, omission, process, state, agent), with justification from the argument's language |
| `structural_role` | How this causal claim functions in the argument: `direct_premise` (stated as a premise), `inferred_conclusion` (the conclusion is a causal claim), `suppressed_premise` (implicitly required for the inference to go through), `auxiliary` (background causal assumptions not central to the inference) |

### Section 2: Causal Theory Diagnosis

Diagnosis of which theory of causation the argument presupposes, with evidence:

| Field | Description |
|-------|-------------|
| `primary_theory` | The dominant theory of causation presupposed by the argument: `regularity`, `counterfactual`, `probabilistic`, `process`, `interventionist`, `primitivist`, `powers-based`, `agency`, `difference-making`, `INUS`, `mechanistic`, or `hybrid`/`underdetermined` |
| `evidence` | Specific textual and inferential evidence for the diagnosis: which features of the argument's causal claims, modal language, counterfactual reasoning, or methodological assumptions point to this theory? |
| `secondary_theories` | Other theories that the argument seems to draw on in subsidiary or inconsistent ways; flag theory-switching where detected |
| `humean_anti_humean` | Classification as `Humean` (causation reduces to non-causal facts — regularities, counterfactuals, probabilities), `anti-Humean` (causation is irreducible — powers, production, primitivism), or `neutral`/`ambivalent` |
| `relata_constraints` | What types of relata the presupposed theory requires: regularity theories work best with event-types; counterfactual theories with events or facts; powers theories with objects bearing properties; process theories with spatiotemporally continuous processes. Does the argument's relatum-ontology match the presupposed theory? |

### Section 3: Theory-Adequacy Assessment

Assessment of whether the presupposed causal theory supports the inferences the argument draws:

- **Inference audit**: For each causal claim, determine whether the presupposed theory's truth-conditions for "A causes B" are satisfied by the evidence the argument provides. If the argument asserts "A causes B" as a premise but provides no evidence meeting the theory's criteria, this is a gap.
- **Modal strength check**: Does the argument draw conclusions that require a modal strength (necessity, counterfactual robustness, lawlikeness) that the presupposed theory cannot deliver? Regularity theories support only contingent generalization; counterfactual theories support context-sensitive dependence; powers theories support metaphysical necessity. Mismatch indicates a theory-adequacy failure.
- **Transitivity assessment**: Does the argument rely on causal transitivity (A causes B, B causes C, therefore A causes C)? Different theories license transitivity to different degrees. Process theories (salmon/dowe) typically support transitivity; counterfactual theories do not in general (Lewis's early/late preemption cases); probabilistic theories support only qualified transitivity.
- **Causal selection critique**: Does the presupposed theory provide resources for distinguishing genuine causes from background conditions? If the argument selects one factor as "the cause" from a complex causal field and the presupposed theory treats all causal factors symmetrically, this is a selection problem.

### Section 4: Problem Detection

Systematic detection of classic causal problems:

| Problem | Detection Protocol |
|---------|-------------------|
| **Causal Exclusion** | Does the argument posit multiple causes for a single effect where one cause is physical and another is mental (or higher-level)? Apply Kim's exclusion argument: if physical cause P is sufficient for effect E, and mental cause M is distinct from P, then either M is excluded (epiphenomenalism) or M=P (reduction) or there is systematic overdetermination. Flag any argument that posits mental causation without addressing exclusion. |
| **Causal Overdetermination** | Are two or more causes each claimed to be sufficient for the same effect? Distinguish benign overdetermination (firing squad cases — both bullets would have been sufficient) from systematic overdetermination (every mental cause overdetermines its physical effect, which is widely held to be implausible). Assess whether the argument acknowledges the overdetermination and provides a response. |
| **Causal Preemption** | Does the argument's theory of causation handle preemption — cases where a backup cause would have produced the effect had the actual cause not done so? Counterfactual theories notoriously struggle with early and late preemption. If the argument presupposes a counterfactual theory and draws conclusions from causal claims about which factor "actually caused" an outcome in a preemption-like scenario, flag the vulnerability. |
| **Absence Causation** | Does the argument treat absences (omissions, lacks, non-occurrences) as causes? "The drought caused the famine" — the drought is an absence of rain. Not all theories accommodate absence causation: regularity theories can handle it (regular connection between absences and outcomes); process theories cannot (an absence is not a spatiotemporally continuous process); powers theories struggle (absences lack causal powers). Flag any gap between the argument's reliance on absence causation and the presupposed theory's capacity to accommodate it. |
| **Causal Transitivity Failure** | Does the argument rely on a chain of causal inferences? Map the chain and check whether the presupposed theory licenses each transitivity step. Flag any step where the theory does not guarantee transitivity. |
| **Causal Circularity** | Does the argument define cause in terms of effect and effect in terms of cause, creating a circle? Flag circular definitions that render the causal analysis uninformative. |

### Section 5: Alternative Theoretical Readings

For each causal claim, evaluate whether the argument would survive reinterpretation under a different theory of causation:

- **Counterfactual reading**: If the argument currently presupposes a regularity theory, what happens if reinterpreted counterfactually? Does the argument's evidence support the required counterfactuals? Would the counterfactual reading introduce preemption problems?
- **Probabilistic reading**: What happens if "A causes B" is reinterpreted as "A raises the probability of B"? Does this weaken or strengthen the argument's conclusions?
- **Powers-based reading**: What happens if causation is reinterpreted in terms of the manifestation of causal powers? This typically strengthens modal conclusions (powers support necessity claims) but introduces ontological commitments (powers are entities in their own right).
- **Interventionist reading**: What happens if causation is reinterpreted in terms of Woodward's interventionist framework (X causes Y iff there is a possible intervention on X that changes Y)? This supports causal inference in epistemology but requires well-defined variables and an intervention concept.
- **Primitivist reading**: What happens if causation is taken as a metaphysical primitive not reducible to anything else? This avoids reduction problems but abandons explanatory ambitions — the argument can no longer explain what causation consists in.

For each alternative reading, assess: (a) does the argument's evidence still support the causal claim under this reading? (b) does the conclusion still follow? (c) does the alternative reading introduce new problems the original reading avoided?

## Methodological Foundations

This skill draws on eight foundational sources in the philosophy of causation, spanning Humean, anti-Humean, and interventionist traditions:

1. **Hume (1739/1748) "A Treatise of Human Nature" / "An Enquiry Concerning Human Understanding"** — The classical regularity theory of causation. Hume argues that causation consists in constant conjunction, temporal priority, and contiguity, and that necessary connection is a projection of the mind. The Humean framework establishes the reductionist paradigm: causation is nothing over and above non-causal facts. The distinction between Humean reductionism (causation reduces to non-causal facts) and anti-Humean realism (causation is irreducible or involves real necessary connections) structures the entire field.

2. **Lewis (1973) "Causation" / Lewis (2000) "Causation as Influence"** — The counterfactual theory of causation: event C causes event E iff C and E are distinct actual events and the counterfactual "if C had not occurred, E would not have occurred" is true. Lewis's analysis in terms of possible worlds and comparative similarity provides rigorous truth-conditions. The 2000 revision to "causation as influence" addresses preemption problems. Key concepts: counterfactual dependence, possible worlds, similarity metric, transitivity failures, early and late preemption.

3. **Woodward (2003) "Making Things Happen: A Theory of Causal Explanation"** — The interventionist theory: X causes Y iff there is a possible intervention on X (an ideal experimental manipulation that changes X independently of its other causes) that changes Y (or the probability distribution of Y). Woodward's framework is designed to capture the epistemology of causal inference in science, emphasizing invariance, modularity, and the role of interventions in distinguishing causation from mere correlation.

4. **Salmon (1984) "Scientific Explanation and the Causal Structure of the World" / Dowe (2000) "Physical Causation"** — Process theories of causation: causal processes are spatiotemporally continuous world-lines that transmit a conserved quantity (energy, momentum, charge in Dowe's formulation). Causal interactions are intersections of world-lines where conserved quantities are exchanged. Process theories provide a physicalist account of causation compatible with the special sciences but challenged by absence causation and higher-level causation.

5. **Kim (1998) "Mind in a Physical World"** — The causal exclusion argument. Kim argues that if every physical event has a sufficient physical cause (causal closure of the physical) and mental events are distinct from physical events (non-reductive physicalism), then mental causation is excluded — mental events are either epiphenomenal, identical to physical events, or they systematically overdetermine physical effects. The exclusion problem is the central challenge for non-reductive physicalism and any argument positing mental or higher-level causation.

6. **Mumford & Anjum (2011) "Getting Causes from Powers"** — The powers-based (dispositionalist) theory of causation. Causation occurs when powers (dispositions, capacities) manifest themselves, producing their characteristic manifestations. Powers are irreducible, modal properties of objects that necessitate (or dispose toward) their manifestations when stimulus conditions obtain. This anti-Humean framework treats causation as a real, productive relation grounded in the nature of the entities involved.

7. **Pearl (2009) "Causality: Models, Reasoning, and Inference"** — The structural causal model (causal Bayes nets) framework. Causal relationships are represented as directed acyclic graphs where arrows represent direct causal influence, and the joint probability distribution factorizes according to the graph structure. The `do`-calculus formalizes the distinction between observing and intervening. Pearl's framework provides mathematically rigorous tools for causal inference from observational and experimental data, closely related to Woodward's interventionism.

8. **Schaffer (2016) "The Metaphysics of Causation" (Stanford Encyclopedia)** — A comprehensive survey of the metaphysics of causation that systematizes the distinctions between theories, identifies the core problems (preemption, absence causation, transitivity, overdetermination, the relata question), and maps the dialectical landscape. Essential for orienting causal analysis within the broader metaphysical terrain.

## Steps

### Step 1: Extract All Causal Claims and Identify Causal Relata

Scan the argument reconstruction report (and original text if available) for all instances of causal language. The extraction must be exhaustive — every causal relation asserted, presupposed, or relied upon must be cataloged.

**Detection protocol — scan for the following causal locutions:**

Direct causal verbs:
- "causes," "is a cause of," "is the cause of"
- "produces," "brings about," "gives rise to," "generates," "creates"
- "leads to," "results in," "eventuates in"
- "affects," "influences," "impacts"
- "determines," "makes happen," "is responsible for"

Causal prepositions and connectives:
- "because" (in its causal, not just rationalizing, sense — test: would "causes" be a plausible substitution?)
- "due to," "owing to," "in virtue of" (causal sense)
- "by" (causal instrumental: "by doing X, Y occurs")
- "as a result of," "as a consequence of"
- "makes it the case that," "is what makes"

Causal nominalizations:
- "the cause of," "the effect of," "the result of"
- "causation," "causality," "causal relation"
- "causal power," "causal capacity," "causal mechanism"

Causal metaphors (flag these — they may indicate causal commitment without explicit causal verbs):
- "drives," "fuels," "underlies," "grounds" (if used causally rather than metaphysically)
- "triggers," "sparks," "sets off," "unleashes"

**For each detected causal claim, identify the relata (cause and effect) and their type:**

The relata type taxonomy — what kind of entity stands as cause and effect:

| Relatum Type | Definition | Detection Clue | Example |
|-------------|------------|----------------|---------|
| `event` | A dated, located particular occurrence | The argument uses event-language: "the explosion," "the collapse," "Socrates' death" | "The short circuit caused the fire" — both are events |
| `fact` | A true proposition, a state of affairs that obtains | The argument uses that-clauses: "the fact that...," "S's being F" | "The fact that the bridge had a structural flaw caused its collapse" |
| `property` | A way a thing is — a property, quality, or attribute | The argument uses property-instance language: "the mass of," "the charge of," "the temperature of" | "The solubility of the salt caused it to dissolve" |
| `object` | A concrete particular substance or thing | The argument attributes causal efficacy directly to objects: "the rock broke the window" | "The rock broke the window" — agents or objects as causes |
| `omission` | An absence, a failure to act, a non-occurrence | The argument uses negative causal language: "failure to," "lack of," "absence of," "not Xing" | "The failure to water the plant caused it to die" |
| `process` | An extended, temporally continuous occurrence | The argument uses process-language: "erosion," "natural selection," "globalization" | "Erosion caused the canyon to form" |
| `state` | A persisting condition or a standing state of affairs | The argument uses state-language: "being in a state of," "the condition of" | "The patient's weakened immune state caused the infection" |
| `agent` | A person or conscious being acting intentionally | The argument uses agent-language and attributes causal responsibility to persons | "Brutus caused Caesar's death by stabbing him" |
| `variable` | A variable taking values; typically in interventionist or probabilistic frameworks | The argument uses variable-language: "X causes Y" where X and Y are variable names | "Smoking (X=1) causes lung cancer (Y=1)" |

**Important diagnostic questions for each claim:**
- Is the argument clear about what it takes causal relata to be, or does it slide between event-language and fact-language? (This slip is common and theoretically significant — event-causation and fact-causation have different logical properties.)
- Does the argument attribute causal efficacy to absences? If yes, flag this for Step 4 (absence causation analysis).
- Are the relata fine-grained or coarse-grained? (Fine-grained: "Socrates' drinking hemlock at dusk on that specific occasion"; coarse-grained: "drinking hemlock causes death.")

**Output**: A complete causal claim catalog (CC1 through CCn) with each claim's causal locution, cause relatum (type and specification), effect relatum (type and specification), and structural role in the argument. The catalog should include even causal claims that appear only in the background or as auxiliary assumptions — these may become relevant in Steps 2 and 4.

### Step 2: Diagnose Implicit Causal Theory

Determine which theory of causation the argument presupposes. This is the core diagnostic step: the argument rarely explicitly states its theory of causation, so the theory must be inferred from the argument's causal language, the inferential demands it places on causal claims, and its methodological commitments.

**The theory taxonomy — diagnostic indicators for each theory:**

| Theory | Diagnostic Indicators |
|--------|----------------------|
| **Regularity (Humean)** | The argument appeals to constant conjunction or observed regularities without invoking counterfactuals or mechanisms. Causal claims are supported by citing repeated past co-occurrence. The argument treats causation as a contingent generalization — no talk of necessity, production, or mechanisms. Humean: causation reduces to non-causal facts. |
| **Counterfactual (Lewisian)** | The argument uses counterfactual language: "if X had not occurred, Y would not have occurred." Causal claims are supported or challenged by counterfactual reasoning. The argument appeals to possible worlds or similarity metrics (explicitly or implicitly). The argument distinguishes causation from mere correlation by invoking what would have happened. |
| **Probabilistic** | The argument uses probabilistic language: "raises the probability of," "makes more likely," "is a risk factor for." Causal claims are understood as probabilistic relevance — A causes B iff P(B|A) > P(B|not-A) (possibly with screening-off conditions). The argument may appeal to statistical evidence without claiming deterministic causation. |
| **Process (Salmon/Dowe)** | The argument appeals to mechanisms, physical connections, or continuous transmission of influence. Causal claims are supported by describing the mechanism or spatiotemporal path from cause to effect. The argument treats causation as a physical process and may express skepticism about causation at a distance or causation by absences. |
| **Interventionist (Woodwardian)** | The argument uses intervention-language: "if we intervene to change X, Y changes." The argument appeals to experimental manipulation or invariance under intervention. The argument distinguishes causation from correlation by the possibility of intervention. Variables are well-defined and the argument considers what would happen under hypothetical experiments. |
| **Powers-based / Dispositionalist** | The argument uses powers-language: "has the power to," "disposed to," "capable of producing." Causation is explained in terms of the natures or essences of the objects involved. The argument may appeal to necessary connections grounded in the nature of the relata. Anti-Humean: causation involves real productive relations. |
| **Primitivist** | The argument treats causation as conceptually or metaphysically basic — not analyzable in other terms. The argument uses causal language without attempting to reduce it or explain what it consists in. May be explicit (Anscombe-style: causation is a fundamental category we grasp directly) or implicit (the argument simply assumes we know what "causes" means and never analyzes it). |
| **INUS (Mackie)** | The argument treats causes as Insufficient but Necessary parts of Unnecessary but Sufficient conditions. The argument analyzes causation in terms of complex conditional structures. The argument distinguishes causes from background conditions using INUS logic. |
| **Mechanistic** | The argument appeals to mechanisms as organized systems of entities and activities producing regular changes. Causation is explained by describing the mechanism — its component parts, their organization, and their activities. Common in philosophy of biology and neuroscience. The argument treats mechanistic explanation as the paradigm of causal understanding. |
| **Agency / Manipulability** | The argument ties causation to our experience as agents: we understand causation through our capacity to bring things about. The argument appeals to what we can do or make happen. Associated with von Wright, Menzies & Price, and the agency theory of causation. |

**Diagnostic procedure:**

1. **Lexical scan**: Tabulate all causal vocabulary in the argument. The word choice is the strongest single diagnostic indicator. Counterfactual conditionals ("would have," "if...had not...") strongly suggest counterfactual theory. Powers language ("power to," "disposed to," "virtue of") strongly suggests powers theory. Probabilistic language ("probability," "risk," "likelihood") strongly suggests probabilistic theory.

2. **Inferential scan**: Examine what the argument does with its causal claims. Does it treat "A causes B" as supporting "if A had been absent, B would have been absent"? That is counterfactual reasoning. Does it treat "A causes B" as supporting "P(B|A) > P(B)"? That is probabilistic reasoning. Does it treat "A causes B" as supporting a claim about the transfer of a conserved quantity? That is process reasoning. The inferential demands the argument places on its causal claims reveal the theory it implicitly assumes.

3. **Methodological scan**: Does the argument use experimental evidence? (Suggests interventionist or probabilistic theory.) Does it use conceptual analysis? (Suggests counterfactual or primitivist theory.) Does it use mechanistic decomposition? (Suggests mechanistic theory.) Does it appeal to the nature or essence of things? (Suggests powers theory.)

4. **Consistency check**: Does the argument consistently presuppose one theory, or does it shift between theories? Theory-shifting is a significant finding: an argument that uses regularity language in one premise and counterfactual language in another may be equivocating on "causes." Flag any inconsistency.

5. **Relata compatibility check**: The presupposed theory imposes constraints on what kinds of entities can stand as causes and effects. Process theories require spatiotemporally located relata (events, processes); fact-causation is a poor fit for process theories. Counterfactual theories work well with events or facts; object-causation (objects as direct causes without mediating events) requires a powers-based or primitivist reading. Check whether the argument's relatum-ontology is compatible with the diagnosed theory. If not, the diagnosis may need refinement, or the argument may contain a relata-theory mismatch that should be flagged.

**Output**: A theory diagnosis specifying the primary theory, the evidential basis for the diagnosis (citing specific lexical, inferential, and methodological indicators), any secondary or inconsistent theory commitments, the Humean/anti-Humean classification, and any relata-theory compatibility issues.

### Step 3: Assess Theory Adequacy

Determine whether the presupposed causal theory adequately supports the inferential work the argument demands of its causal claims. A theory-adequacy failure is a structural flaw: the argument needs causation to have property P (e.g., transitivity, necessity, asymmetry), but the theory it presupposes either does not guarantee P or actively denies P.

**The adequacy assessment has four dimensions:**

#### Dimension 1: Inference-Premise Adequacy

For each causal claim that appears as a premise, determine whether the argument provides evidence sufficient to establish that claim under the presupposed theory's truth-conditions.

- Under a **regularity theory**: To establish "A causes B," the argument must provide evidence of constant conjunction — A and B co-occur with regularity. If the argument cites a single instance without establishing a pattern, the premise is not supported.
- Under a **counterfactual theory**: To establish "A causes B," the argument must support the counterfactual "if A had not occurred, B would not have occurred." This requires evidence about the nearest possible worlds or relevant alternatives. If the argument merely asserts a causal relation without engaging with counterfactuals, the premise is unsupported.
- Under a **process theory**: To establish "A causes B," the argument must identify a spatiotemporally continuous process transmitting a conserved quantity from A to B. If the argument posits causation without describing a mechanism or process, the premise is unsupported.
- Under a **powers theory**: To establish "A causes B," the argument must show that A (or its constituents) possesses a power whose manifestation is B, and that the relevant stimulus conditions obtained. If the argument merely observes correlation without identifying powers, the premise is unsupported.
- Under an **interventionist theory**: To establish "A causes B," the argument must identify a possible intervention on A (independent of A's other causes) that changes B. If no plausible intervention can be identified (e.g., because the variables are not well-defined or cannot be independently manipulated), the premise is unsupported.

**Assessment procedure**: For each causal premise, articulate the truth-conditions imposed by the presupposed theory. Then compare the evidence the argument provides against those truth-conditions. Rate: `adequately_supported`, `partially_supported`, `unsupported`, or `inapplicable` (the premise does not make a causal claim).

#### Dimension 2: Inference-Conclusion Adequacy

Determine whether the argument's conclusion follows from the premises given the logical properties of causation under the presupposed theory.

Key logical properties to check:

- **Asymmetry**: If the argument concludes "A causes B," does the presupposed theory guarantee the asymmetry of causation (if A causes B, B does not cause A)? Regularity theories do not guarantee asymmetry without additional constraints (temporal priority); counterfactual theories guarantee asymmetry through the direction of counterfactual dependence but face challenges from backtracking counterfactuals; process theories guarantee asymmetry through the direction of physical processes; probabilistic theories guarantee asymmetry through temporal screening-off.

- **Transitivity**: If the argument chains causal inferences (A causes B, B causes C, therefore A causes C), does the presupposed theory license transitivity? Process theories generally support transitivity; counterfactual theories have well-known failures (preemption cases where A causes B and B causes C but A does not cause C because C's counterfactual dependence on A is broken by an intermediate preempting cause); probabilistic theories support qualified transitivity only with Markov conditions.

- **Causal sufficiency**: If the argument claims that A is sufficient for B, does the presupposed theory deliver sufficiency? Regularity theories deliver only contingent sufficiency (in the circumstances, A is followed by B); powers theories deliver metaphysical sufficiency (given the nature of A, B must follow). If the argument needs metaphysical sufficiency but presupposes a regularity theory, there is an adequacy gap.

#### Dimension 3: Modal Adequacy

Assess the modal strength of the argument's causal claims and whether the presupposed theory can deliver it:

- **Contingent causal claims** ("A causes B in this situation but might not in others"): Any theory can accommodate these.
- **Nomic causal claims** ("A causes B as a matter of natural law"): Regularity theories can accommodate (laws are regularities); powers theories can accommodate (laws are grounded in powers); counterfactual theories require additional machinery (Lewis's best-system account of laws).
- **Metaphysically necessary causal claims** ("A necessarily causes B in all possible worlds in which A exists"): Only powers theories (grounded in essences) and some primitivist theories can deliver metaphysical necessity. Regularity theories and counterfactual theories cannot — causation is a contingent feature of the actual world and its nearest alternatives, not all possible worlds.

If the argument draws modally strong conclusions from modally weak causal premises, flag the modal adequacy gap. This is especially common in arguments that move from scientific causal claims (typically contingent) to metaphysical conclusions about the nature of things (typically necessary).

#### Dimension 4: Explanatory Adequacy

Does the argument treat causal claims as having explanatory force, and if so, does the presupposed theory account for that explanatory force?

- Some theories tightly link causation and explanation (interventionist theory was explicitly designed to capture causal explanation in science; mechanistic theory treats mechanistic explanation as the paradigm of understanding).
- Other theories separate causation and explanation: a regularity theorist may hold that causation is just constant conjunction, and explanation is a separate pragmatic or epistemic matter; a primitivist may hold that causation is a fundamental relation that does not itself explain anything.
- If the argument relies on causal claims to do explanatory work but the presupposed theory divorces causation from explanation, flag the explanatory adequacy gap.

**Output**: A theory-adequacy assessment with the four dimensions rated, specific gaps identified and justified, and a summary adequacy rating: `fully_adequate`, `partially_adequate`, `inadequate` (major gaps), or `underdetermined` (insufficient basis for assessment).

### Step 4: Detect Causal Problems

Systematically screen the argument's causal claims against a checklist of classic causal problems. Each problem has a specific detection protocol.

**Problem 1: Causal Exclusion**

Detection protocol:
1. Does the argument posit mental or higher-level causation alongside physical causation?
2. If yes, does the argument assume causal closure of the physical (every physical event has a sufficient physical cause) — either explicitly or implicitly?
3. If yes, and the mental/higher-level cause is claimed to be distinct from the physical cause (non-reductive), the exclusion problem applies: the mental cause is either excluded (if the physical cause is sufficient), identical to the physical cause (reduction), or the effect is systematically overdetermined.
4. Flag the argument if it posits mental/higher-level causation without addressing the exclusion challenge. Classify as: `exclusion_vulnerable` (the argument is straightforwardly vulnerable to exclusion), `exclusion_avoided` (the argument explicitly addresses and resolves exclusion), `exclusion_inapplicable` (the argument does not involve mental/higher-level causation alongside physical causation).

Special case: The exclusion problem generalizes beyond mental causation to any case where a purported cause at a "higher level" is claimed to cause an effect that also has a "lower level" sufficient cause. This includes biological causation (e.g., gene causation vs molecular causation) and social causation (e.g., institutional causation vs individual causation).

**Problem 2: Causal Overdetermination**

Detection protocol:
1. Does the argument claim or imply that two (or more) distinct causes are each sufficient for the same effect?
2. If yes, classify the overdetermination type:
   - `benign`: Overdetermination that occurs in isolated, coincidental cases (firing squad, two rocks hitting a window simultaneously). Benign overdetermination is metaphysically unproblematic.
   - `systematic`: Overdetermination that occurs as a matter of principle across a whole domain (e.g., every mental cause overdetermines its effect because the physical cause is also sufficient). Systematic overdetermination is widely regarded as implausible — it posits a massive coincidence in nature.
   - `constitutive`: The causes are not genuinely distinct; one is constituted by or grounded in the other. This is not overdetermination proper but may be presented as such.
3. Flag the argument if it relies on systematic overdetermination without defending its plausibility.

**Problem 3: Causal Preemption**

Detection protocol:
1. Does the argument involve a scenario where more than one causal process is present, one of which "actually causes" the effect while the other is a "backup" that would have caused it had the first not done so?
2. If yes, is the argument's presupposed theory able to correctly identify the actual cause? Counterfactual theories struggle here: in a case of early preemption (A1 and A2 both thrown at window; A1 hits first; if A1 hadn't thrown, A2 would have), the counterfactual "if A1 had not occurred, the effect would not have occurred" is false (A2 would have caused it). Lewis's 2000 "influence" revision addresses this, but the argument may presuppose the simpler 1973 counterfactual analysis.
3. Flag preemption vulnerabilities: `preemption_inapplicable` (no preemption scenario), `preemption_handled` (the theory addresses the case), `preemption_vulnerable` (the theory fails the preemption test and the argument relies on a causal claim in a preemption-like scenario).

**Problem 4: Absence Causation**

Detection protocol:
1. Does the argument treat an absence (omission, lack, non-occurrence, failure, negation) as a cause? Revisit the relata-type classification from Step 1 — any cause classified as `omission` triggers this analysis.
2. If yes, assess whether the presupposed theory accommodates absence causation:
   - **Regularity theory**: Can accommodate — regular connection between absence-type events and effects is no more metaphysically mysterious than regular connection between presence-type events.
   - **Counterfactual theory**: Can accommodate — "if the omission had not occurred" (i.e., if the agent had acted) is a well-defined counterfactual.
   - **Process theory**: Cannot accommodate — an absence is not a spatiotemporally continuous process and does not transmit a conserved quantity. Absence causation is a significant challenge for process theories.
   - **Powers theory**: Struggles — absences are not objects or properties, so they cannot bear causal powers. Some powers theorists (Mumford & Anjum) argue that what we call "absence causation" is really presence-causation plus a normative or contrastive framing.
3. If the argument relies on absence causation and the presupposed theory cannot accommodate it, flag: `absence_theory_mismatch`. Identify whether the argument can be reinterpreted without absence causation without loss of argumentative force.

**Problem 5: Causal Transitivity Failure**

Detection protocol:
1. Map the argument's causal chain: A causes B, B causes C, ... , N causes Z. Does the argument infer that A causes Z from a chain of intermediate causal relations?
2. If yes, check whether the presupposed theory licenses transitivity for this chain:
   - Process theories: Transitivity is generally supported — if a conserved quantity is transmitted from A to B and then from B to C, it is transmitted from A to C.
   - Counterfactual theories: Transitivity is not guaranteed in general. Classic counterexamples: A (assassin's poison) causes B (victim drinks poisoned water) causes C (victim dies), but A does not counterfactually-depend-on-C because if the assassin had not poisoned the water, the backup assassin would have. So transitivity fails in preemption cases even when the causal chain is real.
   - Probabilistic theories: Transitivity is not guaranteed in general. A may raise the probability of B, and B may raise the probability of C, but A need not raise the probability of C (if B screens off A from C in certain configurations).
3. Flag: `transitivity_licensed`, `transitivity_unlicensed_but_plausible` (the chain is simple enough that transitivity is intuitively plausible even if not formally guaranteed), `transitivity_unlicensed` (the chain involves preemption or screening-off configurations where transitivity is likely to fail).

**Problem 6: Causal Circularity**

Detection protocol:
1. Does the argument define or analyze causation in terms that themselves presuppose causation?
2. Common circularities:
   - Defining "cause" in terms of "production," and "production" in terms of causation
   - Defining "cause" in terms of "explanation," and "explanation" in terms of causation
   - Defining "cause" in terms of "mechanism," and "mechanism" in terms of causal relations among parts
3. Circular definitions are not fatal — they may be illuminating even if non-reductive — but they should be flagged as such. A causal analysis that claims to be reductive (e.g., a Humean reduction of causation to non-causal facts) but contains hidden circularities is more seriously flawed.

**Output**: A problem detection report listing each detected problem with its classification, the specific causal claims involved, the diagnostic reasoning, and the severity rating: `critical` (likely fatal to the argument), `significant` (weakens the argument substantially), `minor` (identifies a vulnerability unlikely to be decisive), or `absent` (the problem does not apply).

### Step 5: Evaluate Alternative Theoretical Readings

For each causal claim (or cluster of related causal claims), assess whether the argument would fare better, worse, or equivalently under alternative theories of causation. This step serves two purposes: (a) it identifies whether the argument's dialectical force is theory-dependent (it works only under a specific theory and fails under alternatives), and (b) it identifies potential strategies for strengthening the argument by adopting a different causal theory.

**Evaluation procedure for each alternative theory:**

#### Counterfactual Reinterpretation

1. Reinterpret each causal claim "A causes B" as "If A had not occurred, B would not have occurred."
2. Assess: Does the argument's evidence support the required counterfactuals? Counterfactual support typically requires evidence about what would have happened in alternative scenarios — this may not be available for the argument's causal claims.
3. Assess: Does the conclusion follow from the counterfactually reinterpreted premises? If the original argument relied on causal transitivity and the chain contains preemption-like structures, the counterfactual reinterpretation may break the inference.
4. Identify any new preemption problems introduced by the counterfactual reinterpretation.

#### Probabilistic Reinterpretation

1. Reinterpret each causal claim "A causes B" as "A raises the probability of B" (P(B|A) > P(B|not-A), possibly with additional screening-off or causal Markov conditions).
2. Assess: Does the argument provide probabilistic evidence? If the argument provides only anecdotal or qualitative evidence, the probabilistic reinterpretation is underdetermined.
3. Assess: Does the conclusion survive the weakening from deterministic causation to probabilistic relevance? If the conclusion requires that A guarantee B, probabilistic causation is insufficient.

#### Powers-Based Reinterpretation

1. Reinterpret each causal claim "A causes B" as "A (or its constituents) possesses a power to produce B, which manifests when stimulus conditions S obtain."
2. Assess: Does the argument provide evidence of powers or dispositions in the cause? Powers are typically detected through their manifestations under varying stimulus conditions — does the argument provide this kind of evidence?
3. Assess: Does the powers-based reading strengthen the argument's modal conclusions? Powers ground necessary connections (given the nature of the power-bearer and the stimulus conditions), so if the argument aims for modal strength, the powers reading may help.
4. Flag new ontological commitments: powers are entities (dispositional properties) that must be admitted into the ontology. Does the argument's ontological-commitment profile (if available) support this?

#### Interventionist Reinterpretation

1. Reinterpret each causal claim "A causes B" as "There is a possible intervention on A (an ideal experimental manipulation independent of A's other causes) that changes B (or B's probability distribution)."
2. Assess: Are the variables well-defined in a way that supports intervention? Woodward's framework requires variables that take well-defined values and can be independently manipulated.
3. Assess: Is the intervention notion available? The concept of an "intervention" must itself be characterized in non-causal terms, and there are debates about whether this is feasible. If the argument's domain involves variables that cannot be intervened on (e.g., fundamental physical constants, abstract objects), the interventionist reading may not apply.

#### Primitivist Reinterpretation

1. Reinterpret each causal claim "A causes B" as asserting a fundamental, irreducible causal relation.
2. Assess: Does the argument need a reductive analysis of causation, or would taking causation as primitive serve its purposes? Some arguments require a reductive analysis (e.g., arguments that explain causation in terms of something else); a primitivist reading would be incompatible with such arguments.
3. Assess: The primitivist reading avoids all the reductive problems (preemption, absence causation, transitivity) by declining to reduce causation to anything else. But it may be dialectically unsatisfying if the argument's force depends on explaining what causation is.

**Output**: A comparative theory evaluation matrix with rows for each alternative theory and columns for: feasibility of reinterpretation, evidential support under reinterpretation, inferential support under reinterpretation (does the conclusion still follow?), new problems introduced, and overall assessment (better / equivalent / worse / incompatible).

### Step 6: Compile Report

Synthesize all findings from Steps 1-5 into the structured Causal Claim Analysis Report.

**Report structure:**

1. **Header**: Argument identifier, source text reference, date of analysis, analyst identifier.

2. **Section 1: Causal Claim Catalog** — Complete numbered catalog of all causal claims (CC1...CCn), each with: causal locution, cause relatum (type and specification), effect relatum (type and specification), relata type diagnosis with justification, and structural role in the argument.

3. **Section 2: Causal Theory Diagnosis** — Primary theory diagnosis with evidential basis (lexical, inferential, methodological indicators cited), secondary or inconsistent theory commitments flagged, Humean/anti-Humean classification, relata-theory compatibility assessment. Include a narrative paragraph explaining why the diagnosed theory best fits the argument, and what the argument would look like under the nearest alternative theory.

4. **Section 3: Theory-Adequacy Assessment** — Four-dimension assessment (inference-premise, inference-conclusion, modal, explanatory) with ratings and justifications. Summary adequacy rating with explanation.

5. **Section 4: Problem Detection Report** — Each problem (exclusion, overdetermination, preemption, absence causation, transitivity, circularity) classified and rated, with the specific causal claims involved, diagnostic reasoning, and severity. If a problem is absent, state "not applicable" with a brief justification.

6. **Section 5: Alternative Readings** — Comparative theory evaluation matrix with narrative discussion of the most significant alternative readings. Identify which alternative reading would most strengthen the argument and which would most weaken it.

7. **Section 6: Dialectical Implications** — If this argument is advanced in a debate, what is the dialectical situation regarding causation? Can an opponent challenge the argument by adopting a different theory of causation? Is the argument robust across causal theories or theory-dependent?

8. **Section 7: Recommendations** — Optional. If the argument's causal claims are vulnerable to theory-adequacy failures or causal problems, suggest strategies for strengthening them (e.g., adopting a different causal theory, making explicit the theory presupposed, adding premises to address exclusion, reformulating to avoid absence causation).

## Quality Criteria

1. **Exhaustive Extraction**: Every causal claim in the argument is cataloged. No causal locution (verb, preposition, nominalization, metaphor) is overlooked. The catalog distinguishes central causal claims from auxiliary or background ones but does not omit the latter. If no causal claims are present (boundary condition), this finding is reported rather than a forced analysis.

2. **Theory Diagnosis with Evidence**: The theory diagnosis is not asserted but argued for. Each diagnostic indicator (lexical, inferential, methodological) is cited with specific evidence from the argument. The diagnosis acknowledges ambiguity where present and considers alternative plausible diagnoses. The Humean/anti-Humean classification is explicitly justified.

3. **Relatum Clarity**: The cause and effect in each causal claim are identified with precision. Their ontological type (event, fact, property, object, omission, process, state, agent) is diagnosed and justified. Slippage between types is flagged. The compatibility of the relatum-ontology with the diagnosed causal theory is assessed.

4. **Problem Detection Sensitivity**: The six classic causal problems (exclusion, overdetermination, preemption, absence causation, transitivity, circularity) are systematically checked. Problems are not claimed where they do not apply, but they are identified where they do apply, even if the argument does not explicitly discuss them. Problem severity is calibrated — minor vulnerabilities are distinguished from fatal flaws.

5. **Alternative Awareness**: The report does not assume that only one theory of causation could underwrite the argument. Alternative readings are systematically explored and their implications for the argument's force are assessed. The report identifies whether the argument's causal claims are theory-dependent or theory-robust.

6. **Humean/Anti-Humean Transparency**: The report makes explicit whether the argument's causal commitments fall on the Humean or anti-Humean side of the fundamental divide in the metaphysics of causation. This classification is crucial because many downstream metaphysical commitments (about laws, modality, ontology) depend on it.

## Relations to Other Skills

**Depends on:**
- `phil-argument-reconstruct`: The causal claim catalog cannot be reliably built without the standard-form reconstruction. The reconstruction identifies where causal claims appear in the argument's inferential structure and what logical role they play. The quality of the causal claim analysis is bounded by the quality of the reconstruction.
- `phil-ontological-commitment` (optional): The ontological commitment report reveals what kinds of entities the argument is committed to — events, facts, properties, objects. This constrains which theories of causation are ontologically viable for the argument. If the argument's ontology includes only concrete particulars (no events, no facts, no properties), then event-causation and fact-causation theories are unavailable.

**References (read-only):**
- `causation-taxonomy.md`: A canonical taxonomy of theories of causation, their logical properties, and their strengths and weaknesses. Provides the reference framework for the theory diagnosis in Step 2.
- `glossary-metaphysics.md`: Definitions of technical terms (causal relata types, preemption, overdetermination, exclusion, Humean supervenience, etc.) used in the report.
- `modal-logic-primer.md`: Reference for the modal systems (K, T, S4, S5, B) relevant to the modal adequacy dimension of Step 3.

**Dependents (skills that use this skill's output):**
- `phil-grounding-check`: Grounding and causation are distinct but often compared and contrasted. The causal claim analysis clarifies which relations in the argument are causal (and thus subject to the problems of causation) and which might be grounding relations (and thus subject to different metaphysical constraints).
- `phil-natural-kind-analyze`: Natural kind analyses often involve causal claims about the causal powers or causal mechanisms that individuate kinds. The causal claim analysis provides the baseline for evaluating whether kind-based causal claims are well-founded.

## Boundary Conditions

### 1. No Causal Claims

If the argument contains no causal language — no causal verbs, prepositions, nominalizations, or metaphors — output:

> "No causal claims detected. This argument does not rely on causation. Causal claim analysis is not applicable."

Explain why: the argument's surface language and reconstructed logical structure contain no causal relations. Note that some arguments (purely logical, purely conceptual, purely normative without descriptive causal claims) are genuinely non-causal. Do not invent causal claims where none are present.

### 2. Correlation-Causation Ambiguity

If the argument uses language that is ambiguous between correlation and causation — e.g., "is associated with," "is linked to," "goes together with," "covaries with" — flag the ambiguity explicitly:

> "The following passages use language ambiguous between correlation and causation: [list]. Under a correlation-only reading, the argument does not assert causal claims and the causal claim analysis is not applicable. Under a causal reading, the argument asserts causal claims but without clearly specified truth-conditions. The remainder of this report assumes a causal reading for the purpose of analysis, but the correlation-only reading would avoid all of the problems identified below."

Do not force a causal reading where a correlation reading is equally or more plausible. The report should present both readings and assess the argument under each.

### 3. Mental Causation Focus

If the argument centrally concerns mental causation — the claim that mental states or events cause physical states or events, or cause other mental states or events — the exclusion problem analysis (Step 4, Problem 1) becomes the central focus of the report. In such cases:

- Expand the exclusion analysis beyond the standard protocol. Address: (a) the causal closure premise — does the argument accept it or challenge it? (b) the distinctness premise — does the argument claim mental events are distinct from physical events? (c) the exclusion conclusion — does the argument have a response to Kim's dilemma?
- Assess the argument's position on the dialectical landscape: reductionism (mental = physical), epiphenomenalism (mental causes nothing), non-reductive physicalism with exclusion response, dualism, or eliminativism.
- Cross-reference philosophical positions on mental causation: Kim, Davidson (anomalous monism), Yablo (determinable/determinate), Bennett, List & Stoljar, etc.

### 4. Causal Pluralism

If the argument explicitly or implicitly endorses causal pluralism — the view that "causation" is not a single relation but a family of relations (e.g., physical causation, biological causation, social causation) with different properties — the theory diagnosis in Step 2 must accommodate this. Rather than diagnosing a single theory, the report should:

- Identify which causal relation is invoked in each causal claim.
- Determine whether the argument treats different causal relations as having different logical properties (transitivity, asymmetry, etc.).
- Assess whether the pluralism is well-motivated and consistently applied, or whether it functions as an ad hoc defense against causal problems.
- Flag any equivocation where the argument exploits the ambiguity of "causes" between different causal relations.

### 5. Historical Texts

When the argument is drawn from a historical text (pre-20th-century), the theory diagnosis must account for the historical context. Pre-Humean texts presuppose a broadly Aristotelian or Scholastic causal framework (four causes, powers, substantial forms). Humean texts presuppose the regularity theory (even if Hume himself was more nuanced). The report should diagnose the historical theory but also assess the argument under contemporary theories — this reveals whether the argument's force survives translation into contemporary terms.

## ARS Interface

The causal claim analysis report serves three primary functions within the broader Academic Research System (ARS).

**1. Academic Paper Integration**

The report can be passed to `ars academic-paper` as a "causal structure analysis" section suitable for inclusion in the argument-analysis chapter of a philosophy paper. The structured format (causal claim catalog, theory diagnosis, adequacy assessment, problem report) maps naturally to academic prose. The section would typically read: "The argument relies on the following causal claims: ... These claims presuppose a [theory]-theory of causation, as evidenced by ... This theory is [adequate/inadequate] for the argument's purposes because ... The argument is vulnerable to the following causal problems: ..."

**2. Deep Research Integration**

The report informs `ars deep-research` by identifying which causal-theoretic debates the paper engages. If the report diagnoses a counterfactual theory and detects a preemption problem, the deep-research module knows to search for literature on causal preemption, Lewis's revisions, and alternative theories that handle preemption better. If the report identifies a causal exclusion problem, the deep-research module searches for the mental causation debate, Kim's argument, and responses to exclusion. This enables targeted literature discovery rather than generic keyword searching.

**3. Reviewer Integration**

When used with `ars reviewer` or `ars rebuttal-audit`, the causal claim analysis report identifies vulnerabilities that a reviewer is likely to raise. A reviewer trained in the metaphysics of causation will notice theory-adequacy gaps and causal problems. The report enables the author to anticipate and address these critiques before submission — either by strengthening the argument's causal foundations or by explicitly limiting the scope of the argument's causal claims.

**4. Inter-Skill Data Flow**

The causal claim analysis report shares a data contract with the ontological commitment report (both reference `glossary-metaphysics.md` and the relatum-type taxonomy) and with the natural kind analysis report (which may use causal-claim analysis output to assess whether kind-based causal claims are well-founded). The structured format supports automated cross-referencing between reports.
