# Philo — 分析哲学写作工作流

同时支持 Claude Code 与 Codex 的分析哲学研究与写作系统。提供从文献管理、PDF 阅读、论证重构、概念分析到论文写作、审稿、修订的完整工具链。

**版本**: 0.7.0-alpha
**语言**: Chinese（写作输出）/ English（技能定义与架构文档）

---

## 依赖关系

本仓库只是框架层——不含任何论文或文献内容。依赖按"缺失时损失什么"分层：

### 必需

| 依赖 | 角色 |
|------|------|
| **Claude Code 或 Codex** | 运行时宿主；两端消费同一套平台中立工作流 |
| **pdfminer.six** | PDF 文本与元数据提取，由 `Scripts/pdf-extract.py` 调用（`py -3 -m pip install --user pdfminer.six`）。纯 Python，不受 Windows 智能应用控制拦截 |
| **Python 3.11+** | 生成/校验插件清单与市场文件、项目指针，以及运行可移植的文献扫描与 Zotero helper |

### 可选 — 学术基础设施

| 依赖 | 角色 | 缺失时 |
|------|------|--------|
| **academic-research-skills** v3.15.0（ARS 插件） | 文献检索、格式转换、引用验证等 `ars-*` 能力 | 30 个内部分析方法不受影响；仅 ARS 相关能力不可用 |

### 可选 — Zotero 集成

| 依赖 | 角色 | 缺失时 |
|------|------|--------|
| **Zotero desktop** | 阅读与标注端；其 Linked Attachment Base Directory 指向文献 PDF 仓库 | `phil:research ingest` 的 Zotero 注册步骤自动跳过，其余步骤不受影响 |
| **zotero MCP server** | 完整后端：本地读取、云端写入、DOI/ISBN/BibTeX 注册 | Step 8 标记为 `partial` 或 `skipped` |
| **Codex Zotero 插件** | 本地搜索、导出和引用操作；不能替代 linked-file 创建 | Step 8 状态为 `partial` |
| **`zotero-attach-linked.py`** | 位于 `Framework/Workflow/Scripts/`，从用户级运行时配置读取认证 | linked 附件改为手动待办 |

### 用户自备

- **`Private/` 内层 git 仓库**——论文、文献库、个人样文的内容层。被本仓库 gitignore，由使用者自建独立私有仓库。框架所有命令按 `Private/` 的目录契约（见下）读写内容。

依赖流向概览：

```
phil:* 命令（5）──→ 技能（4）+ 内部方法包（5 包 30 方法）+ 服务（5）──→ 数据契约（Schemas 17 + Contracts 2）
      │                    │
      │                    ├──→ pdf-extract.py + pdfminer.six（必需）
      │                    └──→ ars-*（可选，ARS 插件）
      │
      └─ phil:research ingest 注册步骤 ──→ zotero MCP（读本地 / 写云端）
                               └──→ zotero-attach-linked.py（Python 3）──→ Zotero Web API
```

---

## 快速开始

两个宿主都通过 `Framework/Plugin/` 中的 `phil` 插件调用公开入口：Claude Code 使用 `/phil:<name>`，Codex 将 `phil:<name>` 路由到同一插件。`phil:full` 是插件里的一个薄入口技能，执行 `Framework/Workflow/Commands/phil-full.md` 的状态机规格。未加载插件的宿主可直接读取 `Framework/Plugin/skills/<name>/SKILL.md` 并照做。两端唯一事实源位于 `Framework/Workflow/`。

### 安装插件

Claude Code（每台机器一次）：

```
claude plugin marketplace add <repository root>
claude plugin install phil@phil-local
```

插件从仓库原地加载，修改技能后在下次会话或执行 `/reload-plugins` 后生效。

Codex：

```
codex plugin marketplace add <repository root>
```

然后在插件浏览器中安装 `phil`。Codex 从缓存加载已安装的副本，因此修改技能后需要重新安装。此路由遵循官方文档，但尚未在本项目实测。

### 1. 放入参考文献

将 PDF 放入 `Private/Bibliography/PDF/`，然后运行：

```
phil:research ingest
```

系统会扫描文献库，对新 PDF 完成"刮削"：提取元数据、重命名为规范文件名（`{Author}_{Year}_{Title}.pdf`，下划线分段）、登记 INDEX、生成 Level 0.5 摘要，并向主题匹配的写作项目推荐。支持三类文档——**论文**、**专著**（摘要带章节段）、**编者文集**（卷条目 + 每篇成员论文独立登记、独立摘要，共享同一份卷 PDF）。需要深入分析时再运行 `phil:research reconstruct`（论证重构 → `Private/Bibliography/Analysis/`）。分析分级递进：

