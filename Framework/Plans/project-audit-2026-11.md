# 项目审计报告

- 日期：2026-11-22
- 版本：0.7.0-alpha（含未提交改动）
- 范围：框架层的结构、脚本、技能、跨 harness 兼容和使用成本
- 写作质量诊断含手稿内容，单独放在 `Private/Style/writing-quality-diagnosis-2026-11.md`

## 一、结论

项目的方向是对的：manifest 做单一真源，生成器产出各平台适配层，确定性脚本守住完整性。问题集中在四处：

1. **完整性闸门有实质漏洞。** Citation Gate 的第一跳没有真正读取 `refs.md`，文件改动后审批依然有效。这些已修复。
2. **写作质量没有责任环节。** 七条写作标准和八个审稿维度都针对论证，没有一条针对可读性。这是用户感到产出质量差的主因。
3. **跨 harness 已接近单源，但根指南被加载两遍。** 现在就可以只维护一份 `AGENTS.md`。
4. **成本集中在常驻指南和方法文件。** 每次会话固定加载约 5.8 万字符，单次分析最多可加载约 49 万字节方法文本。

## 二、本轮已完成的修改

全部在工作区，未提交。验证结果：137 个测试通过（审计前 96 个），`workflow-doctor` 通过，生成器重复运行无差异。`content-doctor` 剩余 25 项，均为 PDF 缺失或分析尚未验证，符合当前同步状态。

| 范围 | 修复内容 |
|---|---|
| Citation Gate | 第一跳改为读取 `refs.md`；拦截 `rejected` KEY 和错配的分析元数据；BLOCK 时退出码非零 |
| 哈希 | 文本按 LF 计算，修复 Windows 上对分析文件的误报；PDF 仍按原始字节计算 |
| 工作流状态 | 文件改动后审批失效；`status` 真正只读；闭环 PASS 必须有报告；拦截 Windows 根路径；原子写入；降级高危发现必须说明理由 |
| 观点台账 | 状态变更保留历史，损坏文件给出明确错误 |
| 文献索引 | 支持转义的竖线；格式错误的行会报错，不再错位读取 |
| 哲学家数据库 | 校验 `--person-id`，修复路径穿越；`source-backed` 必须对应 INDEX 中的 KEY；审批可安全重试 |
| Zotero 脚本 | 写入令牌防止重试时重复创建；部分失败时保留已创建的 key；不再强制使用写死的代理 |
| 适配层 | 已被第三节决定 4 的插件迁移取代 |
| 契约和文档 | 修正错误的方法 ID、无法运行的命令示例、互相矛盾的写权限说明、过时的版本和数量 |
| 写作规则 | 取消堆连接词的要求；禁止“只加不删”的修订；审稿视角中的哲学家归属必须有来源 |

## 三、结构性改动与决定

### 决定 1：根指南只维护一份（已完成）

用户选择只保留瘦身后的 `AGENTS.md`。新的 `AGENTS.md` 约 6,400 字符，由人工维护；`CLAUDE.md` 和根指南模板已删除，细节移到 `Framework/Workflow/References/project-conventions.md`。原来每次会话固定加载约 5.8 万字符，现在约 6,400 字符。随 `.claude/rules` 删除，四条行为规则的全文不再在 Claude Code 中自动加载，与 Codex 一致：`AGENTS.md` 保留每条规则的要点，需要时再读全文。如果希望 Claude Code 始终加载规则全文，可以在 `AGENTS.md` 里加 `@Framework/Workflow/Rules/<rule>.md` 导入，Codex 会把这一行当普通文字。

### 决定 2：写作流程改为两段式（已采用，2026-11-22）

建议按“论证稿 → 成文 → 分项编辑 → 冷读 → 作者定稿”重组 `phil-write`，审稿增加可读性维度，并新增只报告、不打分的 `prose-lint` 脚本。用户同意先试点，确认新流程更好后再设为默认。

第一轮（2026-11-22）用三节真实手稿比较新旧流程，两组用同一份论证稿，由用户盲评：

- 总分 58 比 57，偏好 1 比 1，另有 1 节持平。新流程没有明显更好，所以 `drafting: pipeline` 仍是可选项，不设为默认。
- 冷读指标偏向新流程（文字卡顿 7 比 10），但用户认为新流程的 s1 “机械、呆板”。冷读只测懂不懂，测不出这一点。
- 原因是成文规则纠枉过正：“一句只讲一件事”加上“少用关联词”，把逐条罗列的论证稿写成了断言清单。两组还共有套路化的节间衔接和防御性措辞，都来自上游规则和论证稿。

已据此修订风格卡、成文、编辑、论证稿和冷读规则，并给 `prose-lint` 增加“断续句群”检查。新流程的 s1 在这项上是 48%，旧流程是 17%。第二轮用修订后的规则重跑了 s1、s2：断续句占比降到 0% 和 22%，主张全部复原，剩下的防御性措辞主要来自论证稿。

