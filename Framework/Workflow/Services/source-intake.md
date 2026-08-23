---
id: service.source-intake
kind: service
authority: write — may rename PDFs, register INDEX rows, write summaries, and enqueue philosopher observations
consumers: [phil-research/ingest]
scripts: [bibliography-scan.py, philosopher-db.py]
safety: "--dry-run is the default safety path; a dry run writes nothing"
---

# Source Intake Service

Normalizes new PDFs into the master library: deterministic scan, title-page extraction, canonical rename, INDEX registration, Level 0.5 summaries, philosopher observations, and recommendation trigger point 1. Zotero writes are owned by the separate `service.zotero-registration`.

## Step 1: Scan (deterministic — token-economy hard requirement)

Detect unprocessed PDFs programmatically. **Never read the directory listing or INDEX.md into the model to make this judgment.**

```bash
python "Framework/Workflow/Scripts/bibliography-scan.py" --json
```

A PDF is **unprocessed** if ANY of: (1) filename does not match `^[^_]+_(\d{4}|nd)_.+\.pdf$`; (2) no INDEX inventory row references it; (3) `Private/Bibliography/Summaries/{stem}.summary.txt` does not exist. The model consumes only the difference set. A clean library yields "0 unprocessed" — the scan is idempotent and doubles as a consistency checker.

## Step 2: Extract (pdf skill — never `pdftotext` CLI)

Extract full text plus title-page metadata: author(s), year, complete title, venue. **Rule 2: metadata must be read from the PDF itself — never recalled from model memory.** If the year is absent, ask the user once for that item (other PDFs proceed); unresolvable → `nd` + `[year unverified]` in INDEX.

**Document type** (`paper` / `monograph` / `collection`) is decided by **whether chapters are independent, separately-citable works**, not author count:
- `paper` — journal article or standalone preprint (default).
- `monograph` — one continuous argument; chapters are segments, not INDEX rows.
- `collection` — edited volume or self-collection of previously published papers; each member is independently citable.

For books also extract (Rule 2, from the PDF): ISBN from the copyright page; DOIs (whole-book from the copyright page; each chapter's from its first-page footer); the table of contents with page ranges and, for a collection, each chapter's printed author(s).

## Step 3: Dedupe

Match extracted metadata (author surname + title keywords) against existing INDEX rows. A match under a different filename → ask the user before creating a second entry; never auto-create a second KEY for the same work.

## Step 4: Rename

Canonical stem `{Author}_{Year}_{Title}`: segments joined by underscores, words within a segment hyphen-joined; Author = first author's surname (first **editor's** surname for a collection); Year = 4 digits or `nd`; Title = complete title-page title, punctuation stripped, TitleCase. Stems over 100 characters truncate at the subtitle boundary (INDEX keeps the full title). **One physical file per volume** — never split or copy. Rename with plain `mv` (PDFs are in no git; quote paths — the repo root contains a space). A paired analysis file under an old stem moves with `git mv` inside `Private/` and gets its header updated.

## Step 5: Register

Insert or update (never duplicate) the INDEX inventory row: KEY (`AUTHOR-TITLE`, no year; collision → append year), Author, complete Title, PDF path, Analysis Level, Topics; refresh the "Last updated" footer. By type: paper/monograph → one row; collection → one volume row (KEY `EDITOR-TITLE`, owns the Zotero `book` item) **plus one row per member paper** (member KEY `AUTHOR-TITLE`; PDF column = shared volume file + page range + `in {VOLUME-KEY}`).

## Step 6: Summarize (`method.dialectic.summarize`)

Invoke the summarize method with extracted text + verified metadata + document type; write to `Private/Bibliography/Summaries/`: paper → one file; monograph → one file with volume summary + per-chapter segments (~150–300 chars each); collection → volume summary + one independent file per member paper (`{chapter-author}_{volume-year}_{chapter-title}.summary.txt`, own topics, `container` field). Levels are append-only: set 0.5 only if the row was below it.

## Step 6B: Philosopher observations (one deterministic batch)

After all summaries in the batch are written:

```bash
python "Framework/Workflow/Scripts/philosopher-db.py" observe --input <summary-1> --input <summary-2>
```

The script derives source authors, resolves aliases, records counts, creates private review candidates, and updates only deterministic domain connections. It never approves a claim. Identical summary ID/hash pairs are no-ops. With `--dry-run`, pass it here too. Report changed artifacts, pending candidates, and domain updates.

## Step 7: Recommend (trigger point 1)

For each `Private/Projects/*/`, resolve guidance as `PROJECT.md` → `AGENTS.md` → `CLAUDE.md`. Match the summary's `topics[]` against its topic-keyword list. Report overlaps and **offer** (never auto-write) `candidate` rows for that project's refs.md. Skip KEYs already present under any status. For a collection, match **each member's own topics** and offer the member KEY as the candidate.

## Output

Batch report in Chinese: 总览 (scanned/processed/skipped + types); 逐文献块 (original → canonical name, KEY, type, actions, topics, recommendation hits); for collections, per-member KEY/page-range/summary/recommendation/bookSection key; 尾注 (INDEX consistency, follow-ups, Zotero status). Filenames, KEYs, and topics remain English.
