# Sorites Paradox

## Form

### Core Structure — Classical Sorites

```
[1] Base premise: 1 grain of sand is not a heap
[2] Tolerance premise: If n grains are not a heap, then n+1 grains are not a heap
[3] By repeated application of modus ponens: for any n, n grains are not a heap
∴ [4] 10,000 grains are not a heap
    But obviously 10,000 grains are a heap → contradiction
```

### Generalized Sorites Structure

```
[1] Base case: Fa              (a clearly does not satisfy the vague predicate F)
[2] Tolerance: ∀n(Faₙ → Faₙ₊₁) (If aₙ is not F, then aₙ₊₁ is not F)
[3] Sorites series: a₁, a₂, ..., aₖ (a gradual series from clearly-not-F to clearly-F)
[4] Classical logic: first-order logic + modus ponens
∴ [5] Faₖ ∧ ¬Faₖ             (Contradiction)
```

### Observational Sorites

```
[1] Objects differing only imperceptibly in a relevant respect are indistinguishable
    with respect to the predicate
[2] A series of objects differing only imperceptibly from clear case to clear
    counter-case can be constructed
∴ [3] The predicate must either apply to all or none → contradiction with observation
```

## Distinctive Features

1. **The tolerance principle**: The paradox turns on the intuition that vague predicates are tolerant of small changes — if x and y differ only marginally along the relevant dimension, they cannot differ in the application of the predicate. This intuition conflicts with classical logic.

2. **Inductive structure**: Unlike most philosophical paradoxes which derive a contradiction from a small set of premises, the sorites derives a contradiction through an indefinitely long chain of conditionals. The length of the chain is essential — a two-step sorites is not compelling.

3. **Ubiquity of vague predicates**: Nearly all ordinary predicates are vague (heap, bald, tall, red, child, etc.). The paradox is therefore not an isolated puzzle but a challenge to the very possibility of meaningful discourse using ordinary language.

4. **Applied sorites**: The paradox extends beyond simple predicates to philosophically central concepts — personal identity (Parfit's spectrum), composition (when does a collection compose an object?), free will (van Inwagen's consequence argument + vague boundary).

## Solutions

| Approach | Key Proponent | Core Claim | Cost |
|----------|---------------|------------|------|
| Epistemicism | Williamson (1994) | There is a sharp cutoff; we cannot know where it is | Bivalence preserved; sharp boundary posited |
| Supervaluationism | Fine (1975), Keefe (2000) | Vague predicates are semantically incomplete; truth is super-truth across precisifications | Classical logic largely preserved; higher-order vagueness |
| Many-Valued Logic | Lukasiewicz, Zadeh | Truth comes in degrees; the conditional is not fully true | Abandons bivalence; degree-theoretic semantics required |
| Contextualism | Raffman (1994) | The extension of vague predicates shifts with context | Context-dependence does all work |
| Nihilism | Unger (1979) | Nothing satisfies vague predicates; heaps do not exist | Radically revisionary; denies ordinary belief |
| Dialetheism | Priest | The contradiction is true: the last non-heap is also a heap | Accepts true contradictions |

## Evaluation Criteria

1. **Preservation of classical logic**: Solutions that abandon bivalence, excluded middle, or classical validity face the burden of providing a replacement logic.

2. **Phenomenology of vagueness**: Does the solution respect the *experience* of vagueness — the genuine uncertainty about borderline cases, the absence of detectable sharp boundaries?

3. **Higher-order vagueness**: Even if a solution handles first-order vagueness, does it address the problem that the boundary between clear cases and borderline cases is itself vague? Many solutions generate a higher-order sorites.

4. **Scope**: Does the solution handle all vague predicates uniformly, or does it require piecemeal treatment?

## Reconstruction Notes

- The most critical element in reconstructing a sorites is identifying the **tolerance principle** — the conditional `Faₙ → Faₙ₊₁` — and assessing its plausibility independent of the paradox.
- Distinguish the **logical** structure (which premises generate the contradiction) from the **philosophical** structure (which premise is rejected, and why).
- When the sorites is applied to a philosophical problem (e.g., personal identity), reconstruct how the tolerance principle maps onto the target domain. The mapping is often controversial.
- Note whether the author accepts the **inductive** form (n applications of universal instantiation + modus ponens) or the **conditional** form (a single long conditional). Logical systems that restrict induction for vague predicates block the former but not necessarily the latter.

## References

- Williamson, Timothy. *Vagueness*. Routledge, 1994.
- Keefe, Rosanna, and Peter Smith, eds. *Vagueness: A Reader*. MIT Press, 1996.
- Keefe, Rosanna. *Theories of Vagueness*. Cambridge University Press, 2000.
- Hyde, Dominic. "Sorites Paradox." *Stanford Encyclopedia of Philosophy*. 2023.
- Sorensen, Roy. "Vagueness." *Stanford Encyclopedia of Philosophy*. 2022.
- Unger, Peter. "There Are No Ordinary Things." *Synthese*, 1979.
- Fine, Kit. "Vagueness, Truth and Logic." *Synthese*, 1975.
- Raffman, Diana. "Vagueness Without Paradox." *Philosophical Review*, 1994.
