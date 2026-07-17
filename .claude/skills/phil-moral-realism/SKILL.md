---
name: phil-moral-realism
description: "Moral Realism Argument Analysis — analyze arguments for/against moral realism, anti-realism, error theory, and non-cognitivism; map positions on the realism spectrum"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Moral Realism Argument Analysis

## Overview

The moral realism/anti-realism debate is the organizing axis of metaethics. This skill analyzes arguments about the existence and nature of moral facts — whether moral claims are truth-apt, whether any are true, and what makes them true if they are. It classifies positions along the realism spectrum, from robust non-naturalism through various realist intermediate positions, across the fault line to anti-realist positions (error theory, expressivism, fictionalism, relativism), mapping both the positive arguments offered for a position and the negative arguments deployed against rival views.

A central task of this skill is distinguishing the *argument* being advanced from the *position* being defended. Many texts argue for or against moral realism without self-identifying in these terms, and many arguments operate dialectically (e.g., a "companions in guilt" argument that defends realism by challenging the queerness objection). The skill therefore performs a dual function: position classification and argument structure analysis.

The realism spectrum captures the diversity of metaethical positions along four core dimensions: (1) cognitivism — whether moral judgments are truth-apt; (2) truth-status — whether any moral judgments are in fact true; (3) mind-independence — whether moral facts exist independently of human attitudes or conventions; and (4) ontological commitment — what kind of entities moral facts/properties are if they exist. Different combinations of answers to these four questions yield the eleven canonical positions on the spectrum. The skill maps every argument onto this matrix, identifying both its explicit and implicit commitments.

Because metaethics arguments often operate at multiple levels — first-order (arguing directly for a position), second-order (arguing about what a position requires), and dialectical (arguing that rival positions face insuperable difficulties) — the skill tracks the argument's dialectical role as well as its content. This enables downstream consumers (particularly `phil-moral-disagreement`, `phil-moral-epistemology`, and `phil-moral-supervenience`) to situate the argument within the broader metaethical landscape.

## Input

**Required**:
- An argument-reconstruction report (output of `phil-argument-reconstruct`), providing the reconstructed standard form of the metaethical argument, including explicit premises, implicit premises, logical form, and structural assessment.

**Optional**:
- A premise-audit report (output of `phil-premise-detect`), identifying implicit metaethical presuppositions — particularly useful for detecting implicit cognitivist or realist commitments in arguments that operate at the normative level.
- The original philosophical text, for context-sensitive interpretation of metaethical stance markers when the reconstruction alone is ambiguous.

## Output

A **Moral Realism Position Analysis Report** conforming to the `moral-realism-schema.json` specification, structured as follows:

1. **Position Classification**: Precise classification on the realism spectrum (see taxonomy in Step 2), with textual evidence for the classification. Includes the exact position name, a brief definition of that position, and the specific textual markers that support the classification.

2. **Key Commitments**: The argument's stances on the four core metaethical dimensions, each with an explicit/implicit designation:
   - **Cognitivism**: Does the argument treat moral judgments as truth-apt? (explicit or implicit commitment.)
   - **Truth-status**: Does the argument claim that some moral judgments are true, or that all are false? (explicit or implicit commitment.)
   - **Mind-independence**: Does the argument claim moral facts are mind-independent, mind-dependent, or is it silent on the issue?
   - **Existence of moral facts**: What ontological status does the argument assign to moral facts/properties — existent (fundamental/derivative/constructed), non-existent (error), fictional, or projected?

3. **Argument Structure Analysis**: How the reconstructed argument supports or challenges each of the four commitments. Distinguishes between:
   - **Positive arguments**: Arguments offered *for* the position (with reconstructed premise-conclusion form for each).
   - **Negative arguments**: Arguments deployed *against* rival positions (with the specific target position and the premise under attack identified).
   - **Dialectical role**: Whether the argument is first-order (directly for/against realism), second-order (about what realism requires, about burden of proof, about explanatory adequacy), or purely defensive (responding to an objection).

