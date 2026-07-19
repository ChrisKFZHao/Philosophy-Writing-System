<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Citation Integrity Rules

Never generate unverified references, quotations, page numbers, or publication details.

## Behavioral Guidelines

- **No fabricated bibliography**: Cite only works you have actually read — via this project's PDFs, notes, or reconstruction texts. If unread, explicitly mark with `[source unverified]` or `[citation needed]`
- **No invented quotations**: Do not produce "as X argues in Y..." content unless you have actually read the source and can verify the quotation
- **Distinguish known from inferred**: If you infer a philosopher's position or a source's existence from general philosophical knowledge, use explicit hedging ("presumably...", "possibly...", "it appears that...") and never mix it with assertoric language
- **Philosopher database is a routing layer, not a citation exception**: `source-backed` claims in `Shared/Philosophers-DB/Profiles/` may orient analysis only by routing to their evidence KEY. Manuscripts must cite that source and pass the normal two-hop Citation Gate. `prompt-only` claims are `[source unverified]` discovery hints and must not appear as unsupported assertions

## Citation Gate (two-hop check)

Every citation in a manuscript must pass two-hop verification; failure at either hop means **BLOCK**:

1. **Hop 1 (paper list)**: The cited KEY must appear in this paper's `refs.md` (`Private/Projects/{topic}/refs.md`). Not in the list → first register the source in refs.md (status `cited`)
2. **Hop 2 (analysis level)**: The KEY's analysis level in `Private/Bibliography/INDEX.md` must satisfy the dependency level of the cited claim. If a manuscript claim depends on Level N analysis but the source's `.analysis.txt` is only at Level N-1 or below → BLOCK and require the analysis to be completed first
