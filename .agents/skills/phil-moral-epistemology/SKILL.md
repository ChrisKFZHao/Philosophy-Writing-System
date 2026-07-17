---
name: phil-moral-epistemology
description: "Moral Epistemology Analysis — evaluate the possibility of moral knowledge; analyze intuitionist, coherentist, and reliabilist justification pathways; assess evolutionary debunking challenges"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Moral Epistemology Analysis

## Overview

How, if at all, we can have moral knowledge is a foundational question that constrains metaethical theory choice. If moral realism is true but moral knowledge is impossible, then moral realism is an empty doctrine — there are moral facts, but we can never access them, and our moral practices are systematically unjustified. If moral knowledge is possible, the epistemology must be compatible with the metaphysics and semantics of the moral domain. This skill provides a systematic framework for analyzing an argument's epistemological commitments, identifying its justification pathway, and evaluating its vulnerability to skeptical challenges — most notably the evolutionary debunking challenge, which has emerged as one of the most powerful skeptical arguments in contemporary metaethics.

The skill is designed to be applied after an argument-reconstruction report has been produced and, ideally, after a moral-realism analysis has classified the argument's metaphysical commitments. Different forms of realism (naturalist, non-naturalist, constructivist) carry different epistemological burdens and are vulnerable to different skeptical challenges. The epistemological analysis must be sensitive to these differences: a naturalist realist who identifies moral properties with natural properties may have an easier epistemological story to tell than a non-naturalist who posits sui generis moral properties accessible only through a special faculty of moral intuition.

The skill covers five main justification pathways. First, intuitionism (Moore, Ross, Audi) holds that we have direct, non-inferential justification for at least some moral beliefs through rational intuition or intellectual seeming — we "just see" that certain things are right or wrong. Second, coherentism holds that moral beliefs are justified by their coherence with other beliefs in a reflective equilibrium (Rawls) — no belief is foundational; justification is holistic. Third, reliabilism holds that moral beliefs are justified if they are produced by a reliable belief-forming process — the epistemology need not be accessible to the believer. Fourth, rationalism holds that moral truths are knowable a priori through reason alone, analogous to mathematical knowledge. Fifth, perceptual models (McGrath, Audi) hold that moral properties can be literally perceived in a way analogous to secondary qualities.

A major focus of the skill is the evolutionary debunking challenge, articulated most influentially by Sharon Street (2006) and Richard Joyce (2006). The challenge takes the form of a dilemma: either the evolutionary forces that shaped our moral beliefs tracked the moral truth, or they did not. If they did not, then our moral beliefs are unjustified — they are explained by fitness-enhancing effects, not truth-tracking. If they did, the realist owes an account of how this tracking relation works, and it is not clear such an account can be provided. The skill requires the analyst to apply this dilemma to the argument's epistemological commitments and assess whether a "third-factor" response (Enoch, Shafer-Landau, Copp) can defuse the challenge.

The skill also addresses the relationship between moral epistemology and the broader architecture of justification. The reflective equilibrium method, central to much contemporary moral philosophy, receives special attention: the analyst must assess whether the argument's appeal to reflective equilibrium is merely an appeal to coherence (and thus vulnerable to the isolation objection — a coherent set of false beliefs can be in equilibrium) or whether it incorporates a more robust, foundationalist element.

Finally, the skill considers the interplay between moral epistemology and moral disagreement. If widespread peer disagreement about morality is acknowledged, the epistemological implications must be assessed. Does disagreement undermine the reliability of moral intuition? Does it block the route to moral knowledge even if moral facts exist?

## Input

**Required:**
- `argument-reconstruction report` — A completed argument-reconstruction analysis report from the `phil-argument-reconstruct` skill. The epistemological analysis depends on a clear understanding of what the argument claims about how we know moral truths, what justificatory structure it assumes or argues for, and what epistemological commitments are implicit in its premises or methodology.

