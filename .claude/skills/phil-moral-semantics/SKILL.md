---
description: "Moral Semantics Analysis — analyze moral language; map cognitivism/expressivism/prescriptivism positions; evaluate Frege-Geach problem responses and truth-aptness"
name: phil-moral-semantics
domain: metaethics
version: 1.0.0
---

# Moral Semantics Analysis

## Overview

Whether moral language expresses beliefs (cognitivism) or non-cognitive attitudes such as emotions, prescriptions, or plans (expressivism/prescriptivism/emotivism) is one of the deepest and most consequential divides in metaethics. This division shapes what kind of thing a moral disagreement could be, whether moral knowledge is possible, how moral arguments work at all, and how moral judgment connects to motivation. This skill analyzes an argument's semantic commitments — its stance on the meaning and function of moral language — and assesses how well the implicit or explicit semantic theory handles the central technical challenge: the embedding problem, also known as the Frege-Geach problem.

The skill classifies semantic positions with precision — not merely "cognitivist" versus "non-cognitivist" but the specific version (e.g., "Blackburn-style quasi-realist expressivism," "Gibbard-style norm-expressivism," "Schroeder's relational expressivism," "Ridge's hybrid expressivism," "Cornell-style synthetic naturalism," "analytic functionalist naturalism"). It then tests the semantics against the five canonical Frege-Geach embedding contexts (conditional antecedents, negation, interrogatives, attitude reports, and moral modus ponens). It analyzes the role of thick and thin moral concepts and how their distribution bears on semantic theory choice. Finally, it evaluates the truth-theoretic presuppositions that may, when deflationary truth is in play, collapse the cognitivism/non-cognitivism distinction into something closer to a verbal dispute.

The analysis is not merely classificatory but evaluative: it assesses whether the semantic theory the argument presupposes is adequate to the argument's own logical practices. If an argument treats moral claims as truth-apt in its reasoning but presupposes an expressivist semantics, the tension must be identified and its severity assessed.

## Input

**Required:**
- `argument-reconstruction` report (output of `phil-argument-reconstruct`): A structured representation of the argument's premises, conclusions, and inferential steps. The inferential structure is essential for Frege-Geach testing — the tests require explicit premise-conclusion structures to evaluate how moral sentences behave in embedded and unembedded contexts. If the reconstruction is incomplete about the argument's logical form, Frege-Geach testing will be unreliable.

**Optional:**
- `concept-map` report (output of `phil-conceptual-analysis`): Provides an analysis of the moral concepts the argument deploys — their definitions, conditions, and relationships. Used in Step 4 (thick/thin concept analysis) to identify the distribution of thick and thin concepts and assess their semantic implications.
- `original-text`: The primary source text, used when the reconstruction report does not capture semantic signals with sufficient nuance. Semantic analysis is sensitive to word choice ("express," "true," "belief," "attitude," "fact") in ways that structural reconstructions may abstract away from.

## Output

The skill produces a **Moral Semantics Analysis Report** structured according to the `moral-semantics-schema.json` specification. The report contains five principal sections:

**1. Semantic Position Classification**

Precise classification of the argument's semantic theory, with the exact version specified:

- **Cognitivist positions**: `non-naturalist` (Moore, Enoch — moral beliefs are about sui generis non-natural properties), `synthetic_naturalist_cornell` (Boyd, Sturgeon — moral properties are synthetic natural kinds identified a posteriori), `analytic_naturalist` (Jackson, Smith — moral properties are analyzable via conceptual analysis into natural properties), `reductive_naturalist` (Railton — moral properties reduce to natural properties via empirical theory).
- **Non-cognitivist positions**: `emotivist` (Ayer — moral claims express emotions), `prescriptivist` (Hare — moral claims are universalizable prescriptions), `expressivist_quasi_realist` (Blackburn — moral claims express attitudes but earn truth-talk), `norm_expressivist` (Gibbard — moral claims express plan-acceptance), `relational_expressivist` (Schroeder — moral claims express relational attitudes).
- **Hybrid positions**: `hybrid_expressivist` (Ridge — moral claims express both beliefs and desires), `fictionalist` (Joyce, Kalderon — moral discourse is a useful fiction).
- **Other**: Any position not captured above, with explicit specification.

Each classification is accompanied by textual evidence (specific phrases, premises, or structural features that indicate the semantic position) and a rationale explaining why this specific version, rather than its nearest neighbors, is the correct classification.

