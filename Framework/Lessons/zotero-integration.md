# Zotero Integration: Unified PDF Repository & Migration Workflow

> Distilled from the `instantaneous-velocity` pilot (2026-07-14; details in that project's `feedback-to-framework.md`). Status: validated end-to-end on 6 items including annotation preservation.

## Architecture

**One PDF repository, two consumers.** `Private/Bibliography/PDF/` is the single physical home for all literature PDFs. Zotero reads them as *linked* attachments (its Linked Attachment Base Directory points at this folder); the writing framework reads them via the canonical stem recorded in `INDEX.md`. Neither side owns a private copy.

**Naming ownership belongs to the framework, not Zotero.** Files carry the canonical stem `{Author}_{Year}_{Title}` (see CLAUDE.md naming conventions). Zotero's own renaming templates cannot produce this format (no hyphen-joining within segments), so Zotero must never rename — a file is renamed *before* it is linked, and never again afterwards.

**Three-way mapping.** `INDEX.md`'s `Zotero` column maps `KEY ↔ Zotero item key ↔ file stem`. `—` means the source is not in Zotero. Zotero collections are *not* mirrored as directories; a collection that matures into a paper becomes a `Private/Projects/{topic}/` project whose `refs.md` lists the member KEYs.

**Lazy migration.** Zotero items with stored (imported) attachments are migrated to the unified repository only when their collection becomes a writing project — never as a bulk sweep.

## Ingestion flows

### New PDF (not yet in Zotero)
1. Drop into `Private/Bibliography/PDF/` → `/phil:ingest` (rename to canonical stem, INDEX registration, Level 0.5 summary)
2. Zotero registration is **automated by `/phil:ingest` Step 8** under an identifier gate (paper → DOI; book → cascade DOI-first → ISBN → bibtex):
   - **Paper with a DOI** (read from the PDF, Rule 2): the command creates the parent item via `zotero_add_by_doi(attach_mode='none', if_exists='skip')`, cross-checks the CrossRef metadata against the title-page metadata, attaches the canonical PDF as a `linked_file` via the web API (payload below), and backfills INDEX's `Zotero` column. No stored copy ever exists; no manual click.
   - **Monograph / collection** (Rule 2 identifiers from the PDF): the command runs a **fallback cascade — DOI-first → ISBN → bibtex** (revised from ISBN-only after the OSM Vol. 12 test, 2026-07-14, where both ISBNs *and* the whole-book DOI returned "not found" while every chapter DOI resolved). In order: (1) **DOI** — try the whole-book DOI via `zotero_add_by_doi(attach_mode='none')`, and for a collection add each member via its **per-chapter DOI** (`zotero_add_by_doi` returns a clean CrossRef `bookSection`; this is preferred over hand-built bibtex — verify each returned title against the TOC, as CrossRef may drop a subtitle); (2) **ISBN** — if no usable DOI, `zotero_add_by_isbn(if_exists='skip')` (creates a `book`). `zotero_add_by_isbn` has **no `attach_mode`** — resolvers normally have no OA PDF, but verify via `zotero_get_item_children` and trash any stored attachment; Open Library / Google Books metadata is *less* reliable than CrossRef → title-page cross-check mandatory; (3) **bibtex** — if neither resolves, build from verified metadata via `zotero_add_by_bibtex` (`@book` volume + `@incollection` per member). Whichever path is used, the single volume PDF is attached as a `linked_file` to the book item **and every member item** in one batch POST (`zotero-attach-linked.py --parents <book>,<sec1>,<sec2>,…`). Each item key is backfilled to its INDEX row (volume row = book key; member rows = bookSection keys).
   - **Neither DOI nor ISBN** (SEP entries, working papers): Step 8 skips automation and reports a manual follow-up — in Zotero, create/import the item metadata, then **Attach Link to File** → the canonical file, and report the item key for INDEX backfill.
3. The new item(s) land in the local Zotero UI only after a desktop sync (writes go to the cloud first).

### Existing Zotero item with stored attachment (migration)
1. Copy (do not move) the PDF out of `Zotero/storage/…` into `Private/Bibliography/PDF/` under the canonical stem → `/phil:ingest`
2. Convert the Zotero side stored→linked **via the web API** (method below)
3. Record the item key in INDEX's `Zotero` column

## Stored→linked conversion via web API (annotation-preserving)

Prerequisites: write-enabled API key configured in the zotero MCP env in `~/.claude.json` (hybrid mode: reads stay on local SQLite via `ZOTERO_LOCAL=true`; writes go to the cloud). The item must already be synced to the cloud; desktop must sync once afterwards for changes to land locally.

Per item (all requests to `api.zotero.org/users/{userID}`):

1. `POST /items` — create a `linked_file` attachment under the parent:
   `{"itemType":"attachment","linkMode":"linked_file","parentItem":"<parent>","path":"attachments:<canonical-stem>.pdf","contentType":"application/pdf","title":"<canonical-stem>.pdf"}`
   (`attachments:` = base-directory-relative path — survives machine moves). The reusable helper `.claude/scripts/zotero-attach-linked.py --parent <parent> --stem <canonical-stem>.pdf --verify` encapsulates this POST (auth from `~/.claude.json`, proxy, retries, verify) — the same script `/phil:ingest` Step 8 uses.
2. `GET /items/<old-att>/children` — list annotations; for each, `PATCH {"parentItem":"<new-att>"}` (annotation reparenting is allowed; returns 204)
3. Verify the annotation count on the new attachment matches, then `PATCH {"deleted":1}` on the old stored attachment (recoverable from Trash — do not empty Trash until the user has visually confirmed)

### Known constraints and pitfalls
- `linkMode` is immutable via the API (400 "Cannot change attachment linkMode") — in-place conversion is impossible; create-new + reparent is the only API path
- Every key-based write requires the `If-Unmodified-Since-Version` header; retry wrappers must not drop it (a dropped header produces 428, and a *partially applied* batch)
- `api.zotero.org` requires the local proxy (`127.0.0.1:6789`) and is still flaky — scripts need per-request retries
- Zotero metadata is not trustworthy for INDEX registration: aggregator imports (e.g. JSTOR) list journal editors as co-authors. Title-page verification (Rule 2) applies on the Zotero inflow path too
- Linked files consume no Zotero cloud storage quota — and several items may link the *same* path (a collection's book item + every bookSection all point at the one volume PDF); this is expected, not duplication
- A single write batch is capped at 50 items; `zotero-attach-linked.py --parents` auto-splits beyond that
- Fallback without an API key: Zotmoov plugin converts stored→linked with annotations intact, but emits its own template filename → manual per-item relink (delete emitted file, open attachment, Locate → canonical file)

## Verification (after desktop sync)
- `zotero_get_attachment_path(<parent-key>)` → path under `Private/Bibliography/PDF/` with the canonical stem
- `zotero_get_annotations(<new-att-key>)` → count matches the pre-migration count
