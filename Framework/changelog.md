# Framework Changelog

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