用户审阅第二轮稿后认为质量较好，可以使用。流水线因此设为起草的默认方式，`PROJECT.md` 写 `drafting: classic` 可退回旧流程；论证稿关口的否定条目审查改为必做。详情见私有仓库的 `Style/pipeline-pilot/STATUS.md`。

### 决定 3：方法文件瘦身（试点完成）

最大的 5 个方法各写了一张约 10KB 的执行卡，原文完整保存为 `references/<slug>-full.md`，只在执行卡解决不了的歧义时加载。试点结果见第九节。

### 决定 4：入口和分发（已完成）

用户选择迁移到插件。公开技能现在只有一棵树 `Framework/Plugin/`，带 Claude Code 和 Codex 两份清单；入口是 `/phil:research`、`/phil:tutor`、`/phil:write`、`/phil:review`、`/phil:full`。生成的 `.claude/skills`、`.claude/commands`、`.claude/rules`、`.agents/skills` 和 `Private/` 里的桥接文件都已删除。本机已在用户级安装插件，它从仓库原地加载。Codex 路径按官方文档配置，尚未实测。

使用注意：

- VS Code 扩展按窗口缓存斜杠菜单，技能或插件变化后要运行 Developer: Reload Window。
- 项目设置只从会话启动目录读取。从 `Private/Projects/<topic>` 启动的会话看不到根目录 `settings.local.json` 里的技能开关。

### 暂缓项

`advance` 目前允许跳过阶段，审稿和分节审计也不是完成的必要条件。规则要求“用户可以跳过，但要留下记录”，所以合适的修法是增加跳过记录，这会改变状态 schema，建议在决定 2 之后一起做。

## 四、结构与代码

**做得好的地方**

- manifest 校验严格，方法、服务、技能的边界清楚。
- 生成器和 doctor 让多平台产物不易漂移。
- 判断交给模型、校验交给脚本的分工合理。

**仍需处理的问题**

- ~~`.claude/settings.json` 里有未提交的 WebFetch 放行项~~：已按用户要求移到 `settings.local.json`。
- 在本机 Git Bash 中，`python` 和 `python3` 指向 Windows Store 占位程序，文档里的脚本命令会失败。关闭系统的“应用执行别名”即可解决。
- 三个脚本各有一份相同的哈希函数。文件名用连字符，无法直接互相导入，暂时靠测试保证一致。
- `Lessons/zotero-integration.md` 仍写着特定机器的代理地址。

## 五、Skill 思路

**阅读**

