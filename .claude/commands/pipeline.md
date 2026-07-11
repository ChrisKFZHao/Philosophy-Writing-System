---
description: 一键全流程 — 调用 phil-orchestrator agent，5 阶段：哲学问题 → 文献综述 → 大纲 → 初稿 → 终稿，每阶段质量门控
---

# /phil:pipeline

## Usage

```
/phil:pipeline <research question or topic>
```

## 定位

一键全流程哲学论文生产。调用 `phil-orchestrator` agent。

## 编排

| 组件 | 说明 |
|------|------|
| Agent | `phil-orchestrator` |

## 5 阶段流程

| 阶段 | 内容 | 质量门 |
|------|------|--------|
| 1 | 哲学问题澄清 + 立场明确 | 论题清晰度检查 |
| 2 | 文献综述 + 分析 | 引用完整性检查 |
| 3 | 结构化大纲 | 论证逻辑检查 |
| 4 | 逐节撰写初稿 | 7 哲学散文标准检查 |
| 5 | 审稿 + 修订 → 终稿 | 8 维度审稿 |

每个阶段通过质量门后才能进入下一阶段。未通过时循环修订直到通过或用户手动跳过。

## Notes

- 各阶段内部自动调用 `/phil:reconstruct`、`/phil:evaluate`、`/phil:review`、`/phil:write`
- 可选择性调用 ARS 功能（deep-research、citation-check、format-convert）
