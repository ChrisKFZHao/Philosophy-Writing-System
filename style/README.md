# Style — 文风与格式定制

本目录用于存放个人写作风格和格式模板，使项目产出的论文在文风和版式上与你保持一致。

## 目录结构

```
style/
├── writing/          ← 行文：样文（你的过往写作，用于学习文风）
│   ├── paper-1.txt   （你自己的论文、评论、笔记等）
│   └── ...
└── format/           ← 格式：版式模板
    ├── templates/    （Word .dotx 模板）
    ├── latex/        （LaTeX 项目文件 .cls/.sty 等）
    └── pdf/          （目标期刊的已发表论文 PDF，供版式参考）
```

## writing/（行文）

放入你写过的高质量文本——样文越多、质量越高，输出的文风越贴近你。

**适用场景：**

1. **ARS Style Calibration** — ARS 的 Style Calibration 功能接受 3+ 篇过往论文，学习你的句子节奏、用词偏好、引文集成风格。参见 `shared/style_calibration_protocol.md`
2. **phil-writer 文风参考** — phil-writer agent 在写作时可以引用这些样文作为文风基准
3. **手动对比** — 输出前后对照样文，自行调整不一致之处

**建议放入：**

- 你写过的哲学论文（已发表或未发表均可）
- 详细的评论或笔记片段（体现你的论述节奏）
- 反映你写作风格的任何中文/英文学术文本

## format/（格式）

存放目标出版物的版式要求。使格式化输出不必每次都从头配置。

**建议放入：**

- **LaTeX 项目**（`.cls` / `.sty` / 完整项目文件夹）——目标期刊或你的个人 LaTeX 模板
- **Word 模板**（`.dotx`）——你惯用的排版模板
- **PDF 样张**——目标期刊的已发表论文 PDF，供格式参考
- **格式要求文档**——期刊的 author guidelines（PDF 或网页存档）

**使用方式：**

- `ars-format-convert` 命令可转换为 LaTeX/DOCX/PDF 格式，结合本目录的模板使用
- `phil-orchestrator` 的 Stage 5 中可选调用 `ars-format-convert` 进行格式转换

## 与项目现有机制的关联

| 组件 | 关联方式 |
|------|----------|
| `phil-writer` agent | 写作时可参考 `style/writing/` 样文调整文风 |
| `phil-orchestrator` | Stage 5 格式化步骤可使用 `style/format/` 中的模板 |
| ARS `style_calibration_protocol.md` | 3+ 篇样文 → 学习写作风格 |
| ARS `ars-format-convert` | 使用 `style/format/` 中的模板输出为 LaTeX/DOCX/PDF |
| ARS `ars-disclosure` | 结合期刊格式要求生成 AI 使用声明 |
