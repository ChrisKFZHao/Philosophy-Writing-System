---
description: "Normativity Analysis — analyze the source and structure of normativity; classify categorical/hypothetical imperatives, internal/external reasons, and constitutive vs substantive normativity"
domain: metaethics
version: 1.0.0
---

# Normativity Analysis

## Overview

Normativity — the "ought"-ness or reason-giving force that makes certain considerations count in favor of actions, beliefs, or attitudes — is philosophy's central puzzle about practical thought. Any argument that deploys normative language ("ought," "should," "reason," "obligation," "duty," "right," "wrong") presupposes some account of what normativity is, where it comes from, and how it binds agents. This skill systematically excavates those presuppositions.

The skill analyzes how an argument understands normativity across four dimensions: its source (constitution, reasons, desires, rational structure, social practice, or evolutionary function), its structure (categorical versus hypothetical), its bindingness mechanism (what makes the claim grip the agent), and its overall architecture (how normative claims relate to one another). It classifies normative claims according to both domain (moral, prudential, epistemic, instrumental, aesthetic, legal, social) and structure (categorical/hypothetical), then diagnoses the underlying theory of normativity that the argument presupposes, whether explicitly defended or implicitly assumed.

Normativity is not a single uniform phenomenon. The same argument may deploy moral, prudential, epistemic, and instrumental "oughts" with different structural properties and different sources of normativity. A core task of this skill is to disambiguate these varieties and avoid the common error of treating all normative claims as if they were instances of a single kind. An argument that is constitutivist about moral normativity may be simultaneously Humean about prudential normativity; an argument that treats epistemic reasons as categorical may treat instrumental reasons as hypothetical. The analysis must reflect this complexity.

This skill does not evaluate first-order normative ethics — it does not assess whether a particular moral claim is correct or whether the argument's normative conclusions are sound. Rather, it excavates the meta-level normative infrastructure that makes first-order claims intelligible as normative at all. The question is not "Is the argument right about what we ought to do?" but "What theory of normativity does the argument need for its claims to make sense, and does it supply that theory?"

The analysis is foundational within the metaethics pipeline because normative architecture constrains every downstream analysis: what counts as a moral property (metaphysics), what moral language means (semantics), and how moral judgment connects to motivation (psychology) all depend on how the argument thinks normativity works. An argument that reduces all normativity to instrumental desire-satisfaction will have fundamentally different commitments across all three downstream domains than one that treats normativity as constitutive of agency itself.

## Input

**Required:**
- `argument-reconstruction` report (output of `phil-argument-reconstruct`): A structured representation of the argument's premises, conclusions, inferential steps, and — critically — its implicit assumptions. The reconstruction must be in standard premise-conclusion form, because normative source diagnosis depends on understanding what the argument treats as basic (premise) versus derived (conclusion). If the reconstruction does not flag implicit premises, the normativity analysis may miss the argument's deepest normative commitments.

**Optional:**
- `moral-realism-analysis` report (output of `phil-moral-realism`): When available, supplies background on the argument's metaphysical commitments. This is particularly useful for diagnosing realist normativity sources — if the argument is a robust moral realist, its normative source theory is likely also realist (normative facts are mind-independent). Conversely, if the argument is anti-realist, its normative source theory is constrained accordingly.
- `original-text`: The primary source text, used when the reconstruction report is ambiguous about normative structure and direct textual inspection is needed to resolve classification questions. Particularly valuable when the reconstruction omits qualifying language ("tends to," "normally," "pro tanto") that affects normative classification.

## Output

The skill produces a **Normativity Analysis Report** structured according to the `normativity-schema.json` specification. The report contains six principal sections:

**1. Normativity Source Classification**

The underlying theory of where normativity comes from, classified into one or more of the following categories, each accompanied by textual evidence and a rationale:

- `constitutivist`: Normativity arises from the constitutive standards of some inescapable activity or identity (agency, personhood, reasoning, practical identity).
- `reasons_fundamentalist`: Normative reasons are primitive and irreducible; they are not analyzable in terms of desires, rationality, or anything else. All other normative concepts are analyzable in terms of reasons.
- `rationalist`: Normativity derives from the structure of practical reason itself — what a fully rational agent would do, will, or endorse.
- `humean`: Normativity derives from an agent's desires, broadly construed to include passions, sentiments, and pro-attitudes. All reasons are means to satisfying existing desires.
- `expressivist`: Normativity is not a property to be described but a stance to be expressed. Normative language expresses attitudes rather than stating facts.
- `realist`: Normativity is a mind-independent feature of reality — there are normative facts that hold regardless of anyone's attitudes or responses.
- `contractualist`: Normativity derives from what could be justified to others, what principles no one could reasonably reject, or what would be agreed to under specified conditions.
- `second_personal`: Normativity has an irreducibly interpersonal, addressive structure — moral obligation arises from the practice of holding one another accountable.
- `evolutionary`: Normativity is explained (and sometimes debunked) by evolutionary function — norms exist because they promoted reproductive fitness.
- `other`: A novel or hybrid source theory not captured above, with explicit specification.

