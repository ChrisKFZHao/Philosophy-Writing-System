---
description: 多角度同时批判哲学文献 — 并行运行反例生成、辩证映射、类比评估、一致性检查、直觉泵检测、方法论反思、谬误分析
---

# /phil:evaluate

## Usage

```
/phil:evaluate <text or argument>
```

或先提供文本再触发 `/phil:evaluate`。接受 `/phil:reconstruct` 的输出作为输入时效果最佳。

## 定位

多角度同时批判**他人已有文献**。7 个评价维度并行运行，输出集成的批判评价报告。

## 编排的技能

全部 7 个技能无依赖关系，**并行运行**：

| 技能 | 功能 |
|------|------|
| `phil-counterexample` | 构造反例：6 种反例类型 + 四维评估 + 辩证预期 |
| `phil-dialectical-map` | 辩证映射：thesis-objection-response 攻防树 |
| `phil-analogy-check` | 类比评估：源-目标对应、共享属性相关性、反类比检测 |
| `phil-parity-check` | 一致性检查：推理对等性、companions-in-guilt、虚假对等 |
| `phil-intuition-pump` | 直觉泵分析：直觉→判断链、框架效应、debunking 易感性 |
| `phil-methodology` | 方法论反思：方法归类、一致性检查、替代方法 |
| 谬误检测 | 基于 `fallacy-catalog.md` 的谬误扫描 |

## 输出格式

生成集成的批判评价报告，包含以下章节：

1. **执行摘要**：最严重的 3-5 个问题、整体论证力评估
2. **反例清单**：按严重性排序，含类型、目标前提、辩证预期
3. **辩证结构**：攻击-防御树的 ASCII 可视化
4. **类比评估**：每个类比论证的映射充分性评分
5. **一致性检查**：对等性主张的验证结果
6. **直觉泵分析**：framing 偏差和 debunking 评估
7. **方法论审计**：方法分类、一致性、替代方案
8. **谬误清单**：检测到的逻辑跳跃和谬误
9. **改进建议**：最应该被作者处理的 3-5 个关键问题

## Notes

- 所有输出使用中文
- 7 个技能并行运行，每个独立产出后再合并
- 如果已有 `/phil:reconstruct` 的输出，直接将其作为输入——不需要重新分析
- 与 `/phil:review` 的区别：evaluate 针对他人文献的论证质量，review 针对自己写作的论文评审
