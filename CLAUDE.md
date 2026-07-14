# CLAUDE.md

> **Project Status: Alpha** — All modules, agents, and skills are functional but have not undergone extensive field testing. Behavioral rules, workflows, and knowledge bases are subject to refinement.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Nature

This is a philosophical writing workflow project, not a code project. All files are text or PDF.

## Behavioral Rules

These rules apply to ALL interactions in this project. Full rule text is in `.claude/rules/`.

### Rule 1: No Sycophancy — Conditional Socratic Engagement
→ [rules/socratic-engagement.md](.claude/rules/socratic-engagement.md)
Assess clarity before responding. Clear ideas → execute directly. Vague ideas → Socratic questioning.
Trigger is **vagueness**, not novelty. Do not fabricate objections for the sake of appearing rigorous.

### Rule 2: No Hallucinated Citations
→ [rules/citation-integrity.md](.claude/rules/citation-integrity.md)
Never generate unverified references, quotations, page numbers, or publication details.
Mark unverified claims with `[source unverified]` or `[citation needed]`.

### Rule 3: Trigger-Based Version Management
→ [rules/version-management.md](.claude/rules/version-management.md)
Version cuts are NOT automatic. Three triggers: (1) post-review revision, (2) new insight/argument, (3) significant compression/expansion. Same-day triggers are merged. Draft file (`-draft.txt`) is never versioned.

## Directory Structure

**双仓库结构（v0.4）：隐私边界 = 仓库边界。** 外层仓库只含框架（可分享）；全部论文、文献、个人风格样本在 `Private/`（外层 gitignore，独立内层 git 仓库 + 私有 remote）。

```
.claude/       Framework 可执行层（外层仓库追踪）
  ├── settings.json   Permissions + hooks (committed)
  ├── commands/       7 composite commands (phil:* namespace)
  ├── rules/          3 behavioral rule modules
  ├── skills/         29 domain analysis skills (engine)
  ├── agents/         7 philosophy-specialized agents (3 dialogic + 4 production)
  ├── references/     方法论知识（glossaries, argument forms, taxonomies）
  └── shared/         Data contracts (12 JSON schemas + 5 report templates)
Framework/     Framework 非执行层（外层仓库追踪）
  ├── ARCHITECTURE.md 系统架构文档
  ├── changelog.md    框架版本历史
  └── lessons/        各论文 feedback-to-framework 的蒸馏
Shared/        可分享的策展知识（外层仓库追踪）
  └── philosophers-db/  49 位哲学家档案
Private/       私有内容层（外层 gitignore；内层独立仓库，PDF 除外）
  ├── Papers/{topic}/   每篇论文一个目录（手稿、refs.md、VERSIONS.md、
  │                     feedback-to-framework.md、论文级 CLAUDE.md）
  ├── bibliography/     文献总库（pdf/ 不进任何 git、analysis/、INDEX.md）
  ├── concepts/         跨论文概念笔记
  └── style/            个人写作样本（文风校准用）
style/format/  格式模板（LaTeX/Word 模板，可分享，外层追踪）

Memory: C:\Users\zhaok\.claude\projects\C--Projects-Philosophical-Writing\memory\
  Session-persistent knowledge (user preferences, project feedback, references)
```

## Commands Reference

| Command | Function | Runs |
|---------|----------|------|
| `phil:reconstruct` | 全维度理解文献 | 9-20 skills (mixed serial/parallel, auto domain detection) |
| `phil:evaluate` | 多角度同时批判 | 7 skills (fully parallel) |
| `phil:review` | 同行审稿 | phil-reviewer agent (8 dimensions + perspective simulation) |
| `phil:write` | 哲学写作 | phil-writer agent (outline / draft / revision) |
| `phil:comment` | 论证细节和概念澄清 | phil-commentator agent (6 critical dimensions) |
| `phil:pipeline` | 一键全流程 | phil-orchestrator agent (5 stages with quality gates) |
| `phil:tutor` | 导师式文献对话 — 询问思路、追问理解、推荐文献 | phil-tutor agent (Socratic dialogue + 4-phase arc) |

Each command file in `.claude/commands/` defines its skill composition, execution order, and output format.

## Workflow Conventions

### Papers (Private/Papers/{topic}/)
- Plain text writing; no markup languages（终稿 LaTeX 以 .txt 存于同目录；编译时临时复制 .txt → .tex）
- Writing in Chinese
- Directory & filenames use English kebab-case of paper topic

**Per-paper files:**
- `CLAUDE.md` — 论文级约定 + 主题关键词（文献推荐匹配用）
- `refs.md` — 论文级文献清单：`KEY | 角色(core-target/support/background) | 状态(cited/candidate/rejected) | 备注`，通过 KEY 指向文献总库 INDEX，零文件复制
- `{topic}-draft.txt` — Working draft. Freely overwritten. Never versioned.
- `{topic}-v{N}.txt` — Cut version. Created from draft when a trigger fires.
- `{topic}-review.txt` — Review report.
- `VERSIONS.md` — 本论文版本历史。Every cut version MUST be documented here with date, triggers, and description.
- `feedback-to-framework.md` — 写作中发现的框架缺陷记录，定期蒸馏进 `Framework/lessons/`

**Version cut process:** Copy `{topic}-draft.txt` → `{topic}-v{N}.txt` → document in `VERSIONS.md`. The draft persists as the working copy for the next round.

