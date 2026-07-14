# Format — 版式模板

本目录存放目标出版物的版式要求与排版模板（可分享的策展知识，外层仓库追踪）。使格式化输出不必每次从头配置。

> 个人写作样本（文风校准用）不在此处——见 `Private/Style/`（私有仓库）。

## 建议放入

- **LaTeX 项目**（`.cls` / `.sty` / 完整项目文件夹）——目标期刊或你的个人 LaTeX 模板
- **Word 模板**（`.dotx`）——你惯用的排版模板
- **PDF 样张**——目标期刊的已发表论文 PDF，供版式参考（注意：`*.pdf` 被 gitignore，仅本地存放）
- **格式要求文档**——期刊的 author guidelines（网页存档或文本）

## 使用方式

- `ars-format-convert` 命令可转换为 LaTeX/DOCX/PDF 格式，结合本目录的模板使用
- `phil-orchestrator` 的 Stage 5 中可选调用 `ars-format-convert` 进行格式转换

## 与项目机制的关联

| 组件 | 关联方式 |
|------|----------|
| `phil-writer` agent | 写作时参考 `Private/Style/` 样文调整文风（行文），本目录负责版式（格式） |
| `phil-orchestrator` | Stage 5 格式化步骤可使用本目录中的模板 |
| ARS `style_calibration_protocol.md` | 3+ 篇样文 → 学习写作风格（样文在 `Private/Style/`） |
| ARS `ars-format-convert` | 使用本目录中的模板输出为 LaTeX/DOCX/PDF |
| ARS `ars-disclosure` | 结合期刊格式要求生成 AI 使用声明 |
