---
name: phil-moral-disagreement
description: "Moral Disagreement Analysis — evaluate arguments from moral disagreement and their implications for moral realism; assess conciliationist challenges and convergence responses"
---

# Moral Disagreement Analysis

## Overview

The existence of widespread, persistent moral disagreement is one of the most influential arguments against moral realism in contemporary metaethics. This skill provides a systematic framework for analyzing disagreement-based arguments, evaluating their inferential strength, and assessing the realist's available responses.

The phenomenon of moral disagreement is undeniable. Different cultures, communities, and individuals hold deeply incompatible moral views on matters ranging from the permissibility of abortion and euthanasia to the moral status of animals and the requirements of distributive justice. The question is what this disagreement tells us about the nature of morality. J. L. Mackie (1977) famously argued that the best explanation of persistent moral disagreement is that there are no objective moral facts to converge upon — the "argument from relativity." This challenge has been refined and extended through work on peer disagreement in epistemology, giving rise to the conciliationist challenge: if you discover that an epistemic peer disagrees with you, you should reduce confidence in your view, and by parity of reasoning, awareness of pervasive moral peer disagreement should undermine confidence in all moral beliefs.

The skill is designed to be applied after an argument-reconstruction report has been produced. It takes that report as primary input and produces a structured analysis report that classifies the disagreement at issue, reconstructs the argumentative move from disagreement to anti-realism or skepticism, evaluates the strength of that inference, and critically assesses the realist's available responses — including convergence arguments, peerhood denial strategies, and companions-in-guilt arguments.

This skill also addresses a distinctive self-reflexive worry: if moral disagreement itself supports skepticism about morality, does disagreement about the epistemic significance of disagreement (a meta-disagreement) undermine that very argument? The skill requires the analyst to consider whether the disagreement argument is self-defeating, and to incorporate that assessment into the overall evidential significance rating.

The skill covers four major realist response strategies. First, convergence arguments (Shafer-Landau, Smith) hold that moral disagreement is overstated — that there is far more agreement than disagreement, especially at the level of fundamental principles, and that residual disagreement is explained by non-moral factual disagreement or irrationality. Second, peerhood denial strategies challenge whether moral disputants genuinely count as epistemic peers, pointing to cognitive biases, motivated reasoning, or differential access to relevant evidence. Third, companions-in-guilt arguments maintain that if moral disagreement undermines moral realism, then by parity of reasoning, disagreement in other domains (philosophy itself, epistemology, aesthetics) undermines realism in those domains too — a cost few are willing to bear. Fourth, some realists grant the disagreement but deny the anti-realist inference, arguing that moral facts can obtain even in the presence of widespread error.

The skill also incorporates empirical dimensions. Doris and Stich have argued that empirical moral psychology reveals systematic patterns of moral variation that are resistant to rational resolution, strengthening the disagreement argument. The analyst must assess whether empirical claims about moral psychology are well-supported and whether they genuinely favor anti-realism.

## Input

**Required:**
- `argument-reconstruction report` — A completed argument-reconstruction analysis report (from the `phil-argument-reconstruct` skill) that identifies the argument's premises, conclusions, inferential structure, and implicit assumptions. The disagreement analysis depends on a clear understanding of what the argument claims, how it reasons from disagreement to its conclusion, and what role disagreement plays in the overall dialectic.

**Optional:**
- `moral-realism analysis report` — A completed moral-realism analysis report (from the `phil-moral-realism` skill) that characterizes the argument's metaethical commitments. This is valuable because the force of a disagreement argument depends partly on what form of realism is being challenged — non-naturalist realism may be more vulnerable to disagreement arguments than naturalist realism, for example.
- `empirical evidence dossier` — A collection of relevant empirical studies on moral variation, moral psychology, or cross-cultural ethics. This is relevant when the disagreement argument makes empirical claims about the extent, persistence, or nature of moral disagreement.

**Input format:** Structured reports as Markdown documents or equivalent structured text. The analyst should verify that the argument-reconstruction report is complete before proceeding. If critical premises are missing or underspecified, the analyst should note this and, where possible, reconstruct the missing elements from context.

