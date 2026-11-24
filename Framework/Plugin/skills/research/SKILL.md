---
name: research
description: "Work on philosophical sources: ingest PDFs, reconstruct or evaluate an argument, comment on a text, translate a reading passage, or maintain the philosopher database. Use for 文献入库、论证重构、批判性评估、文本评注、对照翻译、哲学家数据库."
---

# phil-research

> **Paths.** `<root>` is the nearest ancestor of the working directory containing `Framework/Workflow/manifest.json`; if there is none, stop and report it. `Framework/…` and `Private/…` paths resolve from `<root>`. Bare `Methods/`, `Services/`, `Rules/`, `Schemas/`, `Scripts/`, `Contracts/`, `Commands/`, `References/`, and `Templates/` paths resolve from `<root>/Framework/Workflow/`. Run scripts with `<root>` as the working directory.

One public skill because its six modes share one **research kernel**: source identity, title-page provenance, current source hashes, evidence locators, coverage planning with hash-current reuse, bibliography registration, and the Citation Gate boundary. The modes are otherwise isolated — each has its own contract file, method selection, and side-effect policy. This is a kernel share, not a claim that the modes are the same cognitive task.

## Modes

| Mode | Contract | Authority | Typical call |
|---|---|---|---|
| `ingest` | [references/modes/ingest.md](references/modes/ingest.md) | **write** — rename/register sources, enqueue observations, Zotero writes via service | `phil:research ingest [--dry-run] [pdf]` |
| `reconstruct` | [references/modes/reconstruct.md](references/modes/reconstruct.md) | read-only analysis; persists analysis artifacts under `Private/Bibliography/Analysis/` | `phil:research reconstruct --level <1|2|3> [--full] <text>` |
| `evaluate` | [references/modes/evaluate.md](references/modes/evaluate.md) | read-only critique of a source or analysis artifact | `phil:research evaluate [--full] <text>` |
| `comment` | [references/modes/comment.md](references/modes/comment.md) | read-only qualitative commentary; no bibliography or project mutation | `phil:research comment <argument or text>` |
| `translate` | [references/modes/translate.md](references/modes/translate.md) | **write** — translations and glossaries under `Private/Bibliography/Reader/{stem}/` | `phil:research translate <KEY> --pages 12-40` |
| `philosophers` | [references/modes/philosophers.md](references/modes/philosophers.md) | queue maintenance; semantic approval always explicit and source-backed | `phil:research philosophers <op>` |

## Routing

1. An explicit mode argument always wins.
2. Natural-language intent that maps cleanly to one mode routes automatically ("帮我消化这篇文献" → `reconstruct`; "扫描库里新 PDF" → `ingest`; "把这篇翻成中文对照读" → `translate`).
3. If a material ambiguity remains, ask **one focused question** instead of invoking several modes. Never run multiple modes speculatively.
4. Old command names are recognized and translated with an explicit notice: `phil:reconstruct/evaluate/comment/ingest/philosophers` → `phil:research <mode>`. A legacy name never silently selects a different mode than its replacement.

## Kernel invariants (all modes)

- **Source identity**: a source is its bibliography KEY (`AUTHOR-TITLE`) + canonical file stem. Metadata comes from the title page (Rule 2), never from model memory.
- **Provenance**: every analytical claim about a source is anchored to an evidence locator (page/section/paragraph) with a hash-current source SHA-256; partial retrieval never counts as full reading coverage (`Services/evidence-retrieval.md`).
- **Coverage and reuse**: persisted coverage is expressed in canonical `method.<package>.<slug>` IDs; reuse requires `verified` status plus matching source and analysis hashes. Stale artifacts are reported, never silently trusted.
- **Citation Gate boundary**: no manuscript-facing claim bypasses `Services/citation-gate.md` (two hops: refs.md registration + verified hash-current analysis).
- **Status vocabulary**: `full` / `partial` / `skipped` for Zotero; `verified` / `provisional` / `stale` for analyses; decisions `run` / `reuse` / `skip` in every preplan.
- **Disclosure**: new AI-authored completions carry `[AI 补全]` per the shared runtime policy.
- **External writes**: only `ingest` (via its services) registers sources in the library or writes to Zotero. `reconstruct` persists only its paired analysis artifacts under `Private/Bibliography/Analysis/` and their philosopher observations. `translate` writes only translations and glossaries under `Private/Bibliography/Reader/{stem}/` (plus a project glossary only when asked). `philosophers` writes only through the philosopher-db service. `evaluate` and `comment` write nothing. No mode edits manuscripts or `refs.md`.

## Method and service loading contract

Loading is deterministic; the manifest (`Framework/Workflow/manifest.json`) is the authoritative resolver:

1. Resolve the public skill and the explicit mode (this file).
2. Read **only** that mode's contract file under `references/modes/`.
3. Resolve the contract's method/service IDs through the manifest.
4. Read **only** the listed method files (`Framework/Workflow/Methods/<package>/<slug>.md`) and service files (`Framework/Workflow/Services/<slug>.md`), plus directly named schemas.
5. Fail with an explicit missing-ID error; never silently load an entire package, and never guess a replacement method.

Method files carry procedure and decision rules; the manifest carries identity, routing, dependencies, and exposure policy. Methods and services are never generated as runtime skills or adapters. Examples, extended checklists, and reference files stay unloaded unless a live ambiguity or an explicit request requires them.

## Cost-aware delegation

Apply the session-scoped policy in `Rules/runtime-compatibility.md`: on the first eligible task, ask once whether a lower-cost host candidate may be reused this session. Eligible work is repeatable, independent, read-only, non-interactive, and produces only discardable candidates that this skill validates before any write or Citation Gate use. Reconstruction and evaluation run their deterministic preplan before loading selected methods. If the candidate is unavailable or insufficient, retain the current model.

## Failure handling

- **Missing method/service ID in the manifest** → stop with `missing-ID <id>`; do not substitute.
- **Source hash changed** → affected coverage is `stale`; report and rerun only the dimensions the new target requires.
- **Zotero backend degraded** → `ingest` Steps 1–7 complete; Step 8 reports `partial`/`skipped` with a manual follow-up.
- **No translation gateway** → `translate` falls back to a subagent that follows `Templates/Translate/system.md` and writes the same records, then runs `translate.py check`. Credentials are never printed.
- **Ambiguous mode** → one focused question; never a multi-mode sweep.

## State behavior

Inside a recognized writing project (`Private/Projects/{topic}/`), runs update `{topic}-workflow-state.json` (schema v2, via `Scripts/project-state.py`); outside a project, this skill operates statelessly and creates no project files unless requested. Within `phil:full`, this skill is invoked by the pipeline's `research` stage and follows `Commands/phil-full.md`.

## Output language

Reports are written in Chinese (project convention); filenames, KEYs, method IDs, statuses, and topics remain in English.
