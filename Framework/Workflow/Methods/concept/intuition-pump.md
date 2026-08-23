---
id: method.concept.intuition-pump
package: concept
legacy_ids: [phil-intuition-pump]
label: Intuition Pump Analysis
consumers: [phil-research/reconstruct, phil-research/evaluate, phil-write, phil-review]
selector: feature-detected
side_effects: read-only
---

# Intuition Pump Analysis (method.concept.intuition-pump)

> Internal method module — not a registered runtime skill. Loaded on demand by the consuming skill's mode contract through the manifest resolver; never loaded wholesale.

# method.concept.intuition-pump — Intuition Pump Analysis

---

## 1. Overview

Intuition pumps are philosophical devices — thought experiments, vignettes, cases, and narrative scenarios — designed to elicit specific intuitive judgments that then function as premises or dialectical leverage in arguments. The term originates with Daniel Dennett, who used it critically to describe thought experiments that, in his view, seduce readers into assenting to conclusions without adequate rational grounding. In _Elbow Room_ (1984) and later in _Intuition Pumps and Other Tools for Thinking_ (2013), Dennett characterizes intuition pumps as cognitive prosthetics: tools that can illuminate when well-designed but that more often exploit cognitive shortcuts to manufacture agreement. His critique is not that intuitions are worthless but that intuition pumps can bypass deliberative reasoning, triggering automatic assent to conclusions that would not survive reflective scrutiny.

Dennett's critical stance notwithstanding, intuition pumps are ubiquitous in analytic philosophy and arguably constitutive of its method. Gettier cases — in which a justified true belief is paired with an element of epistemic luck — elicit the intuition that justified true belief is insufficient for knowledge, a judgment that has structured the epistemology of the past six decades. Trolley problems target moral intuitions about harm, agency, and the doing-allowing distinction, generating data that moral theorists must accommodate or explain away. Twin Earth scenarios mobilize semantic intuitions about reference and meaning to argue for externalism about content. Mary's room probes intuitions about physicalism and qualitative experience. Thomson's violinist tests intuitions about bodily autonomy and the right to life. Frankfurt cases challenge the principle of alternate possibilities by engineering scenarios where an agent could not have done otherwise yet seems intuitively responsible. Across epistemology, ethics, metaphysics, philosophy of mind, and philosophy of language, intuition pumps do heavy argumentative work, and philosophers routinely treat the intuitions they elicit as evidence that theories must accommodate.

Intuitions are not, however, a stable or uncontested class of cognitive states. The experimental philosophy movement — launched by Weinberg, Nichols, and Stich (2001) and expanded by Machery, Mallon, Nichols, and Stich (2004) — has marshaled empirical evidence that philosophical intuitions vary systematically across cultures, socioeconomic backgrounds, personality traits, and framing conditions. This finding challenges the armchair methodology that treats philosophers' own intuitions as reliable evidence about the phenomena under investigation. If epistemic intuitions vary with cultural background, whose intuitions should epistemology systematize? If moral intuitions are shaped by affect and framing, what reason do we have to treat them as tracking moral truth? Meanwhile, a growing debunking literature — advanced by Greene (2008), Singer (2005), Kahane (2011), and Nichols (2014), among others — argues that many moral and modal intuitions are byproducts of evolutionarily adaptive but truth-insensitive cognitive heuristics. The intuition that pushing a large man off a footbridge is impermissible, while pulling a switch is not, may reflect an evolutionarily ancient disgust response to physical contact with a conspecific rather than sensitivity to a deep moral distinction. If so, the intuition's probative value is undermined.

Yet the situation is not one-sided. Defenders of philosophical intuition have developed sophisticated responses. Williamson (2007) argues that philosophical methodology does not rely on a special faculty of "intuition" distinct from ordinary theoretical judgment, deflating both the pro-intuition picture and the anti-intuition critique. Proponents of the "expertise defense" argue that trained philosophers' intuitions are more reliable than lay intuitions, just as chess masters' positional intuitions outperform novices'. Reflective equilibrium as a methodology does not require that any single intuition be indefeasible — only that intuitions be weighed holistically against theoretical considerations, with each capable of revising the other. And some philosophers argue that intuition variation, while real, is overstated by experimental philosophy studies that use underdetermined vignettes or fail to control for comprehension.

This skill provides a systematic, neutral analytical framework for evaluating intuition pumps. It is neither an instrument of wholesale debunking nor a defense of armchair methodology. It treats intuition pumps as objects of philosophical engineering: devices constructed to perform cognitive work, susceptible to analysis in terms of mechanism, structure, transparency, framing, and dialectical load-bearing capacity. The skill reconstructs the chain from pump to intuition to judgment to premise; classifies the cognitive faculty being targeted; assesses susceptibility to debunking explanations; detects framing effects that might manufacture or distort the elicited intuition; and evaluates whether the intuition, once subjected to critical scrutiny, genuinely supports the conclusion it is enlisted to serve. The output is a structured report that maps the intuition's dialectical ecology — where it sits in the argument, what alternatives exist if it is rejected, and what the overall argumentative architecture looks like with and without the pump.

---

## 2. Input

**Required:**

- **The intuition pump text.** The thought experiment, vignette, or case description as it appears in the philosophical work, quoted or closely paraphrased. The complete scenario must be provided, including any surrounding commentary that sets up the pump, primes the reader, or guides the expected response. Omissions or paraphrases that alter the framing are flagged, since framing is itself an object of analysis.

- **The argument that the pump supports.** The target conclusion and the inferential chain connecting the elicited intuition to that conclusion. This should be provided in premise-conclusion form where possible, with each inferential step made explicit. The analysis must be able to identify the precise point at which the intuition enters the argument and the work it is expected to do.

- **Context of deployment.** The dialectical situation: is the pump offered as a counterexample to a universal claim, as an illustration of a theoretical point, as a standalone argument, or as part of a cumulative case? What is the pump responding to? What alternative position does it challenge? This context determines the burden the pump must carry — a pump used as a counterexample bears more weight than one used as an illustration.

**Optional (strongly recommended for thorough analysis):**

- **Experimental philosophy data.** Survey results, cross-cultural studies, replication findings, and meta-analyses bearing on the relevant intuition. This includes studies that report consensus as well as studies that report variation. The absence of relevant studies should be noted as an empirical gap rather than taken to indicate consensus.

- **Psychological literature.** Research on the cognitive mechanisms implicated by the pump: dual-process theory, moral foundations theory, heuristics-and-biases research, affect-as-information literature, cognitive load studies, and neuroimaging findings where relevant. This literature is used to classify the pump mechanism (Step 1), detect framing and bias effects (Step 5), and assess debunking susceptibility (Step 6).

- **Competing philosophical analyses.** How other authors have diagnosed the pump's force or failure. Citation of the secondary literature on canonical pumps provides comparative leverage and prevents the analysis from reinventing known diagnoses.

- **Authorial commentary.** The pump-creator's own description of what the reader is supposed to intuit, why it matters, and how the intuition is supposed to support the conclusion. This is not treated as authoritative — authors can misdescribe their own pumps — but it establishes the intended effect against which the pump's actual effect can be measured.