**Preconditions:** The argument under analysis must make a claim about moral disagreement and draw a metaethical conclusion from it. Arguments that merely mention disagreement without using it evidentially do not trigger this skill. The analyst should also confirm that the disagreement in question is moral disagreement, not merely disagreement about non-moral facts that happen to have moral implications.

## Output

The output is a structured **Moral Disagreement Analysis Report** containing the following sections:

1. **Disagreement Type Classification** — A precise classification along four dimensions:
   - *Domain:* What is the disagreement about? (Specific moral issue, class of issues, moral principles, moral epistemology, moral semantics)
   - *Persistence:* Is the disagreement persistent across time and reflection, or does it appear to be resolvable with further information or deliberation?
   - *Peerhood status:* Do the disputants qualify as epistemic peers with respect to the disputed proposition? (Equal intelligence, equal access to evidence, equal freedom from bias, equal diligence)
   - *Resolution prospects:* Is there reason to think the disagreement could in principle be resolved? Through what mechanism? What would convergence require?

2. **Argument Structure Analysis** — A step-by-step reconstruction of the argument from disagreement to its metaethical conclusion. This identifies:
   - The specific premises linking disagreement to anti-realism or skepticism
   - Any suppressed premises (e.g., "if there were objective moral facts, we would expect convergence")
   - The logical form of the inference (inference to the best explanation, modus tollens, Bayesian updating)
   - The scope of the conclusion (global anti-realism, local skepticism about specific moral issues, or merely a shift in burden of proof)

3. **Inference Strength Assessment** — An evaluation of how strongly the disagreement evidence supports the anti-realist or skeptical conclusion. This considers:
   - Alternative explanations of the disagreement (non-moral factual disagreement, irrationality, partiality)
   - Whether the disagreement is fundamental (disagreement in moral principles) or superficial (disagreement in application of shared principles to contested facts)
   - Whether the disagreement is faultless (neither party is making a mistake) or fault-based (at least one party is in error)
   - The probabilistic weight: how surprising is moral disagreement on the assumption of realism versus anti-realism?

4. **Realist Response Evaluation** — A critical assessment of each available realist response:
   - *Convergence:* Does the evidence support the claim that moral disagreement is overstated? Is there significant agreement at the level of fundamental principles?
   - *Peerhood denial:* Can epistemic peerhood be plausibly denied? On what grounds?
   - *Companions in guilt:* Does the parity argument succeed? Are the relevant domains genuinely analogous?
   - *Error tolerance:* Can the realist consistently hold that there are objective moral facts while acknowledging widespread moral error?

5. **Evidential Significance Rating** — A summary judgment on the overall dialectical significance of the disagreement argument, using a structured rating scale (e.g., "strongly supports anti-realism," "modestly supports anti-realism," "dialectically neutral," "modestly supports realism," "strongly supports realism"). This rating should be defended with reference to the preceding analysis.

6. **Self-Defeat Assessment** — An evaluation of whether the disagreement argument is self-defeating, given that there is meta-disagreement about the epistemic significance of disagreement itself.

## Methodological Foundations

This skill draws on several foundational texts and debates:

**Mackie's Argument from Relativity (1977).** In *Ethics: Inventing Right and Wrong*, J. L. Mackie argues that "the actual variations in the moral codes are more readily explained by the hypothesis that they reflect ways of life than by the hypothesis that they express perceptions, most of them seriously inadequate and badly distorted, of objective values." This is the locus classicus of the disagreement argument. Mackie's argument is best understood as an inference to the best explanation: realism predicts convergence, but we observe divergence, so we should prefer an explanation that does not posit objective values as the objects of (highly fallible) perception. Analysts should distinguish Mackie's argument from the distinct argument from queerness, though both appear in the same text and are sometimes conflated.

