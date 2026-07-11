# Distinction Tracking Examples

---

## Example: The Distinction Network in Berlin's "Two Concepts of Liberty"

### Input

> Berlin, *Two Concepts of Liberty* (1958), opening paragraphs (paraphrased summary).
> Berlin introduces the distinction between negative liberty and positive liberty as the core framework of the essay.
> Subsequently, he further divides positive liberty into three forms: Stoic inner freedom,
> rationalist self-realization freedom, and collectivist "higher self" freedom.

### Output

```
## Distinction Tracking Report

### Distinction Inventory

| ID | Concept A vs. B | Type | Exhaustive? | Mut. Exclusive? | Location |
|----|-----------------|------|-------------|-----------------|----------|
| D1 | Negative liberty / Positive liberty | Dichotomy | No† | Yes | §1 ¶1 |
| D2 | Inner freedom (Stoic) / Self-realization (rationalist) / Higher self (collectivist) | Trichotomy (nested under Positive liberty) | No† | Partial | §§3-5 |
| D3 | Formal liberty / Substantive liberty | Dichotomy (cross-cutting D1) | No | Yes | §6 |

† Berlin acknowledges that other variants of the concept of liberty may exist; the distinctions are not exhaustive.

### Function Analysis for Each Distinction

#### D1: Negative liberty / Positive liberty
- **Function**: Argument-space partitioning + Refutational tool
- **Role in the argument**: Berlin uses this distinction to warn that positive liberty is easily abused to suppress negative liberty.
  The essay's entire structure (first half describing positive liberty, second half describing negative liberty) corresponds to this distinction.
- **Consequence if this distinction were absent**: Berlin's core thesis would not stand — he needs this distinction to show
  how the same concept leads to diametrically opposed conclusions.

#### D2: Three sub-forms of positive liberty
- **Function**: Argument-space partitioning
- **Role in the argument**: To show the sliding path from "being one's own master" to "accepting the collective will."
  The first two forms (Stoic, rationalist) are conceptually legitimate;
  the third form (collectivist) is, in Berlin's view, a distortion of positive liberty — but this very distinction is what the essay argues for.
- **Consequence if this distinction were absent**: Unable to show the concrete path by which positive liberty is gradually twisted into an instrument of oppression.

### Consistency Check

| ID | Drift in later uses? | Specific issue |
|----|---------------------|----------------|
| D1 | **Partial drift** | In §2, "liberty" shifts from one pole of D1 toward an attitude toward the state — "negative" becomes "not interfered with by the state," "positive" becomes "attaining freedom through the state" — this is an extension of the original concept, but at the level of political practice rather than philosophical analysis. This shift is flagged as required by the argument, not a conceptual error. |
| D2 | No | D2 subclass boundaries remain consistent. |
| D3 | No | Consistent. |

### Distinction Network

```
D1 (Negative liberty / Positive liberty)
    │
    ├── contains ── D2 (Three sub-forms of positive liberty: Stoic / Rationalist / Collectivist)
    │
    └── parallel ── D3 (Formal liberty / Substantive liberty)
         Note: D3 cross-cuts D1 — both negative and positive liberty have formal/substantive dimensions
```

### Missing Distinctions

- **"Capacity for liberty vs. exercise of liberty"**: The text conflates "being capable of exercising liberty" with "actually exercising liberty."
  Berlin's argument shifts in §7 toward institutional protections, but does not distinguish whether the capacity for liberty is practically available.

### Overall Assessment

- Distinction reliance: **High** — Berlin's essay is driven almost entirely by distinction D1;
  without D1 there would be no essay.
- Key issue: Partial drift of D1 in §2 — sliding from a "philosophical conceptual distinction" toward a "political-practice distinction."
          This shift is required by the argument but increases conceptual ambiguity.
```
