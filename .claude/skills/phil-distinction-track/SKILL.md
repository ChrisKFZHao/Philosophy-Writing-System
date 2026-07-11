---
description: Distinction Tracking — identify, index, and trace all key conceptual distinctions in philosophical texts; test distinctions for consistency, exhaustiveness, and argumentative function
domain: general
version: 1.0.0
---

# Distinction Tracking

## Overview

"Philosophy begins with distinctions" — from Plato's knowledge/opinion, Hume's ideas/impressions, Kant's analytic/synthetic, Berlin's negative/positive liberty, to contemporary mind/body, realism/anti-realism, descriptive/normative, the entire history of analytic philosophy is a history of distinctions.

This Skill systematically tracks all key conceptual distinctions throughout a text. It seeks to answer:

- Which distinctions are introduced in the text? Which are explicit, and which are implicit?
- What argumentative work do these distinctions perform?
- Do the distinctions remain consistent across the text, or do they drift?
- Which distinctions are exhaustive (forming dichotomies), and which are open-ended?
- What are the interrelations among distinctions — which are parallel, nested, or in collision?

## Input

- One or more philosophical text passages (Chinese or English)
- Optional:
  - A report from `phil-conceptual-analysis` (providing deep analysis background for individual concepts)
  - A known list of domain-standard distinctions

## Output

A structured **Distinction Tracking Report**, containing:
- A distinction inventory (name of each distinction, the two or more poles of the concept)
- Distinction function analysis (what argumentative work the distinction performs)
- Consistency check (whether distinctions drift)
- Distinction type classification (dichotomy vs. trichotomy vs. open-ended; exhaustive vs. non-exhaustive)
- Distinction network diagram (which distinctions interrelate, nest, or collide)
- Missing distinctions (distinctions the text ought to have drawn but did not)

## Methodological Foundations

1. **Concept Mapping / Distinction Drawing**: Mapping the "logical geography" of concepts — Ryle's (1949) concept of "category mistakes," Austin's (1956) "technique of distinction-drawing"
2. **Theory of Distinctions**: Some distinctions carve at the "natural joints" reflecting the real structure of the world; others are "artificial lines" drawn for convenience — philosophy's task is to distinguish these two kinds. Williamson (2007) critiques excessive distinction-drawing; Stoljar (2010) distinguishes "hard distinctions" from "standpoint distinctions"
3. **Taxonomic Method**: Many philosophical arguments depend on assumptions of taxonomic exhaustiveness — test the exhaustiveness and mutual exclusivity of implicit distinctions
4. **Drift Detection (Concept Drift / Equivocation)**: The same term is assigned different distinction criteria at different stages of the argument — this leads to fallacies

## Steps

### Step 1: Scanning and Extraction

Identify all conceptual contrasts and distinctions in the text. Distinctions typically appear in pairs:

- Explicit distinctions: "X vs. Y," "not-X but Y," "X in the sense of …, not Y"
- Implicit distinctions: Context suggests a distinction without stating it explicitly

**Output**: A preliminary inventory of all distinctions.

### Step 2: Indexing and Numbering

Assign each distinction a unique identifier and tag it with:

- **Text location** (first introduction + subsequent uses)
- **Distinction type**:
  - **Dichotomy** (dichotomy / binary): Two classes that are complementary sets (possible/impossible)
  - **Trichotomy** (trichotomy / ternary): Three classes (past/present/future)
  - **Polytomy** (polytomy / multinary): Multiple classes (divisions of color)
  - **Scalar** (open-ended / scalar): Not finite classes but distinctions along a continuous spectrum (high/low)
  - **Hierarchical**: Distinctions forming levels (genus → species → finer species)
- **Exhaustiveness**: Does the distinction claim to exhaust all possibilities?
- **Mutual exclusivity**: Are the distinguished classes mutually exclusive?

**Output**: A numbered distinction index table.

### Step 3: Function Analysis

Analyze the **argumentative function** of each distinction — why was it introduced? What work does it do in the argument?

| Function Type | Description | Example |
|---------------|-------------|---------|
| **Clarificatory distinction** | Eliminates ambiguity, precisifies concepts | "Freedom, not in the sense of freedom of the will (metaphysical), but in the sense of freedom of action (political)" |
| **Refutational tool** | Uses a distinction to expose a fallacy in an opponent's argument | "You have conflated causal relevance with causal determination" |
| **Defensive tool** | Uses a distinction to ad hoc except a counterexample, avoiding refutation | "That counterexample falls under a different category" (note: may become an ad hoc classification) |
| **Argument-space partitioning** | Divides possible positions into classes, then argues for each | "There are only three possible positions: A, B, C; nothing else is possible" |
| **Definitional aid** | Defines a concept through contrast — "X means: that kind of thing which is not Y" | "Justice is a matter of distribution according to desert, not a psychological state of feeling that one has received one's due" |