**The Conciliationist Challenge (Christensen, Elga).** Contemporary epistemology of disagreement has developed a formal challenge that sharpens Mackie's insight. The conciliationist principle holds that, upon discovering that an epistemic peer disagrees with you, you should reduce your confidence in your view (conciliate). Applied to morality, the challenge is that awareness of pervasive moral peer disagreement should lead to a general reduction in confidence in all moral beliefs — potentially to the point of suspension of judgment. Christensen's (2007) "Epistemology of Disagreement: The Good News" and Elga's (2007) "Reflection and Disagreement" are key sources. Analysts should distinguish equal-weight views (both parties should revise equally) from more moderate conciliationist views.

**Convergence Arguments (Shafer-Landau, Smith).** Realists have responded by arguing that moral disagreement is in fact much less extensive than it appears. Russ Shafer-Landau's *Moral Realism: A Defence* (2003) argues that many apparent moral disagreements are really disagreements about non-moral facts, and that there is significant convergence on fundamental moral principles. Michael Smith's *The Moral Problem* (1994) develops a convergence thesis based on the idea that fully rational agents would converge in their desires. The analyst must assess whether convergence arguments shift the explanatory burden back to the anti-realist.

**Doris and Stich on Empirical Moral Psychology.** John Doris and Alexandra Plakias (2008) and Stephen Stich and colleagues have argued that empirical moral psychology reveals patterns of moral variation that are deep, systematic, and resistant to rational resolution — thereby strengthening the disagreement argument. Analysts should evaluate whether the cited empirical evidence supports the claimed conclusions and whether it is subject to methodological critique (e.g., by Machery and Mallon).

**The Self-Defeat Worry.** A distinctive reflexive challenge: if disagreement about P undermines justification for P, and there is disagreement about the epistemic significance of disagreement itself, then the disagreement argument may be self-defeating. This worry is pressed by, among others, Thomas Kelly in "The Epistemic Significance of Disagreement" (2005). The analyst must consider whether the argument can be formulated so as to avoid this reflexive problem.

## Steps

### Step 1: Characterize the Disagreement

**Objective:** Identify and describe the specific disagreement at issue in the argument under analysis.

**Methodological Guidance:**
Begin by extracting from the argument-reconstruction report every claim about moral disagreement. Identify what proposition(s) are disputed, who the relevant disputants are (actual historical communities, hypothetical rational agents, the author and their opponents), and what evidence is offered for the existence and persistence of the disagreement.

Key questions to answer:
- What exactly is disagreed about? Is it a specific moral judgment (e.g., "abortion is wrong"), a moral principle (e.g., "one ought to maximize utility"), a moral-epistemic claim (e.g., "moral intuitions are reliable"), or a metaethical claim (e.g., "moral properties exist")?
- Who disagrees? Are they identified communities (ancient Greeks vs. contemporary liberals), hypothetical reasoners (ideal observers, fully informed rational agents), or the author's philosophical opponents?
- What is the scope of the disagreement claim? Does the argument assert universal disagreement across all moral issues, or only disagreement about some specific domain?
- What evidence (historical, anthropological, psychological, sociological) is cited to establish the existence and persistence of the disagreement?

**Output of this step:** A clear, concise statement of the disagreement characterized along the dimensions of content, parties, scope, and evidential basis. This should be precise enough to support the classification in Step 2.

**Pitfalls to avoid:**
- Conflating disagreement about moral facts with disagreement about non-moral facts that have moral implications.
- Assuming that cited disagreement is genuine rather than merely apparent (e.g., verbal disagreement).
- Overlooking the distinction between actual disagreement and merely possible disagreement (the latter has different evidential force).

### Step 2: Classify the Disagreement Type

**Objective:** Classify the disagreement along theoretically significant dimensions that determine its evidential force.

**Methodological Guidance:**
Apply a structured classification scheme. First, determine whether the disagreement is fundamental (disagreement at the level of basic moral principles or values) or superficial (disagreement in the application of shared principles, which may be attributable to non-moral factual disagreement or cognitive limitations). Fundamental disagreement is more threatening to realism than superficial disagreement.

