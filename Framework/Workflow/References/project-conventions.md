# Project Conventions

Detailed conventions kept out of the always-loaded `AGENTS.md`. Read the relevant section before ingesting sources, creating a project, cutting a version, or working with Zotero.

## Naming & Language Conventions

**Directory naming:**
- Every non-hidden framework or content directory starts with an uppercase letter (`Framework/`, `Shared/`, `Private/`, `Private/Projects/`, `Private/Bibliography/PDF/`). Hyphenated names capitalize each segment; acronyms stay uppercase (`Philosophers-DB`).
- Exception 1: hidden host directories (`.claude/`, `.agents/`, `.claude-plugin/`) and the plugin's `skills/` directory keep the names their hosts require.
- Exception 2: content-item directories (individual project topics, e.g. `Private/Projects/srinivasan-critique/`) use lowercase English kebab-case, matching their filename prefix (`srinivasan-critique-draft.txt`).
- Filenames use lowercase kebab-case, except conventional uppercase files (`AGENTS.md`, `README.md`, `INDEX.md`, `VERSIONS.md`, `ARCHITECTURE.md`, `MEMORY.md`).
- Exception 3 — bibliography stems: files in `Private/Bibliography/` share the canonical stem `{Author}_{Year}_{Title}` across `.pdf` / `.analysis.md` / `.summary.md`. Segments are separated by **underscores**; words within a segment are hyphen-joined (underscores mark segment boundaries, so hyphens stay free for hyphenated surnames and the title itself). Author = first author's surname, capitalized, ASCII. Year = 4 digits, or `nd` when unverifiable from the PDF (then marked `[year unverified]` in INDEX). Title = the complete title from the title page (articles kept, subtitle included, punctuation stripped, TitleCase). Examples: `Austin_1956_A-Plea-for-Excuses.pdf`, `Shafer-Landau_2003_Moral-Realism-A-Defence.pdf`. Safety valve: stems over 100 characters truncate at the subtitle boundary (INDEX keeps the full title). KEYs stay `AUTHOR-TITLE` without year — the KEY is the stable identifier consumed by refs.md and the Citation Gate; the file stem is the locator. On an AUTHOR-TITLE collision, the newer entry's KEY appends the year.
  - **Books (monographs and edited collections)**: Author segment = first author's surname for a monograph, **first editor's surname** for a collection (e.g. `Chalmers_2009_Metametaphysics.pdf`). One physical volume PDF only — never split into per-chapter files. A **monograph** is one INDEX row; its chapters are segments inside the single `.summary.md`, not separate rows. An **edited collection** (or a single author's self-collection of previously published papers) gets a volume row (KEY `EDITOR-TITLE`) **plus one row per member paper** (KEY `AUTHOR-TITLE` of that paper); the member row's PDF column points at the shared volume file with a page range and container KEY (`PDF/{volume-stem}.pdf, pp. X–Y, in {VOLUME-KEY}`), and its summary is an independent `{chapter-author}_{volume-year}_{chapter-title}.summary.md`. The type test is whether chapters are independent, separately-citable works — not author count.

**Language:**
- Definition layer (rules, commands, agents, skills, schemas, ARCHITECTURE, changelog, this file) — **English**.
- Writing output (manuscripts, analysis reports, review reports) — **Chinese**.
- Deliberate exceptions kept in **Chinese**: the two `README.md` files (user-facing docs) and the 5 report templates in `Framework/Workflow/Templates/` (they are output skeletons — their headings become the headings of generated reports).

## Removed Entrypoints

No aliases are retained (0.7.0-alpha).

| Removed command | Use instead |
|---|---|
| `phil:reconstruct` | `phil:research reconstruct` |
| `phil:evaluate` | `phil:research evaluate` |
| `phil:comment` | `phil:research comment` |
| `phil:ingest` | `phil:research ingest` |
| `phil:philosophers` | `phil:research philosophers` |
| `phil:pipeline` | `phil:full start` |

`phil:tutor`, `phil:write`, and `phil:review` keep their names, now bound directly to the canonical skills. The deterministic resolver: `workflow-policy.py removed-entrypoint <command>`.

## Workflow Conventions

### Writing projects (Private/Projects/{topic}/)
- Manuscripts (`-draft.txt`, `-v{N}.txt`) are plain text with no markup (final LaTeX is stored as .txt in the same directory; copy .txt → .tex temporarily at compile time)
- Every other generated file is Markdown (`.md`): conception, outline, review reports, argument sheets, pipeline prose and logs, summaries, analyses. Older `.txt` intermediates stay readable; create new ones as `.md`
- Manuscripts are written in Chinese
- Directory & filenames use English kebab-case of the project topic
- Resolve project guidance in this order: `PROJECT.md`, `AGENTS.md`, then a legacy `CLAUDE.md`. New projects use `PROJECT.md` plus the generated `AGENTS.md` pointer.
- Each project declares its draft collaboration mode via `collaboration: user-led | assistant-led`; legacy `claude-led` and `codex-led` values normalize to `assistant-led` with a deprecation notice.

**Per-project files:**
- `PROJECT.md` — platform-neutral project conventions + topic keywords (new-project standard)
- `AGENTS.md` — generated pointer to the root guide
- `glossary.md` (optional) — fixed English → Chinese renderings, a table `| English | 中文 | 备注 |`; `避免：A、B` in 备注 lists variants to avoid. One file serves `translate.py --project` and `prose-lint.py --glossary` in `phil:write` pass 3, so the manuscript and the reading page use the same terms
- `refs.md` — project-level reference list: `KEY | role (core-target/support/background) | status (cited/candidate/rejected) | notes`; each KEY points to the master library INDEX — zero file duplication
- `{topic}-conception.md` — Conception notes from ideation (Stage 3, `phil:tutor` incubating mode). Freely overwritten. Never versioned. Consumed by `phil:write outline`.
- `{topic}-outline.md` — Human-readable outline produced by `phil:write outline` and consumed by draft mode; the approval gate hashes this artifact.
- `{topic}-idea-ledger.json` — Structured living registry for substantive ideas that were activated, parked, rejected, or superseded. Never versioned and never silently deletes an idea.
- `{topic}-workflow-state.json` — Cross-session pipeline state (schema v2): run, stage, status, collaboration mode, artifact hashes, approvals (conception/outline/review/citation-closure), review-finding ledger, section audit, and derived next action. Maintained via `Scripts/project-state.py`. Never versioned as manuscript content.
- `{topic}-draft.txt` — Working draft. Freely overwritten. Never versioned.
- `{topic}-v{N}.txt` — Cut version. Created from draft when a trigger fires.
- `{topic}-review.md` — Review report.
- `VERSIONS.md` — This project's version history. Every cut version MUST be documented here with date, triggers, and description.
- `feedback-to-framework.md` — Framework defects discovered during writing; periodically distilled into `Framework/Lessons/`

**Version cut process:** Copy `{topic}-draft.txt` → `{topic}-v{N}.txt` → document in `VERSIONS.md`. The draft persists as the working copy for the next round.

### Bibliography (Private/Bibliography/) — master reference library, single source of truth

```
Private/Bibliography/
├── PDF/                              Original PDFs (tracked in the private repository)
├── Analysis/                         Paired analysis text + verification metadata (`.analysis.meta.json`)
├── Summaries/                        Level 0.5 summaries ({Author}_{Year}_{Title}.summary.md)
├── Extract/{stem}/                   Evidence units from pdf-extract.py (derived, not tracked)
├── Reader/{stem}/                    Reading page: translation*.jsonl, agent-notes.json, user-notes.json, reader.json (tracked);
│                                     reader.html built by reader-build.py (derived, not tracked);
│                                     reader-serve.py serves it locally and saves annotations to user-notes.json;
│                                     notes-routed.json records which notes reader-notes.py routed to a project
├── Philosopher-Queue/                 Private observations, counters, and review candidates
└── INDEX.md                          Master inventory (KEY, analysis level, topics tags)
```

**Analysis levels (progressive, append-only):**
- Level 0.5: Summary — core thesis + argument route + key concepts + interlocutors + topics — *trigger: PDF ingestion (`phil:research ingest` → `method.dialectic.summarize`)*. A monograph's summary carries per-chapter segments; an edited collection yields a volume summary plus one independent summary per member paper.
- Level 1: Argument reconstruction — *trigger: selected as a paper dependency*
- Level 2: + Implicit premises, charity audit, conceptual analysis, distinction tracking — *trigger: first citation in a manuscript*
- Level 3: + Dialectical mapping, ontological commitment, modal analysis, domain-specific skills — *trigger: source becomes core target/dependency*

**Three recommendation trigger points** (model-executed): (1) on ingestion — new source's topics matched against each project's `PROJECT.md` topic keywords (executed by `phil:research ingest`); (2) during in-project work — phil:tutor scans INDEX for entries whose topics match but which are absent from this project's refs.md (skipping `rejected`); (3) on citation extraction — `method.dialectic.citation-extract` outputs acquisition_candidates.

### Citation Gate (Rule 2 enforcement, two-hop)
The semantic claim-to-source judgment is model-executed; artifact verification is deterministic:
1. **Hop 1**: the cited KEY must be registered in this project's `refs.md`
2. **Hop 2**: The paired `.analysis.meta.json` must exist, declare at least Level N, have `verification_status: verified`, and match the current PDF and analysis SHA-256 hashes. Missing, provisional, stale, hash-mismatched, or shallow analyses → **BLOCK**. The INDEX level is an inventory view, not sufficient verification evidence.

## Reusability & Token Economy

Distilled from live runs (v0.4.2–v0.4.5). Goal: spend tokens on philosophy, not plumbing — without degrading capability (when a cheap path is insufficient, escalate; never guess).

1. **Capability lookup order**: dedicated tools (file tools, `Scripts/pdf-extract.py` for PDFs) → Zotero MCP/tools → `Framework/Workflow/Scripts/` → only then write new code. Before writing any helper, check `Framework/Workflow/Scripts/` and `Framework/Lessons/` for a prior solution.
2. **Solidify on second use**: an inline solution needed twice becomes a parameterized script in `Framework/Workflow/Scripts/` (secrets from user-level runtime configuration; proxy + retries built in; documented in changelog). Precedent: `zotero-attach-linked.py` — its urllib/proxy/retry logic is never rewritten inline.
3. **Batch over loop**: with 2+ items, use batch variants — `zotero-attach-linked.py --parents` (single POST, auto-split at 50), `zotero_get_items_children`, `zotero_batch_update_tags` — instead of N single calls.
4. **Read at the cheapest sufficient level**: INDEX row → `.summary.md` (Level 0.5) → `.analysis.md` → PDF outline / page range → full text. Never run full-text extraction to answer what a summary already answers. Full-text reads are justified only by the analysis-level escalation triggers (Citation Gate) or an explicit read request.
5. **Validated methods are settled**: procedures marked verified in `Framework/Lessons/` (e.g. the annotation-preserving stored→linked migration) are executed, not re-tested. Check `history.txt` / changelog / Lessons before re-investigating a known problem.
6. **Environment facts are read, not re-probed**: network proxy, Zotero hybrid MCP mode, API-key location, the 50-item write-batch cap — all recorded in user-level runtime guidance, Lessons, and memory.
7. **Cost-aware delegation**: No workflow or role selects a provider or concrete model. Treat economical model use as a session-scoped prompt policy, not a static mapping or automatic router. When the first eligible task appears, ask once whether a lower-cost host candidate may be reused for this session; the user may revoke it at any time, after which no further delegation is requested in that session, and new sessions ask again. Eligible work is repeatable, independent, read-only, non-interactive, and produces only discardable candidate artifacts. The parent task must validate candidates before writing files, treating claims as verified, or using them in the Citation Gate. Writing, review, Citation Gate decisions, bibliography or project changes, user dialogue, and orchestration retain the current model. If the authorized candidate is unavailable or insufficient, retain the current model rather than choose another. Do not claim a candidate is optimal without host-provided cost, cache, latency, and quality evidence. Reconstruction and evaluation run a deterministic preplan before loading selected skills; examples and checklists remain unloaded unless a live ambiguity or explicit request requires them.
8. **State before rereading**: Query the compact idea-ledger/workflow-state helpers before loading full artifacts. Hash-valid persisted outputs are reused; stale outputs are reported rather than silently trusted.

## Common Operations

### Interactive shell commands
Prefix with `!` to run in-session:
```
!ls "Private/Bibliography/PDF/"
!wc -m "Private/Projects/srinivasan-critique/srinivasan-critique-draft.txt"
```

### PDF Processing Workflow
1. Place PDF in `Private/Bibliography/PDF/`
2. Run `phil:research ingest` — extracts text with `Scripts/pdf-extract.py`, renames to the canonical stem, registers in INDEX.md, generates the Level 0.5 summary, and runs recommendation trigger 1
3. When the source becomes a paper dependency, run `phil:research reconstruct` → `Private/Bibliography/Analysis/{Author}_{Year}_{Title}.analysis.md` (Level 1)
4. Escalate analysis level as needed per Citation Gate rules

### Zotero Integration
→ Full workflow: [Framework/Lessons/zotero-integration.md](Framework/Lessons/zotero-integration.md)

`Private/Bibliography/PDF/` is Zotero's Linked Attachment Base Directory — one physical PDF repository, two consumers (Zotero reads via linked attachments; the framework reads via canonical stems). Core invariants:

- **Naming ownership belongs to the framework**: rename to the canonical stem *before* linking in Zotero; never rename after. Zotero must never auto-rename linked files.
- **INDEX.md `Zotero` column**: `KEY ↔ Zotero item key ↔ file stem` three-way mapping (`—` = not in Zotero).
- **Fixed order for new PDFs**: ingest first, then link in Zotero. Step 8 uses DOI-first → ISBN → bibtex and `Framework/Workflow/Scripts/zotero-attach-linked.py`; when the full Zotero backend is unavailable, Steps 1–7 still complete and Step 8 reports `partial` or `skipped` with a manual follow-up.
- **Lazy migration**: stored attachments are migrated only when their collection becomes a writing project — no bulk sweeps. Zotero collections are not mirrored as directories.
- **MCP mode**: hybrid — reads on local SQLite (`ZOTERO_LOCAL=true`), writes via user-level credentials; cloud writes land locally only after a desktop sync. Zotero-imported metadata is unreliable, so title-page verification applies on this inflow path too.

### Manuscript Work Cycle
0. **Orchestrate end-to-end**: `phil:full start` — state machine from intake to citation closure (`start` / `status` / `resume`)
1. **Incubate**: `phil:tutor incubating` → `{topic}-conception.md` (thesis + argument sketch in the user's own words)
2. **Draft** in `Private/Projects/{topic}/{topic}-draft.txt`
3. **Review** with `phil:review` → review report
4. **Revise** draft → cut version when trigger fires
5. **Version cut**: `cp draft.txt v{N}.txt` + update `VERSIONS.md`

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

**Argument Forms**: 26 canonical forms in `Framework/Workflow/References/argument-forms/` (see `argument-forms/INDEX.md` for the general/metaphysics/metaethics breakdown).

**Glossaries & Taxonomies**: `Framework/Workflow/References/` contains domain-specific reference files.

**Philosopher Database**: `Shared/Philosophers-DB/` — canonical claim-level JSON profiles plus generated domain views. `source-backed` claims route to bibliography evidence; `prompt-only` claims are `[source unverified]` discovery hints and cannot bypass the Citation Gate.

**Data Contracts**: `Framework/Workflow/Schemas/` contains 17 JSON schemas; `Framework/Workflow/Templates/` contains the report templates.