| Level | 内容 | 触发条件 |
|-------|------|----------|
| 0.5 | 轻量摘要（论题+路线+概念+论敌+topics） | PDF 入库时（phil:research ingest） |
| 1 | 论证重构 | 选定为论文依赖时 |
| 2 | + 隐含前提、慈善审查、概念分析、区分追踪 | 首次在手稿中引用 |
| 3 | + 辩证映射、本体论承诺、模态分析 | 成为核心论敌或关键依赖 |

### 2. 阅读与构思

```
phil:tutor              # reading 模式（默认）：苏格拉底式文献对话
phil:tutor incubating   # incubating 模式：构思孵化
```

阅读阶段用 **reading 模式**与导师对话——检验你对核心文献的理解、暴露盲区、推荐下一步阅读。读透之后进入 **incubating 模式**孵化你自己的论点：讨论文献间关系、切入角度、候选论题，产出 `{topic}-conception.md`（前提级论证骨架；论题必须是你本人的表述，AI 补充的前提一律以 `[AI 补全]` 显式披露）。独立的 `{topic}-idea-ledger.json` 保留弃用观点；v0.6.3 在 Stages 3–6 按七类真实事件查询最多两条候选，再由当前专业角色判断其是否会实质改变论证。阶段边界不会周期扫描，观点状态也不会因再次提及而自动改变。

### 3. 写论文

```
phil:write outline                        # 大纲（优先消费 conception 文件）
phil:write draft [user-led|assistant-led] # 初稿（双协作模式）
phil:review                               # 8 维度评审
phil:write revision                       # 修订
```

初稿支持两种协作模式，在项目级 `PROJECT.md` 用 `collaboration:` 键声明：**`user-led`**（严肃学术论文——用户逐节主笔，AI 只在能指名论证缺陷时发起挑战）/ **`assistant-led`**（课程论文——AI 逐节代笔，每节边界提出 1–3 个归属问题）。旧值 `claude-led`、`codex-led` 在一个小版本内继续接受，但会提示弃用；新披露统一使用 `[AI 补全]`。

或一键全流程：`phil:full start`——状态机管线"先读后立论"管线（主题定向 → 阅读分析 → 构思孵化 → 大纲 → 初稿迭代 → 审稿终稿），每个阶段门都是**宽容性诘问门**：能指名的缺陷才触发挑战，其余补全并披露，你永远可以决定推进。

---

## Zotero 集成

`Private/Bibliography/PDF/` 同时是 Zotero 的 Linked Attachment Base Directory——一份物理 PDF 仓库，Zotero 与本框架各自以自己的方式引用同一批文件：Zotero 通过 linked 附件阅读/标注，框架通过 INDEX 的规范词干读取。核心约定：

运行时先报告 Zotero 后端状态：`full` 可执行完整注册与 linked-file 创建；`partial` 仅允许本地查询、导出和引用操作；`skipped` 完成 ingest 步骤 1–7 后生成手动待办。`--dry-run` 在任何状态下都不写 Zotero。

- **命名权归框架**：新 PDF 先 `phil:research ingest` 改规范词干，再链接进 Zotero；链接后文件名冻结，Zotero 不得再改名
- **自动注册**（v0.4.3+）：`phil:research ingest` 在标识符闸门下自动完成 Zotero 侧登记——论文走 DOI；书籍走级联 **DOI 优先 → ISBN → bibtex**（学术出版社的 ISBN 常在开放书目库查无，而 CrossRef 注册了逐章 DOI）；编者文集的成员论文优先走章级 DOI（返回规范 `bookSection`），卷 PDF 批量链接到卷条目和全部成员条目。任何解析器返回的元数据都须对照 PDF 扉页/目录核对（Rule 2 覆盖入库通道）。无标识符且无元数据来源时回退为手动待办，不强行自动化
- **INDEX.md 的 `Zotero` 列**：`KEY ↔ Zotero item key ↔ 文件词干` 三方映射
- **懒迁移**：Zotero 分类只在升格为写作项目时才把其存量条目迁入统一仓库，不做批量搬迁
- **混合读写**：MCP 读走本地 Zotero 数据库，写走 Web API，云端写入需桌面端同步一次落地

