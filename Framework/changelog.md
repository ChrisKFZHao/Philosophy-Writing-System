# Framework Changelog

## Unreleased

**Session-scoped cost-aware delegation**

- Removed static role-to-model mappings, including the former generated high-tier Claude mapping. Generated roles now inherit the host session model.
- Replaced the unimplemented routing design with a session-scoped prompt policy. The user authorizes one lower-cost host candidate once per session; no catalog, telemetry, pricing estimate, or automatic host task creation is stored or inferred.
- Only repeatable, independent, read-only, non-interactive candidate work may use that authorization. Parent tasks validate candidates before writes, verified claims, or Citation Gate use; writing, review, artifact changes, user dialogue, and orchestration retain the current session model.

## v0.7.0-alpha — 2026-08-24

**Skill consolidation and writing workflow refactor (breaking, no deprecation period)**

- Consolidated 30 atomic public skills, 9 workflows, and 7 roles into **four public skills** (`phil-research`, `phil-tutor`, `phil-write`, `phil-review`) plus the non-skill `phil:full` command specification. The 30 atomic capabilities are preserved as internal method modules under `Framework/Workflow/Methods/` (5 packages, stable IDs `method.<package>.<slug>`), never registered as runtime skills.
- `phil-research` is one public skill because its five modes share an evidence/provenance kernel; each mode (ingest / reconstruct / evaluate / comment / philosophers) has an isolated contract under `Skills/phil-research/references/modes/` with its own method selection and side-effect policy. Only `ingest` writes; `philosophers` approval is always explicit and source-backed.
- Removed public entrypoints: `phil:reconstruct`/`phil:evaluate`/`phil:comment`/`phil:ingest`/`phil:philosophers` → `phil:research <mode>`; `phil:pipeline` → `phil:full start`; all `source-command-*` Codex bridges removed. No aliases or deprecation shims. Deterministic resolver: `workflow-policy.py removed-entrypoint <command>`; committed mapping: `Migration/migration-v0.7.json`.
- Role and workflow prompt sources deleted after migration: writer/reviewer/tutor/metaphysician/metaethicist/commentator/orchestrator content absorbed into the four SKILL.md entrypoints and `Commands/phil-full.md`. Generated adapters remain non-authoritative.
- Deterministic five-step method/service loading contract through manifest v2 (the authoritative resolver): resolve skill+mode → read only that mode's contract → resolve IDs via the manifest → read only the listed files → fail on missing IDs; never load a whole package, never guess.
- New shared services with explicit authority boundaries: `source-intake` (library intake pipeline), `zotero-registration` (identifier-gated external writes), `citation-gate` (two-hop gate + philosopher-claim gate), `philosopher-db`, and `evidence-retrieval` (evidence units, locators, hash-current reuse; 0.7.0 is local deterministic extraction plus the cache/index contract — vector/FTS retrieval deferred to 0.7.1 pending recall/precision fixtures). New contracts: `Contracts/evidence-unit.schema.json`, `Contracts/workflow-state.schema.json` (v2).
- Writing protocol made authoritative across `phil-write` and `phil:full`: intake → outline (`{topic}-outline.txt`) → approval → section brief → draft → section audit → revision → citation closure. `user-led`/`assistant-led` share identical quality gates; they differ only in authorship identity and modification authority. Citation closure requires a machine PASS plus user acknowledgement and cannot be waived.
- Workflow state upgraded to schema v2 (`project-state.py` rewritten): runs, stages (conditional incubation), statuses, approvals (conception/outline/review/citation-closure), review-finding ledger, section audit, POSIX-relative artifact paths, hash-validated `resume` with rewind to the earliest affected stage, `start` refusing to overwrite unfinished runs.
- `workflow-policy.py` planners now emit canonical method IDs; legacy labels and `phil-*` skill IDs normalize on read, and new writes never use aliases. The v0.6 planner outputs were captured on a 32-case fixture corpus before the old sources were deleted (`Tests/fixtures/v06-planner-baseline.json`); the suite replays them and asserts identical decisions under the ID mapping.
- Generator, doctor, and tests now derive every inventory from the manifest — no hard-coded counts. `workflow-doctor.py` adds a stale-phrase scan and manifest-consistency checks (core = claude = codex skills; wrappers = exposure; no `.claude/agents`; no `source-command-*`).
- `Migration/migrate-v07.py`: deterministic 0.6→0.7 migration (dry-run default, `--apply` to write, fail-on-unknown-ID, write whitelist, `working-notes.md` never touched) — analysis metadata `workflow_id`/coverage to canonical method IDs, v1→v2 state conversion, project guidance command references. Applied to the private library: one analysis meta migrated (Srinivasan 2018); no live v1 workflow states existed; the three project guidance files needed no changes.
- Documentation: ARCHITECTURE rewritten for 0.7.0-alpha; root guidance, both READMEs, project adapter template, and analysis-metadata schema updated; removed-entrypoint table added with old→new command mappings.

