# Dialectical Mapping Quality Checklist

> After each dialectical mapping analysis, check each item. A fully checked list indicates a high-quality dialectical tree report.

---

## Thesis Identification & Root Node

- [ ] **Central thesis correctly identified**: The root node T is the actual thesis under debate, not a tangential claim or a reformulation that changes its argumentative content.
- [ ] **Thesis ownership annotated**: The proponent of T is identified — whether a specific author, text, school, or generalized philosophical position.
- [ ] **Core argument reconstructed**: The thesis node includes at least a brief reconstruction of the proponent's central inferential chain (may reference a `phil-argument-reconstruct` report).
- [ ] **Compound thesis decomposed**: If T is a compound claim (e.g., conjunctive or biconditional), its constituents are separated and each tracked individually through the dialectical tree.
- [ ] **Thesis scope clarified**: The intended scope of T (universal, domain-restricted, ceteris paribus) is noted, as it determines which objections are relevant.

## Objection Coverage

- [ ] **All major objections captured**: Every objection raised against T in the source texts is present as an O-node — no significant objection is omitted.
- [ ] **Objection type correctly classified**: Each objection is classified into one of the six recognized types — Counterexample, Logical, Reductio, Distinction, Incoherence, or External Challenge — with justification.
- [ ] **Attack point precisely annotated**: For each objection, the specific target is named — which premise [T.P1, T.P2, ...], inferential step [P1+P2 to C], or conclusion of the thesis is attacked.
- [ ] **Objection ownership annotated**: The source of each objection (author, text, school) is recorded, especially in cross-text dialectics.
- [ ] **Implicit objections considered**: Objections that are logically implied by the debate structure but not explicitly raised in the texts are flagged as implicit objections with Low confidence.

## Response Tracking

- [ ] **Every objection has a response or an "unresponded" flag**: No objection node is left without either a response node or an explicit annotation that the proponent has not yet responded.
- [ ] **Response strategy correctly classified**: Each response is classified into one of the six recognized strategies — Reject Counterexample, Distinction Defense, Scope Restriction, Premise Explicitation, Thesis Revision (T'), or Reject Objection's Premise — with justification.
- [ ] **Response- objection linkage bi-directional**: Each response node explicitly references the objection it addresses, and each objection node references its response(s). Links are not broken or one-directional.
- [ ] **Thesis revision (T') tracked as a new node**: If the proponent revises the thesis in response to an objection, the revised thesis T' is tracked as a distinct node with its own argumentative content.
- [ ] **Response adequacy assessed**: Beyond merely describing the response strategy, the analysis evaluates whether the response actually succeeds in neutralizing the objection.

## Counter-Response & Iteration

- [ ] **Counter-responses traced**: For each response, any further objections raised against it are mapped as C-nodes, continuing the dialectical iteration.
- [ ] **Dialectical depth preserved**: Multi-round attack-response sequences are not compressed into a single layer — at minimum the Objection, Response, and Counter-Response layers are preserved if present.
- [ ] **Convergence or divergence assessed**: Whether the dialectical process is converging (objections being resolved), diverging (new disagreements emerging), or stalled is explicitly noted.
- [ ] **No premature closure**: If the debate contains further rejoinders that have not been mapped, the tree does not declare closure — the analysis acknowledges incompleteness.

## Dialectical Status Assignment

- [ ] **Status for every node**: Each node (T, O-nodes, R-nodes, C-nodes) has a dialectical status — refuted, survived, weakened, pending, or abandoned.
- [ ] **Status triggering conditions met**: Each status assignment is justified by reference to the triggering conditions defined in the SKILL.md (e.g., "refuted" only if the objection is widely accepted and unrepairable).
- [ ] **Status consistency across tree**: If a thesis is marked "survived" but one of its supporting premises is marked "refuted," this inconsistency is flagged and explained.
- [ ] **Abandoned status evidenced**: If a thesis or response is marked "abandoned," textual evidence (e.g., later publications) shows the proponent has substantively dropped the claim — not merely that the claim is weak.

## Tree Structure & Formal Properties

- [ ] **No circularities**: The dialectical tree contains no circular attack-response chains (e.g., O1 attacks T, R1 defends T by invoking what O1 denies).
- [ ] **Proper nesting maintained**: Counter-responses are correctly nested under their target responses; objections are correctly nested under their target thesis nodes.
- [ ] **ASCII diagram well-formed**: The text diagram uses consistent tree-drawing characters, correctly represents the parent-child relations of all nodes, and is visually parseable.
- [ ] **Depth and breadth balanced**: The tree captures both the number of distinct objection lines (breadth) and the depth of iteration on the most significant lines.
- [ ] **Node count reasonable**: The tree includes all dialectically significant moves without being bloated by minor terminological quibbles or redundant restatements.

## Dialectical Fairness & Historical Fidelity

- [ ] **Principle of charity applied dialectically**: Each party's argument — proponent and critic alike — is presented in its strongest version before critique. No straw-manning of objections or responses.
- [ ] **Role annotation unambiguous**: Every node explicitly distinguishes "who is asserting what" — the voice of the proponent and the voice of the critic are never conflated.
- [ ] **Moves match actual debate**: The dialectical moves attributed to parties correspond to arguments actually made in the source texts — not imagined moves that "would be" good responses.
- [ ] **Historical sequence respected**: If the debate has a chronological dimension, the temporal order of dialectical moves is preserved (or explicitly noted if reordered for clarity).
- [ ] **Unresolved disagreements listed**: All nodes marked "pending" or where the dialectic remains open are collected in the Overall Assessment's unresolved-disagreements list.

## Report Quality

- [ ] **Executive summary present**: A one-paragraph overview covers dialectical depth, current thesis status, key turning point, and unresolved disagreements.
- [ ] **All node types present in report**: Thesis node, objection layer, response layer, counter-response layer (if applicable), and dialectical tree diagram are all included in the output.
- [ ] **Dialectical tree diagram included**: A text-based tree diagram using ASCII characters correctly represents all nodes and their relations.
- [ ] **Overall assessment substantive**: The final assessment goes beyond summarizing the tree — it identifies the most significant dialectical turning point and explains why it matters.
- [ ] **Source references complete**: For cross-text dialectics, every node includes a source citation (author, text, page/section) so the mapping is auditable.
