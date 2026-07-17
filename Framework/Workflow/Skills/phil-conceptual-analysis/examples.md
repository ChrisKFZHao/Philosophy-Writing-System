# Conceptual Analysis Examples

> This document demonstrates the practical application of conceptual analysis across different philosophical domains. Each example shows the complete input-to-output process.

---

## Example 1: Classical Conceptual Analysis — "Knowledge" as "Justified True Belief"
### Domain: Epistemology

### Input

> Socrates asks Theaetetus: "What is knowledge?"
> Theaetetus answers: Knowledge is justified true belief.

This classic candidate definition comes from Plato's *Theaetetus*. Let us test it using the method of conceptual analysis.

### Output

```
## Conceptual Analysis Report

### Basic Information
- **Concept**: Knowledge
- **Domain**: Epistemology
- **Analysis Version**: v1.0

### Candidate Definitions

D1: Knowledge = df. justified true belief (propositional knowledge)
    - Source: Plato, *Theaetetus*; the starting point challenged by Gettier 1963
    - Constituent elements:
      (a) Belief condition: S believes that p
      (b) Truth condition: p is true
      (c) Justification condition: S has justified grounds for believing that p

### Necessary Conditions

NC1: S believes that p — Test: passed ✅
      → Without belief there is no knowledge (you cannot know what you do not believe)
NC2: p is true — Test: passed ✅
      → A false belief does not count as knowledge (even if it appears to be knowledge)
NC3: S has justified grounds for believing that p — Test: disputed ⚠️
      → Gettier cases show that justified true belief may still not be knowledge

### Sufficiency Test

SC: (a) ∧ (b) ∧ (c) jointly constitute sufficient conditions — Test: failed ❌
      Counterexample: In the cases constructed by Gettier (1963), someone holds a
      justified true belief, but the belief is true due to luck (coincidence) —
      intuitively we would not call this knowledge.

### Case Testing

#### Positive Cases
PC1: I see rain outside the window, I believe "it is raining," it is indeed raining,
      and I have visual evidence. → D1 covers this case; this is a typical instance of knowledge.

#### Borderline Cases
BC1: I intuitively believe that 2+2=4, but do I need "justification" — is this called knowledge?
      → Fuzzy area revealed: the "justification" condition for a priori knowledge differs from
        that for empirical knowledge.
BC2: Does a computer's "knowledge" count as knowledge? Computers have no belief states.
      → Fuzzy area revealed: is the concept restricted to human/cognitive agents?

#### Counterexamples
CC1: Gettier case (Gettier, 1963)
      S sees a box containing a doctoral diploma in Jones's office, and therefore believes
      "someone in the office has a doctorate." In fact, Jones is not there, but another person,
      Smith — who has no diploma — is in the office. Jones's box does contain the diploma — so
      S's belief is true and justified, but is this knowledge?
      Impact: D1 is falsified — justified true belief is not sufficient for knowledge.

CC2: Fake barn country (Goldman, 1976)
      S drives through a countryside full of fake barns and happens to see the one real barn.
      S believes "this is a barn," and indeed it is a barn. But is this knowledge?
      Impact: Further challenges D1, showing that knowledge requires a causal/reliable connection.

### Distinction Mapping

| Adjacent Concept | Commonality | Key Difference | Boundary Type |
|-----------------|-------------|----------------|---------------|
| True belief | Belief that is true | Lacks the justification condition | Kind (without justification it is not knowledge) |
| Wisdom | Both involve cognitive achievement | Wisdom requires deeper understanding and judgment | Kind (they are not on the same level) |
| Understanding | Knowledge is a necessary component of understanding | Understanding requires systematic grasp | Degree / Kind |

### Conceptual Structure Type

- Determination: Classical concept (but the classical definition faces severe challenges)
- Rationale: The concept of knowledge in ordinary use exhibits the form of a classical concept —
  people tend to think that knowledge has clear boundaries — but the Gettier problem and subsequent
  literature demonstrate that its defining conditions are extraordinarily difficult to complete.

### Dimensional Analysis

| Dimension | Role in the Concept | Does variation change application? |
|-----------|---------------------|-------------------------------------|
| Propositional knowledge vs. knowledge by acquaintance | Two types of knowledge | Yes ("knowing the capital of Quebec" vs. "knowing the taste of Quebec") |
| A priori vs. empirical | Different sources of justification | No (both are knowledge) |
| Individual vs. collective | The subject of knowledge | Yes (whether collective knowledge is genuine knowledge is disputed) |
| Absolute vs. gradable | Whether knowledge's boundaries are sharp or fuzzy | Disputed (is knowledge gradable?) |

### Reconstruction Notes and Technical Details

- This analysis is based on post-Gettier epistemological discussion. D1 has been widely abandoned;
  alternative theories include:
  - Goldman: causal/reliabilist epistemology
  - Nozick: sensitivity condition
  - Sosa: virtue epistemology
  - Williamson: knowledge first
- The value of this analysis lies in demonstrating the method of classical conceptual analysis —
  find a candidate definition → extract necessary/sufficient conditions → construct counterexample tests
```

