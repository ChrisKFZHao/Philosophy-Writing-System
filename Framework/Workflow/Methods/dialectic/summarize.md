---
id: method.dialectic.summarize
package: dialectic
legacy_ids: [phil-summarize]
label: Level 0.5 Summary
consumers: [phil-research/ingest]
selector: feature-detected
side_effects: read-only
---

# Level 0.5 Summary (method.dialectic.summarize)

> Internal method module — not a registered runtime skill. Loaded on demand by the consuming skill's mode contract through the manifest resolver; never loaded wholesale.

# SKILL: method.dialectic.summarize — Level 0.5 Source Summary

## 1. Overview

Produces the Level 0.5 summary of a single document: core thesis + argument route + key concepts + interlocutors + topics, rendered as a ~300–500 character Chinese summary plus structured JSON. This is the cheapest rung of the analysis ladder (below Level 1 argument reconstruction) and the substrate for the three recommendation trigger points.

This skill is a **pure function**: (extracted text + verified metadata) in → one summary out. It does not touch the filesystem, INDEX.md, or any project files — the caller (normally `/phil:ingest`) writes `Private/Bibliography/Summaries/{stem}.summary.md` and updates the INDEX row.

Output conforms to `summary-schema.json` (`Framework/Workflow/Schemas/summary-schema.json`).

## 2. Input

- **Required**: Full extracted text of the source (from `Scripts/pdf-extract.py`, normally its cached evidence units).
- **Required**: Verified source metadata (author, year, complete title, **source type**, canonical PDF path). Metadata must have been read from the document itself, not recalled (Rule 2). `source_type` (paper / monograph / collection / chapter) selects the summarizing mode in Step 6.
- **For a monograph**: the table of contents (chapter numbers + titles) so the volume summary can carry per-chapter segments.
- **For a collection member (chapter)**: that single paper's text, its container metadata (volume KEY, page range), and the volume's own title — each member paper is summarized as its own standard single-paper run, not folded into the volume file.
- **Optional**: The existing INDEX row for this KEY (topics continuity when regenerating).
- **Optional**: Existing topic vocabulary (INDEX Topics column, project keyword lists) for tag alignment.

## 3. Output

A structured summary conforming to `summary-schema.json`, containing:
- Source metadata (echoed from input, with `year_verified` provenance flag)
- Core thesis, argument route, key concepts, interlocutors, topics
- Rendered Chinese summary text (~300–500 chars)
- A compact `philosopher_observations[]` block for explicitly named, substantively engaged figures; the private maintenance queue consumes this block without rereading the PDF

## 4. Methodological Foundations

Structured abstracting, distinguished from evaluation: a Level 0.5 summary states **what the text argues**, not whether the argument succeeds (evaluation belongs to phil:evaluate and Level 2+ analyses). Topics vocabulary should align with the existing INDEX topics and project keyword lists — matching stability across the library matters more than tag novelty.

## 5. Steps

### Step 1: Locate the Thesis
Identify the core claim the text commits itself to — typically in the abstract, introduction, or conclusion. State it as the author's own commitment (charity), not a paraphrase colored by critique.

### Step 2: Trace the Argument Route
Sketch the major argumentative moves in order (e.g., "distinguishes X from Y → argues Z fails for Y → concludes W"). This is a route map, not a full reconstruction — premise-level detail belongs to Level 1.

### Step 3: Extract Key Concepts
List 3–6 concepts the text defines, refines, or centrally relies on.

### Step 4: Identify Interlocutors
List the named positions or authors the text substantively engages with (targets, allies, foils). Named engagement only — do not infer unnamed influences.

For each substantive figure, add one structured observation with canonical/display name, role (`core-target`, `supporting`, `opposition`, or `background`), and at most two claims explicitly attributed by the text. Each claim must state its category and an auditable section/page/summary-field locator. Do not convert passing mentions into observations and do not infer influence. The caller derives the source author and their `core_thesis`, so omitting a duplicate author observation is allowed.