**Optional:**
- `moral-realism analysis report` — A completed moral-realism analysis report from the `phil-moral-realism` skill. This is valuable because the epistemological commitments and vulnerabilities of an argument depend on its metaphysical commitments. A non-naturalist realist faces different epistemological challenges than a naturalist realist or a constructivist.
- `moral-disagreement analysis report` — A completed Moral Disagreement Analysis Report from the `phil-moral-disagreement` skill. Disagreement bears directly on moral epistemology, especially if the argument makes conciliationist claims or relies on the convergence of moral judgments.
- `evolutionary-psychology evidence dossier` — Relevant empirical evidence about the evolutionary origins of moral cognition. This is relevant when the argument's epistemological claims are challenged on evolutionary debunking grounds.

**Input format:** Structured reports as Markdown documents. The analyst should verify that the argument-reconstruction report identifies the argument's epistemological claims before proceeding.

**Preconditions:** The argument must make or presuppose epistemological claims about how moral knowledge is acquired or justified. Arguments that are purely metaphysical or semantic without epistemological commitments do not trigger this skill (though most moral arguments have at least implicit epistemological commitments that can be surfaced).

## Output

The output is a structured **Moral Epistemology Analysis Report** containing the following sections:

1. **Justification Pathway Classification** — A precise classification of the argument's justification pathway, with sub-type specification:
   - *Intuitionist:* Rational intuition, intellectual seeming, self-evidence, prima facie duties (Ross), moderate intuitionism (Audi)
   - *Coherentist:* Reflective equilibrium (narrow/wide), holistic justification, coherence as the sole criterion
   - *Reliabilist:* Process reliabilism, indicator reliabilism, virtue epistemology, proper functionalism
   - *Rationalist:* A priori reason, conceptual analysis, transcendental arguments
   - *Perceptual:* Moral perception (McGrath), perceptual analogy, secondary quality model
   - *Hybrid:* Combinations of the above (e.g., intuitionist foundationalism with coherentist superstructure)

2. **Epistemic Access Mechanism** — An account of the specific mechanism by which, according to the argument, moral truths are accessed or moral beliefs are formed. This includes:
   - The cognitive faculty or process involved (reason, intuition, perception, emotion, empathy, social learning)
   - The phenomenological character of the access (is it inferential or immediate? Does it involve a distinctive "seeming"?)
   - The scope of the mechanism (what range of moral truths does it purport to deliver?)
   - The reliability conditions (under what conditions is the mechanism reliable, and are those conditions typically met?)

3. **Skeptical Challenge Assessment** — A systematic evaluation of skeptical challenges to the claimed justification pathway:
   - *Evolutionary debunking:* Does the evolutionary explanation of our moral beliefs undermine their justification? Is the tracking premise defensible?
   - *Disagreement-based skepticism:* Does pervasive moral peer disagreement undermine the reliability of the claimed access mechanism?
   - *Causal skepticism:* Does the causal origin of moral beliefs (in culture, upbringing, emotion) undermine their epistemic status?
   - *Regress arguments:* Does the justification pathway avoid the Agrippan trilemma (foundationalism, coherentism, infinitism)?

4. **Evolutionary Debunking Vulnerability** — A dedicated, in-depth assessment of the argument's vulnerability to evolutionary debunking:
   - Application of Street's Darwinian dilemma: does evolution explain our evaluative attitudes without reference to their truth?
   - Assessment of the tracking relation: could natural selection have favored truth-tracking moral capacities?
   - Third-factor response viability: can a third factor (e.g., the link between survival and genuinely valuable states) explain the correlation between evolved moral beliefs and moral truth?
   - Joyce's version: even if evolution produced true moral beliefs, does the insensitivity of the belief-forming process to moral truth undermine justification?

5. **Reflective Equilibrium Structure** — An analysis of whether and how the argument employs reflective equilibrium methodology:
   - Narrow reflective equilibrium (coherence among moral judgments and principles) vs. wide reflective equilibrium (incorporating background theories from psychology, biology, metaphysics)
   - The independence constraint: are the considered judgments that serve as data independent of the principles they are used to justify?
   - The isolation objection: does the coherence requirement provide any genuine constraint on moral truth, or could a coherent but systematically false moral system satisfy it?

