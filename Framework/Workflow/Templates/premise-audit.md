# Premise Audit Template

Template for `phil-premise-detect` output reports.

---

```
===============================================================================
隐含前提审计报告
===============================================================================

日期：{YYYY-MM-DD}
分析对象：{Reconstructed argument reference}
审计者：phil-premise-detect skill v{version}
基于：{phil-argument-reconstruct output reference}
===============================================================================


0. 审计范围
-------------------------------------------------------------------------------

{Which arguments are being audited? List argument IDs from the reconstruction.}


1. 隐含前提清单
-------------------------------------------------------------------------------

### ARG-{N}: {Argument Name}

[IP-{N}.1] {Implicit premise statement}
  类型：{conceptual_bridge / category_jump / missing_universal /
         existential_presupposition / exclusivity_assumption /
         background_framework / hidden_quantification_shift}
  确定性：{high / medium / low}
  理由：{Why this certainty rating?}
  拒绝影响：{fatal / severe / mild / none}
  说明：{What happens to the argument if this premise is rejected?}

[IP-{N}.2] ...


2. 按类型汇总
-------------------------------------------------------------------------------

### 概念桥接前提 (Conceptual Bridge)
- [IP-X.Y]: {Brief description}
- ...

### 范畴跳跃前提 (Category Jump)
- ...

### 缺失全称前提 (Missing Universal)
- ...

### 存在预设 (Existential Presupposition)
- ...

### 排他性假设 (Exclusivity Assumption)
- ...

### 背景框架前提 (Background Framework)
- ...

### 隐藏量词转换 (Hidden Quantification Shift)
- ...


3. 高影响发现（确定性高 + 拒绝影响 ≥ severe）
-------------------------------------------------------------------------------

{List of implicit premises that are both high-certainty and would severely
or fatally damage their arguments if rejected. These are the most important
findings of the audit.}

1. [IP-X.Y] ({Argument}): {Statement} — 拒绝影响: {fatal / severe}
2. ...


4. 总体评估
-------------------------------------------------------------------------------

{1-2 paragraphs: How premise-dependent is the overall argument? Are the
implicit premises plausible? Which ones would an opponent most likely
challenge? What is the argument's hidden assumption profile — does it rely
heavily on contested background frameworks or are its implicit premises
relatively uncontroversial?}

===============================================================================
* 审计完成。隐含前提的确定性评估基于文本证据和哲学背景知识。
* 拒绝影响评估假设前提被完全拒绝（而非被修正）的情况。
===============================================================================
```