### Step 5: Assign Topics
Assign 4–8 English topic tags (lowercase phrases, comma style matching the INDEX Topics column). Reuse existing INDEX/project vocabulary where apt; introduce new tags only for genuinely new subject matter.

### Step 6: Render the Chinese Summary (mode by source type)
Compose the summary in Chinese; filenames, KEYs, and topic tags remain in English. Steps 1–5 run against the appropriate unit for each mode:

- **paper / preprint** — one summary, 300–500 characters, covering all five elements. (Unchanged.)
- **monograph** — a volume-level summary (300–500 chars, the whole book's thesis + argument arc + concepts + interlocutors + topics) **plus** one segment per chapter (~150–300 chars each), populating `chapters[]`. Steps 1–4 are applied once to the whole book and once per chapter; topics (Step 5) are assigned at the volume level only.
- **collection member (chapter)** — run the full paper pipeline (Steps 1–5) on that single member paper exactly as for a standalone paper, 300–500 chars, with its own topics; set `container` to the volume KEY + page range. The edited volume itself also gets a summary in `collection` mode: a volume-level summary of the editors' framing question and the structural arc across parts (no per-member fold-in — each member has its own file).

### Step 7: Assemble JSON
Assemble the structured output with a `SUM-` prefixed `summary_id`, per `report-id-registry.md`. Add `philosopher_observations[]` without a second model pass. Monograph summaries carry `chapters[]` (in-file per-chapter `summary_text`); a collection **volume** summary carries `members[]` (a pointer manifest — chapter_no, title, author, pages, member_key — whose actual summaries live in separate member files); collection **member** summaries carry `container`.

## 6. Quality Criteria

- **Length discipline**: Chinese summary within 300–500 characters (paper, monograph volume-level, and each collection-member paper); monograph chapter segments ~150–300 characters each
- **Charity**: thesis stated in the author's own commitments
- **Tag stability**: topics reuse existing library vocabulary where applicable
- **No hallucination**: every element grounded in the provided text; no claims, works, or positions the text does not contain (Rule 2)
- **Observation economy**: at most two attributed claims per substantive figure; no duplicate author observation and no separate PDF read
- **Summary ≠ evaluation**: no verdicts on argument success

## 7. Relations to Other Skills

- **Upstream**: `Scripts/pdf-extract.py` (text extraction); `/phil:ingest` (orchestration, metadata verification)
- **Downstream**: recommendation trigger point 1 (ingest-time matching); phil:tutor trigger point 2 (INDEX scanning); `method.argument.argument-reconstruct` (Level 1 escalation)
- **References**: `Private/Bibliography/INDEX.md` (topics vocabulary); `Private/Projects/*/PROJECT.md (falling back to AGENTS.md or CLAUDE.md)` (project keyword lists)

## 8. Boundary Conditions

- **Non-philosophy PDF**: flag it and ask the user whether to summarize anyway or skip
- **Unextractable text** (scanned PDF, encoding failure): report the failure; produce no summary from guesswork
- **Monograph (single-author book)**: produce a volume-level summary plus per-chapter segments (`chapters[]`) in one file — not one coarse-grained whole. The citation unit stays the book (KEY + page number); chapter segments are a reading/recommendation aid and do not become INDEX rows or Zotero sub-items.
- **Edited collection**: the volume gets a `collection`-mode summary; **each member paper is summarized independently** (its own `chapter`-mode file, INDEX row, and Zotero bookSection). Type test is whether the chapters are independent works — a single-author self-collection of previously published papers is treated as a collection, not a monograph.
- **Unverified year**: set `year_verified: false` and `year: "nd"`; never substitute a year from model memory

## 9. Interface with ARS

The summary can seed `ars-abstract` comparison work. It is not a substitute for ARS literature-review artifacts (`ars-lit-review`), which operate across sources rather than within one.