6. **Overall Epistemic Assessment** — A summary judgment on the epistemic status of the argument's moral claims, using a structured rating scale (e.g., "knowledge is possible," "justified belief is possible," "merely permissible belief," "skepticism is warranted"). This rating should be defended with reference to the preceding analysis.

## Methodological Foundations

This skill draws on several foundational texts and debates in moral epistemology:

**Intuitionism (Moore, Ross, Audi).** G. E. Moore's *Principia Ethica* (1903) articulated a form of intuitionism on which "good" is a simple, non-natural property known through intuition — not through sensory perception or inference. W. D. Ross's *The Right and the Good* (1930) developed a pluralistic intuitionism of prima facie duties, known through intuitive apprehension of their self-evident moral character. Robert Audi's *The Good in the Right* (2004) defends a moderate intuitionism that treats moral intuitions as intellectual seemings — they provide prima facie justification but are defeasible by countervailing considerations and do not require a special faculty. Analysts should distinguish classical intuitionism (self-evidence, indefinability) from moderate intuitionism (defeasible seemings, fallibilism).

**Reflective Equilibrium (Rawls).** John Rawls's *A Theory of Justice* (1971) introduced reflective equilibrium as the central method of moral epistemology. We work back and forth between considered judgments about particular cases and general principles, adjusting each until we reach a state of equilibrium where principles and judgments cohere. This is a coherentist epistemology: no judgment is immune from revision, and justification is a matter of overall coherence. Narrow reflective equilibrium involves only moral judgments and principles; wide reflective equilibrium incorporates background theories from other domains. The skill requires the analyst to determine which form is employed and to assess the independence of the considered judgments that serve as inputs.

**Street's Darwinian Dilemma (2006).** Sharon Street's "A Darwinian Dilemma for Realist Theories of Value" presents a powerful evolutionary debunking challenge. The realist must either claim that there is no relation between evolutionary pressures and evaluative truth (making it a massive coincidence that our evolved evaluative attitudes track the truth) or claim that there is a relation (but then must explain how natural selection favored truth-tracking evaluative capacities — a claim that appears inconsistent with evolutionary biology, which explains our evaluative attitudes in terms of fitness enhancement, not truth). The skill requires careful application of this dilemma to the specific epistemological commitments of the argument under analysis.

**Joyce's Evolutionary Debunking (2006).** Richard Joyce's *The Evolution of Morality* (2006) develops a related but distinct debunking argument. Joyce focuses on the insensitivity of our moral belief-forming processes to moral truth. Even if our evolved moral beliefs happen to be true, they are not justified because the process that produced them is insensitive to moral truth — we would have held the same beliefs regardless of whether they were true. This is an undercutting defeater for moral beliefs, not merely a rebutting defeater.

**The Third-Factor Response (Enoch, Shafer-Landau, Copp).** A prominent realist response to evolutionary debunking posits a "third factor" that explains both (a) why evolution favored certain evaluative tendencies and (b) why those tendencies track the moral truth. David Enoch (2010) argues that survival (or reproductive success) is good — or at least, that what promotes survival tends to be good. This provides a linking premise: evolution favored beliefs and attitudes that promote survival, and survival-promoting states of affairs are (generally) genuinely valuable, so evolution favored truth-tracking evaluative attitudes after all. Shafer-Landau (2012) and Copp (2008) offer related responses. The skill requires assessment of whether these responses succeed for the specific argument under analysis.

**McGrath's Moral Perception.** Sarah McGrath's work on moral perception (e.g., "Moral Perception and Its Rivals," 2018) explores the possibility that we can literally perceive moral properties — that moral perception is a genuine form of perception, analogous to the perception of secondary qualities or social properties. The skill requires the analyst to consider whether a perceptual model can meet the epistemological demands faced by the argument under analysis.

## Steps

### Step 1: Identify Epistemological Claims

**Objective:** Extract and catalog all epistemological claims made or presupposed by the argument.

