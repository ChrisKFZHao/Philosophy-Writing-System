# CLAUDE.md

> **Project Status: Alpha** — All modules, agents, and skills are functional but have not undergone extensive field testing. Behavioral rules, workflows, and knowledge bases are subject to refinement.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Nature

This is a philosophical writing workflow project, not a code project. All files are text or PDF.

## Behavioral Rules

These rules apply to ALL interactions in this project. Full rule text is in `.claude/rules/`.

### Rule 1: No Sycophancy — Conditional Socratic Engagement
→ [rules/socratic-engagement.md](.claude/rules/socratic-engagement.md)
Assess clarity before responding. Clear ideas → execute directly. Vague ideas → Socratic questioning.
Trigger is **vagueness**, not novelty. Do not fabricate objections for the sake of appearing rigorous.

### Rule 2: No Hallucinated Citations
→ [rules/citation-integrity.md](.claude/rules/citation-integrity.md)
Never generate unverified references, quotations, page numbers, or publication details.
Mark unverified claims with `[source unverified]` or `[citation needed]`.

### Rule 3: Trigger-Based Version Management
→ [rules/version-management.md](.claude/rules/version-management.md)
Version cuts are NOT automatic. Three triggers: (1) post-review revision, (2) new insight/argument, (3) significant compression/expansion. Same-day triggers are merged. Draft file (`-draft.txt`) is never versioned.

## Naming & Language Conventions

**Directory naming:**
- Every directory outside `.claude/` starts with an uppercase letter (`Framework/`, `Shared/`, `Private/`, `Private/Projects/`, `Private/Bibliography/PDF/`). Hyphenated names capitalize each segment; acronyms stay uppercase (`Philosophers-DB`).
- Exception 1: the `.claude/` tree stays lowercase — its paths (`skills/`, `agents/`, `commands/`, …) are fixed by Claude Code's discovery mechanism.
- Exception 2: content-item directories (individual project topics, e.g. `Private/Projects/srinivasan-critique/`) use lowercase English kebab-case, matching their filename prefix (`srinivasan-critique-draft.txt`).
- Filenames use lowercase kebab-case, except conventional uppercase files (`CLAUDE.md`, `README.md`, `INDEX.md`, `VERSIONS.md`, `ARCHITECTURE.md`, `MEMORY.md`).
- Exception 3 — bibliography stems: files in `Private/Bibliography/` share the canonical stem `{Author}_{Year}_{Title}` across `.pdf` / `.analysis.txt` / `.summary.txt`. Segments are separated by **underscores**; words within a segment are hyphen-joined (underscores mark segment boundaries, so hyphens stay free for hyphenated surnames and the title itself). Author = first author's surname, capitalized, ASCII. Year = 4 digits, or `nd` when unverifiable from the PDF (then marked `[year unverified]` in INDEX). Title = the complete title from the title page (articles kept, subtitle included, punctuation stripped, TitleCase). Examples: `Austin_1956_A-Plea-for-Excuses.pdf`, `Shafer-Landau_2003_Moral-Realism-A-Defence.pdf`. Safety valve: stems over 100 characters truncate at the subtitle boundary (INDEX keeps the full title). KEYs stay `AUTHOR-TITLE` without year — the KEY is the stable identifier consumed by refs.md and the Citation Gate; the file stem is the locator. On an AUTHOR-TITLE collision, the newer entry's KEY appends the year.

**Language:**
- Definition layer (rules, commands, agents, skills, schemas, ARCHITECTURE, changelog, this file) — **English**.
- Writing output (manuscripts, analysis reports, review reports) — **Chinese**.
- Deliberate exceptions kept in **Chinese**: the two `README.md` files (user-facing docs) and the 5 report templates in `.claude/shared/templates/` (they are output skeletons — their headings become the headings of generated reports).

## Directory Structure

**Dual-repo structure (v0.4): the privacy boundary IS the repo boundary.** The outer repo contains only the framework (shareable); all papers, bibliography, and personal style samples live in `Private/` (gitignored by the outer repo; an independent inner git repo with a private remote).

