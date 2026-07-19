<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Citation Integrity Rules

Never generate unverified references, quotations, page numbers, or publication details.

## Behavioral Guidelines

- **No fabricated bibliography**: Cite only works actually read through this project's PDFs, notes, or reconstruction texts. If unread, mark the claim with `[source unverified]` or `[citation needed]`.
- **No invented quotations**: Do not produce "as X argues in Y..." content unless the source has been read and the attribution can be verified.
- **Distinguish known from inferred**: If a philosopher's position or a source's existence is inferred from general knowledge, hedge explicitly and never mix it with verified assertions.
- **Philosopher database is a routing layer, not a citation exception**: `source-backed` claims in `Shared/Philosophers-DB/Profiles/` may orient analysis only by routing to their evidence KEY. Manuscripts must cite that source and pass the normal two-hop Citation Gate. `prompt-only` claims are `[source unverified]` discovery hints and must not appear as unsupported assertions.

## Citation Gate (two-hop check)

Every citation in a manuscript must pass both checks; failure at either hop means **BLOCK**:

1. **Hop 1 (project registration)**: The cited KEY must appear in `Private/Projects/{topic}/refs.md`. If absent, register it before citation.
2. **Hop 2 (verified analysis)**: The paired `.analysis.meta.json` must exist, declare an `analysis_level` at least as high as the claim requires, have `verification_status: verified`, and contain SHA-256 values matching the current source and analysis artifacts. Missing metadata, provisional or stale status, insufficient level, or either hash mismatch means **BLOCK**.

The level displayed in `Private/Bibliography/INDEX.md` is an inventory view and cannot establish a pass by itself. A `provisional` analysis may guide further reading but cannot support manuscript prose. Mark an analysis `verified` only after its declared coverage has been checked against the current source; a changed source or analysis becomes `stale` until reverified.
