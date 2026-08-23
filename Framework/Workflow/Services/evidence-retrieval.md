---
id: service.evidence-retrieval
kind: service
authority: read — deterministic local extraction and cache reads; never mutates sources
consumers: [phil-research/reconstruct, phil-research/evaluate, phil-tutor, phil-write, phil-review]
scripts: [pdf skill extraction, hash-verified reuse]
contract: Contracts/evidence-unit.schema.json
scope: "0.7.0: local deterministic extraction + cache/index contract; vector embeddings and external RAG deferred to 0.7.1 pending recall/precision fixtures"
---

# Evidence Retrieval Service

Defines how evidence is located, quoted, and reused without re-extracting whole PDFs into model context.

## Evidence units

Every quoted or analyzed passage is exchanged as an **evidence unit** (`Contracts/evidence-unit.schema.json`): locator (page/section/paragraph), exact text span, source identity (bibliography KEY + file stem), source SHA-256, extraction version, and unit hash. A retrieved evidence packet always includes the hit, its local paragraph neighborhood, the locator, the selection reason, and its verification status.

## Retrieval rules

1. **Reuse before reopening**: consult hash-current extraction units and reading maps before reopening a PDF. A unit is reusable only when its recorded source SHA-256 matches the current file and its extraction version is current.
2. **Extraction-version invalidation**: bumping the extraction version invalidates cached units from older versions; they are re-derived lazily, not trusted.
3. **Neighborhood expansion**: a locator hit is always presented with its local paragraph neighborhood — never a bare sentence torn from context.
4. **Partial retrieval never counts as full reading coverage.** The Citation Gate and final analyses require explicit page/section provenance; an evidence packet assembled from keyword hits is labeled partial coverage and cannot upgrade an analysis level by itself.
5. A complete PDF is never loaded into model context when locators and units already answer the question (token-economy rule 4: read at the cheapest sufficient level).

## 0.7.0 scope

Local deterministic extraction (via the `pdf` skill) plus the cache/index contract above. A SQLite FTS5 or hybrid RAG implementation is a 0.7.1 follow-up, to be adopted only after recall/precision fixtures exist; until then no vector database or external embedding service is introduced.
