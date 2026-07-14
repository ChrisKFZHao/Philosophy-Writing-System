# 引用完整性规则

永远不要生成未经核实的参考文献、引文、页码或出版细节。

## 行为准则

- **不虚构书目**：只引用你实际读过的著作——通过本项目的 PDF、笔记或重构文本。未读过则明确标注 `[source unverified]` 或 `[citation needed]`
- **不发明引文**：除非实际读过并能验证引用，否则不要产出"正如 X 在 Y 中论证……"内容
- **区分 known 与 inferred**：如果从一般哲学知识推断某位哲学家的立场或某来源的存在，使用明确的 hedging（"据推测……""可能……""似乎……"），永远不与断言性语言混用
- **知识库例外**：`Shared/philosophers-db/` 中的哲学家信息经过策展，可以引用。但不在该数据库中的具体论文、页码和引文都需要验证

## Citation Gate（两跳检查）

手稿中的每条引用必须通过两跳验证，任一跳失败即 **BLOCK**：

1. **第一跳（论文清单）**：引用的 KEY 必须出现在本论文的 `refs.md` 中（`Private/Papers/{topic}/refs.md`）。不在清单中 → 先将文献登记入 refs.md（状态 `cited`）
2. **第二跳（分析级别）**：该 KEY 在 `Private/bibliography/INDEX.md` 中的分析级别必须满足引用主张的依赖级别。手稿主张依赖 Level N 的分析，但源文献的 `.analysis.txt` 只有 Level N-1 或更低 → BLOCK，要求先补齐分析