**2. Truth-Aptness Assessment**

The argument's stance on whether moral sentences are truth-apt, and what theory of truth is presupposed:
- `robust/correspondence`: Truth as correspondence to mind-independent fact. Truth-aptness is a substantial claim — moral sentences are truth-apt only if there are moral facts for them to correspond to.
- `deflationary/minimalist`: Truth as a disquotational device ("'p' is true iff p"). Truth-aptness is trivial — any declarative sentence is truth-apt.
- `epistemic`: Truth as idealized rational acceptability or warranted assertibility.
- `coherence`: Truth as coherence with a system of beliefs.

The assessment includes an analysis of whether the truth-theory collapses the cognitivism/non-cognitivism distinction. If the argument uses deflationary truth and simultaneously insists on a sharp distinction, this tension is flagged and analyzed.

**3. Frege-Geach Handling Evaluation**

Systematic testing of the argument's semantic theory against five canonical embedding contexts:
1. Conditional antecedents: "If lying is wrong, then getting your brother to lie is wrong."
2. Negation: "It is not the case that lying is wrong."
3. Interrogatives: "Is lying wrong?"
4. Attitude reports: "John believes that lying is wrong."
5. Moral modus ponens: Full validation of modus ponens with moral premises.

For each test: a passing/failing/ambiguous assessment with explanation. If the argument's text is silent, the report notes whether the semantic theory can handle the test based on the theoretical literature.

**4. Thick/Thin Concept Analysis**

Analysis of the distribution and role of thick concepts (courageous, cruel, generous, honest) versus thin concepts (good, bad, right, wrong, ought) in the argument, and how this distribution bears on semantic theory choice. Thick concepts pose challenges for both cognitivists and expressivists; the analysis identifies which challenge the argument must address.

**5. Semantic Parsimony Assessment**

Evaluation of whether the semantics is parsimonious relative to the argument's explanatory goals — whether it introduces unnecessary theoretical machinery, or conversely, whether it is too sparse to account for the full range of moral language phenomena present in the argument.

## Methodological Foundations

This skill draws on the following key philosophical resources. Each entry describes the core contribution and how it is operationalized.

**1. Ayer's Emotivism** (Language, Truth and Logic, 1936)

Ayer argues that moral judgments do not express propositions at all — they express emotions and are used to evoke emotions in others. "Stealing is wrong" does not state a fact; it functions like "Stealing — boo!" combined with an attempt to elicit a similar attitude in the audience. Emotivism is the simplest form of non-cognitivism and the historical starting point for the debate. Its virtue is its clean explanation of the connection between moral judgment and motivation (emotions motivate). Its fatal flaw, identified by subsequent critics, is the Frege-Geach problem: it cannot explain how moral sentences function in logical reasoning, because emotions do not have logical relations.

*Operationalization*: Emotivism serves as the baseline non-cognitivist position. When an argument's semantic view resembles emotivism, the analysis checks whether it inherits emotivism's vulnerability to the Frege-Geach problem. The skill also uses emotivism as a contrast class — more sophisticated expressivist views are understood as attempts to preserve emotivism's insights while solving its technical problems.

**2. Hare's Prescriptivism** (The Language of Morals, 1952)

Hare improves on emotivism by treating moral judgments as universalizable prescriptions — they are not descriptions of facts but imperatives addressed to all agents in relevantly similar circumstances. Unlike emotivism, prescriptivism can explain moral reasoning: prescriptions can contradict each other (you cannot simultaneously prescribe φ and prescribe not-φ for the same circumstances), be entailed by other prescriptions, and be universalized. However, prescriptivism still faces a version of the Frege-Geach problem: how do prescriptions function in unasserted contexts like conditional antecedents?

*Operationalization*: Prescriptivism is identified by its characteristic vocabulary — "prescribe," "command," "imperative," "universalizable." When an argument uses this vocabulary, the analysis classifies it as prescriptivist and applies the Frege-Geach tests specifically calibrated for prescriptive semantics.

**3. The Frege-Geach Problem** (Geach, "Assertion," 1965; Searle, "Meaning and Speech Acts," 1962)

The Frege-Geach problem is the central technical challenge to non-cognitivism. The problem: if moral sentences do not express propositions (belief-eligible contents), how can they function in unasserted contexts? In "If lying is wrong, then getting your brother to lie is wrong," the antecedent "lying is wrong" is not asserted — the speaker is not expressing disapproval of lying. Yet the sentence is meaningful, and the inference to the conclusion is valid. Non-cognitivist theories must provide a compositional semantics that explains how the meaning of a complex moral sentence is a function of the meanings of its parts, including when those parts appear in unasserted contexts.

