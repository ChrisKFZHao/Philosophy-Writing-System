---
id: method.argument.analogy-check
package: argument
legacy_ids: [phil-analogy-check]
label: Analogy Check
consumers: [phil-research/evaluate, phil-write, phil-review]
selector: feature-detected
side_effects: read-only
---

# Analogy Check (method.argument.analogy-check)

> Execution card. Follow it as the complete procedure. Load `references/analogy-check-full.md` only when the card does not settle a live ambiguity.

## Use when
- An argument infers an unobserved property in T from similarities to S.
- You must grade force or prepare proponent/respondent guidance.
- Not for bare comparisons, metaphors, tautologies, or sourceless analogies.

## Inputs
- Required: argument reconstruction (method.argument.argument-reconstruct): premises, conclusion, classification; ideally S, T, shared properties, projected P*. Extract missing elements in Step 1.
- Optional: original text; conceptual analysis (concept.conceptual-analysis); `fallacy-catalog.md`; dialectical map (dialectic.dialectical-map); `analogy.md`.
- Priority: `analogy.md`, original text, conceptual analysis (Step 3), fallacy entry (Step 4), dialectical map (Step 7); note unavailable inputs.

## Procedure

**1. map source–target correspondences**
- Tabulate cited S items → T counterparts; flag missing counterparts.
- Weight (Gentner): O entities < A monadic properties < R1 first-order relations (primary) < R2 relations among relations (greatest).
- Keep P* apart from shared; P* as shared = circularity/question-begging.
- Verify via `analogy.md`; exclude example/precedent.

**2. classify the analogy type**
- Hesse, exhaustive: positive (shared) / negative (differing) / neutral (unknown in T, incl. P*); one per S property.
- illustrative (clarifies a known feature, no knowledge claim, exempt prior association, zero force) vs argumentative (novel conclusion); flag mismatch.
- a priori (conceptual/definitional/logical, armchair) vs empirical (contingent causal/statistical/nomological) (Keynes).
- formal (structural isomorphism, no substantive tie to P*) vs material (nomologically/causally connected cluster licensing inference) (Hesse); material > formal.
- Pitfalls: context ≠ function; no evidence ≠ a priori (in-principle evaluability; empirical without evidence = finding); categories ≠ formal.
- Unclean → state why.

**3. evaluate the relevance of shared properties**
- Bartha: in S, is a connection shared properties→P* established?
- Types: causal (cause/mechanism of P*); definitional/conceptual (entailed eo ipso); functional (function manifested as P*; isomorphism warrants it); statistical (correlation; representative S).
- None → fails; force severely diminished regardless of count or vividness; "no known" (remediable) vs "no conceivable" (fatal); not automatically a fallacy.
- Satisfied → state the principle; grade: established law / robust defeasible generalization / plausible contested hypothesis / merely conceivable; it bounds strength.
- Illustrative → accuracy vs source-artifact distortion; misleading fails even if vivid.

**4. detect and assess disanalogies**
- Relevant iff it interacts with the Step 3 principle to undermine/block/query the projection; orthogonal = irrelevant, note only.
- defeating: severs causal/conceptual/probabilistic link; no support; repair: new source/pathway or abandon the conclusion.
- weakening: lowers probability/narrows scope, no sever; repair by qualification ("probably", "in most cases"), independent evidence, or concede + remainder suffices.
- Trace the exact broken link; vague "important ways" insufficient.
- Judge responses to anticipated disanalogies.
- Defeating → `fallacy-catalog.md`: foreseeable + suppressed/ignored → suppressed disanalogy; record under fallacy cross-reference.
- Search: negative analogy → filter relevance → counterfactual (T shared it → stronger? genuine if yes, dissimilarity if no).
- Structural: S higher-order relation (feedback loop, hierarchy, symmetry) absent in T while P* depends on it; more severe.

**5. construct a counter-analogy audit**
- Walton CQ4: equally similar case with P* false?
- S' shares cited properties but lacks P* (or is inconsistent).
- Plausibility (genuine? stretched = dismiss); relevance (same pathway? S''s own disanalogy absent S–T); burden (principled distinction? none = suspect).
- Judge any rejection of competitors.
- Same abstraction; discount higher/lower.
- Symmetry: mutual undermining → neither decisive; dispute = which case captures T's features.
- Diversity: independent counters stronger; cross-case false conclusions = unreliable.
- Strong = counters fail sharing or self-undermine; weak = plausible parallel without contrivance.