Second, determine whether the disagreement is faultless (neither party is making a mistake — both are correct or neither is correct) or fault-based (at least one party holds a false belief). Note that the faultless/fault-based distinction partly presupposes the truth about metaethics: realists will tend to see moral disagreement as fault-based (someone is getting it wrong), while relativists may see it as faultless. The analyst should not presuppose the answer but should identify which classification is most defensible given independent considerations.

Third, assess peerhood: do the disputants qualify as epistemic peers with respect to the disputed proposition? This requires considering:
- Cognitive parity: Are the disputants equally intelligent and competent?
- Evidential parity: Do they have access to the same relevant evidence?
- Bias parity: Are they equally free from distorting influences (self-interest, ideology, motivated reasoning)?
- Diligence parity: Have they invested comparable effort in reaching their views?
If peerhood can be plausibly denied, the conciliationist challenge loses much of its force.

Fourth, assess resolution prospects: could the disagreement in principle be resolved? If so, through what mechanism (further empirical information, conceptual clarification, rational reflection, convergence of affective responses)? The more intractable the disagreement appears, the stronger the anti-realist argument.

**Output of this step:** A structured classification entry for each dimension, with explicit justification for each classification judgment.

**Pitfalls to avoid:**
- Conflating "faultless" with "irresolvable" — a disagreement can be fault-based yet practically irresolvable.
- Assuming peerhood without adequate evidence about the cognitive and evidential situation of the disputants.
- Overlooking the possibility that some forms of moral disagreement (e.g., about the weight of competing considerations) may be more persistent than others.

### Step 3: Reconstruct the Disagreement Argument

**Objective:** Produce a precise logical reconstruction of the argument from moral disagreement to its anti-realist or skeptical conclusion.

**Methodological Guidance:**
Using the argument-reconstruction report as a base, isolate the premises that connect the fact of moral disagreement to the metaethical conclusion. Produce an explicit premise-conclusion structure. For Mackie-style arguments, this typically takes the form:

1. There is widespread, persistent moral disagreement across cultures and individuals.
2. The best explanation of this disagreement is that moral judgments are not tracking objective moral facts but rather reflect culturally variable ways of life, emotional responses, or social norms.
3. Therefore, we should prefer an anti-realist account of moral discourse over a realist one.

For conciliationist arguments, the structure is more formal:

1. If you discover that an epistemic peer disagrees with you about P, you should reduce confidence in P.
2. For any given moral belief M, there exists an epistemic peer who disagrees with you about M.
3. Therefore, you should reduce confidence in all your moral beliefs.

Identify any suppressed premises. Common suppressed premises in disagreement arguments include:
- "If there were objective moral facts, we would expect convergence of moral beliefs (at least among competent inquirers)."
- "Moral disagreement is not plausibly attributed to non-moral factual disagreement or irrationality."
- "The persistence of disagreement after full reflection indicates the absence of objective truth."

Identify the logical form of the inference: inference to the best explanation, Bayesian confirmation, modus tollens, or a burden-shifting argument (the disagreement shows the realist owes an explanation). The logical form matters for assessing the argument's vulnerability to different responses.

**Output of this step:** A numbered premise-conclusion argument, with implicit premises made explicit, and the logical form identified.

**Pitfalls to avoid:**
- Conflating Mackie's argument from relativity with his argument from queerness — these are distinct arguments.
- Failing to make suppressed premises explicit, which can obscure the argument's vulnerabilities.
- Overlooking the scope of the conclusion — some arguments target only non-naturalist realism, not all forms of realism.

### Step 4: Evaluate the Inference

**Objective:** Critically assess whether the fact of moral disagreement genuinely supports the anti-realist or skeptical conclusion.

**Methodological Guidance:**
Evaluate each premise of the reconstructed argument. Is the existence and extent of moral disagreement adequately supported? Could the disagreement be explained without abandoning realism? The key question is whether the disagreement is more surprising on the assumption of realism than on the assumption of anti-realism — that is, whether it differentially confirms anti-realism.