完整方法（含注释保全的 stored→linked 迁移步骤、已知坑）见 [`Framework/Lessons/zotero-integration.md`](Framework/Lessons/zotero-integration.md)。

---

## 项目结构

**双仓库结构（v0.4）：隐私边界 = 仓库边界。** 本仓库只含可分享的框架；论文与文献在 `Private/`（gitignore，独立私有仓库）。

```
Philosophical Writing/
├── README.md                         # 本文件（外层仓库）
├── Framework/Workflow/               # 平台中立唯一事实源
│   ├── manifest.json                 #   v2 注册表：4 技能 + 5 方法包 + 30 方法 + 5 服务 + 1 命令
│   ├── Methods/ Services/ Contracts/ #   内部方法包、权限化服务、跨层数据契约
│   ├── Commands/                     #   phil-full 状态机命令规格
│   ├── Rules/ References/ Schemas/   #   规则、知识与数据契约
│   ├── Templates/                    #   报告与新项目模板
│   └── Scripts/                      #   生成器、doctor、状态工具、扫描器、Zotero helper
├── .claude/                          # 仅含 Claude Code 设置（settings.json）
├── .claude-plugin/marketplace.json   # Claude Code 市场文件（指向 ./Framework/Plugin）
├── .agents/plugins/marketplace.json  # Codex 市场文件（指向 ./Framework/Plugin）
├── Framework/                        # Framework 文档层（外层仓库）
│   ├── Plugin/                       #   phil 插件：两份清单 + skills/
│   ├── ARCHITECTURE.md               #   系统架构文档
│   ├── changelog.md                  #   框架版本历史
│   └── Lessons/                      #   论文反馈蒸馏（如 zotero-integration.md）
├── Shared/                           # 可分享策展知识（外层仓库）
│   ├── Philosophers-DB/              #   规范 JSON 档案 + 动态多领域视图
│   └── Format/                       #   格式模板（LaTeX/Word，可分享）
└── Private/                          # 私有内容层（gitignore；独立内层仓库）
    ├── Projects/{topic}/             #   手稿 + refs.md + conception + idea-ledger +
    │                                 #   workflow-state + VERSIONS.md
    ├── Bibliography/                 #   文献总库（PDF/、Analysis/、Summaries/、Philosopher-Queue/、INDEX.md）
    ├── Concepts/                     #   跨项目概念笔记
    └── Style/                        #   个人写作样文（文风校准）
```

**命名规范**：非隐藏目录大写开头；`.claude/`、`.agents/`、`.claude-plugin/` 等宿主隐藏目录与插件的 `skills/` 目录是命名例外。写作项目条目目录使用小写 kebab-case。新项目以 `PROJECT.md` 为中立配置，并配一个生成的 `AGENTS.md` 指针；旧项目按 `PROJECT.md → AGENTS.md → CLAUDE.md` 回退（`CLAUDE.md` 只作旧项目回退）。

**语言规范**：定义层为英文；写作输出为中文；两个 README 与 `Framework/Workflow/Templates/` 的 5 个报告模板为刻意保留的中文。

---

## 可用命令

| 命令 | 功能 | 编排 |
|------|------|------|
| `phil:research` | 共享证据/溯源内核，六个隔离模式 | `ingest`（文献入库刮削：重命名、登记 INDEX、0.5 级摘要、Zotero 自动注册、入库推荐）/ `reconstruct`（渐进式理解，确定性 Level 1/2/3 规划，仅补缺失覆盖）/ `evaluate`（定向批判）/ `comment`（论证细节）/ `translate`（按证据单元对照翻译，术语表与确定性质检）/ `philosophers`（哲学家数据库维护） |
| `phil:tutor` | 导师式对话 | reading 文献对话 / incubating 构思孵化（产出 conception 文件） |
| `phil:write` | 哲学写作 | outline / draft / revision；draft 含 user-led / assistant-led 双协作模式（质量门槛完全一致） |
| `phil:review` | 同行审稿 | full（8 维度 + 立场模拟）/ targeted / re-review；只读，不直接改稿 |
| `phil:full` | 一键全流程状态机 | start / status / resume；v2 工作流状态、审批门、发现账本、断点续跑 |

