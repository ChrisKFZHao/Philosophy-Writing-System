---
description: "Evaluate arguments from moral disagreement"
---

# /phil-moral-disagreement

Loads the `phil-moral-disagreement` skill to evaluate arguments that leverage the existence, nature, or persistence of moral disagreement for or against metaethical positions.

## Usage

```
/phil-moral-disagreement [text]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) and a moral realism position analysis (`/phil-moral-realism`) are recommended.

## Behavior

1. Identifies the structural form of the disagreement argument — is it an abductive argument (best explanation of disagreement favors anti-realism) or a direct argument (disagreement is incompatible with moral facts)?
2. Classifies the type of disagreement invoked: inter-cultural, intra-cultural, peer disagreement, fundamental vs. superficial, persistent vs. resolvable
3. Evaluates whether the disagreement is best explained by: (a) genuine moral facts plus epistemic shortfall, (b) cultural variation without objective moral facts, (c) evolutionary pressures on moral judgment, or (d) conceptual confusion
4. Applies the convergence critique — is the prevalence of moral convergence (e.g., across fundamental norms) a counterweight to disagreement arguments?
5. Analyzes whether the disagreement argument targets all normative domains equally (companions-in-guilt vulnerability) or is specific to morality
6. Outputs the moral disagreement analysis report

## Notes

- References: `moral-realism-taxonomy.md`, `glossary-metaethics.md`
- Cross-domain: Closely tied to `phil-moral-realism` (disagreement as a core anti-realist challenge); interfaces with `phil-moral-epistemology` (disagreement as epistemic defeater)
- Distinguishes metaethical disagreement arguments from first-order normative disagreement about specific moral questions
