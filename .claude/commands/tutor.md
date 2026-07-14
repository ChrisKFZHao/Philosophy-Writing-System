---
description: 导师式文献对话 — 询问你的思路、追问理解、发现盲点、推荐阅读文献并规划下一步
---

# /phil:tutor

## Usage

```
/phil:tutor
```

直接触发即可。Agent 会自动问候并开始对话。

如果已有具体问题或文献要讨论，可以直接说：

```
/phil:tutor 我在读 Srinivasan 的 "Anger"，但不太确定她 argument 中的 implicit premise 是什么
```

## 定位

阅读文献时的**导师对话**工具。phil:tutor 不是一个分析引擎（那是 phil:reconstruct 的工作），而是一个对话伙伴——帮助你理清思路、发现盲点、决定下一步读什么。

与 phil:reconstruct 的关系：
- **reconstruct** 做机械分析 → 把文本拆成论证结构
- **tutor** 做对话引导 → 帮你理解这个结构意味着什么
- 建议：先读文本 → 再用 tutor 讨论 → 再用 reconstruct 深入分析

## 使用的 Agent

本命令启动 `phil-tutor` agent（定义于 `.claude/agents/phil-tutor.md`）。

该 agent 在需要时可内部调用以下技能：
- `phil-citation-extract` — 提取当前文献的引文用于推荐

## 对话流程

Agent 会按以下四个阶段引导对话：

| 阶段 | Agent 做什么 | 你做什么 |
|------|-------------|---------|
| 1: 摸底 | 问你在读什么、处于什么阶段 | 描述你的当前阅读或问题 |
| 2: 追问 | Socratic 提问，检查理解深度 | 回答、反思、暴露盲点 |
| 3: 推荐 | 基于对话推荐文献 | 评估推荐是否合适 |
| 4: 规划 | 给出阅读计划和工具建议 | 确认或调整计划 |

你也可以随时跳过某个阶段，直接问具体问题。

## Notes

- Agent 使用中文对话（项目约定），引文元数据保留英文
- 遵守引用完整性规则（Rule 2）：不虚构书目信息
- 如果已运行 phil:reconstruct，可以告诉 agent，它会在追问中参考分析结果
- Agent 的知识来源：philosophers-db/（49 位哲学家）、argument-forms/（26 种论证形式）、Private/bibliography/INDEX.md（项目书目）
