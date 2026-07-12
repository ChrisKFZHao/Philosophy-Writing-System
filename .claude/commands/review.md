---
description: 哲学论文同行评审 — 调用 phil-reviewer agent，8 维度审稿 + 立场模拟（Quinean/Lewisian/Kripkean 等视角）
---

# /phil:review

## Usage

```
/phil:review <manuscript>
```

## 定位

审稿**自己的写作**。调用 `phil-reviewer` agent，提供仿真的同行评审体验。

## 编排

| 组件 | 说明 |
|------|------|
| Agent | `phil-reviewer` |
| 审稿维度 | 8 个：论证完整性、概念精确性、辩证意识、模态准确性、区分保存、反例抵御、本体论清晰性、方法论适当性 |
| 立场模拟 | 可选：以特定哲学家视角审稿（Quinean / Lewisian / Kripkean / Williamsonian / Parfitian） |

## 输出格式

标准审稿报告，包含：
1. 总体评价
2. 按维度逐项评分与评论
3. 主要问题（按严重性排序）
4. 次要问题
5. 修改建议（按优先级排列）

## Notes

- 与 `/phil:evaluate` 的区别：review 针对自己的手稿，提供建设性修改建议；evaluate 针对他人文献，提供批判性分析
- 与 `/phil:comment` 的区别：review 是整体论文审稿，comment 聚焦论证细节和概念澄清
- 所有输出使用中文（项目约定）
- 输出格式遵循 `shared/templates/` 中的审稿报告模板
