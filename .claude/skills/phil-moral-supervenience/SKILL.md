---
description: "Moral Supervenience Analysis — analyze the supervenience of moral properties on natural properties; evaluate Blackburn's supervenience challenge and realist/expressivist responses"
name: phil-moral-supervenience
domain: metaethics
version: 1.0.0
---

# Moral Supervenience Analysis

## Overview

That moral properties supervene on natural properties — that there can be no moral difference without some natural difference — is one of the few near-consensus claims in metaethics. Virtually everyone agrees that if two actions, persons, or states of affairs are identical in all natural (descriptive, non-moral) respects, they must be identical in all moral respects. The question is not whether moral properties supervene on natural properties, but why they do — and what this tells us about the nature of morality.

Simon Blackburn (1971, 1984, 1993) transformed this near-consensus into a powerful challenge to moral realism. If moral properties are distinct, irreducible properties — as the non-naturalist realist claims — then the supervenience of the moral on the natural appears to be a mysterious, unexplained necessity. Why must the moral covary with the natural in this way? The expressivist, by contrast, can explain supervenience as a constraint internal to moral discourse — we refuse to apply different moral predicates to natural duplicates because doing so would violate the very point and purpose of moral language. Thus, Blackburn argues, supervenience is better explained by expressivism than by realism, and this explanatory advantage counts against realism.

This skill provides a systematic framework for analyzing supervenience claims in moral arguments. It specifies the supervenience relation at issue, assesses the explanatory burden it imposes, and evaluates the competing realist and anti-realist attempts to discharge that burden. The skill is designed to be applied after an argument-reconstruction report has been produced and, ideally, after a moral-realism analysis has classified the argument's metaphysical commitments. The form and strength of the supervenience claim, and the difficulty of explaining it, vary significantly depending on whether the argument is committed to non-naturalist realism, naturalist realism, constructivism, or expressivism.

The skill covers the canonical taxonomy of supervenience relations (Kim 1984): weak vs. strong supervenience (strong supervenience holds across possible worlds; weak supervenience holds only within worlds), and global vs. local supervenience (global supervenience is a claim about whole worlds; local supervenience is a claim about individuals or regions). The moral supervenience claim is typically understood as strong and global: any possible world that is naturally identical to the actual world must be morally identical to it. The skill requires the analyst to specify which form of supervenience is claimed or presupposed by the argument.

A central focus is Blackburn's explanatory challenge — the "why supervenience?" question. Why must moral properties supervene on natural properties? This cannot be a brute fact, Blackburn argues, because supervenience is a necessary constraint, and unexplained necessities are objectionable. The realist who treats moral properties as irreducible faces a heavy explanatory burden. The expressivist, by contrast, can treat supervenience as a conceptual constraint built into the function of moral language. The skill requires the analyst to assess whether this explanatory asymmetry is genuine and, if so, how damaging it is to realism.

The skill also evaluates the major realist responses. The conceptual truth response (Jackson 1998) holds that supervenience is analytic — it follows from the very meaning of moral terms via conceptual analysis. The grounding response (Fine, Rosen) holds that moral properties are grounded in natural properties, and the grounding relation explains supervenience. The reductive identification response holds that moral properties just are natural properties, in which case supervenience is explained by identity — it is trivially necessary that if A=B, then A supervenes on B. Each response faces objections, and the skill requires the analyst to assess their viability for the specific argument under analysis.

Finally, the skill considers Dreier's (1992) triviality objection: if supervenience is merely the claim that moral properties cannot differ without some natural difference, this is true of any property whatsoever (since any property supervenes on the total set of all properties including itself). The challenge is to formulate a non-trivial supervenience relation that captures what is distinctive about the moral case. The analyst must assess whether the argument's supervenience claim survives the triviality worry.

## Input

**Required:**
- `argument-reconstruction report` — A completed argument-reconstruction analysis report from the `phil-argument-reconstruct` skill. The supervenience analysis depends on a clear identification of any supervenience claims in the argument, their role in the argumentative structure, and their relationship to the argument's conclusions.

