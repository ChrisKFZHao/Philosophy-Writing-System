<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Runtime Compatibility

Apply these rules in both Claude Code and Codex.

## Project Guidance

Resolve project guidance in this order: `PROJECT.md`, `AGENTS.md`, then `CLAUDE.md`.
Use the first file found as authoritative. A new project should use `PROJECT.md` plus
the two thin runtime adapters from `Framework/Workflow/Templates/Project/`.

When a project is inside a nested repository (for example `Private/Projects/<topic>`),
the nested repository is a content boundary, not a second workflow source. Resolve the
nearest ancestor containing both `Framework/Workflow/` and the outer runtime adapter
directories (`.agents/skills/` or `.claude/`). Use the generated bridge in the nested
repository only to reach that outer source; never copy or silently substitute skill text.

## Collaboration Modes

Accept `user-led` and `assistant-led`. Normalize the legacy values `claude-led` and
`codex-led` to `assistant-led`, state that the alias is deprecated, and continue.
Use `[AI 补全]` for every new charitable completion. Preserve historical disclosure
markers when quoting or editing an existing artifact.

## Cost-Aware Delegation

Core workflows, roles, manifests, and output contracts must not map a workflow or role
to a provider or concrete model. Treat economical model use as a session-scoped prompt
policy, not as a static task category or an automatic router.

Keep temporary session state as `economic_delegation = unknown | enabled | disabled`.
When the first eligible task appears in a session, ask the user once whether a lower-cost
host candidate may be used and, if enabled, which host candidate to reuse. Never persist
this authorization beyond the current session; the user may revoke it at any time. After
revocation, set the state to `disabled` and do not ask or delegate again in that session.

An eligible task must be repeatable, independent, read-only, non-interactive, and return
only a discardable candidate artifact. The parent task must validate that artifact before
writing project or bibliography files, treating any claim as verified, or using it in the
Citation Gate. Suitable examples include summary drafts, topic-tag candidates,
structured extraction, and citation candidates.

Writing and revision, formal review, Citation Gate decisions, bibliography or project
changes, user-facing dialogue, and workflow orchestration always retain the current
session model. If the authorized candidate is unavailable or insufficient, retain the
current model rather than automatically choosing another candidate. Do not claim a
candidate is optimal without host-provided cost, cache, latency, and quality evidence.

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
