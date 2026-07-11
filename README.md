# Philo — 分析哲学写作工作流

基于 Claude Code 的分析哲学研究与写作系统。提供从 PDF 阅读、论证重构、概念分析到论文写作、审稿、修订的完整工具链。

**版本**: 0.1-alpha  
**语言**: Chinese（写作输出）/ English（技能定义与架构文档）  
**构建于**: `academic-research-skills` v3.15.0

---

## 快速开始

### 1. 放入参考文献

将 PDF 放入 `bibliography/pdf/`，然后运行：

```
/phil-reconstruct
```

系统会提取文本、重构论证，生成分析文件到 `bibliography/analysis/`。分析分三级递进：

| Level | 内容 | 触发条件 |
|-------|------|----------|
| 1 | 论证重构 | PDF 添加时 |
| 2 | + 隐含前提、慈善审查、概念分析、区分追踪 | 首次在手稿中引用 |
| 3 | + 辩证映射、本体论承诺、模态分析 | 成为核心论敌或关键依赖 |

### 2. 明确立场

通过对话（或 `/phil-pipeline` Stage 1）明确你的核心主张和论证方向。Rule 1（条件 Socratic 追问）保障效率——想法清晰时直接推进，模糊时才追问。

### 3. 写论文

```
/phil-write outline     # 大纲
/phil-write draft       # 初稿
/phil-review            # 8 维度评审
/phil-write revision    # 修订
```

或一键全流程：`/phil-pipeline`

---

## 项目结构

```
Demo/
├── README.md                         # 本文件
├── ARCHITECTURE.md                   # 系统架构文档 0.1-alpha
├── bibliography/                     # 参考文献
│   ├── pdf/                          #   原始 PDF
│   ├── analysis/                     #   分析文件（每篇一个 .analysis.txt）
│   └── INDEX.md                      #   文献索引（含分析级别）
├── manuscript/                       # 手稿
│   ├── {topic}-draft.txt             #   工作草稿（自由覆写）
│   ├── {topic}-v{N}.txt              #   切分版本（触发式）
│   ├── {topic}-review.txt            #   审稿报告
│   └── VERSIONS.md                   #   版本历史
├── paper/                            # 最终论文（LaTeX .txt）
└── .claude/                          # Claude Code 配置
    ├── CLAUDE.md                     #   项目指引 + 行为规则
    ├── skills/                       #   28 个哲学分析技能
    ├── agents/                       #   9 个领域特化 agent
    ├── commands/                     #   33 个用户命令
    ├── references/                   #   知识库（术语表、论证形式、哲学家数据库）
    └── shared/                       #   数据契约（JSON Schema + 模板）
```

---

## 可用命令

### 分析链

| 命令 | 功能 |
|------|------|
| `/phil-reconstruct` | 论证重构 |
| `/phil-charity` | 慈善原则审查 |
| `/phil-premises` | 隐含前提检测 |
| `/phil-counterexample` | 反例生成 |
| `/phil-concepts` | 概念分析 |
| `/phil-dialectic` | 辩证映射 |
| `/phil-thought` | 思想实验分析 |
| `/phil-distinctions` | 区分追踪 |
| `/phil-modal` | 模态论证分析 |
| `/phil-analogy` | 类比论证评估 |
| `/phil-parity` | 推理一致性检查 |
| `/phil-intuition` | 直觉泵检测 |
| `/phil-methodology` | 方法论反思 |
| `/phil-context` | 思想史脉络化 |
| `/phil-analyze` | 全流程分析（编排以上所有） |

### 形而上学

| `/phil-ontology` | `/phil-identity` | `/phil-grounding` |
| `/phil-conceivability` | `/phil-causation` | `/phil-essence` |
| `/phil-natural-kind` |

### 元伦理学

| `/phil-moral-realism` | `/phil-normativity` | `/phil-moral-semantics` |
| `/phil-moral-psychology` | `/phil-moral-disagreement` | `/phil-moral-epistemology` |
| `/phil-moral-supervenience` |

### 写作与生产

| 命令 | 功能 |
|------|------|
| `/phil-write` | 哲学写作（outline / draft / revision） |
| `/phil-review` | 哲学审稿（8 维度 + 立场模拟） |
| `/phil-comment` | 哲学评论（批判 / 回应 / 辩证定位） |
| `/phil-pipeline` | 5 阶段全流程编排 |

---

## 行为规则

系统内置三条硬性约束（详见 `CLAUDE.md`）：

1. **不谄媚——条件 Socratic 追问**：想法清晰 → 直接执行；想法模糊 → 追问澄清。不以"制造反对"冒充"严谨"。
2. **不虚构引用**：未经核实的参考文献、引文、页码一律标注 `[source unverified]` 或 `[citation needed]`。Citation Gate：分析级别不足 → 阻断引用。
3. **触发式版本管理**：不自动切版本。仅在三类事件触发时切分——(a) 审稿/评论后修订，(b) 新洞见或新论证，(c) 压缩或扩展。

---

## Alpha 版本说明

当前为 **Alpha** 版本，所有模块均已完成基础实现但未经充分实战验证：

| 模块 | 状态 | 说明 |
|------|------|------|
| 分析技能（28 个） | Alpha | 全部完成，已内部测试 |
| 命令（33 个） | Alpha | 全部完成 |
| 知识库（~50 个参考文件） | Alpha | 术语表、论证形式、哲学家数据库均已填充 |
| 对话 agent（5 个） | Alpha | 已完成，待更多交互验证 |
| 写作生产（4 个 agent + 4 个命令） | Alpha | 已完成，仅 Srinivasan 一篇测试 |
| 行为规则（3 条） | Alpha | 已部署，待长期使用校准 |
| 文献管理 | Alpha | Citation Gate 框架就位，1 篇分析文件 |

**已知限制**：
- 分析文件基于阅读笔记重建（Srinivasan），PDF 原文对照验证待完成
- 写作流水线仅完成一次完整测试（srinivasan-critique）
- 哲学家数据库覆盖不均衡（分析传统为主，大陆哲学较弱）
- 无自动化测试套件

---

## 依赖

- **Claude Code** (claude.ai/code)
- **academic-research-skills** v3.15.0（ARS 插件——可选，提供文献检索、格式转换、引用验证等学术基础设施）
- **pdftotext**（PDF 文本提取）

---

*最后更新: 2026-07-11*