*Operationalization*: The five Frege-Geach tests (conditional antecedents, negation, interrogatives, attitude reports, moral modus ponens) are the core analytical procedure in Step 3. The skill does not merely check whether the argument mentions the Frege-Geach problem; it tests whether the argument's actual semantic practice — its use of moral sentences in embedded contexts — is consistent with its explicit or implicit semantic theory.

**4. Blackburn's Quasi-Realist Program** (Spreading the Word, 1984; Essays in Quasi-Realism, 1993)

Blackburn's quasi-realism is an expressivist research program that aims to show that expressivism can "earn the right" to use realist-sounding language — "moral truth," "moral fact," "moral knowledge" — without abandoning its non-cognitivist core. The key move is treating moral *attitudes* (not beliefs) as the primary bearers of logical relations. Attitudes can be inconsistent (approving of X and disapproving of X is a clash of attitudes), can be entailed by other attitudes, and can be combined in complex attitudinal structures that mirror the logical structure of complex sentences. Quasi-realism is expressivism with full-strength truth-talk.

*Operationalization*: Quasi-realism is identified by its characteristic combination: denial of robust moral facts + full use of truth-talk + explanation of logical relations in terms of attitudes. When diagnosing quasi-realism, the skill checks whether the argument provides an attitudinal semantics or merely asserts that expressivism is compatible with truth-talk.

**5. Gibbard's Norm-Expressivism** (Wise Choices, Apt Feelings, 1990; Thinking How to Live, 2003)

Gibbard analyzes moral judgments as expressions of acceptance of systems of norms — they are states of "planning" what to do in various circumstances, rather than beliefs about normative facts. The key innovation is providing a formal possible-worlds semantics for planning states, making the Frege-Geach problem formally tractable. "Lying is wrong" expresses a plan to avoid lying; "If lying is wrong, then X is wrong" expresses a complex planning state whose content can be given in possible-worlds terms.

*Operationalization*: Norm-expressivism is identified by its distinctive vocabulary — "plan," "planning state," "norm acceptance," "hyperplan." The analysis checks whether the argument's semantics can provide a compositional account of planning-state content, or merely asserts that planning states have logical structure.

**6. Schroeder's Relational Expressivism** (Being For, 2008; Noncognitivism in Ethics, 2013)

Schroeder argues that expressivism need not assign a single attitude type (e.g., disapproval) to moral predicates. Instead, complex moral sentences express complex relational attitudes. "Murder is wrong" expresses the attitude of *being for* blaming for murder. "If murder is wrong, then abortion is wrong" expresses the attitude of *being for* (not blaming for murder, or blaming for abortion). This relational structure allows expressivism to explain the validity of moral modus ponens compositionally, without the ad hoc machinery of earlier expressivist attempts.

*Operationalization*: Relational expressivism is the most technically sophisticated expressivist theory. The analysis checks whether the argument's semantics assigns relational attitudes (being for, being against) to moral predicates, and whether it can explain the inconsistency of "murder is wrong" and "murder is not wrong" as a clash of relational attitudes.

**7. Ridge's Hybrid Expressivism** (Impassioned Belief, 2014)

Ridge argues that moral judgments express both beliefs (a cognitive component) and desires or other pro-attitudes (a non-cognitive component). The belief component handles the Frege-Geach problem (beliefs have standard logical properties), while the desire component explains the tight connection to motivation. The hybrid approach aims to combine the advantages of cognitivism (straightforward semantics) with the advantages of expressivism (motivational internalism).

*Operationalization*: Hybrid expressivism is identified by its claim that moral judgments have *two* semantic components — one descriptive, one expressive. The analysis checks whether the argument provides a compositional account of how the two components combine, and whether the view collapses into one of its components under pressure.

## Steps

### Step 1: Identify Semantic Markers

Scan the argument-reconstruction report and source text for semantic indicators — words, phrases, and structural features that reveal the argument's semantic commitments.

**Procedural guidance:**