---

## Example 2: Cluster Concept — The Concept of "Game"
### Domain: Philosophy of Language / Metaphysics

### Input

> Wittgenstein, in *Philosophical Investigations*, argues that "game" has no unified essential definition but is instead connected by "family resemblances." He challenges the basic assumption of classical conceptual analysis.

### Output

```
## Conceptual Analysis Report

### Basic Information
- **Concept**: Game (ordinary concept)
- **Domain**: Philosophy of language, metaphilosophy
- **Analysis Version**: v1.0

### Candidate Definitions

D1 (classical presupposition): A game should be defined by a set of necessary and sufficient conditions.
D2 (Wittgensteinian): A game is a family resemblance concept; no single feature runs through all games.

### Necessary Condition Tests

Candidate necessary conditions tested against all instances of "game":
- NC1: Having rules — Test: disputed ⚠️
  → Most games have rules, but does "free play" (e.g., a child playing in the water at the beach)
    count as a game?
- NC2: Having winners and losers — Test: failed ❌
  → Solitaire puzzles or playing in the sand have no winners or losers
- NC3: Entertainment value — Test: disputed ⚠️
  → A professional chess player's match is "work" not entertainment, yet it is still a game
- NC4: Voluntary participation — Test: disputed ⚠️
  → Forcing a child to play piano is not a game, but is it a "game" of following musical rules?

### Sufficiency Test

SC: (has rules ∧ has winners/losers ∧ entertainment value ∧ voluntary participation) — Test: failed ❌
  → This condition set excludes many activities we clearly call "games" (e.g., solitaire puzzles),
    while also including activities we clearly do not call games (e.g., court proceedings have rules
    and winners/losers).
  → No set of conditions can simultaneously cover all games and exclude all non-games.

### Case Testing

#### Positive Cases
PC1: Chess (clear rules, winners/losers, requires strategy)
PC2: Hide-and-seek (simple rules, entertainment, children's activity)
PC3: Video games (complex rules, winners/losers, voluntary participation)
      → These cases are all clearly "games," but what features do they share?

#### Counterexamples (targeting the classical definition)
CC1: Is professional boxing a "sport" or a "game"? It has rules, winners/losers, but involves
      serious harm. → If boxing is a game, then activities involving the possibility of harm
      can be considered games.
CC2: Children running and rolling freely on the grass — no rules, no winners/losers, but joyful.
      → If this is a game, then the absence of rules does not preclude an activity from being a game.
CC3: Mathematical games (e.g., Sudoku) — entertainment or intellectual training?
      → If this is a game, then "serious purpose" does not exclude the nature of game-playing.

### Distinction Mapping

| Adjacent Concept | Commonality | Key Difference | Boundary Type |
|-----------------|-------------|----------------|---------------|
| Sport | Rules, winners/losers, physical participation | Sport has standardized rules and competitive institutions | Degree (many activities are both games and sports) |
| Art | Creativity, self-expression | Art does not require a rule system | Kind (but "game-like" performance art has overlap) |
| Ritual | Rule-governed, fixed procedures | Ritual has serious/sacred purposes | Kind (but serious forms of "game" approach ritual) |
| Work | Occupies time and energy | Work has an external purpose (income/output) | Kind (but professional gamers' work is playing games) |

### Conceptual Structure Type

- Determination: **Cluster concept** (family resemblance)
- Rationale: No single set of features is shared by all instances of games. Games are connected
  by an overlapping network of similarities (e.g., having rules, having winners/losers,
  entertainment value, voluntariness, competitiveness, simulation, etc.) — each game possesses
  some of these features, but no feature is common to all games.
  This is the core of Wittgenstein's famous "family resemblance" argument.

### Dimensional Analysis

| Dimension | Role in the Concept | Does variation change application? |
|-----------|---------------------|-------------------------------------|
| Entertainment ← → Professionalism | Degree of seriousness of the game | Yes (professional games remain games, but approach the boundary of work) |
| Rigid rules ← → Free play | Degree of structure | Yes (extreme free play has disputed boundaries) |
| Competitiveness ← → Cooperativeness | Nature of purpose | No (both competitive and cooperative games are games) |
| Physical ← → Intellectual | Mode of participation | No (e.g., both chess and soccer are games) |

### Reconstruction Notes and Technical Details

- Wittgenstein's family resemblance argument is used as an argument against "essentialist" concepts,
  but its scope of application is disputed.
- Subsequent discussions of cluster concepts in conceptual analysis include:
  - Needham (1975): Do family resemblance concepts genuinely exist?
  - Lakoff (1987): Empirical research on prototype theory
  - Putnam (1975): The concept of "stereotype" in semantics
```

