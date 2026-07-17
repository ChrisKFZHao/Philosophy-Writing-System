<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Runtime Compatibility

Apply these rules in both Claude Code and Codex.

## Project Guidance

Resolve project guidance in this order: `PROJECT.md`, `AGENTS.md`, then `CLAUDE.md`.
Use the first file found as authoritative. A new project should use `PROJECT.md` plus
the two thin runtime adapters from `Framework/Workflow/Templates/Project/`.

## Collaboration Modes

Accept `user-led` and `assistant-led`. Normalize the legacy values `claude-led` and
`codex-led` to `assistant-led`, state that the alias is deprecated, and continue.
Use `[AI 补全]` for every new charitable completion. Preserve historical disclosure
markers when quoting or editing an existing artifact.

## Delegation

When delegation is available, parallelize only stages with no dependency relation.
When it is unavailable, execute the same dependency graph serially. Never change the
required inputs, output sections, or Citation Gate decision because of runtime limits.

## Zotero

Classify the available backend before `/phil:ingest` Step 8:

- `full`: Zotero MCP write tools and the linked-file helper are available. Run Step 8.
- `partial`: only a local Zotero plugin/API is available. Permit local search, export,
  and citation operations, but do not claim metadata registration or linked-file creation.
- `skipped`: no Zotero backend is available. Complete Steps 1-7 and emit a manual follow-up.

`--dry-run` never writes to Zotero, regardless of backend status.
