# Format — 版式模板

本目录存放导出用的版式模板，由 `Framework/Workflow/Scripts/render-output.py` 使用（`phil:write export` 模式，规则见 `Framework/Plugin/skills/write/references/export.md`）。文风样本不在这里，在 `Private/Style/`。

## 现有模板

| 文件 | 用途 | 说明 |
|---|---|---|
| `handout.css` | A4 讲义（PDF） | 正文宋体配 Georgia，标题微软雅黑，墨蓝强调色；编号项连续编号，论题框，参考文献悬挂缩进 |
| `slides.css` | 16:9 幻灯片（PDF） | 每个一级标题一页，页码在右下；讲者备注不打印 |
| `reference.pptx` | 幻灯片（pptx） | 由 `render-output.py make-reference` 从 Pandoc 默认模板生成：主题字体设为微软雅黑，强调色 #1F3A5F |
| `reference.docx` | Word 文件 | 同上生成：西文 Times New Roman，中文宋体 |

两份样式表都把中文引号、破折号和省略号交给中文字体，避免用西文字体的窄引号。换字体或配色时，改样式表顶部的变量；改 pptx 和 docx 模板后，重新运行 `make-reference`，或直接用 PowerPoint、Word 编辑这两个文件的母版和样式。

## 依赖

- **Pandoc**（3.x，有签名）：脚本依次在 PATH、`PANDOC` 环境变量和 `%LOCALAPPDATA%\Programs\pandoc\` 中查找。
- **PDF**：用 Edge 或 Chrome 的无头模式打印 HTML，不需要 LaTeX。

## 可以放进来的其他东西

- 目标期刊的 LaTeX 类文件或 Word 模板
- 期刊的格式要求（作者指南的网页存档或文本）
- 已发表论文的 PDF 样张，仅供本地参考（`*.pdf` 不进 git）
