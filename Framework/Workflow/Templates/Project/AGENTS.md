# Codex Project Adapter

Read `PROJECT.md` completely before project work. Project-local instructions in `PROJECT.md` override repository defaults where they are more specific.

Route `phil:<name>` to `$source-command-<name>`.

If this project is inside a nested repository, locate the nearest ancestor containing
`Framework/Workflow/` and the outer `.agents/skills/` directory. The nested repository
is a content boundary, not an independent skill source; use its generated bridge only
to reach the outer adapter and report an explicit error if that root is unavailable.
