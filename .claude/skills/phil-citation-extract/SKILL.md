---
description: Extracts all citations from a philosophical text, classifies by role (core-target/supporting/opposition/background/passing-mention), and cross-references against the project bibliography
domain: general
version: 1.0.0
---

# SKILL: phil-citation-extract — Citation Extraction and Role Classification

## 1. Overview

Extracts every explicit citation from a philosophical text, classifies each by its argumentative role in the source, and cross-references against the project's bibliography (bibliography/INDEX.md). This skill serves as a mechanical extraction engine — it does not evaluate importance or generate reading plans (those are handled by the phil:tutor agent or phil:trail command).

Output conforms to `citation-extract-schema.json` (`.claude/shared/citation-extract-schema.json`).

## 2. Input

- **Required**: The source philosophical text (paper, monograph chapter, preprint) as plain text.
- **Optional**: Content of `bibliography/INDEX.md` for cross-referencing. If unavailable, all citations are marked as not-in-bibliography.
- **Optional**: Known author name or topic hints for disambiguation.

## 3. Output

A structured citation inventory conforming to `citation-extract-schema.json`, containing:
- Source metadata (title, author, year, type)
- Citation list with role classification and cross-reference status
- Core works identification (works the text centrally engages with)

## 4. Methodological Foundations

This skill adapts standard citation context analysis (Small, 1978 — "Cited Documents as Concept Symbols") to the specific conventions of analytic philosophy:
- Philosophy citations are argumentatively loaded — they signal agreement, disagreement, or target status, not mere reference
- Philosophers often cite by name + position ("Kripke's causal theory") rather than formal bibliographic reference
- A single cited work may serve multiple functions across different sections

## 5. Steps

### Step 1: Text Scan and Citation Identification
Parse the text for citation markers: author names with years, footnote/endnote references, parenthetical citations, "cf." and "see" references. Extract each candidate citation with 1-2 sentences of surrounding context. Capture all entries in the bibliography/references section.

### Step 2: Disambiguation and Normalization
Resolve ambiguous references (e.g., "Lewis (1986)" — which Lewis? Multiple works in 1986?). Use:
- Context clues from the surrounding text
- Known works from the project's philosopher database (.claude/references/philosophers-db/)
- Explicit cross-checking with the bibliography

When disambiguation is uncertain, list alternatives with `confidence: low`.

### Step 3: Role Classification
For each citation, classify its argumentative role using textual evidence:

| Role | Signal Phrases | Decision Rule |
|------|----------------|---------------|
| **core-target** | "I argue against X", "X's view is the focus", "the target of this critique" | The text is primarily engaging with this work |
| **supporting** | "Following X", "As X shows", "X establishes that" | Cited in agreement as evidence |
| **opposition** | "Contra X", "X objects that", "X's challenge fails" | Cited as a view to be rejected |
| **background** | "This debate originates with X", "the X tradition" | Provides framing or context |
| **passing-mention** | "See also X", "cf. X", "(X, 2000)" | Brief reference without substantive engagement |

Each classification must include a `role_justification` and `confidence` level.

### Step 4: Bibliography Cross-Reference
For each citation, look up `bibliography/INDEX.md` by author surname + title keywords. Record:
- Whether a match was found (`in_bibliography`)
- Current analysis level (0-3) if matched
- PDF availability

For unmatched entries, note the reason.

### Step 5: Core Works Synthesis
Compile the list of works that are the text's main interlocutors:
- All `core-target` citations
- `opposition` citations that receive sustained engagement (across multiple sections)
- Any `supporting` works that appear across multiple argument sections

### Step 6: Report Assembly
Assemble the complete structured output.

## 6. Quality Criteria

- **Completeness**: All explicit citations must be captured
- **Role Accuracy**: Each role classification must be justified by textual evidence
- **Disambiguation Rigor**: When uncertain, list alternatives rather than silently choosing
- **No Hallucination**: Report only citations actually found in the text; never fabricate citation details (Rule 2 compliance)

## 7. Relations to Other Skills

- **Upstream**: None (accepts raw text directly)
- **Downstream**: `phil:tutor` agent uses output for literature recommendations; `phil:trail` command uses output for reading plan generation
- **References**: `bibliography/INDEX.md` for cross-referencing; `.claude/references/philosophers-db/` for disambiguation

## 8. Boundary Conditions

- **No citations**: Output empty `citations` array and note this
- **Chinese text citing Western works**: Scan for both transliterations and original names; use philosophers-db/ for matching
- **INDEX.md unavailable**: Set `bibliography_index_available: false`, flag all as unmatched
- **Generic references** ("the Kripkean picture"): Note as "generic reference" without full citation_id

## 9. Interface with ARS

The citation inventory can be passed to ARS `citation-check` for verification of bibliographic details. Unmatched citations can seed a `deep-research` literature acquisition request.
