# Philo — 分析哲学写作工作流

基于 Claude Code 的分析哲学研究与写作系统。提供从文献管理、PDF 阅读、论证重构、概念分析到论文写作、审稿、修订的完整工具链。

**版本**: 0.4.2-alpha  
**语言**: Chinese（写作输出）/ English（技能定义与架构文档）  
**构建于**: `academic-research-skills` v3.15.0

---

## 快速开始

### 1. 放入参考文献

将 PDF 放入 `Private/Bibliography/PDF/`，然后运行：

```
phil:ingest
```

系统会扫描文献库，对新 PDF 完成"刮削"：提取元数据、重命名为规范文件名（`{Author}_{Year}_{Title}.pdf`，下划线分段）、登记 INDEX、生成 Level 0.5 摘要，并向主题匹配的写作项目推荐。需要深入分析时再运行 `phil:reconstruct`（论证重构 → `Private/Bibliography/Analysis/`）。分析分级递进：

| Level | 内容 | 触发条件 |
|-------|------|----------|
| 0.5 | 轻量摘要（论题+路线+概念+论敌+topics） | PDF 入库时（phil:ingest） |
| 1 | 论证重构 | 选定为论文依赖时 |
| 2 | + 隐含前提、慈善审查、概念分析、区分追踪 | 首次在手稿中引用 |
| 3 | + 辩证映射、本体论承诺、模态分析 | 成为核心论敌或关键依赖 |

### 2. 明确立场

通过对话（或 `phil:pipeline` Stage 1）明确你的核心主张和论证方向。Rule 1（条件 Socratic 追问）保障效率——想法清晰时直接推进，模糊时才追问。

### 3. 写论文

```
phil:write outline     # 大纲
phil:write draft       # 初稿
phil:review            # 8 维度评审
phil:write revision    # 修订
```

或一键全流程：`phil:pipeline`

---

## Zotero 集成（v0.4.2 新增）

`Private/Bibliography/PDF/` 同时是 Zotero 的 Linked Attachment Base Directory——一份物理 PDF 仓库，Zotero 与本框架各自以自己的方式引用同一批文件：Zotero 通过 linked 附件阅读/标注，框架通过 INDEX 的规范词干读取。核心约定：

- **命名权归框架**：新 PDF 先 `phil:ingest` 改规范词干，再在 Zotero "Attach Link to File" 链接；链接后文件名冻结，Zotero 不得再改名
- **INDEX.md 的 `Zotero` 列**：`KEY ↔ Zotero item key ↔ 文件词干` 三方映射
- **懒迁移**：Zotero 分类只在升格为写作项目时才把其存量条目迁入统一仓库，不做批量搬迁
- **混合读写**：MCP 读走本地 Zotero 数据库，写走 Web API（key 配置于 `~/.claude.json`），云端写入需桌面端同步一次落地

完整迁移方法（含注释保全的 API 步骤、已知坑）见 [`Framework/Lessons/zotero-integration.md`](Framework/Lessons/zotero-integration.md)。

---

## 项目结构

**双仓库结构（v0.4）：隐私边界 = 仓库边界。** 本仓库只含可分享的框架；论文与文献在 `Private/`（gitignore，独立私有仓库）。

```
Philosophical Writing/
├── README.md                         # 本文件（外层仓库）
├── .claude/                          # Framework 可执行层（外层仓库）
│   ├── settings.json                 #   权限 + hooks（提交 git）
│   ├── commands/                     #   8 个综合命令（phil:* 命名空间）
│   ├── rules/                        #   3 个行为规则模块
│   ├── skills/                       #   30 个哲学分析技能
│   ├── agents/                       #   7 个领域特化 agent
│   ├── references/                   #   方法论知识（术语表、论证形式、分类学）
│   └── shared/                       #   数据契约（13 JSON Schema + 模板）
├── Framework/                        # Framework 非执行层（外层仓库）
│   ├── ARCHITECTURE.md               #   系统架构文档
│   ├── changelog.md                  #   框架版本历史
│   └── Lessons/                      #   论文反馈蒸馏（如 zotero-integration.md）
├── Shared/                           # 可分享策展知识（外层仓库）
│   ├── Philosophers-DB/              #   49 位哲学家档案（General/Metaphysics/Metaethics）
│   └── Format/                       #   格式模板（LaTeX/Word，可分享）
└── Private/                          # 私有内容层（gitignore；独立内层仓库）
    ├── Projects/{topic}/             #   每个写作项目一个目录：手稿 + refs.md +
    │                                 #   VERSIONS.md + feedback-to-framework.md
    ├── Bibliography/                 #   文献总库（PDF/ 不进 git、Analysis/、INDEX.md）
    ├── Concepts/                     #   跨项目概念笔记
    └── Style/                        #   个人写作样文（文风校准）
```

