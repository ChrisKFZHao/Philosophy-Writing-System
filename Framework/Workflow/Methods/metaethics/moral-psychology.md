---
id: method.metaethics.moral-psychology
package: metaethics
legacy_ids: [phil-moral-psychology]
label: Moral Psychology Analysis
consumers: [phil-research/reconstruct, phil-write]
selector: feature-detected
side_effects: read-only
---

# Moral Psychology Analysis (method.metaethics.moral-psychology)

> Internal method module — not a registered runtime skill. Loaded on demand by the consuming skill's mode contract through the manifest resolver; never loaded wholesale.

# Moral Psychology Analysis

## Overview

The relation between moral judgment and motivation is a crux of metaethics — it constrains what kind of thing a moral judgment could be. If moral judgments necessarily motivate (motivational internalism), this favors non-cognitivism: attitudes motivate, but beliefs alone do not (per the Humean theory of motivation). If it is possible to sincerely judge that one ought to φ without being motivated to φ (motivational externalism), cognitivism remains viable — moral judgments can be beliefs that only contingently motivate, with motivation provided by additional factors such as desire, character, or concern. This skill analyzes an argument's psychological commitments, tests them against canonical counterexamples (the amoralist and the akratic agent), and traces their metaethical implications.

The skill classifies the argument's position on motivational internalism/externalism with precision — distinguishing strong motivational internalism, weak motivational internalism, rational internalism, and motivational externalism. It diagnoses the argument's commitment to the Humean theory of motivation (the belief-desire model) or an anti-Humean alternative. It systematically tests the argument's handling of the amoralist — the person who sincerely judges that φ is morally required but feels no motivation to φ — which is the primary counterexample to strong and weak internalism. It also tests the argument's handling of akrasia — knowing the better but doing the worse — which challenges rational internalism. The analysis culminates in an assessment of what the motivational view entails about the nature of moral judgment: which metaethical positions (cognitivist realism, non-cognitivism, error theory, constructivism, constitutivism) are compatible with the argument's moral psychology, and which are ruled out.

Moral psychology is not an isolated subdomain of metaethics — it is the linchpin connecting semantics, metaphysics, and normativity. An argument's moral psychology determines the space of viable semantic theories (expressivism does well with internalism; cognitivism requires externalism or anti-Humeanism) and constrains its normative theory (reasons internalism and motivational internalism are distinct but mutually reinforcing). The analysis must trace these connections explicitly.

## Input

**Required:**
- `argument-reconstruction` report (output of `method.argument.argument-reconstruct`): A structured representation of the argument's premises and conclusions, with particular attention to claims about moral judgment, motivation, desire, belief, and action. The reconstruction must capture the argument's psychological claims in their logical relations to other claims.