Consider alternative realist explanations of the disagreement:
- *Non-moral factual disagreement:* Disputants agree on moral principles but disagree about relevant non-moral facts (e.g., about when a fetus becomes sentient, or about the economic consequences of a policy).
- *Irrationality explanation:* One or both parties are subject to cognitive biases, motivated reasoning, or insufficient reflection that leads them to moral error.
- *Indeterminacy explanation:* Moral facts may be objective but indeterminate in some cases, permitting a range of acceptable moral judgments.
- *Difficulty explanation:* Moral truths may be objectively real but epistemically difficult to access, leading to predictable error patterns.
- *Partiality explanation:* Moral judgments are particularly susceptible to distortion by self-interest and partiality, making disagreement unsurprising even if objective moral truths exist.

For each alternative explanation, assess its plausibility. Does it account for the specific pattern of disagreement observed? Does it require ad hoc assumptions? Does it shift the dispute to a different domain (e.g., from moral disagreement to disagreement about what the non-moral facts are)?

Assess the probability of disagreement conditional on realism versus anti-realism. If moral realism is true and moral facts are difficult to know, disagreement might be exactly what we should expect. If so, the disagreement argument is weak. If, however, realism predicts convergence and we observe divergence, the argument has force.

**Output of this step:** A structured evaluation of each premise and alternative explanation, with an overall assessment of the inferential strength of the disagreement argument.

**Pitfalls to avoid:**
- Evaluating the inference based on intuitive plausibility rather than systematic analysis of alternative explanations.
- Neglecting to consider how the specific form of realism at issue (naturalist vs. non-naturalist, reductionist vs. non-reductionist) affects the inference.
- Treating "disagreement is expected under realism" as an adequate response without showing that the specific pattern of disagreement matches realist predictions.

### Step 5: Assess Realist Responses

**Objective:** Critically evaluate the four main realist response strategies.

**Methodological Guidance:**
For each response strategy, articulate the strongest version of the response and then subject it to criticism.

*Convergence Response:* The claim is that moral disagreement is overstated; there is far more agreement than the anti-realist acknowledges. Assess this by considering:
- What moral principles do all (or nearly all) cultures and individuals accept? (Candidates: prohibitions on killing innocents, requirements of reciprocity, some form of the Golden Rule.)
- Are these convergences better explained by realism or by shared human nature (evolutionary, psychological, or social commonalities)?
- Does convergence at the level of abstract principles establish convergence of moral truth, or is the relevant disagreement at the level of specific application?
- Shafer-Landau's version: even if there is significant moral disagreement, it may be explained by the difficulty of moral inquiry rather than the absence of moral facts.

*Peerhood Denial Response:* The claim is that moral disputants are not genuine epistemic peers. Assess by considering:
- Are there systematic asymmetries in cognitive ability, access to evidence, or freedom from bias?
- Does motivated reasoning or self-interest systematically distort moral judgment in a way that undermines peerhood?
- Even if peerhood can be denied in many cases, can it be denied in all cases? A single genuine peer disagreement may be enough for the conciliationist challenge.
- Is the peerhood denial strategy question-begging if it assumes that those who disagree with us are thereby irrational or biased?

*Companions-in-Guilt Response:* The claim is that if moral disagreement undermines moral realism, then by parity of reasoning, disagreement in other domains undermines realism in those domains. Assess by considering:
- Are the domains genuinely analogous? Does disagreement in, say, epistemology or metaphysics have the same features (persistence, peerhood, fundamentality) as moral disagreement?
- Is the anti-realist willing to accept anti-realism about the companion domains? If not, why the asymmetry?
- Does the existence of a self-defeat worry for the disagreement argument (disagreement about the epistemic significance of disagreement) constitute a special case of the companions-in-guilt response?

*Error Tolerance Response:* The claim is that the realist can consistently hold that there are objective moral facts while acknowledging that many (perhaps most) people have false moral beliefs. Assess by considering:
- Does this response make moral facts epistemically inaccessible to an implausible degree?
- Can the realist explain why error is so widespread without rendering moral knowledge impossible?
- Does this response converge with the difficulty explanation from Step 4?