- **Empirical data on intuition-to-world correlation.** Where available, studies testing whether people's intuitive classifications or judgments in the target domain align with expert consensus or independently established ground truth. For example, if a semantic intuition pump claims that ordinary speakers judge a term to refer to X, corpus linguistic or experimental semantic data can test that claim.

---

## 3. Output

The skill produces a structured analytical report with the following sections:

1. **Pump Mechanism Classification.** Identification of the cognitive faculty or faculties the pump targets. Classification uses a taxonomy derived from the psychological and philosophical literature on intuition types: the pump may target perceptual seemings (it presents a scenario that looks a certain way), conceptual competence (it probes the boundaries of a concept), moral sentiment (it activates affective responses to normatively charged scenarios), modal imagination (it asks whether a scenario is conceivable or possible), memory-based recognition (it invokes pattern recognition from past experience), linguistic competence (it queries grammaticality or semantic judgments), or practical reasoning (it asks what an agent ought to do). Many pumps target hybrid mechanisms, and the classification identifies both the primary and secondary mechanisms at work.

2. **Intuition Content.** A precise statement of the elicited intuition, formulated as the proposition the reader is meant to find intuitively compelling. This is distinguished from (a) the psychological state of intuiting, (b) the judgment the reader forms on the basis of the intuition, and (c) the premise the judgment becomes in the argument. Example: in the standard Gettier case, the elicited intuition is roughly "Smith does not know that the man who will get the job has ten coins in his pocket," the judgment is that this is a case of justified true belief without knowledge, and the premise is that justified true belief is insufficient for knowledge.

3. **Intuition-to-Judgment-to-Premise Chain.** A stepwise reconstruction in three stages. Stage one: the raw intuitive response — what the reader feels or is inclined to think upon encountering the pump. Stage two: the propositional judgment — the articulated propositional content extracted from the intuitive response. Stage three: the argumentative premise — the role that judgment plays in the larger argument. The reconstruction identifies any implicit enrichment or interpretive steps between the stages. It flags gaps where the felt intuition underdetermines the propositional content, or where the propositional judgment underdetermines the argumentative premise.

4. **Argumentative Role.** Specification of the pump's dialectical function with reference to a taxonomy of argumentative roles: counterexample to a universal claim, case triggering a modus ponens inference (if theory T is true, then pump P should be judged J; P is not judged J; therefore T is false), source of data for reflective equilibrium (the intuition is one considered judgment among many, to be weighed holistically), intuition of possibility licensing a modal argument (if P is conceivable, then P is possible; the pump makes P conceivable), absurdity generator (the pump is designed to elicit an intuition that some view entails an absurd consequence), or intuition of explanation (the pump makes salient an explanatory relationship). The role determines the dialectical burden the pump must bear.

5. **Empirical Backing Assessment.** Evaluation of the available empirical evidence regarding whether the intuition is (a) widely shared across relevant populations, (b) stable under cross-cultural and demographic variation, (c) responsive to framing manipulations (does re-describing the pump alter the elicited intuition?), and (d) correlated with independently verifiable features of the target domain. When empirical evidence is absent, this is flagged. When evidence is mixed, the conflicting findings are reported and weighted. The assessment classifies the intuition on a scale from "robustly shared across all sampled populations" through "shared within some populations but not others" to "highly variable and culturally or demographically specific."

6. **Framing and Bias Detection.** Systematic analysis of the pump's narrative construction for features that may bias intuitive responses. This includes: ordering effects (does the sequence of information shape the intuition?), affectively laden language (are emotionally charged terms doing argumentative work?), implicit contrast cases (is the reader's judgment anchored by an unstated comparison?), selective description (what does the author choose to mention or omit, and would including omitted details alter the intuition?), rhetorical posture of inevitability (phrases like "surely," "obviously," "one cannot help but judge"), and anchoring effects (does an initial numerical or descriptive claim set a baseline that shapes subsequent judgment?). For each detected feature, the analysis proposes a neutral re-description and assesses whether the intuition survives the reframing.

7. **Debunking Susceptibility.** Systematic evaluation of whether the intuition is vulnerable to debunking explanations. Three families of debunking argument are considered. Evolutionary debunking: the intuition is a byproduct of selection pressures that favored fitness-enhancing responses rather than truth-tracking ones, and there is no reason to think fitness and truth coincide in this domain. Process debunking: the intuition arises from cognitive processes known to be unreliable in the relevant domain (e.g., the affect heuristic in moral judgment, the availability heuristic in probability judgment). Genealogical debunking: the intuition's causal origins — in culture, upbringing, or contingent historical circumstances — are independent of the truth it purports to track. Each debunking argument is stated in explicit premise-conclusion form and evaluated for soundness. The analysis distinguishes between debunking that fully undermines the intuition's evidential value, debunking that partially reduces its weight, and debunking that fails because the causal explanation is consistent with truth-tracking.

8. **Dialectical Alternatives.** Mapping of the argumentative landscape under the supposition that the intuition is not granted. Five outcomes are possible. Collapse: the argument depends on the intuition and has no independent support. Weakening: the argument loses force but may retain some plausibility from other considerations. Restructuring: the argument can be reformulated with different intuitions or non-intuitive premises. Burden-shifting: the opponent must explain away the intuition's apparent compellingness even if the intuition is not treated as evidence. Overdetermination: the conclusion is independently supported and the intuition pump is merely illustrative. The analysis specifies which outcome applies and why.

9. **Verdict on Dialectical Force.** A final, integrative assessment of whether the intuition pump carries the argumentative weight assigned to it. Verdict categories: "dialectically decisive" (the pump provides strong, non-redundant support for the conclusion and survives all challenges), "dialectically weighty but defeasible" (the pump provides genuine support but can be overridden by countervailing considerations), "dialectically weak" (the pump provides only marginal support, easily outweighed), "dialectically inert" (the pump does no argumentative work that is not already done by other premises), or "dialectically counterproductive" (the pump invites debunking or framing critiques that undermine other parts of the argument). The verdict includes a confidence assessment.

---

## 4. Methodological Foundations

This skill draws on the following canonical sources and research programs. Each entry identifies the core contribution and its role in the analytical framework.

1. **Dennett on Intuition Pumps as Cognitive Prosthetics.**
   - Dennett, Daniel C. (1984). _Elbow Room: The Varieties of Free Will Worth Wanting._ MIT Press.
   - Dennett, Daniel C. (2013). _Intuition Pumps and Other Tools for Thinking._ W. W. Norton.
   - _Contribution:_ Dennett treats intuition pumps as engineered cognitive artifacts — some illuminating, some misleading — and provides the foundational vocabulary for analyzing their construction and operation. His framework emphasizes that pumps can seduce by exploiting cognitive shortcuts rather than by tracking truth, and it introduces the distinction between pumps that make a phenomenon _thinkable_ (legitimate heuristic value) and pumps that make a conclusion seem _inevitable_ (illegitimate rhetorical force). Used in: Step 1 (mechanism identification), Step 4 (cognitive transparency), and the framing of the whole analytical enterprise.

