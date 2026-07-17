<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Counterexample Construction & Evaluation Quality Checklist

> After each counterexample analysis, check each item. A fully checked list indicates a high-quality counterexample report.

---

## Attack Point & Targeting Checks

- [ ] **Argument reconstruction ingested**: The standard-form argument (premises [P1]...[Pn], conclusion [C], implicit premises [IP1]...[IPn]) has been extracted from the `phil-argument-reconstruct` report.
- [ ] **Attack priority correctly ordered**: The most vulnerable premise is identified first, followed by the highest-impact premise, followed by implicit premises — not simply attacked in textual order.
- [ ] **Target precision verified**: Each counterexample explicitly names which premise, inferential step, or conceptual boundary it targets. No counterexample attacks "the argument in general."
- [ ] **Certainty ratings referenced**: The argument reconstruction's premise-level certainty ratings have been consulted to prioritize attack points, not assumed from general impression.
- [ ] **Implicit premises not overlooked**: If `phil-premise-detect` output is available, its flagged implicit premises have been reviewed as high-value attack points.

## Counterexample Type Classification

- [ ] **Type correctly classified**: Each counterexample is classified as one of the six recognized types — Factual, Thought Experiment, Logical, Analogical, Borderline, or Vagueness — with a justification for the classification.
- [ ] **Type-argument fit**: The chosen counterexample type is appropriate for the target. For example, a factual counterexample targeting a universal empirical claim; a logical counterexample targeting a deductive inference.
- [ ] **Mixed types flagged**: If a counterexample draws on multiple types (e.g., thought-experiment with logical structure), this hybrid character is explicitly noted rather than forced into a single category.
- [ ] **Type limitations acknowledged**: Where the chosen type has known limitations (e.g., borderline counterexamples depend on controversial views of vagueness), these are flagged.

## Logical Structure & Internal Consistency

- [ ] **Contradiction-free scenario**: The counterexample's own internal description contains no logical contradiction. A counterexample that is itself incoherent is worthless.
- [ ] **Target-hit verification**: The counterexample genuinely falsifies the target premise or breaks the inferential chain — not merely a tangentially related scenario that leaves the target intact.
- [ ] **No collateral damage**: The counterexample does not inadvertently challenge premises the analyst accepts or that are independently well-supported, unless this trade-off is explicitly acknowledged.
- [ ] **Inferential chain counterexamples structurally precise**: For counterexamples targeting [P1+P2 to C], the scenario satisfies P1 and P2 but renders C false — tested formally, not just gestured at.
- [ ] **Conceptual boundary counterexamples Gettier-compliant**: For counterexamples targeting necessary/sufficient conditions, the scenario satisfies all stated conditions yet intuitively resists the concept — the Gettier template is faithfully applied.
- [ ] **Sorites/vagueness counterexamples properly structured**: If a vagueness counterexample is used, the sorites chain is explicit — the tolerance principle at work is named and the boundary problem is precisely located.

## Modal Strength Assessment

- [ ] **Modal status of the counterexample classified**: Is the counterexample merely logically possible, metaphysically possible, nomologically possible, or actually true? The modal strength is explicitly stated.
- [ ] **Modal strength matches argumentative need**: A merely logically possible counterexample may refute a claim of logical necessity, but a metaphysically possible counterexample is needed to refute a claim of metaphysical necessity — the modal bar is correctly calibrated.
- [ ] **Actual-world counterexamples flagged for extra force**: If the counterexample is an actual historical or real-world case, its elevated dialectical force (it cannot be dismissed as "merely possible") is explicitly noted.
- [ ] **Modal weakness acknowledged**: If the counterexample is only prima facie conceivable (weak modal force), this limitation is disclosed rather than the counterexample being presented as stronger than it is.

## Four-Dimension Evaluation

- [ ] **Intuitive Force rated with justification**: Each counterexample's intuitive force (Strong / Moderate / Weak) is rated, and the rating includes a justification — not merely a label.
- [ ] **Conceivability rated with justification**: Each counterexample's conceivability (High / Medium / Low / Disputed) is assessed against logical consistency and metaphysical coherence.
- [ ] **Isolation assessed**: Whether the counterexample challenges only the target premise without collateral impact on other accepted premises is rated (Good / Fair / Poor).
- [ ] **Independence assessed**: Whether the counterexample avoids dependence on a specific contested philosophical stance is rated (Yes / Partial / No). If the counterexample only works given, e.g., consequentialism or dualism, this is flagged.
- [ ] **Four-dimension conflicts noted**: Where dimensions conflict (e.g., high intuitive force but poor isolation), the trade-off is explicitly discussed rather than glossed over.

## Dialectical Anticipation

- [ ] **All five rebuttal strategies considered**: For each counterexample, the opponent's possible responses are checked against: reject the intuition, redefine the concept, distinction strategy, accept but downgrade, and crushing acceptance.
- [ ] **Rebuttal plausibility assessed**: Each anticipated rebuttal is evaluated for reasonableness — not merely listed as a formal exercise.
- [ ] **Counterexample impact recalibrated post-rebuttal**: If a rebuttal would succeed, the counterexample's downgraded impact is explicitly stated. If no plausible rebuttal exists, this is argued, not assumed.
- [ ] **Lakatosian dialectic considered**: The possibility that the opponent will "monster-bar" or "exception-bar" the counterexample (revise definitions to exclude it) is anticipated, following the Lakatos (1976) framework.
- [ ] **Dialectical closure assessed**: Whether the counterexample-rebuttal exchange reaches a stable equilibrium or remains open is explicitly noted.

## Boundary Conditions & Honesty

- [ ] **No forced counterexample**: If the argument appears entirely sound and no valid counterexample can be constructed, this is honestly reported — "No valid counterexample found" — rather than a specious one being fabricated.
- [ ] **Disputed counterexamples flagged**: If a counterexample's validity depends heavily on specific philosophical intuitions that are themselves contested, its disputed status is prominently flagged in the report.
- [ ] **Sound-argument acknowledgment**: If the argument withstands counterexample scrutiny, this positive assessment is stated clearly — the skill does not presuppose every argument has a fatal flaw.

## Report Quality

- [ ] **Executive summary present**: A concise overview covers attack priority, counterexample count and types, most effective counterexample, and overall impact on the argument.
- [ ] **Each counterexample fully described**: Scenario description, type classification, target specification, four-dimension ratings, and dialectical anticipation are all present for every counterexample.
- [ ] **Overall impact assessment clear**: The argument-level impact (Fatal / Severe / Moderate / Weak) is stated with reasoning, not merely summarizing individual counterexample ratings.
- [ ] **Textual evidence anchored**: References to the argument reconstruction report — premise numbers, certainty ratings, inferential links — are precise and traceable.
- [ ] **Dialectical tone maintained**: The report presents the target argument at its strongest before critiquing it; no straw-manning or dismissive language.
