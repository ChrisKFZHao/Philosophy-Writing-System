# Counterexample Generation and Evaluation — examples (conditional reference for method.argument.counterexample)

> Loaded only when the consuming mode's live ambiguity or the user's explicit request requires it; never loaded by default with the method file.

# Counterexample Construction Examples

---

## Example 1: Gettier-Style Counterexample — Against the JTB Analysis of Knowledge

### Input

```
[P1] Knowledge = Justified True Belief (JTB analysis)
[P2] Smith believes "Jones will get the job"
[P3] Smith has justified evidence: "the boss said so" and "Jones has ten coins in his pocket"
[P4] In fact, Smith gets the job (not Jones)
───────
[C]  ∴ Smith does not know "the person who will get the job has ten coins in his pocket"
```

### Output

```
## Counterexample 1: Gettier's Ten-Coins Case

- **Type**: Thought Experiment Counterexample
- **Target**: [P1] — the JTB analysis of knowledge
- **Scenario Description**:
  Smith and Jones are both applying for the same job. Smith has strong evidence to believe:
  (a) Jones will get the job (the boss said so), and
  (b) Jones has ten coins in his pocket (Smith counted them).
  Therefore, Smith justifiably believes: "The person who will get the job has ten coins in his pocket."

  But in fact, the boss changes his mind: Smith himself gets the job. And — crucially —
  Smith himself also happens to have ten coins in his pocket (unbeknownst to him).

  The proposition "The person who will get the job has ten coins in his pocket" is **true** (Smith himself has ten coins),
  and Smith also **justifiably believes** it (based on the evidence he has about Jones),
  but intuitively: Smith does not know this proposition. His justified true belief is **lucky** — he does not believe it for the reasons that make it true.

- **Intuitive Force**: Strong (this case is universally acknowledged to have overturned the JTB analysis)
- **Conceivability**: High
- **Isolation**: Good
- **Independence**: Yes

- **Anticipated Rebuttal**: One might say "the ten-coins case is too peculiar to demonstrate a problem with the general conceptual analysis"
- **Preliminary Assessment**: This response is not a challenge to the counterexample itself but a methodological objection. If one accepts "cases as an explanatory method,"
         then this counterexample is fatal — a case that satisfies all definitional conditions is intuitively rejected.
```