An argument may exhibit multiple source theories for different normative domains. The report must track domain-specific source attributions.

**2. Ought-Type Classification**

A mapping of each normative claim in the argument to its domain and structure:

- Domain: `moral`, `prudential`, `epistemic`, `instrumental`, `aesthetic`, `legal`, `social`.
- Structure: `categorical` (binding regardless of desires or contingent ends) or `hypothetical` (binding conditional on desires or ends).
- For each claim: the exact textual location, the normative vocabulary used, the agent addressed, the content prescribed, and the classification with justification.

**3. Reasons Internalism/Externalism Assessment**

A determination of whether the argument treats normative reasons as necessarily connected to an agent's motivational set (internalism) or as existing independently of it (externalism). Sub-classifications include:

- `strong_motivational_internalism`: Judgment that one has a reason necessarily involves motivation.
- `weak_motivational_internalism`: Reasons must be capable of motivating under appropriate conditions.
- `rational_internalism`: Reasons connect to what a rational agent would be motivated by.
- `humean_internalism` (Williams-style): Reasons must connect via a sound deliberative route to the agent's subjective motivational set.
- `strong_externalism`: Reasons exist independently of any connection to the agent's motivations.
- `moderate_externalism`: Reasons are independent of current motivation but not of idealized motivation.

**4. Bindingness Mechanism**

An analysis of what, according to the argument, makes a normative claim binding on an agent. This section traces the "because" chain: "Agent A ought to φ because..." The mechanism is classified as: `rational_requirement`, `constitutive_necessity`, `desire_dependence`, `social_practice`, `evolutionary_function`, `irreducible_normative_fact`, `second_personal_address`, `expressivist_commitment`, or `hybrid/other`. For each central normative claim, the full bindingness chain is articulated.

**5. Normative Architecture Map**

A structural description of how normative claims relate to one another in the argument: `foundational` (one master principle grounds all others), `coherentist` (mutual support without foundation), `hierarchical` (layered priority ordering), or `network` (interdependent nodes without strict hierarchy). Includes a textual or schematic diagram showing support relations, dependencies, and tensions.

**6. Summary Assessment**

A concise synthesis (2-4 paragraphs) of the normative theory diagnosed, its strengths and tensions as they appear in the argument, its regress-stopping adequacy, and its metaethical implications for downstream analysis (metaphysics, semantics, psychology).

## Methodological Foundations

This skill draws on the following key philosophical resources and debates. Each entry describes the core contribution and how it is operationalized in the analysis.

**1. Kant's Categorical/Hypothetical Distinction** (Groundwork of the Metaphysics of Morals, 1785)

The fundamental distinction between imperatives that bind unconditionally — regardless of the agent's desires, goals, or contingent identity — and those that bind only conditionally, given some end the agent has or could have. Kant argues that moral imperatives must be categorical because morality cannot depend on contingent desires; if it did, immoral agents who lacked the relevant desires would have no reason to be moral.

*Operationalization*: The categorical/hypothetical distinction is the primary analytical tool for Step 2 (Classify Normativity Type). The test: reformulate the claim as "If you want X, then you ought to Y." If this captures the claim fully, it is hypothetical. If the claim purports to bind even absent any such condition, it is categorical. The skill also tracks arguments that treat apparently categorical moral claims as ultimately hypothetical through reductionist strategies (e.g., "if you want to be rational, you ought to be moral").

**2. Korsgaard's Constitutivism and the Regress Argument** (The Sources of Normativity, 1996)

Korsgaard argues that any normative claim can be challenged with "but why should I care about that?" If the answer points to a further normative source, the same question can be asked again, generating an infinite regress. The regress stops only at a "constitutive standard" — a norm that is constitutive of the very activity of asking the normative question, such that one cannot coherently question it without engaging in the activity it constitutes. For Korsgaard, the relevant activity is agency itself, and the constitutive standards are those of practical identity.

*Operationalization*: The regress test is the primary tool for Step 5 (Check Bindingness Mechanism). For each normative claim, the analysis asks: "Why is this binding?" and traces the answer chain. If the chain never reaches a regress-stopper — a point where the question "but why should I care?" becomes incoherent — the argument has a normative gap. The skill identifies whether the argument's proposed regress-stopper is genuinely constitutive (part of what it is to be an agent) or merely stipulative.

**3. Williams on Internal Reasons** ("Internal and External Reasons," 1981)

Williams argues that all reasons must be internal: an agent has a reason to φ only if φ-ing would serve or promote some element of the agent's "subjective motivational set" (S) — their desires, projects, commitments, and dispositions — via a sound deliberative route. There are no "external reasons" that bind regardless of S. The purported external reason statement "A has a reason to φ" is either false (if no sound deliberative route from S leads to φ-ing) or, if the speaker intends it as a reason regardless of S, unintelligible — it fails to state a genuine reason.