4. **Dialectical Vulnerabilities**: A systematic assessment of which canonical metaethical challenges apply to the argument's position:
   - Queerness challenge (Mackie, 1977)
   - Disagreement challenge (Mackie, 1977; Doris & Plakias, 2008)
   - Supervenience challenge (Blackburn, 1971)
   - Frege-Geach problem (Geach, 1965; Searle, 1962)
   - Evolutionary debunking challenge (Street, 2006; Joyce, 2006)
   - Open question argument (Moore, 1903)
   - Moral Twin Earth objection (Horgan & Timmons, 1991)
   - For each challenge: vulnerability rating (high/medium/low/not applicable) with justification, and whether the argument has resources to respond.

5. **Recommended Counter-positions**: The most dialectically effective rival positions (2-4), with a brief rationale explaining why each counter-position threatens the argument's premises or conclusion.

6. **Spectrum Position Map**: A visual placement of the argument's position on the realism spectrum, showing adjacent positions and the fault lines that separate them.

## Methodological Foundations

1. **Moore's Open Question Argument** (1903, *Principia Ethica*): For any natural property N, the question "Is X that is N good?" remains open — hence goodness is not identical to any natural property. This argument is foundational for non-naturalist realism and constitutes a persistent challenge to any form of analytic or reductive naturalism. Its core philosophical move — the semantic test of identity claims — generalizes to other domains.

2. **Mackie's Error Theory and the Argument from Queerness** (1977, *Ethics: Inventing Right and Wrong*): Mackie advances two arguments against moral realism. The *argument from relativity* holds that the best explanation of widespread, persistent moral disagreement is that moral judgments reflect cultural traditions rather than tracking objective facts. The *argument from queerness* holds that moral facts, if they existed, would be entities of a "very strange sort" — intrinsically normative and action-guiding, metaphysically unlike anything else in the natural world, and requiring a "special faculty of moral intuition" for epistemic access. Since such entities are ontologically extravagant, we should conclude that all positive moral claims are false (error theory).

3. **The Realism Spectrum** (Sayre-McCord, 1988, "Moral Theory and Explanatory Impotence"; Shafer-Landau, 2003, *Moral Realism: A Defence*): Moral realism is not a single position but a spectrum organized by the strength of ontological commitment. The canonical ordering: robust non-naturalism (Enoch, Moore) > quietist realism (Scanlon, Dworkin) > Cornell realism (Boyd, Sturgeon) > analytic functionalism (Jackson, Smith) > reductive naturalism (Railton, Schroeder) > response-dependence (McDowell, Wiggins) > constructivism (Korsgaard, Street) > error theory (Mackie) > expressivism (Blackburn, Gibbard) > fictionalism (Joyce) > relativism (Harman, Wong). Positions adjacent on the spectrum share commitments; non-adjacent positions differ on at least two of the four core dimensions.

4. **The Companions in Guilt Strategy** (Cuneo, 2007, *The Normative Web*): If moral facts are rejected for having a feature F (e.g., being irreducibly normative), and epistemic facts (or mathematical facts, or prudential facts) also have feature F, then the rejection of moral facts entails the rejection of those other facts — an unacceptable consequence because epistemic facts (for example) cannot be coherently rejected. This strategy neutralizes queerness-based objections by showing they prove too much.

5. **Enoch's Robust Realism** (2011, *Taking Morality Seriously*): Defends non-naturalist moral realism against the queerness challenge by arguing that irreducibly normative truths are *indispensable* to practical deliberation — we cannot make sense of deliberative practice without them — and that entities indispensable to a non-optional practice are ontologically legitimate even if they cannot be reduced to natural facts.

