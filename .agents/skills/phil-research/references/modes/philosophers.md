<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Mode contract: philosophers

Maintain the source-backed philosopher database: inspect private observations, review and apply candidates, lazily audit held sources, validate profiles, and rebuild domain views. All operations are deterministic delegations to one service.

## Usage

```
phil:research philosophers status
phil:research philosophers review [person-id]
phil:research philosophers approve <candidate-id>
phil:research philosophers reject <candidate-id>
phil:research philosophers reopen <candidate-id>
phil:research philosophers audit <person-id>
phil:research philosophers rebuild
```

## Execution

Every operation routes to `Services/philosopher-db.md` (which drives `Scripts/philosopher-db.py`). Read that service file before executing. This contract adds only:

- **status** — counts only; no profile loading.
- **review** — the selected profile plus only the artifacts its pending candidates name; candidates presented grouped, nothing approved implicitly.
- **approve / reject / reopen** — the explicit subcommand is the user's decision; approval verifies KEY existence in INDEX, locator existence in the held artifact, and correct primary/secondary classification **before** applying, and routes evidence through `Services/citation-gate.md` (`philosopher-claim-gate`).
- **audit** — the lazy ladder (INDEX rows → summaries → analyses → minimal PDF pages), submitted as one deterministic observation batch.
- **rebuild** — validates every profile and fails rather than publishing an invalid source-backed claim.

## Authority

Queue and profile writes go through the service's explicit paths only. Semantic approval is always explicit and source-backed; a `prompt-only` claim stays `[source unverified]` and can never support an assertion or bypass the Citation Gate. Private queue data (local paths, project-use) never enters `Shared/`.

## Output

Reports in Chinese; person IDs, candidate IDs, bibliography KEYs, statuses, and domain IDs in English.
