---
description: Literature ingestion ("scraping") — scans the bibliography for unprocessed PDFs, renames them to the canonical stem, registers them in INDEX.md, generates Level 0.5 summaries, and runs recommendation trigger point 1
---

# /phil:ingest

## Usage

```
/phil:ingest                    # scan the whole library, process every unprocessed PDF
/phil:ingest <pdf-filename>     # process a single PDF (filename relative to Private/Bibliography/PDF/)
/phil:ingest --dry-run          # report what would be done without changing anything
/phil:ingest --force <KEY>      # regenerate the summary for an already-processed entry
```

## Positioning

The **entry point of the PDF Processing Workflow** (media-library "scraper" analogy): whenever new PDFs land in `Private/Bibliography/PDF/`, this command normalizes them into the library. It implements **recommendation trigger point 1** (on ingestion — new source's topics matched against each project CLAUDE.md's topic keywords).

Relation to phil:reconstruct:
- **ingest** performs cheap intake: rename + register + Level 0.5 summary (the lowest analysis rung)
- **reconstruct** performs deep analysis: Level 1+ argument reconstruction, escalated per Citation Gate rules
- Order: PDF added → `/phil:ingest` → (when the source becomes a paper dependency) `phil:reconstruct`

## Orchestration

| Component | Description |
|-----------|-------------|
| Shell set-comparison | Step 1 scan: programmatic diff of PDF directory vs INDEX registrations (no model reading) |
| `pdf` skill | Text + title-page metadata extraction (never `pdftotext` CLI directly) |
| `phil-summarize` skill | Level 0.5 summary generation (pure function; this command writes the file) |

## Steps

### Step 1: Scan (MUST be programmatic — token-economy hard requirement)

Detect unprocessed PDFs by shell set-comparison. **Do not read the directory listing or INDEX.md into the model to make this judgment.**

```bash
ls "Private/Bibliography/PDF/"*.pdf                              # actual files
grep -o 'PDF/[^ |]*\.pdf' "Private/Bibliography/INDEX.md"        # registered paths
```

A PDF is **unprocessed** if ANY of:
1. Its filename does not match the canonical stem pattern `^[^_]+_(\d{4}|nd)_.+\.pdf$`
2. No INDEX inventory row's PDF column references it
3. `Private/Bibliography/Summaries/{stem}.summary.txt` does not exist

The model consumes only the resulting difference set (a few filenames). Expensive steps (extraction, metadata, summary) run only for PDFs in that set. A clean library yields "0 unprocessed" — the command is idempotent and doubles as a consistency checker.

### Step 2: Extract (per unprocessed PDF)

Use the `pdf` skill to extract full text plus title-page metadata: author(s), year, complete title, venue. **Rule 2: metadata must be read from the PDF itself — never recalled from model memory.** If the year is absent from the PDF, ask the user once for this item (other PDFs in the batch proceed); if the user cannot verify, use `nd` in the stem and mark `[year unverified]` in INDEX.

### Step 3: Dedupe

Match extracted metadata (author surname + title keywords) against existing INDEX rows. If an existing row matches under a different PDF filename, this is a duplicate or a retrofit case — **ask the user before creating a second entry**; never auto-create a second KEY for the same work.

### Step 4: Rename

Compute the canonical stem `{Author}_{Year}_{Title}`:
- Segments separated by **underscores**; words within a segment joined by hyphens (underscore = segment boundary; hyphens stay free for hyphenated surnames and the title itself)
- Author = first author's surname, capitalized, ASCII
- Year = 4 digits or `nd`
- Title = the **complete title** from the title page (articles kept, subtitle included, punctuation stripped, TitleCase, hyphen-joined). Examples: `Austin_1956_A-Plea-for-Excuses.pdf`, `Shafer-Landau_2003_Moral-Realism-A-Defence.pdf`
- Path safety valve: if the stem exceeds 100 characters, truncate at the subtitle boundary; INDEX keeps the full title with a note

Then:
- Rename the PDF with plain `mv` (PDFs are in no git); quote paths (repo root contains a space)
- If a paired analysis file exists under an old stem, `git mv` it inside `Private/` to the new stem and update its header lines to reference the canonical PDF path

### Step 5: Register

Insert or update (never duplicate) the INDEX inventory row: KEY, Author, Title (complete), PDF path, Analysis Level, Topics. KEY format stays `AUTHOR-TITLE` (no year — KEY is the stable identifier consumed by refs.md and the Citation Gate; the file stem is the locator). On an AUTHOR-TITLE collision, the newer entry appends the year: `AUTHOR-TITLE-1998`. Refresh the "Last updated" footer.

### Step 6: Summarize

Invoke `phil-summarize` with the extracted text + verified metadata; write the result to `Private/Bibliography/Summaries/{stem}.summary.txt` (create `Summaries/` on first run). Levels are append-only: set Analysis Level to 0.5 only if the row was below it; a Level 3 entry keeps Level 3 but still gains the summary file (the recommendation substrate).

### Step 7: Recommend (trigger point 1)

Match the summary's `topics[]` against every `Private/Projects/*/CLAUDE.md` `## 主题关键词` list. Report overlaps per project and **offer** (never auto-write) `candidate` rows for that project's refs.md. Skip KEYs already present in that refs.md under any status, including `rejected`.

## Output Format

Batch report (in Chinese, project convention):

1. **总览** — scanned N / unprocessed M / processed / skipped / needs-year
2. **逐文献块** — original name → canonical name; KEY; actions taken (renamed / registered / analysis-renamed / summarized / skipped + reason); topics; per-project recommendation hits (or "已登记，抑制推荐")
3. **尾注** — INDEX consistency notes; follow-ups surfaced (e.g., provisional analyses whose PDF is now available for verification)

## Notes

- Write all output in Chinese (project convention); filenames, KEYs, and topics remain in English
- PDFs never enter git; analysis/summary renames use `git mv` inside the inner `Private/` repo
- Year and complete title must come from the PDF title page (Rule 2); fallback chain: read PDF → ask user → `nd` + `[year unverified]`
- On dedupe ambiguity (same work, different file), ask — do not create a second KEY
- `--dry-run` performs Step 1 (and metadata peeks where needed for reporting) but writes nothing
