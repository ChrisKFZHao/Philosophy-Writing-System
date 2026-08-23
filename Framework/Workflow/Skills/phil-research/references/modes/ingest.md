# Mode contract: ingest

Library intake ("scraping"): scans the bibliography for unprocessed PDFs and normalizes them into the master library. This is the entry point of the PDF processing workflow and implements **recommendation trigger point 1**. The only `phil-research` mode with write authority.

## Usage

```
phil:research ingest                     # whole library, every unprocessed PDF
phil:research ingest <pdf-filename>      # single PDF (relative to Private/Bibliography/PDF/)
phil:research ingest --dry-run           # report only, write nothing
phil:research ingest --force <KEY>       # regenerate the summary of a processed entry
```

## Execution

This mode is a thin contract over two services — it routes, supervises, and reports; the services own the procedure and the side effects:

1. **`Services/source-intake.md`** — deterministic scan, title-page extraction (pdf skill), document-type triage, dedupe, canonical rename, INDEX registration, Level 0.5 summaries via `method.dialectic.summarize`, philosopher observation batching, and recommendation trigger point 1 (project topic-keyword matching; offers `candidate` refs.md rows, never auto-writes).
2. **`Services/zotero-registration.md`** — Step 8 only: identifier-gated Zotero registration (paper → DOI; book → DOI cascade → ISBN → bibtex) with linked-file attachment. Backend classified `full`/`partial`/`skipped`; `--dry-run` skips every write of this step entirely.

Read both service files (and only then the summarize method) before executing a real run. Relation to `reconstruct`: ingest performs cheap intake (rename + register + Level 0.5 summary — the lowest analysis rung); reconstruct performs Level 1+ analysis, escalated later per Citation Gate rules. Order: PDF added → ingest → (when the source becomes a paper dependency) reconstruct.

## Authority and safety

- May rename PDFs, write INDEX rows and summaries, enqueue philosopher observations, and request Zotero writes — nothing else. Never writes project manuscripts or refs.md.
- `--dry-run` is the default safety path for a first pass over an unfamiliar batch.
- Year and complete title come from the PDF title page (Rule 2); fallback chain: read PDF → ask user once → `nd` + `[year unverified]`.
- On dedupe ambiguity, ask — never create a second KEY for the same work.

## Output

The batch report format defined in `Services/source-intake.md` (Chinese; filenames, KEYs, topics in English), plus the Zotero status block (`full`/`partial`/`skipped`, created/existing items, manual follow-ups, cascade level used, desktop-sync reminder).
