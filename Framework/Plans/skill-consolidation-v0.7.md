# Skill Consolidation and Writing Workflow Refactor

**Target version:** `0.7.0-alpha`  
**Status:** Working draft  
**Last updated:** 2026-08-24

This plan records the decisions confirmed so far. It remains open for revision while the remaining design questions are discussed.

## Summary

- Consolidate the current 30 atomic skills, 9 workflows, and 7 roles into four public skills. Preserve atomic capabilities as internal methods that are not registered as skills.
- Replace duplicated role and workflow prompt sources with four canonical `SKILL.md` entrypoints and one non-skill full-pipeline command specification.
- Make `phil-research` a shared evidence/provenance kernel with isolated mode contracts, rather than a single undifferentiated super-skill.
- Preserve the project as a self-contained philosophical writing framework. External academic-writing projects are architectural references only and will not become runtime dependencies.
- Release the breaking restructure as `0.7.0-alpha`; do not retain a deprecation period for removed public entrypoints.

## External Reference Decisions

- [Academic Research Skills v3.20.1](https://github.com/Imbad0202/academic-research-skills/blob/main/docs/ARCHITECTURE.md): adopt staged artifacts, explicit human checkpoints, integrity gates, and resumable state. Do not reproduce its later agent matrix, protocol proliferation, or cross-file hash-lock maintenance burden.
- [ARS-Codex](https://github.com/Imbad0202/academic-research-skills-codex/blob/main/skills/academic-research-suite/SKILL.md): adopt intent routing and conditional loading of internal workflow material. Do not adopt a single public suite skill; this project will expose four capability skills.
- [STORM](https://github.com/stanford-oval/storm): use pre-writing perspective exploration and simulated questioning as references for research orientation and tutoring, while keeping drafting separate.
- [PaperQA2](https://github.com/Future-House/paper-qa) and [OpenScholar](https://github.com/AkariAsai/OpenScholar): use evidence-first retrieval, reranking, reusable evidence packets, and claim-to-source attribution as references for research and citation closure.
- [AI Scientist](https://github.com/SakanaAI/AI-Scientist): adopt explicit artifact contracts and independent review boundaries; do not adopt autonomous end-to-end authorship.

## Public Interfaces

| User command | Canonical skill | Modes and responsibility |
|---|---|---|
| `phil:research` | `phil-research` | `ingest`, `reconstruct`, `evaluate`, `comment`, `philosophers` |
| `phil:tutor` | `phil-tutor` | `reading`, `incubating`; conception tutoring remains an independent capability |
| `phil:write` | `phil-write` | `outline`, `draft`, `revision` |
| `phil:review` | `phil-review` | `full`, `targeted`, `re-review`; review is read-only unless revision is explicitly requested |
| `phil:full` | Non-skill command | `start`, `status`, `resume`; orchestrates the four skills through persisted state |

### Compatibility Policy

- Replace `phil:reconstruct`, `phil:evaluate`, `phil:comment`, `phil:ingest`, and `phil:philosophers` with `phil:research <mode>`.
- Replace `phil:pipeline` with `phil:full`.
- Retain the user-facing names `phil:tutor`, `phil:write`, and `phil:review`, but bind them directly to the new canonical skills.
- Remove all `source-command-*` entrypoints and generated bridges. Do not retain aliases or deprecation shims.
- An explicit mode always wins. When natural-language intent maps cleanly to one mode, route automatically; when a material ambiguity remains, ask one focused question instead of invoking several modes.

### Collaboration Mode Resolution

- For a new run, resolve collaboration mode in this order: explicit user instruction, `PROJECT.md`, then `user-led`.
- For a resumed run, preserve the mode recorded in workflow state. A later change requires explicit user authorization and a recorded transition.
- `user-led` and `assistant-led` use identical quality gates, artifact contracts, and test coverage. They differ only in authorship identity and modification authority.

## Canonical Structure

- Make the following four files the only authoritative skill entrypoints:
  - `Framework/Workflow/Skills/phil-research/SKILL.md`
  - `Framework/Workflow/Skills/phil-tutor/SKILL.md`
  - `Framework/Workflow/Skills/phil-write/SKILL.md`
  - `Framework/Workflow/Skills/phil-review/SKILL.md`
- Define the full state-machine orchestration once in `Framework/Workflow/Commands/phil-full.md`. It may reference the four skills but must not duplicate their protocols.
- Add shared internal directories under `Framework/Workflow/`: `Methods/<package>/`, `Services/`, and `Contracts/`. These are framework sources, not public skill entrypoints.
- Remove the independent canonical `Roles/` and `Workflows/` prompt sources after their unique rules have been migrated. Mode references may exist under a skill, but must contain only mode-specific routing, contracts, and authority boundaries; they must not become renamed copies of the old workflows.
- Treat 250–350 lines as the normal `SKILL.md` target and 500 lines as a validated hard ceiling. Retain only routing, shared invariants, input/output contracts, authority boundaries, and failure handling in each entrypoint.
- Move detailed methods, examples, and checklists behind conditional references. Eliminate the repeated boilerplate currently shared by 25 atomic skills.

### `phil-research` Kernel and Mode Isolation

`phil-research/SKILL.md` owns only the research invariants shared across modes:

- source identity, title-page provenance, and current source hash;
- evidence locators, coverage planning, and hash-current reuse;
- bibliography registration and the two-hop Citation Gate boundary;
- common status vocabulary, output disclosure, and external-write rules.

Each mode has a separate, short contract under `Skills/phil-research/references/modes/`:

| Mode | Mode contract | Distinct authority or side effect |
|---|---|---|
| `ingest` | `modes/ingest.md` | May rename/register sources and request Zotero writes; `--dry-run` remains the default safety path |
| `reconstruct` | `modes/reconstruct.md` | Read-only progressive comprehension and coverage ledger |
| `evaluate` | `modes/evaluate.md` | Read-only targeted assessment of current source/analysis artifacts |
| `comment` | `modes/comment.md` | Read-only qualitative commentary; no bibliography or project mutation |
| `philosophers` | `modes/philosophers.md` | Private queue/profile maintenance; approval remains explicit and source-backed |

This grouping is justified by the shared research kernel, not by identical cognitive tasks. The mode contracts select methods and services; they do not duplicate the kernel or hide full workflow protocols in `phil:full`.

### Method and Service Loading Contract

Use these canonical paths:

```text
Framework/Workflow/
├── Methods/
│   ├── argument/<slug>.md
│   ├── concept/<slug>.md
│   ├── dialectic/<slug>.md
│   ├── metaphysics/<slug>.md
│   └── metaethics/<slug>.md
├── Services/<slug>.md
└── Contracts/<contract>.schema.json
```

The manifest is the authoritative resolver. It must support these item kinds:

- `skill`: one of the four public skills;
- `method_package`: package ID, source directory, and member method IDs;
- `method`: stable method ID, package, source path, legacy IDs, consumers, selectors, inputs, outputs, and side-effect policy;
- `service`: shared deterministic or permissioned operation such as source intake, Citation Gate, or philosopher database maintenance;
- `command`: `phil:full` and its state-machine contract.

Loading is deterministic:

1. Resolve the public skill and explicit mode.
2. Read only that mode's contract file.
3. Resolve the contract's method/service IDs through the manifest.
4. Read only the listed method and service files, plus directly named schemas.
5. Fail with an explicit missing-ID error; never silently load an entire package or guess a replacement.

Method files contain procedure and decision rules; the manifest contains identity, routing, dependencies, and exposure policy. `method` and `service` items are never generated as runtime skills or adapters.

## Internal Method Packages

Convert the 30 public atomic skills into non-registered method modules. Use stable coverage IDs in the form `method.<package>.<slug>`. Not every research operation is a method: Zotero access, Citation Gate verification, and philosopher-database mutation are services with explicit authority boundaries.

| Package | Methods migrated from existing skills |
|---|---|
| `argument` | `analogy-check`, `argument-reconstruct`, `charity-check`, `counterexample`, `parity-check`, `premise-detect` |
| `concept` | `conceptual-analysis`, `distinction-track`, `intuition-pump`, `natural-kind-analyze`, `thought-experiment` |
| `dialectic` | `citation-extract`, `contextualize`, `dialectical-map`, `methodology`, `summarize` |
| `metaphysics` | `causation-analyze`, `conceivability-arg`, `essence-detect`, `grounding-check`, `identity-persistence`, `modal-arg`, `ontological-commitment` |
| `metaethics` | `moral-disagreement`, `moral-epistemology`, `moral-psychology`, `moral-realism`, `moral-semantics`, `moral-supervenience`, `normativity` |

- Store a committed migration map containing every old skill ID, its new method ID, package, and existing human-readable labels.
- Make coverage independent of public skill names. Preserve human labels as display metadata rather than identifiers.
- Let each mode contract route directly to only the method/service files required for the current task. Do not load an entire package by default.
- Share a method across skills instead of copying its instructions into multiple entrypoints.

## Reading and Evidence Retrieval Boundary

- Define `Contracts/evidence-unit.schema.json` and an `evidence-provider` service interface for page/section/paragraph locators, text spans, source hash, extraction version, and unit hash.
- Reuse hash-current extraction units and reading maps before reopening a PDF. A retrieved evidence packet must include the hit, its local paragraph neighborhood, locator, selection reason, and verification status.
- `0.7.0-alpha` uses local deterministic extraction and a cache/index contract; it does not require a vector database or external embedding service. A SQLite FTS5 or hybrid RAG implementation is a `0.7.1-alpha` follow-up after recall/precision fixtures exist.
- Partial retrieval never counts as full reading coverage. Citation Gate and final analysis must retain explicit page/section provenance.

## Writing Skill Protocol

Use one authoritative sequence:

`intake -> outline -> outline approval -> section brief -> draft -> section audit -> revision -> citation closure`

### Intake

- Resolve the deliverable, argument maturity, length and format constraints, available sources, citation readiness, and collaboration mode.
- Distinguish confirmed facts, user commitments, provisional inferences, and unresolved questions.

### Outline

- Store the human-readable outline in `{topic}-outline.txt`.
- Define the thesis, section functions, argument dependencies, anticipated objections, evidence requirements, and citation slots.
- In `phil:full`, require outline approval before drafting. A direct request to skip approval records `waived` with the authorizing user instruction rather than silently bypassing the gate.

### Section Brief and Draft

- Give every section a brief containing its argumentative purpose, central claim, premises or evidence, incoming and outgoing transition, source function, and prohibited conceptual drift.
- In `user-led` mode, do not supply substantive prose or directly modify the manuscript without passage-level authorization. In `assistant-led` mode, drafting and direct revision are allowed within the approved outline.
- Mark substantive assistant completion with `[AI 补全]` wherever the shared runtime policy requires disclosure.

### Section Audit and Revision

- Audit conceptual economy, definition-before-use, explicit transitions, analytical source introduction, argumentative contribution, and citation readiness.
- Use the persisted review-finding ledger to drive revision. Never silently delete, collapse, or mark a finding resolved without evidence.

### Citation Closure

- Require every body citation to have a bibliography entry and remove uncited bibliography entries unless the user explicitly requests a broader reading list.
- Preserve the existing two-hop Citation Gate: project registration plus verified, hash-current analysis at the required level.
- Keep citation existence, claim support, and bibliography closure as separate checks.

## Full Pipeline State

Use these stages for `phil:full` (`incubation` is conditional):

`intake -> research -> [incubation] -> outline -> section_brief -> draft -> section_audit -> review -> revision -> citation_closure -> complete`

Upgrade project workflow state to schema v2 with these fields:

- `schema_version`
- `run_id`
- `entrypoint`
- `stage`
- `status`
- `collaboration_mode`
- `artifacts[]`, including artifact kind, path, SHA-256, and status
- `approvals.conception`, including decision, artifact hash, timestamp, and reason when incubation runs
- `approvals.outline`, including decision, approved artifact hash, timestamp, and reason
- `approvals.review`, including editorial decision, review artifact hash, timestamp, and reason
- `approvals.citation_closure`, including integrity result, user acknowledgement timestamp, and report hash
- `review_findings[]`, including stable ID, severity, target, status, and source review hash
- `section_audit`, including report hash, unresolved finding count, and machine verdict
- `next_action`
- `updated_at`

Use these state rules:

- Status values are `not_started`, `in_progress`, `awaiting_user`, `blocked`, `stale`, and `completed`.
- Outline decisions are `pending`, `approved`, `rejected`, and `waived`.
- Conception decisions are `pending`, `accepted`, and `waived`; `waived` requires an explicit user instruction.
- Review decisions are `pending`, `accept`, `minor`, `major`, and `reject`.
- Review-finding states are `open`, `accepted`, `rejected`, `resolved`, and `deferred`.
- `section_audit` is a machine/advisory report, not a second outline-style approval. Unresolved high-severity findings prevent `complete` until resolved or explicitly deferred with a recorded reason.
- If intake finds no current conception artifact, `phil:full` invokes `phil:tutor incubating`, records the returned conception artifact and hash, enters `awaiting_user`, and proceeds only after `approvals.conception=accepted`. A valid current conception is reused; an explicit skip records `waived`.
- Standalone `phil:tutor incubating` and the pipeline use the same skill contract; `phil:full` consumes its artifact and does not duplicate its dialogue protocol.
- Citation closure requires a machine PASS followed by user acknowledgement. It cannot be waived to bypass the two-hop Citation Gate.
- `status` is read-only and reports the next valid action.
- `start` must not overwrite an unfinished run; it reports the existing state and directs the user to `resume`. A completed run may start a new `run_id`.
- `resume` validates artifact hashes before reusing outputs. A mismatch marks affected artifacts and the run `stale`, returns to the earliest affected stage, and requests renewed confirmation.
- Inside a recognized writing project, all four skills update v2 state. Outside a project, direct skills operate statelessly and do not create project files unless requested. `phil:full` requires an existing project.

## Manifest, Generation, and Migration

- Upgrade `Framework/Workflow/manifest.json` so it registers exactly four public skills, five method packages, 30 internal methods, the required services, and the `phil:full` command specification. Only the four skills are exposed as runtime skills.
- Remove hard-coded skill, workflow, role, schema, and adapter counts from the generator, doctor, and tests. Derive all inventories from the manifest.
- Generate exactly four Codex skills and four Claude skills.
- Claude may receive thin command wrappers for `phil:research`, `phil:tutor`, `phil:write`, `phil:review`, and `phil:full`; these wrappers only delegate and are not canonical definitions.
- Route Codex commands through the generated root guidance to the four exact skill IDs or the `phil:full` command specification.
- Regenerate `AGENTS.md`, `Framework/Workflow/Templates/Root/root-guidance.md`, all private project bridges, and both runtime adapters from the manifest; none may retain the old count or command table.
- Generate removed-entrypoint messages from the migration map. For example, `phil:reconstruct` must report `phil:research reconstruct`, and `phil:pipeline` must report `phil:full start`; no removed command may silently guess a mode.
- Capture the old routing/coverage/state outputs on the regression fixture corpus before deleting the old generated adapters or workflow sources; use those snapshots as the migration baseline.
- Add a deterministic migration script that defaults to dry-run and requires `--apply` for writes. It must:
  - Migrate all old skill and workflow IDs through the committed mapping table.
  - Preserve existing human-readable labels.
  - Update all machine-readable metadata fields containing old IDs, including analysis metadata and workflow state.
  - Update the project guidance and generated adapters for `instantaneous-velocity`, `rawlsian-ai`, and `srinivasan-critique`.
  - Fail on unknown IDs instead of guessing or dropping data.
  - Restrict writes to known framework, adapter, project-guidance, and metadata targets.
- Preserve the existing user modification in `Private/Projects/instantaneous-velocity/working-notes.md`; the migration must neither read it as configuration nor write to it.
- Update `Framework/ARCHITECTURE.md`, the two user-facing README files, generated root guides, `Framework/changelog.md`, and the doctor for `0.7.0-alpha`.

## Test Plan

### Structure and Routing

- Assert that each runtime exposes exactly four skills and that no `source-command-*` or public atomic-skill adapters remain.
- Assert that method packages, methods, services, and commands are present only in the neutral framework layer and are not emitted as runtime skill directories.
- Test the deterministic mode-to-method/service load plan, including missing IDs, package-wide load prevention, and side-effect policy resolution.
- Test every new command and mode, including natural-language routing and one-question ambiguity handling.
- Confirm that removed command forms return an explicit migration message containing the old command, replacement command, and replacement mode where applicable.
- Scan for stale hard-coded counts and obsolete phrases such as `28 skills`, `30 skills`, `9 workflows`, `7 roles`, and `39 skills` where they no longer describe history.
- Assert that generated `AGENTS.md` and root guidance match a fresh generator run and list exactly the new commands.

### Migration and State

- Cover all 30 old skill IDs and every preserved human label in migration fixtures.
- Assert that unknown IDs fail without partial writes.
- Test v1-to-v2 state migration for all three private projects.
- Test conception acceptance/waiver, outline approval, review decisions, citation-closure acknowledgement, outline changes after approval, section-audit blocking, stale artifact hashes, review-finding transitions, and `start/status/resume` behavior.

### Migration Regression Baseline

- Run the old and new routes on the same anonymized fixture corpus covering ingestion, reconstruction, evaluation, commentary, philosopher maintenance, writing, review, and full-pipeline resume.
- Compare route selection, coverage IDs and `run/reuse/skip` decisions, hashes, locators, schema validity, Citation Gate verdicts, and planned side effects.
- Do not require generated prose to be byte-identical; require no loss of required fields, provenance, authority boundaries, or explicit uncertainty. Any intentional behavior change must be recorded with a fixture-specific rationale.

### Writing and Review

- Run paired, anonymized scenarios in `user-led` and `assistant-led` modes for vague conception, source-driven outlining, section drafting, and review-driven revision.
- Require identical structural, argumentative, section-audit, and citation-closure gates in both modes.
- Verify that `user-led` refuses unauthorized drafting or direct edits while `assistant-led` permits them inside the approved scope.
- Verify that `phil-review` does not edit the manuscript and that revision consumes review findings without suppressing unresolved issues.

### Citation Integrity

- Cover a valid two-hop citation, an unregistered KEY, insufficient analysis level, provisional verification, stale PDF hash, stale analysis hash, and body-to-bibliography mismatch.
- Confirm that bibliography closure does not promote an unverified source or bypass the Citation Gate.
- Verify evidence-unit locators, neighborhood expansion, extraction-version invalidation, and partial-coverage labeling without loading a complete PDF into the model context.

### Final Validation

- Run manifest, generator, doctor, schema, adapter, and end-to-end tests.
- Regenerate both runtime adapters and assert a clean second generation with no diff.
- Forward-test each of the four skills in a fresh context using raw task artifacts rather than the intended answer or implementation diagnosis.
- Forward-test the `phil-research` modes independently so success in one mode cannot be attributed to leaked context from another mode.

## Assumptions and Fixed Decisions

- The repository remains self-contained; no ARS code or package is vendored or installed.
- Public entrypoint removal is intentionally breaking and has no deprecation period.
- Conception tutoring remains independent from research and writing.
- The full pipeline is a state-machine command, not a fifth skill.
- `phil-research` remains one public skill only because its shared provenance/evidence kernel removes duplicated protocol; mode procedures and side-effect services remain isolated and independently testable.
- `user-led` and `assistant-led` remain equal in quality expectations.
- The current dual-repository privacy boundary and two-hop Citation Gate remain unchanged.
- `0.7.0-alpha` defines the evidence-provider and cache contracts but defers vector embeddings and external RAG services until a later recall/precision evaluation.
- Provider and model selection remain session-scoped policy and are not encoded into skills or the manifest.
- This file remains a working draft until the remaining design questions are resolved.
