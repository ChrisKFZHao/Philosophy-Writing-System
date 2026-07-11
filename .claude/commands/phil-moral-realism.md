---
description: "Analyze moral realism/anti-realism/error theory arguments"
---

# /phil-moral-realism

Loads the `phil-moral-realism` skill to classify and analyze arguments about the existence, nature, and objectivity of moral facts.

## Usage

```
/phil-moral-realism [text]
```

Prerequisite: An argument reconstruction (`/phil-reconstruct`) is recommended to isolate the metaethical argument in standard form.

## Behavior

1. Scans for metaethical stance markers indicating positions on the realism/anti-realism spectrum
2. Classifies the argument's position on the full realism spectrum: robust non-naturalism through reductive naturalism, constructivism, error theory, expressivism, to relativism
3. Maps the argument's commitments on four core dimensions: cognitivism, truth-evaluability, existence of moral facts, and mind-independence
4. Reconstructs the positive argument for the position and any negative arguments against rival views
5. Identifies dialectical vulnerabilities: queerness, disagreement, supervenience, Frege-Geach, evolutionary debunking, open question, moral twin earth
6. Outputs the moral realism position analysis report

## Notes

- References: `moral-realism-taxonomy.md`, `glossary-metaethics.md`, `metaethical-distinctions.md`
- Cross-domain: Feeds into `phil-moral-disagreement` (disagreement challenge), `phil-moral-epistemology` (possibility of moral knowledge), and `phil-moral-supervenience` (supervenience explanatory burden)
- Distinguishes the argument being analyzed from the metaethical position being defended