*Operationalization*: Williams's internalism is the benchmark for Step 4 (Assess Reasons Internalism/Externalism). The analysis applies the "sound deliberative route" test: is there a path of sound practical reasoning from the agent's existing motivations to the prescribed action? If the argument asserts reasons without tracing such a route, it is externalist — and faces the burden of explaining what an "external reason" could be.

**4. Parfit on Reasons Fundamentalism** (On What Matters, Vols. 1-2, 2011; Vol. 3, 2017)

Parfit defends the view that normative reasons are fundamental and irreducible. They cannot be analyzed in terms of desires (contra Williams), constitutive standards (contra Korsgaard), or natural facts (contra naturalist realism). Reasons are the basic normative unit; all other normative concepts — ought, good, right, wrong — are analyzable in terms of them. Parfit also argues that reasons are object-given rather than state-given: a reason to φ is provided by facts about φ-ing (or its outcomes), not by facts about the agent's mental states.

*Operationalization*: Reasons fundamentalism provides the diagnostic criteria for identifying one major source theory in Step 3. Indicators include: treating "is a reason for" as primitive, resisting analysis of reasons in other terms, appealing to intuitive reason-judgments as bedrock, and distinguishing sharply between object-given and state-given reasons.

**5. Scanlon on the Buck-Passing Account** (What We Owe to Each Other, 1998)

Scanlon argues that being good or valuable is not itself a reason-giving property. Rather, to call something good is to claim that it has other, natural properties that provide reasons to respond to it in certain ways — to admire it, respect it, promote it, etc. Goodness "passes the buck" to the underlying reason-giving properties. The normative work is done by reasons, not by the property of goodness itself.

*Operationalization*: The buck-passing account provides a diagnostic tool for Step 3: does the argument treat value properties (goodness, rightness) as normatively basic, or as placeholders for clusters of reasons? If the argument says "X is good because it has property P, and P gives us reason to promote X," it is buck-passing. If it says "X is good, and its goodness itself gives us reason to promote X," it is treating goodness as a basic normative property — a non-buck-passing view.

**6. Darwall's Second-Person Standpoint** (The Second-Person Standpoint, 2006)

Darwall argues that moral obligation has an irreducibly second-personal structure. Moral reasons are not simply reasons that exist from the first-personal standpoint of practical deliberation (Korsgaard) or the third-personal standpoint of objective value (realism). Rather, they are reasons that can be addressed as demands from one person to another within a relationship of mutual accountability. The authority to make such demands, and the obligation to comply with them, are constituted by the practice of holding one another accountable.

*Operationalization*: The second-personal framework provides the diagnostic criteria for the `second_personal` source classification in Step 3. Indicators include: grounding obligation in the standing to make demands, analyzing moral reasons in terms of accountability relations, and treating the I-you address relation as normatively basic rather than derivative.

**7. Street's Evolutionary Challenge** ("A Darwinian Dilemma for Realist Theories of Value," 2006)

Street argues that evolutionary forces have shaped our evaluative attitudes for reproductive fitness, not truth-tracking. This creates a dilemma for realist theories of value: either (a) there is no relation between evolutionary influences and mind-independent normative truths, in which case our normative beliefs are likely false (since they were shaped by fitness, not truth), or (b) there is a tracking relation, in which case the normative truths themselves are explained by non-normative evolutionary facts — which is incompatible with realism's claim that normative truths are fundamentally normative.

*Operationalization*: The evolutionary challenge is used in Step 5 to assess whether a realist source theory has the resources to answer the Darwinian dilemma. If the argument is realist and does not address the evolutionary challenge, the report flags this as a significant vulnerability. The challenge also bears on Step 4: if our normative judgments were shaped by evolution, and internalism ties reasons to our motivational set (which is evolutionarily shaped), internalism may inherit the same debunking pressure.

## Steps

### Step 1: Extract Normative Claims

Identify every normative claim in the reconstructed argument. This is the foundational data-gathering step — everything downstream depends on a complete and accurate extraction.

**Procedural guidance:**

1. **Scan for explicit normative vocabulary**: Work through the reconstructed argument premise by premise and conclusion by conclusion. Search for: "ought," "should," "must," "reason" (used as a count noun — "a reason to φ," not "the reason why"), "obligation," "duty," "right," "wrong," "good," "bad," "valuable," "worth," "required," "permitted," "forbidden," "fitting," "appropriate," "justified," "rational," "reasonable," "warranted," "merited," "deserves."

2. **Capture implicit normative claims**: Some statements lack overt normative vocabulary but function to guide action or assessment. Examples: "That would be a mistake" (normative, not merely predictive), "The right response is..." (normative, even if 'right' is not emphasized), "One cannot consistently..." (can be normative if it implies an obligation of consistency), "This is what we do" (can be normative if it implies a standard). Flag borderline cases for special attention in later steps.

3. **Record for each claim**:
   - Exact textual location (premise number, paragraph reference).
   - The normative vocabulary used.
   - The agent to whom the claim is addressed (universal agent, role-specific, context-specific, the reader, the arguer).
   - The action, attitude, or belief prescribed, proscribed, or evaluated.
   - Whether the claim is presented as basic/underived (a premise) or as supported by other claims (a conclusion or intermediate lemma).

