# Analytic Philosophy Writing System — Architecture Document

> **Version**: 0.7.0-alpha &emsp; **Status**: Alpha
>
> **Runtime hosts**: Claude Code and Codex (any runtime with file-read access can execute the neutral layer)
>
> The philosophy workflow is self-contained. `academic-research-skills` remains an optional supplement for literature search, format conversion, and citation verification.
>
> **Subdomain Coverage**: General Analytic Philosophy · Metaphysics · Metaethics

---

## 1. What Changed in 0.7.0-alpha

0.6 exposed 30 atomic public skills, 9 workflows, and 7 roles. 0.7 consolidates them into **four public skills** and **one non-skill command**, preserving every atomic capability as internal, non-registered methods:

| 0.6 surface | 0.7 surface |
|---|---|
| 30 atomic `phil-*` skills | `Framework/Workflow/Methods/` — 5 packages, 30 methods (`method.<package>.<slug>`), loaded on demand |
| 9 `Workflows/*.md` | mode contracts under the four skills + `Commands/phil-full.md` |
| 7 `Roles/*.md` | absorbed into the four SKILL.md entrypoints (writer → `phil-write`, reviewer → `phil-review`, tutor+metaphysician+metaethicist → `phil-tutor`, orchestrator → `phil-full`, commentator → `phil-research/comment`) |
| `phil:reconstruct/evaluate/comment/ingest/philosophers` | `phil:research <mode>` |
| `phil:pipeline` | `phil:full` (state machine, schema v2) |
| `source-command-*` Codex bridges | removed; root-guidance routing to the four generated skills |

The removal is intentionally breaking with no deprecation period. The deterministic resolver is `workflow-policy.py removed-entrypoint <command>`; the committed mapping table is `Migration/migration-v0.7.json`.

**Why one `phil-research`**: its six modes share one evidence/provenance kernel (source identity, title-page provenance, hash-current reuse, coverage ledger, Citation Gate boundary) — the share removes duplicated protocol. The modes themselves are isolated: separate contract files, separate method selection, separate side-effect policy (only `ingest` and `translate` write — `translate` only under `Private/Bibliography/Reader/`; approval in `philosophers` is always explicit and source-backed).

## 2. Design Principles

1. **Single source of truth**: `Framework/Workflow/manifest.json` (schema v2) is the authoritative resolver; the plugin's hand-maintained skills live in `Framework/Plugin/skills/`. Generated manifests, marketplace files, and project pointers never become sources of truth.
2. **Minimal public surface**: four public skills plus the `full` pipeline entrypoint (a thin plugin skill), symmetric across runtimes. Methods, packages, and services are internal and loaded on demand through the manifest.
3. **Deterministic before model-executed**: scans, plans, gates, state transitions, and migration are script-enforced; the model executes semantics (feature classification, claim-to-source judgment, dialogue).
4. **Staged artifacts with resumable state**: every pipeline stage produces a hashed artifact recorded in v2 workflow state; `resume` validates hashes and rewinds to the earliest affected stage.
5. **Charity gates, not hard blocks**: a nameable defect triggers a challenge; a gap short of a defect is completed charitably with `[AI 补全]` disclosure; overrides are recorded, never silent (Rule 1 §Workflow Gates).
6. **Citation integrity is fail-closed**: the two-hop Citation Gate (refs.md registration + verified hash-current analysis) blocks on any gap; citation closure cannot be waived (Rule 2).
7. **Cost-aware, not cost-encoded**: no skill or manifest entry selects a provider or model; delegation is a session-scoped prompt policy (Rules/runtime-compatibility.md).

## 3. Directory Tree

