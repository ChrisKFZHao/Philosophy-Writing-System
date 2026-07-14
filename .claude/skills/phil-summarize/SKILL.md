---
description: Generates a Level 0.5 summary of a single philosophical source — core thesis, argument route, key concepts, interlocutors, and topic tags — as the cheapest analysis rung and the substrate for literature recommendation
domain: general
version: 1.0.0
---

# SKILL: phil-summarize — Level 0.5 Source Summary

## 1. Overview

Produces the Level 0.5 summary of a single document: core thesis + argument route + key concepts + interlocutors + topics, rendered as a ~300–500 character Chinese summary plus structured JSON. This is the cheapest rung of the analysis ladder (below Level 1 argument reconstruction) and the substrate for the three recommendation trigger points.

This skill is a **pure function**: (extracted text + verified metadata) in → one summary out. It does not touch the filesystem, INDEX.md, or any project files — the caller (normally `/phil:ingest`) writes `Private/Bibliography/Summaries/{stem}.summary.txt` and updates the INDEX row.

Output conforms to `summary-schema.json` (`.claude/shared/summary-schema.json`).

## 2. Input

- **Required**: Full extracted text of the source (from the `pdf` skill).
- **Required**: Verified source metadata (author, year, complete title, source type, canonical PDF path). Metadata must have been read from the document itself, not recalled (Rule 2).
- **Optional**: The existing INDEX row for this KEY (topics continuity when regenerating).
- **Optional**: Existing topic vocabulary (INDEX Topics column, project keyword lists) for tag alignment.

## 3. Output

A structured summary conforming to `summary-schema.json`, containing:
- Source metadata (echoed from input, with `year_verified` provenance flag)
- Core thesis, argument route, key concepts, interlocutors, topics
- Rendered Chinese summary text (~300–500 chars)

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

### Step 5: Assign Topics
Assign 4–8 English topic tags (lowercase phrases, comma style matching the INDEX Topics column). Reuse existing INDEX/project vocabulary where apt; introduce new tags only for genuinely new subject matter.

### Step 6: Render the Chinese Summary
Compose the summary in Chinese, 300–500 characters, covering all five elements (thesis, route, concepts, interlocutors, topics). Filenames, KEYs, and topic tags remain in English.

### Step 7: Assemble JSON
Assemble the structured output with a `SUM-` prefixed `summary_id`, per `report-id-registry.md`.

## 6. Quality Criteria

- **Length discipline**: Chinese summary within 300–500 characters
- **Charity**: thesis stated in the author's own commitments
- **Tag stability**: topics reuse existing library vocabulary where applicable
- **No hallucination**: every element grounded in the provided text; no claims, works, or positions the text does not contain (Rule 2)
- **Summary ≠ evaluation**: no verdicts on argument success

## 7. Relations to Other Skills

- **Upstream**: `pdf` skill (text extraction); `/phil:ingest` (orchestration, metadata verification)
- **Downstream**: recommendation trigger point 1 (ingest-time matching); phil:tutor trigger point 2 (INDEX scanning); `phil-argument-reconstruct` (Level 1 escalation)
- **References**: `Private/Bibliography/INDEX.md` (topics vocabulary); `Private/Projects/*/CLAUDE.md` (project keyword lists)

## 8. Boundary Conditions

- **Non-philosophy PDF**: flag it and ask the user whether to summarize anyway or skip
- **Unextractable text** (scanned PDF, encoding failure): report the failure; produce no summary from guesswork
- **Book-length source**: summarize the whole at coarse grain; chapter-level summaries are out of scope (note this in the output)
- **Unverified year**: set `year_verified: false` and `year: "nd"`; never substitute a year from model memory

## 9. Interface with ARS

The summary can seed `ars-abstract` comparison work. It is not a substitute for ARS literature-review artifacts (`ars-lit-review`), which operate across sources rather than within one.
