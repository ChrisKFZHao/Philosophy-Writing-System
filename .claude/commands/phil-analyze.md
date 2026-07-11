---
description: Full Analysis Pipeline — Orchestrate all 28 Layer 1 skills into an end-to-end analytic philosophy analysis with automatic domain feature detection
---

# /phil-analyze

Loads the full analysis orchestration pipeline. Composes all 28 phil-* skills across 5 analysis phases, with automatic detection of metaphysics and metaethics domain features.

## Usage

```
/phil-analyze <text>
```

Or provide text first, then trigger with `/phil-analyze`.

## Behavior

### Phase 1: Reading & Comprehension
1. **Domain Detection**: Automatically scan the text for domain features:
   - **Metaphysics triggers**: ontological language (存在, 实体, 属性, 同一性), modal operators (必然, 可能, 偶然), identity statements, causal assertions (导致, 引起, 因为), grounding language (奠基于, 依赖于, 随附于)
   - **Metaethics triggers**: moral language (善, 恶, 应当, 对/错), normative statements (理由, 义务, 规范), realism/anti-realism claims, motivational language (动机, 欲望, 驱动)
2. Run `phil-contextualize` to situate the text within its intellectual history and debate tradition.

### Phase 2: Argument Analysis
3. Run `phil-argument-reconstruct` on each argument in the text → standard premise-conclusion form.
4. Run `phil-charity-check` on all reconstructions → verify principle of charity.
5. Run `phil-premise-detect` → surface implicit premises with certainty and rejection impact assessments.
6. Run `phil-modal-arg` → evaluate modal argument structures, scope ambiguity, and conceivability inferences.
7. **If metaphysics triggers detected**, also run:
   - `phil-ontological-commitment` → identify entity types and existence categories presupposed.
   - `phil-identity-persistence` → analyze identity conditions across time/worlds (if identity statements present).
   - `phil-conceivability-arg` → evaluate conceivability-to-possibility chains (if modal/conceivability language present).
8. **If metaethics triggers detected**, also run:
   - `phil-moral-realism` → analyze stance on realism/anti-realism spectrum.
   - `phil-normativity` → analyze source and structure of normativity.
   - `phil-moral-semantics` → analyze moral language and semantic commitments.
   - `phil-moral-psychology` → analyze judgment-motivation relation.

### Phase 3: Conceptual Analysis
9. Run `phil-conceptual-analysis` → clarify key concepts, necessary/sufficient conditions, case testing.
10. Run `phil-distinction-track` → scan, index, and analyze all conceptual distinctions; check consistency.
11. Run `phil-thought-experiment` → deconstruct any thought experiments, evaluate intuition mechanisms.
12. Run `phil-intuition-pump` → identify intuition pumps and assess framing effects.
13. **If metaphysics triggers detected**, also run:
    - `phil-grounding-check` → detect grounding, supervenience, realization relations; map ontological dependence.
    - `phil-essence-detect` → detect and evaluate essence/accident claims (Finean and Kripkean frameworks).
    - `phil-natural-kind-analyze` → analyze natural kind classification and essentialism/HPC/conventionalism commitments.
    - `phil-causation-analyze` → identify theoretical affiliations of causal claims; evaluate Humean vs. anti-Humean.
14. **If metaethics triggers detected**, also run:
    - `phil-moral-disagreement` → evaluate arguments from moral disagreement; assess conciliationist challenges.
    - `phil-moral-epistemology` → evaluate moral knowledge claims; assess intuitionist/coherentist/reliabilist pathways.
    - `phil-moral-supervenience` → analyze moral-to-natural supervenience; evaluate Blackburn's challenge.

### Phase 4: Critical Evaluation
15. Run `phil-counterexample` → generate and evaluate counterexamples; anticipate rebuttals.
16. Run `phil-parity-check` → test parity and relevant-similarity claims; evaluate companions-in-guilt arguments.
17. Run `phil-dialectical-map` → build thesis-objection-response dialectical trees.
18. Run `phil-analogy-check` → evaluate analogical arguments for source-target correspondence.
19. Run `phil-methodology` → identify, classify, and evaluate methodological commitments.

### Phase 5: Integrated Report
20. Assemble all analysis outputs into a comprehensive integrated report with:
    - Executive summary
    - Domain classification and feature detection results
    - Argument reconstruction section (all arguments in standard form)
    - Conceptual analysis section (key concepts, distinctions, thought experiments)
    - **Ontological audit** (if metaphysics triggers): entity inventory, category assignments, modal status of commitments
    - **Metaethical stance audit** (if metaethics triggers): realism spectrum position, semantic commitments, normative structure
    - Dialectical structure visualization (ASCII tree)
    - Critical evaluation section (counterexamples, parity findings, methodological assessment)
    - Open questions and recommendations for further analysis

## Notes

- All output in Chinese (per project convention)
- Follow up with `/phil-pipeline` to proceed from analysis to writing
- Domain detection is automatic; the orchestrator explicitly reports which triggers were found and which skills were activated
- Skills are run with dependency ordering: reconstruction before charity, charity before premises, premises before counterexamples
- The integrated report serves as the primary input for the writing pipeline (Stage 2 of `/phil-pipeline`)
