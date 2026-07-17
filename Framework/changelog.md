# Framework Changelog

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

- New Step 8 (DOI-gated, cloud write): for a PDF with a verified DOI, `zotero_add_by_doi(attach_mode='none', if_exists='skip')` creates the parent metadata item (no stored copy), CrossRef metadata is cross-checked against the title-page metadata (Rule 2 on the inflow path), the canonical PDF is attached as a `linked_file` via the reusable helper `.claude/scripts/zotero-attach-linked.py` (auth from `~/.claude.json`, proxy, retries, `--verify`), and INDEX's `Zotero` column is backfilled with the parent key
- First committed framework script: `.claude/scripts/zotero-attach-linked.py` fills the zotero MCP's linked-file gap and is shared by Step 8 and the Lessons migration path
- No-DOI sources (SEP entries, working papers) fall back to a reported manual follow-up — automation is never forced on unverifiable metadata
- Guardrails: `--dry-run` skips Step 8 (it writes to the cloud); collections are never auto-filed (lazy-migration principle); the API key/userID are read from `~/.claude.json` at run time and never hardcoded; item keys are written straight into INDEX, never round-tripped through subagent return values (proxy redaction rewrites `KEY:` lines to `[密钥]`)
- `Framework/Lessons/zotero-integration.md` "New PDF" flow updated to describe the automated path; validated live on `BUILES-RATES-OF-CHANGE`

## v0.4.2-alpha — 2026-07-14

**Zotero integration: unified PDF repository + annotation-preserving migration** (pilot: `instantaneous-velocity`, 6 items; first `Framework/Lessons/` entry)

- `Private/Bibliography/PDF/` doubles as Zotero's Linked Attachment Base Directory — one physical repository, two consumers; naming ownership stays with the framework (rename before link, frozen after)
- INDEX.md gains a `Zotero` column: `KEY ↔ Zotero item key ↔ file stem` three-way mapping
- Validated stored→linked migration via web API preserving annotations (`linkMode` is API-immutable → create linked attachment + reparent annotations + trash old); Zotmoov UI path retained as no-API fallback
- Lazy migration policy: Zotero collections are not mirrored; a collection is migrated only when it becomes a writing project
- MCP hybrid mode: local SQLite reads + web API writes (key in `~/.claude.json`); JSTOR-style metadata pollution confirmed → Rule 2 title-page verification mandatory on the Zotero inflow path
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