```
.claude/       Framework executable layer (tracked by outer repo; lowercase — tool constraint)
  ├── settings.json   Permissions + hooks (committed)
  ├── commands/       8 composite commands (phil:* namespace)
  ├── rules/          3 behavioral rule modules
  ├── skills/         30 domain analysis skills (engine)
  ├── agents/         7 philosophy-specialized agents (3 dialogic + 4 production)
  ├── references/     Methodological knowledge (glossaries, argument forms, taxonomies)
  └── shared/         Data contracts (13 JSON schemas + 5 report templates)
Framework/     Framework non-executable layer (tracked by outer repo)
  ├── ARCHITECTURE.md System architecture document
  ├── changelog.md    Framework version history
  └── Lessons/        Distilled feedback-to-framework from individual projects
Shared/        Shareable curated knowledge (tracked by outer repo)
  ├── Philosophers-DB/  49 philosopher profiles (General/Metaphysics/Metaethics)
  └── Format/           Format templates (LaTeX/Word — shareable)
Private/       Private content layer (outer gitignore; independent inner repo, PDFs excluded)
  ├── Projects/{topic}/   One directory per writing project (manuscript, refs.md,
  │                       VERSIONS.md, feedback-to-framework.md, project-level CLAUDE.md)
  ├── Bibliography/       Master reference library (PDF/ in no git, Analysis/, INDEX.md)
  ├── Concepts/           Cross-project concept notes
  └── Style/              Personal writing samples (style calibration)

Memory: C:\Users\zhaok\.claude\projects\C--Projects-Philosophical-Writing\memory\
  Session-persistent knowledge (user preferences, project feedback, references)
```

## Commands Reference

| Command | Function | Runs |
|---------|----------|------|
| `phil:reconstruct` | Full-dimensional understanding of a source | 9-20 skills (mixed serial/parallel, auto domain detection) |
| `phil:evaluate` | Simultaneous multi-angle critique | 7 skills (fully parallel) |
| `phil:review` | Peer review | phil-reviewer agent (8 dimensions + perspective simulation) |
| `phil:write` | Philosophical writing | phil-writer agent (outline / draft / revision) |
| `phil:comment` | Argument detail and conceptual clarification | phil-commentator agent (6 critical dimensions) |
| `phil:pipeline` | One-command full pipeline | phil-orchestrator agent (5 stages with quality gates) |
| `phil:tutor` | Tutor-style literature dialogue — probe ideas, test understanding, recommend sources | phil-tutor agent (Socratic dialogue + 4-phase arc) |
| `phil:ingest` | Literature ingestion ("scraping") — scan library, rename to canonical stem, register in INDEX, Level 0.5 summary, recommendation trigger 1 | shell scan + pdf skill + phil-summarize |

Each command file in `.claude/commands/` defines its skill composition, execution order, and output format.

## Workflow Conventions

### Writing projects (Private/Projects/{topic}/)
- Plain text writing; no markup languages (final LaTeX is stored as .txt in the same directory; copy .txt → .tex temporarily at compile time)
- Manuscripts are written in Chinese
- Directory & filenames use English kebab-case of the project topic

**Per-project files:**
- `CLAUDE.md` — project-level conventions + topic keywords (used for literature-recommendation matching)
- `refs.md` — project-level reference list: `KEY | role (core-target/support/background) | status (cited/candidate/rejected) | notes`; each KEY points to the master library INDEX — zero file duplication
- `{topic}-draft.txt` — Working draft. Freely overwritten. Never versioned.
- `{topic}-v{N}.txt` — Cut version. Created from draft when a trigger fires.
- `{topic}-review.txt` — Review report.
- `VERSIONS.md` — This project's version history. Every cut version MUST be documented here with date, triggers, and description.
- `feedback-to-framework.md` — Framework defects discovered during writing; periodically distilled into `Framework/Lessons/`

**Version cut process:** Copy `{topic}-draft.txt` → `{topic}-v{N}.txt` → document in `VERSIONS.md`. The draft persists as the working copy for the next round.

### Bibliography (Private/Bibliography/) — master reference library, single source of truth

```
Private/Bibliography/
├── PDF/                              Original PDFs (in NO git — immutable, re-obtainable)
├── Analysis/                         Paired analysis files ({Author}_{Year}_{Title}.analysis.txt)
├── Summaries/                        Level 0.5 summaries ({Author}_{Year}_{Title}.summary.txt)
└── INDEX.md                          Master inventory (KEY, analysis level, topics tags)
```

**Analysis levels (progressive, append-only):**
- Level 0.5: Summary — core thesis + argument route + key concepts + interlocutors + topics — *trigger: PDF ingestion (`/phil:ingest` → phil-summarize)*
- Level 1: Argument reconstruction — *trigger: selected as a paper dependency*
- Level 2: + Implicit premises, charity audit, conceptual analysis, distinction tracking — *trigger: first citation in a manuscript*
- Level 3: + Dialectical mapping, ontological commitment, modal analysis, domain-specific skills — *trigger: source becomes core target/dependency*