6. **Blackburn's Quasi-Realism** (1993, *Essays in Quasi-Realism*): An expressivist program that mimics realist-sounding discourse ("moral truths," "moral facts," "moral knowledge") while maintaining that the underlying function of moral language is expressive rather than descriptive. Quasi-realism is the thesis that expressivism can *earn the right* to use realist language through a systematic explanation of why expressivist commitments license realist-sounding talk.

7. **Joyce's Evolutionary Debunking and Fictionalism** (2001, *The Myth of Morality*; 2006, *The Evolution of Morality*): Evolutionary forces shaped our moral judgments to track fitness, not truth. Since there is no reason to think fitness-tracking coincides with truth-tracking in the moral domain, moral judgments are unjustified (debunking). However, moral discourse may still be useful as a fiction — we can continue to make moral judgments while withholding belief in their truth (fictionalism).

## Steps

### Step 1: Identify Metaethical Stance Markers

Scan the text (or the argument-reconstruction report) for language that reveals metaethical commitments. Metaethical stance markers are the surface-level indicators of deeper theoretical commitments:

**Cognitivist markers** (treat moral language as truth-apt):
- "moral belief," "moral knowledge," "moral truth," "moral proposition"
- "is true/false," "correct/incorrect," "accurate/inaccurate"
- "discover," "apprehend," "perceive" (applied to moral facts)
- "moral epistemology," "moral justification," "moral evidence"

**Non-cognitivist markers** (treat moral language as non-truth-apt or expressively primary):
- "express approval/disapproval," "endorse," "prescribe," "commend"
- "project," "emotive meaning," "expressive function"
- "plan," "accept a norm," "commit to"
- Emphasis on the action-guiding or motivational role of moral language

**Realist markers** (commit to moral facts/properties):
- "moral facts," "moral properties," "moral reality"
- "mind-independent," "objective value," "stance-independent"
- "discover" (applied to moral truths), "recognition" of moral requirements
- "truthmaker," "correspondence" (for moral claims)

**Anti-realist markers** (deny or deflate moral facts):
- "project," "invent," "construct," "constitute"
- "error," "fiction," "make-believe," "relative to"
- "no moral facts," "moral properties do not exist"
- "framework-dependent," "convention," "agreement"

**Error-theoretic markers** (cognitivist but all positive claims false):
- "no moral facts," "systematically false," "erroneous"
- "error," "mistaken," "false presupposition"
- "Although we speak as if... there really are no..."

**Constructivist markers** (moral facts constituted by practical reason):
- "constituted by," "constructed from," "practical standpoint"
- "legislated by," "willed," "endorsed from the practical point of view"
- "procedural," "constitutive standards of agency"

Document each marker with its source location (premise number, paragraph, or line reference). Aggregate the markers to form an initial classification hypothesis.

### Step 2: Classify Position on the Realism Spectrum

Using the taxonomy in `moral-realism-taxonomy.md`, classify the argument's metaethical position with maximum precision. The realism spectrum, organized by the four core dimensions:

| Position | Cognitivism | Truth-Evaluable | Some True Claims | Mind-Independent Facts | Core Proponent |
|----------|-------------|-----------------|------------------|------------------------|----------------|
| Robust Non-Naturalism | Yes | Yes | Yes | Yes (strong) | Enoch, Moore |
| Quietist Realism | Yes | Yes | Yes | Yes (minimal) | Scanlon, Dworkin |
| Cornell Realism | Yes | Yes | Yes | Yes (synthetic a posteriori) | Boyd, Sturgeon |
| Analytic Functionalism | Yes | Yes | Yes | Yes (network analysis) | Jackson, Smith |
| Reductive Naturalism | Yes | Yes | Yes | Yes (reductive identity) | Railton, Schroeder |
| Response-Dependence | Yes | Yes | Yes | Partial (dispositional) | McDowell, Wiggins |
| Constructivism | Yes | Yes | Yes | No (constituted by reason) | Korsgaard, Street |
| Error Theory | Yes | Yes | No (all false) | — (they do not exist) | Mackie, Joyce |
| Expressivism (Standard) | No | No | No | No | Ayer, early Stevenson |
| Expressivism (Quasi-Realist) | No | Yes (minimal) | Varies (quasi-truth) | No (projective) | Blackburn, Gibbard |
| Fictionalism | Yes | Yes | No (useful fiction) | No (fictional) | Joyce, Kalderon |
| Relativism | Yes | Yes | Yes (relative) | No (framework-dependent) | Harman, Wong |

