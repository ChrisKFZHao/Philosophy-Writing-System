---
description: "Analyze moral language — cognitivism/expressivism/prescriptivism"
---

# /phil-moral-semantics

Loads the `phil-moral-semantics` skill to analyze the semantic commitments of moral language — what moral utterances mean, whether they express beliefs, and how they embed in logical contexts.

## Usage

```
/phil-moral-semantics [text]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) and a moral realism analysis (`/phil-moral-realism`) are recommended to provide context.

## Behavior

1. Scans for semantic indicators — truth predicates applied to moral claims, belief/attitude language, embedding behavior in conditionals and negations
2. Classifies the argument's semantic stance: cognitivist vs. non-cognitivist; descriptivist vs. expressivist vs. prescriptivist
3. Identifies the argument's implicit theory of meaning for moral terms — is it referential, inferential role, expressivist, hybrid?
4. Tests for Frege-Geach embedding viability: can the account explain moral claims in unasserted contexts (conditionals, disjunctions, attitude reports)?
5. Analyzes the argument's treatment of thick moral concepts and their descriptive/evaluative entanglement
6. Evaluates the argument's theory of truth for moral discourse — robust correspondence, deflationary minimalism, quasi-realist appropriation
7. Outputs the moral semantics analysis report

## Notes

- References: `glossary-metaethics.md`, `metaethical-distinctions.md`
- Cross-domain: Feeds into `phil-moral-realism` (semantic commitments constrain viable realist positions); interfaces with `phil-moral-psychology` (semantic vs. psychological accounts of moral judgment)
- Distinguishes semantic theories of moral meaning from metaphysical theories of moral facts
