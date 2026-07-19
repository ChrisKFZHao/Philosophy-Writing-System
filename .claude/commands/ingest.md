---
description: "Literature ingestion (\"scraping\") — scans the bibliography for unprocessed PDFs, renames them to the canonical stem, registers them in INDEX.md, generates Level 0.5 summaries, batch-records philosopher observations, runs recommendation trigger point 1, and auto-registers sources in Zotero as linked-file items"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->
# /phil:ingest

## Usage

```
/phil:ingest                    # scan the whole library, process every unprocessed PDF
/phil:ingest <pdf-filename>     # process a single PDF (filename relative to Private/Bibliography/PDF/)
/phil:ingest --dry-run          # report what would be done without changing anything
/phil:ingest --force <KEY>      # regenerate the summary for an already-processed entry
```

## Positioning

The **entry point of the PDF Processing Workflow** (media-library "scraper" analogy): whenever new PDFs land in `Private/Bibliography/PDF/`, this command normalizes them into the library. It implements **recommendation trigger point 1** (on ingestion — new source topics matched against each project's guidance-file keywords).

Relation to phil:reconstruct:
- **ingest** performs cheap intake: rename + register + Level 0.5 summary (the lowest analysis rung)
- **reconstruct** performs deep analysis: Level 1+ argument reconstruction, escalated per Citation Gate rules
- Order: PDF added → `/phil:ingest` → (when the source becomes a paper dependency) `phil:reconstruct`

## Orchestration

| Component | Description |
|-----------|-------------|
| Shell set-comparison | Step 1 scan: programmatic diff of PDF directory vs INDEX registrations (no model reading) |
| `pdf` skill | Text + title-page metadata extraction (never `pdftotext` CLI directly); for books, also the copyright-page ISBN and the table of contents |
| `phil-summarize` skill | Level 0.5 summary generation (pure function; this command writes the file) — paper / monograph (chapter segments) / collection (per-paper summaries) modes |
| `philosopher-db.py` | Batch-ingests compact philosopher observations into the private review queue; never approves semantic content |
| zotero MCP + web API | Step 8 Zotero registration (book cascade DOI → ISBN → bibtex): `zotero_add_by_doi` (paper; book/chapter DOIs — preferred for collection members), `zotero_add_by_isbn` (book, if no DOI), `zotero_add_by_bibtex` (`@book`/`@incollection` fallback when resolvers fail); the raw web API attaches linked files (single or batch, cloud write) |

## Steps

### Step 1: Scan (MUST be programmatic — token-economy hard requirement)

Detect unprocessed PDFs with the deterministic scanner. **Do not read the directory listing or INDEX.md into the model to make this judgment.**

```bash
python "Framework/Workflow/Scripts/bibliography-scan.py" --json
```

A PDF is **unprocessed** if ANY of:
1. Its filename does not match the canonical stem pattern `^[^_]+_(\d{4}|nd)_.+\.pdf$`
2. No INDEX inventory row's PDF column references it
3. `Private/Bibliography/Summaries/{stem}.summary.txt` does not exist

The model consumes only the resulting difference set (a few filenames). Expensive steps (extraction, metadata, summary) run only for PDFs in that set. A clean library yields "0 unprocessed" — the command is idempotent and doubles as a consistency checker.

### Step 2: Extract (per unprocessed PDF)

Use the `pdf` skill to extract full text plus title-page metadata: author(s), year, complete title, venue. **Rule 2: metadata must be read from the PDF itself — never recalled from model memory.** If the year is absent from the PDF, ask the user once for this item (other PDFs in the batch proceed); if the user cannot verify, use `nd` in the stem and mark `[year unverified]` in INDEX.

**Determine the document type** — `paper` / `monograph` / `collection` — from the title page and table of contents. The test is **whether the chapters are independent works**, not the number of authors:
- `paper` — a journal article or standalone preprint (the default; skip the book-specific extraction below).
- `monograph` — a book whose chapters form one continuous argument by one author (or co-authors throughout). Chapters are **not** independently citable works.
- `collection` — an edited volume (or a single author's self-collection of previously published papers) whose chapters are independent, separately-authored, separately-citable works.

For `monograph` and `collection`, additionally extract (Rule 2, from the PDF):
- the **ISBN** from the copyright page and any **DOIs** (whole-book DOI from the copyright page; each chapter's DOI from its first-page footer) — used by Step 8's book cascade (DOI-first → ISBN → bibtex);
- the **table of contents** — chapter/part numbers, titles, and page ranges; for a collection, each chapter's **author(s)** as printed. This drives per-chapter segments (monograph) or per-paper rows and summaries (collection).

### Step 3: Dedupe

Match extracted metadata (author surname + title keywords) against existing INDEX rows. If an existing row matches under a different PDF filename, this is a duplicate or a retrofit case — **ask the user before creating a second entry**; never auto-create a second KEY for the same work.

### Step 4: Rename

Compute the canonical stem `{Author}_{Year}_{Title}`:
- Segments separated by **underscores**; words within a segment joined by hyphens (underscore = segment boundary; hyphens stay free for hyphenated surnames and the title itself)
- Author = first author's surname, capitalized, ASCII. **For a `collection`, use the first editor's surname** (e.g. `Chalmers_2009_Metametaphysics.pdf` for Chalmers, Manley & Wasserman eds.)
- Year = 4 digits or `nd`
- Title = the **complete title** from the title page (articles kept, subtitle included, punctuation stripped, TitleCase, hyphen-joined). Examples: `Austin_1956_A-Plea-for-Excuses.pdf`, `Shafer-Landau_2003_Moral-Realism-A-Defence.pdf`
- Path safety valve: if the stem exceeds 100 characters, truncate at the subtitle boundary; INDEX keeps the full title with a note

**One physical file per volume.** A monograph or collection PDF is renamed as a single volume file — never split into per-chapter PDFs and never copied. Member papers of a collection point at this one volume file with a page range (Step 5); their own `.summary.txt` / `.analysis.txt` carry chapter-level stems but no separate PDF.

Then:
- Rename the PDF with plain `mv` (PDFs are in no git); quote paths (repo root contains a space)
- If a paired analysis file exists under an old stem, `git mv` it inside `Private/` to the new stem and update its header lines to reference the canonical PDF path

### Step 5: Register

Insert or update (never duplicate) the INDEX inventory row: KEY, Author, Title (complete), PDF path, Analysis Level, Topics. KEY format stays `AUTHOR-TITLE` (no year — KEY is the stable identifier consumed by refs.md and the Citation Gate; the file stem is the locator). On an AUTHOR-TITLE collision, the newer entry appends the year: `AUTHOR-TITLE-1998`. Refresh the "Last updated" footer.

By document type:
- **paper / monograph** — one row (the whole work). The monograph's chapters do **not** get their own rows; they live as segments inside the one summary file.
- **collection** — a **volume row** plus **one row per member paper**:
  - *Volume row*: KEY = `EDITOR-TITLE`; PDF column = the volume file; owns the Zotero `book` item; Topics span the whole volume.
  - *Member-paper rows*: KEY = `AUTHOR-TITLE` of that paper (standard convention; collision → append year). The **PDF column points at the shared volume file plus the page range and container KEY**, e.g. `PDF/Chalmers_2009_Metametaphysics.pdf, pp. 347–383, in CHALMERS-METAMETAPHYSICS`. Topics are the member paper's own. This is what makes each member independently citable — refs.md registers the member KEY, and the two-hop Citation Gate reads the member row's analysis level.

### Step 6: Summarize

Invoke `phil-summarize` with the extracted text + verified metadata + document type; write the result(s) to `Private/Bibliography/Summaries/`. Create `Summaries/` on first run. Levels are append-only: set Analysis Level to 0.5 only if the row was below it; a higher-level entry keeps its level but still gains the summary file (the recommendation substrate).

By document type:
- **paper** — one file `Summaries/{stem}.summary.txt`. (Unchanged.)
- **monograph** — one file `Summaries/{stem}.summary.txt` containing the volume-level summary **plus per-chapter segments** (`chapters[]`, ~150–300 chars each), driven by the Step 2 table of contents.
- **collection** — a **volume summary file** `Summaries/{volume-stem}.summary.txt` (`collection` mode: editors' framing + structural arc) **plus one independent file per member paper**, `Summaries/{chapter-author}_{year}_{chapter-title}.summary.txt` (year = the volume's year), each a full single-paper summary with its own topics and a `container` field (volume KEY + page range). Member files are flat in `Summaries/` (no subdirectory).

### Step 6B: Record philosopher observations (one deterministic batch)

After all summary files in this ingestion batch are written, pass them to the maintenance script in one invocation, repeating `--input` for each file:

```bash
python "Framework/Workflow/Scripts/philosopher-db.py" observe --input <summary-1> --input <summary-2>
```

The script derives source authors, resolves known aliases, records source/role counts, creates private review candidates, and updates only domain connections that meet the deterministic two-source/one-central-source threshold. It never approves a claim. Identical summary ID/hash pairs are no-ops; a changed artifact supersedes its pending candidates. With `--dry-run`, pass `--dry-run` here too and perform no queue or profile write. Report the number of changed artifacts, pending candidates, and domain updates.

### Step 7: Recommend (trigger point 1)

For each `Private/Projects/*/`, resolve guidance as `PROJECT.md`, then `AGENTS.md`, then `CLAUDE.md`. Match the summary's `topics[]` against its `## 主题关键词` or `## Topic Keywords` list. Report overlaps per project and **offer** (never auto-write) `candidate` rows for that project's refs.md. Skip KEYs already present in that refs.md under any status, including `rejected`.

For a **collection**, match **each member paper's own topics** (not just the volume's) — a single collection often contributes candidate references to several different projects. Offer the member paper's KEY (not the volume KEY) as the candidate, since that is the citable unit.

### Step 8: Zotero registration (identifier-gated, cloud write)

Auto-create the Zotero item(s) and attach the canonical PDF as a **linked file**, so batch ingestion never requires manual "Attach Link to File" clicks. This step writes to the Zotero cloud; new items land in the local Zotero UI only after a desktop sync.

Classify the runtime backend before doing any write, following `Framework/Workflow/Rules/runtime-compatibility.md`:
- `full`: Zotero MCP write tools plus the linked-file helper are available; run this step normally.
- `partial`: only a local Zotero plugin/API is available; do not create metadata or linked files, and report a manual follow-up.
- `skipped`: no Zotero backend is available; complete Steps 1-7 and report a manual follow-up.

When `--dry-run` is present, report the detected backend but skip every Step 8 write.

**Identifier gate: DOI-first, then ISBN, then bibtex/manual.** Read every identifier from the PDF (Rule 2, never from model memory):
- `paper` — try the **DOI** (§8A).
- `monograph` / `collection` — a **fallback cascade** (§8B), *not* ISBN-only: scholarly-press ISBNs are frequently absent from Open Library / Google Books while the publisher registers CrossRef DOIs (validated 2026-07-14 on Oxford Studies in Metaphysics Vol. 12 — both ISBNs and the whole-book DOI failed to resolve, yet every chapter DOI resolved cleanly). Try, in order: (1) the **whole-book DOI** and, for a collection, the **per-chapter DOIs**; (2) the copyright-page **ISBN**; (3) resolver-independent creation from verified metadata via `zotero_add_by_bibtex` (`@book` / `@incollection`).

If nothing resolves and no verified metadata is available to build a bibtex entry, skip the automation for that item, leave its INDEX `Zotero` column as `—`, and add a **manual-follow-up block** to the report (New Item → verify metadata → Attach Link to File → report the item key back for INDEX backfill).

#### 8A. Paper (DOI path) — unchanged

a. **Create the parent item (metadata only, no stored copy):**
   `zotero_add_by_doi(doi=<verified DOI>, attach_mode='none', if_exists='skip')`.
   - `attach_mode='none'` guarantees no stored PDF copy is ever created (preserves the one-physical-repository invariant).
   - `if_exists='skip'` prevents duplicating an item already in Zotero. If the tool reports the item already exists, look up its parent key (e.g. `zotero_search_items` by title/DOI) and proceed to the attach step with that key.

b. **Capture the parent item key** from the tool result. **Never round-trip the key through a subagent return value** — a proxy-side redaction filter rewrites `KEY:`-like lines to `[密钥]`. Write the key directly into INDEX from this command's own context.

c. **Cross-check CrossRef metadata against the title-page metadata from Step 2** (Rule 2 — aggregators mis-attribute authors, e.g. JSTOR listing journal editors as co-authors). If title, author list, or year diverge, correct via `zotero_update_item(item_key=<parent>, ...)`.

d. **Attach the canonical PDF as a linked file** (single-parent mode, step 8C).

e. **Backfill the INDEX row's `Zotero` column** from `—` to the parent key.

#### 8B. Monograph / collection (book cascade: DOI → ISBN → bibtex)

Try the sub-steps in order; stop at the first that yields a clean item. Every create uses `attach_mode='none'` (or a tool that attaches nothing) to preserve the one-physical-repository invariant.

a. **DOI attempt** (preferred — CrossRef metadata is the most reliable):
   - *Whole-book DOI* (copyright page): `zotero_add_by_doi(doi=<book DOI>, attach_mode='none', if_exists='skip')` creates a `book`. Scholarly-press whole-book DOIs sometimes fail on CrossRef even when chapter DOIs resolve — if it fails, **do not stop; continue**.
   - *Collection member DOIs* (each chapter's first-page footer; OUP/OSO uses a systematic `…/<book-doi>.003.000N` scheme, N = chapter number): `zotero_add_by_doi` per chapter creates a clean `bookSection` with CrossRef metadata. **This is the preferred member-creation path** — CrossRef-verified, superior to hand-built `@incollection` bibtex. Cross-check each returned title against the Step 2 TOC (CrossRef occasionally drops a subtitle — keep the full title in INDEX/summary). If the whole-book DOI failed but chapter DOIs work, create the `book` volume item via sub-step (c). CrossRef over the proxy is flaky — retry transient SSL/EOF failures per DOI (they are network errors, not wrong DOIs).

b. **ISBN attempt** (only if no usable DOI): `zotero_add_by_isbn(isbn=<verified ISBN>, if_exists='skip')` (creates a `book`). `zotero_add_by_isbn` has **no `attach_mode` parameter** — the ISBN resolvers (Open Library / Google Books) normally have no OA PDF, so no stored copy should result, but **verify via `zotero_get_item_children`** and trash any stored attachment that appears. Open Library / Google Books metadata is *less* reliable than CrossRef → title-page cross-check is mandatory.

c. **bibtex fallback** (neither resolver finds the item, but Step 2 gave verified metadata): `zotero_add_by_bibtex` with an `@book` entry for the volume and, for a collection, one `@incollection` entry per member (fields from the verified TOC: `author` = chapter author, `title` = chapter title, `booktitle` = volume title, `editor`, `year`, `pages`, `publisher`), `attach_mode='none'`. Resolver-independent and fully Rule-2-grounded (this is how the OSM Vol. 12 `book` item was created after both ISBNs and the whole-book DOI failed).

d. **Capture keys** (book key + each member key) directly from tool results (same no-subagent-return rule as 8A-b).

e. **Cross-check metadata** against the Step 2 title-page/TOC values regardless of which path produced the item; correct via `zotero_update_item`.

f. **Attach the canonical volume PDF as a linked file** to the book item and, for a collection, **to every member item as well** — one physical file, many linking items — via batch mode (step 8C).

g. **Backfill INDEX**: the volume row's `Zotero` column = book key; each member-paper row's `Zotero` column = its bookSection key.

#### 8C. Linked-file attachment (shared helper)

The Zotero MCP has no linked-file-creation tool; use the reusable helper `Framework/Workflow/Scripts/zotero-attach-linked.py`. It reads credentials from process environment variables or the active runtime's user-level configuration, never from repository files. It uses the configured proxy, falling back to `127.0.0.1:6789`, retries transient failures, and prints only resulting attachment keys:

```bash
# single parent (paper, or a monograph's book item)
python "Framework/Workflow/Scripts/zotero-attach-linked.py" --parent <parent-key> --stem <canonical-stem>.pdf --verify

# batch — collection: the book item + every bookSection, one POST, same volume stem
python "Framework/Workflow/Scripts/zotero-attach-linked.py" --parents <book-key>,<sec1-key>,<sec2-key>,... --stem <volume-stem>.pdf --verify
```

It emits the `linked_file` payload `{"path":"attachments:<stem>.pdf", ...}` (`attachments:` = base-directory-relative, survives machine moves). `--verify` GETs each new attachment back to confirm `linkMode`/`path`. A new-item POST needs no `If-Unmodified-Since-Version` (that header is only for key-based PATCH/DELETE). Batch mode prints `ATTACHMENT_KEY <parent> <key>` per line and auto-splits at Zotero's 50-item cap. Capture the printed keys from stdout — do not route them through a subagent return value.

**Collections are not auto-filed** — Zotero collections stay user-managed (lazy-migration principle). Remind the user in the report to file the new item(s) into a collection manually if desired.

## Output Format

Batch report (in Chinese, project convention):

1. **总览** — scanned N / unprocessed M / processed / skipped / needs-year；每篇标注类型（paper / monograph / collection）
2. **逐文献块** — original name → canonical name; KEY; document type; actions taken (renamed / registered / analysis-renamed / summarized / skipped + reason); topics; per-project recommendation hits (or "已登记，抑制推荐"); **Zotero 状态**（`full` / `partial` / `skipped`，以及已建条目、已存在条目或手动步骤）
   - **论文集额外列出各成员论文**：成员 KEY、页码范围、成员摘要文件、各自的推荐命中、各自的 bookSection `<key>`
3. **尾注** — INDEX consistency notes; follow-ups surfaced (e.g., provisional analyses whose PDF is now available for verification); **Zotero 桌面同步提醒**（新建条目须桌面端同步一次后才出现在本地界面）+ 任何解析全失败的手动待办；书籍入库所走的级联层级（DOI/ISBN/bibtex，注明哪一级命中）；若走了 ISBN 路径，附 `zotero_add_by_isbn` 未产生 stored 副本的核验结果

## Notes

- Write all output in Chinese (project convention); filenames, KEYs, and topics remain in English
- PDFs never enter git; analysis/summary renames use `git mv` inside the inner `Private/` repo
- Year and complete title must come from the PDF title page (Rule 2); fallback chain: read PDF → ask user → `nd` + `[year unverified]`
- On dedupe ambiguity (same work, different file), ask — do not create a second KEY
- Document type is decided by **whether chapters are independent works**, not author count: monograph = one continuous argument (chapters are segments, not INDEX rows); collection = independent separately-citable papers (each gets its own row, summary file, and bookSection); a single author's self-collection of previously published papers is a collection
- One physical PDF per volume — never split or copy; collection member rows point at the shared volume file + page range + `in <volume-KEY>`
- `--dry-run` performs Step 1 (and metadata peeks where needed for reporting) but writes nothing — it **skips Step 8 entirely** (Step 8 writes to the Zotero cloud)
- Step 8 is identifier-gated: **paper → DOI**; **book → cascade DOI-first (whole-book and, for collections, per-chapter DOIs) → ISBN → `@book`/`@incollection` bibtex**; nothing resolves and no metadata → manual-follow-up block. Per-chapter DOIs are preferred over hand-built `@incollection` bibtex when present (CrossRef-verified). Rule 2 (title-page verification) applies to CrossRef *and* Open Library / Google Books metadata (the latter is less reliable — cross-check is mandatory), and to CrossRef's own output (it may drop subtitles). `zotero_add_by_isbn` has no `attach_mode`; verify no stored copy when the ISBN path is used. Zotero collections are never auto-filed
- Zotero credentials are read from process environment variables or the active runtime's user-level configuration and are never hardcoded or echoed; item keys are written straight into INDEX, never passed through subagent return values (proxy redaction rewrites `KEY:` lines to `[密钥]`)