**Precision rule**: Classify to the most specific position on the spectrum, never merely "realist" or "anti-realist." If the argument is ambiguous between two adjacent positions (e.g., quietist realism vs. analytic functionalism), note the ambiguity and articulate the *diagnostic question* that would resolve it (e.g., "Does the argument claim that moral concepts are analyzable in terms of non-moral concepts? If yes, analytic functionalism; if no, quietist realism.").

If the argument is ambiguous between two *non-adjacent* positions, present both as live possibilities with the distinguishing evidence and note that the text is underspecified.

### Step 3: Reconstruct the Core Argument

Extract the argument's positive case (what it affirms or argues for) and negative case (what it rejects or argues against):

**Positive argument extraction**:
- What is the principal argument offered *for* the classified position?
- Reconstruct it in standard premise-conclusion form, using the argument-reconstruction report as source material.
- Identify whether the positive argument is: (a) an existence argument (arguing *that* moral facts exist), (b) a nature argument (arguing *what kind* of thing moral facts are), or (c) an indispensability argument (arguing that moral facts are *required* for some practice).

**Negative argument extraction**:
- What rival positions does the argument attack?
- For each target, identify which specific premise or commitment of the rival is under attack.
- Classify the negative argument type: queerness argument, disagreement argument, open question argument, supervenience challenge, evolutionary debunking, companions in guilt response, or other.

**Dialectical role classification**:
- **First-order**: The argument directly argues for or against the existence/nature of moral facts.
- **Second-order**: The argument argues about what moral realism *requires* (e.g., "realism requires explaining supervenience"), about *burden of proof* (e.g., "the anti-realist bears the burden"), or about *explanatory adequacy* (e.g., "realism better explains moral practice").
- **Defensive**: The argument responds to an objection without advancing a positive case.

### Step 4: Map the Semantic Commitments

Determine what the argument presupposes or asserts about moral language. Each sub-analysis identifies a commitment that has downstream implications for the realism spectrum classification:

**Truth-aptness commitment**:
- Does the argument treat moral sentences as capable of being true or false?
- What theory of truth does the argument presuppose — correspondence (robust), deflationary/minimalist (disquotational), epistemic, or coherence?
- If deflationary truth is presupposed, does this collapse the cognitivism/non-cognitivism distinction? (Under deflationism, any grammatical declarative is "truth-apt.")

**Belief-expression commitment**:
- Does the argument treat moral judgments as expressing beliefs (cognitive states representable as propositional attitudes with mind-to-world direction of fit) or non-cognitive attitudes (desire-like states with world-to-mind direction of fit)?
- If the argument is ambiguous, are there markers of direction of fit? ("Discovering" moral facts suggests world-to-mind; "projecting" or "endorsing" suggests mind-to-world.)

**Embedding behavior commitment**:
- Does the argument embed moral claims in unasserted contexts (conditionals, negations, interrogatives, attitude reports)?
- If the argument is non-cognitivist, does it implicitly face the Frege-Geach problem? Does the text acknowledge or address it?
- If the argument is cognitivist, does it exploit the compositional semantics of moral language as evidence for cognitivism?

**Thick/thin concept distribution**:
- Does the argument deploy thick moral concepts (courageous, cruel, generous, treacherous), thin moral concepts (good, right, ought, wrong), or both?
- If thick concepts dominate, does the argument exploit their fact-value entanglement — the way thick concepts seem to combine descriptive adequacy conditions with evaluative force?

### Step 5: Map the Metaphysical Commitments