1. **Cognitivist markers**: "moral belief," "moral truth," "moral proposition," "is true" / "is false" (applied to moral claims), "moral knowledge," "moral fact," "discover" (moral truths), "correct" / "incorrect" (applied to moral claims), "objective moral reality," "represents moral facts," "corresponds to," "moral property." Also: the argument's unselfconscious use of truth-predicates for moral claims ("it is true that lying is wrong") without qualifying them as merely "minimal" truth.

2. **Non-cognitivist markers**: "express," "endorse," "prescribe," "approve" / "disapprove," "plan," "accept" (norms, not propositions), "project," "emotive," "attitude" (as what moral language expresses), "non-cognitive," "desire-like," "practical" (as opposed to theoretical). Also: explicit denial that moral claims are truth-apt ("moral claims are neither true nor false"), or restriction to "minimal" truth.

3. **Hybrid markers**: Simultaneous use of belief-language and attitude-language; claims that moral judgments have "both" descriptive and expressive components; "dual-aspect" or "bifurcated" semantics for moral language.

4. **Truth-minimalist markers**: "true by default," "deflationary," "disquotational," "truth is not a substantial property," "minimal truth," "truth as a logical device." These are significant because deflationary truth makes truth-aptness trivial and threatens to collapse the cognitivism/non-cognitivism distinction.

5. **Fictionalist markers**: "useful fiction," "pretend," "make-believe," "as if," "myth," "error" (about moral facts combined with continued moral discourse), "revolutionary" vs. "hermeneutic" fictionalism.

6. **Record each marker**: For each semantic marker, record the exact text, source location, and the type of semantic commitment it suggests (cognitivist, non-cognitivist, hybrid, minimalist, fictionalist). This becomes the evidence base for classification in Step 2.

### Step 2: Classify Semantic Position

Classify the argument's semantic position with the greatest possible precision. Never use generic labels like "cognitivist" or "non-cognitivist" — specify the exact version.

**Procedural guidance:**

1. **Use the classification table**:

| Position | Moral Sentences Express | Truth-Apt? | Core Proponent(s) | Key Text |
|---|---|---|---|---|
| Cognitivist Non-Naturalist | Beliefs about irreducible moral facts | Yes (robust) | Moore, Enoch | Principia Ethica |
| Cognitivist Naturalist (Cornell) | Beliefs about synthetic natural properties | Yes (robust) | Boyd, Sturgeon | "How to Be a Moral Realist" |
| Cognitivist Naturalist (Analytic) | Beliefs about analytic natural properties | Yes (robust) | Jackson, Smith | From Metaphysics to Ethics |
| Cognitivist Naturalist (Reductive) | Beliefs about reducible natural properties | Yes (robust) | Railton | "Moral Realism" |
| Emotivism | Emotions | No | Ayer, early Stevenson | Language, Truth and Logic |
| Prescriptivism | Universal prescriptions | No | Hare | The Language of Morals |
| Quasi-Realist Expressivism | Attitudes, earns truth-talk | Yes (minimal) | Blackburn | Essays in Quasi-Realism |
| Norm-Expressivism | Plans/acceptance of norms | Yes (minimal) | Gibbard | Wise Choices, Apt Feelings |
| Relational Expressivism | Relational attitudes (being-for) | Yes (minimal) | Schroeder | Being For |
| Hybrid Expressivism | Beliefs + desires/attitudes | Yes (hybrid) | Ridge | Impassioned Belief |
| Fictionalism | Beliefs about a useful fiction | Fiction-internal | Joyce, Kalderon | The Myth of Morality |

2. **Distinguish nearest neighbors**: For each classification, explain why this specific version rather than its closest competitor. "The argument is classified as quasi-realist expressivism rather than norm-expressivism because it grounds logical relations in attitudes directly (Blackburn's approach) rather than providing a formal possible-worlds semantics for planning states (Gibbard's approach). Evidence: the argument speaks of 'clashes of attitude' (paragraph 3) and 'earning the right to truth-talk' (paragraph 7) — both characteristic Blackburnian formulations."

3. **Handle ambiguity**: If the argument is ambiguous between two or more semantic positions, explicitly identify the diagnostic question that distinguishes them and note that the available evidence does not resolve it. "The argument is ambiguous between cognitivist naturalism (analytic) and cognitivist naturalism (synthetic). It treats moral properties as natural but does not specify whether the reduction is conceptual (analytic) or empirical (synthetic). The diagnostic question — 'Are moral-natural property identities knowable a priori or a posteriori?' — cannot be answered from the text."