4. **Disambiguate descriptive "oughts"**: Some uses of "ought" are predictive ("the train ought to arrive by 3pm"), epistemic-modal ("given the evidence, the hypothesis ought to be true"), or merely conventional ("you ought to use the side door" meaning "this is the normal practice"). Exclude these from the normative claim set, but note them in a separate list of "apparent normative claims excluded as descriptive" so the exclusion is transparent and contestable.

5. **Produce a claim inventory table**: Create a table with columns: ID, Text/Location, Normative Vocabulary, Agent, Content, Status (basic/derived). This table becomes the working document for Steps 2-6.

### Step 2: Classify Normativity Type

For each normative claim extracted in Step 1, classify it along two dimensions: ought-domain and categorical/hypothetical structure.

**Procedural guidance:**

1. **Domain classification**:
   - `moral`: Concerns interpersonal obligations, rights, welfare, justice, virtue, or character — what we owe to each other. Diagnostic question: "Could someone fail to comply with this claim without wronging anyone (including themselves)?" If violating the claim necessarily involves wronging someone, it is moral.
   - `prudential`: Concerns the agent's own well-being, flourishing, or self-interest. Diagnostic question: "Is this claim about what would be good *for the agent*?" Prudential claims are agent-relative in a distinctive way.
   - `epistemic`: Concerns what one ought to believe given one's evidence, or what methods of belief-formation are justified. Diagnostic question: "Does this claim govern belief or inquiry rather than action?"
   - `instrumental`: Concerns means-end relations — what one ought to do given some end one has or should have. Diagnostic question: "Does this claim's bindingness depend entirely on the agent's having a particular end?"
   - `aesthetic`: Concerns beauty, artistic value, or fittingness of aesthetic response. Diagnostic question: "Is this claim about what is beautiful, artistically valuable, or aesthetically fitting?"
   - `legal`: Concerns what the law requires or permits. Diagnostic question: "Does this claim's normative force derive from a legal system?"
   - `social`: Concerns etiquette, custom, or social convention. Diagnostic question: "Does this claim's normative force derive from social practice rather than morality or law?"

2. **Categorical/hypothetical classification**:
   - Apply the Kantian test: reformulate the claim as "If you want X, then you ought to Y." If this captures the claim fully — if the "ought" would not apply to an agent who lacked the relevant desire or end — it is hypothetical. If the claim purports to bind even absent any such condition, it is categorical.
   - Borderline cases: Some claims are structurally hypothetical but functionally categorical because the antecedent condition (e.g., "if you are a rational agent") applies to all agents. Note this distinction — a claim can be formally hypothetical (conditional in form) but substantively categorical (the condition is inescapable).
   - Reductionist strategies: Some arguments treat apparently categorical moral claims as ultimately hypothetical by embedding them in a broader conditional (e.g., "if you want to be rational, you ought to be moral" or "if you want to flourish, you ought to be just"). These reductionist strategies should be explicitly noted.

3. **Tabulate results**: Extend the claim inventory table from Step 1 with columns for Domain, Structure (Categorical/Hypothetical), and Justification (brief rationale for the classification).

### Step 3: Diagnose Source Theory

Determine where, according to the argument, normativity ultimately comes from. This is the most interpretive step and requires careful attention to both explicit meta-normative claims and implicit structural commitments.

**Procedural guidance:**

1. **Start with explicit claims**: Does the argument say anything direct about the source of normativity? ("Normativity arises from...", "The source of all normative force is...", "What makes a consideration normative is...", "Norms are constituted by..."). If the argument has an explicit normative theory, classify it and cite the textual evidence.

2. **Infer from implicit structure**: If the argument is silent about its normative source, infer from structural features:
   - Does it derive all norms from a single principle (suggesting foundationalism, possibly rationalist or constitutivist)?
   - Does it treat all reasons as means to satisfying desires (suggesting Humeanism)?
   - Does it appeal to what "we" would or could agree to (suggesting contractualism)?
   - Does it treat normative truths as discovered rather than made (suggesting realism)?
   - Does it analyze normative language in terms of expression rather than description (suggesting expressivism)?
   - Does it address the agent second-personally ("you must...") as a source of normative force (suggesting second-personal theory)?
   - Does it give a genealogical explanation of normative thought (suggesting evolutionary theory)?

3. **Use the diagnostic table**:

| Source Theory | Key Diagnostic Indicator | Key Proponent | Falsification Test |
|---|---|---|---|
| Constitutivist | Norms grounded in what is constitutive of agency/practice | Korsgaard, Velleman | Would the norm bind a non-agent? |
| Reasons Fundamentalist | "Reason" treated as primitive, unanalyzable | Parfit, Scanlon | Can the argument analyze reasons in other terms? |
| Rationalist | Norms = what a fully rational agent would do/will | Smith, Korsgaard | Would an irrational agent lack the reason? |
| Humean | Reasons = means to satisfying existing desires | Williams (internalist), Schroeder | Does the reason exist for a desire-less agent? |
| Expressivist | Normative language = expression of attitude | Blackburn, Gibbard | Does the argument treat normative claims as truth-apt? |
| Realist | Normative facts are mind-independent | Enoch, Shafer-Landau | Would normative truths exist without any minds? |
| Contractualist | Normativity = what could be agreed to / not reasonably rejected | Scanlon, Darwall, Rawls | Would norms bind those outside the agreement? |
| Second-Personal | Normativity = accountability relations | Darwall | Can the norm be stated without I-you address? |
| Evolutionary | Norms explained by selective pressure | Street, Joyce | Does the explanation justify or debunk? |

