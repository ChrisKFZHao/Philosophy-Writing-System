# AGENTS.md

Guidance for AI agents working in this repository. Project status: **alpha**.

This is a philosophical reading and writing workflow, not a software project. Manuscripts, analyses, and bibliography are text or PDF. Helper scripts live only in `Framework/Workflow/Scripts/`; they read secrets from user-level configuration and never print them.

## Rules

Full text is in `Framework/Workflow/Rules/`. Read the relevant file before a gate, citation, or version decision.

1. **No sycophancy; Socratic only when needed** ([socratic-engagement.md](Framework/Workflow/Rules/socratic-engagement.md)). Assess clarity first. Clear idea: execute. Vague idea: question it. Never invent objections to look rigorous. At workflow gates and section boundaries, challenge a nameable defect; otherwise complete charitably and disclose it with `[AI 补全]`. Dialogue gates never hard-block.
2. **No hallucinated citations** ([citation-integrity.md](Framework/Workflow/Rules/citation-integrity.md)). Never generate unverified references, quotations, page numbers, or publication details. Mark them `[source unverified]` or `[citation needed]`. The Citation Gate cannot be waived.
3. **Trigger-based versions** ([version-management.md](Framework/Workflow/Rules/version-management.md)). Cut a version only after a post-review revision, a new argument, or a significant compression or expansion. Same-day triggers merge. `-draft.txt` is never versioned.
4. **Runtime compatibility** ([runtime-compatibility.md](Framework/Workflow/Rules/runtime-compatibility.md)). Follow the shared policy for project guidance, collaboration aliases, delegation, and Zotero degradation.

## Entry points

The `phil` plugin in `Framework/Plugin/` provides these skills to Claude Code (`/phil:<name>`) and Codex. If your host has not loaded the plugin, read `Framework/Plugin/skills/<name>/SKILL.md` and follow it.

| Entry | Purpose | Modes |
|---|---|---|
| `phil:research` | Work on sources | `ingest`, `reconstruct`, `evaluate`, `comment`, `translate`, `philosophers` |
| `phil:tutor` | Dialogue with the user | `reading`, `incubating` |
| `phil:write` | Write a manuscript, or export it as a handout or slides | `outline`, `draft`, `revision`, `export` |
| `phil:review` | Read-only peer review | `full`, `targeted`, `re-review` |
| `phil:full` | End-to-end pipeline | `start`, `status`, `resume` |

An explicit mode wins. Clear natural-language intent routes automatically. A material ambiguity gets one focused question.

Methods and services are internal. Load them only as a skill directs, through `Framework/Workflow/manifest.json`.

## Repository map

```
AGENTS.md          This guide
Framework/
  Plugin/          The phil plugin: public skills for both hosts
  Workflow/        manifest, Methods, Services, Rules, Schemas, Contracts,
                   Commands, References, Templates, Scripts, Tests
  ARCHITECTURE.md  changelog.md  Lessons/  Plans/
Shared/            Philosophers-DB, Format templates
Private/           Manuscripts, bibliography, style samples
```

`Private/` is an independent git repository with a private remote. The outer repository never tracks it. Run git for writing content inside `Private/`.

## Language and naming

- Definition layer (rules, skills, methods, schemas, architecture, changelog, this file): English.
- Writing output (manuscripts, analysis and review reports): Chinese.
- `README.md` and the report templates in `Framework/Workflow/Templates/` stay in Chinese.
- Directories start with an uppercase letter. Filenames use lowercase kebab-case. Project directories use the kebab-case topic.
- Bibliography files share the stem `{Author}_{Year}_{Title}`. Read the naming section of the conventions file before renaming or registering a source.

## Working in a project

- A project lives in `Private/Projects/{topic}/`. Read its `PROJECT.md` first; it overrides these defaults.
- Collaboration is `user-led` (default) or `assistant-led`. In `user-led`, never rewrite the manuscript without passage-level authorization.
- Manuscripts are plain text. Core files: `{topic}-draft.txt`, `{topic}-v{N}.txt`, `refs.md`, `VERSIONS.md`. Every other file you generate (conception, outline, review, sheets, summaries, analyses, intermediate drafts) is Markdown (`.md`).
- To cut a version, copy the draft to `{topic}-v{N}.txt` and record the date, triggers, and description in `VERSIONS.md`.
- Workflow state and the idea ledger are maintained only through `Scripts/project-state.py` and `Scripts/idea-ledger.py`.

## Bibliography and citations

- `Private/Bibliography/INDEX.md` is the master inventory. Source PDFs in `Private/Bibliography/PDF/` are tracked in the private repository; extraction caches and rendered exports are not.
- Analysis levels are progressive: 0.5 summary, 1 reconstruction, 2 implicit premises and concepts, 3 dialectical and domain analysis.
- Every citation passes the two-hop Citation Gate: the KEY is registered in the project's `refs.md`, and its `.analysis.meta.json` is verified, deep enough, and hash-current. See `Framework/Workflow/Services/citation-gate.md`.
- `prompt-only` claims in `Shared/Philosophers-DB/` are unverified hints and can never support a citation.

## Keeping cost down

- Read the cheapest sufficient level: INDEX row, summary, analysis, PDF page range, then full text.
- Query the compact state helpers before rereading artifacts. Reuse hash-valid outputs and report stale ones.
- Check `Framework/Workflow/Scripts/` and `Framework/Lessons/` before writing a helper. An inline solution needed twice becomes a script.
- Use batch operations for two or more items.
- Delegate only repeatable, read-only work, as Rule 4 describes, and validate the result before relying on it.

## Common commands

Run from the repository root. Where `python` is not available, use `py -3`.

```bash
python Framework/Workflow/Scripts/workflow-doctor.py
python Framework/Workflow/Scripts/build-adapters.py --check
python Framework/Workflow/Scripts/content-doctor.py
python -m unittest discover -s Framework/Workflow/Tests -p 'test_*.py'
wc -m "Private/Projects/{topic}/{topic}-draft.txt"
```

## More detail

- [Project conventions](Framework/Workflow/References/project-conventions.md): file naming, per-project files, analysis levels, PDF intake, Zotero, LaTeX, session logging, token economy.
- [Architecture](Framework/ARCHITECTURE.md): system design and inventory.
- [Zotero integration](Framework/Lessons/zotero-integration.md): the full linked-file workflow.

Durable shared state belongs in project artifacts, `Framework/Lessons/`, or the gitignored `history.txt`. At the end of a conversation, append a session summary to `history.txt`.
