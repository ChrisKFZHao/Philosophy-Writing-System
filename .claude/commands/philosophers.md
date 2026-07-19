---
description: "Maintain the source-backed philosopher database — inspect private observations, review and apply candidates, lazily audit held sources, validate profiles, and rebuild domain views"
---

<!-- Generated from Framework/Workflow. Do not edit directly. -->
# /phil:philosophers

## Usage

```text
/phil:philosophers status
/phil:philosophers review [person-id]
/phil:philosophers approve <candidate-id>
/phil:philosophers reject <candidate-id>
/phil:philosophers reopen <candidate-id>
/phil:philosophers audit <person-id>
/phil:philosophers rebuild
```

## Invariants

- `Shared/Philosophers-DB/Profiles/` is the only canonical knowledge store. Domain Markdown files are generated link views.
- `Private/Bibliography/Philosopher-Queue/` contains unreviewed observations and decisions; never copy its local paths or project-use data into Shared.
- A `prompt-only` claim is `[source unverified]` and cannot support an assertion. A `source-backed` claim must carry a bibliography KEY, primary/secondary source type, analysis level, locator, and approval time.
- Approval changes semantic content; always show the exact candidate, evidence, target profile, and merge/new-claim action before applying it. A contradictory candidate adds evidence and marks the claim contested; it never overwrites history.
- The database routes to evidence. Any manuscript citation still cites the bibliography source and passes the two-hop Citation Gate.

## Operations

### status

Run `philosopher-db.py status --json`. Report processed artifacts, observed people, and candidate counts in Chinese. Do not load profiles or observations.

### review

Run `status --person <id-or-name>`, then read only the selected canonical profile and the summary/analysis artifacts named by its pending candidates. Present candidates grouped as new person, new claim, additional evidence, conflict, and domain link. Do not approve anything implicitly.

### approve / reject / reopen

Treat the explicit command as the user's decision. For approval, verify the cited KEY exists in `Private/Bibliography/INDEX.md`, the locator exists in the held artifact, and primary/secondary classification is correct. Apply the exact candidate with `philosopher-db.py approve`; use `--merge-claim-id` only after identifying the same claim, and use `--statement`/`--category` only for the wording the user approved. Use the matching deterministic subcommand for reject or reopen, then report the resulting candidate status.

### audit

Audit one person lazily in this order: bibliography INDEX rows mentioning the person → Level 0.5 summaries → existing analyses → only the necessary PDF page/section. Assemble the grounded results as one `observation-batch` JSON in a temporary file, submit it through `philosopher-db.py observe --input <temporary-file>`, then remove the temporary file. This keeps audit idempotent and uses the same queue path as ingest. Do not approve candidates and do not search externally by default.

### rebuild

Run `philosopher-db.py rebuild`. This validates every profile, regenerates INDEX and domain views, and fails rather than publishing an invalid source-backed claim.

## Output

Write reports in Chinese. Keep person IDs, candidate IDs, bibliography KEYs, statuses, and domain IDs in English.