Determine what the argument presupposes or asserts about moral reality. These commitments jointly determine the position on the realism spectrum:

**Existence claim**:
- Does the argument commit to the existence of moral facts, properties, or truths? At what ontological level?
  - *Fundamental*: Moral facts are among the basic constituents of reality (robust non-naturalism).
  - *Derivative*: Moral facts exist but are reducible to or grounded in natural facts (naturalist realism).
  - *Constructed*: Moral facts exist but are constituted by the operations of practical reason (constructivism).
  - *Projected*: Moral "facts" are projections of attitudes; they do not literally exist (expressivism).
  - *Non-existent*: Moral facts do not exist, but moral discourse may still be useful (error theory, fictionalism).

**Mind-independence commitment**:
- To what extent does the argument claim moral facts are independent of human attitudes, conventions, or practical standpoints?
- Distinguish between: (a) *strong mind-independence* — moral facts would exist even if no agents existed (robust non-naturalism); (b) *response-dependence* — moral facts are constituted by the responses of suitably situated agents under ideal conditions; (c) *stance-dependence* — moral facts are constituted by the practical standpoint of agency (constructivism); (d) *mind-dependence* — moral facts depend on actual attitudes or conventions (relativism, expressivism).

**Supervenience stance**:
- Does the argument acknowledge that moral properties supervene on natural properties? (If two situations are identical in all natural respects, they cannot differ in moral respects.)
- If the argument acknowledges supervenience, does it treat it as a *brute fact* (requiring no explanation) or as something that *requires explanation* (posing an explanatory challenge)?
- Naturalist realists can explain supervenience easily (moral properties *are* natural properties, or are grounded in them). Non-naturalist realists face the explanatory challenge.

**Naturalism stance**:
- Does the argument embrace or reject the reducibility of moral properties to natural properties?
- If reductionist, what is the *reduction base* — the set of natural properties to which moral properties are reduced? (E.g., Railton's reduction to what would be rationally endorsed from an impartial standpoint; Jackson's network analysis of moral terms via folk platitudes.)
- If non-reductionist, how does the argument account for the apparent connection between moral and natural properties without reduction?

### Step 6: Identify Dialectical Vulnerabilities

For each canonical metaethical challenge, determine whether and how it applies to the argument's position. Each challenge targets specific commitments; not all challenges apply to all positions:

**Queerness challenge** (Mackie, 1977):
- Targets: Positions that posit irreducibly normative facts (robust non-naturalism, quietist realism, non-naturalist versions of other positions).
- Test: Does the argument's position require entities that are (a) metaphysically queer — intrinsically action-guiding, unlike any natural entities — and (b) epistemologically queer — requiring a "special faculty" for epistemic access?
- Vulnerability rating: High if the position commits to non-natural moral facts without addressing the queerness challenge. Low if the position is naturalist, or if it offers a companions-in-guilt response (normativity is not uniquely moral) or an indispensability response (Enoch).

**Disagreement challenge** (Mackie, 1977; Doris & Plakias, 2008):
- Targets: Positions that claim moral facts are objective and mind-independent.
- Test: Is widespread, persistent moral disagreement better explained by the *non-existence* of mind-independent moral facts (anti-realism) or by the *difficulty* of accessing them (realism)?
- Vulnerability rating: High for non-naturalist realism (no mechanism to explain why access to non-natural facts would produce disagreement). Lower for naturalist realism (disagreement can be explained by differing empirical beliefs or background theories). Not applicable to anti-realist positions (disagreement is expected).

**Supervenience challenge** (Blackburn, 1971):
- Targets: Non-naturalist and non-reductivist realist positions.
- Test: If moral properties supervene on natural properties, what explains this necessary connection? Naturalists can explain it via identity or grounding; non-naturalists must treat it as a brute necessity, which is mysterious.
- Vulnerability rating: High for non-naturalist realism without an account of supervenience. Low for naturalist realism and anti-realism.

