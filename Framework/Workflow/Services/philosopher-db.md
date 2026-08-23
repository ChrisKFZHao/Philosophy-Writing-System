---
id: service.philosopher-db
kind: service
authority: "write — private queue maintenance and deterministic view rebuild; semantic approval is always explicit and source-backed"
consumers: [phil-research/philosophers, phil-research/ingest]
scripts: [philosopher-db.py]
contract: Shared/Philosophers-DB (canonical profiles), Private/Bibliography/Philosopher-Queue (private)
---

# Philosopher Database Maintenance Service

Maintains the source-backed philosopher database: private observation queue, candidate review, explicit approval, lazy audit, validation, and domain-view rebuild.

## Invariants

- `Shared/Philosophers-DB/Profiles/` is the only canonical knowledge store; domain Markdown files are generated link views.
- `Private/Bibliography/Philosopher-Queue/` holds unreviewed observations and decisions; its local paths and project-use data never enter Shared.
- A `prompt-only` claim is `[source unverified]` and cannot support an assertion. A `source-backed` claim carries a bibliography KEY, primary/secondary type, analysis level, locator, and approval time, and its evidence must pass the Citation Gate (`service.citation-gate`).
- Approval changes semantic content: always show the exact candidate, evidence, target profile, and merge/new-claim action before applying. A contradictory candidate adds evidence and marks the claim contested; it never overwrites history.
- The database routes to evidence: a manuscript still cites the bibliography source through the Citation Gate.

## Operations

- **status** — `philosopher-db.py status --json`; report processed artifacts, observed people, candidate counts. Do not load profiles.
- **review [person]** — `status --person <id>` first, then read only the selected canonical profile and the artifacts named by its pending candidates. Present candidates grouped: new person / new claim / additional evidence / conflict / domain link. Never approve implicitly.
- **approve / reject / reopen** — the explicit command is the user's decision. On approval, verify the KEY exists in INDEX, the locator exists in the held artifact, and primary/secondary classification is correct. Apply via `philosopher-db.py approve` (`--merge-claim-id` only after identifying the same claim; `--statement`/`--category` only for approved wording). Reject/reopen use the matching deterministic subcommand; report the resulting status.
- **audit <person>** (lazy, this order): INDEX rows mentioning the person → Level 0.5 summaries → existing analyses → only the necessary PDF page/section. Assemble one `observation-batch` JSON in a temporary file, submit via `philosopher-db.py observe --input <temp>`, then remove the temp file (idempotent, same queue path as ingest). Do not approve candidates; do not search externally by default.
- **rebuild** — `philosopher-db.py rebuild`: validates every profile, regenerates INDEX and domain views, and **fails rather than publishing an invalid source-backed claim**.

Reports are written in Chinese; person IDs, candidate IDs, bibliography KEYs, statuses, and domain IDs stay in English.
