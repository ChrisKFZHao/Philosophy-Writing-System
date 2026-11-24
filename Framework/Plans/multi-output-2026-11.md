# 多种输出：讲义、幻灯片及其他（方案草稿）

- 日期：2026-11-22
- 状态：已定案，试做中（2026-11-22）。入口为 `phil:write export`；Pandoc 3.14 解压版已装在 `%LOCALAPPDATA%\Programs\pandoc`；先用 rawlsian-ai 试做讲义和幻灯片，由 Sonnet 写，主会话把关风格和美观
- 需求：除论文正文外，项目还能产出报告幻灯片（PPT）、讲义等。用户要求以成本和效果为准（本项目开源）

## 一、现状

项目现在只产出论文正文：手稿是 `.txt`，LaTeX 也存成 `.txt`，编译时再复制成 `.tex`。`Shared/Format/README.md` 还在引用已经删除的 `ars-format-convert`、`phil-orchestrator`、`phil-writer`，内容已过时。

本机条件：没有 LaTeX、Office、LibreOffice；Windows 的“智能应用控制”处于强制模式，会拦截没有签名的程序。选工具时必须考虑这一点。

## 二、调研结论

### 2.1 哲学报告和讲义的惯例

以下来自哲学系和哲学家写的报告指南，由调研代理收集，链接附在文末；个别条目没有逐条核对。

1. **讲义开头是一句话的主张，加上不超过五个前提的主论证。** 写不出来，说明论文本身还没想清楚。（Elga，Princeton）
2. **长度：报告讲义一张纸正反面**；读书会和研讨课讲义 2–4 页。（Daily Nous；McGill 课程说明）
3. **节、前提、例子、定义连续编号**，跨节也不重新起号，口头报告时用编号指代。（Lasnik，UMD）
4. **幻灯片只放关键词**，完整句子只用于定义和形式化论证，一条要在两秒内读完；长引文放讲义，不放幻灯片。（Koksvik）
5. **不要念论文。** 如果必须念，先删掉无趣的段落。（Koksvik；Daily Nous）
6. **时间控制在目标的正负 15% 以内**，讲义上标出可以略过的部分。（Lasnik；Elga）
7. **研讨课报告约三分之二复述文本**，含两三个理解问题；**三分之一提出自己的异议**。（Hoek）
8. **引文用原典编号**，如 Stephanus 页码、Bekker 编号，不用译本页码。（McGill；BPA）
9. **讲义和幻灯片互补，内容不重复。**

### 2.2 论文转幻灯片的系统

| 系统 | 做法 | 输出 | 对我们的启示 |
|---|---|---|---|
| PPTAgent（arXiv 2501.03936，MIT） | 先分析参考模板的页型，再按大纲逐页编辑模板 | 可编辑 pptx | 用模板槽位，不从零排版；内容、设计、连贯分开评 |
| Paper2Poster（arXiv 2505.21497，MIT） | 解析 → 布局 → 渲染，用视觉模型检查溢出 | 可编辑 pptx 海报 | 渲染后检查；用“读者能否答出要点”（PaperQuiz）检验压缩是否丢了内容 |
| AutoPresent（arXiv 2501.00912，MIT） | 模型写生成幻灯片的代码 | pptx | 生成代码才能得到可编辑的文件，但代价高、不稳定 |
| SlideGen（arXiv 2512.04529，MIT） | 多个代理分工，19 个固定版式槽位，讲者备注单独生成 | 可编辑 pptx | 版式固定、备注分开；版面密度可以自动检测 |

后两项的出处由调研代理读过，我没有抽查。

**共同的教训：模型负责内容，版式交给固定模板和脚本；渲染之后要检查。**

### 2.3 工具链（本机实测）

