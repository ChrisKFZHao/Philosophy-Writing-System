# Editor passes

You edit one section in three passes, in this order. Each pass uses only its own checklist. In every pass you must not add, drop, strengthen, or weaken a claim; check each change against the argument sheet. Keep a pattern where the argument needs it, and never trade precision for smoothness.

## Pass 1: structure

- Each paragraph does one job from the sheet, and its first sentence starts doing it. Cut announcements such as 先看……、现在回到……、下面说明…….
- The paragraphs follow the sheet's order of argument.
- The section picks up the previous section's last point in substance. Cut recap and roadmap formulas (上一节说明……、本节先……再……、下一节将……) unless the section has four or more moves; the paper's roadmap belongs in the introduction. Keep a hand-off only when the next section answers a question raised here.
- Nothing is said twice. When two paragraphs make the same point, keep the clearer one.
- Paragraphs run about 200–500 characters. Split a paragraph that does two jobs.

## Pass 2: sentences

The lint report points to candidates. The examples come from 余光中《怎样改进英式中文》 and 思果《翻译研究》.

| Pattern | Fix | Example |
|---|---|---|
| Sentence over about 60 characters | Split at a logical joint, and carry the relation into the new sentence with 所以、但、因为 or the like. Never split one inference into two bare assertions | |
| Three or more sentences in a row with no logical link (lint `bare-run`) | Write in the relations the sheet implies: cause, concession, example, consequence. Merge a premise with its conclusion where they form one step | 合理多元是说……。整全性学说是……。这些学说彼此冲突。→ 合理多元是说……；这里的整全性学说指……，它们彼此冲突，却各自连贯 |
| Several disclaimers in one paragraph (lint `disclaimer`) | Never string them into one sentence: a row of negations reads as a list of excuses. Put each next to the claim it protects, state the positive claim first, and report disclaimers that block no likely misreading to the author as sheet candidates for cutting | |
| Three or more 的 in one clause | Turn a modifier into a clause or a verb | 弯弯的杨柳的稀疏的倩影 → 弯弯的杨柳投下稀疏的倩影 |
| 进行、作出、加以 + noun | Use the real verb | 心理学家在老鼠的身上进行试验 → 心理学家用老鼠来做试验 |
| 由于……使得 | Drop the preposition and let the subject act | 由于他的家境贫穷，使得他只好休学 → 他家境贫穷，只好休学 |
| Long pre-modifier | Move it after the noun as a clause | 我见到一个长得像你兄弟说话也有点像他的陌生男人 → 我见到一个陌生男人，长得像你兄弟，说话也有点像他 |
| 作为……之一 | Make it a plain statement | 作为竹林七贤之一的刘伶以嗜酒闻名 → 刘伶是竹林七贤之一，以嗜酒闻名 |
| 不是 A，不是 B，而是 C | State C first; keep at most one contrast | |
| Insertion between dashes, long parenthesis | Give it its own sentence, or a footnote | |
| Several hedges in one sentence | One qualification, at the point of assertion | |
| Stock phrases such as 值得注意的是、这意味着 | Delete, or replace with the actual point | |
| Abstract noun as subject | Restore the actor | |

Vary sentence length. A run of uniformly long sentences is a defect even when each sentence is grammatical, and so is a run of short sentences that reads like a list. Do not shorten sentences that a first reader follows without trouble: the lint flags are candidates, not targets.

## Pass 3: terms and citations

- The same concept uses the same word throughout the section.
- Each term is defined before or at its first use, and English is glossed once.
- When the project has `Private/Projects/{topic}/glossary.md`, its renderings are fixed for the terms this section uses. Run `prose-lint.py <file> --glossary Private/Projects/{topic}/glossary.md`; a deviation needs a stated reason in the change log, for example the author defines the term differently. Propose new recurring terms to the user for the glossary instead of adding them silently.
- Citations read `（作者，年份）` and match the sheet. No KEY placeholder and no new source remains.
- Every sheet line is still present, at its original strength.

## Output

1. The revised section as plain text.
2. A change log for each pass, one line per change: location → change → reason.
3. The net change in Chinese characters.
4. Lint flags you deliberately kept, each with a reason.

In `user-led` mode, return a numbered list of suggested edits instead of a revised section: location, current text, suggested text, reason.
