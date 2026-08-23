# Modal Argument Analysis — checklist (conditional reference for method.metaphysics.modal-arg)

> Loaded only when the consuming mode's live ambiguity or the user's explicit request requires it; never loaded by default with the method file.

# Modal Argument Analysis Quality Checklist

> After each modal argument analysis, check each item. A fully checked list indicates a high-quality modal analysis report.

---

## Modal Operator Detection

- [ ] **All modal terms captured**: Every occurrence of possibility (possible, could, might), necessity (necessary, must), contingency (contingent, not necessary), impossibility (impossible), and conceivability (conceivable) vocabulary has been located with original-text citations.
- [ ] **Modal type discriminated**: Each modal claim is classified as logical, metaphysical, physical/nomological, or conceptual modality — not all lumped under a generic "modal" label.
- [ ] **Operator logical form annotated**: Each modal operator is mapped to its logical symbol — ◇ for possibility, □ for necessity, ¬◇ for impossibility, ◇p ∧ ◇¬p for contingency.
- [ ] **Implicit modality detected**: Where the argument's structure implies a modal claim without explicit modal vocabulary (e.g., counterfactual conditionals implying possibility), this is flagged with Low confidence.
- [ ] **Conceivability distinguished from possibility**: Conceivability terms are flagged for special handling and not silently treated as equivalent to possibility operators, per the No Leaping Principle.

## Scope Resolution

- [ ] **De dicto vs. de re reading generated**: For every modal claim involving a quantified expression, both the de dicto reading (□∃x(Fx)) and the de re reading (∃x□(Fx)) are explicitly generated and compared.
- [ ] **Wide vs. narrow scope alternatives generated**: For modal claims with temporal or other operators, all plausible scope permutations are listed before determining the intended reading.
- [ ] **Author's intended scope identified**: The interpretation most consistent with the author's argumentative context is identified, with textual justification — not merely assumed from surface syntax.
- [ ] **Scope ambiguity impact assessed**: Where scope indeterminacy could affect argument validity, this is recorded as a modal scope gap with an explanation of how each reading changes the conclusion.
- [ ] **Nested modal operators resolved**: Where one modal operator falls within the scope of another (e.g., "possibly necessarily P"), the nesting is explicitly diagrammed and its implications traced.

## Modal System Assessment

- [ ] **Implicit modal system identified**: The modal logical system the argument implicitly assumes — K, T, S4, S5, or B — is identified with justification grounded in the argument's modal moves.
- [ ] **System axioms checked against argument**: The key axiom of the attributed system (K: distribution; T: necessity entails actuality; S4: □p → □□p; S5: ◇p → □◇p; B: p → □◇p) is checked against the argument's actual use.
- [ ] **Rival system challenge assessed**: If a reader holding a different modal system (e.g., S4 rather than S5) would reject a crucial step, this vulnerability is recorded with explanation.
- [ ] **System attribution not overclaimed**: The analysis does not attribute a specific modal system when the argument's modal reasoning is too informal to support such attribution — the framework is used diagnostically, not imposed.
- [ ] **Accessibility relation characterized**: The accessibility relation between worlds that the argument assumes — reflexive, transitive, symmetric, or Euclidean — is described, in technical terms or plain-language paraphrase.
- [ ] **Framework Transparency Principle satisfied**: The argument's implicit modal system and axiomatic assumptions are made explicit, per the Quality Criteria.

## Conceivability Check

- [ ] **Conceivability type identified**: The kind of conceivability at work — prima facie, ideal, logical, or physical — is identified, not left as an undifferentiated "conceivable."
- [ ] **Claimed possibility type identified**: The type of possibility the argument concludes to — logical, metaphysical, physical, or conceptual — is explicitly stated.
- [ ] **Conceivability-possibility gap assessed**: The degree of support the conceivability type provides for the claimed possibility type is evaluated. A mismatch (e.g., weak prima facie conceivability supporting a strong metaphysical possibility claim) is flagged as a violation.
- [ ] **Chain strength rated with justification**: The conceivability-to-possibility chain is rated (Strong / Medium / Weak / Broken) with a paragraph of explanation — not a bare label.
- [ ] **Yablo-style objections considered**: Following Yablo (1993), whether the conceivability might be due to the subject's failure to fully grasp the scenario (as opposed to genuine possibility) is considered.
- [ ] **No-leaping principle enforced**: Every step in the modal reasoning chain is independently tested — no jumping directly from "conceivable" to "necessary" or "impossible" without intermediate analysis.

## Possible-Worlds Semantics

- [ ] **Base world and target world identified**: For arguments involving possible-worlds reasoning, the base world (actual world) and each target world hypothesized are explicitly named and described.
- [ ] **Accessibility relation justified**: The grounds on which the target world is claimed to be accessible from the base world are examined — is it logical structure, shared natural laws, shared essences, or something else?
- [ ] **Counterpart theory vs. trans-world identity noted**: Where cross-world identity is at stake, whether the argument presupposes counterpart theory or strict trans-world identity is flagged — these have different modal implications.
- [ ] **Recombination principle checked**: If the argument uses the principle that any recombination of distinct entities yields a possible world, the limits of this principle are assessed and over-application flagged.
- [ ] **Two-dimensional semantics considered**: Where the necessary a posteriori or contingent a priori is relevant, Chalmers/Jackson-style two-dimensional analysis is applied to check whether the modal claim survives epistemic scrutiny.

## Modal Fallacy Detection

- [ ] **Necessity-distribution fallacy checked**: Any move from "Necessarily(P ∨ Q)" to "Necessarily(P) ∨ Necessarily(Q)" — or similar distribution errors — is flagged as a modal scope fallacy.
- [ ] **Barcan formula issues flagged**: Where quantified modal logic is in play, any implicit reliance on the Barcan formula (◇∃xFx → ∃x◇Fx) or its converse is flagged.
- [ ] **Rigid/non-rigid designation conflated**: If the argument treats a non-rigid designator as rigid (or vice versa) in a modal context, this conflation is identified.
- [ ] **Essentialist leaps detected**: Moves from "X is necessarily F" to "F is essential to X" without justification are flagged, as are moves from "X is contingently F" to "F is accidental to X."
- [ ] **Necessity-of-identity issues flagged**: Where identity claims are embedded in modal contexts, whether the argument respects the necessity of identity (a=b → □(a=b)) is checked — violations or unstated dependencies flagged.
- [ ] **Ordinary vs. technical modal distinguished**: Ordinary modal pragmatics (e.g., epistemic "might" or deontic "must") are not subjected to full S5 analysis unless the argument's core depends on them — technical frameworks are used judiciously.

## Report Quality

- [ ] **Executive summary present**: A one-paragraph overview covers modal argument salience, most critical modal operator, key scope ambiguity (if any), and overall modal framework assessment.
- [ ] **Modal operators table complete**: The operators table includes Location, Term, Type, and Potential Issue for every modal expression found in the argument.
- [ ] **Scope analysis detailed**: For each ambiguous modal claim, all plausible readings are presented and the intended reading is argued — not merely asserted.
- [ ] **Framework analysis justified**: The implicit modal system attribution includes the basis for the attribution and any challenges from rival systems.
- [ ] **Overall assessment actionable**: The final assessment identifies the 2-3 most significant modal issues (gaps, scope ambiguities, framework problems) and explains their impact on the argument's validity.
