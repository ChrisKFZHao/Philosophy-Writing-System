---
id: service.zotero-registration
kind: service
authority: "write — external cloud writes to the Zotero backend; identifier-gated; never creates stored PDF copies"
consumers: [phil-research/ingest]
scripts: [zotero-attach-linked.py]
safety: "classified backend (full/partial/skipped) per runtime-compatibility.md; --dry-run skips every write"
---

# Zotero Registration Service

Auto-creates Zotero items for ingested sources and attaches the canonical PDF as a **linked file**, so batch ingestion never requires manual "Attach Link to File" clicks. This step writes to the Zotero cloud; new items appear in the local UI only after a desktop sync.

## Backend classification (before any write)

Per `Framework/Workflow/Rules/runtime-compatibility.md`: `full` (MCP write tools + linked-file helper available) → run normally; `partial` (local plugin/API only) → no metadata or linked-file creation, report manual follow-up; `skipped` → complete intake without this step and report. Under `--dry-run`, report the detected backend but skip every write.

## Identifier gate: DOI-first → ISBN → bibtex

Read every identifier from the PDF (Rule 2 — never from model memory):
- `paper` — try the **DOI** (§A).
- `monograph` / `collection` — the **book cascade** (§B): scholarly-press ISBNs frequently fail to resolve while CrossRef chapter DOIs succeed (validated 2026-07-14, OSM Vol. 12). Try in order: whole-book DOI and per-chapter DOIs; copyright-page ISBN; resolver-independent `zotero_add_by_bibtex` (`@book` / `@incollection`).

Nothing resolves and no verified metadata → skip automation, leave the INDEX `Zotero` column as `—`, and add a manual-follow-up block (New Item → verify metadata → Attach Link to File → report the item key back for INDEX backfill).

### A. Paper (DOI path)

1. `zotero_add_by_doi(doi=..., attach_mode='none', if_exists='skip')` — `attach_mode='none'` guarantees no stored copy (one-physical-repository invariant); `if_exists='skip'` prevents duplicates (on an existing item, look up its key and continue with it).
2. **Capture the parent item key directly from the tool result.** Never round-trip a key through a subagent return value — a proxy-side redaction filter rewrites `KEY:`-like lines to `[密钥]`.
3. Cross-check CrossRef metadata against the Step 2 title-page metadata (aggregators mis-attribute authors); correct via `zotero_update_item`.
4. Attach the canonical PDF as a linked file (§C).
5. Backfill the INDEX `Zotero` column with the parent key.

### B. Monograph / collection (book cascade)

a. **DOI attempt** (preferred — CrossRef is the most reliable): whole-book DOI creates a `book`; if it fails, **continue, do not stop**. Per-chapter DOIs (OUP/OSO scheme `…/<book-doi>.003.000N`) each create a clean `bookSection` — **the preferred member path**, superior to hand-built bibtex. Cross-check each title against the TOC (CrossRef may drop subtitles). If the whole-book DOI failed but chapter DOIs work, create the `book` via (c). Retry transient SSL/EOF failures per DOI (network errors, not wrong DOIs).
b. **ISBN attempt** (no usable DOI): `zotero_add_by_isbn(isbn=..., if_exists='skip')`. It has **no `attach_mode`** — verify via `zotero_get_item_children` and trash any stored attachment that appears. Open Library / Google Books metadata is less reliable → title-page cross-check mandatory.
c. **bibtex fallback** (verified metadata available): `@book` for the volume + one `@incollection` per collection member (fields from the verified TOC), `attach_mode='none'`.
d–g. Capture keys directly from tool results; cross-check metadata regardless of path; attach the volume PDF as a linked file to the book item **and every member item** (§C batch mode); backfill INDEX (`Zotero` column = book key / each member's bookSection key).

### C. Linked-file attachment (shared helper)

The Zotero MCP has no linked-file-creation tool; use `Framework/Workflow/Scripts/zotero-attach-linked.py` (credentials from process environment or user-level runtime configuration, never repository files; configured proxy with `127.0.0.1:6789` fallback; retries; prints only attachment keys):

```bash
python "Framework/Workflow/Scripts/zotero-attach-linked.py" --parent <key> --stem <stem>.pdf --verify
python "Framework/Workflow/Scripts/zotero-attach-linked.py" --parents <book>,<sec1>,<sec2> --stem <volume-stem>.pdf --verify
```

The `linked_file` payload uses `attachments:` base-directory-relative paths (survive machine moves). Batch mode auto-splits at Zotero's 50-item cap and prints `ATTACHMENT_KEY <parent> <key>` per line — capture keys from stdout, never through a subagent.

## Invariants

- **Collections are not auto-filed** — Zotero collections stay user-managed (lazy-migration principle); remind the user to file items manually.
- `attach_mode='none'` (or equivalent) on every create — never a stored PDF copy.
- Item keys are written straight into INDEX from the command's own context.