**命名规范**：`.claude/` 之外的目录全部大写开头（连字符逐段大写，缩写全大写，如 `Philosophers-DB`）；写作项目条目目录用小写 kebab-case（如 `srinivasan-critique/`，与文件名前缀一致）；文件名小写 kebab-case（惯例大写文件除外：`CLAUDE.md`、`INDEX.md`、`VERSIONS.md` 等）。文献库文件用规范词干 `{Author}_{Year}_{Title}`（下划线分段、段内连字符，完整标题，如 `Austin_1956_A-Plea-for-Excuses.pdf`），`.pdf`/`.analysis.txt`/`.summary.txt` 三类同词干；引用 KEY 保持 `AUTHOR-TITLE` 不带年份。

**语言规范**：定义层（rules/commands/agents/skills/schemas/CLAUDE.md/ARCHITECTURE/changelog）为英文；写作输出（手稿、分析报告、评审报告）为中文；两个 README 与 `.claude/shared/templates/` 的 5 个报告模板为刻意保留的中文（面向使用者的文档 / 输出物骨架）。

---

## 可用命令

| 命令 | 功能 | 编排 |
|------|------|------|
| `phil:reconstruct` | 全维度理解文献 | 9-20 技能（混合串并行，自动领域检测） |
| `phil:evaluate` | 多角度同时批判 | 7 技能（全并行） |
| `phil:review` | 同行审稿 | phil-reviewer agent（8 维度 + 立场模拟） |
| `phil:write` | 哲学写作 | phil-writer agent（outline / draft / revision） |
| `phil:comment` | 论证细节和概念澄清 | phil-commentator agent（6 批判维度） |
| `phil:pipeline` | 一键全流程 | phil-orchestrator agent（5 阶段 + 质量门） |
| `phil:tutor` | 导师式文献对话 | phil-tutor agent（Socratic 追问 + 引文推荐 + 阅读规划） |
| `phil:ingest` | 文献入库刮削 | shell 扫描 + pdf skill + phil-summarize（重命名、登记 INDEX、0.5 级摘要、入库推荐） |

每个命令在 `.claude/commands/` 中定义了完整的技能编排、执行顺序和输出格式。底层 30 个分析技能可通过 Skill tool 单独调用。

---

## 行为规则

系统内置三条硬性约束（详见 `.claude/rules/`）：

1. **不谄媚——条件 Socratic 追问**：想法清晰 → 直接执行；想法模糊 → 追问澄清。不以"制造反对"冒充"严谨"。
2. **不虚构引用**：未经核实的参考文献、引文、页码一律标注 `[source unverified]` 或 `[citation needed]`。Citation Gate：分析级别不足 → 阻断引用。
3. **触发式版本管理**：不自动切版本。仅在三类事件触发时切分——(a) 审稿/评论后修订，(b) 新洞见或新论证，(c) 压缩或扩展。

---

## Alpha 版本说明

当前为 **Alpha** 版本，所有模块均已完成基础实现但未经充分实战验证：

| 模块 | 状态 | 说明 |
|------|------|------|
| 分析技能（30 个） | Alpha | 全部完成，已内部测试 |
| 命令（8 个） | Alpha | 全部完成 |
| 知识库（87 个参考文件） | Alpha | 术语表、论证形式、哲学家数据库均已填充 |
| 对话 agent（3 个） | Alpha | 已完成，待更多交互验证 |
| 写作生产（4 个 agent + 7 个命令） | Alpha | 已完成，仅 Srinivasan 一篇测试 |
| 行为规则（3 条） | Alpha | 已部署，待长期使用校准 |
| 文献管理 | Alpha | Citation Gate 框架就位，10 个 KEY 入库（1 篇 Level 3，9 篇 Level 0.5） |
| Zotero 集成 | Alpha | 试点完成（instantaneous-velocity，6 条迁移+注释保全验证），56 条存量待懒迁移 |

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

*最后更新: 2026-07-14（v0.4.2 Zotero 集成：统一 PDF 仓库 + INDEX Zotero 列 + 注释保全迁移）*
