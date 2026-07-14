# Report ID Prefix Registry

Central registry of report ID prefixes used across the 30 analysis skills. Each skill generates reports with unique identifiers for cross-reference traceability.

| Prefix | Skill | Domain |
|---|---|---|
| `ARG-` | `phil-argument-reconstruct` | General |
| `CHAR-` | `phil-charity-check` | General |
| `PREM-` | `phil-premise-detect` | General |
| `MODAL-` | `phil-modal-arg` | General |
| `CONC-` | `phil-conceptual-analysis` | General |
| `DIST-` | `phil-distinction-track` | General |
| `TE-` | `phil-thought-experiment` | General |
| `IP-` | `phil-intuition-pump` | General |
| `CTX-` | `phil-contextualize` | General |
| `CE-` | `phil-counterexample` | General |
| `SUM-` | `phil-summarize` | General |
| `DMAP-` | `phil-dialectical-map` | General |
| `ANLG-` | `phil-analogy-check` | General |
| `METH-` | `phil-methodology` | General |
| `PAR-` | `phil-parity-check` | General |
| `CAUS-` | `phil-causation-analyze` | Metaphysics |
| `ESS-` | `phil-essence-detect` | Metaphysics |
| `ONT-` | `phil-ontological-commitment` | Metaphysics |
| `GRND-` | `phil-grounding-check` | Metaphysics |
| `ID-` | `phil-identity-persistence` | Metaphysics |
| `NATK-` | `phil-natural-kind-analyze` | Metaphysics |
| `CONCV-` | `phil-conceivability-arg` | Metaphysics |
| `NORM-` | `phil-normativity` | Metaethics |
| `REAL-` | `phil-moral-realism` | Metaethics |
| `SEM-` | `phil-moral-semantics` | Metaethics |
| `PSY-` | `phil-moral-psychology` | Metaethics |
| `DISA-` | `phil-moral-disagreement` | Metaethics |
| `EPI-` | `phil-moral-epistemology` | Metaethics |
| `SUPV-` | `phil-moral-supervenience` | Metaethics |

> **Note**: Prefixes are conventions, not strictly enforced by schema validation. When a skill's output references another skill's report, use the registered prefix for consistent traceability. New prefixes should be added to this registry.
