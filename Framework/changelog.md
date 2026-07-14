# Framework Changelog

## v0.4-alpha — 2026-07-14

**仓库重构：Framework/Private 双仓库分离 + 文献联动机制**

- 隐私边界 = 仓库边界：全部论文、文献、个人风格样本移入 `Private/`（外层 gitignore，独立内层 git 仓库 + 私有 remote）
- PDF 不进任何 git（不可变二进制），备份靠文件同步
- 外层仓库解除对 manuscript/、bibliography/ 的追踪（历史保留，仓库为 private）
- `philosophers-db` 从 `.claude/references/` 迁至 `Shared/`（策展知识，可分享）
- `ARCHITECTURE.md` 迁至 `Framework/`；新增 `Framework/lessons/`（论文反馈蒸馏）
- 文献联动：论文级 `refs.md`（KEY 视图，零复制）+ INDEX `topics` 列 + Citation Gate 两跳化
- 推荐机制：phil-tutor 库内反向匹配 + phil-citation-extract 采购建议输出
- 预留：Level 0.5 摘要行（v0.5 phil-summarize 落地）

## v0.3-alpha — 2026-07-12

- Schema 全接线（12 schemas）、agent 精简（9→7）、INDEX 死链修复、hook 移除、约定统一
- phil:tutor 导师式文献对话 agent + phil-citation-extract 引文提取 skill

## v0.2-alpha — 2026-07-11

- 工作流重构：33→6 复合命令 + rules/ 提取 + phil:* 命名空间
- style/ 风格化目录 + 文风校准与格式定制

## v0.1-alpha — 2026-07-10

- 初始版本：29 skills + 知识库 + ARS 桥接