**Frege-Geach problem** (Geach, 1965; Searle, 1962):
- Targets: Non-cognitivist positions (expressivism, prescriptivism, emotivism).
- Test: Can the position explain how moral sentences function in unasserted contexts — conditionals, negations, interrogatives, attitude reports — where they seem to behave like ordinary propositions?
- Vulnerability rating: High for simple emotivism and early prescriptivism. Lower for sophisticated expressivism (Blackburn, Gibbard, Schroeder) that provides a compositional semantics. Not applicable to cognitivist positions.

**Evolutionary debunking challenge** (Street, 2006; Joyce, 2006):
- Targets: Realist positions (especially non-naturalist).
- Test: Evolutionary forces shaped our moral judgments to track fitness, not truth. If there is no reason to think fitness-tracking coincides with truth-tracking in the moral domain, then moral judgments are unjustified *unless* the realist can provide a "tracking account" — an explanation of how evolutionary pressures would lead us to track moral truth.
- Vulnerability rating: High for non-naturalist realism (the tracking account is hardest to provide). Moderate for naturalist realism (moral truth may be partially constituted by what conduces to flourishing, which evolution may track). Low for constructivism and expressivism (evolution shapes the *content* of moral judgment without raising a truth-tracking problem) and error theory (evolution explains why we have *false* moral beliefs).

**Open question argument** (Moore, 1903):
- Targets: Analytic or reductive naturalist positions.
- Test: For the proposed reduction of moral property M to natural property N, is the question "X is N, but is X M?" a *closed* question (answerable by conceptual analysis alone) or an *open* question (remaining meaningful and debatable)?
- Vulnerability rating: High for analytic naturalism (if the reduction is supposed to be conceptual). Lower for synthetic naturalism (Cornell realism — the reduction is a posteriori, not conceptual). Not applicable to non-naturalism and non-cognitivism.

**Moral Twin Earth** (Horgan & Timmons, 1991):
- Targets: Synthetic naturalist positions (Cornell realism).
- Test: Imagine a Twin Earth community that uses "good" to refer to a different natural property than we do (e.g., what maximizes utility vs. what satisfies reflective desires). If our "good" and their "good" pick out different natural properties, are we *disagreeing* (sharing a concept but disagreeing about its extension) or merely *talking past each other* (using the same word for different concepts)?
- Vulnerability rating: High for Cornell realism (if we are disagreeing, the synthetic identity claim fails; if we are talking past each other, the semantic externalist picture is preserved but at the cost of making cross-community moral disagreement impossible). Moderate for analytic functionalism (the functional role constrains extension more tightly).

For each applicable challenge, provide a vulnerability rating (high/medium/low) with a justification grounded in the argument's specific commitments. Also assess whether the argument has explicit *resources* for responding — does it address the challenge directly, or could it be extended to do so?

### Step 7: Compile the Report

Produce the complete Moral Realism Position Analysis Report in the Output format described above. Synthesize the findings from Steps 1-6 into a coherent report.

**Report assembly guidelines**:
- Lead with the position classification and the textual evidence supporting it (Steps 1-2).
- Present the four key commitments (Steps 4-5), each annotated as explicit or implicit.
- Present the argument structure analysis (Step 3), distinguishing positive arguments, negative arguments, and dialectical role.
- Present the dialectical vulnerability assessment (Step 6) as a table with challenge name, vulnerability rating, justification, and whether the argument has response resources.
- Conclude with recommended counter-positions, selected for maximum dialectical pressure on the argument's weakest commitments.
- Add a spectrum position map showing the classified position relative to adjacent positions, with the fault lines annotated.

**Evidence requirement**: Every commitment attribution must be traceable to a specific premise in the reconstruction report or a specific passage in the source text. Use parenthetical citations throughout.

## Quality Criteria