| 工具 | 许可证 | 本机能否运行 | 结论 |
|---|---|---|---|
| **Pandoc 3.14** | GPL-2.0+，作为外部命令调用 | 能。`pandoc.exe` 有签名（SignPath Foundation）。解压版 43 MB | **采用** |
| **Edge 无头打印** | Windows 11 自带 | 能，有签名 | **采用**，用来把 HTML 打印成 PDF |
| Typst 0.15 | Apache-2.0 | `typst.exe` 没有签名，会被拦截 | 不用 |
| Quarto 1.11 | MIT | 安装包 134 MB，内置的 Typst 等程序同样可能没有签名 | 不用 |
| Marp | MIT | pptx 默认每页是一张图片，文字改不了 | 不用 |
| Anthropic pptx、docx 技能 | Apache-2.0（已核对 LICENSE） | 每次都让模型现场写生成代码，token 高、结果不确定 | 不依赖；检查思路可以借鉴 |
| python-pptx | MIT | 依赖 lxml、Pillow 两个原生库，签名未查 | 用不上 |

实测：用一份中文示例 Markdown（葛梯尔问题，三页内容）在本机分别生成：

- **pptx。** Pandoc 直接生成，4 页，都是原生文本框，中文正常，讲者备注进了备注栏。主题的东亚字体为空，由 PowerPoint 自行回退。
  - 改进办法：脚本从 Pandoc 的默认参考模板生成 `reference.pptx`，把东亚字体设为微软雅黑。只用标准库改 XML 即可。
- **docx。** Pandoc 直接生成。
- **A4 讲义 PDF。** Pandoc 先生成 HTML，套上打印样式表，再用 Edge 无头打印。结果是 1 页，中文、编号、引文块和表格的排版都正常。不需要 LaTeX 或 Typst。
- **幻灯片 PDF。** 原理相同：样式表把每个一级标题排成一页 16:9。这条路线还没有实测。

其他系统上，用 Chrome 或 Chromium 加同样的参数即可。

## 三、建议做法

### 3.1 原则

1. **模型只写一份内容稿，脚本出所有格式。** 内容稿是 Pandoc Markdown，开头一段 YAML 写明种类、时长和听众。幻灯片按一级标题分页，讲者备注写在 `::: notes` 块里。模型从不写排版代码。
2. **内容尽量取自已有产物，不重新生成。** 论证稿本身就是一份讲义的骨架：编号的主张、理由、反对与回应、术语、引用，正对应哲学讲义的惯例 1、3。读书会讲义取自重构分析和证据单元。
3. **引文必须能核对。** 内容稿里写 `> 引文 [KEY, p. 12]`。脚本做三件事：
   - 到 `pdf-extract.py` 产出的证据单元里逐字核对引文；
   - 确认 KEY 已经登记在 `refs.md`；
   - 按 INDEX 把标记换成“（作者，年份，页码）”。

   核对不上就标 `[citation needed]`，规则 2 照常适用。
4. **检查分两层。**
   - 脚本检查：每页条数和每条字数（两秒规则）、编号是否连续、引文能否核对、页数和时长是否相称、讲义是否超过两页。
   - 冷读者检查：只看讲义，能否复述主论证。这借自 PaperQuiz，复用写作流水线的冷读环节。

### 3.2 输出种类

| 输出 | 内容来源 | 格式 | 优先级 |
|---|---|---|---|
| 报告讲义 | 论证稿、证据单元、`refs.md` | A4 PDF，可另出 docx | 1 |
| 报告幻灯片 | 同上，再加讲者备注 | pptx（可编辑）和 PDF | 1 |
| 读书会讲义 | 重构分析、证据单元、理解问题 | A4 PDF | 2，等提取层完成 |
| 投稿用 docx | 手稿正文 | docx，参考模板设中文字体和行距 | 3 |

### 3.3 组成

- **脚本 `Scripts/render-output.py`。**
  - 输入一份内容稿，`--to` 可选 `pptx`、`handout-pdf`、`slides-pdf`、`docx`、`html`。
  - 在 PATH 或 `PANDOC` 环境变量里找 Pandoc，在常见位置找 Edge 或 Chrome。
  - 套用 `Shared/Format/` 里的模板。
  - `--check` 输出一份 JSON 检查报告。
  - 只调用外部命令，不引入新的 Python 依赖。
- **模板放在 `Shared/Format/`**：`reference.pptx`、`reference.docx`、`handout.css`、`slides.css`。同时重写过时的 README。
- **两张规则卡**：`handout-rules.md` 和 `slides-rules.md`。把 2.1 的惯例写成模型写内容稿时遵守的规则，每张约 1–2 KB。