- **先读后析。** 现在容易先跑 `reconstruct` 再读，等于把理解这一步交给了模型。建议让用户先写一段自己的重构，再展开 AI 分析并逐点对照。[Bastani 等](https://www.pnas.org/doi/10.1073/pnas.2422633122)发现，给提示而不直接给答案，可以减轻 AI 对学习的负面影响。
- **记录理解检查。** `phil:full` 的 research 阶段要求用户能复述论证，但状态里没有对应记录，这道门实际上无法检查。
- **用论证图贯穿全流程。** 可借鉴 [Argdown](https://argdown.org) 的受限语法，为前提编号，让重构、提纲、草稿和审稿都指向同一批前提。

**写作与引用**

- **引用检查细化到句子。** 现在的闸门只证明“这篇文献分析过”，不能证明“这句话有这段原文支持”。[ALCE](https://arxiv.org/abs/2305.14627) 发现最好的模型也有 50% 的情况缺少完整引用支持。建议增加主张与证据的对照表，并用脚本核对直接引语。
- **审稿独立于写作。** 审稿应在新上下文中运行，避免模型替自己的文字辩护。

**文献发现**

可参考 [philosophy-mcp](https://github.com/sea9401/philosophy-mcp) 和 [Sophotron](https://github.com/rookslog/sophotron) 接入 PhilPapers、SEP 等来源。PhilPapers 的条款严格限制数据再分发，只适合查询和核对，不能镜像到本地。

## 六、跨 harness 兼容

以下事实来自官方文档：

| 能力 | Claude Code | Codex |
|---|---|---|
| 根指南 | 读 `CLAUDE.md`；没有时读 `AGENTS.md`（2.1.277 起） | 读 `AGENTS.md`，合并上限默认 32 KiB |
| 共享方式 | `CLAUDE.md` 写 `@AGENTS.md`，不会重复加载 | 原生支持 |
| 项目技能 | `.claude/skills/` | `.agents/skills/` |
| 自定义命令 | `.claude/commands/phil/x.md` 生成 `/phil:x` | 已弃用，改用技能 |
| 插件 | `.claude-plugin/plugin.json` | 根 `plugin.json` 或 `.codex-plugin/plugin.json` |

**能否只维护一套？** 能，现在只有一份 `AGENTS.md`。Claude Code 在没有 `CLAUDE.md` 时直接读它，Codex 原生读它。审计前本机加载两份，是因为用户设置 `instructionFiles` 为 `claude-md-and-agents-md`，而仓库里两个文件内容几乎相同。

技能目录：已按决定 4 改为一棵插件树，两个宿主共用，做法参照 [obra/superpowers](https://github.com/obra/superpowers)（约 32 万星）。插件可能被复制到缓存目录，所以每个 `SKILL.md` 开头都写明：从会话的工作目录向上找到含 `Framework/Workflow/manifest.json` 的目录作为 `<root>`，再按 `<root>` 解析路径。

**披露方式。** 现在是三层：技能描述常驻（约 370 token），`SKILL.md` 调用时加载，方法和参考文件按需加载。`phil:full` 用 `disable-model-invocation`，只作人工入口。

## 七、使用成本

| 成本来源 | 审计前 | 现在 |
|---|---|---|
| 常驻指南 | 约 5.8 万字符，其中约 2.3 万是重复 | 约 6,400 字符（`AGENTS.md`） |
| 技能列表 | 14 项，10 项是无信息的命令 | 5 项插件技能，常驻约 370 token |
| evaluate 最坏情况的方法加载 | 约 39 万字节 | 约 16 万字节 |
| reconstruct 最坏情况的方法加载 | 约 49 万字节 | 约 43 万字节 |
| review 的方法加载 | 约 24 万字节 | 未变；`methodology` 仍是全文 |
| 方法文本留在主会话 | 每轮都按缓存价重复计费 | 未变；建议把重分析放进子代理 |

## 九、方法执行卡试点

**做法。** 5 个最大的方法各写一张执行卡，并保留全文。每个方法取一段公有领域原典，分别交给只读执行卡的代理和只读全文的代理，共 10 次运行。之后由 10 个评审代理在不知道来源的情况下两两比较，每组交换 A/B 位置各评一次，按覆盖、准确、深度、纪律、可用性五项各 1–5 分打分。

所用原典：

| 方法 | 原典 |
|---|---|
| methodology | Mill《功利主义》第四章 |
| analogy-check | Hume《自然宗教对话录》第二部分 |
| parity-check | Berkeley《三篇对话》第一篇 |
| intuition-pump | Plato《理想国》卷二古各斯之戒（Jowett 译） |
| contextualize | Mill《论自由》第一章 |

**结果。**

| 方法 | 执行卡 | 全文 | 运行 token（卡 / 全文） |
|---|---|---|---|
| analogy-check | 2 胜 | 0 胜 | 61,514 / 71,455 |
| parity-check | 1 胜 | 1 胜 | 59,120 / 74,037 |
| intuition-pump | 1 胜 | 1 胜 | 42,362 / 59,367 |
| contextualize | 1 胜 | 1 胜 | 49,231 / 59,775 |
| methodology | 0 胜 | 2 胜 | 50,133 / 77,512 |
| 合计 | 5 胜，233 分 | 5 胜，230 分 | 少约 23% |

评审在每份报告里找到的引文错误都是 0–2 处，两组相当。methodology 两次都以 1 分之差落败，评审指出执行卡把方法分类压缩得太狠，导致对“两种方法是嵌套还是竞争”的判断变弱。

**处理。** 前四张执行卡已经合入，原文作为 `references/<slug>-full.md` 保留。methodology 暂不替换，下一步应在执行卡里补回分类表的简表，再测一次。

**局限。** 每个方法只用了一段原典，评审是同一类模型，样本小。结论只能说明“没有看到质量下降”，不能说明执行卡更好。

## 八、建议路线

1. ~~根指南单源化和入口清理（决定 1、4）~~：已完成。
2. ~~写作流程试点（决定 2）~~：已采用，设为默认。
3. 方法执行卡（决定 3）：前四张已合入；修订 methodology 后重测，再推广到其余 25 个方法。
4. 阅读与引用增强：先读后析、论证图、句子级证据核对。

## 附：主要参考

- Claude Code：[Memory](https://code.claude.com/docs/en/memory)、[Skills](https://code.claude.com/docs/en/skills)、[Plugins](https://code.claude.com/docs/en/plugins)
- Codex：[AGENTS.md](https://developers.openai.com/codex/guides/agents-md)、[Skills](https://developers.openai.com/codex/skills)、[Plugins](https://developers.openai.com/codex/plugins/build)
- 开放标准：[Agent Skills](https://agentskills.io/specification)、[AGENTS.md](https://agents.md)
- 研究：[PaperQA2](https://arxiv.org/abs/2409.13740)、[OpenScholar](https://arxiv.org/abs/2411.14199)、[ALCE](https://arxiv.org/abs/2305.14627)、[STORM](https://arxiv.org/abs/2402.14207)、[DeepA2](https://arxiv.org/abs/2110.01509)、[LearnLM](https://arxiv.org/abs/2412.16429)