2. **Experimental Philosophy and Intuition Variation.**
   - Weinberg, Jonathan M., Shaun Nichols, and Stephen Stich (2001). "Normativity and Epistemic Intuitions." _Philosophical Topics_ 29(1–2): 429–460.
   - Machery, Edouard, Ron Mallon, Shaun Nichols, and Stephen P. Stich (2004). "Semantics, Cross-Cultural Style." _Cognition_ 92(3): B1–B12.
   - Machery, Edouard (2017). _Philosophy Within Its Proper Bounds._ Oxford University Press.
   - _Contribution:_ This research program provides the empirical backbone for questioning the universality of philosophical intuitions and introduces methodological tools — survey methods, cross-cultural comparison, framing manipulation — for assessing whether a given intuition is shared or parochial. Machery (2017) systematizes the "argument from variation": if intuitions vary across demographics, they cannot all be true, and without a principled way to select which population's intuitions are veridical, none are epistemically privileged. Used in: Step 5 (empirical backing assessment), Step 6 (debunking susceptibility via the variation argument).

3. **Heuristics, Biases, and Framing Effects.**
   - Tversky, Amos, and Daniel Kahneman (1974). "Judgment under Uncertainty: Heuristics and Biases." _Science_ 185(4157): 1124–1131.
   - Kahneman, Daniel, and Amos Tversky (1979). "Prospect Theory: An Analysis of Decision under Risk." _Econometrica_ 47(2): 263–291.
   - Tversky, Amos, and Daniel Kahneman (1981). "The Framing of Decisions and the Psychology of Choice." _Science_ 211(4481): 453–458.
   - Kahneman, Daniel (2011). _Thinking, Fast and Slow._ Farrar, Straus and Giroux.
   - _Contribution:_ The heuristics-and-biases tradition supplies the analytical tools for detecting when an intuition pump exploits framing, anchoring, availability, affect, representativeness, or substitution heuristics to manufacture intuitive assent. Kahneman's System 1 / System 2 dual-process model provides the cognitive architecture for distinguishing intuitive from reflective judgment. Used in: Step 5 (framing and bias detection), Step 6 (process debunking).

4. **Reflective Equilibrium and the Methodological Role of Intuitions.**
   - Rawls, John (1971). _A Theory of Justice._ Harvard University Press (especially Section 9 on reflective equilibrium).
   - Daniels, Norman (1979). "Wide Reflective Equilibrium and Theory Acceptance in Ethics." _Journal of Philosophy_ 76(5): 256–282.
   - Singer, Peter (2005). "Ethics and Intuitions." _The Journal of Ethics_ 9(3–4): 331–352.
   - _Contribution:_ Rawls articulates the canonical methodology in which considered judgments (intuitions) serve as provisional fixed points to be systematized into principles, with principles and judgments mutually adjusting until equilibrium is reached. Daniels extends this to "wide" reflective equilibrium that incorporates background theories. Singer provides the critical counterpoint, arguing that many moral intuitions are evolutionary or cultural byproducts and that the method of reflective equilibrium merely systematizes prejudice unless intuitions are independently vetted. Used in: Step 3 (classifying the role of the intuition in the argumentative architecture), Step 8 (dialectical alternatives when intuition is rejected).

5. **The Epistemology of Intuition and the Expertise Defense.**
   - Williamson, Timothy (2007). _The Philosophy of Philosophy._ Blackwell.
   - Sosa, Ernest (2007). _A Virtue Epistemology: Apt Belief and Reflective Knowledge, Volume I._ Oxford University Press.
   - _Contribution:_ Williamson argues that philosophical methodology does not rely on a special faculty of "intuition" distinct from ordinary theoretical judgment — philosophers engage in the same kind of counterfactual reasoning as scientists and historians. This deflationary account reframes the debate: the question is not whether "intuition" is reliable but whether ordinary counterfactual judgment, applied to philosophical cases, is reliable. Sosa develops a virtue-epistemological account of intuition as an intellectual seeming that can be more or less competent, allowing for the possibility that philosophical training improves intuitive reliability. Used in: Boundary Condition 3 (expert vs. lay intuitions), Step 6 (evaluating whether debunking arguments target the right target).

6. **Cognitive Architecture of Moral Judgment.**
   - Greene, Joshua D., R. Brian Sommerville, Leigh E. Nystrom, John M. Darley, and Jonathan D. Cohen (2001). "An fMRI Investigation of Emotional Engagement in Moral Judgment." _Science_ 293(5537): 2105–2108.
   - Greene, Joshua D. (2008). "The Secret Joke of Kant's Soul." In W. Sinnott-Armstrong (ed.), _Moral Psychology, Vol. 3: The Neuroscience of Morality._ MIT Press, pp. 35–79.
   - Greene, Joshua D. (2014). _Moral Tribes: Emotion, Reason, and the Gap Between Us and Them._ Penguin.
   - _Contribution:_ Greene's dual-process model — distinguishing automatic, affect-driven intuitions (System 1) from controlled, principle-based reasoning (System 2) — provides a framework for classifying the cognitive systems implicated by moral intuition pumps. His finding that "personal" moral dilemmas (involving physical contact and intended harm) engage emotional processing while "impersonal" dilemmas engage cognitive processing has direct application to the analysis of trolley-style pumps. Used in: Step 1 (mechanism classification), Step 5 (framing detection — specifically, whether the pump's narrative features trigger affective vs. cognitive processing), Step 6 (process debunking based on dual-process architecture).

7. **Debunking Arguments in Metaethics and Metaphysics.**
   - Street, Sharon (2006). "A Darwinian Dilemma for Realist Theories of Value." _Philosophical Studies_ 127(1): 109–166.
   - Kahane, Guy (2011). "Evolutionary Debunking Arguments." _Nous_ 45(1): 103–125.
   - Nichols, Shaun (2014). "Process Debunking and Ethics." _Ethics_ 124(4): 727–749.
   - _Contribution:_ These works formalize the logic of debunking arguments — explaining why an intuition exists without reference to its truth — and provide evaluative criteria for determining whether a debunking argument succeeds. Street's evolutionary debunking challenges moral realism directly. Kahane provides a taxonomy of debunking arguments and identifies the conditions under which they succeed or fail. Nichols develops the distinction between evolutionary and process debunking and argues that process debunking can succeed even where evolutionary debunking fails. Used in: Step 6 (debunking susceptibility evaluation), Step 9 (verdict formulation).

