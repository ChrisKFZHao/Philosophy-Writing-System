# Mereological Argument

## Form

### Core Structure — The Special Composition Question (SCQ)

```
[1] Under what conditions do the xs compose a y?
    (The Special Composition Question — van Inwagen)
[2] Candidate answers:
    a. Universalism: For any xs, there exists a y such that the xs compose y (always)
    b. Nihilism: For no xs (except singletons) does there exist a y such that the xs
       compose y (never)
    c. Moderate answers: The xs compose y iff condition C is satisfied (sometimes)
    d. Organicism (van Inwagen): The xs compose y iff the activity of the xs
       constitutes a life
[3] Argument for position P — three canonical forms:
```

### Argument for Universalism (Lewis/Van Inwagen's Rejection of Restrictivism)

```
[1] If composition is restricted (not universal), there must be a non-arbitrary
    condition C that determines when composition occurs
[2] Any such condition C involves vagueness in borderline cases (when does a collection
    of simples gradually brought together begin to compose?)
[3] Vague composition entails vague existence (whether y exists would be indeterminate)
[4] Vague existence is impossible (existence is precise; there is no ontological
    vagueness)
∴ [5] Composition is not restricted (reject restrictivism)
    [6] Composition is universal
```

### Argument for Nihilism (Dorr/Sider)

```
[1] If composite objects exist, then there must be a non-arbitrary answer to the
    Special Composition Question
[2] All proposed answers to the SCQ (organicism, universalism, moderate views) face
    decisive objections
[3] Universalism entails an explosion of gerrymandered, arbitrary objects (trout-turkeys)
    that are implausible ontological commitments
[4] Organicism entails that most ordinary objects (tables, chairs, planets) do not exist
    — a radical revision of common sense
∴ [5] The only defensible answer to the SCQ is nihilism: nothing composes anything
    (except perhaps simples trivially composing themselves)
```

### Argument for Organicism (van Inwagen)

```
[1] Common sense affirms the existence of composite objects (tables, persons, planets)
[2] Common sense also denies the existence of arbitrary mereological sums (the fusion of
    my left ear and the Eiffel Tower)
[3] The only non-arbitrary, principled answer to the SCQ compatible with (1) and (2)
    is organicism: composition occurs only when the activity of the xs constitutes a life
[4] Nihilism and universalism are both incompatible with (1) and (2)
∴ [5] Organicism is the correct answer to the SCQ
```

## Formal Mereological Axioms

```
Reflexivity:   ∀x P(x, x)           (Everything is part of itself)
Antisymmetry:  ∀x∀y [(P(x,y) ∧ P(y,x)) → x = y]  (No two distinct things are parts of each other)
Transitivity:  ∀x∀y∀z [(P(x,y) ∧ P(y,z)) → P(x,z)]   (Parts of parts are parts)
```

From these, supplementary principles are defined:

```
Proper Parthood:  PP(x,y) =df P(x,y) ∧ x ≠ y
Overlap:          O(x,y)  =df ∃z (P(z,x) ∧ P(z,y))
Fusion:           F(t, φ) =df ∀y (O(y,t) ↔ ∃x (φ(x) ∧ O(y,x)))
```

## Distinctive Features

1. **The SCQ as a metaphysical forcing function**: The Special Composition Question serves as a focal point — it forces every metaphysical position to take a stand on when composition occurs. Unlike many philosophical questions, the SCQ has a small, well-defined answer space (universalism, nihilism, organicism, restrictivism) that structures debate.

2. **The vagueness argument as a methodological weapon**: Sider and Lewis use the impossibility of vague existence to argue *for* unrestricted composition and *against* restrictivism. This argumentative strategy — leveraging the precision of existence against moderate metaphysics — recurs in debates about identity, persistence, and ontological commitment.

3. **The common-sense constraint**: Van Inwagen's argument explicitly appeals to common-sense intuitions about composite objects as a constraint on theory choice. Both universalism (too many objects) and nihilism (too few) violate common sense; organicism alone preserves it — though at the cost of denying that tables and chairs literally exist.

4. **Mereology as a formal tool**: Mereological arguments are distinctive in employing a formal axiomatic system (classical extensional mereology). Arguments are evaluated not only for philosophical plausibility but also for consistency with the axioms.

## Evaluation Criteria

1. **The force of the vagueness argument**: Does vague composition genuinely entail vague existence? If composition is a human-constructed category rather than a joint-carving one, vagueness may be tolerable (the "semantic indecision" response).

2. **The common-sense constraint**: How much weight should common-sense beliefs about composition carry? Van Inwagen's own view violates common sense in denying the existence of tables and chairs — does this undermine his appeal to common sense against nihilism?

3. **The arbitrariness objection**: Universalism generates gerrymandered objects (trout-turkeys, incars). Are these genuine ontological commitments or harmless byproducts of a simple theory? Universalists argue the latter.

4. **Gunky and junky worlds**: Does the favored answer to the SCQ apply to worlds that are gunky (every part has proper parts) or junky (every object is a proper part of something)? Some answers to the SCQ are incompatible with such worlds.

## Reconstruction Notes

- When reconstructing a mereological argument, first identify **which answer to the SCQ** the author defends, and then identify **the argumentative strategy**: positive argument for their view, or eliminative argument against alternatives.
- The vagueness argument requires special care: the premise `[IP] Vague composition entails vague existence` is often contested. Reconstruct it explicitly and note whether the author provides independent support.
- Distinguish **ontological** claims (what exists) from **semantic** claims (what "exists," "object," and "compose" mean). Some restrictivists deflect the vagueness argument by noting that semantic indecision does not entail ontological vagueness.
- When formal mereological axioms are invoked, note whether the argument assumes **classical extensional mereology** (CEM) or some non-classical mereology. The axioms of CEM are substantive metaphysical commitments.

## References

- van Inwagen, Peter. *Material Beings*. Cornell University Press, 1990.
- Lewis, David. *Parts of Classes*. Blackwell, 1991.
- Lewis, David. *On the Plurality of Worlds*. Blackwell, 1986. (See section on unrestricted composition)
- Sider, Theodore. *Four-Dimensionalism: An Ontology of Persistence and Time*. Oxford University Press, 2001.
- Sider, Theodore. "Against Vague and Unnatural Existence: Reply to Liebesman and Eklund." *Nous*, 2014.
- Dorr, Cian. "What We Disagree About When We Disagree About Ontology." In *Fictionalism in Metaphysics*, 2005.
- Varzi, Achille. "Mereology." *Stanford Encyclopedia of Philosophy*. 2019.
