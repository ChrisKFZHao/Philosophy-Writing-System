# Argument sheet

One sheet per section. It records what the section claims and why, in short Chinese lines, without prose. The composer turns it into prose; the cold-read comparison checks the prose against it. Every substantive line is a claim, a reason, an objection, a limit, a term, a citation, or a transition.

## Format

```
# §<n> <标题>
功能：<本节在全文中的作用，一句>
承接：<上一节留下的问题，一句>
主张：
  C1 <主张，按作者实际持有的强度>
  C2 …
理由：
  C1 ← R1 <理由>；R2 <理由>
  C2 ← …
反对与回应：
  O1 <反对意见的最强版本> → <回应>
界限：<本节不主张什么>
术语：<本节首次使用的术语> = <含义>
引用：<KEY> → <作者，年份> → 支撑 <C1/R2…>
转出：<交给下一节的问题，一句>
```

## Rules

- Write each claim at the strength the author holds it. Keep words such as 必要、充分、至少、可能 explicit, and never strengthen or weaken them in later steps.
- Mark an assumption as `假设：`.
- List every distinction the section draws, with both sides named.
- Every citation line must name a KEY registered in the project's `refs.md`, with the author and year taken from `Private/Bibliography/INDEX.md`.
- Every 界限 line, and every claim that says what something is not, names the misreading it blocks: `界限：本节不主张 X（防：读者以为 Y）`. At the gate, list these lines for the user and propose cutting the ones that block no likely misreading. Each surviving line becomes prose, so unneeded disclaimers make the section sound defensive.
- 承接 and 转出 record content: the open question and the question handed on. They are not instructions to write a recap or a 下一节将 sentence.
- Prefix any line the assistant added with `[AI 补全]`, and say why the author's version needed it.
- Order the lines in the order the argument should run. The composer may merge lines into one paragraph but may not reorder the argument.

## Example

```
# §2 知识与辩护
功能：说明辩护为什么不足以把真信念变成知识
承接：§1 留下的问题是“辩护加真”是否足以构成知识
主张：
  C1 存在得到辩护的真信念却不是知识的情形
  C2 因此，辩护加真不是知识的充分条件（仍可能是必要条件）
理由：
  C1 ← R1 一个人依据可靠证据推出某个信念，信念碰巧为真，但使它为真的事实与证据无关
  C2 ← R2 C1 中的情形满足“辩护加真”，却缺少知识
反对与回应：
  O1 R1 的证据其实不构成辩护 → 证据满足通常的辩护标准，否认这一点会让大多数日常辩护也不成立
界限：本节不讨论辩护是否为知识的必要条件
术语：辩护 = 持有信念的充分理由
转出：如果辩护加真不够，还缺什么
```
