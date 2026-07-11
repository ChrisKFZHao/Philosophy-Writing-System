---
description: 哲学写作 — 调用 phil-writer agent，三种模式：outline（结构化大纲）、draft（逐节撰写）、revision（基于审稿修订）
---

# /phil:write

## Usage

```
/phil:write <mode: outline|draft|revision> [context]
```

## 定位

哲学论文写作。调用 `phil-writer` agent。

## 编排

| 组件 | 说明 |
|------|------|
| Agent | `phil-writer` |
| 模式 | outline（结构化大纲） / draft（逐节撰写） / revision（基于审稿修订） |

### Outline 模式
- 输入：论题或研究问题 + 分析上下文
- 输出：结构化大纲（论题、章节规划、区分清单、预期反驳）

### Draft 模式
- 输入：已批准的大纲 + 分析输出
- 输出：完整手稿章节，论证优先的散文，中文学术规范

### Revision 模式
- 输入：手稿 + 审稿人反馈
- 输出：修订稿 + 修改日志，按类型优先级排序（结构 → 概念 → 辩证 → 模态 → 风格）

## 7 个哲学散文标准

1. 论证透明度
2. 概念精确性
3. 模态准确性
4. 辩证定位
5. 区分保存
6. 反例抵御
7. 本体论明晰性

## Notes

- 写作输出使用中文
- 建议先运行分析技能（`/phil:reconstruct` + `/phil:evaluate`）再写作
- 可选择性调用 ARS 功能（citation-check、format-convert、disclosure）做最后打磨
