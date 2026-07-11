# Charity Check Examples

---

## Example 1: Weakened Argument — Empiricism Oversimplified

### Input (Argument Reconstruction Report Summary)

```
[P1] All human knowledge comes from sensory experience.
[P2] Mathematical truths do not come from sensory experience.
───────
[C]  ∴ Mathematical truths are not knowledge.
```

Reconstruction note: "The argument relies on P1 as the sole criterion of knowledge."

### Output

```
## Charity Audit Report

### Premise-Level Charity Assessment

| Premise | Original Expression | Reconstructed Version | Charity | Issue Description |
|---------|--------------------|-----------------------|---------|-------------------|
| [P1] | "Knowledge comes from experience" | All human knowledge comes from sensory experience | **Under-charitable** | Universalized and locked onto the word "sensory," while the original may allow other channels of experience |

### Violation Details

#### Violation 1: [P1] Interpretation of "Knowledge comes from experience"

- **Location**: Premise number [P1]
- **Original Expression**: "Knowledge comes from experience" (paraphrase of Locke, Essay, II.i.2)
- **Reconstructed Version**: [P1] All human knowledge comes from sensory experience
- **Problem**: Restricting "experience" to "sensory experience" excludes possible inner experience (such as self-perception,
         affective experience, etc.). For Locke himself, experience divides into "sensation" (sensory) and
         "reflection" (reflection on internal operations), both termed "experience."
- **Alternative Interpretations**: 
  - **Strong alternative**: P1: All human knowledge's conceptual material ultimately derives from experience (sensory or reflective)
    (Distance: Small — only one word needs changing)
- **Impact of Substitution**: With the strong alternative, P2 no longer conflicts (mathematical truths may acquire
                    conceptual material from reflective experience), and the argument's validity is weakened.
```

---

## Example 2: Charitable Argument — Already Fair to the Interlocutor

### Input

```
[P1] An act is pious if and only if it is loved by the gods (candidate definition of Divine Command Theory).
[P2] If P1, then the concept of "piety" depends on whether gods exist.
[P3] For persons engaged in reflection on faith, it cannot be determined whether gods exist.
───────
[C]  ∴ For such persons, the concept of "piety" is open to question.
```

### Output

```
## Charity Audit Report

### Audit Status: Pass

### Premise-Level Charity Assessment

| Premise | Charity | Notes |
|---------|---------|-------|
| [P1] | Sufficiently Charitable | Already labeled as a "candidate definition," marking P1 as provisional; not attributed to the author as a conclusion |
| [P2] | Sufficiently Charitable | A clear logical consequence of P1 |
| [P3] | Sufficiently Charitable | Qualified with "For such persons," without overgeneralizing |

### Holistic Structural Charity

- Argument structure reflects authorial intent: Yes
- Explanation: The reconstruction preserves the provisional status of P1, without attributing "Divine Command Theory"
  to the author. The qualification on P3 does not absolutize it into universal skepticism.

### Summary

- Charity violation count: 0
- Commentary: Across multiple ambiguous passages, the text selects charitable and reasonable interpretations,
  and annotates provisional elements.
```