**Methodological Guidance:**
Begin by examining the argument-reconstruction report for explicit claims about how moral knowledge is acquired, what justifies moral beliefs, or what makes moral beliefs epistemically respectable. Look for both explicit epistemological claims ("we know that X is wrong because...") and implicit presuppositions (the argument's methodology may presuppose a particular epistemology even if it does not articulate one).

Key questions to answer:
- Does the argument appeal to moral intuitions? If so, what is the epistemic status claimed for those intuitions? Are they treated as data, as foundational justification, as revisable starting points, or as merely psychological phenomena?
- Does the argument employ reflective equilibrium? If so, is it narrow or wide? What are the inputs to the equilibrium process?
- Does the argument claim that some moral truths are self-evident, known a priori, or accessible through reason alone?
- Does the argument rely on empirical evidence about moral psychology or moral development? If so, what epistemological weight does it give this evidence?
- Does the argument address skeptical challenges? If so, how does it respond to them?

Distinguish the argument's own epistemological commitments from the epistemological commitments of the theory it argues for. A non-cognitivist argument against moral knowledge, for example, makes epistemological claims about realism without endorsing a positive epistemology of its own.

**Output of this step:** A catalog of epistemological claims, tagged as explicit or implicit, with citations to the argument-reconstruction report.

**Pitfalls to avoid:**
- Failing to distinguish between the epistemology of moral theory discovery (how we figure out what is right) and the epistemology of moral justification (what makes our beliefs justified).
- Assuming that appeal to intuition is necessarily intuitionist — coherentists also appeal to intuitions but treat them as revisable data, not foundations.
- Overlooking implicit epistemological commitments embedded in the argument's methodology.

### Step 2: Classify Justification Pathway

**Objective:** Classify the argument's justification pathway with sub-type precision.

**Methodological Guidance:**
Using the catalog from Step 1, determine which justification pathway(s) the argument employs. The primary classification categories are:

*Intuitionist Pathway:* The argument treats at least some moral beliefs as non-inferentially justified through rational intuition or intellectual seeming. Sub-types:
- Classical intuitionism (Moore): moral truths are self-evident and indefinable; intuition is a sui generis faculty.
- Rossian intuitionism: prima facie duties are self-evident; actual duties are determined through deliberative judgment, not deduction.
- Moderate intuitionism (Audi): intuitions are intellectual seemings that provide defeasible prima facie justification; no special faculty is required; intuitions are fallible.
- Rationalist intuitionism: moral truths are synthetic a priori, known through reason.

*Coherentist Pathway:* The argument justifies moral beliefs entirely through their coherence relations with other beliefs. Sub-types:
- Narrow reflective equilibrium: coherence among moral judgments and moral principles only.
- Wide reflective equilibrium: coherence among moral judgments, moral principles, and relevant background theories (psychological, biological, metaphysical).
- Pure coherentism: justification is coherence among beliefs in a maximally coherent system; no belief is epistemically prior.

*Reliabilist Pathway:* The argument justifies moral beliefs by appeal to the reliability of the process that produces them. Sub-types:
- Process reliabilism: moral beliefs are justified if produced by a reliable cognitive process, regardless of whether the believer can articulate the justification.
- Virtue epistemology: moral beliefs are justified if produced by intellectual virtues (open-mindedness, intellectual courage, etc.).
- Proper functionalism: moral beliefs are justified if produced by cognitive faculties functioning properly according to a design plan.

*Rationalist Pathway:* The argument treats moral truths as knowable through reason alone, analogous to mathematical or logical knowledge. Sub-types:
- Conceptual analysis: moral truths are analytic or follow from the analysis of moral concepts.
- Kantian rationalism: moral truths are deliverances of practical reason.
- Transcendental arguments: moral truths are necessary conditions of practical agency.

*Perceptual Pathway:* The argument treats moral properties as perceivable. Sub-types:
- Literal perception (McGrath): moral properties are directly perceived.
- Perceptual analogy: moral knowledge is relevantly analogous to perceptual knowledge.
- Secondary quality model: moral properties are analogous to secondary qualities (colors, tastes), perceived through sensibility.

*Hybrid Pathway:* The argument combines elements from multiple pathways. For example, an intuitionist foundationalism (basic moral beliefs are non-inferentially justified) combined with a coherentist superstructure (non-basic moral beliefs are justified by coherence with basic beliefs and each other). Specify which elements are combined and how they interact.

**Output of this step:** A precise classification of the justification pathway, with sub-type and textual support from the argument-reconstruction report.

**Pitfalls to avoid:**
- Classifying too quickly based on surface features (e.g., the word "intuition") without analyzing the epistemic role assigned.
- Forcing the argument into a single category when it may employ a hybrid pathway.
- Confusing the genetic question (how we come to hold moral beliefs) with the justificatory question (what makes them justified).

### Step 3: Assess Epistemic Access

**Objective:** Characterize the mechanism by which moral truths are accessed and assess its reliability.

**Methodological Guidance:**
For the identified justification pathway, specify the access mechanism in detail. What cognitive faculty or process delivers moral knowledge? What is its phenomenological character? Under what conditions is it reliable?

For intuitionist pathways, the access mechanism is rational intuition or intellectual seeming. Key questions:
- What is the phenomenology of moral intuition? Is it analogous to perceptual seeming, intellectual seeming (like mathematical intuition), or emotional response?
- Are moral intuitions subject to calibration (can we distinguish reliable from unreliable intuitions)?
- Are moral intuitions systematically distorted by cultural background, self-interest, or emotion? If so, can the distortion be corrected for?
- Is there independent evidence that moral intuition is truth-tracking (as opposed to merely fitness-tracking or conformity-tracking)?

For coherentist pathways, the access mechanism is the reflective equilibrium process. Key questions:
- What are the starting points (considered judgments), and are they epistemically independent of the principles they support?
- Does the equilibrium process genuinely constrain the output, or can it rationalize any set of moral beliefs given sufficient adjustments?
- What is the epistemological status of the coherence relation itself — why does coherence with other beliefs make a belief more likely to be true?

For reliabilist pathways, the access mechanism is the reliable process. Key questions:
- What is the process, and is there evidence of its reliability?
- Is the reliability of the process itself in need of justification? If so, does this lead to a regress?
- Can the reliabilist explain the normative authority of moral beliefs (why we should care about what the reliable process delivers)?

For rationalist pathways, the access mechanism is a priori reason. Key questions:
- What is the source of a priori moral knowledge? Is it conceptual, rational intuition, or transcendental argument?
- Are there synthetic a priori truths in the moral domain, and if so, how are they accessed?
- Does rationalism avoid the empirical challenges (evolutionary debunking, cultural variation) that face other pathways?

For perceptual pathways, the access mechanism is moral perception. Key questions:
- Is the perception literal or analogical? If literal, what is the perceptual organ or faculty?
- Can moral perception be distinguished from emotional response or cultural conditioning?
- Does perceptual access to moral properties survive the argument from perceptual variation (different perceivers perceive different moral properties)?

Assess reliability: given what we know about human psychology, is the claimed access mechanism likely to be reliable? Consider empirical evidence from moral psychology, social psychology, and cognitive science.

**Output of this step:** A detailed characterization of the access mechanism with a reliability assessment.

**Pitfalls to avoid:**
- Assuming reliability without argument — the analyst must assess, not assume.
- Neglecting empirical evidence about the actual operation of the claimed access mechanism.
- Conflating the claim that a mechanism is reliable with the claim that we can know it is reliable (the KK principle is not assumed).

### Step 4: Evaluate Skeptical Challenges

**Objective:** Systematically evaluate the argument's vulnerability to skeptical challenges.

**Methodological Guidance:**
Apply four main skeptical challenges to the identified justification pathway.

*Evolutionary Debunking Challenge:* Assess whether the evolutionary origins of moral cognition undermine the justification pathway. Street's dilemma provides the framework:
- Horn 1: If evolutionary forces did not track moral truth, then our moral beliefs are explained without reference to their truth — an undercutting defeater. The probability that our moral beliefs are true, given their evolutionary origin, is low (unless a tracking relation is established).
- Horn 2: If evolutionary forces did track moral truth, the realist owes an explanation of how. This explanation must be consistent with evolutionary biology, which typically explains traits in terms of fitness enhancement, not truth-tracking.
- Third-factor option: a third factor explains both why evolution favored certain evaluative tendencies and why those tendencies correlate with moral truth. Assess whether this response is available for the specific argument under analysis.

*Disagreement-Based Skepticism:* Assess whether pervasive moral disagreement undermines the reliability of the claimed access mechanism. If moral intuition delivers incompatible outputs across cultures and individuals, what reason is there to trust one's own intuitions? Key considerations:
- Does the argument acknowledge the extent of moral disagreement? If so, how does it respond?
- Is the disagreement fundamental or superficial (from the disagreement analysis, if available)?
- Can peerhood be denied for those who disagree with the argument's moral conclusions?

*Causal Skepticism:* Assess whether the causal origins of moral beliefs (in culture, upbringing, emotion, evolved dispositions) undermine their epistemic status. This challenge is related to but distinct from evolutionary debunking: even if evolution is not the relevant causal factor, the fact that moral beliefs are causally shaped by non-truth-tracking factors (parental influence, social conformity, emotional salience) may undermine justification. Key questions:
- Does the causal etiology of the relevant moral beliefs include truth-conducive factors?
- Is the belief-forming process sensitive to moral truth (would the believer hold different beliefs if the moral facts were different)?

*Agrippan Trilemma:* Assess whether the justification pathway avoids the Agrippan trilemma of foundationalism (arbitrary stopping point), coherentism (circularity), and infinitism (impossible completion). For each pathway:
- Foundationalism (intuitionism): Are the foundational beliefs genuinely self-justified, or is the stopping point arbitrary?
- Coherentism: Does coherence provide a genuine constraint on truth, or can any set of beliefs be made coherent?
- Infinitism: If the argument posits an infinite chain of justification, is this psychologically or epistemically possible?

**Output of this step:** A structured assessment of each skeptical challenge, with specific reference to the argument's justification pathway and commitments.

**Pitfalls to avoid:**
- Treating skeptical challenges as all-or-nothing — an argument may be partly vulnerable without being fully undermined.
- Applying challenges that are not relevant to the argument's specific epistemological commitments.
- Neglecting to consider whether the argument has resources to respond that are not explicitly articulated.

### Step 5: Test Third-Factor Response Viability

**Objective:** Assess whether a third-factor response can defuse the evolutionary debunking challenge for this argument.

**Methodological Guidance:**
The third-factor response is the most prominent realist reply to evolutionary debunking. It requires identifying a factor F such that:
1. F explains why evolution favored certain evaluative tendencies (e.g., tendencies to value survival, cooperation, harm-avoidance).
2. F also explains why those tendencies correlate with (or constitute) moral truth (e.g., survival is genuinely good, cooperation is genuinely right).

Key variants of the third-factor response:
- *Enoch's "survival is good" response:* Natural selection favored tendencies to pursue survival and reproductive success. But survival and reproductive success are (in many cases) genuinely valuable. So there is a third factor — the value of survival — that explains both the evolutionary pressure and the truth of the relevant evaluative beliefs.
- *Shafer-Landau's "reliable mechanism" response:* Evolution may have produced a reliable mechanism for detecting moral truths, even if the mechanism was selected for fitness-enhancing rather than truth-tracking reasons. (Compare: visual perception was selected for fitness-enhancing reasons, but it successfully tracks physical truths.)
- *Copp's "society-centered" response:* Moral truths are truths about what meets the needs of society. Evolution favored tendencies that promote social cohesion and cooperation. Since moral truth just is what meets society's needs, the evolutionary explanation and the moral truth converge.

Assess the viability of the third-factor response for the specific argument under analysis:
- Is the third factor genuinely explanatory of both the evolutionary pressure and the moral truth?
- Does the third factor cover the full range of moral beliefs, or only a subset (e.g., other-regarding moral beliefs but not self-regarding ones)?
- Does the third-factor response concede too much to the debunker? If the best explanation of our moral beliefs is evolutionary and the truth-link is secondary, does this undermine the epistemic standing of moral beliefs even if a truth-link exists?
- Does the third-factor response work for all forms of realism, or only for naturalist realism (on which moral facts are natural facts that evolution might track)?

**Output of this step:** A detailed assessment of whether the third-factor response is available and, if so, how effective it is for the specific argument.

**Pitfalls to avoid:**
- Assuming that the third-factor response succeeds globally without testing it against the specific moral claims of the argument under analysis.
- Neglecting to consider whether the third factor introduces a coincidence that is itself epistemically problematic.
- Confusing third-factor responses with tracking responses — a third factor can establish correlation without establishing sensitivity.

### Step 6: Compile Report with Overall Epistemic Assessment

**Objective:** Produce the final Moral Epistemology Analysis Report.

**Methodological Guidance:**
Integrate the findings from Steps 1 through 5 into a comprehensive report following the output structure. The report should include:

1. Justification pathway classification with sub-type.
2. Epistemic access mechanism with reliability assessment.
3. Skeptical challenge evaluation (evolutionary debunking, disagreement, causal, regress).
4. Third-factor response viability assessment.
5. Reflective equilibrium structure analysis (if applicable).
6. Overall epistemic assessment with rating.

The overall epistemic assessment should use a consistent rating scale:
- **Knowledge is possible:** The argument's justification pathway survives skeptical challenges; moral knowledge is achievable on this account.
- **Justified belief is possible:** The argument provides justification for moral beliefs, but knowledge-level warrant is not achieved (e.g., Gettier-style concerns apply, or the justification is adequate but the truth connection is not fully secure).
- **Merely permissible belief:** The argument does not provide positive justification for moral beliefs, but moral beliefs are not irrational or impermissible — they are epistemically permissible without being justified.
- **Pro tanto justification only:** The argument provides some justification, but it is defeated or insufficient on its own; additional support is needed.
- **Skepticism is warranted:** The argument's epistemological commitments are undermined by skeptical challenges; moral knowledge (or justified belief) is not possible on this account.

The report should identify the strongest and weakest elements of the argument's epistemology, note any unresolved tensions, and suggest what additional epistemological work would be needed to strengthen the argument's position.

**Output of this step:** The complete Moral Epistemology Analysis Report.

## Quality Criteria

1. **Justification Pathway Precision:** The report must correctly identify the argument's justification pathway and sub-type, with textual support. Misclassification at this stage undermines all subsequent analysis. The distinction between intuitionism and coherentism is especially important, as these pathways face different skeptical challenges.

2. **Skeptical Challenge Rigor:** The evaluation of skeptical challenges must be systematic and thorough. Each challenge should be applied specifically to the argument's epistemological commitments, not discussed in the abstract. The analyst should not merely note that a challenge exists but should assess its force given the specific features of the argument.

3. **Third-Factor Analysis:** The assessment of the third-factor response should be nuanced. It should consider both the strength of the response in general and its applicability to the specific argument. The report should not assume that the third-factor response succeeds or fails universally.

4. **Epistemic Humility:** The report should reflect appropriate epistemic humility. Moral epistemology is a contested field, and the analyst should not present contentious epistemological positions as established. The report should acknowledge uncertainties, note where the evidence is inconclusive, and avoid overclaiming.

5. **Intuitionist/Coherentist Distinction Clarity:** Because the boundary between intuitionism and coherentism is contested (both appeal to intuitions; both allow for revision), the report must be especially careful in drawing this distinction. The key difference is the epistemic role assigned to intuitions: are they non-inferentially justified foundations, or are they merely revisable inputs to a coherence-generating process? The report should make this distinction explicit and defend the classification.

## Relations to Other Skills

**Dependencies (skills this skill requires as input):**
- `phil-moral-realism` — Optional but highly recommended. The epistemological analysis is more powerful when the argument's metaphysical commitments are clearly identified, as different metaphysical positions carry different epistemological burdens.
- `phil-conceptual-analysis` — Optional. If the argument involves conceptual analysis of moral concepts (e.g., "good," "right," "ought"), the conceptual analysis provides useful context for assessing epistemological claims.

**References (knowledge resources this skill draws upon):**
- `glossary-metaethics.md` — For definitions of key metaethical terms and epistemological terms.
- `metaethical-distinctions.md` — For canonical distinctions (cognitivism/non-cognitivism, internalism/externalism, naturalism/non-naturalism) that bear on epistemological questions.

**Downstream skills (skills that may use this skill's output):**
- `phil-argument-reconstruct` — If the epistemological analysis reveals new epistemological commitments, these may need to be incorporated into the argument reconstruction.
- ARS synthesis skills — The Moral Epistemology Analysis Report is a component of the full metaethical analysis and is used in ARS Phase 4 synthesis.

## Boundary Conditions

**When to apply this skill:**
- The argument makes explicit epistemological claims about how moral knowledge is acquired, what justifies moral beliefs, or what the epistemic status of moral judgments is.
- The argument relies on a specific epistemological method (intuition, reflective equilibrium, conceptual analysis) that carries implicit epistemological commitments.
- The argument is an evolutionary debunking argument or responds to one.
- The argument addresses moral skepticism or the possibility of moral knowledge.

**When to skip this skill:**
- The argument makes no epistemological claims and has no implicit epistemological commitments (rare — most moral arguments have some epistemological dimension).
- The argument is purely semantic (e.g., about the meaning of moral terms) without implications for how moral beliefs are justified.
- The argument is purely metaphysical (e.g., about the existence of moral properties) and does not address the epistemological question of access.

**Edge cases and special handling:**
- *Pure first-order moral argument:* If the argument is a first-order normative argument (e.g., "abortion is wrong because it kills an innocent person") without explicit epistemological reflection, note that there are implicit epistemological commitments (the arguer presumably believes they know the moral premises and their justification). Offer to analyze these implicit commitments without imposing an epistemological framework that the argument does not endorse.
- *Empirical psychology dependence:* If the argument's epistemological claims depend on empirical claims about moral psychology (e.g., "moral intuitions are reliably produced by System 1 processing"), flag this as needing empirical support. The epistemological assessment should distinguish between what follows if the empirical claims are true and what follows given our current level of empirical confidence.
- *Non-cognitivist arguments:* If the argument is non-cognitivist (moral judgments are not truth-apt), the epistemological analysis shifts: the question is not "how do we know moral truths?" but "what makes moral judgments warranted or rational?" Use the same framework but adapt the justification pathways accordingly (e.g., expressivists may appeal to coherence of attitudes, not coherence of beliefs).
- *Particularist challenges:* If the argument is a moral particularist argument (there are no general moral principles), the epistemological implications should be assessed: how does justification work in a principle-free moral epistemology?

## ARS Interface

This skill is part of the Academic Research Skills (ARS) metaethics pipeline (Phase 2: Metaethical Analysis). It conforms to the ARS skill interface specification.

**Trigger conditions:**
- The ARS orchestrator invokes this skill when the argument-reconstruction report identifies epistemological commitments and the pipeline workflow specifies metaethical analysis.
- This skill may also be invoked manually when a user requests analysis of a moral epistemology argument.

**Input contract:**
- The skill expects a valid argument-reconstruction report in the ARS standard format.
- The report must include identifiable epistemological claims or implicit epistemological commitments.
- If the input does not meet these conditions, the skill should return an error or skip notification.

**Output contract:**
- The skill produces a Moral Epistemology Analysis Report in ARS-compatible Markdown format.
- The report includes metadata tags (`#METAETHICS`, `#EPISTEMOLOGY`, `#PHASE2`) for pipeline integration.
- The overall epistemic assessment uses the ARS standard rating vocabulary for cross-skill consistency.

**Integration notes:**
- The report may be consumed by downstream ARS skills (e.g., synthesis, rebuttal audit) without reformatting.
- The report is designed to be included in a cumulative ARS project dossier.
- The epistemological analysis is complementary to the metaphysical analysis from `phil-moral-realism` and the disagreement analysis from `phil-moral-disagreement` — together they provide a complete Phase 2 metaethical profile.

**State management:**
- This skill does not maintain persistent state between invocations.
- Each analysis is self-contained and does not depend on previous analyses except through explicit input reports.
