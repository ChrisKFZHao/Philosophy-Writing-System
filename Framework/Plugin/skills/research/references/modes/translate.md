# Mode contract: translate

Bilingual reading support: translate evidence units into Chinese, one unit at a time, and hand the result to `reader-build.py`. The translation is a reading aid, never a source.

## Usage

```
phil:research translate <KEY> --pages 12-40
phil:research translate <KEY> --from <UNIT_ID> --to <UNIT_ID>
phil:research translate <KEY> --all
```

Options: `--project <topic>` for the project glossary, `--out <dir>` for a scratch output, `--jobs N` for parallel requests, `--yes` to allow more than 60 uncached units, `--no-terms` to skip automatic term proposals.

## Authority

- Writes only under `Private/Bibliography/Reader/{stem}/`: `translation.jsonl`, `glossary.md`, and the derived `reader.html`.
- Writes `Private/Projects/{topic}/glossary.md` only when the user explicitly asks to commit proposed terms there.
- Never edits manuscripts, `refs.md`, the source PDF, or `Extract/` evidence units.
- Uses the user's model gateway. Credentials come from the environment or `~/.claude/settings.json`; never print, log, or write them.

## Procedure

1. **Resolve the source.** Find the KEY in `Private/Bibliography/INDEX.md`; the PDF cell gives the stem `Author_Year_Title`. Do not guess a stem from the request.
2. **Ensure evidence units exist.** Check `Private/Bibliography/Extract/{stem}/blocks.jsonl`. If absent, run `Scripts/pdf-extract.py blocks <pdf> --key <KEY>`. Run `pdf-extract.py ocr-needed <pdf>` first; if the selected pages are scanned, OCR only those pages (never the whole book by default).
3. **Choose the selection.** Translate what the user actually wants to read: the stated pages, section, or unit range. If the request does not identify a selection, ask one focused question. Never select the whole book unless the user asks for it.
4. **Plan.** Run `translate.py plan STEM [selection] --project <topic>`. Report selected, cached, verbatim, source characters, and the call estimate. If more than 60 units would be translated, show the estimate and ask before adding `--yes`.
5. **Terms.** Unless `run` will propose them automatically, run `translate.py terms ...`; show the proposed terms briefly and proceed unless the user objects. Proposed rows carry `自动提议，待确认`.
6. **Translate.** Run `translate.py run STEM [selection] --project <topic>`. Each finished unit is appended immediately; the file is compacted in document order at the end.
7. **Report QA.** Run `translate.py check STEM [--out <dir>]` and report flags by unit.
   - A `page-markers` error that survived the repair call must be fixed before the page is built: rerun that unit with `--force --from ID --to ID`.
   - A `glossary` error goes to the user with the unit. The source may legitimately use another sense (a quotation, or "angry" rendered 生气), so either rerun the unit or accept it.
   - Warnings are prompts for a human look. Never use them to justify silent edits.
8. **Build the page.** Run `reader-build.py STEM`. For interactive annotation, tell the user to run `reader-serve.py STEM`, which writes `user-notes.json` beside the page.

## Rule 2 boundary

- A translation is never a source. Manuscripts cite the original unit's printed page (the `⟦p…⟧` label), not the Chinese line.
- Quoting our own translation in a manuscript requires `笔者据原文译` and a check against the original unit.
- A published Chinese translation is a separate source with its own KEY.
- The Citation Gate still hashes the source PDF; translation does not change it.

## Fallback (no gateway credentials, or the host is Codex)

A subagent follows `Templates/Translate/system.md` and the glossary, translates the selected units, and writes the same `translation.jsonl` records (`unit_id`, `unit_sha256`, `zh`, `model`, `glossary`, `glossary_sha256`, `translated`, `qa`). Then run `translate.py check` and report the flags. Do not write partial records that lack the source hash.

## Output

Chinese report: source and selection; units translated / cached / verbatim; model and glossary used; QA flags by unit; refresh state of `reader.html`; any stale units (`unit_sha256` no longer current). Filenames, KEYs, stems, and statuses remain in English.
