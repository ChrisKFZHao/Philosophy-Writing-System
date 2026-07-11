# Bibliography Index

> **Project Status: Alpha** — Analysis files are provisional; levels subject to revision upon PDF verification.

Tracks all references used in this project. Every citation in a manuscript must trace back to an analysis file here with sufficient level for the claim being cited.

## Structure

```
bibliography/
├── pdf/                              Original PDFs
├── analysis/                         Paired analysis files (.analysis.txt)
│   └── {Author-Title}.analysis.txt
└── INDEX.md                          This file
```

## Analysis Levels

| Level | Label | Content | Trigger |
|-------|-------|---------|---------|
| 1 | Reconstruction | Argument reconstruction (phil-reconstruct) | On PDF addition |
| 2 | Standard | + Implicit premises, charity audit, conceptual analysis, distinction tracking | On first citation in a manuscript |
| 3 | Deep | + Dialectical mapping, ontological commitment, modal analysis, domain-specific skills | When the source becomes a core target or key dependency |

Citation rule (Option A): if a manuscript claim depends on analysis at Level N, but the source's `.analysis.txt` is only at Level N-1 or below, **block and require analysis completion before proceeding**.

## Reference Inventory

| ID | Author | Title | PDF | Analysis Level | Manuscripts Using |
|----|--------|-------|-----|----------------|-------------------|
| SRINIVASAN-ANGER | Srinivasan, Amia | "Anger" | pdf/Anger__Srinivasan__A_.pdf | Level 3 | srinivasan-critique (core target) |

Note: analysis file provisional at Level 3 — arguments reconstructed from reading notes, pending PDF verification.

---

*Last updated: 2026-07-11*