1. **Spectrum Precision**: Classify to the exact position on the realism spectrum (e.g., "analytic functionalism" not "naturalism"; "quasi-realist expressivism" not "non-cognitivism"). If ambiguous, articulate the diagnostic question that resolves the ambiguity rather than generalizing to a broader category.

2. **Commitment Transparency**: For each of the four core dimensions, explicitly state: (a) what the argument commits to, (b) whether the commitment is explicit (stated in a premise) or implicit (required for the argument to work but not stated), and (c) the specific textual evidence for the commitment.

3. **Argument-vs-Position Distinction**: The analysis must keep two questions distinct: "What metaethical position does the argument support?" and "Is the argument structurally sound?" A valid argument for a minority position and a fallacious argument for the consensus position should both receive accurate classifications with clear structural assessments.

4. **Dialectical Fairness**: Present rival positions in their strongest form, per the principle of charity. Do not dismiss error theory because its conclusion is "counterintuitive" or non-naturalism because its entities are "spooky" — analyze the specific argument's resources for responding to each challenge on its own terms.

5. **Textual Grounding**: Every commitment attribution must be traceable to a specific premise, claim, or marker in the reconstructed argument or source text. Avoid attributing commitments to "the author" that are merely typical of the position the author defends — the author may hold an idiosyncratic version.

6. **Vulnerability Assessment Calibration**: Vulnerability ratings must be calibrated to the specific argument, not to the position in general. A robust realist argument that anticipates and addresses the queerness challenge should receive a lower vulnerability rating than a robust realist argument that ignores it, even though both are classified as the same position.

7. **Cross-Commitment Consistency**: Check whether the argument's semantic, metaphysical, and psychological commitments are mutually consistent. Flag any inconsistencies — e.g., cognitivist semantics combined with strong motivational internalism and Humean psychology generates Smith's "moral problem."

## Relations to Other Skills

**Depends on (upstream)**:
- `phil-argument-reconstruct`: Takes the reconstructed standard form as input for position classification, commitment mapping, and argument structure analysis. Without a reconstruction, stance markers cannot be reliably mapped to inferential roles.
- `phil-premise-detect`: Uses the premise audit to identify implicit metaethical presuppositions that the explicit argument depends on. Many metaethical arguments have significant implicit commitments (e.g., an argument at the normative level may implicitly presuppose cognitivism).

**References (knowledge dependencies)**:
- `Framework/Workflow/References/moral-realism-taxonomy.md`: The canonical realism spectrum taxonomy — detailed definitions of each position and the diagnostic questions that distinguish adjacent positions. This is the primary reference for Step 2 classification.
- `Framework/Workflow/References/glossary-metaethics.md`: Definitions of all core metaethical terms used throughout the analysis.
- `Framework/Workflow/References/metaethical-distinctions.md`: The realism/anti-realism, cognitivism/non-cognitivism, naturalism/non-naturalism, reductionism/non-reductionism distinctions.
- `Framework/Workflow/References/argument-forms/open-question-argument.md`: Canonical structure of Moore's open question argument.
- `Framework/Workflow/References/argument-forms/queerness-argument.md`: Canonical structure of Mackie's argument from queerness.
- `Framework/Workflow/References/argument-forms/companions-in-guilt.md`: Canonical structure of the companions in guilt strategy.
- `Framework/Workflow/References/argument-forms/disagreement-argument.md`: Canonical structure of the argument from moral disagreement.

**Dependents (downstream)**:
- `phil-moral-disagreement` (P2): Uses the realism position classification and vulnerability assessment to evaluate how disagreement arguments bear on the argument — whether disagreement is predicted, problematic, or irrelevant given the position.
- `phil-moral-epistemology` (P2): Uses the realism stance and the supervenience and evolutionary debunking vulnerability assessments to evaluate the possibility of moral knowledge on the argument's view.
- `phil-moral-supervenience` (P2): Uses the realism stance and supervenience stance to determine the explanatory burden imposed by moral supervenience and whether the argument discharges it.