8. **Cognitive Phenomenology and the Feeling of Rightness.**
   - Thompson, Valerie A., Jamie A. Prowse Turner, and Gordon Pennycook (2011). "Intuition, Reason, and Metacognition." _Cognitive Psychology_ 63(3): 107–140.
   - Thompson, Valerie A., and Kinga Morsanyi (2012). "Analytic Thinking: Do You Feel Like It?" _Mind and Society_ 11(1): 93–105.
   - _Contribution:_ This research examines the metacognitive experience accompanying intuitions — the "feeling of rightness" (FOR) — and how it interacts with analytic reasoning. A high FOR can suppress analytic engagement, leading subjects to endorse intuitively compelling but incorrect answers. This has direct application to intuition pump analysis: a pump that generates a strong feeling of rightness may discourage the critical scrutiny that would reveal its flaws. Used in: Step 4 (cognitive transparency), Step 5 (framing detection — specifically, whether the pump's rhetorical posture generates an artificially inflated FOR).

---

## 5. Steps

Execute the following analytical steps in sequence. Each step builds on the output of the preceding ones. The analysis should be thorough at each step; do not defer difficult judgments to later steps.

**Step 1: Identify the Pump Mechanism.**

Extract the pump from its textual and dialectical context. Identify exactly which features of the scenario are doing the cognitive work — which details are load-bearing for the intuition and which are incidental. A pump is not merely its abstract structure; it is the concrete scenario as presented, with all its narrative particularities.

Classify the mechanism by the cognitive faculty it targets. The pump may target _perceptual seemings_ (the scenario looks a certain way, and the intuition is an intellectual analog of perceptual experience); _conceptual competence_ (the scenario probes the boundaries of a concept by presenting a borderline or contested case); _moral sentiment_ (the scenario activates affective responses — disgust, outrage, compassion — to normatively charged situations); _modal imagination_ (the scenario asks whether a state of affairs is conceivable, and the intuition is that it is genuinely possible); _memory-based recognition_ (the scenario invokes pattern recognition from past experience, triggering a "that's just like..." response); _linguistic competence_ (the scenario queries grammaticality or semantic judgments that native speakers are supposed to make automatically); _practical reasoning_ (the scenario presents a choice situation, and the intuition is about what an agent ought to do); or _mathematical or logical intuition_ (the scenario presents an abstract structure, and the intuition is that a certain axiom or inference is self-evident).

Many pumps target hybrid mechanisms. For example, trolley problems target both moral sentiment (the affective response to pushing vs. pulling a switch) and practical reasoning (the calculation of consequences). The classification should identify the primary mechanism and any secondary mechanisms, noting where they interact or conflict. A particularly important interaction is between affective and cognitive mechanisms: a pump may trigger an affective response that is then rationalized as a principled judgment, and the analysis must distinguish the causal driver from the post hoc rationalization.

**Step 2: Reconstruct the Intuition-to-Judgment-to-Premise Chain.**

Map the inferential path in three stages with explicit propositions at each stage.

_Stage A — Raw Intuitive Response:_ What does the reader feel, sense, or find themselves inclined to think upon encountering the pump? This is a psychological state, not yet articulated as a proposition. It may be a feeling of wrongness, a sense that something is amiss, an inclination to classify the case one way rather than another, or a phenomenology of obviousness. The raw intuitive response is often inchoate and may admit of multiple propositional articulations.

_Stage B — Propositional Judgment:_ The articulated propositional content extracted from the intuitive response. What proposition does the reader judge to be true on the basis of the intuition? This is the first stage at which truth-evaluable content appears. The propositional judgment typically takes the form "In this case, X is F" or "In this case, agent A ought to phi." The analysis must verify that the propositional judgment is genuinely supported by the raw intuitive response and not an over-interpretation. A common failure mode: the raw intuition supports a vague, qualified judgment, but the argument requires a precise, unqualified premise, and the transition is made without acknowledgment.

_Stage C — Argumentative Premise:_ The role that the propositional judgment plays in the larger argument. This typically involves generalization: from "In this case, X is F" to "Therefore, the concept of F does not reduce to conditions C1...Cn" or "Therefore, the theory that...is false." The analysis must identify whether the generalization is licensed by the particular judgment. A pump that elicits a particular judgment does not automatically warrant a universal conclusion; the inferential gap between the particular and the general must be made explicit and assessed.

The reconstruction should also check for _imported content_: does the pump rely on background assumptions, theoretical commitments, or conceptual frameworks that are not themselves supported by the pump? If the reader must already accept a substantive theoretical framework for the pump to elicit the intended intuition, then the pump is question-begging, and this must be flagged.

**Step 3: Classify the Intuition Type.**

Assign the intuition to one or more categories using a principled taxonomy:

- _Categorization intuitions:_ Is X an instance of kind K? (e.g., the Gettier intuition that Smith's belief is not knowledge.)
- _Moral intuitions:_ Is action A permissible, obligatory, or wrong? (e.g., the trolley intuition that pushing is wrong but switching is permissible.)
- _Modal intuitions:_ Is P possible, necessary, or contingent? (e.g., the zombie intuition that a physical duplicate without consciousness is conceivable and therefore possible.)
- _Conceptual intuitions:_ Does concept C apply to case S? (e.g., the Twin Earth intuition that "water" does not refer to XYZ.)
- _Epistemic intuitions:_ Does S know that P? Is belief B justified? Is evidence E sufficient? (Gettier cases again, but also fake barn cases, lottery paradox intuitions, etc.)
- _Semantic intuitions:_ Does term T refer to R in scenario S? Is sentence S true in context C?
- _Mathematical or logical intuitions:_ Is axiom A self-evident? Is inference rule R valid?
- _Phenomenological intuitions:_ What is it like to undergo experience E? (e.g., the Mary's room intuition that Mary learns something new upon seeing red.)
- _Metaphysical intuitions:_ Does object O persist through change C? Is property P intrinsic or extrinsic? Is relation R fundamental or grounded?

Note that many pumps target hybrid intuition types, and classification can be contested. The Gettier intuition is both a categorization intuition and an epistemic intuition. The trolley intuition is both a moral and a practical intuition. The classification is not an end in itself but a tool for determining which cognitive faculties are implicated and therefore which debunking arguments, empirical studies, and alternative framings are relevant.

**Step 4: Assess the Pump's Cognitive Transparency.**

Determine whether the pump's mechanism is cognitively transparent — that is, whether the reader can see how the pump's features generate the intuition and can critically evaluate whether those features genuinely license the inference.

A pump is _cognitively transparent_ when (a) the features of the scenario that drive the intuition are identifiable by the reader upon reflection, (b) the inferential path from scenario features to intuitive judgment is available to conscious scrutiny, and (c) the reader can evaluate whether those features are genuinely truth-conducive in the relevant domain. Transparent pumps invite critical engagement: the reader can ask "Is this feature doing legitimate cognitive work, or is it a rhetorical device?" and can answer that question by reasoning about the pump.

A pump is _cognitively opaque_ when the intuition is elicited by psychological processes that operate below the threshold of conscious awareness or control. The pump may exploit implicit associations (e.g., pairing a disfavored view with negative imagery), affective priming (e.g., using emotionally charged language to create a visceral response that is then attributed to the scenario's normative features), fluency heuristics (e.g., making one option easier to process than another), or anchoring effects (e.g., presenting a numeric anchor that shapes subsequent judgments). Opaque pumps are not automatically illegitimate — many legitimate cognitive processes operate below conscious awareness — but their opacity is a methodological liability that must be flagged. The pump's dialectical force is reduced to the extent that the reader cannot distinguish between (a) an intuition that tracks the target phenomenon and (b) an intuition that is an artifact of the pump's construction.

The analysis should also evaluate the _feeling of rightness_ (FOR) that the pump generates, drawing on Thompson et al. (2011). A pump that generates an artificially high FOR — through rhetorical confidence, professional authority, or narrative vividness — may discourage the analytic engagement that would reveal its flaws. The analysis must distinguish between the genuine epistemic confidence that a well-constructed pump warrants and the metacognitive illusion of confidence that a rhetorically effective pump manufactures.

**Step 5: Check for Framing, Ordering, and Bias Effects.**

Systematically examine the pump's narrative construction for features that may bias intuitive responses. This step operationalizes the Kahneman-Tversky framework within philosophical argument analysis.

_Ordering effects:_ Does the sequence in which information is presented influence the intuition? Would presenting the same information in a different order — or presenting countervailing information before the pump's key features — alter the intuitive response? This is particularly relevant for pumps that build narrative momentum, leading the reader through a sequence of increasingly loaded claims before arriving at the intuition.

_Affective framing:_ Does the language carry affective valence that could be neutralized? Are emotionally charged terms — "murder," "innocent," "sacrifice," "violation" — doing argumentative work that should be done by the scenario's structural features? The analysis should test whether the intuition survives neutral redescription. If replacing "murder" with "killing" or "innocent" with "uninvolved" alters the elicited intuition, then affect is doing work that structure is not.

_Implicit contrast cases:_ Is the reader's judgment anchored by an unstated comparison? A pump that presents scenario S as eliciting intuition I may depend on the reader's contrasting S with an implicit S* that is never stated. The analysis should make the implicit contrast explicit and assess whether the intuition depends on the contrast or on S itself.

_Selective description:_ What does the author choose to mention or omit, and would including omitted details alter the intuition? This is the most common framing effect in philosophical pumps. Authors highlight features that support the intended intuition and omit features that would militate against it. The analysis should identify what is omitted and, where possible, construct a version of the pump that includes the omitted features to test whether the intuition survives.

_Rhetorical posture of inevitability:_ Phrases like "surely," "obviously," "one cannot help but judge," "it is clear that," and "any reasonable person would agree" are not arguments; they are social-pressure mechanisms that discourage dissent. The analysis should flag these and assess whether the intuition would be compelling without them.

_Anchoring effects:_ Does the pump present an initial claim — numerical, descriptive, or evaluative — that serves as an anchor for subsequent judgments? For example, a pump that begins "Suppose a doctor could save five patients by..." has already anchored the reader to the five-to-one ratio, potentially shaping subsequent judgments about proportionality.

For each detected framing feature, the analysis should propose a neutral re-description that preserves the pump's structural core while removing the biasing element. If the intuition does not survive neutral re-description, then the pump's dialectical force is substantially weakened — the intuition is an artifact of the framing, not a response to the scenario's philosophically relevant features.

**Step 6: Evaluate Debunking Susceptibility.**

Systematically evaluate whether the intuition is vulnerable to debunking explanations. This step considers three families of debunking argument.

_Evolutionary debunking (Street 2006, Kahane 2011):_ The intuition is a byproduct of selection pressures that favored fitness-enhancing responses rather than truth-tracking ones. For example, the intuition that incest is wrong may be explained by evolved kin-recognition and incest-avoidance mechanisms; the intuition that pushing is worse than switching may be explained by evolved aversions to physical contact with conspecifics. The debunking argument runs: (1) the intuition is explained by evolutionary pressures that are independent of the truth of the intuited proposition; (2) there is no reason to think that evolutionary pressures in this domain tracked truth; therefore (3) the intuition does not provide evidence for the truth of the intuited proposition. The analysis must evaluate both premises: is the evolutionary explanation genuinely adequate? And is it genuinely independent of truth? Some evolutionary explanations are consistent with truth-tracking (e.g., evolved mathematical intuitions may track mathematical truth because survival required accurate quantity estimation), and the analysis must distinguish these from genuinely debunking explanations.

_Process debunking (Nichols 2014):_ The intuition arises from cognitive processes known to be unreliable in the relevant domain. This differs from evolutionary debunking in not requiring an evolutionary story — the processes may be culturally acquired, developmentally normal, or individually learned, and they are debunked because they are demonstrably unreliable. For example, if a moral intuition is driven by the affect heuristic (the tendency to judge risks and benefits based on emotional valence), and the affect heuristic is known to produce systematic errors in domains with similar structure, then the intuition is process-debunked. The analysis must evaluate (a) whether the process is genuinely implicated in generating the intuition, (b) whether the process is genuinely unreliable in the relevant domain, and (c) whether the intuition can be generated by alternative, reliable processes even if it is also generated by the unreliable one.

_Genealogical debunking:_ The intuition's causal origins — in culture, upbringing, or contingent historical circumstances — are independent of the truth it purports to track. This is a broader form of debunking that does not require an evolutionary or process-reliability story, only a demonstration that the intuition would exist regardless of whether it is true. For example, if a semantic intuition about reference is shown to be an artifact of a particular philosophical tradition rather than a deliverance of universal semantic competence, it is genealogically debunked. The analysis must evaluate whether the genealogical explanation is genuinely adequate and genuinely independent of truth.

For each debunking argument that is plausibly applicable, the analysis states the argument in premise-conclusion form, evaluates its soundness, and classifies the outcome: (a) fully debunking — the intuition carries no evidential weight; (b) partially debunking — the intuition carries less weight than initially supposed; (c) consistent with truth-tracking — the debunking explanation is compatible with the intuition's being reliable; or (d) inapplicable — the debunking argument does not target this type of intuition.

**Step 7: Determine Whether the Intuition Carries the Argumentative Weight.**

Integrate the findings from Steps 1–6 to determine whether the intuition pump successfully supports the conclusion it is enlisted to serve.

This step requires calibrating the burden the pump bears against the pump's performance across the analytical dimensions. A pump that is offered as a decisive counterexample to a universal claim must meet a higher standard than a pump that is offered as one data point in a wide reflective equilibrium. The analysis must therefore assess (a) what the argument needs the pump to do, (b) whether the pump has done it, and (c) if the pump has only partially done it, whether the shortfall is fatal.

Evaluate the following dimensions:

- _Mechanism adequacy:_ Does the pump actually target the cognitive faculty it needs to target? A pump designed to elicit a conceptual intuition that in fact elicits a moral intuition is a mechanism mismatch, and the elicited intuition may not support the intended conclusion.
- _Chain integrity:_ Are there gaps in the intuition-to-judgment-to-premise chain that the argument requires to be closed? If the raw intuition supports a vague judgment but the argument needs a precise premise, the pump falls short.
- _Empirical robustness:_ Is the intuition widely shared, cross-culturally stable, and resistant to framing? A contested or variable intuition cannot bear heavy dialectical weight unless there is a principled argument for privileging one population's intuitions over another's.
- _Debunking resistance:_ Does the intuition survive the debunking arguments that target it? An intuition that is fully debunked carries no weight. An intuition that is partially debunked carries reduced weight.
- _Framing independence:_ Does the intuition survive neutral re-description, or is it an artifact of the pump's narrative construction? A framing-dependent intuition carries little weight because there is no reason to prefer the author's framing to alternative framings that would yield different intuitions.

State a confidence level: high confidence (convergent support from multiple analytical dimensions, the pump performs well across the board), moderate confidence (some dimensions favorable, others unfavorable, reasonable disagreement about the overall assessment), or low confidence (conflicting signals, insufficient evidence, or the pump is too ambiguous for confident evaluation).

**Step 8: Assess Dialectical Alternatives If the Intuition Is Rejected.**

Map the argumentative landscape under the counterfactual supposition that the intuition is not granted — either because it is contested, debunked, or simply not shared by the interlocutor. This step is essential because a pump that is dialectically inert (the argument survives without it) is analytically interesting in a different way from a pump that is dialectically load-bearing (the argument collapses without it).

Five outcomes are possible:

_Collapse:_ The argument depends entirely on the intuition, which is both load-bearing and contested. If the interlocutor does not share the intuition, the argument provides no independent reason to accept the conclusion. Example: a perceptual dogmatist argument that depends entirely on the intuition that perceptual seemings provide immediate justification, where that intuition is precisely what the skeptic contests.

_Weakening:_ The argument depends partly on the intuition, but other premises do independent work, and the conclusion may still be plausible — just less well-supported — without it. Example: a cumulative-case argument for moral realism in which one intuition pump is found wanting but others survive.

_Restructuring:_ The argument can be reformulated to reach the same or a similar conclusion without relying on the contested intuition. The pump may have been illustrative rather than essential, or there may be alternative argumentative routes to the same conclusion. The analysis should specify what the restructured argument looks like and whether it is dialectically stronger or weaker than the original.

_Burden-shifting:_ Even if the intuition is not treated as evidence, its apparent compellingness requires explanation from the opponent. The pump shifts the dialectical burden: the opponent must explain why a widely shared, psychologically robust intuition is nevertheless false. This is a weaker dialectical role than providing direct evidence, but it is a genuine dialectical role. The analysis should assess whether the burden-shifting is successful — that is, whether the opponent genuinely owes an explanation, or whether the pump's compellingness has already been accounted for (e.g., by debunking).

_Overdetermination:_ The conclusion is independently supported by other arguments, and the intuition pump is redundant. In this case, the pump analysis is still valuable — it identifies that a particular argumentative move is unnecessary and potentially distracting — but the pump does not affect the overall dialectical situation. The report should note the overdetermination without concluding that the pump is worthless; even redundant pumps can serve expository, pedagogical, or heuristic functions.

The analysis should specify which outcome applies and justify the classification with reference to the argument's structure and the pump's role within it.

---

## 6. Quality Criteria

A high-quality intuition pump analysis satisfies the following criteria:

1. **Mechanism Precision.** The pump mechanism is identified with sufficient specificity that a reader unfamiliar with the philosophical literature can understand which cognitive faculty is being targeted and how the pump's features are designed to engage it. Vague classifications — "this is a moral intuition" — are replaced with precise diagnoses — "this pump targets the affective disgust response via a vivid description of bodily violation, which is then recruited to support a deontological constraint on harm, without the reader's consciously recognizing that affect rather than principle is driving the judgment." Precision enables evaluation: a precisely identified mechanism can be tested; a vaguely identified mechanism cannot.

2. **Chain Completeness.** The reconstruction of the intuition-to-judgment-to-premise chain identifies every inferential step, including implicit enrichments that the author may have treated as obvious but that are in fact substantive. No gap between "what the reader feels" and "what the argument needs" is glossed over. If the chain contains an inference that goes beyond the intuition — for example, from "this particular case is not knowledge" to "no analysis of knowledge in terms of justified true belief plus condition X can succeed" — that inference is separately identified and evaluated.

3. **Empirical Grounding.** Claims about whether an intuition is "widely shared," "universal," or "intuitive" are supported by citation of experimental philosophy studies where available, or explicitly flagged as unverified armchair speculation where such studies do not exist. Speculation about psychological mechanisms — "this pump likely exploits the availability heuristic" — is distinguished from empirically established findings — "studies by ... demonstrate that this pump exploits the availability heuristic." The absence of empirical evidence is not taken to indicate consensus; it is reported as a gap.

4. **Debunking Rigor.** Debunking arguments are reconstructed with the same charity and precision as the pump itself. The analysis does not treat debunking as automatically successful; each debunking argument is evaluated for soundness, and debunking failures are noted alongside debunking successes. A common failure mode in intuition pump analysis is to cite a debunking argument as though its mere existence undermines the intuition, without evaluating whether the debunking argument's premises are true and whether they genuinely entail the intuition's evidential impotence. This skill avoids that failure mode.

5. **Framing Sensitivity.** The analysis identifies specific textual features — specific words, phrasings, ordering decisions, and omissions — that may bias intuitive responses. It proposes at least one alternative framing that would test whether the intuition survives neutral redescription. This is not a demand that all philosophical prose be affectively flat; philosophical writing legitimately employs rhetoric. The criterion is that the analysis must flag when rhetoric is doing more work than argument, and it must distinguish between rhetoric that illuminates and rhetoric that manipulates.

6. **Dialectical Mapping.** The report situates the pump within the broader argumentative architecture and assesses what happens to the argument if the pump fails. An analysis that stops at "the intuition is suspect" without tracing the downstream consequences is incomplete. The dialectical mapping answers the question: "Does it matter that this pump fails?" In some cases, the answer is "no" — the pump is redundant and the argument survives intact — and that finding is itself a valuable contribution.

7. **Neutral Tone.** The analysis maintains methodological neutrality throughout. It does not assume that intuitions are epistemically worthless or that armchair methodology is bankrupt. It does not assume that intuitions are reliable guides to philosophical truth or that experimental philosophy critiques are overblown. The analytical framework treats intuition pumps as cognitive artifacts to be evaluated, not as targets to be debunked or defended. The verdict — whether laudatory, critical, or mixed — follows from the analysis and is presented as defeasible, not as a final settlement of the philosophical question.

8. **Defeasibility Acknowledgment.** Every verdict includes an explicit acknowledgment of its own defeasibility. The analysis identifies which findings could overturn the verdict if new evidence emerged — e.g., "the verdict that this intuition is dialectically weak depends on the finding that the intuition varies cross-culturally; if future studies find the variation to be an artifact of translation or comprehension, the verdict would shift to dialectically weighty but defeasible." This criterion ensures that the analysis is a contribution to ongoing inquiry, not a premature closure.

---

## 7. Relations to Other Skills

**Depends on:**

- **`method.concept.thought-experiment`** — Provides the foundational analysis of thought experiments as a genre, including the distinction between destructive and constructive thought experiments, the role of particularity and generality, the relationship between the scenario's narrative features and its logical structure, and the taxonomy of thought-experiment functions (counterexample, illustration, consistency test, possibility proof, explanation). The intuition pump skill presupposes that the target has already been identified as a thought experiment and builds on that genre analysis to examine the specifically intuition-eliciting features. For pumps that are not formally structured as thought experiments but as looser vignettes, anecdotes, or cases, `method.concept.thought-experiment` provides the baseline template for extracting the core logical structure and distinguishing the pump's argumentative content from its rhetorical dressing.

- **`method.argument.argument-reconstruct`** — Supplies the fully reconstructed argument in which the intuition functions as a premise or dialectical move. The intuition pump analysis cannot proceed unless the pump's argumentative embedding is clear: what role does the intuition play, what does it support, and what depends on it? `method.argument.argument-reconstruct` provides the premise-conclusion map, identifies the logical structure (deductive, inductive, abductive, analogical), and specifies the dialectical context. The intuition pump analysis then interrogates the intuition-premises in that map, assessing whether they can bear the weight the argument assigns to them.

- **`method.concept.conceptual-analysis`** — Many intuition pumps are designed to probe the boundaries of a concept — they present a borderline or contested case and elicit an intuition about whether the concept applies. `method.concept.conceptual-analysis` provides the framework for understanding what kind of conceptual work the pump is doing: is it testing necessary and sufficient conditions, exploring prototype structure, or investigating the concept's normative dimensions? The intuition pump analysis builds on this to assess whether the pump genuinely illuminates the concept or merely exploits its vagueness.

**Feeds into:**

- **`method.argument.counterexample`** — When a pump functions as a counterexample to a universal claim, the intuition pump analysis provides the materials for evaluating whether the counterexample succeeds. Specifically, if the intuition elicited by the pump is debunking-susceptible, framing-dependent, or culturally specific, the counterexample may fail even if it is intuitively compelling. The counterexample analysis uses the pump analysis to determine whether the particular case genuinely falsifies the universal claim or merely appears to.

- **`method.dialectic.methodology`** — The findings of repeated intuition pump analyses bear directly on methodological debates about the role of intuitions in philosophical argument. A corpus of pump analyses can reveal patterns: whether a particular philosopher's argumentative practice systematically relies on culturally specific or affectively driven intuitions; whether certain domains (normative ethics, modal metaphysics, conceptual analysis) are disproportionately dependent on pumps with low dialectical force; and whether the "method of cases" as a general philosophical methodology survives systematic scrutiny of its canonical deployments. The pump analysis skill is thus a methodological instrument: it operationalizes the critique of armchair philosophy by providing a systematic, case-by-case evaluation framework.

- **`method.argument.charity-check`** — An intuition pump analysis that finds a pump to be dialectically weak may trigger a charity check: is there a stronger version of the pump, or an alternative interpretation under which it succeeds? The charity-check skill provides the framework for determining whether the pump, charitably reconstructed, performs better than the analysis suggests. This is particularly relevant when the pump's author is a major figure whose argumentative competence should not be hastily dismissed.

**References:**

- **`thought-experiment-templates.md`** — A reference document cataloging common intuition pump templates and their characteristic mechanisms. Templates include: the "bystander vs. participant" framing in trolleyology, the "fake barn" template in epistemology, the "twin" template in semantics (Twin Earth, Twin Oscar, Twin Earthlings), the "pre-established harmony" template in philosophy of mind, the "experience machine" template in value theory, the "transparent eyeball" template in philosophy of perception, the "swampman" template in teleosemantics, and the "Frankfurt-style" template in free will debates. When an analyzed pump instantiates a known template, the template reference provides comparative leverage: how have parallel pumps been analyzed, what framing effects are characteristic of this template, and what debunking arguments have been advanced against it? The reference also documents template variants — how canonical pumps have been modified to resist standard objections — which is useful for assessing whether the pump in question incorporates the standard modifications or is vulnerable to known countermoves.

---

## 8. Boundary Conditions

The following edge cases define the limits of the skill's analytical purview. When a case exhibits one or more of these features, the analysis should explicitly note the limitation and proceed with appropriate caution, or in some cases decline to apply the framework.

**1. Intuitively Compelling but Empirically False.**

Some intuitions are widely shared and psychologically robust yet demonstrably false. The Muller-Lyer illusion is the paradigm: the intuition that the lines differ in length persists even when the subject knows — has measured and confirmed — that they are equal. The intuition is cognitively impenetrable: knowledge of the truth does not dissolve it. In philosophical contexts, certain metaphysical, semantic, or moral intuitions may be similarly persistent despite being in tension with our best theories. For example, some philosophers report that the intuition that consciousness is non-physical persists even after they have accepted physicalism on theoretical grounds. The analysis must distinguish between the _felt compellingness_ of an intuition — which can survive empirical or theoretical refutation — and its _evidential value_ — which cannot. An intuition that survives debunking in the psychological sense (the person continues to feel its pull) may nonetheless be debunked in the epistemic sense (it provides no reason to believe). The Muller-Lyer case is instructive: no one treats the persistent illusion as evidence that the lines really differ in length. The analysis must determine whether the philosophical intuition in question is analogous — a cognitive illusion that deserves no more epistemic deference than the Muller-Lyer — or whether the persistence of the intuition in the face of contrary theory is itself evidence that the theory is incomplete.

**2. Culturally Specific Intuitions.**

An intuition that is robustly shared within one cultural or linguistic community but absent or reversed in another presents a special challenge. The experimental philosophy literature documents numerous cases: East Asian participants diverge from Western participants on epistemic intuitions about Gettier cases and reference intuitions about proper names; socioeconomic status predicts intuitions about moral responsibility; political orientation predicts intuitions about free will. The analysis must determine whether the cultural variation is philosophically significant or whether it can be explained away. Two positions must be evaluated. The _expertise position_ holds that one culture's intuitions are more reliable — because that culture has better conceptual tools, more relevant experience, or a philosophical tradition that has refined intuitive judgment in the relevant domain. The _no-fault-disagreement position_ holds that the variation is undecidable and neither community's intuitions are epistemically privileged. The analysis should not automatically treat culturally specific intuitions as debunked; cultural variation does not entail that all variants are equally unreliable, and some cultural traditions may genuinely track philosophical truth better than others. But the burden of proof is on the proponent of culturally specific intuitions to provide a non-question-begging reason for privileging their community's intuitive responses. Absent such a reason, the intuition carries weight only for interlocutors who already belong to the relevant community, which limits its dialectical force in cross-cultural philosophical exchange.

**3. Expert vs. Lay Intuitions.**

Some philosophers defend the epistemic credentials of _philosophers'_ intuitions while conceding that untutored lay intuitions are unreliable. This "expertise defense" — that philosophical training refines intuitive judgment much as chess training refines positional intuition or radiology training refines perceptual diagnosis — is contested. Empirical evidence is mixed: some studies find that philosophers' intuitions are more stable and less subject to framing effects than lay intuitions; others find that philosophical training has no effect on intuitive reliability in the relevant domains, or that philosophers' intuitions are subject to the same biases but philosophers are better at post hoc rationalization. The analysis must evaluate whether the pump is designed to elicit lay intuitions (the reader is meant to respond as an ordinary person, and the pump's force depends on the ordinariness of the response) or expert intuitions (the reader is expected to bring specialized conceptual competence, theoretical knowledge, or dialectical experience to bear on the case). If the pump targets lay intuitions but the argument requires expert-level discrimination — for example, if the pump asks the reader to intuit a subtle modal distinction that only trained metaphysicians can reliably draw — then there is a mismatch that weakens the pump. Conversely, if the pump is designed for expert consumption and the expertise defense holds, then lay variation data may be irrelevant.

**4. The "Intuition" Label as a Term of Dismissal.**

In some dialectical contexts, labeling an opponent's judgment an "intuition" — or worse, a "mere intuition" — is a rhetorical move designed to downgrade its epistemic status without engaging its content. The label functions as a conversation-stopper: "That is just your intuition" implies that the judgment is subjective, unreasoned, and not entitled to dialectical consideration. The analysis must distinguish between (a) cases where the "intuition" label is analytically justified — the judgment genuinely arises from an intuitive cognitive process and has the epistemic profile of an intuition — and (b) cases where "intuition" is deployed as a dialectical evasion — the judgment may be the product of reasoning, theoretical commitment, or evidence, and the "intuition" label is used to dismiss it without argument. When analyzing a pump that has been _dismissed_ as an intuition by an opponent, the analysis should evaluate whether the dismissal is warranted or whether it is an attempt to shift the burden of proof illegitimately. This requires examining the cognitive provenance of the judgment: is it genuinely an intuition (fast, automatic, affectively tinged, resistant to conscious control) or is it a considered judgment (slow, deliberative, explicitly reasoned)? If the latter, the "intuition" label is a category mistake that the analysis should flag.

**5. Genuinely Unanalyzable Gut Feelings.**

Some philosophical judgments resist analysis into pump mechanisms, cognitive faculties, and debunking pathways — not because the analysis is difficult, but because the judgment is phenomenologically primitive and lacks the structural features that the analytical framework presupposes. When a philosopher reports that a proposition "just seems true" without any identifiable narrative, scenario, case, or cognitive trigger — when the judgment presents itself as a bare intellectual seeming with no elicited component — the apparatus of intuition pump analysis may have no purchase. There is no pump to analyze, no mechanism to identify, no framing to detect. The analysis should acknowledge this limitation frankly: the skill is designed for _engineered_ intuitions — intuitions elicited by _constructed scenarios_ with identifiable features designed to trigger specific cognitive responses. It is not designed for bare intellectual seemings, intellectual appearances, or "rational intuitions" in the rationalist tradition (e.g., the intuition that everything must have a sufficient reason, or that a whole is greater than its part). If the target "pump" turns out to have no pump at all — no scenario, no mechanism, no engineered elicitation — the analysis should terminate with a classification of "not an intuition pump" and a referral to other skills: `method.argument.premise-detect` for treatment as an undefended premise, or `method.metaphysics.conceivability-arg` if the judgment is a modal seeming deployed in a conceivability argument. The boundary between engineered intuitions and bare seemings is not always sharp, and the analysis should err on the side of attempting pump analysis when the judgment is even partially elicited by a scenario.

---

## 9. ARS Interface

This skill integrates with the Academic Research System (ARS) pipeline across multiple phases of analysis.

**Pre-analysis Phase: Literature Retrieval and Verification.**

When a user invokes `/phil-intuition` and either provides or requests the optional inputs — experimental philosophy data, psychological literature on the relevant cognitive mechanisms, competing philosophical analyses of the same pump — the skill may trigger ARS queries to retrieve relevant empirical studies and secondary literature. The primary pathway is:

- `academic-research-skills:ars-lit-review` — Retrieves experimental philosophy studies, psychological research on the cognitive mechanisms implicated by the pump, and philosophical commentary on the pump and its variants. The lit review is scoped to the specific intuition or intuition family (e.g., "Gettier intuitions across cultures," "framing effects in trolley problems," "the expertise defense and modal intuitions").

- `academic-research-skills:ars-abstract` — When the pump is drawn from a specific philosophical text, retrieves the source paper's abstract and, where available, citation context (who cites the pump, how it has been received). This provides the author's own framing and indicates the pump's reception in the literature.

- `academic-research-skills:ars-citation-check` — During the analysis, if a debunking argument or empirical claim requires verification (e.g., "study X found that this intuition varies by culture," "debunking argument Y is generally regarded as successful"), the skill may issue targeted citation checks to verify that the cited studies exist, support the claimed finding, and have not been retracted, substantially qualified, or undermined by replication failures.

**Analysis Phase: Independent Operation.**

The skill operates independently of ARS during the core analytical process (Steps 1–8), drawing on its internal methodological framework. ARS is not called for the analytical reasoning itself — the pump analysis is a structured exercise in philosophical argument evaluation, not a literature review. However, when the analysis encounters an empirical question that is decisive for the verdict — e.g., "does the intuition survive neutral reframing?" when no reframing study exists in the retrieved literature — the skill may recommend (but not autonomously execute) an empirical investigation via ARS.

**Post-analysis Phase: Workflow Integration.**

After the structured report is generated, the findings may feed into downstream ARS workflows depending on the user's broader research objectives:

- **Rebuttal and critical commentary.** If the pump analysis reveals that a key intuition in a target paper is debunking-susceptible, framing-dependent, or empirically contested, the analysis report can be routed to `academic-research-skills:ars-rebuttal-audit` for integration into a rebuttal, critical commentary, or peer review. The pump analysis provides the detailed case against the intuition; the rebuttal audit embeds it in the broader critical argument.

- **Study design and empirical follow-up.** If the pump analysis identifies empirical gaps — no experimental philosophy studies on the relevant intuition, no cross-cultural data, no framing-manipulation studies — the report can trigger `academic-research-skills:ars-plan` to design a study protocol for testing the intuition's cross-cultural stability, framing sensitivity, or correlation with ground truth. This pathway operationalizes the experimental philosophy critique: the analysis identifies that an empirical question needs answering, and the ARS pipeline designs the study to answer it.

- **Full argument evaluation.** If the pump is embedded in a larger argument being reconstructed and evaluated, the pump analysis report feeds into `academic-research-skills:ars-full` as one analytical module within a comprehensive argument evaluation. The full evaluation integrates the pump analysis with other analytical modules — premise analysis, logical structure assessment, alternative argument mapping — to produce a complete assessment of the argument's dialectical force.

- **Revision coaching.** If the user is the author of the pump and the analysis identifies weaknesses, the report can be routed to `academic-research-skills:ars-revision-coach` for guidance on strengthening the pump — e.g., neutralizing framing effects, adding detail to block debunking interpretations, or restructuring the argument to reduce dependence on the contested intuition.

**Cache and Persistence.**

Pump analyses for canonical philosophical thought experiments — Gettier cases, trolley problems (bystander, footbridge, loop, and other variants), Twin Earth, Mary's room, Thomson's violinist, Frankfurt cases, the Chinese room, the experience machine, the utility monster, the original position, brains in vats, swampman, zombies, inverted spectra, the trolley problem's many variants, fake barn cases, Goldman's fake barn region, Lehrer's Truetemp, Parfit's teletransporter, Williams's Gauguin, and others — may be cached via `academic-research-skills:ars-cache-invalidate` and reused across sessions when the same pump is encountered in different argumentative contexts. The cache key should include: (a) the pump identifier (canonical name or structural description), (b) the target argument (since the same pump can play different roles in different arguments), and (c) the analytical framework version (1.0.0). Cached analyses should be reviewed for freshness when reused; new empirical literature or philosophical commentary may require updating the analysis.

**Disclosure and Provenance.**

All ARS-mediated research findings incorporated into the pump analysis must be disclosed in the output report with full provenance information, following `academic-research-skills:ars-disclosure` standards. This includes: source identification (author, title, venue, year, DOI or URL), retrieval date, the specific claim for which the source is cited, and any limitations, caveats, or conflicts of interest reported by the original studies. The disclosure requirement serves both epistemic transparency and dialectical fairness: the reader should be able to verify that the empirical claims in the pump analysis are genuinely supported by the cited literature, and the author of the pump should be able to assess whether the empirical evidence deployed against their intuition is sound.

## Conditional references

Loaded only on a live ambiguity or an explicit request — never with this method by default: `references/intuition-pump-checklist.md`, `references/intuition-pump-examples.md`.