**Output of this step:** A structured evaluation of each response strategy, identifying the strongest realist response(s) and their remaining vulnerabilities.

**Pitfalls to avoid:**
- Treating response strategies as mutually exclusive when they can be combined (e.g., convergence plus difficulty explanation).
- Confusing the dialectical burden — the realist does not need to prove convergence; it is enough to show that the anti-realist inference is not compulsory.
- Neglecting to assess whether the responses are mutually consistent.

### Step 6: Compile Report with Evidential Significance

**Objective:** Produce the final Moral Disagreement Analysis Report with an overall assessment.

**Methodological Guidance:**
Integrate the findings from Steps 1 through 5 into a comprehensive report. The report should follow the output structure specified above. The evidential significance rating should summarize the dialectical status: does the disagreement argument succeed in shifting the burden of proof, or does the realist have adequate responses?

The rating should use a consistent scale:
- **Strongly supports anti-realism:** The disagreement argument succeeds; realist responses are inadequate.
- **Modestly supports anti-realism:** The disagreement argument has some force but is not decisive; realist responses partially succeed but leave residual concerns.
- **Dialectically neutral:** The disagreement argument and realist responses are in equipoise; neither side gains a clear advantage from the fact of moral disagreement.
- **Modestly supports realism:** Realist responses succeed in defusing the disagreement argument; the pattern of moral agreement/disagreement is at least as well explained by realism.
- **Strongly supports realism:** The pattern of moral agreement is better explained by realism than by anti-realism; disagreement is exactly what we would expect given the difficulty of moral inquiry.

Include a self-defeat assessment: does disagreement about the epistemic significance of disagreement undermine the disagreement argument itself? If the argument can be reformulated to avoid self-defeat, explain how.

The report should conclude with a summary of the key dialectical moves and the overall state of play, identifying any remaining open questions that would benefit from further analysis.

**Output of this step:** The complete Moral Disagreement Analysis Report.

## Quality Criteria

The following criteria should be used to evaluate the quality of a Moral Disagreement Analysis Report:

1. **Disagreement Typology Precision:** The report must correctly classify the disagreement along the four specified dimensions (domain, persistence, peerhood, resolution prospects). Classifications should be justified with reference to the argument's own claims and, where relevant, independent evidence. Vague or underspecified classifications reduce the report's diagnostic value.

2. **Inference Evaluation Rigor:** The evaluation of the argument from disagreement to its conclusion must be systematic and thorough. The report should identify all key premises, make implicit premises explicit, and critically evaluate each. Alternative explanations of the disagreement should be considered and assessed for plausibility. The report should not simply assert that the inference is strong or weak but should demonstrate this through structured analysis.

3. **Response Fairness:** Realist responses should be presented in their strongest forms, not strawmanned. The report should consider how a sophisticated realist would respond to the disagreement argument, drawing on the best available versions of convergence, peerhood denial, companions-in-guilt, and error tolerance strategies. The report should identify vulnerabilities in realist responses but should not dismiss them without adequate argument.

4. **Empirical Grounding:** Where the disagreement argument makes empirical claims (about the extent of moral variation, about moral psychology, about cross-cultural patterns), the report should assess whether these claims are adequately supported. It should flag unsupported empirical assertions and note where further empirical evidence would be required to strengthen or weaken the argument.

5. **Self-Defeat Awareness:** The report must consider whether the disagreement argument is vulnerable to a reflexive self-defeat problem. It should assess whether the argument's own premises are subject to the kind of disagreement that the argument treats as undermining, and whether this reflexive problem can be avoided through careful formulation.

## Relations to Other Skills

**Dependencies (skills this skill requires as input):**
- `phil-argument-reconstruct` — The disagreement analysis cannot proceed without a clear reconstruction of the argument's structure, premises, and conclusions. The argument-reconstruction report is the primary input.
- `phil-moral-realism` — Optional but highly recommended. The force of a disagreement argument depends on the specific form of realism it targets. A moral-realism analysis report provides the necessary context.