### 3.4 成本

| 项目 | 成本 |
|---|---|
| 模型写内容稿 | 一份讲义加一套 20 分钟的幻灯片，约 2,000–4,000 个输出 token |
| 格式转换和检查 | 由脚本完成，不花 token |
| 返修 | 只改检查不通过的页，最多两轮 |
| 对比：让模型现场写 pptxgenjs 代码 | 每次约 1–2 万 token，结果还不稳定 |

## 四、决定记录（原为待决事项）

1. **安装 Pandoc。** 建议解压到用户目录（43 MB，不需要管理员权限），脚本通过 `PANDOC` 环境变量找到它；也可以装 MSI 版。
2. **入口放在哪里。**
   - A：新增公开技能 `phil:present`，模式为 `handout`、`slides`、`reading-handout`、`docx`。只有调用时才加载，常驻成本是一行描述，约 60 token。
   - B：作为 `phil:write` 的新模式 `export`，读书会讲义则放进 `phil:research`。
   - 建议选 A：这类产出既来自写作，也来自阅读，单独成一个技能更清楚。
3. **先做哪几种。** 建议先做报告讲义和幻灯片，用 `rawlsian-ai` 已有的论证稿试做一份，你看效果后再推广。

## 附：主要来源

- 报告指南：Elga, https://swh.princeton.edu/~adame/teaching/general/talks-and-presentations-guide.pdf ；Lasnik, https://terpconnect.umd.edu/~lasnik/Prof%20Meth2018/Conference%20presentations%20and%20job%20talks%20HO.pdf ；Koksvik, https://www.koksvik.net/talk.php ；Daily Nous, https://dailynous.com/2014/09/25/giving-a-philosophy-talk ；Hoek, https://danielhoek.com/wp-content/uploads/2023/10/Presentation-instructions-Phil-Lang.pdf
- 系统：PPTAgent https://github.com/icip-cas/PPTAgent ；Paper2Poster https://github.com/Paper2Poster/Paper2Poster ；SlideGen https://github.com/Y-Research-SBU/SlideGen ；AutoPresent https://arxiv.org/abs/2501.00912
- 工具：Pandoc https://pandoc.org/MANUAL.html ；Anthropic skills https://github.com/anthropics/skills （pptx 目录的 LICENSE.txt 为 Apache-2.0，已核对）

## 五、试做结果（2026-11-22，rawlsian-ai）

- 产出：`Private/Projects/rawlsian-ai/export/`。包括两页 A4 讲义（28 个编号项，6 条参考文献），以及 20 分钟报告用的 16 页幻灯片加标题页（PDF 和 pptx 各一份，每页都有讲者备注）。
- 分工：内容稿由 Sonnet 写，渲染脚本由 Sonnet 写；主会话核对内容是否忠实于原稿，修改措辞，调整版式。
- 内容稿初稿的问题和处理：
  - 一个前提的说法偏离原稿；一处观点归属过宽；一处条件句被写成了断言。三处都已对照原稿改正。
  - “不是……也不是……”式的防御性条目约 15 处，删去大半。
  - 第一张幻灯片与自动生成的标题页重复。
  - 据此在 `export.md` 里补了规则：说清楚是什么；对比每项最多一处；不重复论题；不写标题页。
- 冷读：读者只看讲义，就复述出了论题和全部六步论证，通过。另指出：
  - 定义 (8) 与前提 (1) 重复，已删。
  - (4) 的说法不清，已改。
  - (20)、(26) 的含义不清。这两处出在原稿的论证本身，作为审稿意见交给作者。
- 版式调整：
  - 中文引号改用全角字形；引用前不加空格；引用放在句号之前。
  - 改用等高数字；参考文献改为悬挂缩进；长标题拆成主标题和副标题。
- 待办：
  - pptx 的实际版面要在 PowerPoint 或 WPS 里确认，本机没有 Office。
  - 幻灯片里引用讲义的编号目前是手写的，讲义一改就要同步。可以考虑让脚本按讲义的 `(@label)` 自动换算。

