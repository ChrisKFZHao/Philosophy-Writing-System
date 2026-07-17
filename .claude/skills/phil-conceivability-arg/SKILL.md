---
name: phil-conceivability-arg
description: "Conceivability Argument Analysis — evaluate the conceivability-to-possibility chain; analyze zombie arguments and modal epistemology in philosophical reasoning"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Conceivability Argument Analysis

## Overview

The conceivability-to-possibility inference is one of the most contested moves in analytic metaphysics. The general form is seductively simple: "I can conceive of P; therefore, P is possible; therefore, Q." But each link in this chain requires independent justification, and the entire chain is vulnerable at multiple points. From Descartes's argument for dualism to Chalmers's zombie argument against physicalism, conceivability arguments have shaped the course of metaphysics — and have been subject to sustained methodological critique from modal skeptics who doubt that our powers of conception are a reliable guide to the modal structure of reality.

This skill systematically evaluates every inferential link in a conceivability argument. It does not ask "is the conclusion true?" but rather "does the conceivability of the premises actually support the possibility of the conclusion, and does that possibility actually entail the argument's ultimate thesis?" The analysis produces a chain diagram, a link-by-link evaluation with individual ratings, a modal framework assessment, a gap analysis that distinguishes bridgeable from unbridgeable gaps, and an overall strength rating (Strong/Medium/Weak/Broken).

The gold standard for this analysis is the zombie argument against physicalism: "Zombies are conceivable; therefore, zombies are metaphysically possible; therefore, physicalism is false." But the methodology applies equally to any argument that moves from what we can imagine or conceive to what is possible or actual: conceivability arguments for dualism, against materialism, for the existence of God (the ontological argument has a conceivability component), for essential properties, for the possibility of time travel, and for disembodied existence. The common structure — a chain from conceivability to possibility to a metaphysical conclusion — unites these diverse arguments under a single analytic framework.

The skill's core methodological commitment is to treat each inferential link as a separate argumentative step that must be individually assessed. The gap between conceivability and possibility is not one gap but a series of smaller gaps, each of which may be bridged or may fail independently. This granular approach respects the dialectical structure: often the most interesting criticism of a conceivability argument is not that the whole chain fails, but that a specific link (e.g., the move from ideal conceivability to genuine possibility under two-dimensional semantics) does not hold, while other links remain intact.

The skill is built on the post-Kripkean consensus that conceivability is neither necessary nor sufficient for possibility, and that the burden of proof is on anyone who wants to draw metaphysical conclusions from conceivability data. It incorporates the two-dimensional semantic framework (Chalmers, Jackson) as the most sophisticated defense of the inference, while also engaging critically with that framework's limitations and with the objections from modal skepticism (van Inwagen) and the phenomenal concept strategy (Loar, Balog, Papineau). The analysis is dialectically fair — it presents the strongest version of the argument under examination before evaluating it.

## Input

**Required:**
- `argument-reconstruction report` (from `phil-argument-reconstruct`): Provides the standard form of the conceivability argument, with the inferential links made explicit. The reconstruction should isolate each step: conceivability claim, possibility claim, intermediate conclusion, final conclusion. The chain reconstruction in Step 1 depends on this input; its accuracy is bounded by the quality of the reconstruction.
- `modal-argument analysis report` (from `phil-modal-arg`): Provides the modal framework analysis — S4/S5 determination, accessibility relations, De dicto/De re distinctions, iterated modality usage. Essential for Step 5 (modal framework check) and for evaluating whether the modal operators used in the argument have the right logical properties to support the inference chain. The conceivability-to-possibility inference is irreducibly modal; it cannot be evaluated without clarity about what "possibility" means.

**Optional:**
- `original text`: The source material. Conceivability arguments often involve thought experiments (zombies, disembodied minds, inverted spectra) whose details are more vivid and revealing in the original prose than in the formalized reconstruction. Direct access enables verification of the conceivability language and capture of nuance lost in reconstruction.
- `concept-map report`: A concept map may reveal whether the key concepts (consciousness, physical, zombie) are sufficiently well-defined for the conceivability claim to be assessable.

## Output

**Conceivability Argument Analysis Report** — containing:

### Section 1: Chain Reconstruction

The conceivability chain represented as numbered, explicit links. Each link is a single, well-formed claim that can be evaluated independently. The full chain is presented at the outset so the reader can see the argument's architecture before the evaluation begins. Example for a Chalmers-style zombie argument:
```
L1: Zombies (physical duplicates without consciousness) are conceivable.
L2: If zombies are conceivable, then zombies are metaphysically possible.
L3: If zombies are metaphysically possible, then consciousness is non-physical.
L4: Therefore, consciousness is non-physical.
```