---

## Example 3: Distinction Mapping — "Justice" vs. "Fairness"
### Domain: Political Philosophy / Ethics

### Input

> In political philosophy discussions, it is often said that "this is unfair but may be just" or
> "this appears fair but is unjust." What is the precise relationship between these two concepts?
> Are they interchangeable, or do they carry out different philosophical work?

### Output

```
## Conceptual Analysis Report

### Basic Information
- **Concept**: Fairness and Justice
- **Domain**: Political Philosophy / Ethics
- **Analysis Version**: v1.0
- **Analysis Type**: Distinction mapping (focus on Section 6 Distinction Mapping)

### Candidate Definitions

D1 (Justice): The basic structure of society, in distributing rights and duties, gives each person
    what they deserve. — Different theories of justice offer different accounts of "desert"
    (Rawls: difference principle; Nozick: entitlements; utilitarianism: maximization)
D2 (Fairness): Procedural, impartial treatment, especially at the level of rule enforcement.
    — Fairness is typically associated with procedural impartiality, not substantive distributive outcomes.

### Necessary Conditions

Justice:
NC1: Concerned with "desert" — Test: passed ✅
NC2: Concerned with the basic structure of society — Test: passed ✅
NC3: Can permit inequality (as long as it conforms to some principle of justice) — Test: disputed ⚠️

Fairness:
NC1: Procedural neutrality — Test: passed ✅
NC2: Application of the same standard to all persons — Test: passed ✅
NC3: Equality of outcome is not a necessary condition for fairness — Test: passed (but highly disputed)

### Sufficiency Test

Justice:
SC: Distribution according to desert — Test: failed ❌
  → "What is desert" is itself the most contested question.
  → Different theories of justice yield completely opposed sets of sufficient conditions.

### Distinction Mapping
                                                  (CORE DISTINCTION)
| Concept | Commonality | Key Difference | Boundary Type |
|---------|-------------|----------------|---------------|
| Justice | Both involve "giving each their due" | Justice concerns **substantive outcomes** — whether society has given each their due; fairness concerns **procedural impartiality** | Kind |
| Fairness | Both require impartiality | Fairness is **procedural** — whether rules are applied equally; justice is **substantive** — whether the rules themselves are legitimate | Kind |

### Conceptual Structure Type

- Determination: Classical concepts (each individually has a classical structure, but the relation
  between them is distinction-based)
- Rationale: Justice and fairness each have a relatively clear set of necessary conditions. The
  dispute is not over their individual definitions but over whether they point to different
  normative dimensions. Rawls's "justice as fairness" attempts to unify the two, but critics
  hold that justice > fairness or that fairness ≠ justice.

### Dimensional Analysis (Key Dimension: Procedural vs. Substantive)

This is the most important dimensional axis:
- Pure procedural justice: If the procedure is correct, the outcome is just (e.g., gambling)
- Perfect procedural justice: There is an independent standard of right outcome, and the procedure
  can realize it (e.g., cutting a cake)
- Imperfect procedural justice: There is an independent standard, but the procedure cannot perfectly
  realize it (e.g., criminal trials)

The core insight of the distinction map: when a text switches between "justice" and "fairness,"
observe whether the context of use is a procedural context or a substantive context — this
typically explains why the author uses one term rather than the other.

### Reconstruction Notes and Technical Details

- Rawls (1971) defines justice as fairness, unifying the two within his theory — but in everyday
  and political discussion the two are often kept separate.
- Sen (2009) *The Idea of Justice* criticizes Rawls's institution-focused approach and advocates
  a comparative conception of justice — this poses new challenges for distinguishing "justice" from "fairness."
```