**Three recommendation trigger points** (model-executed): (1) on ingestion — new source's topics matched against each project CLAUDE.md's topic keywords (executed by `/phil:ingest`); (2) during in-project work — phil:tutor scans INDEX for entries whose topics match but which are absent from this project's refs.md (skipping `rejected`); (3) on citation extraction — phil-citation-extract outputs acquisition_candidates.

### Citation Gate (Rule 2 enforcement, two-hop)
This is a model-executed behavioral rule:
1. **Hop 1**: the cited KEY must be registered in this project's `refs.md`
2. **Hop 2**: If a manuscript claim depends on analysis at Level N, but the source's `.analysis.txt` is only at Level N-1 or below → **BLOCK** and require analysis completion. No citation passes without a verified analysis backing it.

## Common Operations

### Interactive shell commands
Prefix with `!` to run in-session:
```
!ls "Private/Bibliography/PDF/"
!wc -m "Private/Projects/srinivasan-critique/srinivasan-critique-draft.txt"
```

### PDF Processing Workflow
1. Place PDF in `Private/Bibliography/PDF/`
2. Run `/phil:ingest` — extracts text via the `pdf` skill (**not** direct `pdftotext` CLI), renames to the canonical stem, registers in INDEX.md, generates the Level 0.5 summary, and runs recommendation trigger 1
3. When the source becomes a paper dependency, run `phil:reconstruct` → `Private/Bibliography/Analysis/{Author}_{Year}_{Title}.analysis.txt` (Level 1)
4. Escalate analysis level as needed per Citation Gate rules

### Manuscript Work Cycle
1. **Draft** in `Private/Projects/{topic}/{topic}-draft.txt`
2. **Review** with `phil:review` → review report
3. **Revise** draft → cut version when trigger fires
4. **Version cut**: `cp draft.txt v{N}.txt` + update `VERSIONS.md`

### LaTeX Compilation
```bash
cd "Private/Projects/{topic}" && cp topic.txt topic.tex && pdflatex topic.tex
```

### Character count
```bash
wc -m "Private/Projects/{topic}/{topic}-draft.txt"
```

### Committing the Private repo
Git operations for writing content happen inside `Private/` (independent repo, private remote). The outer repo never tracks `Private/` content.

### Session Logging
Session summaries are written to `history.txt` by the model at the end of each conversation, per the memory convention `session-summary-to-history`. The file is gitignored as a local log.

## Knowledge Base

**Argument Forms**: 26 canonical forms in `.claude/references/argument-forms/` (see `argument-forms/INDEX.md` for the general/metaphysics/metaethics breakdown).

**Glossaries & Taxonomies**: `.claude/references/` contains domain-specific reference files (glossary-metaphysics.md, glossary-metaethics.md, ontological-categories.md, causation-taxonomy.md, moral-realism-taxonomy.md, normativity-taxonomy.md, fallacy-catalog.md, modal-logic-primer.md, thought-experiment-templates.md).

**Philosopher Database**: `Shared/Philosophers-DB/` — 49 philosophers across 3 domains (General/Metaphysics/Metaethics). Curated — may be cited.

**Data Contracts**: `.claude/shared/` — 13 JSON schemas for cross-skill composability + 5 report templates in `.claude/shared/templates/` (templates deliberately in Chinese — output skeletons).

## Cross-Session Memory

Persistent file-based memory at `C:\Users\zhaok\.claude\projects\C--Projects-Philosophical-Writing\memory\`. Each memory is a `.md` file with frontmatter. `MEMORY.md` serves as the session index.

Write memories for: user preferences, project goals, substantive feedback, external references. Do NOT memory code structure, git history, or CLAUDE.md contents — those are already in the repo.

## Architecture

The complete system architecture is defined in `Framework/ARCHITECTURE.md` (0.4-alpha), built atop `academic-research-skills` v3.15.0 (external plugin — all `ars-*` capabilities require this plugin to be installed), covering three subdomains: general analytic philosophy, metaphysics, and metaethics.

- **30 Skills** — Phase 1-6 complete. All skills in `.claude/skills/`
- **8 Commands** — Composite orchestration in `.claude/commands/`
- **7 Agents** — 3 dialogic (metaphysician, metaethicist, phil-tutor) + 4 production (writer, reviewer, commentator, orchestrator). All in `.claude/agents/`
- **13 JSON Schemas + 5 Report Templates** — Data contracts in `.claude/shared/`
- **26 Argument Forms** — Canonical definitions in `.claude/references/argument-forms/`
- For complete skill inventory, build roadmap, and detailed architecture — see `ARCHITECTURE.md`