## v0.6.3-alpha — 2026-07-19

**Event-driven idea resurfacing and cost-aware analysis planning**

- Enabled bounded semantic resurfacing across Stages 3–6. Only seven named events may query the idea ledger; deterministic overlap filtering returns at most two candidates, the current specialist presents only ideas that would materially change the argument, and prior status is preserved until explicit user reactivation.
- Reworked `phil:reconstruct` into progressive Level 1/2/3 coverage. A deterministic policy plan reuses only verified source-and-analysis-hash-current coverage, invalidates stale artifacts, runs only missing applicable dimensions, and preserves explicit `full` / `deep` coverage.
- Reworked `phil:evaluate` around an always-fresh lightweight inference/fallacy baseline plus feature- or intent-selected dimensions. Counterexample, dialectical, analogy, parity, intuition-pump, and methodology analysis no longer run merely to fill a fixed report shape.
- Added on-demand skill-material loading: selected skills still load their complete operational instructions, while examples, long checklists, and extended references remain unloaded unless a live ambiguity or explicit request requires them.
- Validation: 60 standard-library tests pass; `workflow-doctor.py`, the 203-file adapter freshness check, script compilation, and diff-format checks pass. A live provisional Srinivasan artifact is correctly refused for reuse and blocked by the Citation Gate. The private content doctor still reports pre-existing malformed/missing summaries, that provisional analysis, and legacy project-guidance warnings; no expensive literature work was rerun to conceal those defects.

## v0.6.2-alpha — 2026-07-19

**Project-state and citation-integrity foundation**

- Added structured per-project idea-ledger and workflow-state contracts with standard-library helpers for stable IDs, status transitions, compact candidate queries, artifact hashing, gate decisions, and cross-session resumption.
- Added paired analysis verification metadata. Citation Gate now blocks missing, provisional, stale, hash-mismatched, or shallow analyses instead of trusting the INDEX level alone; the existing Srinivasan analysis remains provisional until full-PDF verification.
- Added a content doctor and corrected bibliography scanning to parse inventory rows rather than prose examples, validate PDF/INDEX/summary/analysis/refs links, and degrade cleanly when `Private/` is absent.
- Added deterministic tests for the new schemas, helpers, scanner, doctor, and Citation Gate paths. Cross-stage semantic resurfacing of archived ideas is deliberately deferred to the next quality-sensitive work package.
- Reserved the next safety-and-recovery work package: dependency-aware automatic rollback, stale-output fail-closed gates, direct philosopher-claim hash verification, atomic state writes, and bounded Stage 3-6 idea resurfacing. This is planned work, not a claim of current support.

## v0.6.1-alpha — 2026-07-19

**Philosophers-DB v2: claim-level provenance, dynamic intake, and generated domain views**