```
Framework/Plugin/            the phil plugin — single public skill tree for both hosts
├── plugin.json              Codex portable manifest (generated)
├── .claude-plugin/plugin.json   Claude Code manifest (generated)
└── skills/                  research/ (+ references/modes/), tutor/, write/, review/, full/

Framework/Workflow/
├── manifest.json            v2 registry: 4 skills, 5 method packages, 30 methods,
│                            5 services, 1 command — with modes, consumers, selectors,
│                            legacy IDs, and side-effect policy per item
├── Methods/                 Internal method packages (never registered as skills)
│   │                        (+ references/ per package: v0.6 examples/checklists as
│   │                        conditional references, loaded only on live ambiguity
│   │                        or explicit request, named by their method files)
│   ├── argument/            analogy-check, argument-reconstruct, charity-check,
│   │                        counterexample, parity-check, premise-detect
│   ├── concept/             conceptual-analysis, distinction-track, intuition-pump,
│   │                        natural-kind-analyze, thought-experiment
│   ├── dialectic/           citation-extract, contextualize, dialectical-map,
│   │                        methodology, summarize
│   ├── metaphysics/         causation-analyze, conceivability-arg, essence-detect,
│   │                        grounding-check, identity-persistence, modal-arg,
│   │                        ontological-commitment
│   └── metaethics/          moral-disagreement, moral-epistemology, moral-psychology,
│                            moral-realism, moral-semantics, moral-supervenience, normativity
├── Services/                Permissioned shared operations
│   ├── source-intake.md     library intake pipeline (scan → extract → rename → register → summarize → observe → recommend)
│   ├── zotero-registration.md  identifier-gated Zotero writes (DOI → ISBN → bibtex cascade)
│   ├── citation-gate.md     two-hop Citation Gate + philosopher-claim gate
│   ├── philosopher-db.md    philosopher database maintenance
│   └── evidence-retrieval.md  evidence units, locators, hash-current reuse (0.7.0: local deterministic + cache contract)
├── Contracts/               Cross-layer data contracts
│   ├── workflow-state.schema.json   pipeline state v2
│   └── evidence-unit.schema.json    evidence unit v1
├── Commands/                phil-full.md — the state-machine command specification
├── Migration/               migration-v0.7.json (committed ID map), migrate-v07.py, generate-manifest.py
├── Rules/                   socratic-engagement, citation-integrity, version-management, runtime-compatibility
├── References/              glossaries, 26 argument forms, distinctions, fallacy catalog, templates
├── Schemas/                 17 method-output data contracts + report-id registry
├── Templates/               report templates, project templates
├── Tests/                   structure/routing, policy planning + v0.6 regression baseline, state v2, citation gate, content doctor
└── Scripts/                 build-adapters, workflow-doctor, content-doctor, workflow-policy,
                             project-state, idea-ledger, philosopher-db, bibliography-scan, zotero-attach-linked
```