### Bibliography (Private/bibliography/) — 文献总库，唯一真源

```
Private/bibliography/
├── pdf/                              Original PDFs（不进任何 git——不可变二进制，可重新下载）
├── analysis/                         Paired analysis files ({Author-Title}.analysis.txt)
├── summaries/                        Level 0.5 摘要（v0.5 落地）
└── INDEX.md                          主清单（KEY、分析级别、topics 标签）
```

**Analysis levels (progressive, append-only):**
- Level 0.5: Summary — 核心论题+论证路线+关键概念+论敌+topics — *trigger: PDF added (v0.5, phil-summarize)*
- Level 1: Argument reconstruction — *trigger: selected as a paper dependency*
- Level 2: + Implicit premises, charity audit, conceptual analysis, distinction tracking — *trigger: first citation in a manuscript*
- Level 3: + Dialectical mapping, ontological commitment, modal analysis, domain-specific skills — *trigger: source becomes core target/dependency*

**文献推荐三触发点**（模型执行）：(1) 入库时——新文献 topics ↔ 各论文 CLAUDE.md 主题关键词匹配；(2) 论文内工作时——phil:tutor 扫描 INDEX 中 topics 匹配但不在本论文 refs.md 的条目（跳过 rejected）；(3) 引文提取时——phil-citation-extract 输出 acquisition_candidates。

### Citation Gate (Rule 2 enforcement, two-hop)
This is a model-executed behavioral rule:
1. **Hop 1**: 引用的 KEY 必须在本论文 `refs.md` 中登记
2. **Hop 2**: If a manuscript claim depends on analysis at Level N, but the source's `.analysis.txt` is only at Level N-1 or below → **BLOCK** and require analysis completion. No citation passes without a verified analysis backing it.

## Common Operations

### Interactive shell commands
Prefix with `!` to run in-session:
```
!pdftotext "Private/bibliography/pdf/xxx.pdf" -
!wc -m "Private/Papers/srinivasan-critique/srinivasan-critique-draft.txt"
```

### PDF Processing Workflow
1. Place PDF in `Private/bibliography/pdf/`
2. Use the `pdf` skill to extract text (**not** direct `pdftotext` CLI)
3. Run `phil:reconstruct` → `Private/bibliography/analysis/{Author-Title}.analysis.txt` (Level 1)
4. Escalate analysis level as needed per Citation Gate rules

### Manuscript Work Cycle
1. **Draft** in `Private/Papers/{topic}/{topic}-draft.txt`
2. **Review** with `phil:review` → review report
3. **Revise** draft → cut version when trigger fires
4. **Version cut**: `cp draft.txt v{N}.txt` + update `VERSIONS.md`

### LaTeX Compilation
```bash
cd "Private/Papers/{topic}" && cp topic.txt topic.tex && pdflatex topic.tex
```

### Character count
```bash
wc -m "Private/Papers/{topic}/{topic}-draft.txt"
```

### Private 仓库提交
论文内容的 git 操作在 `Private/` 内进行（独立仓库，私有 remote）。外层仓库永不追踪 Private/ 内容。

### Session Logging
Session summaries are written to `history.txt` by the model at the end of each conversation, per the memory convention `session-summary-to-history`. The file is gitignored as a local log.

## Knowledge Base

**Argument Forms**: 26 canonical forms in `.claude/references/argument-forms/` (see `argument-forms/INDEX.md` for the general/metaphysics/metaethics breakdown).

**Glossaries & Taxonomies**: `.claude/references/` contains domain-specific reference files (glossary-metaphysics.md, glossary-metaethics.md, ontological-categories.md, causation-taxonomy.md, moral-realism-taxonomy.md, normativity-taxonomy.md, fallacy-catalog.md, modal-logic-primer.md, thought-experiment-templates.md).

**Philosopher Database**: `Shared/philosophers-db/` — 49 philosophers across 3 domains (general/metaphysics/metaethics). Curated — may be cited.

**Data Contracts**: `.claude/shared/` — 11 JSON schemas for cross-skill composability + 5 report templates in `.claude/shared/templates/`.

## Cross-Session Memory

Persistent file-based memory at `C:\Users\zhaok\.claude\projects\C--Projects-Philosophical-Writing\memory\`. Each memory is a `.md` file with frontmatter. `MEMORY.md` serves as the session index.

Write memories for: user preferences, project goals, substantive feedback, external references. Do NOT memory code structure, git history, or CLAUDE.md contents — those are already in the repo.

## Architecture

The complete system architecture is defined in `Framework/ARCHITECTURE.md` (0.4-alpha), built atop `academic-research-skills` v3.15.0 (external plugin — all `ars-*` capabilities require this plugin to be installed), covering three subdomains: general analytic philosophy, metaphysics, and metaethics.

- **29 Skills** — Phase 1-6 complete. All skills in `.claude/skills/`
- **7 Commands** — Composite orchestration in `.claude/commands/`
- **7 Agents** — 3 dialogic (metaphysician, metaethicist, phil-tutor) + 4 production (writer, reviewer, commentator, orchestrator). All in `.claude/agents/`
- **12 JSON Schemas + 5 Report Templates** — Data contracts in `.claude/shared/`
- **26 Argument Forms** — Canonical definitions in `.claude/references/argument-forms/`
- For complete skill inventory, build roadmap, and detailed architecture — see `ARCHITECTURE.md`