- Migrated 49 domain-folder Markdown entries into one canonical `Profiles/` store. All 640 legacy claims are preserved as `prompt-only`; no unsupported legacy content is treated as cited or verified.
- Added primary/secondary evidence records, source-backed versus prompt-only claim states, dispute state, stable claim IDs, multi-domain links, and generated INDEX/domain views.
- Added the private `Philosopher-Queue/`, idempotent `philosopher-db.py` batch helper, 5-source/3-substantive new-person threshold, immediate existing-profile candidates, deterministic two-source/one-central-source domain promotion, and candidate approval/rejection/reopen lifecycle.
- Added `phil:philosophers` (9th workflow), optional philosopher observations in Level 0.5 summaries and persisted reconstructions, and two JSON contracts. Ingest records each batch once without rereading PDFs.
- Removed the former whole-database citation exception: prompt-only content is `[source unverified]`; source-backed claims route to the actual bibliography KEY and remain subject to the two-hop Citation Gate.

## v0.6.0-alpha — 2026-07-17

**Platform-neutral workflow core with generated Claude Code and Codex adapters**

- Added `Framework/Workflow/manifest.json` as the validated inventory and dependency contract for 30 atomic skills, 8 composite workflows, and 7 roles.
- Moved editable skills, workflows, roles, rules, references, schemas, templates, and helper scripts into `Framework/Workflow/`; `.claude/` and `.agents/skills/` are now deterministic committed adapters.
- Added `build-adapters.py` (`--check`) and `workflow-doctor.py`; generation rejects unknown fields, duplicate IDs/sources, missing dependencies, missing sources, output collisions, stale files, and unexpected adapter files.
- Completed Codex coverage with `source-command-write`, `source-command-comment`, `source-command-pipeline`, and `source-command-tutor`; role-led Codex workflows now read the canonical role prompt instead of referring to an unavailable named agent.
- Replaced provider-specific collaboration output with canonical `user-led | assistant-led` and `[AI 补全]`; `claude-led` and `codex-led` remain deprecated aliases for one minor version.
- Added runtime-neutral `quality_tier: inherit | high` and capability declarations. Claude maps `high` to `opus`; Codex inherits the session model and serializes dependency stages when delegation is unavailable.
- Added `bibliography-scan.py` to replace Bash-only `ls`/`grep` intake checks, plus `workflow-policy.py` and stdlib regression tests.
- Moved and extended `zotero-attach-linked.py` to read credentials from environment or either runtime's user configuration. Ingest now reports Zotero `full`, `partial`, or `skipped`; dry-run never writes.
- Added platform-neutral new-project templates without modifying the three existing projects in the independent `Private/` repository.
- Removed machine-specific paths and automatic project-MCP enablement from tracked Claude settings; `.claude/settings.local.json` is now ignored.

## v0.5.0-alpha — 2026-07-17

**Writing-workflow reorganization: reading-before-thesis 6-stage pipeline + lenient interrogation (宽容性诘问) + tutor incubating mode + dual draft collaboration + per-agent model economy**