v0.7 移除的入口：`phil:reconstruct`→`phil:research reconstruct`、`phil:evaluate`→`phil:research evaluate`、`phil:comment`→`phil:research comment`、`phil:ingest`→`phil:research ingest`、`phil:philosophers`→`phil:research philosophers`、`phil:pipeline`→`phil:full start`。不保留别名或弃用垫片；确定性解析器 `workflow-policy.py removed-entrypoint <命令>`。原 30 个原子技能降级为 `Framework/Workflow/Methods/` 内部方法包，按需经 manifest 解析加载，不再注册为运行时技能。

四个公开技能位于 `Framework/Plugin/skills/`，命令规格在 `Framework/Workflow/Commands/`，方法与服务在 `Framework/Workflow/`（Methods/Services/Contracts）定义。生成器只输出两份插件清单、两个市场文件与 `Private/**/AGENTS.md` 指针；`--check` 还会因遗留适配器路径而失败。修改中立源后运行 `build-adapters.py`，提交生成结果，并以 `build-adapters.py --check` 防止漂移。

**经济性委派**：工作流和角色均不写供应商或具体模型名，也不把任务类别硬绑到模型。当前以会话级提示词政策识别可降档的重复性子任务：首次合格任务出现时只确认一次；其后仅可将独立、只读、无交互且只产生候选工件的任务交给已确认的低成本候选。主任务必须在写入、采纳或进入 Citation Gate 前复核结果；写作、评审、引用验证、资料库或项目修改、用户对话和编排始终保留当前模型。候选不可用或能力不足时不自动换选，且没有宿主提供的成本、缓存、时延和质量数据时不宣称最优。重构与评估先做便宜的确定性预规划，再只加载选中的技能；长示例和检查表仅在真实歧义或显式请求时读取。

---

## 行为规则

系统内置三条硬性约束及一条运行时兼容规则（详见 `Framework/Workflow/Rules/`）：

1. **不谄媚——条件 Socratic 追问**：想法清晰 → 直接执行；想法模糊 → 追问澄清。不以"制造反对"冒充"严谨"。在工作流阶段门与写作分节边界另有第二触发：能指名的论证缺陷 → 挑战；其余缺口 → 补全并以 `[AI 补全]` 显式披露；阶段门永不硬阻断。
2. **不虚构引用**：未经核实的参考文献、引文、页码一律标注 `[source unverified]` 或 `[citation needed]`。Citation Gate：KEY 未登记、分析级别不足、验证状态非 `verified` 或 PDF/分析哈希失配均阻断引用。
3. **触发式版本管理**：不自动切版本。仅在三类事件触发时切分——(a) 审稿/评论后修订，(b) 新洞见或新论证，(c) 压缩或扩展。

---

## Alpha 版本说明

当前为 **Alpha** 版本，所有模块均已完成基础实现但未经充分实战验证：

| 模块 | 状态 | 说明 |
|------|------|------|
| 内部分析方法（30 个，5 个方法包） | Alpha | 全部完成，已内部测试 |
| 公开入口（research / tutor / write / review / full） | Alpha | 全部完成 |
| 知识库（87 个参考文件） | Alpha | 术语表、论证形式、哲学家数据库均已填充 |
| 对话模式（phil:tutor 的 reading / incubating） | Alpha | 已完成，待更多交互验证 |
| 写作生产（phil:write + phil:review） | Alpha | 已完成；由 phil:full 状态机编排，含双协作模式，验证运行待做 |
| 行为规则（3 条 + 运行时兼容） | Alpha | 已部署；兼容规则统一项目指南、协作别名、delegation 与 Zotero 降级 |
| 文献管理 | Alpha | Citation Gate 已增加 analysis metadata 与哈希验证；ingest 已实战运行论文/专著/文集三类文档 |
| Zotero 集成 | Alpha | 注释保全迁移与自动注册均经实战验证；存量按懒迁移原则逐步转换 |

**已知限制**：
- 双端静态与脚本测试已建立；五个公开入口仍需分别在 Claude Code 与 Codex 完成人工最小验收
- 哲学家数据库覆盖不均衡（分析传统为主，大陆哲学较弱）
- 观点台账已接入 Stage 3–6 的事件驱动召回；仍需在两个运行时分别完成真实长文写作的人工验收
- 已有生成一致性、manifest/frontmatter、别名、Zotero 降级、文献扫描与哲学家数据库治理的标准库测试；五个公开入口仍需分别在两个宿主中做人工最小验收

---

*最后更新: 2026-11-22（按 v0.7.0-alpha 校正）*