4. **Domain-specific sourcing**: An argument may mix source theories. For each domain identified in Step 2, ask: "What makes *this kind of* normative claim binding?" A common pattern is constitutivism for moral norms + Humeanism for prudential norms. Document each domain-source pair separately.

5. **Provide evidence**: Every source attribution must be supported by at least one specific textual or structural marker. "The argument presupposes constitutivism because it grounds moral obligation in 'what is necessary for being an agent at all' (Premise 3) and explicitly appeals to Korsgaard's regress argument (paragraph 4)." No bare labels.

### Step 4: Assess Reasons Internalism/Externalism

Determine whether the argument treats normative reasons as necessarily connected to an agent's motivational capacities (internalism) or as existing independently of them (externalism).

**Procedural guidance:**

1. **Check for explicit position**: Does the argument directly state a position on reasons internalism/externalism? ("Reasons are internal to an agent's motivational set," "An agent can have a reason even if she has no desire that would be served by acting on it.") If explicit, classify and cite.

2. **Apply diagnostic questions** (if position is implicit):
   - Does the argument ever claim that someone "has a reason" to φ despite lacking (and having no deliberative route from) any relevant desire? If yes, externalist.
   - Does the argument treat motivational incapacity (depression, exhaustion, ideological delusion) as undercutting the *existence* of a reason or merely blocking its *uptake*? If the former, internalist (weak). If the latter, externalist.
   - How does the argument respond to skeptical challenges? If the skeptical "why should I care?" is answered by pointing to the skeptic's existing commitments or desires, internalist. If it is answered by pointing to facts that hold regardless of the skeptic's psychology, externalist.