- `phil-orchestrator`'s pipeline goes from 5 stages to 6: Stage 0 (prerequisite, outside the pipeline) `/phil:ingest`; Stage 1 Topic Orientation & Reading Plan; Stage 2 Reading & Analysis; Stage 3 Ideation / Conception Incubation (构思孵化, NEW); Stage 4 Outline; Stage 5 Draft & Iterative Revision; Stage 6 Review & Final. The old Stage 1 ("question formulation") is split: scoping → new Stage 1, thesis crystallization → new Stage 3
- Rule 1 (`socratic-engagement.md`) gains a `## Workflow Gates: Lenient Interrogation (宽容性诘问)` section: two triggers (vagueness OR a nameable defect); a defect triggers a challenge; a gap short of a defect gets charitable completion disclosed via `[Claude 补全]`; gates are dialogic and never hard-block; overrides are recorded. Citation Gate (Rule 2) is explicitly unchanged
- `phil-tutor` gains two modes — `reading` (existing 4-phase literature dialogue) and `incubating` (Stage 3: landscape recall → angle probing → argument sketching → conception consolidation) — plus a `tools:` line (Read, Grep, Glob, Write, Edit); incubating mode writes `Private/Projects/{topic}/{topic}-conception.txt` with the thesis kept in the user's own words and all Claude contributions disclosed
- New per-project artifact `{topic}-conception.txt`: Chinese content, freely overwritten, never versioned (Rule 3 exemption added in `version-management.md`)
- `phil-writer` draft mode gains dual collaboration modes declared via the project CLAUDE.md's `collaboration:` key: `user-led` (严肃学术论文 — user writes, Claude gives defect-triggered Socratic feedback plus disclosed suggestions, applies only user-accepted edits) and `claude-led` (课程论文 — Claude drafts with default-on boundary interrogation, 1–3 ownership questions per section boundary); new Quality Standard 8, Disclosure Integrity; outline mode preferentially consumes the conception file, refining rather than replacing the user's thesis; revision mode interacts with the active collaboration mode
- Command files and the root `CLAUDE.md` conventions updated to match the new stages, modes, and artifact
- `ARCHITECTURE.md` bumped to 0.5.0-alpha with the 6-stage pipeline redrawn (§6), agent-layer sections updated (Layers 3 and 5), and 5 pre-existing path typos fixed (`agentsphil:*` → `agents/phil-*`)
- Model economy: all 7 agents gain `model:` frontmatter — `inherit` for phil-tutor, metaphysician, metaethicist, phil-writer (quality-sensitive dialogue/prose follows the session model); `opus` for phil-reviewer, phil-commentator, phil-orchestrator (review/coordination pinned to Opus 4.8) — plus session-level guidance (bulk ingestion/summarization on a cheaper session model) and a pricing snapshot (cached 2026-06-24, $/MTok in/out: Fable 5 10/50 · Opus 4.8 5/25 · Sonnet 5 3/15, intro 2/10 through 2026-08-31 · Haiku 4.5 1/5)
- Roadmap reorder: multi-purpose output (paper/report/presentation) moves from v0.5 to v0.6; the former v0.6 items (Stage 2.5 incubation + adversarial gates, "A2+B2") land now, in lenient form; commentator-as-skeptic remains an optional Stage 6 escalation
- **Validation: pending** — the batch-convention validation run (retro-incubation via `/phil:tutor incubating` + a `user-led` draft session on the srinivasan-critique project) has not yet been executed; results will be appended once it runs

## v0.4.5-alpha — 2026-07-14

**`/phil:ingest` Step 8 book gate: ISBN-only → fallback cascade DOI-first → ISBN → bibtex** (validated on the first real edited-collection ingestion)

- First edited-collection ingestion end-to-end: *Oxford Studies in Metaphysics, Volume 12* (Bennett & Zimmerman eds., OUP 2020) — 1 volume row (`BENNETT-OSM-12`) + 9 member-paper rows (page ranges + container KEY), volume + 4 PART II "Metaphysics of Science" member summaries (Baker, Dasgupta, Bhogal, Ney) at Level 0.5, 5 other members registered summary-pending; Zotero: 1 `book` + 9 `bookSection` items + one batch linked-file POST to all 10 parents (`zotero-attach-linked.py --parents`, verified)
- **Live finding that drove the change**: both the copyright-page ISBN (`9780192893314`) and the ebook ISBN (`9780191914584`) returned "not found" on Open Library *and* Google Books, and the whole-book DOI failed on CrossRef — but **every chapter DOI (`…/<book-doi>.003.000N`) resolved cleanly as a CrossRef `bookSection`**. The v0.4.4 ISBN-only book gate would have dead-ended here
- **Gate revised** (ingest.md §8B, CLAUDE.md, Lessons): books now run a cascade — (1) whole-book DOI + per-chapter DOIs (per-chapter is the *preferred* collection-member path, CrossRef-verified, superior to hand-built `@incollection` bibtex), (2) copyright-page ISBN, (3) resolver-independent `@book`/`@incollection` bibtex from verified metadata. Papers unchanged (DOI). Rule 2 now explicitly covers CrossRef's own output too (it dropped ch. 7's subtitle "Completeness or Maximality?")
- `zotero_add_by_isbn`'s no-`attach_mode` / no-stored-copy verification is retained for when the ISBN path is actually taken; the OSM item was created via `@book` bibtex (book) + per-chapter DOIs (members), all `attach_mode='none'`, book item children verified empty
- Batch mode (`--parents`) exercised for real: 10 parents, single POST, script retries absorbed 2 transient CrossRef/proxy SSL failures