Generated files (committed, never hand-edited): the two plugin manifests (`Framework/Plugin/plugin.json`, `Framework/Plugin/.claude-plugin/plugin.json`), the two marketplace files (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`), and each `Private/` project's `AGENTS.md` pointer.

## 4. Public Interfaces

| Command | Canonical artifact | Modes |
|---|---|---|
| `phil:research` | `Framework/Plugin/skills/research/SKILL.md` | `ingest`, `reconstruct`, `evaluate`, `comment`, `philosophers` |
| `phil:tutor` | `Framework/Plugin/skills/tutor/SKILL.md` | `reading`, `incubating` |
| `phil:write` | `Framework/Plugin/skills/write/SKILL.md` | `outline`, `draft`, `revision` |
| `phil:review` | `Framework/Plugin/skills/review/SKILL.md` | `full`, `targeted`, `re-review` |
| `phil:full` | `Framework/Plugin/skills/full/SKILL.md` (spec: `Commands/phil-full.md`) | `start`, `status`, `resume` |

Routing rules: an explicit mode always wins; clean natural-language intent routes automatically; a material ambiguity gets one focused question — never a speculative multi-mode sweep. Legacy command names are translated with an explicit notice via the migration map.

### Method and service loading contract

Deterministic, five steps: (1) resolve skill + mode; (2) read only that mode's contract; (3) resolve its method/service IDs through the manifest; (4) read only the listed files plus named schemas; (5) fail on a missing ID — never load a whole package, never guess a replacement. Method files carry procedure and decision rules; the manifest carries identity, routing, dependencies, and exposure policy.

### Collaboration modes

`user-led` and `assistant-led` share identical quality gates, artifact contracts, and test coverage; they differ only in authorship identity and modification authority (passage-level authorization in `user-led`; drafting within the approved outline in `assistant-led`). Resolution for a new run: explicit instruction → `PROJECT.md` → `user-led`. Resumed runs preserve the recorded mode; changing it requires explicit authorization and a recorded transition.

## 5. Writing Skill Protocol

One authoritative sequence (see `Framework/Plugin/skills/write/SKILL.md`):

`intake -> outline -> outline approval -> section brief -> draft -> section audit -> revision -> citation closure`

- **Intake**: deliverable, argument maturity, constraints, sources, citation readiness, collaboration mode; confirmed facts vs user commitments vs provisional inferences vs open questions.
- **Outline**: `{topic}-outline.md` — thesis, section functions, argument dependencies, anticipated objections, evidence requirements, citation slots. Consumes `{topic}-conception.md` preferentially; substantive deviation is flagged and justified, never silent.
- **Section brief**: purpose, central claim, premises/evidence, incoming/outgoing transitions, source function, prohibited conceptual drift.
- **Section audit**: conceptual economy, definition-before-use, explicit transitions, analytical source introduction, argumentative contribution, citation readiness. Machine/advisory — unresolved high-severity findings block `complete` until resolved or explicitly deferred with reason.
- **Citation closure**: every body citation has a bibliography entry; uncited entries removed unless a broader reading list is requested; two-hop gate on every cited KEY; existence, claim support, and closure are separate checks. Machine PASS + user acknowledgement; **cannot be waived**.

## 6. Full Pipeline State (schema v2)

Stages: `intake -> research -> [incubation] -> outline -> section_brief -> draft -> section_audit -> review -> revision -> citation_closure -> complete`

State file `{topic}-workflow-state.json`, maintained by `Scripts/project-state.py` (`init` / `status` / `resume` / `artifact` / `advance` / `approve` / `finding` / `audit`). Fields: `schema_version, project, run_id, entrypoint, stage, status, collaboration_mode, artifacts[] (kind, POSIX-relative path, SHA-256, status), approvals (conception?, outline, review?, citation_closure?), review_findings[], section_audit?, next_action, updated_at`.

Rules: status values `not_started / in_progress / awaiting_user / blocked / stale / completed`; outline decisions `pending / approved / rejected / waived`; conception `pending / accepted / waived`; review `pending / accept / minor / major / reject`; findings `open / accepted / rejected / resolved / deferred`. `start` refuses to overwrite an unfinished run; `resume` validates artifact hashes, marks mismatches `stale`, rewinds to the earliest affected stage, and requests renewed confirmation. Paths are POSIX-relative (cross-runtime). Inside a recognized project, all four skills update this state; outside, they operate statelessly. `phil:full` requires an existing project.

Incubation is conditional: no current conception artifact → invoke `phil:tutor incubating`, record artifact + hash, `awaiting_user`, proceed on `approvals.conception = accepted` (explicit skip records `waived`). Standalone and pipeline incubation share one skill contract — `phil-full` consumes the artifact and never duplicates the dialogue protocol.

## 7. Research Kernel and Services

`phil-research`'s kernel invariants (all modes): source identity = bibliography KEY + canonical stem; metadata from the title page (Rule 2); every analytical claim anchored to an evidence locator with hash-current source SHA-256; partial retrieval never counts as full reading coverage; coverage in canonical method IDs with legacy normalization on read; status vocabulary (`full/partial/skipped`, `verified/provisional/stale`, `run/reuse/skip`).

Services own the side effects: `source-intake` (the only library-write path, `--dry-run` default safety), `zotero-registration` (identifier-gated external writes, backend-classified), `citation-gate` (read + block), `philosopher-db` (queue writes; semantic approval always explicit and source-backed), `evidence-retrieval` (read; 0.7.0 local deterministic + cache contract — vector/FTS retrieval is deferred to 0.7.1 pending recall/precision fixtures).

## 8. Deterministic Planning and the Regression Baseline

`workflow-policy.py` provides `reconstruction-plan` and `evaluation-plan`: the model classifies features once, the planner emits the `run/reuse/skip` ledger over canonical method IDs, reusing only verified hash-current coverage. Coverage aliases (legacy labels and `phil-*` skill IDs) normalize on read; new writes are canonical-only. `removed-entrypoint` resolves removed commands to their replacements.

The v0.6 planner outputs were captured on a fixture corpus **before** the old adapters and workflow sources were deleted (`Tests/fixtures/v06-planner-baseline.json`, 32 cases). The test suite replays every case against the new planner, maps module IDs old→new through the committed migration map, and asserts identical decisions, selectors, and reasons — the deterministic no-behavior-drift guarantee. Generated prose is not compared byte-for-byte; required fields, provenance, authority boundaries, and explicit uncertainty must not regress, and any intentional change carries a fixture-specific rationale.

## 9. Generation, Doctor, and Migration

- **`build-adapters.py`**: derives the two plugin manifests, the two marketplace files, and the `Private/**/AGENTS.md` pointers from the manifest; inventory is derived, never hard-coded; `--check` verifies freshness and fails if any legacy adapter path exists (a root `CLAUDE` guide, generated skill/command/rule directories under the host dot-directories, or the old Codex skills tree); second generation is byte-identical (no diff).
- **`workflow-doctor.py`**: JSON validity (manifest, schemas, contracts, migration map, philosopher DB), plugin skill frontmatter, manifest-derived inventory (plugin skill dirs = entrypoints; exposure.skills = skill items; Methods/ tree = manifest methods; services present), stale-phrase scan (`30 skills`, `9 workflows`, `7 roles`, `39 skills`, `28 skills`, `source-command-`, `28 phil-*`) over living definitions (changelog, Lessons, and Plans are historical records and exempt), method-ID reference checks, forbidden-content checks, markdown-link check, philosopher-database validation, and the adapter check.
- **`migrate-v07.py`**: deterministic 0.6→0.7 migration — analysis metadata (`workflow_id`, coverage → canonical method IDs), v1→v2 workflow state, project guidance command references. Defaults to dry-run; `--apply` writes; fails on unknown IDs; writes restricted to a whitelist; `Private/Projects/*/working-notes.md` never read or written.

## 10. Naming Conventions

Unchanged from 0.6 (see `Framework/Workflow/References/project-conventions.md`): uppercase framework/content directories; lowercase kebab-case content-item directories; canonical bibliography stems `{Author}_{Year}_{Title}` with underscore segment boundaries; KEYs `AUTHOR-TITLE` without year. New in 0.7: method files `Methods/<package>/<slug>.md` with ID `method.<package>.<slug>`; services `Services/<slug>.md` with ID `service.<slug>`; contracts in `Contracts/*.schema.json`; internal framework scripts keep kebab-case filenames.

## 11. Extensibility

- **Adding a method**: add `Methods/<package>/<slug>.md` (header: id, package, legacy_ids, label, consumers, selector, side_effects) and regenerate the manifest (`Migration/generate-manifest.py`). It becomes loadable by its consumers; nothing is re-registered publicly.
- **Adding a mode**: add a contract under the skill's `references/modes/`, list its method/service selection, and regenerate the manifests and marketplace files (`build-adapters.py`). The SKILL.md routing table gains one row.
- **Adding a service**: add `Services/<slug>.md` with an explicit authority boundary; register in the manifest; reference from mode contracts.
- **Splitting a public skill**: only by plan (this consolidation's inverse is not a routine operation); the manifest, generated plugin manifests and marketplace files, doctor, tests, and migration map all key off the four-skill exposure.
