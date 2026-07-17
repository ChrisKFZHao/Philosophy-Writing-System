---
description: Full-dimensional comprehension of philosophical texts — simultaneously runs argument reconstruction, charity audit, implicit premise detection, conceptual analysis, distinction tracking, thought experiment analysis, modal analysis, and contextualization, with automatic domain detection triggering specialized metaphysics/metaethics analyses
---

# /phil:reconstruct

## Usage

```
/phil:reconstruct <text>
```

Or provide the text first, then trigger `/phil:reconstruct`.

## Role

Full-dimensional comprehension of others' texts. Runs all "understanding"-level analysis skills in a single pass and outputs an integrated argument-comprehension report.

## Orchestrated Skills

Executed in stages according to dependencies; skills within a stage may run in parallel:

### Stage 1: Core Argument Analysis (serial, strong dependencies)
| # | Skill | Depends on |
|------|------|------|
| 1 | `phil-argument-reconstruct` | None — must run first |
| 2 | `phil-charity-check` | Output of 1 (the reconstruction is needed to audit charity) |
| 3 | `phil-premise-detect` | Output of 2 (implicit premises can only be identified once the charitable version is fixed) |
| 4 | `phil-modal-arg` | Output of 1 (the reconstruction is needed to assess modal structure) |

### Stage 2: Conceptual and Experimental Analysis (parallel)
| Skill | Depends on |
|------|------|
| `phil-conceptual-analysis` | Output of 1 (the reconstruction is needed to locate key concepts) |
| `phil-distinction-track` | Output of 1 |
| `phil-thought-experiment` | Output of 1 |
| `phil-intuition-pump` | Output of 1 |

### Stage 3: Contextualization (serial)
| Skill | Depends on |
|------|------|
| `phil-contextualize` | After Stages 1-2 are complete; contextual positioning based on the full understanding |

### Stage 4: Automatic Domain Detection (triggered as needed)
Automatically detect and trigger the following skills based on the text's content:
- **Metaphysics triggers** (ontological/identity/grounding/conceivability/causation/essence/natural-kind vocabulary): run the corresponding skills
- **Metaethics triggers** (moral/normative/reasons/obligation vocabulary): run the corresponding skills

Domain detection logic:
- Scan the text for keywords → list the triggered domains → report to the user for confirmation → run the corresponding skills

## Output Format

Generate an integrated argument-comprehension report (structure follows `analysis-report-schema.json`) containing the following sections:

1. **Executive summary**: the text's core thesis, argument type, and an overview of its logical structure
2. **Argument reconstruction**: numbered premise-conclusion chains, implicit premises flagged, logical form
3. **Charity audit**: assessment of the reconstruction's charitableness, alternative readings
4. **Concept map**: key concepts and their definitions, the network of relations among concepts
5. **Distinction index**: inventory and analysis of all conceptual distinctions in the text
6. **Thought experiments and intuition pumps**: structural deconstruction and assessment of argumentative force
7. **Modal assessment**: analysis of the logical structure of modal claims
8. **Contextual positioning**: the text's place within the dialectical tradition
9. **Domain-specific analysis** (as needed): ontological commitment inventory / metaethical position analysis
10. **Open questions**: concepts awaiting clarification, premises awaiting completion

## Notes

- Write all output in Chinese (project convention)
- Domain detection is automatic; explicitly report which domains were triggered and which skills were activated
- This command's output is the primary input to `/phil:evaluate` and `/phil:write draft`
- Stage 1 cannot be parallelized (strong dependencies); Stage 2 may run in parallel internally
