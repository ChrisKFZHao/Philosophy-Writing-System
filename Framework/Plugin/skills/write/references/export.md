# Export: handouts and slides

Export turns a finished argument into a talk handout, a slide deck, or a Word file. The model writes only a content file in Markdown. `Scripts/render-output.py` produces every format from it, applies the templates in `Shared/Format/`, and checks the result. The model never writes layout code.

## Sources

Use what already exists, in this order: the argument sheets in `{topic}-sheets/`, the manuscript, the conception, `refs.md`. Add no claim, example, objection, or source that these do not contain. Keep every claim at the strength the manuscript gives it. If the material has a gap, write `【待补：…】` and report it.

## Files

Content files live in `Private/Projects/{topic}/export/`: `{topic}-handout.md` and `{topic}-slides.md`. Rendered files go next to them, with a `.check.json` report for each. Content files are living files and are never versioned.

## Content file format

Pandoc Markdown with a YAML header:

```
---
kind: handout            # handout | slides
title: …
subtitle: …              # optional
author: …
event: …                 # optional: venue or seminar
date: 2026-11-22
minutes: 20              # slides only: talk length
---
```

- **Continuous numbering.** Number theses, premises, examples, and definitions with Pandoc example lists, `(@label)`, so numbers run on across sections. Refer back with `(@label)`.
- **Citations.** Write `[@KEY]` or `[@KEY, 137]`. The script replaces them with （作者 年份, 137） from `Private/Bibliography/INDEX.md`, refuses a KEY missing from `refs.md`, and appends 参考文献 to a handout.
- **Quotations.** Write a quotation as a block quote ending in a citation. Quote only text that appears word for word in the manuscript or in an evidence unit from `pdf-extract.py`. The script checks each quotation against those sources and reports any it cannot find. Never write a quotation from memory (Rule 2).
- **Thesis.** Put the one-sentence thesis in a `::: thesis` block; the templates set it off in a box.
- **Slides.** Each `#` heading starts one slide. Speaker notes go in a `::: notes` block after the slide's content, preceded by a blank line.

## Handout rules

A handout is what the audience reads while you speak, and what they keep afterwards.

1. Open with the thesis in one sentence, then the main argument as at most five numbered premises and a conclusion. If the argument does not fit in five premises, the manuscript's argument is not yet clear; report that instead of padding.
2. Fit on one A4 sheet, both sides: at most two pages.
3. Give each section a short heading. Under it, write numbered items, not paragraphs. Each item is one complete sentence, written in the manuscript's terms.
4. Say what each thing is. Add a contrast (“……而非……”) only where the manuscript makes it a point, at most one per item; never stack “不是……也不是……”. A handout full of disclaimers reads as defensive.
5. Define each technical term once, as a numbered definition, at the point where it is first needed.
6. List the main objections with their numbered replies, each reply in one or two sentences. Optionally leave one objection unanswered for the discussion and mark it 留待讨论.
7. Put quotations here, not on slides. Keep each under about 80 characters, and quote at most three or four passages.
8. Do not repeat the slides. Do not repeat yourself either: if the thesis says the conditions are necessary but not sufficient, no later item needs to say it again. The handout carries the argument and the quotations; the slides carry the route through them.

## Slide rules

Slides guide listeners through the talk; they are not the speaker's script.

1. Plan about one slide per one to one and a half minutes. For a 20-minute talk, write 12–18 slides including the title slide.
2. Write keywords and short phrases, not full sentences. The exceptions are a definition, a thesis, and a numbered premise, which keep their full wording. Items say what something is or does; a slide carries at most one “不是……” item.
3. Put at most five items on a slide. Make each readable in two seconds: at most about 20 Chinese characters.
4. Number premises as on the handout, so the speaker can say "前提 3" and the audience can find it.
5. Give each slide a plain heading that names its point in the argument. Skip agenda slides; one roadmap slide after the title is enough.
6. Put no quotation longer than one line on a slide; point to the handout's number instead.
7. Write speaker notes for every content slide: two to five full sentences saying what to argue there. The notes may use the manuscript's wording.
8. Do not write a title slide; the YAML header makes it. Keep `title` short enough for one line and put the rest in `subtitle`.
9. End with a slide that restates the thesis and the main argument's numbers, then a discussion slide listing two or three questions the talk leaves open.

## Procedure

1. **Check the source.** Confirm which manuscript version to use and the talk length. In `user-led` mode, export never changes the manuscript.
2. **Write the content files.** Use a fresh subagent if available. Give it only this file, the sources listed above, and the length. The handout and the slides may be written by one agent, because they must not overlap.
3. **Render and check.** Run `py -3 Framework/Workflow/Scripts/render-output.py <content file> --to pdf` for a handout. For slides, run it twice, with `--to pptx` and `--to pdf`. Each run writes a `.check.json`.
4. **Revise.** Send only the items the check flags, and any style problems, back to the writer. Allow at most two rounds.
5. **Cold read.** Give a fresh reader only the handout and ask for the thesis and the main argument. If the reader cannot reconstruct them, the handout is not done. This is the same test as `cold-read.md`, questions 1–2.
6. **Present.** Show the user the rendered files, the check report, and the cold reader's reconstruction. The user edits the content files; re-render after each edit.
