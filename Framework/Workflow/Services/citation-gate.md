---
id: service.citation-gate
kind: service
authority: "read + block — verifies citations; never rewrites manuscripts or bibliography entries itself"
consumers: [phil-write, phil-review, phil-full, phil-research/reconstruct]
scripts: [workflow-policy.py citation-gate]
contract: Contracts/workflow-state.schema.json (unrelated) / Schemas/analysis-metadata-schema.json
---

# Citation Gate Service (Rule 2 enforcement, two-hop)

The semantic claim-to-source judgment is model-executed; artifact verification is deterministic. The gate is invoked at every manuscript citation, at citation closure, and before any philosopher-DB `source-backed` claim is used as evidence.

## Deterministic check

```bash
python "Framework/Workflow/Scripts/workflow-policy.py" citation-gate \
  --key <KEY> --refs <project>/refs.md \
  --required-level <N> \
  [--metadata <analysis.meta.json>] [--source-path <pdf>] [--analysis-path <analysis.md>]
```

`--registered` is a legacy boolean flag that asserts Hop 1 without reading the project file; when `--refs` is given it is ignored.

## The two hops

1. **Hop 1 — project registration**: the cited KEY must appear as the first cell of a row in this project's `refs.md`. A KEY that is absent (or appears only in another column) → `block, key-not-in-refs`; a KEY whose status is `rejected` → `block, key-rejected`.
2. **Hop 2 — verified, hash-current analysis**: the paired `.analysis.meta.json` must exist, declare at least the required level, carry `verification_status: verified`, and match the current PDF and analysis SHA-256 hashes. When `--key` is given and the metadata carries a `bib_key`, it must equal that KEY. Failure modes: `analysis-metadata-missing`, `analysis-level-insufficient`, `analysis-unverified`, `analysis-stale`, `analysis-key-mismatch`.

The INDEX level is an inventory view, **not** sufficient verification evidence.

## Rules of use

- Coverage recorded in analysis metadata uses canonical `method.<package>.<slug>` IDs (legacy labels and `phil-*` skill IDs normalize on read; new writes never use aliases).
- `provisional`, missing, stale, hash-mismatched, or shallow analyses → **BLOCK**. Escalate the analysis via `phil:research reconstruct` to the required level, then re-check.
- Citation existence, claim support, and bibliography closure are **three separate checks** — a passing gate does not certify that the bibliography is closed, and vice versa.
- Philosopher-DB claims route through `philosopher-claim-gate`: `prompt-only` claims are `[source unverified]` discovery hints and can never pass; `source-backed` claims must carry a bibliography KEY, source type, analysis level, locator, and approval time, with evidence passing both hops.
- The gate cannot be waived. Citation closure requires a machine PASS plus user acknowledgement; skipping is not an offered option.
