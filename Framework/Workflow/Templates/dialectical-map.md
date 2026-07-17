# Dialectical Map Template

Template for `phil-dialectical-map` output reports.

---

```
===============================================================================
辩证映射报告
===============================================================================

日期：{YYYY-MM-DD}
分析对象：{Debate / Text / Set of arguments}
映射者：phil-dialectical-map skill v{version}
===============================================================================


0. 辩论概述
-------------------------------------------------------------------------------

{1-2 paragraphs: What is the debate about? What is the central question?
Who are the main participants? What is at stake?}


1. 辩证树
-------------------------------------------------------------------------------

### 可视化

{ASCII tree diagram showing the full dialectical structure:

                    [T1] Central Thesis
                       │
          ┌────────────┼────────────┐
          │            │            │
     [O1] Obj. 1   [O2] Obj. 2  [O3] Obj. 3
     (Undermining) (Rebutting)  (Outflanking)
          │            │            │
     [R1] Resp.   [R2] Resp.   [R3] Resp.
     (Strong)     (Adequate)   (Weak)
          │            │            │
          └────────────┼────────────┘
                       │
                  [T1'] Modified Thesis
                       │
                  [O4] Further Obj.
                       │
                  [R4] Resp.
                  (Bedrock)

Legend:
  [T] = Thesis    [O] = Objection    [R] = Response
  Strong = fully answered    Adequate = blunted    Weak = survives
  Bedrock = fundamental disagreement, no further argument available
}


2. 节点清单
-------------------------------------------------------------------------------

### 论点节点 (Thesis Nodes)

| ID | 内容 | 状态 | 来源 |
|----|------|------|------|
| T1 | {Thesis statement} | {established / contested_defensible / vulnerable / refuted} | {Philosopher / Text} |
| T2 | ... | ... | ... |

### 反对节点 (Objection Nodes)

| ID | 目标 | 类型 | 内容 | 严重性 | 来源 |
|----|------|------|------|--------|------|
| O1 | T1 | undermining | {Objection statement} | {fatal / severe / moderate / minor} | {Philosopher} |
| O2 | T1 | rebutting | ... | ... | ... |

### 回应节点 (Response Nodes)

| ID | 目标 | 内容 | 力度 | 状态变化 |
|----|------|------|------|----------|
| R1 | O1 | {Response statement} | {strong / adequate / weak / unavailable} | T1: vulnerable → contested_defensible |
| R2 | O2 | ... | ... | ... |


3. 辩证状态总览
-------------------------------------------------------------------------------

| 主张 | 初始状态 | 经辩证后 | 变化 |
|------|----------|----------|------|
| {Claim 1} | {State} | {State} | {What changed and why} |
| ... | ... | ... | ... |


4. 基岩分歧
-------------------------------------------------------------------------------

{List of bedrock disagreements — points where the dialectic cannot proceed
further because parties disagree on fundamental premises, methods, or standards.}

1. {Path}: {Nature of the disagreement}
   - 立场A: {What position A holds at bedrock}
   - 立场B: {What position B holds at bedrock}
   - 为何是基岩: {Why further argument is impossible — what would need to change for resolution}


5. 辩证动态分析
-------------------------------------------------------------------------------

{2-3 paragraphs analyzing the dialectical dynamics:
- What patterns emerge? (e.g., objections cluster around a particular type of premise)
- Where is the debate most active?
- Where is there surprising consensus?
- What moves shift the burden of proof?
- What would it take to resolve the central disagreement?}


6. 战略评估
-------------------------------------------------------------------------------

### 对辩护者
{What does the defender of the thesis need to do to strengthen their position?
Which objections are most threatening? Where should they focus their efforts?}

### 对批评者
{What is the most promising line of attack? Which premise is most vulnerable?
Is there an outflanking move that the defender has not considered?}

===============================================================================
* 辩证映射完成。状态评估基于当前辩论中的最佳论证。
* "基岩"标记表示在当前框架内无法进一步推进的分歧。
===============================================================================
```