4. **Assess consistency**: Check whether the argument's semantic position is internally consistent and consistent with its semantic practice. "The argument explicitly claims to be non-cognitivist (paragraph 2: 'moral claims are not truth-apt') but consistently embeds moral claims in truth-functional contexts (paragraphs 5, 7, 12: 'it is true that...', 'if it is the case that...'). This is a performative inconsistency: the argument's practice presupposes truth-aptness that its theory denies."

### Step 3: Test Frege-Geach Handling

The Frege-Geach problem tests whether a semantic theory can explain the logical behavior of moral sentences in unasserted (embedded) contexts. Apply all five canonical tests to the argument's semantic commitments.

**Procedural guidance:**

**Test 1: Conditional Antecedents**

Does the semantics handle the following inference?

```
(P1) If lying is wrong, then getting your brother to lie is wrong.
(P2) Lying is wrong.
(C)  Therefore, getting your brother to lie is wrong.
```

For a semantic theory to validate this inference, it must explain: (a) what "lying is wrong" means in the unasserted antecedent of (P1) — it must be the same meaning as in the asserted (P2); (b) why the inference is valid — modus ponens must preserve whatever semantic value the theory assigns to moral claims.

- Cognitivist theories: Straightforward — moral claims express propositions, and propositions have standard logical properties. Modus ponens works normally.
- Expressivist theories: Must explain how the attitude expressed by "lying is wrong" in (P2) is the same attitude that appears as a component of the complex attitude expressed by (P1). Early expressivism (emotivism) cannot do this; sophisticated expressivism (Blackburn, Gibbard, Schroeder) attempts it through various compositional mechanisms.
- Hybrid theories: The belief component handles the logic; the desire component explains the motivational connection.

**Assessment output**: For Test 1, state: "Pass: the semantics validates the conditional antecedent inference because [explanation]" or "Fail: the semantics cannot explain how 'lying is wrong' means the same thing in asserted and unasserted contexts because [explanation]" or "Ambiguous: the argument is silent on this but its semantic theory [would/would not] handle it because [explanation based on theoretical literature]."

**Test 2: Negation**

Does the semantics handle: "It is not the case that lying is wrong"?

The semantics must explain what it is to deny a moral claim — what semantic value corresponds to moral negation?

- Cognitivist: Negation is standard propositional negation. "Not (lying is wrong)" is true iff "lying is wrong" is false.
- Expressivist: Must explain what attitude corresponds to moral negation. Is it the absence of the disapproval attitude? A distinct "toleration" attitude? An attitude of disagreeing with disapproval? The expressivist must provide an account.
- The test also checks whether the semantics validates the law of non-contradiction: "lying is wrong" and "it is not the case that lying is wrong" cannot both be correct.

**Test 3: Interrogatives**

Does the semantics handle: "Is lying wrong?"

The semantics must explain what it is to ask a moral question — what is being asked, and what would count as an answer?

- Cognitivist: A moral question asks whether a certain proposition is true. Answering it involves asserting or denying the proposition.
- Expressivist: What is being asked? If moral claims express attitudes, what does a moral question express? The expressivist must explain how the interrogative mood transforms the attitude expressed by the declarative.

**Test 4: Attitude Reports (Propositional Attitude Ascriptions)**

Does the semantics handle: "John believes that lying is wrong" and "Mary hopes that lying is wrong"?

Moral claims can embed under propositional attitude verbs. The semantics must explain what it is to believe, hope, fear, doubt, or wonder whether a moral claim is the case.

- Cognitivist: Straightforward — moral claims express propositions, and propositional attitudes are attitudes toward propositions.
- Expressivist: Faces a challenge — if "lying is wrong" does not express a proposition, what is the object of John's belief? The expressivist must either analyze "believes that lying is wrong" as ascribing a non-cognitive attitude (disguised belief-ascription) or provide an alternative semantics for propositional attitude ascriptions.

**Test 5: Moral Modus Ponens**

Does the semantics validate the basic validity of modus ponens with moral premises?

```
(P1) If killing is wrong, then abortion is wrong.
(P2) Killing is wrong.
(C)  Therefore, abortion is wrong.
```

This is the most standard Frege-Geach test — if the semantics cannot validate moral modus ponens, it is inadequate as a semantics for moral discourse. The semantics must explain: (a) what logical form (P1) has; (b) why the inference from (P1) and (P2) to (C) is necessarily truth-preserving (or attitude-preserving, or whatever the relevant semantic value is).