**Optional:**
- `moral-realism analysis report` — A completed moral-realism analysis report from the `phil-moral-realism` skill. This is highly recommended, as the explanatory burden imposed by supervenience depends critically on whether the argument is committed to non-naturalist realism, naturalist realism, reductionism, or anti-realism. The supervenience analysis is most powerful when the metaphysical commitments are clearly specified.
- `grounding-check analysis report` — A completed grounding-check analysis report (from the `phil-grounding-check` skill). This is relevant if the argument makes grounding claims (e.g., "moral properties are grounded in natural properties"), as the grounding relation is closely connected to supervenience. Grounding is often proposed as an explanation of supervenience, and a grounding analysis helps assess this proposal.

**Input format:** Structured reports as Markdown documents. The analyst should verify that the argument-reconstruction report identifies supervenience claims or presuppositions before proceeding.

**Preconditions:** The argument must make or presuppose supervenience claims. Almost all moral arguments implicitly presuppose supervenience (if they didn't, they would permit moral differences without any natural difference, which would be a radical position), but the skill is most productively applied when supervenience is explicitly at issue — either as a premise in an argument, as an explanatory challenge, or as a constraint on acceptable theories.

## Output

The output is a structured **Moral Supervenience Analysis Report** containing the following sections:

1. **Supervenience Relation Specification** — A precise specification of the supervenience relation claimed or presupposed:
   - *Strength:* Weak (within-world) or strong (cross-world, necessitated)?
   - *Scope:* Global (whole-world) or local (individuals, actions, regions)?
   - *Base properties:* What class of properties constitutes the supervenience base? (All natural properties, all descriptive properties, the physical, the non-moral, some restricted subset?)
   - *Supervening properties:* What class of moral properties are claimed to supervene? (All moral properties, thick moral concepts, thin moral concepts, some restricted subset?)
   - *Modal force:* Is the supervenience relation nomologically necessary, metaphysically necessary, or conceptually necessary?

2. **Blackburn's Challenge Assessment** — A reconstruction and assessment of the explanatory challenge:
   - What must be explained? The necessity of the covariance, not the covariance itself.
   - Why is the explanatory burden heavier for the realist than for the expressivist, according to Blackburn?
   - Is the challenge best understood as an inference to the best explanation (expressivism explains supervenience better) or as an argument from explanatory burden (realism cannot explain supervenience at all)?
   - What is the dialectical force of the challenge? Is it a decisive objection or a consideration that must be weighed against others?

3. **Realist Response Evaluation** — A critical assessment of each available realist response:
   - *Conceptual truth response:* Is supervenience an analytic truth following from the meaning of moral terms? (Jackson, Smith)
   - *Grounding response:* Is supervenience explained by the grounding of moral properties in natural properties? (Fine, Rosen, Bader)
   - *Reductive identification response:* Are moral properties identical to natural properties, making supervenience a trivial consequence of identity?
   - *Brute necessity response:* Can the realist accept supervenience as a brute modal fact without further explanation?

4. **Expressivist Response Evaluation** — A critical assessment of the expressivist explanation:
   - Does expressivism genuinely explain supervenience, or does it merely redescribe it?
   - Dreier's triviality challenge: does the expressivist explanation succeed only by trivializing the supervenience relation?
   - Is the expressivist explanation ad hoc, or does it follow naturally from the core commitments of expressivism?
   - The "supervenience of attitudes" problem: does expressivism require a parallel explanation of why moral attitudes supervene on natural attitudes, and is this equally challenging?

5. **Overall Dialectical Status** — A summary judgment on whether the supervenience challenge favors one side in the metaethical debate, using a structured rating scale (e.g., "significantly favors anti-realism," "modestly favors anti-realism," "dialectically neutral," "modestly favors realism," "significantly favors realism").

## Methodological Foundations

**Blackburn's Supervenience Challenge (1971, 1984, 1993).** Simon Blackburn's work on moral supervenience spans three decades. In "Moral Realism" (1971), he first articulated the idea that supervenience poses a problem for realism. In *Spreading the Word* (1984), he developed the argument that expressivism can explain supervenience as a constraint on moral judgment — we are not "allowed" to make different moral judgments about natural duplicates because that would defeat the purpose of moral evaluation. In *Essays in Quasi-Realism* (1993), he refined the argument and responded to objections, including Dreier's triviality challenge. The core Blackburnian argument is that the realist who treats moral properties as distinct from natural properties cannot explain why the moral must covary with the natural — the necessity of the covariance is a "queer" modal fact that realism has no resources to explain. Analysts should distinguish the 1971 argument (focused on explanatory inadequacy) from the 1984 argument (focused on conceptual constraints) and the 1993 refinements (addressing triviality and supervenience of attitudes).

**Dreier's Triviality Objection (1992).** James Dreier's "The Supervenience Argument Against Moral Realism" challenges the claim that supervenience is uniquely problematic for realism. Dreier argues that every property supervenes on the class of all properties (trivially, since any property supervenes on itself). So the existence of a supervenience relation is not itself surprising. The challenge is to specify a non-trivial supervenience base — a restricted set of natural properties on which the moral supervenes — and to explain why the moral supervenes on that restricted set. But Dreier argues that this restricted supervenience may not be necessary — it is a contingent feature of the actual world that moral properties covary with certain natural properties (e.g., the wrongness of an act of killing is tied to the physical properties of the killing), but there are possible worlds where the supervenience base is different. This deflates the explanatory challenge. Analysts must assess whether the argument under analysis formulates the supervenience claim in a way that survives Dreier's critique.

**McPherson's Explanatory Challenge (2012).** Tristram McPherson's "Ethical Non-Naturalism and the Metaphysics of Supervenience" reformulates and sharpens the supervenience challenge. McPherson argues that the non-naturalist realist faces a dilemma: either accept that supervenience is a brute necessity (but then the non-naturalist is committed to a class of unexplained modal facts that are in tension with naturalism) or explain supervenience (but the available explanations — conceptual truth, grounding, reduction — compromise non-naturalism). McPherson's formulation focuses on the tension between non-naturalism and unexplained modal facts, rather than on explanatory competition with expressivism. Analysts should assess which formulation of the challenge is most relevant to the argument under analysis.

**Kim's Supervenience Taxonomy (1984).** Jaegwon Kim's "Concepts of Supervenience" provides the standard taxonomy. Weak supervenience: within any possible world, natural duplicates are moral duplicates. Strong supervenience: across any possible worlds, natural duplicates are moral duplicates. Global supervenience: any two possible worlds that are naturally indistinguishable are morally indistinguishable. The standard moral supervenience claim is strong global supervenience — a very strong modal claim. Analysts should use Kim's taxonomy to specify precisely what supervenience relation is at issue.

**Jackson's Conceptual Analysis Response (1998).** Frank Jackson's *From Metaphysics to Ethics* argues that supervenience is a conceptual truth — it follows from the meaning of moral terms, which can be revealed through conceptual analysis. If moral terms are analyzed in descriptive terms, then supervenience is analytic and unproblematic. This is a form of reductive realism, and its viability depends on the success of conceptual analysis in ethics — a highly contested issue. Analysts should assess whether Jackson's response is available for the specific argument under analysis.

**Fine/Rosen Grounding-Based Response.** Kit Fine and Gideon Rosen have developed grounding as a metaphysical relation distinct from supervenience. Supervenience is a modal correlation; grounding is a non-causal determination relation (the mental is grounded in the physical; the legal is grounded in the social). If moral properties are grounded in natural properties, then supervenience follows as a consequence of grounding — grounding explains why the supervenience relation holds. Analysts should assess whether the grounding response explains the necessity of supervenience or merely redescribes it.

## Steps

### Step 1: Identify and Specify the Supervenience Relation

**Objective:** Identify and precisely specify the supervenience relation claimed or presupposed by the argument.

**Methodological Guidance:**
Begin by examining the argument-reconstruction report for explicit supervenience claims. These may take the form of explicit principles (e.g., "if two actions are identical in all natural respects, they are identical in all moral respects") or implicit presuppositions (the argument's methodology may assume that moral properties covary with natural properties). Also check the moral-realism analysis report and grounding-check analysis report if available.

Key questions to answer for specification:
- *Strength:* Is the supervenience relation weak (within-world only: any two individuals in the same possible world who are natural duplicates are moral duplicates) or strong (cross-world: any two individuals in any possible worlds who are natural duplicates are moral duplicates)? Strong supervenience is a much more demanding claim and raises a correspondingly greater explanatory challenge.
- *Scope:* Is the supervenience relation global (applying to whole worlds: any possible world naturally identical to the actual world is morally identical to it) or local (applying to individuals or actions within a world)? Global supervenience is standard; local supervenience is weaker.
- *Base properties:* What class of properties constitutes the supervenience base? Candidates: all natural properties (the broadest class), all physical properties, all descriptive/non-normative properties, or some specific subset (e.g., properties of pleasure and pain, properties of agency and harm). The narrower the base, the more interesting and controversial the supervenience claim.
- *Supervening properties:* What class of moral properties are claimed to supervene? All moral properties (thick and thin), only thin moral concepts (right, wrong, good, bad), only thick moral concepts (brave, cruel, generous), or some specific subset relevant to the argument?
- *Modal force:* What kind of necessity governs the supervenience relation? Conceptual necessity (true in virtue of the meaning of moral terms), metaphysical necessity (true in all metaphysically possible worlds), nomological necessity (true in all worlds with the same natural laws), or merely de facto covariation (true in the actual world but not necessarily)?

**Output of this step:** A precise, Kim-style specification of the supervenience relation, with explicit justification for each dimension of the specification.

**Pitfalls to avoid:**
- Assuming that the argument is committed to strong global supervenience when it may only require a weaker form.
- Conflating supervenience with reduction — supervenience is a covariance claim that does not by itself imply reduction or identity.
- Failing to specify the supervenience base precisely, which leaves the claim vague and makes the explanatory challenge harder to assess.

### Step 2: Reconstruct Blackburn's Explanatory Challenge

**Objective:** Reconstruct the challenge that the supervenience relation poses for moral realism.

**Methodological Guidance:**
The core of Blackburn's challenge is the "why supervenience?" question. Given that moral properties supervene on natural properties with (typically) strong modal force, the realist must explain why this modal correlation holds. Reconstruct the challenge as a dilemma or an inference to the best explanation.

The explanatory challenge has several formulations:

*Formulation 1: Inference to the best explanation.*
1. Moral properties strongly supervene on natural properties.
2. Realism treats moral properties as distinct, irreducible properties.
3. Expressivism treats moral judgments as expressions of attitudes, and supervenience as a conceptual constraint on those attitudes.
4. Expressivism provides a better explanation of the supervenience relation than realism does.
5. Therefore, supervenience favors expressivism over realism.

*Formulation 2: Explanatory burden.*
1. If realism is true and moral properties are distinct from natural properties, the supervenience of the moral on the natural is a brute, unexplained necessity.
2. Brute, unexplained necessities are objectionable (in general, or in the moral case specifically).
3. Therefore, realism incurs a significant explanatory cost.

*Formulation 3: McPherson's dilemma for non-naturalism.*
1. Non-naturalist realism holds that moral properties are sui generis and not reducible to natural properties.
2. If supervenience is a brute necessity, non-naturalism is committed to unexplained modal facts that are in tension with a naturalistic worldview.
3. If supervenience is explained (by conceptual truth, grounding, or reduction), the explanation compromises non-naturalism by making moral properties naturalistically respectable.
4. Therefore, non-naturalist realism faces an unresolved tension.

Identify which formulation(s) are most relevant to the argument under analysis. The challenge is strongest when directed at non-naturalist realism and weakest when directed at naturalist reductionism (where supervenience is explained by identity).

**Output of this step:** A clear statement of the explanatory challenge, in the formulation most relevant to the argument, with identification of the premises that would need to be defended for the challenge to succeed.

**Pitfalls to avoid:**
- Conflating different formulations of the challenge that have different dialectical force.
- Assuming that the challenge applies equally to all forms of realism — it applies much more forcefully to non-naturalism than to naturalism.
- Neglecting Dreier's preliminary point: the mere fact of supervenience is not surprising; the challenge is to explain a specific, non-trivial supervenience relation.

### Step 3: Assess the Explanatory Burden

**Objective:** Assess the weight of the explanatory burden imposed by the supervenience relation.

**Methodological Guidance:**
The central question is: how heavy is the explanatory burden, and who bears it? This requires assessing both sides of the dialectic.

*For the realist:* How difficult is it to explain moral supervenience given realism?
- If the realist is a naturalist reductionist (moral properties are natural properties), supervenience is trivially explained — it follows from identity. No explanatory burden.
- If the realist is a non-naturalist but accepts grounding (moral properties are grounded in natural properties), the explanatory burden shifts to explaining the grounding relation. Can grounding explain the necessity of supervenience without collapsing into reduction?
- If the realist is a non-naturalist who rejects grounding, the supervenience relation is a brute modal fact. How costly is this? Compare: the relation between mental and physical properties also involves supervenience with no consensus explanation; the relation between the special sciences and fundamental physics involves similar modal correlations. Are these accepted as brute, or do they also pose a challenge?

*For the expressivist:* How good is the expressivist explanation?
- The expressivist explains supervenience as a constraint on moral judgment: we cannot consistently make different moral judgments about natural duplicates because moral judgment involves a commitment to consistency in the application of moral predicates to naturally identical cases.
- But does this explain why the constraint exists, or does it merely redescribe it? The realist can also note that we apply moral predicates consistently.
- The expressivist explanation appears to make supervenience a conceptual necessity (arising from the nature of moral judgment), which may be plausible but does not settle the question of whether moral properties (as opposed to moral concepts) supervene — a metaphysical question that expressivism may lack the resources to address.

*Comparative assessment:* Is the explanatory burden for the realist heavier than for the expressivist? If both face burdens (the realist must explain a metaphysical correlation; the expressivist must explain a conceptual constraint), is one burden heavier? The analyst should avoid simply assuming that expressivism has the upper hand — this is precisely what is at issue.

Consider also whether the explanatory burden is dialectically significant. Even if realism cannot fully explain supervenience, the failure to explain one modal fact may not be a decisive objection. The explanatory burden argument may shift the burden of proof without deciding the issue.

**Output of this step:** A calibrated assessment of the explanatory burden for each position, with a comparative evaluation.

**Pitfalls to avoid:**
- Assuming that the realist bears all the explanatory burden and the expressivist bears none.
- Failing to distinguish between the burden of explaining the covariance (which may be manageable) and the burden of explaining the modal force (which is harder).
- Neglecting that the realist may have resources (grounding, conceptual analysis, reduction) that the expressivist also needs to explain other phenomena.

### Step 4: Evaluate Realist Responses

**Objective:** Critically assess the three main realist responses to the supervenience challenge.

**Methodological Guidance:**
Evaluate each response in its strongest form, considering both its explanatory power and its costs.

*Conceptual Truth Response (Jackson, Smith):* The claim is that moral supervenience is an analytic or conceptual truth — it follows from the meaning of moral terms that they cannot differ without a natural difference. Assessment considerations:
- Can moral terms be given a conceptual analysis that entails supervenience? This requires that moral terms have descriptive content that determines their extension. The success of this response depends on the success of the Canberra Plan or some other form of conceptual analysis.
- Does the conceptual truth response work only for reductive naturalism? If the analysis identifies moral properties with natural properties, it is a form of reductionism, not merely a response to the supervenience challenge.
- Objections: Moore's open question argument suggests that moral terms cannot be analytically reduced to natural terms. The failure of the Canberra Plan in ethics (the "location problem" for moral properties) may indicate that no conceptual analysis is forthcoming.
- Even if supervenience is not analytic, it may be a "conceptual truth" in a broader sense — a constraint we implicitly accept through our competence with moral concepts. This would explain why supervenience seems obvious without requiring a full analysis.

*Grounding Response (Fine, Rosen):* The claim is that moral properties are grounded in natural properties, and grounding explains supervenience. Assessment considerations:
- Grounding is a non-causal determination relation: the moral facts obtain in virtue of the natural facts. If moral facts are grounded in natural facts, then any difference in moral facts requires a difference in the grounding natural facts — which is exactly the supervenience claim.
- Does grounding explain supervenience, or does supervenience explain grounding? If grounding just is the relation that backs supervenience, the explanation may be circular.
- Does the grounding response preserve non-naturalism? If moral properties are grounded in natural properties, in what sense are they non-natural? Some argue that grounding is compatible with non-naturalism (grounded properties need not be reducible to their grounds); others argue that grounding collapses non-naturalism into naturalism.
- The grounding response shifts the explanatory burden from supervenience to grounding: why is the grounding relation itself necessary? This may be a more tractable question, but it is not cost-free.

*Reductive Identification Response:* The claim is that moral properties are identical to (or constituted by) natural properties, in which case supervenience is a trivial consequence of identity (if A=B, then necessarily A supervenes on B because A just is B). Assessment considerations:
- This response is only available to naturalist realists who accept identity claims for moral properties (e.g., rightness = maximization of utility, goodness = satisfaction of desire).
- The main cost is the commitment to specific reductive identifications, which are highly controversial in ethics.
- Even if full reduction is unavailable, partial reduction (identifying moral properties with complex natural properties) or constitution (moral properties are constituted by but not identical to natural properties) may explain supervenience while preserving some autonomy for the moral.
- Does this "response" concede the anti-realist's point? If the realist must be a reductionist to explain supervenience, and reductionism is independently unattractive, then supervenience pushes toward reductionism — which may itself be a conclusion the anti-realist welcomes.

*Brute Necessity Response:* The claim is that the realist can simply accept supervenience as a brute modal fact that does not require further explanation. Assessment considerations:
- Not every necessary connection requires explanation. Some necessities (logical truths, mathematical truths) are brute in the sense that they are not explained by anything more fundamental.
- The question is whether moral-natural supervenience is relevantly similar to other unexplained necessities, or whether its modal status makes it distinctively problematic.
- McPherson argues that brute necessities are especially objectionable for non-naturalists because they introduce a class of "queer" modal facts that sit uneasily with a naturalistic worldview. But the force of this objection depends on the strength of one's commitment to naturalism.

**Output of this step:** A structured evaluation of each realist response, with an assessment of which response(s) are most promising for the specific argument under analysis.

**Pitfalls to avoid:**
- Treating the responses as mutually exclusive — a realist might combine grounding and conceptual truth, for example.
- Assuming that any single response must fully explain supervenience — the realist may only need to show that the explanatory burden is not uniquely heavy for realism.
- Evaluating responses in the abstract rather than against the specific supervenience claim made by the argument.

### Step 5: Evaluate Expressivist Response and Dreier's Triviality Challenge

**Objective:** Critically assess whether expressivism genuinely explains supervenience better than realism.

**Methodological Guidance:**
Blackburn's expressivist explanation: moral judgments express attitudes, not beliefs. The function of moral language is to guide action and coordinate attitudes. This function imposes a consistency constraint: we cannot coherently express different moral attitudes toward natural duplicates because such inconsistency would undermine the practical function of moral discourse. Supervenience is thus a constraint on the coherence of moral attitudes.

Assess this explanation:
- *Explanatory power:* Does the expressivist explanation genuinely explain why supervenience holds, or does it merely explain why we accept that supervenience holds? The realist might accept the psychological explanation (we accept supervenience because of the practical function of moral judgment) while maintaining that supervenience is also a metaphysical truth. The expressivist needs the stronger claim: supervenience is nothing over and above this conceptual constraint.
- *Dreier's triviality challenge (1992):* Dreier argues that expressivism explains supervenience only by trivializing it. The expressivist says we are committed to applying moral terms consistently to natural duplicates. But we are committed to applying any term consistently to natural duplicates — this is just the principle that like cases should be treated alike. So expressivism does not explain anything distinctively moral. The expressivist can respond that moral consistency is a specific, substantive constraint arising from the action-guiding role of moral language, not the generic principle of treating like cases alike. But spelling this out in a non-question-begging way is challenging.
- *The supervenience of attitudes problem:* The expressivist must also explain why moral attitudes supervene on natural attitudes. If expressivism is true, moral judgments are attitudes. But attitudes also exhibit a supervenience pattern: we do not think it is coherent to have different moral attitudes toward natural duplicates. Why does this supervenience of attitudes hold? The expressivist may face a parallel explanatory challenge that is no easier than the realist's challenge about moral properties.
- *The "no property" problem:* Expressivists deny (or quasi-realists earn the right to speak as if there are) moral properties. But the supervenience claim is typically stated as a claim about properties: moral properties supervene on natural properties. If there are no moral properties (strictly speaking), what is the content of the supervenience claim? The expressivist must reformulate supervenience in terms of predicates, concepts, or attitudes. Does this reformulation capture everything the supervenience intuition requires?

**Output of this step:** A balanced assessment of the expressivist explanation, including whether it survives Dreier's triviality challenge and whether it imposes its own explanatory burdens.

**Pitfalls to avoid:**
- Assuming that expressivism automatically wins the explanatory competition without critically examining the expressivist explanation.
- Neglecting to consider whether the expressivist's own explanatory burdens (supervenience of attitudes, triviality, "no property" problem) are as heavy as the realist's.
- Treating Dreier's triviality challenge as decisive without considering expressivist replies.

### Step 6: Compile Report with Dialectical Assessment

**Objective:** Produce the final Moral Supervenience Analysis Report with an overall dialectical status rating.

**Methodological Guidance:**
Integrate the findings from Steps 1 through 5 into a comprehensive report. The dialectical status rating should reflect the balance of considerations:

- **Significantly favors anti-realism:** The supervenience challenge is a powerful objection to moral realism. Realist responses are inadequate, and the expressivist explanation is convincingly superior. Supervenience provides a strong reason to reject non-naturalist realism and/or to adopt expressivism.
- **Modestly favors anti-realism:** The supervenience challenge has some force, but realist responses partially succeed. The explanatory burden is heavier for the realist, but not decisively so. Supervenience counts against realism but is not a decisive consideration.
- **Dialectically neutral:** The supervenience challenge and realist responses are in equipoise. The explanatory burdens are comparable for realism and expressivism, or the challenge can be defused entirely (e.g., by reductive naturalism or by showing that the supervenience claim at issue is trivial).
- **Modestly favors realism:** Realist responses successfully defuse the supervenience challenge. The supervenience relation is adequately explained by grounding, conceptual truth, or reduction. The expressivist explanation faces equal or greater difficulties (triviality, supervenience of attitudes).
- **Significantly favors realism:** The supervenience relation is better explained by realism than by expressivism. Perhaps supervenience supports a reductive form of realism and this is independently motivated; the expressivist alternative is untenable.

The report should also identify which form of realism (naturalist, non-naturalist, constructivist) is most favored or disfavored by the supervenience analysis. Since the supervenience challenge primarily targets non-naturalist realism, the analysis may support naturalist realism without supporting anti-realism more broadly.

The report should conclude with a summary of the key dialectical moves and identify any unresolved issues that would benefit from further analysis (e.g., whether grounding provides a genuine explanation, whether Dreier's triviality challenge can be met, whether the necessity of supervenience must be explained at all).

**Output of this step:** The complete Moral Supervenience Analysis Report.

## Quality Criteria

1. **Supervenience Specification Precision:** The report must precisely specify the supervenience relation using Kim's taxonomy. Vague or underspecified claims ("moral properties depend on natural properties") are insufficient. The report should distinguish weak from strong supervenience, global from local, and should identify the modal force and the base/supervening property classes.

2. **Blackburn's Challenge Clarity:** The report must articulate Blackburn's challenge clearly and distinguish it from related but distinct arguments. The challenge is not that supervenience is inconsistent with realism, but that realism cannot explain it as well as expressivism can. The report should identify which formulation of the challenge is at issue and avoid conflating formulations with different dialectical force.

3. **Explanatory Burden Fairness:** The assessment of explanatory burdens must be even-handed. The report should not assume that the realist bears a heavy burden and the expressivist bears none. Both positions face explanatory challenges, and the report should assess the comparative weight of these challenges without prejudging the outcome.

4. **Response Evaluation Depth:** Realist and expressivist responses should be evaluated in depth, not merely catalogued. The report should identify the strongest versions of each response, articulate the objections they face, and assess whether those objections are decisive. Straw-manning either side reduces the report's credibility and diagnostic value.

5. **Triviality Concern Awareness:** The report must engage with Dreier's triviality challenge. It should assess whether the supervenience claim at issue is non-trivial (i.e., involves a restricted supervenience base) and whether the triviality concern undermines the dialectical significance of the supervenience debate. Ignoring triviality is a significant omission.

## Relations to Other Skills

**Dependencies (skills this skill requires as input):**
- `phil-moral-realism` — Optional but highly recommended. The force of the supervenience challenge depends on the specific form of realism at issue. Non-naturalist realism faces the heaviest explanatory burden; naturalist reductionism faces none. The moral-realism analysis report provides essential context.
- `phil-grounding-check` — Optional. If the argument makes grounding claims, a grounding-check analysis helps assess whether grounding can explain supervenience. The grounding-check report may be integrated into the supervenience analysis.

**References (knowledge resources this skill draws upon):**
- `glossary-metaethics.md` — For definitions of key metaethical terms (realism, anti-realism, naturalism, non-naturalism, expressivism, supervenience, grounding).
- `glossary-metaphysics.md` — For definitions of metaphysical terms (supervenience, grounding, modal force, possible worlds, necessity).
- `argument-forms/moral-supervenience.md` — A canonical formulation of the supervenience argument, useful for standardization and comparison.

**Downstream skills (skills that may use this skill's output):**
- `phil-moral-realism` — If the supervenience analysis reveals tensions in the argument's realist commitments, these may need to be incorporated into an updated moral-realism analysis.
- ARS synthesis skills — The Moral Supervenience Analysis Report is a component of the full metaethical analysis and is used in ARS Phase 4 synthesis.

## Boundary Conditions

**When to apply this skill:**
- The argument makes explicit supervenience claims (e.g., "moral properties supervene on natural properties").
- The argument is a Blackburn-style supervenience challenge to moral realism.
- The argument presupposes supervenience in a way that bears on its metaethical conclusions (e.g., an argument that relies on the impossibility of moral differences without natural differences).
- The argument responds to a supervenience-based challenge, either defending realism or advancing expressivism.

**When to skip this skill:**
- The argument makes no supervenience claims and does not presuppose any supervenience relation that bears on its conclusions.
- The argument is purely first-order normative and does not engage with the metaphysical or semantic dimensions of supervenience.
- The argument is committed to reductive naturalism and explicitly treats supervenience as a trivial consequence of identity — in this case, supervenience analysis adds little beyond what the moral-realism analysis already provides.

**Edge cases and special handling:**
- *Committed to reductive naturalism:* If the argument explicitly commits to reductive naturalism (moral properties are identical to natural properties), supervenience is trivially explained by identity. Note this in the report and proceed to assess whether the reductive identifications are defensible. The supervenience analysis may be brief — the interesting questions shift to whether reductionism is viable.
- *Purely first-order argument:* If the argument is purely first-order but the analyst detects implicit supervenience presuppositions, offer to elevate the analysis to the meta-level. Do not impose a supervenience analysis where the argument does not engage with the metaethical issues. Note the implicit presuppositions and explain their significance for meta-level analysis.
- *Multiple supervenience claims:* If the argument makes multiple supervenience claims (e.g., weak supervenience for thick concepts, strong supervenience for thin concepts), analyze each separately and assess their interactions.
- *Supervenience and grounding:* If the argument makes both supervenience and grounding claims, coordinate with the grounding-check analysis if available. The relationship between supervenience and grounding is contested (some take grounding to explain supervenience, others take them to be independent), and the report should navigate this controversy carefully.

## ARS Interface

This skill is part of the Academic Research Skills (ARS) metaethics pipeline (Phase 2: Metaethical Analysis). It conforms to the ARS skill interface specification.

**Trigger conditions:**
- The ARS orchestrator invokes this skill when the argument-reconstruction report identifies supervenience claims and the pipeline workflow specifies metaethical analysis.
- This skill may also be invoked manually when a user requests analysis of a moral supervenience argument.

**Input contract:**
- The skill expects a valid argument-reconstruction report in the ARS standard format.
- The report must include identifiable supervenience claims or clear supervenience presuppositions.
- If the input does not meet these conditions, the skill should return an error or skip notification.

**Output contract:**
- The skill produces a Moral Supervenience Analysis Report in ARS-compatible Markdown format.
- The report includes metadata tags (`#METAETHICS`, `#SUPERVENIENCE`, `#PHASE2`) for pipeline integration.
- The dialectical status rating uses the ARS standard rating vocabulary for cross-skill consistency.

**Integration notes:**
- The report may be consumed by downstream ARS skills (e.g., synthesis, reviewer critique) without reformatting.
- The report is designed to be included in a cumulative ARS project dossier.
- The supervenience analysis is complementary to the moral-realism analysis and the grounding-check analysis — together they provide a comprehensive metaphysical profile.

**State management:**
- This skill does not maintain persistent state between invocations.
- Each analysis is self-contained and does not depend on previous analyses except through explicit input reports.