**References (knowledge resources this skill draws upon):**
- `glossary-metaethics.md` — For definitions of key metaethical terms (realism, anti-realism, cognitivism, non-cognitivism, naturalism, non-naturalism, error theory, relativism).
- `argument-forms/disagreement-argument.md` — A template or canonical formulation of the disagreement argument, useful for comparison and standardization.

**Downstream skills (skills that may use this skill's output):**
- `phil-moral-epistemology` — The disagreement argument is closely related to moral epistemology, as it can be framed as a skeptical challenge to moral knowledge. Disagreement analysis informs epistemological assessment.
- `phil-moral-supervenience` — If the argument makes supervenience claims, the supervenience analysis skill may be applied subsequently.

## Boundary Conditions

**When to apply this skill:**
- The argument under analysis explicitly invokes moral disagreement as a premise or as evidence for a metaethical conclusion.
- The argument is a conciliationist argument from peer disagreement applied to the moral domain.
- The argument responds to a disagreement-based argument against moral realism.

**When to skip this skill:**
- The argument makes no reference to moral disagreement and does not rely on disagreement as evidence.
- The argument mentions disagreement only in passing, without drawing any metaethical inference from it.
- The disagreement is purely first-order normative (e.g., "Smith and Jones disagree about whether euthanasia is wrong") and the argument does not elevate this to a meta-level claim about the nature of morality.

**Edge cases and special handling:**
- *First-order normative disagreement (not meta-level):* If the argument involves moral disagreement but remains entirely at the first-order level (e.g., "we should resolve our disagreement about abortion policy by voting"), note this distinction. Offer to elevate the analysis to the meta-level by considering whether the fact of first-order disagreement has metaethical implications. Do not force a metaethical analysis where none is intended.
- *Empirical claims about psychology:* If the disagreement argument depends on empirical claims about moral psychology (e.g., "moral judgments are caused by emotional responses that vary across cultures"), flag these as needing empirical support. Note where the empirical literature supports or challenges these claims. Do not treat empirical claims as established unless they are well-supported.
- *Verbal disagreement:* If the disagreement may be merely verbal (disputants use the same words with different meanings), note this possibility and assess whether the disagreement persists under conceptual clarification.
- *Disagreement about disagreement:* If the argument acknowledges meta-disagreement about the epistemic significance of disagreement, this raises the self-defeat worry. Ensure this is addressed in the self-defeat assessment.
- *Local vs. global arguments:* Some arguments use disagreement about a specific moral issue to draw a local skeptical conclusion (e.g., "we cannot know whether abortion is wrong"). Others use the general fact of moral disagreement to draw a global conclusion (e.g., "there are no objective moral facts"). The scope of the argument should be clearly identified and respected in the analysis.

## ARS Interface

This skill is part of the Academic Research Skills (ARS) metaethics pipeline (Phase 2: Metaethical Analysis). It conforms to the ARS skill interface specification.

**Trigger conditions:**
- The ARS orchestrator invokes this skill when the argument-reconstruction report identifies moral disagreement as a significant argumentative element and the pipeline workflow specifies metaethical analysis.
- This skill may also be invoked manually when a user requests analysis of a moral disagreement argument.

**Input contract:**
- The skill expects a valid argument-reconstruction report in the ARS standard format.
- The report must include identifiable claims about moral disagreement and their argumentative role.
- If the input does not meet these conditions, the skill should return an error or skip notification rather than producing an unreliable analysis.

**Output contract:**
- The skill produces a Moral Disagreement Analysis Report in ARS-compatible Markdown format.
- The report includes metadata tags (`#METAETHICS`, `#DISAGREEMENT`, `#PHASE2`) for pipeline integration.
- The evidential significance rating uses the ARS standard rating vocabulary for cross-skill consistency.

**Integration notes:**
- The report may be consumed by downstream ARS skills (e.g., `phil-moral-epistemology`) without reformatting.
- The report is designed to be included in a cumulative ARS project dossier for eventual synthesis into a full paper analysis.

**State management:**
- This skill does not maintain persistent state between invocations.
- Each analysis is self-contained and does not depend on previous analyses except through explicit input reports.