**Optional:**
- `normativity-analysis` report (output of `method.metaethics.normativity`): Provides the reasons internalism/externalism diagnosis that may parallel or constrain the motivational analysis. Reasons internalism (reasons depend on the agent's motivational set) and motivational internalism (moral judgment entails motivation) are distinct theses, but they interact: an argument that is reasons-internalist (Williams-style) has a natural affinity with motivational internalism, and the normativity report supplies the needed context.
- `original-text`: The primary source text, for context-sensitive interpretation of psychological claims. Particularly useful when the argument's psychological vocabulary ("desire," "motivation," "reason") is used in non-standard ways that the reconstruction may normalize.

## Output

The skill produces a **Moral Psychology Analysis Report** structured according to the `moral-psychology-schema.json` specification. The report contains six principal sections:

**1. Internalism/Externalism Classification**

Precise classification of the argument's position on the relation between moral judgment and motivation:

- `strong_motivational_internalism`: Sincere moral judgment necessarily involves motivation to act accordingly. Judgment entails motivation — it is conceptually impossible to judge that one ought to φ and lack all motivation to φ.
- `weak_motivational_internalism`: Sincere moral judgment normally or defeasibly involves motivation. The connection holds absent defeating conditions (depression, exhaustion, ideological false consciousness), but these conditions can sever it.
- `rational_internalism`: Moral judgment entails that a rational agent would be motivated to act accordingly. The connection runs through rationality, not through judgment directly. An irrational agent may judge that she ought to φ and lack motivation, but this is a rational failing.
- `motivational_externalism`: Moral judgment does not necessarily involve motivation at all. Motivation requires additional factors — a desire to be moral, a concern for others, a character trait — that are contingently present or absent. It is fully possible to sincerely judge that one ought to φ and lack all motivation to φ without any rational or conceptual defect.

Each classification is accompanied by textual evidence and an analysis of how the position handles the amoralist and the akratic agent.

**2. Humean/Anti-Humean Diagnosis**

Classification of the argument's theory of motivation:
- `humean`: Beliefs represent the world; desires set ends. Neither alone can motivate action; only a belief-desire pair produces intention and action. "Reason is, and ought only to be, the slave of the passions."
- `anti_humean`: Beliefs alone can motivate. A belief about what one ought to do can directly produce motivation without the mediation of a distinct desire.
- `hybrid`: Beliefs can motivate, but only when combined with certain standing desires or dispositions. Motivation requires both cognitive and conative elements, but the cognitive element can be a moral belief.
- `not_specified`: The argument does not address the Humean theory of motivation.

**3. Amoralist Handling Assessment**

Systematic evaluation of how the argument's view handles the amoralist — the sincere-but-unmotivated moral judge. For each internalism/externalism position, the report assesses whether the amoralist is: (a) conceptually impossible, (b) possible but abnormal/irrational, (c) fully possible and unproblematic, or (d) not addressed by the argument.

**4. Akrasia Analysis**

Systematic evaluation of how the argument's view handles akrasia — knowing the better but doing the worse. For each position, the report assesses: whether akrasia is possible under the view, whether the view makes it too easy or too hard, and whether the view's account of akrasia is empirically adequate.

**5. Motivational Architecture Map**

A structural description of how moral judgment, desire, belief, intention, and action are causally and rationally related in the argument's psychological picture. This includes the direction of fit (mind-to-world for belief, world-to-mind for desire) and the "because" chain from judgment to action.

**6. Metaethical Implications**

A systematic mapping of the argument's moral psychology to compatible and incompatible metaethical positions. Uses the framework of Smith's "moral problem" (the trilemma of cognitivism, internalism, and Humeanism) to structure the analysis where applicable.

## Methodological Foundations

This skill draws on the following key philosophical resources and debates. Each entry describes the core contribution and how it is operationalized.

**1. Hume's Theory of Motivation (the Belief-Desire Model)** (A Treatise of Human Nature, Book II, Part III, Section III, 1739)

Hume argues that reason alone cannot motivate action. Beliefs represent how the world is (they have a mind-to-world direction of fit); desires represent how we want the world to be (they have a world-to-mind direction of fit). Only the combination of a belief (identifying a means) and a desire (setting an end) can produce an intention and action. "Reason is, and ought only to be, the slave of the passions, and can never pretend to any other office than to serve and obey them."

*Operationalization*: The Humean theory is the default psychological framework in metaethics — departures from it must be explicitly argued. The skill diagnoses whether the argument is Humean by checking whether it treats desires as necessary for motivation and whether it treats beliefs as motivationally inert by themselves. The Humean diagnosis constrains the viable metaethical positions via the "moral problem" trilemma: if Humeanism is true and internalism is true, then cognitivism (moral judgments are beliefs) is false.

**2. Smith's Motivational Internalism and the Fetishism Argument** (The Moral Problem, 1994)

Smith identifies the "moral problem" as the apparent inconsistency of three plausible claims: (1) moral judgments express beliefs (cognitivism — required for moral objectivity), (2) moral judgments necessarily motivate (internalism — required for moral practicality), and (3) beliefs alone cannot motivate (Humean theory of motivation). These three cannot all be true. Smith's solution: reject (2) in its strong form and defend rational internalism — the good and rational person would be motivated by the content of their moral beliefs, so motivation tracks rationality rather than being internal to moral judgment per se.

Smith's "fetishism argument" targets motivational externalism: if moral judgment motivates only contingently, then being motivated by one's moral judgment is merely a fetish — a non-rational attachment to doing what one judges right. The genuinely moral person is motivated by the features that make the action right (e.g., the suffering it alleviates), not by the fact that it is right. Externalism makes moral motivation look like a de dicto concern for rightness rather than a de re concern for the right-making features, and this, Smith argues, is a form of moral fetishism.

*Operationalization*: The "moral problem" trilemma provides the organizing framework for Step 6 (Metaethical Implications). The fetishism argument provides a critical tool for evaluating externalist views — if the argument is externalist, does it have a response to the fetishism charge? Does it ground moral motivation in the right-making features rather than in the property of rightness itself?

**3. The Amoralist Challenge** (Brink, Moral Realism and the Foundations of Ethics, 1989; Shafer-Landau, Moral Realism: A Defence, 2003)

The amoralist is the primary counterexample to strong motivational internalism. The amoralist:
- Sincerely judges that φ is morally required.
- Fully understands what this judgment means (the amoralist is not conceptually confused about moral concepts).
- Has no motivation whatsoever to φ.
- May even actively desire to do the opposite of what they judge required.

If such a person is conceptually possible — and some argue that actual cases (depression, exhaustion, severe sociopathy) approximate it — then strong motivational internalism is false: moral judgment does not conceptually entail motivation. The externalist argues that actual amoralists exist; the internalist responds that apparent amoralists either lack full-fledged moral judgment (they use moral words in an "inverted commas" sense) or have some motivation at a deeper level.

*Operationalization*: The amoralist test is the core of Step 4. The analysis does not merely classify whether the argument addresses the amoralist — it tests whether the argument's psychological view *can* accommodate the amoralist, given its other commitments. An internalist view that must deny the conceptual possibility of the amoralist bears the burden of explaining away apparent cases.

**4. The Akrasia Puzzle** (Davidson, "How Is Weakness of the Will Possible?," 1970)

Akrasia — weakness of will, knowing the better but doing the worse — involves a sincere all-things-considered judgment that φ is better than ψ, combined with a free and intentional choice of ψ. Akrasia seems to be a pervasive empirical phenomenon. But it poses a puzzle: if an agent judges that φ is better, all things considered, and is free to choose φ, why would she choose ψ? Davidson's analysis: the akratic agent's all-things-considered judgment is a conditional judgment ("φ is better, given all the reasons") that does not amount to an unconditional judgment ("φ is better, period"), and the agent acts on an unconditional judgment that contradicts the conditional one.

*Operationalization*: The akrasia test is the core of Step 5. For internalist views, the analysis must determine whether the internalist motivation is treated as sufficient for action (which would preclude akrasia entirely — empirically implausible) or merely as one contributory motivational force among others (which allows akrasia but may weaken internalism's claim that moral judgment *necessarily* motivates in a practically significant sense).

**5. The Practicality Requirement on Moral Judgment**

An influential metaethical constraint holds that moral judgments must have a conceptual connection to motivation — it is part of the concept of a moral judgment that it is action-guiding. The strength of this requirement varies across views:
- Strong formulations (Stevenson, Hare): Moral judgment necessarily motivates by itself. Without this connection, moral judgment would not be "practical" in the required sense.
- Weaker formulations (Smith, Korsgaard): Moral judgment rationally requires motivation, but irrational agents may fail to be motivated.
- Externalist rejections (Brink, Shafer-Landau): There is no conceptual connection between moral judgment and motivation. The practicality of morality is a substantive normative claim, not a conceptual truth.

*Operationalization*: The practicality requirement provides the dialectical backdrop for Steps 2-6. The analysis identifies which version of the practicality requirement the argument assumes (if any) and whether this assumption can be sustained given the argument's other commitments.

## Steps

### Step 1: Extract Motivational Claims

Identify all claims in the argument-reconstruction report that relate moral judgment to motivation, desire, belief, intention, or action. This is the foundational data-gathering step.

**Procedural guidance:**

1. **Scan for explicit psychological claims**:
   - **Internalist claims**: "To judge that one ought to φ is to be motivated to φ," "Moral judgment necessarily involves motivation," "Sincere moral judgment entails corresponding motivation," "It is part of the concept of moral judgment that it motivates," "If someone is not motivated by their moral judgment, they do not genuinely hold it."
   - **Externalist claims**: "Moral judgment does not necessarily motivate," "One can judge that φ is wrong without any inclination to avoid φ-ing," "Motivation is external to moral judgment — it requires additional factors like desire or character," "The amoralist is conceptually possible."
   - **Desire-dependence claims**: "Desire is required for any motivation," "Belief alone cannot move to action," "Reason alone is inert," "Motivation requires both a belief and a desire," "Practical reason is the slave of the passions."
   - **Anti-Humean claims**: "Beliefs alone can motivate," "The belief that one ought to φ can directly produce motivation to φ," "Practical reason can be motivating by itself."
   - **Rational connection claims**: "The rational person would be motivated by their moral judgments," "Moral judgment provides reasons that a rational agent would act on," "The connection between judgment and motivation runs through rationality."
   - **Akrasia claims**: "One can know the better and do the worse," "Moral judgment does not guarantee action," "Weakness of will is possible."
   - **Amoralist claims**: "The amoralist is conceptually possible," "Some people judge that φ is wrong without any motivation to avoid φ-ing," "Sociopaths make genuine moral judgments without corresponding motivation."

2. **For each claim, record**:
   - Exact textual location (premise number, paragraph).
   - The exact wording.
   - The psychological commitment it entails (internalism/externalism, Humean/anti-Humean, etc.).
   - Whether the claim is fundamental (a premise) or derived (a conclusion).

3. **Flag implicit psychological commitments**: The argument may deploy motivational concepts without theorizing about them. If the argument assumes that "moral judgment motivates" without arguing for it, note this as an implicit internalist commitment. If the argument deploys a model of action explanation that presupposes the belief-desire framework, note this as an implicit Humean commitment.

4. **Produce a motivational claim inventory**: A table with columns: ID, Text/Location, Claim Type (internalist/externalist/Humean/anti-Humean/akrasia/amoralist), Status (basic/derived/implicit). This table is the working document for Steps 2-6.

### Step 2: Classify Internalism/Externalism

Classify the argument's position on motivational internalism with the greatest possible precision.

**Procedural guidance:**

1. **Use the classification schema**:

| Position | Definition | Motivation Condition | Key Proponent(s) | Amoralist Status |
|---|---|---|---|---|
| Strong Motivational Internalism | Sincere moral judgment necessarily involves motivation | Judgment entails motivation | Early non-cognitivists (Ayer, early Stevenson) | Conceptually impossible |
| Weak Motivational Internalism | Sincere moral judgment normally/defeasibly involves motivation | Judgment normally entails motivation, absent defeaters | Smith (one reading), Dancy | Possible but abnormal |
| Rational Internalism | Moral judgment entails that a rational agent would be motivated | Judgment entails reasons that would motivate a rational agent | Smith (1994), Korsgaard | Possible but irrational |
| Motivational Externalism | Moral judgment does not necessarily involve motivation | Judgment alone entails no motivation | Brink, Shafer-Landau, Railton, Svavarsdóttir | Fully possible |

2. **Apply diagnostic questions**:
   - Does the argument treat the amoralist as conceptually impossible? If yes, strong internalism.
   - Does the argument allow that the amoralist is possible but insist that something has gone wrong (depression, irrationality, false consciousness)? If yes, weak or rational internalism.
   - Does the argument treat the amoralist as a fully possible, unproblematic case? If yes, externalism.
   - Does the argument ground motivation in rationality rather than in judgment directly? If yes, rational internalism.
   - Does the argument allow that moral judgment and motivation are "distinct existences" (Hume) that only contingently co-occur? If yes, externalism.

3. **Distinguish weak from rational internalism**:
   - Weak internalism: the connection between judgment and motivation is *psychological* — it normally holds, but psychological defeaters (depression, exhaustion) can break it.
   - Rational internalism: the connection between judgment and motivation is *normative* — it is a requirement of rationality. The irrational agent fails to be motivated, but this is a rational failing, not merely a psychological one.

4. **Provide evidence**: "The argument is classified as rational internalist because it grounds moral motivation in 'what a practically rational agent would do' (Premise 5) and treats the amoralist as 'irrational' rather than as conceptually impossible (paragraph 8)."

5. **Flag tensions**: If the argument's view is unstable between two positions, flag this. "The argument asserts strong internalism at Premise 3 ('to judge that one ought to φ is to be motivated to φ') but later accommodates the amoralist as 'a person suffering from weakness of will' (paragraph 12). These commitments are in tension: strong internalism rules out the amoralist as conceptually impossible, but the argument treats the amoralist as possible."

### Step 3: Diagnose Humean/Anti-Humean Framework

Determine the argument's theory of motivation — the psychological framework within which moral judgment operates.

**Procedural guidance:**

1. **Classify the framework**:
   - `humean`: Beliefs represent facts; desires set ends. Neither alone can motivate; only a belief-desire pair produces intention and action. The direction-of-fit metaphor: beliefs have mind-to-world direction of fit (they aim to match the world); desires have world-to-mind direction of fit (they aim to make the world match them). Motivation requires both elements.
   - `anti_humean`: Beliefs alone can motivate. A belief about what one ought to do — or a belief with normative content — can directly produce motivation to act accordingly, without the mediation of a distinct desire. Practical reason itself can be motivating.
   - `hybrid`: Beliefs can motivate, but only when combined with certain standing desires, dispositions, or concerns. The motivating force comes from the belief-desire combination, but the belief can be a moral belief rather than a merely factual one.
   - `not_specified`: The argument does not address the nature of motivation.

2. **Apply diagnostic questions**:
   - Does the argument assert or presuppose that "reason alone cannot motivate" or that "belief without desire is inert"? If yes, Humean.
   - Does the argument treat desires as necessary components of any motivational state? If yes, Humean.
   - Does the argument allow that a belief about what one ought to do can directly produce motivation? If yes, anti-Humean.
   - Does the argument distinguish between motivating reasons (psychological states that explain action) and normative reasons (facts that justify action)? This distinction is characteristic of Humean views — the Humean holds that motivating reasons always involve desires, while normative reasons may be desire-independent.
   - Does the argument use direction-of-fit language? "Beliefs aim at truth" (mind-to-world) versus "desires aim at satisfaction" (world-to-mind)?

3. **Assess interaction with internalism**: The Humean/internalism combination generates the "moral problem":
   - Humean + Strong Internalism = Moral judgment cannot be belief (because beliefs don't motivate). Therefore, non-cognitivism.
   - Humean + Externalism = Moral judgment can be belief (because it need not motivate). Cognitivism is viable.
   - Anti-Humean + Internalism = Moral judgment can be belief, and belief motivates. Cognitivism + internalism is viable.
   - Note the argument's position in this matrix and what it entails.

4. **Flag the default**: The Humean theory is the default in contemporary metaethics. If the argument is silent, note: "The argument does not address the Humean theory of motivation. The Humean framework is the default in metaethics; the argument's psychological commitments are assessed against it. If the argument is implicitly anti-Humean, this requires explicit defense."

### Step 4: Test Amoralist Handling

The amoralist is the primary counterexample to strong and weak motivational internalism. Test whether the argument's psychological view can accommodate the amoralist or must explain them away.

**Procedural guidance:**

1. **Characterize the amoralist precisely**: The amoralist is an agent who:
   - Sincerely judges that φ is morally required (this is a genuine moral judgment, not an "inverted commas" use of moral language).
   - Fully understands the concepts involved in the judgment.
   - Has no motivation whatsoever to φ — no desire, no inclination, no felt obligation, no guilt at the thought of not φ-ing.
   - May actively desire to do the opposite of what they judge required.
   - Is not suffering from any cognitive deficit, conceptual confusion, or failure of rationality (in the externalist construal) or is suffering from a rationality deficit (in the rational internalist construal).

2. **Test the argument's view against the amoralist**:
   - **Strong internalism**: Must deny the amoralist is conceptually possible. How? Options: (a) the apparent amoralist is not sincere — they are merely mouthing moral words; (b) the apparent amoralist does not fully understand the concepts — genuine moral understanding entails motivation; (c) the apparent amoralist actually is motivated at some level, despite appearances. Assess whether the argument provides such a response and whether it is plausible.
   - **Weak internalism**: Can accommodate the amoralist as a case where the normal connection between judgment and motivation is defeated — by depression, exhaustion, severe character defect, etc. The amoralist is possible but abnormal. Assess: does the argument specify the defeating conditions, and is the list of defeaters principled or ad hoc?
   - **Rational internalism**: Can accommodate the amoralist as an irrational agent — someone who has reasons to φ but fails to be motivated by them due to a failure of rationality. Assess: does this make the amoralist too easy to accommodate? If any failure of motivation can be attributed to irrationality, rational internalism may become empirically unfalsifiable.
   - **Externalism**: Fully accommodates the amoralist. Moral judgment and motivation are distinct; the amoralist is simply someone who makes moral judgments but lacks the additional motivational factors. Assess: does the argument address the "fetishism" charge (Smith) — that externalism makes moral motivation look like a non-rational attachment to doing what one judges right?

3. **Assess plausibility**: Regardless of the argument's explicit handling, evaluate whether the handling is philosophically plausible:
   - If the argument denies the amoralist's possibility, does it provide a convincing account of apparent amoralists?
   - If the argument accommodates the amoralist as a rationality failure, does it explain what rationality failure consists in?
   - If the argument is silent, explain how its view would most naturally handle the amoralist and what burdens this creates.

### Step 5: Test Akrasia Handling

Akrasia — weakness of will, knowing the better but doing the worse — is a pervasive phenomenon that any moral psychology must accommodate. Test whether the argument's view can handle akrasia without making it impossible or trivial.

**Procedural guidance:**

1. **Characterize akrasia precisely**: The akratic agent:
   - Makes a sincere all-things-considered judgment that φ is better than ψ (or that she ought to φ rather than ψ).
   - Freely and intentionally chooses ψ rather than φ.
   - Acts against her better judgment.
   - Is aware, at the time of action, that she is acting against her better judgment (this distinguishes akrasia from cases where the agent changes her mind or forgets her judgment).

2. **Test the argument's view against akrasia**:
   - **Strong internalism + motivation is sufficient for action**: If moral judgment necessarily motivates, and that motivation is sufficient for action, then akrasia is impossible — the agent will always act on her moral judgment. This is empirically inadequate; akrasia is a pervasive phenomenon. If the argument's view precludes akrasia, flag this as a significant empirical problem.
   - **Strong internalism + motivation is one force among others**: If moral judgment necessarily produces a motivation, but that motivation can be overridden by stronger competing motivations (desire, temptation, fear), then akrasia is possible — the agent is motivated to φ, but more strongly motivated to ψ. This is a more plausible internalist picture, but it weakens the claim that moral judgment necessarily motivates — if the motivation can always be overridden, how significant is the necessity?
   - **Rational internalism**: Akrasia is a failure of rationality — the agent has reasons to φ but fails to be motivated by them. The rational internalist can accommodate akrasia easily (too easily?), but must explain what rationality failure consists in and why it is so common.
   - **Externalism**: Fully accommodates akrasia — the agent judges that φ is required but lacks the desire or character to be motivated to φ. Akrasia is simply a case where the contingent motivational factors do not align with the moral judgment.

3. **Assess empirical adequacy**: Does the view make akrasia (a) impossible (empirically inadequate), (b) possible but surprisingly rare (needs explanation), or (c) fully accommodated (adequate but may trivialize the connection between judgment and motivation)?

4. **Flag the sufficiency question**: The key internalist distinction is whether the motivation entailed by moral judgment is *sufficient* for action or merely *contributory*. If sufficient, akrasia is impossible. If contributory, akrasia is possible but internalism is weakened. The analysis must identify which horn the argument takes.

### Step 6: Assess Metaethical Implications

Trace the implications of the argument's moral psychology for the viable metaethical positions. This step uses the "moral problem" framework (Smith) and the broader metaethical landscape to map what the argument can consistently claim about the nature of moral judgment.

**Procedural guidance:**

1. **Apply the "moral problem" trilemma** (if Humean):
   - The inconsistent triad: (A) Moral judgments are beliefs (cognitivism), (B) Moral judgments necessarily motivate (internalism), (C) Beliefs alone cannot motivate (Humean theory of motivation).
   - Which of (A), (B), or (C) does the argument reject?
     - Reject (A) = non-cognitivism (expressivism, prescriptivism, emotivism).
     - Reject (B) = externalism (cognitivism + externalism is Smith's solution).
     - Reject (C) = anti-Humeanism (cognitivism + internalism + anti-Humean theory of motivation).

2. **Map to metaethical positions**:

| Motivational View | Compatible Metaethical Positions | Incompatible Positions | Key Tension |
|---|---|---|---|
| Strong Internalism + Humean | Expressivism, prescriptivism, emotivism | Cognitivist realism, error theory, constructivism | Cannot treat moral judgment as belief |
| Weak Internalism + Humean | Expressivism (with defeater account), hybrid views | Cognitivist realism (tension with internalism) | Must explain defeaters non-ad-hocly |
| Rational Internalism + Humean | Smith-style cognitivism, Korsgaard-style constitutivism | Strong non-cognitivism (understates role of rationality) | Must explain why rationality ensures motivation |
| Externalism + Humean | Cognitivist realism, error theory, constructivism | Strong expressivism (loses key motivation) | Fetishism charge from internalists |
| Any Internalism + Anti-Humean | Cognitivist realism, constitutivism | None ruled out by psychology alone | Must explain how beliefs motivate without desires |
| Externalism + Anti-Humean | Cognitivist realism | None ruled out by psychology alone | Psychological framework is eclectic |

3. **Identify the argument's position**: Based on the classifications from Steps 2 and 3, identify which row(s) of the table the argument occupies. State the compatible and incompatible positions explicitly.

4. **Trace inferential chains**: Do not merely assert that "internalism favors non-cognitivism." Show the explicit inference:
   - Premise 1: Moral judgment necessarily motivates (internalism, Step 2).
   - Premise 2: Beliefs alone cannot motivate (Humean theory, Step 3).
   - Premise 3: If moral judgment were a belief, it could not motivate (from 2).
   - Premise 4: But moral judgment does motivate (from 1).
   - Conclusion: Therefore, moral judgment is not a belief (non-cognitivism).

5. **Flag dialectical burdens**: If the argument's moral psychology entails a metaethical position, does the argument accept that entailment? If not, flag the inconsistency. "The argument's moral psychology (strong internalism + Humeanism) entails non-cognitivism. But the argument explicitly claims to be a cognitivist realist (paragraph 2: 'moral facts are mind-independent truths'). This is an inconsistency: the argument's psychology and its metaphysics cannot both be true."

### Step 7: Compile Report

Assemble the findings from Steps 1-6 into a structured report conforming to `moral-psychology-schema.json`.

**Procedural guidance:**

1. **Executive Summary**: State the classified position and key implications. "This argument presupposes rational internalism about moral motivation: moral judgment entails that a rational agent would be motivated to act accordingly. Combined with an implicit Humean theory of motivation, this yields a Smith-style resolution of the moral problem: cognitivism is preserved, internalism is weakened to rational internalism, and Humeanism is retained. The view handles the amoralist as irrational and akrasia as a rationality failure."

2. **Internalism/Externalism Classification**: Present the classification with evidence from the motivational claim inventory. State the confidence level. If there are tensions or ambiguities, discuss them.

3. **Humean/Anti-Humean Diagnosis**: Present the classification with evidence. If the argument is silent, note this and assess it against the Humean default.

4. **Amoralist Analysis**: Present the full assessment — the argument's handling (or non-handling) of the amoralist, the plausibility of that handling, and the burdens it creates.

5. **Akrasia Analysis**: Present the full assessment — whether akrasia is possible under the view, whether the sufficiency/contributory distinction resolves the issue, and whether the view is empirically adequate.

6. **Motivational Architecture**: Present a textual diagram showing the causal/rational structure: Moral Judgment --> [Motivation/Belief/Desire/Intention] --> Action. Annotate the diagram with the argument's specific commitments.

7. **Metaethical Implications**: Present the systematic mapping of compatible and incompatible positions. State the explicit inferential chain from psychology to metaethics. Flag any tensions between the argument's psychology and its explicit metaethical commitments.

## Quality Criteria

1. **Internalism precision**: Specify the exact strength level of internalism (strong/weak/rational/externalist) with explicit textual evidence. Never use "internalist" without qualification. The amoralist and akrasia tests depend on the precise formulation — strong and rational internalism have fundamentally different implications.

2. **Amoralist test rigor**: Explicitly evaluate whether the argument's view can accommodate the amoralist. If the argument is silent, trace the implication of its commitments rather than ignoring the test. A view that denies the amoralist's conceptual possibility bears a heavy burden; the analysis must note whether this burden is discharged.

3. **Humean framework transparency**: Explicitly state whether the argument's motivational picture is Humean, anti-Humean, or hybrid. If the argument does not address the issue, note that the Humean theory is the default but that the argument's commitments may implicitly depart from it. Do not assume Humeanism without evidence.

4. **Implication chain explicitness**: For each metaethical implication, show the full inferential chain. Do not assert "internalism favors non-cognitivism" — show the premises about belief, desire, motivation, and judgment that generate the implication. The chain should be transparent enough that a reader can identify which premise they would need to reject to avoid the implication.

5. **Akrasia consistency check**: Explicitly test whether the view makes akrasia impossible, implausibly rare, or fully accommodated. A view that precludes akrasia entirely is empirically inadequate. A view that makes akrasia trivially easy may weaken the claimed connection between judgment and motivation to the point of insignificance.

6. **Smith's moral problem awareness**: If the argument's moral psychology fits the Smithian trilemma structure (cognitivism + internalism + Humeanism), explicitly analyze it in those terms. If the argument does not acknowledge the trilemma, note this as a dialectical gap.

## Relations to Other Skills

**Depends on (upstream):**
- `method.argument.argument-reconstruct`: Takes the reconstructed standard form as input. The motivational claim extraction in Step 1 depends on the reconstruction accurately capturing the argument's psychological premises.
- `method.metaethics.normativity` (optional but recommended): The reasons internalism/externalism diagnosis from the normativity analysis parallels and constrains the motivational internalism/externalism analysis. An argument that is reasons-internalist (Williams-style) creates pressure toward motivational internalism, and vice versa. The normativity report provides the context for assessing whether the argument's psychology and normativity are consistent.

**Referenced knowledge resources:**
- `Framework/Workflow/References/glossary-metaethics.md`: Definitions of core moral-psychological concepts (motivational internalism, motivational externalism, Humean theory of motivation, anti-Humeanism, amoralist, akrasia, practicality requirement, direction of fit, fetishism argument).
- `Framework/Workflow/References/normativity-taxonomy.md`: The taxonomy of normativity source theories — used in Step 6 to cross-reference the motivational analysis with the normative source theory. A Humean about normativity and a Humean about motivation are a natural pair; a constitutivist about normativity and a Humean about motivation may involve tension.

**Feeds into (downstream):**
- `method.metaethics.moral-realism`: Motivational internalism/externalism commitments constrain the viable realism positions. Strong internalism + Humeanism rules out cognitivist realism; externalism is a prerequisite for standard realist views. The moral psychology report should be passed to the realism skill as a constraint document.
- `method.metaethics.moral-semantics`: The semantic analysis is logically independent of moral psychology, but the two must be checked for consistency. Expressivist semantics pairs naturally with motivational internalism (attitudes motivate); cognitivist semantics requires either externalism or anti-Humeanism. Inconsistency between the semantic and psychological analyses should be flagged.

**Independent of (cross-domain):**
- `method.metaethics.moral-disagreement`: The analysis of moral disagreement is logically independent of moral psychology — the nature of moral disagreement does not directly constrain or depend on the judgment-motivation relation. However, radical versions of internalism that make moral judgment essentially expressive may have implications for how moral disagreement is understood.

## Boundary Conditions

**1. No motivational claims**: If the argument contains no claims about the relation between moral judgment and motivation, output: "No moral-psychological premises detected. The argument does not address the motivation relation." Optionally, offer implicit analysis: "Although the argument is silent on moral psychology, its metaethical stance implies motivational commitments. For example, if the argument is expressivist, it likely presupposes internalism; if cognitivist realist, it likely presupposes externalism. Would you like an analysis of these implicit commitments?"

**2. Pure meta-level semantics without psychology**: If the argument discusses the semantics of moral language without addressing motivation, note the gap: "The argument develops moral semantics without addressing moral psychology. This is a significant gap — semantic theories have motivational implications. Expressivist semantics is motivated partly by the need to explain the practicality of moral judgment (internalism); cognitivist semantics needs an account of how moral beliefs motivate (externalism or anti-Humeanism). The argument's failure to address these implications leaves its overall metaethical position incomplete."

**3. Arguments that presuppose empirical psychology**: If the argument appeals to empirical psychological claims (e.g., "studies show that moral judgment reliably produces motivation," "sociopaths demonstrate that motivational externalism is true"), the analysis must note that these claims require empirical support and assess whether the philosophical argument would survive falsification of the empirical claim. "The argument's internalism rests on the empirical premise that moral judgment reliably produces motivation (paragraph 4). If this empirical claim is false, the argument's case for internalism collapses. The philosophical argument is hostage to empirical fortune."

**4. The "Moral Problem" framework**: If the argument explicitly addresses Smith's "moral problem" (the trilemma of cognitivism, internalism, and Humeanism), use Smith's framework as the organizing structure for the entire analysis. If the argument fits the trilemma structure but does not acknowledge it, use the trilemma in the analysis but note: "The argument does not acknowledge Smith's 'moral problem,' but its commitments generate the classic trilemma."

**5. Non-Western or historical moral psychologies**: If the argument operates within a non-Humean psychological framework that does not map neatly onto the belief-desire model (e.g., Aristotelian virtue ethics where perception and desire are integrated, Confucian role ethics, Buddhist moral psychology), classify using the available categories but annotate the cultural or historical distance: "This argument operates within an Aristotelian moral psychology that does not distinguish belief and desire as sharply as the Humean framework. The classification as 'anti-Humean' is approximate and reflects the framework's rejection of the belief-desire dichotomy rather than an explicit engagement with the Humean tradition." Offer to supplement the analysis with framework-specific categories.

**6. Fictionalist and error-theoretic moral psychologies**: If the argument is a moral fictionalist or error theorist, its moral psychology is distinctive: the error theorist holds that moral judgments are beliefs (cognitivism) but all such beliefs are false; the fictionalist holds that moral discourse involves pretense or make-believe rather than belief. The analysis must adapt its categories accordingly — the standard internalism/externalism debate presupposes that moral judgments are genuine (truth-apt) mental states, which error theorists and fictionalists may reject or reinterpret.

## ARS Interface

This skill is part of the Academic Research Skills (ARS) metaethics pipeline. It conforms to the ARS skill specification:

- **Invocation pattern**: This skill is invoked when the system detects a need for moral psychology analysis in a metaethics workflow, typically after normativity analysis (`method.metaethics.normativity`) and before moral realism analysis (`method.metaethics.moral-realism`). It can be invoked standalone or as part of a pipeline run.

- **Schema compliance**: The output conforms to `moral-psychology-schema.json` (located in `shared/`), which defines the JSON structure for moral psychology analysis reports. All required fields are populated; optional fields are populated when information is available. The schema enforces controlled vocabularies for internalism/externalism classification, Humean/anti-Humean classification, amoralist status, and akrasia status.

- **Cache behavior**: Moral psychology analysis reports are cached per argument (keyed by argument-reconstruction hash). If the same argument is analyzed again, the cached report is returned unless invalidated via `ars-cache-invalidate`.

- **Error handling**: If required input is missing, the skill returns a structured error object. If no psychological claims are detected (boundary condition 1), the skill returns a null report with an offer to analyze implicit commitments.

- **Pipeline integration**: Output tagged with `output-type: moral-psychology-analysis`. The report includes `pipeline_metadata` with skill version, generation timestamp, input document hash, and upstream dependency hashes. Downstream skills (primarily `method.metaethics.moral-realism`) consume this output by querying for the `output-type` tag.

- **ARS tool integration**:
  - The Moral Psychology Analysis Report can be passed to ARS `academic-paper` as a "moral-psychological framework statement" for the methodology section.
  - The internalism/externalism classification and amoralist analysis can inform ARS `deep-research` for targeted searches on specific challenges (e.g., "empirical evidence for the amoralist," "responses to Smith's fetishism argument").
  - The metaethical implications assessment can seed ARS `academic-paper-reviewer` for anticipating objections about the coherence of the author's motivational commitments with their semantic and metaphysical views.
  - Citation formats throughout the report are compatible with ARS `citation-check` (Author-Year format with page references where available).

- **Versioning**: This skill follows semantic versioning. Breaking changes to the output schema or classification taxonomy require a major version bump. Additions to the classification taxonomy (e.g., new internalism variants) require a minor version bump. Clarifications, improved procedural guidance, and bug fixes require a patch version bump.