Suppressed premises are surfaced (e.g., "physicalism entails the metaphysical necessity of physical-to-phenomenal supervenience"). Alternative formulations noted if present (e.g., both reductio and direct forms).

### Section 2: Conceivability Type Assessment

Classification of the conceivability claim with textual evidence and justification:

| Type | Definition | Modal Support Strength |
|------|-----------|----------------------|
| Prima Facie Conceivability | Seems conceivable on initial reflection; no obvious contradiction. | Weak — many prima facie conceivable things are impossible (e.g., squaring the circle). Supports only a presumption of possibility, easily defeated. |
| Negative Conceivability | Cannot be ruled out a priori. No detectable contradiction. | Still weak — inability to detect contradiction may reflect ignorance rather than coherence (Kripke: Hesperus ≠ Phosphorus is negatively conceivable but impossible). |
| Positive Conceivability | Can coherently imagine a scenario in some detail. Not merely "not ruled out" but positively constructed. | Stronger — requires positive construction, not just absence of detected contradiction. Still limited by the detail and completeness of the imagined scenario. |
| Ideal Positive Conceivability | Conceivable under ideal rational reflection — after considering all relevant a posteriori information, performing all necessary inferences, and achieving maximal rational coherence. Chalmers's preferred category. | Strongest — Chalmers argues it entails primary (conceptual) possibility. But whether any actual human achieves it is contested. |

