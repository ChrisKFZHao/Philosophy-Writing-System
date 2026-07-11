# Modal Logic Primer

> This document provides foundational concepts in modal logic needed for philosophical argument analysis. Formal proofs are not included.

---

## 1. Modal Operators

### □ (Necessity)
- **Semantics**: true in all accessible possible worlds
- **Everyday expressions**: necessarily, must, cannot be otherwise, essentially
- **Philosophical sub-types**:
  - Logical necessity (true in all logically possible worlds)
  - Metaphysical necessity (true in all metaphysically possible worlds)
  - Nomological/physical necessity (true in all worlds consistent with the laws of physics)
  - Conceptual necessity (true under all conceptual frameworks -- analytic truths)

### ◇ (Possibility)
- **Semantics**: true in at least one accessible possible world
- **Everyday expressions**: possibly, can, perhaps, it could be that
- **Philosophical sub-types**: logical possibility, metaphysical possibility, nomological possibility, conceptual possibility

### ¬◇ (Impossibility)
- **Semantics**: there exists no accessible possible world in which the proposition is true
- **Everyday expressions**: impossible, inconceivable (note: inconceivability does not entail impossibility)

---

## 2. Modal Systems

### System K (Minimal Modal Logic)
```
□(P → Q) → (□P → □Q)   (Axiom K)
□P                     (Necessitation Rule: if ⊢P, then ⊢□P)
```

### System T
```
K + □P → P              (Axiom T: necessity implies actuality)
```
If something is true in all possible worlds, then it is true in the actual world.

### System S4
```
T + □P → □□P            (Axiom 4: necessity is iterable -- necessity is transparent)
```
If something is necessarily true, then it is necessarily necessarily true.

### System S5
```
S4 + ◇P → □◇P           (Axiom 5: possibility is necessary)
```
If something is possibly true, then it is necessarily possible. In S5, all worlds are mutually accessible.

### System B (Brouwer System)
```
T + P → □◇P             (Axiom B: actuality implies the necessity of possibility)
```
If something is true, then it is not possibly impossible -- roughly half of S5.

---

## 3. Key Distinctions

### De dicto vs. De re

| Reading  | Form      | Meaning                          | Example                                                        |
|----------|-----------|----------------------------------|----------------------------------------------------------------|
| De dicto | □∃x(Fx)  | Necessarily, there is some F     | In every possible world, there exists at least one first cause |
| De re    | ∃x□(Fx)  | There is some x that is necessarily F | There exists some particular entity that is a first cause in all possible worlds |

**Philosophical significance**:
- The de re reading is stronger -- it requires tracking the same entity across worlds, which introduces questions of **identity conditions** and **cross-world identification**.
- A classic error: treating a superficially de dicto modal claim as a de re argument.

### Modal Scope Ambiguity

"Possibly, a necessary being exists."

- Wide-scope reading: ◇∃x□(x=x) -- it is possible that there exists a necessary being
- Narrow-scope reading: ∃x◇□(x=x) -- there exists some entity that is possibly necessary

In philosophical writing, the placement of modal operators is often assumed implicitly rather than stated explicitly.

### Rigid Designation (Kripke)

- **Rigid designator**: a name that designates the same object in all possible worlds
- **Non-rigid designator**: a description (e.g., "the President of the United States in 2023") that designates different objects in different possible worlds
- **Modal consequence**: for rigid designators a and b, if a = b, then necessarily a = b (□(a = b))

---

## 4. Common Modal Fallacies

### M-1: Scope Confusion
Conflating the modal reading of "(A → (B → C))" with that of "(A → B) → C."

### M-2: Conceivability Leap
From conceivability → logical possibility → metaphysical possibility → nomological possibility. Each step requires independent justification.

### M-3: De dicto / De re Conflation
Treating de dicto necessity as de re necessity (or vice versa).

### M-4: Assuming S4/S5 by Default
Assuming without argument that System S4 or S5 holds -- but S5 is a very strong philosophical commitment. Chalmers (2002) observes that the necessity of S5 is "no free lunch."

### M-5: Conflating Necessity and Essentiality
Not all necessary properties are essential. Some are "necessary but non-essential" (e.g., "being necessarily self-identical").

### M-6: Possible Worlds as "Concrete" Entities
Mistaking "possible worlds" -- a useful heuristic device -- for genuinely existing concrete entities (Lewis's modal realism vs. the numerous alternative stances).

---

## 5. Analytic Application

When analyzing a modal argument, ask of each modal claim:

1. What kind of necessity/possibility is being invoked? (logical, metaphysical, nomological, conceptual)
2. Is the reading de dicto or de re?
3. Which modal system is implicitly assumed? (K? S4? S5?)
4. What is the accessibility relation?
5. Does the argument involve a conceivability → possibility leap?

---

*Adapted from: Hughes & Cresswell (1996); Kripke (1980); Chalmers (2002); Sider (2010)*
