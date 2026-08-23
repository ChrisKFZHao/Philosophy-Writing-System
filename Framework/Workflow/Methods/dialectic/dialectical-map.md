---
id: method.dialectic.dialectical-map
package: dialectic
legacy_ids: [phil-dialectical-map]
label: Dialectical Mapping
consumers: [phil-research/reconstruct, phil-research/evaluate, phil-research/comment, phil-write, phil-review]
selector: feature-detected
side_effects: read-only
---

# Dialectical Mapping (method.dialectic.dialectical-map)

> Internal method module — not a registered runtime skill. Loaded on demand by the consuming skill's mode contract through the manifest resolver; never loaded wholesale.

# Dialectical Mapping

## Overview

Analytic philosophy is not monologue — it is dialectical, conversational. A complete philosophical debate contains multiple layers of attack and defense: thesis → objection → response → counter-response → revision → ... . This Skill maps this bidirectional adversarial process into a structured **dialectical tree**.

Unlike `method.argument.argument-reconstruct` (which maps the static structure of a single argument), this Skill maps **the interactive relations among multiple arguments** — who is attacking whom, whether the response succeeds, and what the dialectical status is.

## Input

- A complete philosophical debate (may span multiple text passages / multiple papers)
- Or multiple argument reconstruction reports (from `method.argument.argument-reconstruct`)
- Optional:
  - Conceptual analysis report (for tracking conceptual evolution)
  - Distinction-tracking report (for detecting whether distinctions shift during the dialectical process)

## Output

A structured **Dialectical Tree Report** conforming to the `dialectical-tree-schema.json` specification, containing:
- Thesis node (root node T)
- Objection nodes (O1, O2, ...)
- Response nodes (R1, R2, ...)
- Counter-response nodes (C1, C2, ...)
- An argument-reconstruction summary for each node
- Relation annotations between nodes (which premise/inferential step/conclusion is attacked)
- Dialectical status annotations (refuted / survived / weakened / pending / abandoned)

## Methodological Foundations

1. **Dialectical Logic**: The dialectical tradition predates formal logic — Socratic elenchus, Platonic dialogue form, Hegelian sublation (Aristotle, *Topics*; Hegel, *Phenomenology*)
2. **Argumentation Games**: Arguments can be modeled as bidirectional games — a turn-based structure of proponent and opponent (Lorenzen & Lorenz, 1978; Walton, 1996)
3. **Lakatos's "Proofs and Refutations"**: Mathematical and scientific argumentation evolves through a process of revision via counterexamples — "monster-barring," "exception-barring," "lemma-incorporation" (Lakatos, 1976)
4. **Elenctic Structure**: The distinctive form of Socratic debate — drawing the interlocutor into deriving a contradiction from their own beliefs, rather than introducing external evidence (Vlastos, 1983)

## Steps

### Step 1: Identify the Thesis Node (Root)

Locate the starting point of the debate — what is the original thesis?

- Is thesis T a single assertion or a compound claim?
- What is the core inferential chain of the thesis's proponent? (May reference `method.argument.argument-reconstruct` report)
- "Ownership" of the thesis — is it an assertion by a specific author/text, or a generalized philosophical position?

**Output**: Thesis node T, with a brief argument summary.

### Step 2: Map the Objection Layer

Identify objections raised against T.

Each objection is annotated with:
- **Attack point**: Which premise/inferential step/conclusion of T does this objection target?
- **Objection type**:
  - **Counterexample**: Provides a countervailing case
  - **Logical Objection**: Points out a logical error or implicit premise
  - **Reductio**: Derives an absurd consequence from T
  - **Distinction Objection**: Points out that T conflates a key distinction
  - **Incoherence**: T contradicts the proponent's other beliefs
  - **External Challenge**: Introduces evidence/principles not considered by T

**Output**: All first-level objection nodes O1, O2, ...

### Step 3: Map the Response Layer

For each objection, trace the T-proponent's response.