## v0.4.4-alpha — 2026-07-14

**`/phil:ingest` supports monographs and edited collections** (finer-grained summaries + per-paper Zotero items)

- **Document-type detection** (Step 2): `paper` / `monograph` / `collection`, decided by whether chapters are independent, separately-citable works — not by author count (a single author's self-collection is a collection). Books also get ISBN + table-of-contents extraction (Rule 2, from the PDF)
- **Chapter-level summaries** (Step 6): a monograph's `.summary.txt` carries per-chapter segments (`chapters[]`, ~150–300 chars); an edited collection yields a volume summary **plus one independent summary file per member paper** (chapter-level stem, its own topics, a `container` back-link)
- **Per-paper INDEX rows** (Step 5): a collection registers a volume row (KEY `EDITOR-TITLE`) plus one row per member paper (KEY `AUTHOR-TITLE`); member rows point at the shared volume PDF + page range + `in <volume-KEY>`, so each member is independently citable through the two-hop Citation Gate. One physical PDF per volume — never split or copied
- **Two-tier Zotero gate** (Step 8): DOI for papers, **ISBN for books** (`zotero_add_by_isbn`). A collection additionally gets one `bookSection` per member paper (`zotero_add_by_bibtex` `@incollection`), and the volume PDF is linked to the book item + every bookSection in one batch POST. `zotero_add_by_isbn` has no `attach_mode` → first book ingestion verifies no stored copy; Open Library / Google Books metadata cross-check is mandatory (less reliable than CrossRef)
- **`zotero-attach-linked.py` batch mode**: `--parents KEY1,KEY2,…` attaches one stem to many parents in a single POST (auto-splits at Zotero's 50-item cap); single-parent usage unchanged
- Schema: `summary-schema.json` gains `collection` source type, optional `chapters[]` (monograph) and `container` (collection member)

## v0.4.3-alpha — 2026-07-14

**`/phil:ingest` Step 8: Zotero item auto-registration** (batch-scalable — removes the manual "Attach Link to File" click)

- New Step 8 (DOI-gated, cloud write): for a PDF with a verified DOI, `zotero_add_by_doi(attach_mode='none', if_exists='skip')` creates the parent metadata item (no stored copy), CrossRef metadata is cross-checked against the title-page metadata (Rule 2 on the inflow path), the canonical PDF is attached as a `linked_file` via the reusable helper now located at `Framework/Workflow/Scripts/zotero-attach-linked.py` (user-level auth, proxy, retries, `--verify`), and INDEX's `Zotero` column is backfilled with the parent key
- First committed framework script: `zotero-attach-linked.py` fills the Zotero MCP's linked-file gap and is shared by Step 8 and the Lessons migration path; v0.6 moved it to `Framework/Workflow/Scripts/`
- No-DOI sources (SEP entries, working papers) fall back to a reported manual follow-up — automation is never forced on unverifiable metadata
- Guardrails: `--dry-run` skips Step 8 (it writes to the cloud); collections are never auto-filed (lazy-migration principle); the API key/userID are read from user-level runtime configuration and never hardcoded; item keys are written straight into INDEX, never round-tripped through subagent return values (proxy redaction rewrites `KEY:` lines to `[密钥]`)
- `Framework/Lessons/zotero-integration.md` "New PDF" flow updated to describe the automated path; validated live on `BUILES-RATES-OF-CHANGE`

## v0.4.2-alpha — 2026-07-14

**Zotero integration: unified PDF repository + annotation-preserving migration** (pilot: `instantaneous-velocity`, 6 items; first `Framework/Lessons/` entry)

- `Private/Bibliography/PDF/` doubles as Zotero's Linked Attachment Base Directory — one physical repository, two consumers; naming ownership stays with the framework (rename before link, frozen after)
- INDEX.md gains a `Zotero` column: `KEY ↔ Zotero item key ↔ file stem` three-way mapping
- Validated stored→linked migration via web API preserving annotations (`linkMode` is API-immutable → create linked attachment + reparent annotations + trash old); Zotmoov UI path retained as no-API fallback
- Lazy migration policy: Zotero collections are not mirrored; a collection is migrated only when it becomes a writing project
- MCP hybrid mode: local SQLite reads + web API writes (key in user-level runtime configuration); JSTOR-style metadata pollution confirmed → Rule 2 title-page verification mandatory on the Zotero inflow path
- Full workflow: `Framework/Lessons/zotero-integration.md`; B3 (Philosophers-DB master-library rework) moves to v0.4.3

## v0.4.1-alpha — 2026-07-14

**Literature ingestion ("scraping"): `/phil:ingest` command + `phil-summarize` skill** (A1 pulled forward from v0.5)

- `/phil:ingest` (8th command): scans `Private/Bibliography/PDF/` for unprocessed PDFs via programmatic shell set-comparison (token economy — the model never reads the directory/INDEX to judge), then per PDF: extract (pdf skill) → dedupe → rename → INDEX registration → Level 0.5 summary → recommendation trigger point 1
- Canonical bibliography stem `{Author}_{Year}_{Title}` (underscore-separated segments, hyphen-joined words, complete title from the title page) shared across `.pdf` / `.analysis.txt` / `.summary.txt`; KEY format unchanged (`AUTHOR-TITLE`, year-suffix only on collision); 100-char safety valve against Windows path limits
- `phil-summarize` (30th skill): pure-function Level 0.5 summary (core thesis + argument route + key concepts + interlocutors + topics, Chinese, 300-500 chars); `summary-schema.json` (13th schema) + `SUM-` report prefix
- `Summaries/` directory activated (Level 0.5 live); year/title metadata must be read from the PDF itself (Rule 2), fallback `nd` + `[year unverified]`
- B3 (Philosophers-DB master-library rework) moves to v0.4.2

## v0.4-alpha — 2026-07-14

**Repo restructure: Framework/Private dual-repo separation + bibliography linking**

- Privacy boundary = repo boundary: all papers, bibliography, and personal style samples moved into `Private/` (gitignored by the outer repo; independent inner git repo with a private remote)
- PDFs enter NO git (immutable binaries); backup via ordinary file sync
- Outer repo stopped tracking manuscript/ and bibliography/ (history preserved; repo is private)
- Philosophers database moved from `.claude/references/` to `Shared/` (curated, shareable knowledge)
- `ARCHITECTURE.md` moved to `Framework/`; added `Framework/Lessons/` (distilled per-project feedback)
- Bibliography linking: project-level `refs.md` (KEY view, zero duplication) + INDEX `topics` column + two-hop Citation Gate
- Recommendation mechanisms: phil-tutor in-library reverse matching + phil-citation-extract acquisition suggestions
- Reserved: Level 0.5 summary row (lands in v0.5 with phil-summarize)
- Naming & language conventions (same batch, second pass): every directory outside `.claude/` capitalized — `Papers` → `Projects`, `bibliography/pdf/analysis/summaries` → `Bibliography/PDF/Analysis/Summaries`, `philosophers-db` → `Philosophers-DB` (with `General/Metaphysics/Metaethics`), `style/format` → `Shared/Format`, `lessons` → `Lessons`; content-item directories stay lowercase kebab-case. Definition layer (rules/commands/agents/CLAUDE.md/changelog/ARCHITECTURE) converted to English; the two READMEs and the 5 report templates deliberately remain Chinese (user-facing docs / output skeletons).

## v0.3-alpha — 2026-07-12

- Full schema wiring (12 schemas), agent pruning (9→7), INDEX dead-link repair, hook removal, convention unification
- phil:tutor tutor-style literature dialogue agent + phil-citation-extract citation extraction skill

## v0.2-alpha — 2026-07-11

- Workflow refactor: 33→6 composite commands + rules/ extraction + phil:* namespace
- style/ directory for style calibration and format customization

## v0.1-alpha — 2026-07-10

- Initial release: 29 skills + knowledge base + ARS bridge