**Feeds from (cross-domain, upstream Skills that inform this analysis)**:
- `phil-moral-semantics`: Semantic commitments identified by moral semantics analysis — especially cognitivism/non-cognitivism and truth-theory — directly inform the realism spectrum classification. A non-cognitivist semantics rules out all cognitivist realist positions.
- `phil-moral-psychology`: Motivational internalism/externalism commitments constrain viable realism stances. Strong internalism + Humeanism rules out cognitivist realism; externalism is a prerequisite for standard realist views.

**Independent of (cross-domain)**:
- `phil-normativity`: The source of normativity is logically independent of the existence of moral facts. A realist about moral facts could be a constitutivist about normative reasons, and vice versa. However, the two analyses should be checked for mutual consistency.

## Boundary Conditions

1. **No metaethical content**: If the text contains no metaethical stance markers and no arguments about the existence or nature of moral facts, output: "No metaethical arguments detected. The text operates at the first-order normative level without engaging metaethical questions about the status of moral claims."

2. **Pure normative ethics (first-order)**: If the text makes substantive normative claims (e.g., "abortion is wrong," "we ought to maximize utility") without arguing about the *status* of those claims, output: "The text operates at the level of normative ethics without engaging metaethical questions. To elevate to metaethical analysis, consider: what does the author presuppose about the status of these normative claims? Are they treated as objective facts, expressions of attitude, or constructions of practical reason? These implicit commitments can be analyzed but were not argued for in the text."

3. **Historical texts with anachronistic terminology**: If the text predates the contemporary metaethics vocabulary (pre-1903, before Moore's *Principia Ethica*), classify using modern categories but explicitly annotate that the author did not self-identify using these terms. Provide the closest contemporary analogue and note the historical distance. Do not attribute distinctions (e.g., cognitivism/non-cognitivism) to authors writing before those distinctions were drawn.

4. **Excessively ambiguous position**: If the text is genuinely ambiguous between two non-adjacent positions on the realism spectrum, present both interpretations as live possibilities with the distinguishing evidence for each. Do not force a single classification. Articulate what additional textual evidence would resolve the ambiguity (e.g., "If the text additionally claimed that moral truths are mind-independent, the position would be quietist realism rather than constructivism.").

5. **Purely negative or critical arguments**: If the argument only attacks realism (or anti-realism) without defending a positive metaethical position, classify the *target* accurately but note: "The argument's own metaethical commitments are underdetermined by its critical claims." Flag which positive positions are compatible with the argument's premises — several different positions may be consistent with the same set of negative arguments.

6. **Arguments that conflate metaethical and normative levels**: If the argument slides between claims about the *status* of morality (metaethical) and claims about what is *morally required* (normative), flag the conflation: "The argument conflates metaethical and normative levels. Premise P3 is a metaethical claim (about the nature of moral facts); premise P4 is a normative claim (about what we morally ought to do). The inference from P3 to P4 is only valid with an additional bridging premise."

## ARS Interface

- The Moral Realism Position Analysis Report can be passed directly to ARS `academic-paper` as a "metaethical presupposition statement" for the methodology section of a paper. Authors can use it to explicitly state and defend their metaethical commitments.
- Position classifications and dialectical vulnerability assessments are structured inputs for ARS `deep-research`, enabling targeted literature searches: "evolutionary debunking responses for robust non-naturalist realists," "supervenience explanations for quietist realism," etc.
- The report's "Recommended Counter-positions" section can seed ARS `academic-paper-reviewer` for anticipating reviewer objections — each recommended counter-position corresponds to an objection a reviewer might raise.
- The spectrum position map can be included in a paper's introduction as a visualization of the metaethical landscape and the author's placement within it.
- Citation formats throughout the report (Author, Year) are compatible with ARS `citation-check`.
- When the analysis identifies significant implicit commitments, these can be incorporated into ARS `academic-paper` as methodological limitations that the author should acknowledge.
