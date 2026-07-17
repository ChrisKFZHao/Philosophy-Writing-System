# Leibniz's Law (Indiscernibility of Identicals)

## Form

### Core Structure — Indiscernibility of Identicals

```
[1] a = b               (a is identical to b)
[2] F(a)                (a has property F)
∴ [3] F(b)              (b has property F)
```

In formal notation: `(a = b) → ∀F(F(a) ↔ F(b))`

### Contrapositive — Discernibility of Non-Identicals (Identity of Indiscernibles)

```
[1] F(a) ∧ ¬F(b)        (a and b differ in some property)
∴ [2] a ≠ b              (a and b are distinct)
```

In formal notation: `∃F(F(a) ∧ ¬F(b)) → (a ≠ b)`

The two directions together yield the full Leibnizian principle:

> **`a = b ↔ ∀F(F(a) ↔ F(b))`**

Identity of Indiscernibles (right-to-left) is more controversial than Indiscernibility of Identicals (left-to-right) and is typically treated as a substantive metaphysical thesis rather than a logical truth.

## Distinctive Features in Philosophical Analysis

1. **Second-order quantification**: The principle quantifies over properties, not merely individuals. This makes it a powerful but also contested tool — its application depends on what counts as a genuine property.

2. **Substitutivity salva veritate**: Leibniz's Law licenses the substitution of co-referring terms in any context without change of truth-value. Contexts that resist this (so-called "opaque" or "intensional" contexts) are of central importance in philosophy of language and mind.

3. **Formal rigor with substantive import**: The argument appears purely logical, but its application turns on what counts as a "property" — e.g., do modal properties, temporal properties, or intentional properties count?

## Variants and Extensions

### Modal Variant (Necessity of Identity)

```
[1] a = b               (a is identical to b)
[2] □(a = a)            (Necessarily, a is identical to a)
[3] □(a = b)            (From [1] and [2], substituting b for the second occurrence of a in [2])
∴ [4] □(a = b)          (If a = b, then necessarily a = b)
```

This relies on the fact that `□(x = x)` is a property of `a` that `b` must share if `a = b`. Kripke (1971/1980) used this to argue that true identity statements between rigid designators are necessary truths.

### The Problem of Opaque Contexts

```
[1] Lois Lane believes Clark Kent is a reporter
[2] Clark Kent = Superman
[3] Lois Lane believes Superman is a reporter  ← Does NOT follow
```

Belief contexts (and other propositional-attitude contexts) resist substitution. The standard diagnosis: `Lois Lane believes x is a reporter` is not a genuine property of individuals — it is an intensional context that Leibniz's Law does not govern. This is the core of Frege's puzzle about cognitive significance.

### The Masked Man Fallacy

```
[1] I know that my father is my father          (trivially true)
[2] My father = the masked man                   (true, but unknown to me)
[3] I know that the masked man is my father      ← Does NOT follow
```

This is not a counterexample to Leibniz's Law; it is a misuse. Knowledge contexts are opaque. The fallacy consists in treating them as transparent and applying substitutivity where it does not apply.

## Evaluation Criteria

1. **Is the context transparent?** — Substitutivity only holds in extensional (transparent) contexts. Before applying Leibniz's Law, confirm that the property `F` in question is a genuine extensional property.

2. **Is the predication genuine?** — Some apparent properties are not real properties (e.g., "being believed by Lois to be a reporter" is arguably not a monadic property of the individual).

3. **For identity of indiscernibles: are all properties shared?** — The right-to-left direction requires that a and b share *all* properties, including relational and modal ones. This is a stringent condition rarely satisfied in practice.

4. **Temporal and modal sensitivity** — Properties may hold at some times or in some worlds but not others. The principle must be indexed to worlds and times: `(a = b) → ∀F□(F(a) ↔ F(b))` for modal contexts.

## Famous Cases

| Argument | Proponent | Application of Leibniz's Law |
|----------|-----------|------------------------------|
| Necessity of Identity | Kripke (1971) | `a = b → □(a = b)` via modal property substitution |
| Mind-Body Dualism (Zombie Argument) | Chalmers (1996) | I am conscious; my physical duplicate is not; therefore I ≠ my physical duplicate |
| The Paradox of Increase | Gibbard (1975) | Lump of clay has different temporal properties from the statue; therefore Lump ≠ Statue |
| The Guise of the Good | Various | Desiring F is not identical to believing F is good, because they differ in functional role |
| Material Constitution | Various | Statue = clay on Tuesday; clay exists before Tuesday; therefore by Leibniz's Law, statue existed before Tuesday (problematic) |

## Reconstruction Notes

- When reconstructing arguments that rely on Leibniz's Law, explicitly annotate whether it is the **indiscernibility direction** (`= → ∀F`) or the **identity-of-indiscernibles direction** (`∀F → =`) being used — the latter is far more contentious.
- Mark opaque contexts explicitly as `[OC]` — contexts where substitution is blocked.
- The modal variant requires an auxiliary premise: `□(x = x)` (the necessity of self-identity).
- In contemporary metaphysics, Leibniz's Law is often treated as **axiomatic** — it is not argued *for* but *applied*, with the dispute shifting to whether a given context licenses the application.

## References

- Leibniz, G.W. *Discourse on Metaphysics*. 1686.
- Kripke, Saul. "Identity and Necessity." 1971; *Naming and Necessity*. 1980.
- Wiggins, David. *Sameness and Substance Renewed*. 2001.
- Frege, Gottlob. "On Sense and Reference." 1892.
- Sider, Theodore. *Logic for Philosophy*. 2010, Ch. 5.
- Forrest, Peter. "The Identity of Indiscernibles." *Stanford Encyclopedia of Philosophy*. 2010.
