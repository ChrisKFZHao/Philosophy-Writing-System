# Framework Changelog

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