Assessment includes: (a) textual evidence for the claimed type, (b) whether the claimed type is appropriate for the argument's ambition (e.g., an anti-physicalist argument needs at least positive conceivability; prima facie won't do), (c) any dispute about the conceivability claim (e.g., Dennett's denial that zombies are conceivable at all).

### Section 3: Link-by-Link Evaluation

Each link evaluated independently with its own rating:

**L1: Conceivability to Possibility (the Core Link):** Almost always the most contested. Evaluated via:
- Kripke's "necessary a posteriori" objection: some necessary truths known only empirically (water = H2O). Conceivability of their negation is an illusion of ignorance. Does this apply to the target case?
- The "genuine conceivability" challenge: is the conceivability genuine (tracking real modal structure) or merely apparent? What test distinguishes them?
- Two-dimensional semantics defense (Chalmers): primary vs. secondary intensions. Ideal conceivability entails primary possibility; under right conditions, primary possibility entails secondary (metaphysical) possibility. Evaluate whether the conditions hold.
- Completeness challenge: can the scenario be fully specified without underdescribed placeholders? For zombie arguments: can we truly conceive of a complete physical duplicate?
- Rating: Solid / Adequate / Questionable / Broken.

**L2: Possibility to Conclusion (the Entailment Link):** Does possibility entail the conclusion?
- For zombie arguments: zombie possibility entails physicalism is false only if physicalism requires necessary supervenience. Type-B materialists accept the epistemic gap but deny the ontological gap (like water = H2O). If the argument does not address Type-B materialism, flag the gap.
- Check logical form: "◇P; □(P to Q)" yields "◇Q" (valid). But "◇P; if P then Q" does not yield "Q." Ensure the modal logic is correct.
- Does the conclusion match the strength of the possibility claim? Is it overclaimed?

**Intermediate Links:** Any additional links evaluated for logical validity, suppressed premises, and counterexamples.

Each link receives a rating and a detailed paragraph of justification.

### Section 4: Gap Analysis

Systematic identification of where and how the chain weakens:
- **Individual link gap ratings:** Solid / Adequate / Questionable / Broken for each link.
- **Bridgeability assessment:** Unbridgeable (fatal — the inference is impossible to support within the argument's framework), Bridgeable (potentially fixable with additional work), or Dialectically bridgeable (gap exists only given contested assumptions).
- **Cumulative gap assessment:** Even if each link is only Weak independently, the cumulative effect may render the overall chain Broken. Assess whether gaps compound or are independent.
- **Gap severity ranking:** Gaps listed in order of severity (most damaging first), with whether the rest of the argument survives if the gap is conceded.

### Section 5: Modal Framework Assessment

Evaluation of the modal logic and semantics employed:
- **S4 vs. S5 requirements:** Which modal system does the argument need? S5 (universal accessibility) often required for Chalmers-style arguments but is controversial for metaphysical modality.
- **Accessibility relation:** What kind of accessibility (logical, conceptual, metaphysical, physical)? Any slides between different accessibility relations?
- **Iterated modalities:** Does the argument use □◇P or ◇□P? Are these uses properly motivated?
- **De re vs. De dicto:** Does the argument involve de re modality (about objects)? De re modal claims introduce cross-world identity complexities.
- **Modal framework rating:** Explicit and consistent / Implicit but reconstructable / Ambiguous or inconsistent / Missing.

### Section 6: Overall Strength Rating

A summary assessment:
- **Strong:** All links Solid, no unbridgeable gaps. Rarely awarded — requires ideal conceivability properly linked to metaphysical possibility with a defended modal epistemology and tight entailment.
- **Medium:** Most links Solid/Adequate. Gaps are bridgeable. The argument has real force but faces principled objections not yet settled.
- **Weak:** Key links Questionable, significant gaps. The argument does not compel assent even if not definitively refuted.
- **Broken:** At least one link Broken with an unbridgeable gap. The argument fails on its own terms; further work cannot salvage it.

Each rating includes a full paragraph of holistic justification referencing specific link evaluations and gap analysis.

## Methodological Foundations

The skill is grounded in seven canonical sources spanning conceivability, modal epistemology, and the two-dimensionalist defense:

1. **Chalmers, David (2002). "Does Conceivability Entail Possibility?"** In *Conceivability and Possibility*, edited by Tamar Szabo Gendler and John Hawthorne. Oxford University Press. — The definitive defense of the conceivability-to-possibility inference via two-dimensional semantics. Chalmers argues that ideal primary positive conceivability entails primary possibility, and when coupled with the right semantic claims about the terms involved, this can entail secondary (metaphysical) possibility. This is the framework that most contemporary conceivability arguments either adopt or must respond to. The skill uses this as the standard for evaluating whether the core link (conceivability to possibility) is adequately defended.

2. **Chalmers, David (2009). "The Two-Dimensional Argument Against Materialism."** In *The Oxford Handbook of Philosophy of Mind*, edited by Brian McLaughlin, Ansgar Beckermann, and Sven Walter. Oxford University Press. — The full-dress presentation of the two-dimensional argument against materialism, with the zombie argument as a centerpiece. Provides the primary intension/secondary intension framework, the "conceivability-possibility" bridge principle, and responses to standard objections. Essential for evaluating Chalmers-style arguments and for understanding the conditions under which the two-dimensional defense succeeds or fails.

3. **Yablo, Stephen (1993). "Is Conceivability a Guide to Possibility?"** *Philosophy and Phenomenological Research* 53(1): 1-42. — The classic taxonomy of conceivability types and the argument that no single conceivability type provides a reliable guide to possibility. Yablo distinguishes objectual vs. propositional conceivability, argues that even ideal conceivability may mislead if the subject lacks relevant concepts, and provides the conceptual framework for the skill's conceivability type classification. Essential for the critical evaluation of any conceivability claim.

4. **Kripke, Saul (1980).** *Naming and Necessity.* Harvard University Press. — The locus classicus for the necessary a posteriori and the claim that conceivability can be an "illusion of contingency." Kripke argues that we can appear to conceive of something that is in fact impossible if we are ignorant of essential natures (e.g., conceiving that water is not H2O). Any conceivability argument must address the Kripkean challenge, and the skill applies this challenge as a standard check on every conceivability-to-possibility link.

5. **van Inwagen, Peter (1998). "Modal Epistemology."** *Philosophical Studies* 92(1-2): 67-84. — A prominent expression of modal skepticism. Van Inwagen argues that we have no reliable faculty for detecting metaphysical possibility, and that conceivability arguments rest on an unjustified leap from what we can imagine to what is genuinely possible. His skepticism sets the dialectical baseline: the burden of proof is squarely on the proponent of a conceivability argument. The skill uses van Inwagen's skepticism to calibrate expectations — a conceivability argument must do serious work to overcome the skeptical baseline.

6. **Gendler, Tamar Szabo and John Hawthorne, eds. (2002).** *Conceivability and Possibility.* Oxford University Press. — The standard anthology collecting the major positions in the debate, including contributions from Chalmers, Yablo, Bealer, and others. This volume provides the landscape against which specific arguments are located: which positions in the debate does the argument align with, and which objections is it vulnerable to?

7. **Balog, Katalin (1999). "Conceivability, Possibility, and the Mind-Body Problem."** *Philosophical Review* 108(4): 497-528. — Critiques the zombie argument by arguing that the conceivability of zombies is an artifact of our phenomenal concepts, not a guide to metaphysical possibility. The "phenomenal concept strategy" is a key objection that any zombie argument must address. The skill uses Balog's framework as a standard check for zombie-specific arguments.

## Steps

### Step 1: Reconstruct the Conceivability Chain

Extract the full conceivability argument from the reconstructed argument structure and represent it as a numbered sequence of explicit links:

1. **Identify the conceivability premise:** What exactly is claimed to be conceivable? Extract the exact proposition or scenario. Be precise: "zombies are conceivable" is ambiguous between "the concept 'zombie' is coherent" and "I can imagine a zombie scenario." Disambiguate based on the text.

2. **Identify the possibility bridge:** What type of possibility is claimed to follow? Logical possibility, metaphysical possibility, conceptual possibility, physical possibility? This distinction is crucial — some arguments only need conceptual possibility, others need full metaphysical possibility. The modal analysis report from `phil-modal-arg` should have clarified this; verify and apply.

3. **Identify the conclusion premise:** What metaphysical thesis follows from the possibility claim? Does possibility entail the conclusion, or is there a further inference step?

4. **Number each link L1, L2, L3, ..., Ln** as a conditional or inferential step. Each link should be a single, well-formed claim that can be evaluated independently.

5. **Surface suppressed premises:** Are there implicit premises needed to make the chain valid? For example, "if zombies are possible, physicalism is false" requires the suppressed premise that "physicalism entails the metaphysical necessity of phenomenal-physical supervenience." Make these explicit for evaluation.

6. **Check for alternative formulations:** Is the same argument presented in different forms (e.g., both as a reductio and as a direct argument)? Note any differences that might affect evaluation.

7. **Distinguish explicit from implicit links:** The chain representation should distinguish what the argument explicitly states from what it implicitly assumes. An argument may state "zombies are conceivable" and move directly to "physicalism is false" — the implicit links must be surfaced.

The output of this step is a clean, numbered chain representation ready for Step 3's evaluation.

### Step 2: Classify Conceivability Type

Examine the conceivability premise and classify the type of conceivability being claimed. This classification determines the force of the premise:

**Prima Facie Conceivability** (weakest): P seems conceivable on initial reflection. No systematic effort to rule out hidden contradiction. Almost any proposition that does not wear its inconsistency on its face is prima facie conceivable. Provides almost no evidence for possibility — the history of philosophy is replete with things that seemed conceivable but turned out impossible (e.g., squaring the circle by Euclidean construction, a solid iron bar floating on water).

**Negative Conceivability:** P cannot be ruled out a priori. Some effort has been made to detect inconsistency. But limited by the subject's conceptual resources — inability to detect contradiction may reflect ignorance rather than genuine coherence (Kripke: Hesperus ≠ Phosphorus is negatively conceivable but metaphysically impossible).

**Positive Conceivability** (scenario-based): The subject can coherently imagine a scenario in which P is true. The scenario is described in some detail and is internally coherent. Stronger than negative because it requires positive construction, not merely absence of detected contradiction. But still limited — the scenario may be coherent only because it omits relevant details.

**Ideal Positive Conceivability** (Chalmers's gold standard): P is positively conceivable under ideal rational reflection — after considering all relevant a posteriori information, performing all necessary inferences, and achieving maximal rational coherence. The strongest type. The question is whether any actual human achieves ideal rationality; claims of ideal conceivability require careful defense.

**Evidence required for classification:**
- What language does the author use? "Seems conceivable," "I can imagine," "cannot be ruled out a priori," "under ideal reflection"?
- What effort is made to establish conceivability? Is a scenario described in detail? Is there engagement with objections?
- Does the author distinguish between types, or use "conceivable" generically? If generic, flag the ambiguity.

**Classify and document:** State the classified type with textual evidence. Note whether the type is appropriate for the argument's ambitions (e.g., an argument needing ideal conceivability but only providing prima facie evidence has a type-mismatch problem). Note any controversy — do other philosophers dispute that P is conceivable in this sense?

### Step 3: Evaluate Each Link

Perform a detailed, independent evaluation of each link in the conceivability chain:

**Link L1: Conceivability to Possibility (the Core Link):**

*Kripke's Necessary A Posteriori Challenge:*
- State the challenge: some truths are necessary but knowable only a posteriori. We can conceive their negation but this is illusion, not evidence of possibility.
- Apply to target case: Does the target proposition involve natural kind terms or other terms whose essential natures might be opaque to us? For zombie arguments: is the essential nature of "consciousness" partially hidden, such that we might conceive its absence only because we don't fully grasp what consciousness is?
- Assess whether the author engages this challenge and how. Do they argue phenomenal concepts reveal essence directly? Do they appeal to two-dimensional semantics to defuse it?
- Rate: Solid (challenge adequately addressed), Adequate (addressed but some worries remain), Questionable (addressed inadequately), Broken (challenge is fatal and unaddressed).

*The Genuine Conceivability Question:*
- Is the conceivability "genuine" (tracking real modal structure) or merely "apparent" (produced by misdescription or conceptual confusion)?
- What test distinguishes genuine from apparent conceivability? If no test is provided, note the gap.
- For zombie arguments: the phenomenal concept strategy (Loar, Papineau, Balog) holds that phenomenal concepts create an illusion of a gap. If the author does not engage this, flag it.

*Two-Dimensional Semantics Defense (if applicable):*
- Primary intension (a priori, conceptual) vs. secondary intension (a posteriori, metaphysical).
- Ideal conceivability of P implies P's primary intension is possible. Under right conditions, this entails secondary (metaphysical) possibility.
- Evaluate whether the two-dimensional framework is correctly applied and whether conditions for the primary-to-secondary entailment hold.
- Rate: Solid / Adequate / Questionable / Broken.

*Completeness Challenge:*
- Can the scenario be fully specified without underdescribed placeholders?
- For zombie arguments: can a complete physical description be specified such that we can verify physical identity? If the description is schematic ("all the same physical facts"), the conceivability claim is underdetermined.

*Overall L1 Rating:* Solid / Adequate / Questionable / Broken with integrated justification.

**Link L2: Possibility to Conclusion (the Entailment Link):**

- Does the possibility of X entail the falsity of Y? Is this entailment logically valid and supported?
- For zombie arguments: zombie possibility entails physicalism is false only if physicalism requires necessary phenomenal-physical supervenience. State this explicitly. Type-B materialists (Block, Stalnaker) accept the epistemic gap but deny the ontological gap. If the author does not address Type-B materialism, note as a gap.
- Strength check: is the conclusion as strong as the argument claims? "Physicalism is false" vs. the weaker "physicalism is not conceptually necessary" — if the argument moves to the stronger claim without justification, this is overclaiming.
- Rate: Solid / Adequate / Questionable / Broken.

**Intermediate Links:** If more than two links, evaluate each for logical validity, hidden premises, and counterexamples.

**Link-by-Link Summary Table:**

| Link | Description | Rating | Key Issue |
|------|-------------|--------|-----------|
| L1 | Conceivability to Possibility | [rating] | [one-line summary] |
| L2 | Possibility to Conclusion | [rating] | [one-line summary] |

### Step 4: Conduct Gap Analysis

Go beyond link-by-link evaluation to assess the architecture of gaps:

**Identify the weakest link:** Which link has the lowest rating? This is where the argument is most vulnerable.

**Assess gap bridgeability:**
- **Unbridgeable gaps** (fatal): The inference is impossible to support within the argument's framework. Example: the argument requires ideal positive conceivability but no finite subject can achieve ideal rationality. The gap is principled, not merely evidential.
- **Bridgeable gaps** (potentially fixable): The inference needs more support, and that support could in principle be provided. Example: the argument claims positive conceivability but only provides prima facie evidence; a more detailed scenario could bridge the gap.
- **Dialectically bridgeable gaps:** The gap exists only given certain contested assumptions. A Chalmersian might find the argument compelling; a Kripkean would not.

**Cumulative gap assessment:** Even if each link is only Weak rather than Broken, the cumulative effect of multiple weak links can make the overall argument untenable. Assess whether gaps compound (each further weakens the next link) or are independent.

**Framework-internal vs. framework-external gaps:**
- Internal: The argument's own commitments generate a gap (e.g., claiming S5 but using an inference valid only in S4).
- External: General philosophical challenges that apply to all conceivability arguments (e.g., the Kripkean challenge is external).

**Gap severity ranking:** List gaps in order of severity (most damaging first), with a one-sentence description of each and whether the rest of the argument survives if the gap is conceded.

### Step 5: Assess Modal Framework

Evaluate the modal logic and semantics the argument employs (explicitly or implicitly):

**S4 vs. S5:**
- S4: accessibility is reflexive and transitive. ◇□P to □P is NOT valid.
- S5: accessibility is an equivalence relation. ◇□P to □P IS valid. All possible worlds accessible from all others.
- Which system does the argument need? Chalmers's argument often needs S5 to collapse iterated modalities. If the argument needs S5 but only S4 is justified, flag this. S5 is controversial for metaphysical modality — some reject universal accessibility.

**Accessibility Relation:**
- What kind of accessibility: logical, conceptual, metaphysical, physical?
- Check for mixed accessibility: Some arguments slide between different relations (e.g., conceivability establishes conceptual accessibility but conclusion requires metaphysical accessibility). Flag any slides.

**Iterated Modalities:**
- Does the argument use □◇P or ◇□P? Common in conceivability arguments.
- Is the iterated modality properly motivated? The inference from "I can conceive P from my actual epistemic position" to "P is possible from every metaphysically possible world" is non-trivial.

**De re vs. De dicto:**
- Does the argument involve de re modality (about a specific object) or only de dicto (about a proposition)?
- De re modal claims are more contentious because they require cross-world identity. If the argument moves from de dicto conceivability to de re conclusions, flag the gap.

**Modal Framework Rating:**
- Explicit and consistent: Solid foundation.
- Implicit but reconstructable: Adequate.
- Ambiguous or inconsistent: Problematic — flag.
- Missing: No modal framework specified, usage too loose to reconstruct. Fatal for rigorous evaluation — downgrade confidence in all ratings.

### Step 6: Determine Overall Strength Rating

Synthesize all evaluations into a holistic rating:

**Strong:** Every link Solid. No unbridgeable gaps. Conceivability type appropriate and well-supported. Modal framework explicit and correctly applied. The argument engages and defeats main objections. *Note: Strong is a high bar; most conceivability arguments fall short.*

**Medium:** Most links Solid or Adequate. Identified gaps are bridgeable. The argument is dialectically serious — it engages major objections even if it does not decisively defeat all of them. The core inference is defended, though not uncontroversially.

**Weak:** At least one key link Questionable, or multiple minor gaps cumulatively undermine the argument. The argument has identifiable weaknesses a well-informed critic could exploit. It is not compelling as it stands, though it may have value as a "promissory note."

**Broken:** At least one link Broken with an unbridgeable gap. The argument fails on its own terms, or rests on an assumption demonstrably false or incoherent. Further work cannot salvage it — replacement, not repair, is needed.

**Justification Paragraph:** A full paragraph explaining the rating, referencing specific strengths and weaknesses. This paragraph should be usable as a standalone summary judgment.

### Step 7: Compile Report

Assemble the final Conceivability Argument Analysis Report:

1. **Header:** Title, target argument identifier, date of analysis, skill version.
2. **Executive Summary:** One-paragraph overview — what the argument claims, what the analysis finds, overall rating.
3. **Chain Reconstruction:** The numbered link sequence from Step 1, clearly formatted.
4. **Conceivability Type Assessment:** From Step 2, with textual evidence and type-appropriateness assessment.
5. **Link-by-Link Evaluation:** From Step 3, with the summary table and detailed evaluations for each link.
6. **Gap Analysis:** From Step 4, with bridgeability assessment and severity ranking.
7. **Modal Framework Assessment:** From Step 5, with framework rating.
8. **Overall Strength Rating:** From Step 6, with full justification paragraph.
9. **Dialectical Context Note:** How this argument fits into the broader debate and what the analysis implies for that debate.
10. **Recommendations:** If Weak or Broken, what would be needed to strengthen it? If Strong or Medium, what are remaining vulnerabilities?

## Quality Criteria

1. **Gap Transparency:** Every link in the conceivability chain is individually evaluated. No link gets a free pass. The rating for each link is justified with specific reasoning, not gestural judgment. A reader should see exactly where the analyst thinks the argument succeeds or fails. The analysis does not treat the conceivability-to-possibility move as a black box — it opens the box and evaluates each component.

2. **Conceivability Precision with Evidence:** The conceivability type is classified with precision and supported by textual evidence. The analysis distinguishes between "the author says they can conceive X" and "the author has established that X is genuinely conceivable in a sense that supports possibility." If the author uses "conceivable" loosely, the ambiguity is flagged and explored rather than resolved by analyst fiat.

3. **Modal Framework Explicitness:** The modal logic (S4/S5), accessibility relation, and possible-worlds framework are explicitly identified and evaluated. If the argument does not specify its modal framework, this is flagged as a deficit. Inferences that depend on specific modal axioms (especially S5) are identified and the justification for those axioms is checked.

4. **Dialectical Fairness (Principle of Charity):** The analysis presents the strongest version of the argument, not a straw man. If there is a well-known defense of an apparently weak link (e.g., Chalmers's defense of the primary-to-secondary possibility inference), that defense is engaged. The goal is to evaluate the argument at its best, not its worst. But the analysis does not supply premises the argument's proponent would reject.

5. **Two-Dimensional Awareness:** For Chalmers-style arguments, the two-dimensional semantic framework is understood and applied. The distinction between primary and secondary intensions is respected. The analysis does not collapse two-dimensional arguments into one-dimensional conceivability claims. The conditions under which primary possibility entails secondary possibility are evaluated specifically.

6. **Kripkean Literacy:** The Kripkean challenge (necessary a posteriori, illusion of contingency) is applied where relevant. The analyst understands that the necessary a posteriori is the central challenge to conceivability arguments and evaluates whether the argument meets that challenge or is defeated by it. The analysis identifies whether the target proposition might involve an essentialist identification opaque to a priori reflection.

7. **Bridgeability Discrimination:** The gap analysis distinguishes between gaps that are fatal (unbridgeable) and gaps that indicate incomplete work (bridgeable). Not all weaknesses are equal — some can be fixed with further argument; others are cracks in the foundation. This distinction is crucial for revision recommendations.

8. **Cumulative Assessment:** The overall rating reflects the interaction of the links, not just a mechanical average. An argument with two Weak links may be Broken if the weaknesses compound; an argument with one Weak link may be Medium if that link is not load-bearing. The analysis explains how the links interact.

9. **Type-B Physicalism Awareness:** For zombie arguments and related anti-physicalist conceivability arguments, the analysis addresses whether the argument challenges only Type-A physicalism (a priori) or also Type-B physicalism (a posteriori). The distinction between these two forms of physicalism is essential for evaluating the argument's force correctly.

## Relations to Other Skills

### Dependencies (Required Inputs)
- **`phil-modal-arg`** (strong dependency): The modal argument analysis provides the formal modal framework — operators, accessibility relations, possible-worlds semantics, axiomatic commitments. Without this, the conceivability analysis cannot evaluate whether the modal moves are formally valid. The conceivability-to-possibility inference is a bridge from the epistemic to the modal; the modal side of the bridge requires the modal framework.
- **`phil-argument-reconstruct`** (strong dependency): The argument reconstruction provides the logical skeleton — premises, conclusions, inference patterns. The conceivability chain must be extracted from this reconstruction. Without it, the analyst must reconstruct the argument from scratch, which is error-prone and defeats the modular architecture.

### References (Read-Only Knowledge Resources)
- **`modal-logic-primer.md`**: Reference for S4/S5, accessibility relations, iterated modalities, and possible-worlds semantics. Consult for evaluating the formal modal structure.
- **`argument-forms/conceivability-argument.md`**: Reference on the standard form of conceivability arguments, common variants (Cartesian, zombie, ontological), and typical objections. Provides schemas that the target argument can be compared against.

### Dependents (Skills That Use This Output)
- **`phil-essence-detect`**: Essentialist arguments often interact with conceivability arguments. If the conclusion of a conceivability argument is that "the essence of consciousness is non-physical," the essence detection skill uses this analysis to determine whether that essence claim is well-supported. Conversely, essentialist commitments may constrain what is conceivable.
- **`phil-argument-strength`**: The overall argument strength rating uses the conceivability analysis output as one input (the conceivability chain is often the load-bearing inference in a larger argument).
- **`phil-rebuttal-audit`**: The rebuttal audit uses the gap analysis to generate targeted rebuttals — each identified gap becomes a potential line of attack.

### Coordination Notes
- When run after `phil-modal-arg`, use the modal framework specification to populate Step 5. Do not re-analyze the modal framework from scratch — verify and apply.
- When run before `phil-essence-detect`, ensure the conceivability-to-essence inference (if any) is evaluated: does the argument establish an essence claim, or only a possibility claim that might support an essence claim under further assumptions?
- If the target argument is part of a larger anti-physicalist argument, coordinate with the broader analysis: the conceivability argument may be one pillar among several (knowledge argument, explanatory gap).
- For historical arguments (Descartes), adjust vocabulary to avoid anachronism while applying the same structural framework.

## Boundary Conditions

### When to Skip
- **No conceivability argument present:** If the argument does not involve a conceivability-to-possibility inference, terminate with a note: "No conceivability-based reasoning detected in this argument." Do not invent conceivability where it does not exist. An argument using modal operators without invoking conceivability (e.g., direct modal argument from essence to necessity) is not a conceivability argument.
- **Conceivability as minor premise:** If conceivability is mentioned in passing but not load-bearing for the argument's conclusion, perform a limited analysis — classify the conceivability type but do not perform the full link-by-link evaluation. The report should state: "Conceivability plays a minor role — analysis limited to type classification only."
- **Purely epistemic argument:** If "conceivable" is used in the epistemic sense ("I can imagine" without any modal conclusion), this is not a conceivability argument in the metaphysical sense. Skip or provide a one-paragraph note: "Conceivability is epistemic only; no modal inference drawn."

### When to Adjust Scope
- **Zombie-specific arguments:** Devote special attention to the "genuine conceivability" question and the phenomenal concept strategy. Add a dedicated "genuine conceivability deep-dive" evaluating whether zombies are genuinely conceivable or merely seem so. Add a "physicalism entailment deep-dive" examining exactly which formulation of physicalism is targeted. These deep-dives are mandatory for zombie arguments.
- **Conceivability as heuristic:** If the author uses conceivability as a heuristic (="I find it conceivable, which gives me some reason to think it's possible, but I don't claim entailment"), apply a lighter touch. Classify the conceivability type and assess heuristic value, but do not perform the full seven-step evaluation.
- **Historical conceivability arguments** (Descartes, Hume): Adjust for historical context — Descartes did not have access to Kripke or Chalmers. Evaluate within the historical framework but note modern objections as "retrospective challenges." Do not penalize historical authors for failing to anticipate 20th-century modal epistemology.
- **Cross-cultural conceivability claims:** If the argument involves cross-cultural or cross-linguistic conceivability claims ("X is conceivable in framework Y but not in Z"), note the perspectival nature of the conceivability claim. Conceivability is relative to conceptual resources.

### Domain-Specific Guidance
- **Philosophy of Mind (zombie arguments):** Central question: are phenomenal concepts "special"? Do they reveal essence directly (Chalmers) or merely present a mode of presentation concealing physical essence (phenomenal concept strategy)? The analysis must engage this debate.
- **Philosophy of Religion (ontological arguments):** Conceivability of God used to argue for God's possibility, which (with the ontological argument) entails actuality. Apply standard criteria but note the specific theological context.
- **Modal Epistemology (metaphilosophy):** If the argument is itself about modal epistemology (e.g., "conceivability is a reliable guide"), the analysis is meta-level — evaluating the argument about modal epistemology, not a first-order conceivability argument.

### Edge Cases
- **Self-undermining arguments:** An argument concluding "conceivability is NOT a guide to possibility" that itself uses a conceivability inference is self-undermining. Flag explicitly.
- **Conceivability of contradictions:** If the argument claims a logical contradiction is conceivable (dialetheism), this departs from standard assumptions that contradictions are not conceivable. Flag and analyze accordingly.
- **Cross-world conceivability:** If the subject conceives of a scenario from the perspective of another possible world, check whether the modal framework supports cross-world conceivability.

## ARS Interface

### Role in ARS
This skill provides the **conceivability argument evaluation** that ARS uses to assess whether a paper's central modal inference is sound. The conceivability-to-possibility inference is frequently the linchpin of anti-physicalist arguments, dualist arguments, and modal arguments in metaphysics. ARS needs a systematic, repeatable evaluation of this inference to inform its overall assessment.

### Information Provided to ARS
1. **Chain Integrity Assessment:** A clear report on whether each link holds, with specific reasoning. ARS uses this to determine whether the paper's central argument is compelling.
2. **Identified Gaps:** Precise identification of where the argument fails. ARS reviewers can say "the argument fails at the transition from negative conceivability to genuine possibility" rather than "the argument seems weak."
3. **Bridgeability Assessment:** Whether gaps can be fixed — determines whether ARS recommends "revise and resubmit" (bridgeable) or "reject" (unbridgeable).
4. **Dialectical Positioning:** Where the argument stands relative to existing literature — does it engage main objections? Informs assessment of scholarly quality.
5. **Strength Rating:** Summary metric integrated into overall paper evaluation.

### How ARS Uses This Output
- **Main Argument Evaluation:** If the central argument is a conceivability argument, this is the core of ARS's evaluation. A Broken or Weak rating may suffice for rejection; Medium or Strong invites further analysis.
- **Critical Review Generation:** The gap analysis provides specific, well-justified criticisms. ARS can say "the transition from negative conceivability to metaphysical possibility requires the S5 axiom, which is not defended and is controversial."
- **Comparative Assessment:** When reviewing multiple papers with conceivability arguments, structured output enables comparison: "Paper A's zombie argument is Medium (positive conceivability with two-dimensional defense); Paper B's is Weak (only prima facie conceivability without modal framework)."
- **Revision Recommendation:** If gaps are bridgeable, ARS recommends targeted revisions for specific links.
- **Triage:** For otherwise competent papers with a Broken central conceivability inference, ARS quickly identifies the paper as not salvageable.

### ARS-Specific Output Adjustments
When invoked in ARS mode, the output should include:
- **ARS Summary Box:** A standalone paragraph an ARS reviewer can drop directly into their review (e.g., "The paper's central zombie conceivability argument is evaluated as Weak. The core link from positive conceivability to metaphysical possibility is questionable because...").
- **ARS Verdict Options:** Three possible verdicts clearly stated: (1) Argument compelling as is; (2) Argument needs revision but potentially compelling; (3) Argument unsalvageable.
- **ARS Reviewer Recommendations:** Specific, actionable feedback: "The author should either: (a) defend S5 for metaphysical modality, or (b) reformulate the argument to avoid reliance on S5."

### Feedback Loop from ARS
- **Target Venue Context:** If ARS provides journal context, standards adjust. A mind-journal article arguing against Chalmers must engage the full two-dimensional framework; a general journal article may be held to a lower standard.
- **Reviewer Expertise:** If ARS indicates specific reviewer expertise (e.g., modal skeptic), analysis can highlight issues that reviewer would press.
- **Comparative Benchmarks:** ARS may supply benchmarks ("this journal expects conceivability arguments to engage the phenomenal concept strategy") to calibrate expectations.