3. **Classify the specific form**:
   - `strong_motivational_internalism`: Judgment that one has a reason necessarily involves motivation to act on it. (Rare; associated with early non-cognitivism.)
   - `weak_motivational_internalism`: An agent has a reason only if, under appropriate conditions (full information, full rationality, absence of depression), the reason would motivate her.
   - `rational_internalism`: An agent has a reason to φ if and only if φ-ing would be endorsed from the perspective of her motivational set after sound deliberation. (Williams-style internalism is a species of this.)
   - `humean_internalism` (Williams): The reason must connect via a sound deliberative route to the agent's subjective motivational set S. The content of S is contingent and agent-specific.
   - `strong_externalism`: An agent can have a reason to φ even if φ-ing bears no connection whatsoever to her actual or potential motivations. Reasons are independent normative facts.
   - `moderate_externalism`: Reasons are independent of current motivation but may require connection to idealized motivation (where the idealization is defined independently of the agent's actual psychology).

4. **Assess implications**: The internalism/externalism diagnosis has downstream consequences. Internalism limits the viable normativity source theories (constitutivism and expressivism do well; realism struggles). Externalism opens the door to realism but faces the "why care?" challenge. Note these implications.

### Step 5: Check Bindingness Mechanism

Analyze what, according to the argument, makes a normative claim binding — what gives it its grip on the agent such that the agent cannot simply shrug it off without normative failure.

**Procedural guidance:**

1. **Distinguish source from mechanism**: The source theory (Step 3) says *where* normativity comes from (constitution, reasons, desires). The bindingness mechanism says *how* it gets its hold on the agent. Example: a constitutivist source theory may have a "constitutive necessity" bindingness mechanism (the norm binds because conforming to it is necessary for engaging in an inescapable activity). But it could also have a "rational requirement" mechanism (the norm binds because violating it involves a contradiction in the will).

2. **Classify the mechanism**:
   - `rational_requirement`: The claim binds because violating it would involve a contradiction in the will, a failure of instrumental rationality, or an incoherence among one's attitudes. The bindingness is the bindingness of rationality itself.
   - `constitutive_necessity`: The claim binds because conforming to it is necessary for engaging in an inescapable activity (agency, personhood, social life). One cannot opt out of the activity without ceasing to be the kind of thing one is, and the norm is built into the activity.
   - `desire_dependence`: The claim binds because (and only because) it serves the agent's desires or interests. Bindingness is conditional and revocable — if the desires change, the bindingness changes.
   - `social_practice`: The claim binds because of social roles, institutions, conventions, or agreements that the agent is embedded in. Violation constitutes a failure of role-performance or social coordination.
   - `evolutionary_function`: The claim binds because conforming to it was fitness-enhancing; the felt grip of normativity is an adaptation (whether or not it tracks truth).
   - `irreducible_normative_fact`: The claim binds because it is simply a fact that one ought to φ — no further mechanism is needed or available. Normativity is a basic, irreducible feature of reality.
   - `second_personal_address`: The claim binds because it is addressed to the agent within a relationship of mutual accountability, and the agent recognizes the other's standing to make the demand.
   - `expressivist_commitment`: The claim "binds" in the sense that the agent is committed to certain attitudes in virtue of their other attitudes, without there being a normative fact of the matter. Bindingness is internal to the agent's practical perspective.
   - `hybrid/other`: Multiple mechanisms or a novel mechanism, with explicit specification.

3. **Apply the regress test (Korsgaard)**: For the central normative claim in the argument, ask "Why is this binding?" and trace the answer chain:
   - "You ought to keep your promises." Why?
   - "Because promise-keeping is required by the practice of mutual accountability." Why is that practice binding?
   - "Because it is constitutive of interpersonal relationships." Why are those relationships binding?
   - Continue until the chain reaches either a satisfactory terminus (a constitutive standard, a primitive reason, a brute normative fact) or an infinite regress.

4. **Evaluate regress-stopper adequacy**: If the chain stops at a claim like "these are just the fundamental reasons" or "this is just what rationality requires," evaluate whether this is a satisfactory terminus. A terminus is satisfactory if asking "but why should I care about that?" would be incoherent — e.g., because the question itself presupposes the very norm it questions (constitutivism) or because the reason is genuinely primitive and self-evident (reasons fundamentalism).

5. **Flag gaps**: If the argument does not address the regress, note: "The argument's bindingness mechanism is incomplete — it traces the normative chain to step N but does not explain why step N is binding. The regress is not stopped."

### Step 6: Map Normative Structure

Analyze how the various normative claims identified in Step 1 relate to one another structurally. This is the architectural analysis — how the normative claims form a system (or fail to).

**Procedural guidance:**

1. **Identify architectural type**:
   - `foundational`: One or a few fundamental normative principles ground all others via derivation or specification. Structure: a tree with roots (foundational principles) and branches (derived principles, particular judgments). Example: Kant's derivation of all duties from the Categorical Imperative.
   - `coherentist`: Normative claims mutually support one another without any being foundational. Justification is holistic — the system is justified as a whole by its coherence (consistency, explanatory integration, reflective equilibrium). Structure: a web with bidirectional support relations.
   - `hierarchical`: Normative claims are ordered by priority, with higher-order norms governing the application or override of lower-order ones, but without a single foundation. Structure: layered, with meta-norms, norms, rules, and particular judgments.
   - `network`: Normative claims are interconnected with complex inferential and justificatory relations that resist reduction to any simple structure. Some nodes are more central than others, but centrality is a matter of degree and context. Structure: a weighted graph.

2. **Map the relations**: For each normative claim, identify:
   - Which other claims support it (upstream dependencies).
   - Which other claims it supports (downstream reach).
   - Conflicts or tensions with other claims.
   - Whether the support relation is deductive (entailment), probabilistic (making more likely), or justificatory (providing a reason).

3. **Identify foundational claims** (if foundational architecture): Which claims are treated as basic — not derived from or supported by any other normative claim? These are the architecture's axioms.

4. **Flag orphans**: Identify any normative claims that neither support nor are supported by other claims. Orphan claims suggest incomplete normative integration — they are asserted but not connected to the argument's normative system.

5. **Produce a diagram**: Provide a structured textual diagram showing the architecture. Use indentation for hierarchy, arrows (-->) for support relations, and annotations for conflict or tension. Example: "Categorical Imperative [FOUNDATION] --> Duty of Honesty --> Prohibition on Lying --> Prohibition on Exaggeration."

### Step 7: Compile Report

Assemble the findings from Steps 1-6 into a structured report conforming to `normativity-schema.json`.

**Procedural guidance:**

1. **Executive Summary** (2-4 sentences): State the primary normative theory diagnosed and its key features. "This argument presupposes a constitutivist theory of moral normativity, grounded in the constitutive standards of agency as practical identity (Korsgaard-style), combined with a Humean theory of prudential normativity. The bindingness mechanism for moral norms is constitutive necessity; for prudential norms, desire-dependence. The argument is reasons-internalist (Williams-style) about all practical reasons, which constrains its realism options."

2. **Source Classification with Evidence**: Present the source theory classification(s) with domain-specific attribution where relevant. Quote or cite the specific textual basis for each diagnostic judgment. Include confidence levels (high/medium/low) and alternative diagnoses where appropriate.

3. **Ought-Type Table**: Present the full classification table from Step 2. One row per normative claim. Columns: ID, Text, Domain, Categorical/Hypothetical, Justification.

4. **Internalism/Externalism Assessment**: Present the classification with argumentative support. Show why the argument commits to this position. If the argument is silent, state the best structural inference with appropriate caveats.

5. **Bindingness Analysis**: Present the full "because" chain for the central normative claim(s). Classify the mechanism. Evaluate regress-stopper adequacy. Flag gaps.

6. **Normative Architecture**: Present the structural diagram and describe the architecture type. Explain why it is foundational/coherentist/hierarchical/network. Note orphans and tensions.

7. **Metaethical Implications**: Conclude with an explicit statement of what this normative theory entails for downstream metaethical analysis: "Given this argument's constitutivism about moral normativity and reasons internalism, the following metaethical positions are viable: [list]. The following are ruled out or face significant tension: [list]."

**Formatting rules**: Each section should be interpretable independently but cross-referenced. Use consistent labels across sections. Flag interpretative uncertainties explicitly. The report should enable a reader who has not read the original argument to understand its complete normative infrastructure.

## Quality Criteria

1. **Source identification with evidence**: Every classification of the normative source theory must be supported by specific textual or structural evidence from the reconstructed argument. No bare labels — every attribution of "constitutivism," "realism," "Humeanism," etc. must cite the premise, passage, or structural feature that grounds the diagnosis.

2. **Categorical/hypothetical precision**: Each normative claim must be explicitly classified as categorical or hypothetical, with the test applied and the basis for the classification stated. Borderline cases must be discussed, not suppressed. Reductionist strategies (treating apparently categorical claims as ultimately hypothetical) must be explicitly noted.

3. **Internalism/externalism explicitness**: The report must state clearly whether the argument is internalist or externalist about reasons, and at what strength level. If the argument is silent, the report must note this, give the best structural inference, and explain what features of the argument support that inference. The report must also note how the internalism/externalism diagnosis interacts with the source theory diagnosis (consistent? in tension?).

4. **Regress awareness**: The analysis must demonstrate that it has considered whether the argument's normative source can answer Korsgaard's regress challenge. The report must identify the regress-stopper (if any) and evaluate its adequacy. If the argument stops at "these are just the fundamental reasons" or "this is just what rationality requires" without further grounding, the report must flag this.

5. **Domain distinction**: Moral, prudential, epistemic, and instrumental normativity must not be conflated. If the argument itself conflates domains, the report must flag this as analytically problematic. An argument that treats prudential reasons as if they were moral ones is making a category error that the report must identify.

6. **Completeness**: Every normative claim in the argument must be accounted for in the classification table. No orphan normative content. The structural map must include all claims.

7. **Structural clarity**: The normative architecture description must be precise enough that another analyst could reproduce the map from the description alone. The diagram must use consistent notation and explicitly show all documented support relations.

## Relationships to Other Skills

**Depends on (upstream):**
- `phil-argument-reconstruct`: The normativity analysis requires a structured argument map as input. Without a clear view of the argument's premises, conclusions, and inferential structure, normative source diagnosis is unreliable. The reconstruction must flag implicit premises, because an argument's deepest normative commitments are often implicit.
- `phil-conceptual-analysis` (indirect): Understanding key concepts (reason, ought, value, obligation) as they function in the argument informs normativity classification. If the argument uses "reason" in an idiosyncratic way, the concept-map report clarifies this.

**Referenced knowledge resources:**
- `references/normativity-taxonomy.md`: The canonical taxonomy of normative theories, with detailed profiles of each source theory, their key proponents, strengths, and standard objections. All source classifications should be cross-referenced with this taxonomy.
- `references/glossary-metaethics.md`: Standard definitions of key terms (categorical imperative, internal reason, constitutive norm, bindingness, regress argument) to ensure consistent usage across all metaethics skills.
- `references/metaethical-distinctions.md`: A guide to the major distinctions in metaethics and how they cross-cut one another. Used to check for category errors (e.g., treating the internalism/externalism distinction as if it were the same as the cognitivism/non-cognitivism distinction).

**Dependents (downstream):**
- `phil-moral-psychology`: The moral psychology skill builds directly on the normativity analysis. The reasons internalism/externalism diagnosis from this skill feeds into the motivational internalism/externalism analysis in moral psychology. The bindingness mechanism analysis constrains the moral-psychological architecture.
- `phil-moral-realism`: The realism analysis uses normativity sourcing to understand the argument's metaphysical commitments. A realist normativity source supports a realist metaphysics; an expressivist or constitutivist source constrains realism options.
- `phil-moral-semantics` (indirect): Semantic analysis can be informed by normative structure, especially for expressivist theories where semantics and normativity intertwine. The categorical/hypothetical classification bears on semantic analysis because semantic theories must account for both kinds of claims.

**Independent of (cross-domain):**
- `phil-moral-disagreement`: The analysis of moral disagreement is logically independent of normativity source theory — a constitutivist and a realist can agree about the nature of moral disagreement even if they disagree about the source of normativity.

## Boundary Conditions

**1. No normative language**: If the argument contains no normative language whatsoever — no "ought," "should," "reason," "obligation," "duty," "right," "wrong," "good," "bad," or functional equivalents — this skill should not be invoked. Output a null report: "No normative claims detected. The argument is purely descriptive or theoretical without engaging normative questions. Normativity analysis is not applicable."

**2. Descriptive vs. normative "ought"**: The argument may use "ought" in a purely descriptive/predictive sense ("the train ought to arrive at 3pm" meaning "it is predicted to arrive"), an epistemic-modal sense ("given the evidence, the hypothesis ought to be true"), or a conventional sense ("you ought to use the side door" meaning "this is the normal practice"). These are not normative claims and should be excluded. However, the report must note the distinction and list all excluded apparent-normative claims so the exclusion is transparent and contestable. Flag genuinely normative uses that might be disguised as descriptive ("rational agents will φ" functioning as "rational agents ought to φ").

**3. Purely first-order normative ethics**: If the argument engages only in first-order moral reasoning (arguing for or against specific moral conclusions) without addressing meta-level questions about the nature of normativity, the analysis must still proceed because first-order arguments have implicit normative infrastructure. However, the report must explicitly distinguish between the argument's explicit first-order claims and the implicit meta-normative theory being diagnosed. Begin the report with: "This argument does not explicitly theorize its own normativity; the following analysis diagnoses its implicit commitments as inferred from its first-order normative reasoning."

**4. Skeptical arguments (error theory, eliminativism)**: Arguments that deny the existence of normativity are within scope. The analysis should classify their diagnosis of what normativity *would be* (and why it fails) rather than attributing a positive normative theory. The source classification in such cases identifies the target of critique: "This argument presupposes a realist conception of normativity (normative facts as mind-independent) and argues that no such facts exist — hence error theory."

**5. Domain confusion**: If the argument conflates distinct normative domains (e.g., treating prudential reasons as if they were moral ones, or treating instrumental rationality as if it exhausted normativity), the report must flag this explicitly: "The argument conflates [domain A] and [domain B], treating claims of one type as if they had the normative structure of the other. This conflation undermines the precision of its normative analysis."

**6. Incompleteness**: If the argument's normative commitments are radically underdetermined — the text simply does not contain enough to diagnose a source theory or internalism/externalism position — the report should state this clearly and give the range of compatible diagnoses rather than forcing a single classification on insufficient evidence. "The argument's normative commitments are underdetermined. On the available evidence, the normativity source could be either constitutivist or rationalist (reasons fundamentalist and Humean are ruled out by the argument's rejection of desire-dependence). Further textual evidence would be needed to decide between these."

**7. Self-contradictory normative commitments**: If the argument appears to commit to incompatible normative theories in different parts of the text, the report must flag the contradiction: "The argument presupposes a realist source theory for moral normativity (Premise 2: 'moral facts are mind-independent') but also presupposes a Humean theory of reasons (Premise 7: 'all reasons are means to satisfying desires'). These commitments are in tension because mind-independent moral facts would constitute external reasons, which Humeanism rules out."

## ARS Interface

This skill is part of the Academic Research Skills (ARS) metaethics pipeline. It conforms to the ARS skill specification as follows:

- **Invocation pattern**: This skill is invoked when the system detects a need for normativity analysis in a metaethics workflow, typically after argument reconstruction (`phil-argument-reconstruct`) and before moral psychology analysis (`phil-moral-psychology`). It can be invoked standalone or as part of a pipeline run.

- **Schema compliance**: The output conforms to `normativity-schema.json` (located in `shared/`), which defines the JSON structure for normativity analysis reports. All required fields in the schema are populated; optional fields are populated when information is available. The schema enforces controlled vocabularies for source classification, ought-type, internalism/externalism, bindingness mechanism, and architecture type.

- **Cache behavior**: Normativity analysis reports are cached per argument (keyed by argument-reconstruction hash). If the same argument is analyzed again with the same reconstruction input, the cached report is returned unless the cache is invalidated via `ars-cache-invalidate`.

- **Error handling**: If required input is missing, the skill returns a structured error object with a description of what is needed and a suggested remediation. If the argument is outside the boundary conditions, the skill returns an appropriate null or boundary-condition report rather than forcing an analysis.

- **Pipeline integration**: This skill's output is tagged with `output-type: normativity-analysis` for downstream consumption. The report includes a `pipeline_metadata` block with skill version, generation timestamp, input document hash, and upstream dependency hashes (argument-reconstruction report hash). Downstream skills (`phil-moral-psychology`, `phil-moral-realism`) query by `output-type` to locate this report.

- **ARS tool integration**:
  - The Normativity Analysis Report can be passed to ARS `academic-paper` as a "normative framework statement" for the methodology section.
  - The source classification and structure map can inform ARS `deep-research` for targeted searches on specific normativity theories (e.g., "constitutivist responses to the regress problem," "Parfit's objections to Humean normativity").
  - The bindingness mechanism analysis can seed ARS `academic-paper-reviewer` for anticipating objections about the justification of normative claims.
  - Citation formats throughout the report are compatible with ARS `citation-check` (Author-Year format with page references where available).

- **Versioning**: This skill follows semantic versioning. Breaking changes to the output schema or classification taxonomy (e.g., adding a new required field, removing a source theory category) require a major version bump. Additions to the classification taxonomy (e.g., new source theory types) require a minor version bump. Clarifications, improved guidance, and bug fixes require a patch version bump.
