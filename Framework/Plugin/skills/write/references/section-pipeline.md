# Section pipeline

Status: **default** for draft mode since 2026-11-22, after a two-round pilot the user accepted. Use the classic procedure in `SKILL.md` only when the user asks for it or `PROJECT.md` sets `drafting: classic`.

The pipeline separates deciding what a section says from saying it well, and checks the prose with a reader who did not write it. The model never revises its own long draft in one context: research on LLM editing finds that rewriting matters more than spotting problems, and that self-editing works poorly on paragraph-length text.

## Roles

| Role | Who | Sees |
|---|---|---|
| Orchestrator | the session running `phil-write` | everything: outline, analyses, conversation |
| Composer | fresh subagent | only the inputs listed in step 2 |
| Editor | fresh subagent | only the inputs listed in step 4 |
| Cold reader | fresh subagent | only the finished prose and a one-line topic |

Composer, editor, and cold reader run on the current session model; writing and review never move to a cheaper model (Rule 4). If the host cannot start subagents, run each role serially in the same session: before each role, restate only that role's inputs and set earlier drafts aside. Record in the section log that the cold read was not independent.

## Steps for one section

1. **Argument sheet** (orchestrator). Write the sheet as `argument-sheet.md` specifies. Analysis methods are loaded here and nowhere else. **Gate:** the user confirms or edits the sheet. Before asking, list every 界限 line and every claim that says what something is not, each with the misreading it blocks, and propose which to cut (`argument-sheet.md`). This disclaimer review is required, because every surviving line becomes prose. Rule 1 lenient interrogation applies: challenge a nameable defect; fill any other gap and disclose it with `[AI 补全]`. In `assistant-led` mode the user may confirm all sheets of a paper at once.
2. **Compose** (composer). Inputs: the sheet; the last paragraph of the previous section, or the paper's thesis sentence for the first section; `Private/Style/style-card.md`; two or three passages from `Private/Style/exemplars/`; `compose.md`. Never pass analysis reports, method files, the outline, or earlier drafts of the section.
3. **Lint** (script). Run `python Framework/Workflow/Scripts/prose-lint.py <prose file> --json`, adding `--glossary Private/Projects/{topic}/glossary.md` when that file exists. Its flags are prompts for judgment.
4. **Edit** (editor). Inputs: the prose, the sheet, the lint report, the style card, and `edit-passes.md`. Make three passes in order: structure, then sentences, then terms and citations. Each pass uses only its own checklist and must not add, drop, strengthen, or weaken a claim.
5. **Cold read** (cold reader). Inputs: the edited prose and one line naming the paper's topic. Follow `cold-read.md`.
6. **Compare** (orchestrator). Check the cold reader's claim list against the sheet and classify each finding as prose, argument, or context, as `cold-read.md` describes.
   - **pass**: go to step 7.
   - **revise**: send the editor only the prose-caused gaps, then repeat steps 4–6. Allow at most two revision rounds. After that, stop and show the user the remaining gaps instead of polishing further, because extra rounds drift toward bland prose.
   - Argument-caused findings never go to the editor. Present them to the user at step 7 as review notes; if the user changes the sheet, restart the section at step 2.
7. **Finalize** (user). Present the prose, the editor's change log, the cold-read result, and the lint flags that were deliberately kept. The user edits and approves. If the user changed the text, run `prose-lint.py <final> --compare <pipeline output>`, then add the user's recurring edits to `Private/Style/style-ledger.md`. A ledger entry becomes a style-card rule only after the user confirms it.

## Collaboration modes

- **assistant-led**: run steps 1–7.
- **user-led**: the user writes the prose, so skip step 2. In step 4 the editor returns a numbered list of suggested edits, never a rewritten section. Report the cold-read comparison to the user. Apply only the edits the user accepts.

## Files and state

- Sheets, prose versions, and section logs live in `Private/Projects/{topic}/{topic}-sheets/` as `{nn}-{slug}.sheet.md`, `{nn}-{slug}.prose.md`, and `{nn}-{slug}.log.md`. They are living files and are never versioned. The manuscript stays in `{topic}-draft.txt`.
- Record artifacts with `Scripts/project-state.py artifact --kind argument-sheet`, `--kind draft-section`, and `--kind cold-read-report`.
- The composer writes citations as `（作者，年份）` from the sheet's citation lines and never adds a source. The Citation Gate still applies at citation closure.

## Cost

Each section needs three to five subagent calls, each with small inputs. The composer and editor never load method files, which removes the largest cost of the classic procedure.