**Compile results**: After testing all five contexts, produce a summary assessment: "The argument's semantic theory passes N/5 Frege-Geach tests. The failures are Tests [X, Y] because [reasons]. The overall adequacy of the semantics for the argument's logical practice is [adequate/partially adequate/inadequate]."

### Step 4: Analyze Moral Concept Structure

Examine the moral concepts deployed in the argument and analyze how their structure bears on semantic theory choice.

**Procedural guidance:**

1. **Classify each moral concept as thick or thin**:
   - **Thin concepts**: Highly general moral concepts with minimal descriptive content — "good," "bad," "right," "wrong," "ought," "obligatory," "permissible," "forbidden." Thin concepts are the primary battleground for the cognitivism/expressivism debate because their minimal descriptive content makes them hardest for cognitivists to naturalize and easiest for expressivists to analyze as purely expressive.
   - **Thick concepts**: Concepts that combine descriptive and evaluative content in a way that resists disentanglement — "courageous," "cruel," "generous," "honest," "benevolent," "treacherous," "lewd," "chaste," "brutal," "kind." Thick concepts are challenging for both cognitivists (the evaluative component seems tightly linked to motivation, favoring non-cognitivism) and expressivists (the descriptive component seems truth-apt, favoring cognitivism).

2. **Map the distribution**: Count the occurrences of thick versus thin concepts. Determine which type dominates the argument's moral vocabulary. An argument that relies primarily on thin concepts is focused on the core cognitivism/expressivism debate; an argument that relies primarily on thick concepts may need a semantics that handles entangled descriptive-evaluative content.

3. **Assess disentanglement**: Can the evaluative and descriptive components of the argument's thick concepts be separated analytically? If yes (e.g., "courageous" = "disposed to face danger" + "good"), this favors semantic theories that analyze thick concepts as thin evaluation + descriptive content. If no (the evaluative and descriptive are inseparable), this favors semantic theories that treat thick concepts as semantically basic and unified.

4. **Semantic implications**:
   - Dominance of thin concepts + explicit truth-talk = suggests cognitivism.
   - Dominance of thin concepts + attitude-talk = suggests expressivism.
   - Dominance of thick concepts = the argument's semantic theory must handle fact-value entanglement, which is a challenge for both cognitivism and expressivism but in different ways.

### Step 5: Assess Truth-Minimalism Implications

Determine the argument's truth-theoretic commitments and assess whether they collapse or preserve the cognitivism/non-cognitivism distinction.

**Procedural guidance:**

1. **Diagnose truth theory**:
   - `robust/correspondence`: Truth is correspondence to mind-independent fact. Under this theory, truth-aptness is a substantial claim — a discourse is truth-apt only if its claims can correspond to facts of the relevant kind. Cognitivism and non-cognitivism are sharply distinguished.
   - `deflationary/minimalist`: Truth is merely a disquotational device. "'p' is true" means nothing more than "p." Under this theory, truth-aptness is trivial — any declarative sentence that embeds grammatically is automatically truth-apt. This threatens to collapse the cognitivism/non-cognitivism distinction: if both cognitivists and expressivists can call moral claims "true," what is the difference?
   - `epistemic`: Truth as idealized rational acceptability. Under this theory, moral claims are truth-apt if they can be justified under ideal epistemic conditions.
   - `coherence`: Truth as coherence with a system of beliefs.

2. **Assess collapse risk**: If the argument uses deflationary truth AND insists on a sharp cognitivism/non-cognitivism distinction:
   - Flag the tension: "The argument assumes a deflationary theory of truth (paragraph 2: 'truth is merely a disquotational device'), which makes truth-aptness trivial. But the argument simultaneously insists on a sharp distinction between cognitivism and non-cognitivism (paragraph 5). Under deflationism, this distinction collapses — both sides can call moral claims 'true.' The distinction must be recast in other terms."
   - Identify whether the argument recasts the distinction in other terms: the nature of the mental state expressed (belief vs. desire-like state), the direction of fit (mind-to-world vs. world-to-mind), or the explanatory role of moral properties.