**6. assess argumentative force**
- One grade, justified, weighting visible; no averaging or inflation/skepticism.
- **Compelling**: near-deductive; principle entails/near-entails P*; no defeating disanalogy or plausible counter.
- **Strong**: substantial; well-established causal/conceptual link; weakening minor; counters implausible/distinguished.
- **Moderate**: some weight, defeasible; partial prior association, significant weakening, or plausible counter.
- **Weak**: minimal/suggestive; prior association unclear or near-defeating; no credence update.
- **Merely Rhetorical**: persuasion only; vague mapping, irrelevant properties, or unaddressed defeating disanalogy; no loss if omitted.
- One failure overwhelms; factors, descending: prior association (failure caps Weak); one defeating disanalogy → Merely Rhetorical/Weak by foreseeability/addressability; depth R2>R1>attribute (Gentner systematicity); number/variety (Mill's known-shared fraction; Keynes's diverse aspects); counters.
- Illustrative → "N/A – illustrative" (clarity, accuracy, no distortion); note confidence and trade-off range.

**7. formulate dialectical recommendations**
- Argument-specific.
- Proponent: unmet prior association → name establishing evidence (causal, conceptual, statistical); weakening → qualify without abandoning core; illustrative-as-argumentative → relabel + supplement or establish prior association; strong → state principle, preempt disanalogies; weak/rhetorical → abandon, restrict scope, and acknowledge limits.
- Respondent, efficiency: defeating disanalogy (one difference vs whole map); else prior association (fails even in S); weak → dismiss with the specific failure, no burden; plausible counter-analogy → primary, proponent must distinguish.
- Burden: strong/compelling shifts some (respondent must cite a disanalogy or challenge the principle; state what discharges it); weak/rhetorical: none, proponent bears all.
- Larger strategy (multi-pronged, objection reply); use dialectical map.

## Required output
1. **analogy summary** — S, T, conclusion, key mapping, qualifications/scope.
2. **source–target mapping table** — correspondences by object, property, first-order, higher-order; P*; contested; relational weight.
3. **analogy type classification** — illustrative/argumentative; a priori/empirical; formal/material; positive/negative/neutral.
4. **relevance assessment** — principle (causal/definitional/functional/statistical) and strength, or none; illustrative: accuracy.
5. **disanalogy detection and impact analysis** — each difference defeating/weakening/irrelevant, with broken link.
6. **counter-analogy audit** — ≥1 counter-analogy; plausibility and relevance; robustness test.
7. **argumentative force assessment** — Compelling / Strong / Moderate / Weak / Merely Rhetorical, justified by the five factors; "N/A – illustrative" if applicable.
8. **fallacy cross-reference** — single similar instance, suppressed disanalogy, faulty comparison, misleading vividness; weak vs fallacious.
9. **dialectical impact and recommendations** — proponent moves, respondent attacks, burden shifts, strategic role.

## Boundary rules
- Non-analogical comparison (no further-similarity inference): out of scope. Pseudo-analogical: flag, defer to argument-reconstruct. Degree/proportion: reclassify (a fortiori, proportion).
- Metaphor: extract only object/property/relational mappings + P*; if indeterminate, defer to conceptual-analysis or rhetorical analysis. Test: truth-apt?
- Tautology: P* entailed → deductive, not ampliative; reclassify.
- No specifiable source (free-floating): stop; report; flag merely-rhetorical/vagueness fallacy; state the needed specification.
- Legal/moral normative: Step 3 must also identify the normative principle (consistency, fairness, universalizability, precedent) licensing descriptive→normative; its absence is not automatically defeating (like-cases-alike default) but must be noted; precedent authority ≠ analogical strength. Coordinate metaethics.normativity.
- Mathematical/formal: prior association may be proof/isomorphism; disanalogy = structural feature present/absent, defeating iff P* depends on it; provability in S from axioms T also satisfies under the mapping → deductive; flag crossing.
- Cross-categorical: mapping may be indeterminate; the principle may not hold uniformly; special care Steps 1, 3; guard ontological projection (source features into T); coordinate metaphysics.ontological-commitment.
- Review before Step 1; defer or reclassify rather than forcing.

## Quality bar
1. Mapping exhaustive; gaps flagged, none filled/over-attributed.
2. Classification precise, non-overlapping; mixed types disaggregated.
3. Relevance names an exact mechanism; distinguishes established/plausible/speculative/none; frameworks as tools.
4. Disanalogies traced to their pathway with justified labels; repairability noted.
5. Grade reproducible; confidence/disagreement range stated.
6. Recommendations actionable, specific; burden-shifting addressed.
7. Fallacy determination independent of grade: weak ≠ automatically fallacious.

## Conditional references
Load only on a live ambiguity or an explicit request, never by default:
- `references/analogy-check-full.md`: complete method text and theory.
- `references/analogy-check-checklist.md`: post-analysis checklist keyed to Steps 1–7 and outputs.
- `references/analogy-check-examples.md`: worked input-to-output analyses of classic analogies.