Each response is annotated with:
- **Response strategy**:
  - **Reject Counterexample**: The counterexample does not succeed
  - **Distinction Defense**: Exclude the counterexample by refining the concept through finer distinctions
  - **Scope Restriction**: Restrict the thesis to a narrower scope
  - **Premise Explicitation**: Supply a premise that was previously omitted
  - **Thesis Revision (T')**: Revise the original thesis in light of the objection
  - **Reject Objection's Premise**: Challenge the soundness of the objection itself

**Output**: Response nodes for each objection, R1, R2, ...

### Step 4: Iterate — the Counter-Response Layer

For each response, trace any further counter-responses.

If the dialectical process converges (all objections have been effectively responded to) → the dialectical tree closes
If the dialectical process diverges (new disagreements emerge) → a new round of objections and responses

**Output**: Counter-response nodes C1, C2, ... (if any)

### Step 5: Assign Dialectical Status

Each node is annotated with its current dialectical status:

| Status | Meaning | Triggering Condition |
|--------|---------|---------------------|
| **refuted** | The node has been effectively refuted | The objection is widely accepted; the response cannot repair it |
| **survived** | The response has successfully kept the node alive | The objection has been reasonably answered; no further effective counterexample exists |
| **weakened** | Significantly weakened but not fully refuted | The response holds but the thesis requires revision or scope restriction |
| **pending** | The dialectical process is not yet complete | Awaiting further argumentation |
| **abandoned** | The thesis's proponent has substantively abandoned the claim | In subsequent texts, the claim is no longer defended |

**Output**: Status for each node.

### Step 6: Output the Dialectical Tree

```
## Dialectical Tree Report

### Root Node

#### T: <thesis name>
- Source: <text/author>
- Core argument: <brief reconstruction>
- Status: survived / weakened / refuted / pending

### Objection Layer

#### O1: <objection name> — attacks [T.P2]
- Type: Counterexample / Logical / Reductio / Distinction / Incoherence / External
- Description: <brief explanation>
- Status: responded / unresponded

#### O2: ...

### Response Layer

#### R1: response to O1 — Strategy: Distinction Defense
- Description: <how it responds>
- Status: surviving / challenged

### Counter-Response Layer

#### C1: counter-response to R1 — defect in response strategy
- Description: <why R1 does not succeed>
- Status: pending

### Dialectical Tree (Text Diagram)

```
T (survived)
├── O1 (survived) ──── attacks T.P2
│   └── R1 (surviving) ── distinction strategy
│       └── C1 (pending) ── counter-response: scope not clearly delineated
├── O2 (weakened) ──── counterexample attack
│   └── R2 (weakened) ── scope restriction → T'
└── O3 (refuted) ──── logical contradiction attack
    └── R3 (refuted) ── response does not succeed
```

### Overall Assessment

- Dialectical depth: <number of layers>
- Current status of the thesis: survived / weakened / refuted / pending
- Key turning point: <the most significant objection or response>
- Unresolved disagreements: <list>
```

## Quality Criteria

1. **Role annotation**: Each node must explicitly annotate "who is asserting what" — do not conflate proponent and critic
2. **Dialectical fairness**: Each party's argument should be presented in its strongest version (the dialectical version of the principle of charity)
3. **No oversimplification**: Do not compress complex multi-round attack-response sequences into a single layer — preserve the integrity of the dialectical tree

## Relations to Other Skills

**Dependencies**:
- `method.argument.argument-reconstruct`: Provides standard-form arguments for each node
- `method.concept.conceptual-analysis` (optional): Tracks the evolution of conceptual analysis

**Dependents**: None (this is a terminal aggregator Skill)

## Boundary Conditions

1. **Single-argument scenario**: If there is only one isolated argument (with no objections or responses), use `method.argument.argument-reconstruct` rather than this Skill
2. **Cross-text dialectic**: If the dialectic spans multiple texts, annotate the textual source of each node
3. **Incomplete dialectic**: If the debate is still ongoing, annotate with "pending" status

## ARS Interface

- The dialectical tree can be directly converted into the "Literature Review and Critique" section of ARS `academic-paper`
- Unresolved debate nodes can serve as retrieval directions for ARS `deep-research`
- The dialectical tree can serve as a review framework for ARS `academic-paper-reviewer`