---

## Example 4: Conceptual Engineering — "Race" as a Social Construction
### Domain: Social Philosophy / Metaphysics

### Input

> Haslanger (2000) "Gender and Race: (What) Are They? (What) Do We Want Them to Be?"
> She argues that we should not only analyze how "race" is used in everyday life (descriptive
> analysis), but also consider how we should use this concept to serve social justice
> (conceptual engineering / ameliorative analysis).

### Output

```
## Conceptual Analysis Report (Conceptual Engineering Mode)

### Basic Information
- **Concept**: Race
- **Domain**: Social Philosophy / Metaphysics
- **Analysis Version**: v1.0
- **Analysis Type**: Conceptual engineering (ameliorative analysis / revisionary analysis)

### Candidate Definitions

D1 (Everyday essentialism): Race is a naturally occurring group classification of people based on
    biological inheritance.
    — Source: ordinary usage + 19th-century anthropology
    — Problem: modern genetics has refuted the view of "race as biological essence"

D2 (Social constructionism): Race is a social classification that has been "reified" through social
    institutions and historical practices.
    — Source: Omi & Winant (1994) racial formation theory
    — Feature: race is real (it has social consequences), but not biologically real

D3 (Haslanger's ameliorative definition): A group G is a race if and only if:
    (i) Group members are marked as having certain physical/appearance features (this is observed);
    (ii) This marking systematically places them in a position of subordination or privilege
         socioeconomically;
    (iii) This subordination/privilege is partly reinforced by the way group members are "observed"
          on a daily basis.

### Necessary Conditions

NC1: There exist physical/appearance features that are systematically "marked" — Passed ✅
NC2: This marking systematically distributes subordination or privilege — Passed ✅
NC3: This process does not depend entirely on individual choice (it is socially structural) — Passed ✅

### Sufficiency Test

D3 as a three-condition set — Test: passed ✅
      → Haslanger's definition accurately covers core instances of race (e.g., Black, White in the
        U.S. historical context) and excludes non-racial group classifications (e.g., "vegetarians"
        do not satisfy condition iii).

### Distinction Mapping

| Adjacent Concept | Key Difference |
|-----------------|----------------|
| Ethnicity | Ethnicity is based on shared cultural/linguistic/historical traditions; it need not depend on physical marking |
| Class | Class is based on economic position, not physical appearance marking |
| Skin color | Skin color is one dimension of racial marking, but is not race itself |

### Conceptual Structure Type

- Determination: Stipulative concept, but with a strong essentialist flavor
- Rationale: Haslanger's D3 is a deliberately engineered concept — it is not pure everyday
  description but introduces a new definition to achieve a theoretical purpose (diagnosing social
  injustice). However, its structure remains that of a classical concept (conjunction of three
  necessary conditions), so it can be regarded as a "revisionary classical concept."

### Conceptual Engineering Analysis

Why undertake conceptual engineering?
  E1: The everyday concept (D1) is scientifically false and socially harmful
  E2: The social constructionist analysis (D2) is correct but insufficiently precise — it does
      not clearly distinguish race from other social classifications
  E3: D3 both preserves the social utility of the concept of race (we can continue to discuss
      racial injustice) and rejects false ontological commitments (race is not a biological essence)

### Reconstruction Notes and Technical Details

- This example demonstrates the important distinction between "descriptive conceptual analysis"
  and "conceptual engineering."
- Not all conceptual analysis should involve conceptual engineering — most everyday analysis need
  only clarify existing usage. Conceptual engineering is appropriate only when:
  (1) The existing concept has theoretical defects (e.g., based on outdated scientific assumptions), or
  (2) The existing concept has practical harms (e.g., reinforcing social injustice).
```