**Output**: Function annotation for each distinction.

### Step 4: Consistency Check

Check distinctions for consistency across the text:

**Drift detection**:
- Does the same term have different distinction criteria in different paragraphs?
- Do the boundaries of the distinction shift over the course of the argument?
- If so — does this produce an equivocation fallacy in the argument?

Example: In paragraph 1, "freedom = absence of interference" (negative liberty), but in paragraph 3, "freedom = capacity to realize one's will" (positive liberty) — if this shift in distinction is not flagged, it may constitute a covert substitution of concepts.

**Output**: Drift detection results for each distinction.

### Step 5: Distinction Network Analysis

Analyze the interrelations among distinctions:

- **Parallel distinctions**: Two distinctions operate independently, with no intersection
- **Nested distinctions**: One distinction is a sub-distinction of another (e.g., negative/positive liberty → each further divided into formal/substantive liberty)
- **Colliding distinctions**: Two distinctions intersect in application, producing unclear categories

**Output**: Distinction network diagram.

### Step 6: Missing Distinction Detection

Based on the text's argumentative goals and known domain knowledge, detect **distinctions that ought to have been drawn but were not**:

- Has a domain-standard distinction been omitted by the text?
- Does the text fail to distinguish along a dimension important to the argument?
- Does this omission constitute an argumentative defect?

**Output**: A list of missing distinctions.

### Step 7: Output the Tracking Report

```
## Distinction Tracking Report

### Basic Information
- **Tracking ID**: DIST-<xxx>
- **Text**: <text citation>
- **Total distinctions**: <number>

### Distinction Inventory

| ID | Concept A vs. B | Type | Exhaustive? | Mut. Exclusive? | Location |
|----|-----------------|------|-------------|-----------------|----------|
| D1 | X / Y           | Dichotomy | Yes / No | Yes / No | §2 ¶3 |
| ... | | | | | |

### Function Analysis for Each Distinction

#### D1: <name>
- **Function**: <Clarificatory / Refutational / Defensive / Space-partitioning / Definitional>
- **Role in the argument**: <explanation>
- **Consequence if this distinction were absent**: <explanation>

### Consistency Check

| ID | Drift in later uses? | Specific issue |
|----|---------------------|----------------|
| D1 | Yes / No | <if drift, describe location and nature> |
| ... | | |

### Distinction Network

```
D1 (X/Y) ──── nested ────┬── D2 (Xa/Xb)
                          └── (none)
D3 (P/Q) ──── parallel ──── D1 (X/Y)
```

### Missing Distinctions

- <Domain-standard distinction name>: <why it is a relevant missing distinction>
- ...

### Overall Assessment

- Distinction reliance: <the text's degree of reliance on distinctions — Low / Medium / High>
- Key issues: <most significant drift, collision, or omission>
```

## Quality Criteria

1. **Exhaustiveness is not true by default**: If a distinction is presented as exhaustive, must test whether there genuinely are no other possibilities
2. **Drift cannot be ignored**: Even small conceptual drift at key argumentative steps can be amplified into argumentative error
3. **Distinctions are not the more the better**: Invalid or ad hoc distinctions weaken an argument — note cases of excessive or unsupported distinction-drawing

## Relationship to Other Skills

**Dependencies**:
- `phil-conceptual-analysis`: provides deep analysis of individual concepts (optional input)

**Dependents**:
- `phil-dialectical-map`: annotates in the dialectical tree where different arguments use different distinctions
- `phil-counterexample`: uses drifting distinctions as material for counterexample construction

## Boundary Conditions

1. **No distinction content**: If the text is wholly narrative or purely deductive, with no conceptual distinctions → output "No trackable distinctions detected"
2. **Unobvious distinctions**: If a distinction is implicit (not explicitly stated), annotate as "implicit distinction" and provide the inferential basis

## ARS Interface

- The distinction index table can be passed to ARS `academic-paper` as the paper's conceptual framing section
- Drift detection results can serve as critical material for ARS `academic-paper-reviewer`
- The missing-distinction list can be passed to ARS `deep-research` for retrieving standard distinction literature in the domain