3. **Assess significance**: If the collapse is genuine (the argument's truth theory undermines its own distinction), assess whether anything substantive remains of the cognitivism/non-cognitivism debate in the argument, or whether it has become a merely verbal dispute.

### Step 6: Compile Report

Assemble the findings from Steps 1-5 into a structured report conforming to `moral-semantics-schema.json`.

**Procedural guidance:**

1. **Executive Summary**: State the semantic position with precision and the key findings from Frege-Geach testing. "This argument presupposes a quasi-realist expressivist semantics (Blackburn-style): moral claims express attitudes, but the argument earns the right to full truth-talk through Blackburn's program. The semantics passes 4/5 Frege-Geach tests; the attitude-report test (Test 4) reveals a residual tension in the semantics' handling of propositional attitude ascriptions."

2. **Semantic Classification**: Present the classification with detailed evidence. Quote the semantic markers. Explain why this specific version rather than its nearest neighbors. State confidence level.

3. **Frege-Geach Results**: Present the results for all five tests in a structured format (one paragraph per test). Include the reasoning for each assessment. If the argument is silent on a test, present the theoretical assessment.

4. **Thick/Thin Analysis**: Present the concept distribution, classification, and disentanglement analysis. State the semantic implications.

5. **Truth-Minimalism Assessment**: Present the truth-theory diagnosis. If collapse risk exists, present it with an analysis of whether the argument has resources to avoid it.

6. **Overall Assessment**: Synthesize the findings into an overall evaluation of the argument's semantic adequacy. "The argument's semantic theory is [adequate/partially adequate/inadequate] to its own logical practice. The primary strength is [X]; the primary vulnerability is [Y]."

## Quality Criteria

1. **Semantic precision**: Classify to the exact version of the semantic theory — never merely "cognitivist" or "non-cognitivist." Cite the specific features of the text that distinguish this version from its nearest neighbors. If the text is ambiguous, state the range of compatible positions and identify the diagnostic question that would decide among them.

2. **Frege-Geach test rigor**: Apply all five Frege-Geach tests explicitly and individually. Do not aggregate them into a single "handles Frege-Geach" assessment. For each test, show the reasoning — why does the semantics pass or fail? If the text is silent on a test, provide the theoretical assessment based on the classified semantic position's resources as documented in the literature.

3. **Thick/thin awareness**: Identify whether the argument deploys thick concepts, thin concepts, or both, and analyze how this distribution bears on semantic theory choice. Do not analyze an argument that is entirely about thick concepts as if it were about thin concepts, or vice versa.

4. **Truth-theory transparency**: Clearly state the argument's presupposed truth theory and assess whether it collapses the cognitivism/non-cognitivism distinction. If the argument is ambiguous between robust and deflationary truth, analyze both interpretations and their implications.

5. **Compositional adequacy**: Assess whether the semantic theory can provide a compositional semantics for arbitrarily complex moral sentences — whether the meaning of a complex moral sentence is systematically determined by the meanings of its parts and their syntactic arrangement. A theory that handles simple declaratives but cannot explain embeddings is semantically inadequate.

6. **Practice-theory consistency**: Check whether the argument's actual semantic practice (how it uses moral language in its own reasoning) is consistent with its explicit or implicit semantic theory. Flag performative inconsistencies.

## Relations to Other Skills

**Depends on (upstream):**
- `phil-argument-reconstruct`: Takes the reconstructed standard form as input. The Frege-Geach tests require explicit premise-conclusion structures — if the reconstruction does not capture the argument's logical form, the tests cannot be applied reliably.
- `phil-conceptual-analysis`: Uses the concept-map report to identify thick and thin moral concepts, analyze their structure (necessary/sufficient conditions, descriptive/evaluative components), and assess disentanglement.

**Referenced knowledge resources:**
- `references/glossary-metaethics.md`: Definitions of core semantic concepts (cognitivism, non-cognitivism, expressivism, emotivism, prescriptivism, truth-aptness, Frege-Geach problem, thick/thin concepts, minimal truth, quasi-realism, norm-expressivism).
- `references/metaethical-distinctions.md`: The cognitivism/non-cognitivism distinction, the realism/anti-realism distinction (and how they cross-cut), analytic/synthetic naturalism, and radical/moderate expressivism.

**Feeds into (downstream):**
- `phil-moral-realism`: Semantic commitments inform the realism spectrum classification. A non-cognitivist semantics rules out robust realist and standard error-theoretic positions (both require truth-aptness). A cognitivist semantics is compatible with the full realism/anti-realism spectrum. The semantic analysis report should be passed to the realism skill.
- `phil-moral-psychology`: Semantic commitments have implications for moral psychology. Expressivist semantics pairs naturally with motivational internalism (attitudes motivate); cognitivist semantics requires an account of how moral beliefs motivate (externalism or anti-Humeanism).

**Independent of (cross-domain):**
- `phil-normativity`: Semantic analysis of moral language is logically independent of the source and structure of normativity. A constitutivist about normativity could be either a cognitivist or an expressivist about semantics. However, complete metaethical analysis should check for consistency: does the semantic theory cohere with the normative theory?

## Boundary Conditions

**1. No moral semantic content**: If the argument contains no claims about the meaning, function, or truth-status of moral language, output: "No moral semantic claims detected. The argument operates at the first-order normative level without reflecting on the semantics of moral language. Moral semantics analysis yields no explicit findings." Optionally, offer to analyze implicit semantic commitments: "However, the argument's use of moral language reveals implicit semantic commitments. Would you like an analysis of these?"

**2. Pure normative argument without meta-level semantic reflection**: If the argument deploys moral language without theorizing about it, the analysis should proceed by diagnosing implicit commitments. Note in the report: "The argument uses moral language without addressing its semantics. It has implicit semantic commitments — for instance, it treats moral claims as [truth-apt when making logical inferences / expressive when emphasizing practical import] — that it does not articulate or defend." Classify these implicit commitments with lower confidence.

**3. Deflationary truth collapse**: If the argument treats truth as deflationary and moral language as expressive, it may be implicitly collapsing the cognitivism/non-cognitivism distinction. The report must flag this and analyze whether the distinction is being maintained on other grounds (e.g., the nature of the expressed mental state: belief vs. desire-like state).

**4. Arguments about non-moral semantics**: If the argument discusses linguistic meaning generally (philosophy of language) without specific application to moral discourse, note: "The argument engages general philosophy of language without specific application to moral discourse. Its semantic commitments may have implications for moral semantics, but these are not developed. No moral-semantic analysis is possible beyond noting the general semantic framework assumed."

**5. Historical texts predating the Frege-Geach problem**: If the argument predates Geach (1965) and advances a non-cognitivist view (e.g., Ayer 1936, early Stevenson, early Hare), apply the Frege-Geach tests but add the caveat: "This argument was written before the Frege-Geach problem was articulated. The analysis applies the tests to assess whether the semantic theory has the resources to handle embeddings, but the author cannot be faulted for failing to anticipate a problem not yet formulated." Classify whether the theory, as stated, can be extended to handle the problem, or whether it is fundamentally incapable of doing so.

**6. Revisionary semantic theories**: If the argument proposes a revisionary semantics (e.g., "we should stop using moral language in truth-apt ways," "moral discourse should be replaced by..."), distinguish between the descriptive claim (what moral language currently means) and the revisionary claim (what it should mean). Analyze both.

## ARS Interface

This skill is part of the Academic Research Skills (ARS) metaethics pipeline. It conforms to the ARS skill specification:

- **Invocation pattern**: This skill is invoked when the system detects a need for moral semantics analysis in a metaethics workflow, typically after argument reconstruction and conceptual analysis, and before moral realism analysis. It can be invoked standalone or as part of a pipeline run.

- **Schema compliance**: The output conforms to `moral-semantics-schema.json` (located in `shared/`), which defines the JSON structure for moral semantics analysis reports. All required fields are populated; optional fields are populated when information is available.

- **Cache behavior**: Moral semantics analysis reports are cached per argument (keyed by argument-reconstruction hash). If the same argument is analyzed again, the cached report is returned unless invalidated.

- **Error handling**: If required input is missing or malformed, the skill returns a structured error. If no semantic content is detected (boundary condition 1), the skill returns a null report.

- **Pipeline integration**: Output tagged with `output-type: moral-semantics-analysis`. The report includes `pipeline_metadata` with version, timestamp, and input hashes. Downstream skills (`phil-moral-realism`, `phil-moral-psychology`) consume this output.

- **ARS tool integration**:
  - The Moral Semantics Analysis Report can be passed to ARS `academic-paper` as a "semantic framework statement."
  - The Frege-Geach test results can inform ARS `deep-research` for targeted searches on semantic theory responses to the embedding problem.
  - The semantic position classification can seed ARS `academic-paper-reviewer` for anticipating objections about semantic adequacy.
  - Citations are compatible with ARS `citation-check`.

- **Versioning**: Semantic versioning. Breaking schema changes = major bump. New semantic position types = minor bump. Clarifications and fixes = patch bump.