---

## Example 5: Dimensional Analysis — The Negative and Positive Dimensions of "Freedom"
### Domain: Political Philosophy

### Input

> Berlin (1958) proposes "Two Concepts of Liberty": negative liberty (freedom from interference
> by others) and positive liberty (freedom to be one's own master). He wishes to distinguish them,
> not to merge them or choose between them.

### Output

```
## Conceptual Analysis Report

### Basic Information
- **Concept**: Freedom / Liberty
- **Domain**: Political Philosophy
- **Analysis Version**: v1.0
- **Analysis Type**: Dimensional analysis (dimensional analysis is the focus)

### Candidate Definitions

D1 (Negative freedom): Freedom is a sphere of action free from intentional interference by others.
    Source: Berlin (1958); Hobbes; Mill
D2 (Positive freedom): Freedom is the capacity for self-mastery, to be one's own master.
    Source: Berlin (1958); Rousseau; Kant; Marx

### Distinction Mapping

| Conceptual Pair | Core Tension | Boundary Type |
|----------------|-------------|---------------|
| Negative freedom | Concerned with "freedom from what" | The two are not mutually exclusive concepts, but two different dimensions of the concept of freedom |
| Positive freedom | Concerned with "freedom to do what" | (Berlin holds they can conflict; other theorists hold they are complementary) |

### Structural Type

- Determination: Decompositional concept — freedom is composed of more basic dimensions
- Rationale: The concept of freedom itself may be a cluster concept, but Berlin's analytical path
  decomposes freedom into two distinct sub-concepts (negative/positive), each of which individually
  has a classical structure.

### Dimensional Analysis (Focus of This Analysis — The Dimensional Space of Freedom)

Dimension 1: External interference ← → Internal autonomy
  - Negative freedom (freedom from X) vs. Positive freedom (freedom to do X)
  - This is the most famous dimensional axis

Dimension 2: Individual ← → Collective
  - Individual freedom (my right to liberty) vs. Collective freedom (national self-determination / people's freedom)
  - Positive freedom slides from the individual to the collective in Rousseau — this is the danger
    Berlin is most vigilant about

Dimension 3: Opportunity ← → Capability
  - Formal freedom (what I am legally entitled to do) vs. Substantive freedom (what I can actually do)
  - Sen's (1999) capability approach takes this as its core

Dimension 4: Negative ← → Positive (policy dimension)
  - Freedom from state interference vs. Freedom through state-provided resources
  - This is the core battlefield of the concept of "freedom" in contemporary political debate

Dimension 5: Freedom of choice ← → Freedom of the will
  - Political freedom (space for choice at the social level) vs. Metaphysical freedom (free will)
  - The two are easily conflated, and they involve entirely different arguments in political
    philosophy and metaphysics

### Core Insight of the Conceptual Analysis

Berlin's paper's most important contribution is not defining "what freedom is," but revealing that
"the concept of freedom carries fundamentally different dimensions in different philosophical
traditions and social contexts." Many political disagreements stem from conflating different
dimensional axes:
- A is arguing for X using the meaning of negative freedom
- B is arguing against X using the meaning of positive freedom
- The two are in fact not in conflict — they are merely using different dimensions of the same word.

### Reconstruction Notes and Technical Details

- This conceptual analysis does not aim to resolve "what is freedom," but to chart freedom's
  "logical geography."
- MacCallum (1967) proposes a triadic framework: X is free from Y to do Z — freedom always has
  three elements. This analysis attempts to unify the negative and positive dimensions: negative
  freedom emphasizes Y, positive freedom emphasizes Z.
- If one accepts MacCallum's framework, then negative/positive are not two kinds of freedom, but
  two different emphases within a single concept of freedom.
```
