<!-- Generated from Framework/Workflow. Do not edit directly. -->
# Normativity Analysis Examples

> This document demonstrates the practical application of normativity analysis across different philosophical arguments. Each example shows the complete input-to-output process, covering ought-type classification, source diagnosis, reasons internalism/externalism assessment, bindingness mechanism tracing, and normative architecture mapping.

---

## Example 1: Categorical vs. Hypothetical Imperative (Kant)

### Input

*— Adapted from Kant, Groundwork of the Metaphysics of Morals, 1785, Section II*

> All imperatives command either hypothetically or categorically. The former represent the practical necessity of a possible action as a means to achieving something else that one wills (or that it is at least possible for one to will). The categorical imperative would be one that represented an action as objectively necessary of itself, without reference to another end. Because the moral law must apply universally to all rational beings — and cannot depend on any contingent desire, inclination, or purpose — it must be a categorical imperative. A hypothetical imperative cannot ground morality, for if an agent lacked the relevant desire, the imperative would not bind her.

### Output

```
## Normativity Analysis Report

### Basic Information
- **Analysis ID**: NORM-EX001
- **Source**: Kant, Groundwork of the Metaphysics of Morals (1785), Section II
- **Ought Domains Present**: Moral, Instrumental
- **Primary Normative Theory**: Rationalist + Constitutivist (proto-constitutivist)
- **Reasons Position**: Externalist (strong)

### Ought-Type Classification Table

| ID | Text/Location | Domain | Structure | Justification |
|----|--------------|--------|-----------|---------------|
| N1 | "All imperatives command either hypothetically or categorically" | Meta-normative (taxonomic) | N/A | This is a definitional claim about imperatives, not itself a normative prescription |
| N2 | Hypothetical imperative: "if you will the end, you ought to will the means" | Instrumental | Hypothetical | Explicitly conditional on the agent's willing the end. The "ought" vanishes if the end is not willed |
| N3 | Categorical imperative: action "objectively necessary of itself" | Moral | Categorical | Binds unconditionally, regardless of desires, inclinations, or purposes. No "if you want X" condition applies |
| N4 | "The moral law must apply universally to all rational beings" | Moral | Categorical | Universality precludes desire-dependence; must bind every rational agent, not only those with specific inclinations |
| N5 | "A hypothetical imperative cannot ground morality" | Moral (meta-level) | Categorical | Negative claim: hypothetical imperatives are structurally inadequate for moral normativity because they are revocable |

### Normativity Source Classification

**Primary Source: Rationalist** (Confidence: High)

Evidence: The argument grounds moral normativity in the structure of practical reason itself — what is "objectively necessary of itself" for a rational will. The categorical imperative derives its bindingness from the form of rationality, not from any contingent feature of the agent. The universal applicability to "all rational beings" (N4) is the hallmark of rationalist sourcing: the source of the "ought" is the nature of rationality, not desire, social practice, or external fact.

**Secondary Source: Proto-Constitutivist** (Confidence: Medium)

Evidence: Although Kant does not use the post-Korsgaardian vocabulary of "constitutivism," the argument's structure anticipates it. The moral law is grounded in what it is to be a rational agent — the very form of rational willing. The question "why should I be moral?" receives the answer: because to be an agent at all is to be subject to the requirements of practical reason, and morality is the expression of those requirements. This is the constitutivist move avant la lettre.

**Alternative Diagnosis**: Could be classified as `reasons_fundamentalist` if one reads the categorical imperative as a primitive normative fact. However, Kant's explicit grounding in "rational nature" and "the form of practical reason" favors rationalist over reasons-fundamentalist classification.

### Reasons Internalism/Externalism Assessment

**Classification: Strong Externalism** (Confidence: High)

The argument is paradigmatically externalist. The categorical imperative binds an agent regardless of her subjective motivational set. Kant explicitly argues that the moral law must apply "regardless of any contingent desire, inclination, or purpose." An immoral agent who lacks all desire to be moral nonetheless has a moral reason to act rightly — indeed, has the very same moral reasons as a virtuous agent. The reason exists independently of the agent's psychology.

**Implications**: Strong externalism commits the argument to explaining how external reasons can be practical — how a reason that is entirely disconnected from the agent's motivations can nonetheless guide action. Kant's answer (developed elsewhere) is that pure practical reason can itself be a motive (respect for the moral law). Whether this succeeds is the central debate about Kantian moral psychology.

### Bindingness Mechanism

**Primary Mechanism: Rational Requirement** (Confidence: High)

The bindingness chain:
1. "You ought to keep your promises." Why?
2. "Because promise-keeping is required by the moral law." Why is the moral law binding?
3. "Because the moral law is a categorical imperative — objective necessity of itself." Why is that binding?
4. "Because it is a requirement of practical reason — to violate it is to act contrary to one's own rational nature."

**Regress Analysis**: Kant stops the regress at the nature of practical reason itself. The question "why should I care about the requirements of practical reason?" is, for Kant, incoherent — to ask the question is already to engage in practical reasoning, which presupposes the very norms the question attempts to challenge. This is a constitutivist-style regress-stopper (the norm is presupposed by the activity of questioning it), though Kant does not use this vocabulary.

**Evaluation**: The regress-stopper is satisfactory if one accepts that practical reason has constitutive norms. If one denies this — if one treats practical reason as merely instrumental (Humeanism) — the regress is not stopped, and the categorical imperative's bindingness remains unexplained.

### Normative Architecture

**Architecture Type: Foundational**

The moral law (categorical imperative) is the single foundation. All specific moral duties are derived from it via specification. Hypothetical imperatives form a separate, non-moral branch grounded in instrumental rationality.

```
Practical Reason [ROOT]
├── Categorical Imperative [MORAL FOUNDATION]
│   ├── Duty of Honesty
│   ├── Duty of Beneficence
│   └── ... (all specific moral duties)
└── Hypothetical Imperatives [INSTRUMENTAL]
    ├── If you will health, you ought to exercise
    ├── If you will knowledge, you ought to study
    └── ... (all instrumental norms)
```

**Orphan claims**: None. All normative claims are traceable either to the categorical imperative (moral) or to instrumental rationality (non-moral).

### Summary Assessment

This argument presupposes a rationalist theory of moral normativity grounded in the form of practical reason itself — what Kant later develops as the doctrine of the fact of reason. The categorical/hypothetical distinction is the central analytical tool, and the argument's conclusion — that morality must be categorical — follows from the premise that morality must bind universally. The argument is strongly externalist about reasons, which creates downstream obligations in moral psychology to explain how reason alone can motivate. The regress stops at rational nature, which will satisfy rationalists but not Humeans.
```

---

## Example 2: Internal vs. External Reasons (Williams)

### Input

*— Adapted from Williams, "Internal and External Reasons," 1981*

> An agent has a reason to act only if the action in question would serve or promote some element of her subjective motivational set — her desires, projects, commitments, and dispositions. This is the internal interpretation of reasons statements. The alleged "external" reason — a reason that binds an agent regardless of her motivational set — is either false (if no sound deliberative route connects it to S) or, if it purports to be a reason entirely independent of S, unintelligible. The statement "A has a reason to φ" cannot mean "A has a reason to φ regardless of A's motivations," because then the attribution of a reason would float free of any connection to action and practical deliberation. You cannot ascribe a reason to someone that bears no connection whatsoever to what she actually cares about.

### Output

```
## Normativity Analysis Report

### Basic Information
- **Analysis ID**: NORM-EX002
- **Source**: Williams, "Internal and External Reasons" (1981)
- **Ought Domains Present**: Practical (general), Meta-normative
- **Primary Normative Theory**: Humean Internalism
- **Reasons Position**: Humean Internalism (Williams-style)

### Ought-Type Classification Table

| ID | Text/Location | Domain | Structure | Justification |
|----|--------------|--------|-----------|---------------|
| N1 | "An agent has a reason to act only if the action would serve or promote some element of S" | Practical | Hypothetical | The reason is conditional on the agent's subjective motivational set S. If nothing in S is served, no reason exists |
| N2 | External reason statements are "false" or "unintelligible" | Meta-normative | N/A | This is a meta-level claim about the semantics of reasons statements, not a first-order prescription |
| N3 | "You cannot ascribe a reason to someone that bears no connection to what she actually cares about" | Practical (norm of reason-ascription) | Hypothetical | The norm governing reason-ascription is itself grounded in the agent's cares |

### Normativity Source Classification

**Primary Source: Humean** (Confidence: High)

Evidence: The argument explicitly grounds all practical reasons in the agent's "subjective motivational set" — desires, projects, commitments, and dispositions. This is the canonical Humean thesis: reasons are means to satisfying existing desires (broadly construed). The source of normativity is the agent's own motivational psychology. There is no external normative source — no categorical imperative, no irreducible normative facts, no constitutive standards of agency that generate reasons independently of S.

**Key Diagnostic Indicators**:
- Reasons are analyzed in terms of desires/motivational set (not primitive, not grounded in rationality alone)
- The "sound deliberative route" is the mechanism connecting S to action
- The argument explicitly denies that reasons can exist independent of S
- Normativity is agent-relative and contingent on individual psychology

### Reasons Internalism/Externalism Assessment

**Classification: Humean Internalism (Williams-style)** (Confidence: High)

This is the paradigm case of Humean internalism. The defining features are all present:
1. All reasons must connect to S via a sound deliberative route.
2. External reasons — reasons that exist independently of S — are either false or unintelligible.
3. The content of S is contingent and agent-specific.
4. The "sound deliberative route" includes instrumental reasoning, means-end coherence, and imaginative exploration of alternatives, but not the acquisition of new fundamental desires ex nihilo.

This is not merely `weak_motivational_internalism` (reasons must be capable of motivating under appropriate conditions) nor `rational_internalism` (reasons are what a fully rational agent would be motivated by), because Williams grounds reasons specifically in the *actual* contents of S, not an idealized or rationalized version of it. An agent who would have a reason if she were fully rational but who, given her actual S, has no deliberative route to the action, simply has no reason.

### Bindingness Mechanism

**Primary Mechanism: Desire-Dependence** (Confidence: High)

The bindingness chain for a specific reason:
1. "A has a reason to visit the doctor." Why?
2. "Because visiting the doctor serves A's desire to be healthy." Why does that desire give a reason?
3. "Because all reasons are grounded in serving elements of S — there is no further source of normativity."

**Regress Analysis**: Williams stops the regress at S itself — the agent's subjective motivational set. The question "but why should I care about serving my desires?" is, for Williams, misplaced: serving one's desires is not itself a reason one has; rather, having desires is what makes it the case that one has reasons at all. The regress-stopper is the agent's actual motivational psychology, which is a brute psychological fact about the agent, not a normative fact.

**Evaluation**: The regress-stopper is psychologically substantive but normatively minimal. It explains why agents are motivated, but it may not explain why they *ought* to be motivated in the normative sense. Humean internalism collapses prudential normativity into motivational psychology; for critics, this seems to lose the normative force of reasons altogether. If an agent has depraved desires, Humean internalism must say she has reasons to satisfy them — a bullet that Humeans bite but opponents find counterintuitive.

### Normative Architecture

**Architecture Type: Foundational**

The architecture is flat and foundational in an unusual way. Rather than a single normative principle grounding all reasons (as in Kant's rationalism), the foundation is the agent's S — a contingent, agent-specific foundation. Each agent has her own foundational "ground" of normativity.

```
Agent's Subjective Motivational Set S [FOUNDATION — agent-specific]
├── Desire D1 [Health] → Reason to exercise, to visit doctor, to eat well
├── Project P1 [Writing a book] → Reason to research, to schedule writing time
├── Commitment C1 [Friendship with X] → Reason to call X, to help X
└── ... (all reasons derive from elements of S via sound deliberative routes)
```

**Cross-agent variation**: Different agents have different S, so different reasons. There is no universal normative foundation. This is the defining structural feature of Humean internalism.

**Orphan claims**: None. Every reason must trace back to S.

### Summary Assessment

This argument is the standard-bearer for Humean internalism about reasons. Its strength is its tight connection between reasons and motivation — it never faces the problem of explaining how an external reason can grip an agent. Its weakness is that it seems to lose normative objectivity: if an agent's S contains nothing that would ground a reason to be moral, then on Williams's account she has no reason to be moral. The argument also faces the "depraved desires" problem — Humean internalism must grant reasons to satisfy desires that we intuitively think provide no reasons at all. The argument's success depends on whether one finds the Humean picture of normativity intuitively adequate or normatively impoverished.
```

---

## Example 3: Constitutivism (Korsgaard)

### Input

*— Adapted from Korsgaard, The Sources of Normativity, 1996, Lecture 3*

> The normative question — "but why should I care about that?" — can be asked of any normative claim. If we answer by pointing to a further normative source, the question can be asked again, generating an infinite regress. The regress can only be stopped by a norm that is constitutive of the very activity of asking the normative question — a norm that one cannot coherently question without simultaneously engaging in the activity it constitutes. For reflective agents, the relevant activity is agency itself. Practical identity — the description under which you value yourself — is what gives you reasons, and practical identity is constitutive of being an agent at all. You cannot coherently ask "why should I be an agent?" because asking the question is itself an exercise of agency.

### Output

```
## Normativity Analysis Report

### Basic Information
- **Analysis ID**: NORM-EX003
- **Source**: Korsgaard, The Sources of Normativity (1996), Lecture 3
- **Ought Domains Present**: Moral, Prudential, Practical (general)
- **Primary Normative Theory**: Constitutivist
- **Reasons Position**: Internalist (rational-internalist, Korsgaard-style)

### Ought-Type Classification Table

| ID | Text/Location | Domain | Structure | Justification |
|----|--------------|--------|-----------|---------------|
| N1 | "The normative question can be asked of any normative claim" | Meta-normative | N/A | Descriptive claim about the open-ended nature of normative questioning |
| N2 | Answering the normative question by pointing to a further source generates an infinite regress | Meta-normative | N/A | Structural claim about normative justification |
| N3 | "You have reason to act as your practical identity requires" | Moral/Prudential | Categorical (substantively) | Formally hypothetical on having a practical identity, but practical identity is inescapable for agents — thus substantively categorical |
| N4 | "You cannot coherently ask 'why should I be an agent?'" | Practical | N/A | Meta-normative claim about the pragmatics of normative questioning, not a first-order "ought" |
| N5 | Reasons derive from practical identity | Practical | Hypothetical → Categorical | Conditionally grounded in practical identity, but the condition is inescapable for all agents, making the reasons substantively categorical |

### Normativity Source Classification

**Primary Source: Constitutivist** (Confidence: High)

Evidence: This is the canonical constitutivist argument. The normative source is explicitly identified as "constitutive standards of agency" — norms that are constitutive of what it is to be an agent. Korsgaard identifies the constitutive activity as "agency," and the constitutive norms as those of "practical identity." The argument's structure — the regress argument — is the distinctive argumentative signature of constitutivism.

**Key Diagnostic Indicators**:
- Norms grounded in "what is constitutive of agency"
- The regress argument as the primary justificatory strategy
- Practical identity as the bridge between formal agency and substantive reasons
- Inescapability of the constitutive activity as the regress-stopper
- The normative question itself presupposing the norms it questions

**Nearest-neighbor distinction**: This is Korsgaard's constitutivism rather than Velleman's (which grounds norms in the constitutive aim of action — autonomous self-understanding — rather than practical identity) because the argument explicitly invokes "practical identity" as the source of substantive reasons and frames the problem as a regress of normative justification.

### Reasons Internalism/Externalism Assessment

**Classification: Rational Internalism** (Confidence: High)

Korsgaard's position is internalist but not Humean. Reasons must connect to the agent's motivational structure, but the relevant motivational structure is not the agent's contingent desires (S in Williams's sense) but the agent's status as a reflective agent — which is universal across all agents. The reason to be moral is internal because it is grounded in the agent's own practical identity, but it is also universal because every agent necessarily has a practical identity.

This is `rational_internalism` rather than `humean_internalism` because the deliberative route does not start from contingent desires but from the necessary features of agency itself. It is distinct from `strong_externalism` because reasons are still grounded in the agent's own nature (as an agent) rather than in mind-independent facts.

### Bindingness Mechanism

**Primary Mechanism: Constitutive Necessity** (Confidence: High)

The bindingness chain:
1. "You ought to keep your promises." Why?
2. "Because promise-keeping is required by your practical identity as a trustworthy person." Why is that practical identity binding?
3. "Because practical identity is what gives you reasons at all." Why is that binding?
4. "Because practical identity is constitutive of agency — you cannot be an agent without some practical identity." Why must you be an agent?
5. "You cannot coherently ask 'why should I be an agent?' because asking the question is itself an exercise of agency. The question presupposes the very thing it questions."

**Regress Analysis**: Korsgaard's regress-stopper is the inescapability of agency. The question "why should I be an agent?" is pragmatically self-defeating — it can only be asked by an agent, and it challenges the very norms that make asking it possible. This is the strongest form of regress-stopper: transcendental. It is not a brute normative fact or a primitive reason; it is a pragmatic necessity that cannot be coherently denied.

**Evaluation**: The regress-stopper is elegantly non-question-begging — it does not assert a normative premise but demonstrates that the critic is already committed to what she questions. However, the transition from formal agency (the mere capacity to act for reasons) to substantive moral content (specific duties) requires the intermediate step of practical identity, and it is here that the argument is most vulnerable. The skeptic can ask: "Why should I adopt this practical identity rather than that one?" To answer, Korsgaard appeals to the need for practical identity as such, but this may underdetermine which specific identities and obligations result.

### Normative Architecture

**Architecture Type: Foundational**

Agency is the ungrounded ground. Practical identity mediates between formal agency and substantive reasons. The structure is hierarchical with a single foundation.

```
Agency [FOUNDATION — constitutive, inescapable]
└── Practical Identity [INTERMEDIATE LAYER — contingent content, necessary form]
    ├── Moral Identity → Moral Reasons (keeping promises, telling truth, etc.)
    ├── Professional Identity → Role-Specific Reasons
    ├── Personal Identity → Prudential Reasons
    └── ... (all practical identities generate reasons)
```

**Orphan claims**: None. All reasons are traceable through practical identity to agency.

### Summary Assessment

This argument offers the most ambitious solution to the normative regress problem in the literature. Its strength is the transcendental character of the regress-stopper — it avoids both brute normative facts (which satisfy realists but not skeptics) and contingent desires (which satisfy Humeans but lack universality). Its weakness lies in the "content problem": the transition from formal agency to substantive moral content requires practical identity, and the choice of practical identity seems, on Korsgaard's own account, to be a matter of reflective endorsement rather than rational necessity. The argument's downstream metaethical implications: constitutivism is compatible with both cognitivist and expressivist semantics (what matters is the normative source, not the semantics of normative language), but it pushes strongly toward internalist moral psychology — if reasons are grounded in agency, then moral judgment inherently motivates.
```

---

## Example 4: Normative Source Analysis — Practical Reason vs. Desire-Based

### Input

*— Synthetic reconstruction of a hybrid normative theory, drawing on Smith (The Moral Problem, 1994) and Parfit (On What Matters, 2011)*

> There are two fundamentally different kinds of normative reasons. Some reasons are grounded in an agent's desires — if you want to avoid pain, you have a reason to take painkillers. These are desire-based reasons, and their normative force depends entirely on the agent's actual motivational structure. But there are also object-given reasons — reasons provided by facts about the objects of our attitudes rather than facts about our attitudes themselves. For example, the fact that an action would save an innocent life is a reason to perform it, regardless of whether the agent happens to care about innocent lives. Object-given reasons are fundamental and irreducible. We should not try to analyze them in terms of desires, rational requirements, or constitutive norms.

### Output

```
## Normativity Analysis Report

### Basic Information
- **Analysis ID**: NORM-EX004
- **Source**: Synthetic hybrid theory (Smith 1994 / Parfit 2011)
- **Ought Domains Present**: Prudential, Moral
- **Primary Normative Theory**: Reasons Fundamentalism (moral) + Humean (prudential) — hybrid
- **Reasons Position**: Externalist (moral), Internalist (prudential) — domain-specific

### Ought-Type Classification Table

| ID | Text/Location | Domain | Structure | Justification |
|----|--------------|--------|-----------|---------------|
| N1 | "If you want to avoid pain, you have a reason to take painkillers" | Prudential | Hypothetical | Explicitly conditional on the agent's desire. No desire, no reason |
| N2 | "The fact that an action would save an innocent life is a reason to perform it, regardless of whether the agent happens to care" | Moral | Categorical | Explicitly unconditional — binds regardless of the agent's motivational set |
| N3 | "Object-given reasons are fundamental and irreducible" | Meta-normative | N/A | Claim about the metaphysical status of reasons, not a prescription |
| N4 | "We should not analyze object-given reasons in terms of desires, rational requirements, or constitutive norms" | Meta-normative | N/A | Methodological norm about theorizing, not a first-order normative claim |

### Normativity Source Classification

**Dual Source: Reasons Fundamentalism (Moral) + Humean (Prudential)** (Confidence: High)

Evidence: The argument explicitly distinguishes two normative domains with distinct source theories:

**Moral Normativity — Reasons Fundamentalism**:
- Reasons are treated as "fundamental and irreducible" (N3)
- Resists analysis in other terms — not desires, not rationality, not constitution (N4)
- Object-given: reasons are provided by facts about the action/outcome, not about the agent's psychology
- This is Parfit's canonical position: reasons are the basic normative unit

**Prudential Normativity — Humean**:
- Reasons are explicitly conditional on desires (N1)
- The normative force derives from the agent's actual motivational structure
- This is the classic Humean pattern: reason as means to satisfying existing desires

**Consistency Check**: The hybrid position is internally consistent as long as the domains are kept distinct. The argument does not claim that all reasons are desire-based (contra Williams) nor that all reasons are object-given (contra Parfit's stronger claims). The potential tension: if object-given reasons exist, why should a desire-based reason count as a genuine normative reason at all, rather than merely a motivational explanation? The argument does not address this.

### Reasons Internalism/Externalism Assessment

**Classification: Domain-Dependent** (Confidence: High)

- **Moral Reasons — Externalist (Strong)**: Object-given reasons exist independently of the agent's motivational set. An agent who does not care about innocent lives nonetheless has a reason not to kill them. The reason is a normative fact, not a psychological one. This is strong externalism: the reason exists regardless of any connection to the agent's psychology.

- **Prudential Reasons — Internalist (Humean)**: Desire-based reasons exist only if they serve the agent's S. This is Williams-style Humean internalism for the prudential domain.

**Tension**: The dual classification creates an unresolved tension. If one accepts Williams's argument that external reasons are unintelligible, the moral reason claims fail. If one accepts Parfit's argument that fundamental reasons are object-given, the prudential reason claims may not qualify as genuinely normative. The argument needs a bridging principle to explain why both kinds of reasons count as reasons in the same sense.

### Bindingness Mechanism

**Dual Mechanism: Irreducible Normative Fact (Moral) + Desire-Dependence (Prudential)**

**Moral Bindingness Chain**:
1. "You ought not to kill innocents." Why?
2. "Because the fact that an action kills innocents is a reason not to do it." Why is that fact a reason?
3. "Because object-given reasons are fundamental and irreducible — there is no further 'why.' They are normative bedrock."

**Prudential Bindingness Chain**:
1. "You ought to take painkillers." Why?
2. "Because you want to avoid pain — the action serves your desire." Why does serving desires give reasons?
3. "Because desire-based reasons just are reasons grounded in S — there is no further source."

**Regress Analysis**:
- Moral regress stops at primitive object-given reasons. The question "but why should I care about object-given reasons?" receives the answer: they are intrinsically reason-giving. This is satisfactory only if one accepts that normativity can be a primitive feature of reality — a substantial metaphysical commitment.
- Prudential regress stops at the agent's desires. The question "but why should I care about serving my desires?" is rejected as misplaced.

**Gap**: The two regress-stoppers are of fundamentally different kinds (irreducible normative fact vs. psychological fact), and the argument provides no unified account of what makes both count as "normativity."

### Normative Architecture

**Architecture Type: Foundational (Bifurcated)**

Two independent normative foundations, with no common ground. This creates a dual-foundation architecture rather than a single unified system.

```
Normativity
├── OBJECT-GIVEN REASONS [MORAL FOUNDATION — irreducible]
│   ├── Reason: save lives → Duty of Rescue
│   ├── Reason: prevent suffering → Duty of Beneficence
│   └── ... (all irreducibly normative moral reasons)
└── DESIRE-BASED REASONS [PRUDENTIAL FOUNDATION — contingent]
    ├── Desire D1 → Reason to φ1
    ├── Desire D2 → Reason to φ2
    └── ... (all desire-dependent prudential reasons)
```

**Tensions**: The two foundations may conflict. If an agent's desire-based reasons counsel an action that object-given reasons prohibit, which takes priority? The argument provides no priority rule. This is not merely an orphan claim problem but an architectural gap: the normative system lacks a conflict-resolution mechanism.

### Summary Assessment

This hybrid normative theory attempts to have it both ways: irreducible moral normativity (satisfying the intuition that morality is not optional) and desire-based prudential normativity (respecting the connection between reasons and motivation). Its strength is its phenomenologically accurate treatment of different normative domains. Its weakness is the lack of a unified theory of what makes something a "reason" — the argument uses "reason" in two apparently different senses without explaining the common core. The downstream metaethical implications are complex: moral semantics could be either cognitivist or expressivist (reasons-fundamentalist cognitivism is standard, but expressivist interpretations are possible); moral psychology must explain how object-given reasons can motivate (externalism requires an account of rational motivation).
```

---

## Example 5: Error Theory about Categorical Normativity (Mackie)

### Input

*— Adapted from Mackie, Ethics: Inventing Right and Wrong, 1977, Chapter 1*

> If there were objective moral values, they would be entities or qualities of a very strange sort, utterly different from anything else in the universe. Correspondingly, if we were aware of them, it would have to be by some special faculty of moral perception or intuition, utterly different from our ordinary ways of knowing anything else. The postulation of such queer entities is not justified by anything else we know about the world. Therefore, there are no objective moral values. Moral judgments are all false — or, at least, they presuppose something false. However, we can and should continue to use moral language; moral discourse serves important social functions. We simply need to recognize that when we make moral claims, we are projecting our attitudes onto the world, not describing features of it.

### Output

```
## Normativity Analysis Report

### Basic Information
- **Analysis ID**: NORM-EX005
- **Source**: Mackie, Ethics: Inventing Right and Wrong (1977), Chapter 1
- **Ought Domains Present**: Moral (target of critique)
- **Primary Normative Theory**: Error theory about realism; Humean/Expressivist (constructive)
- **Reasons Position**: N/A (error theory eliminates normative reasons)

### Ought-Type Classification Table

| ID | Text/Location | Domain | Structure | Justification |
|----|--------------|--------|-----------|---------------|
| N1 | "If there were objective moral values, they would be queer entities" | Meta-normative (critique) | N/A | Conditional claim about the metaphysical character of what objective values would be like |
| N2 | "There are no objective moral values" | Meta-normative (error-theoretic) | N/A | Ontological denial, not a normative prescription |
| N3 | "Moral judgments are all false" | Meta-normative (semantic) | N/A | Semantic claim about the truth-value of moral judgments |
| N4 | "We can and should continue to use moral language" | Practical (norm of discourse) | Hypothetical | The "should" is conditional on the social function of moral discourse — instrumental normativity |
| N5 | "We are projecting our attitudes onto the world, not describing features of it" | Meta-normative (semantic) | N/A | Descriptive claim about the actual function of moral language |
| N6 | Implicit: Objective moral values would be categorical (binding unconditionally) | Moral (critiqued) | Categorical | The argument's target is categorically binding moral values. The error theory critiques precisely the categorical character of morality |

### Normativity Source Classification

**Target of Critique: Realist** (Confidence: High)

The argument's critique targets a realist conception of normativity: the view that normative facts are mind-independent features of reality that categorically bind agents. Mackie's "queerness" argument is directed at the metaphysical strangeness of such facts — they would be entities of a "very strange sort" (N1) requiring a "special faculty" (N1) to detect. This is unmistakably a critique of robust normative realism.

**Constructive Position: Expressivist/Projectivist** (Confidence: Medium)

Mackie's positive account — that moral judgments "project attitudes onto the world" (N5) — is a form of expressivism avant la lettre. The source of the felt "normativity" of moral claims is our own attitudes, projected outward. But crucially, Mackie denies that this projection generates genuine normative facts — the attitudes are not truth-tracking. This is error-theoretic expressivism: the semantics of moral language is expressivist, but ordinary speakers mistakenly take it to be descriptivist/cognitivist.

**Alternative Diagnosis**: Could be classified as `evolutionary` if one emphasizes Mackie's later work on the evolutionary function of moral attitudes. However, in the canonical Chapter 1 argument, the emphasis is on metaphysical queerness and projection, which favors the expressivist classification.

### Reasons Internalism/Externalism Assessment

**Classification: Not Applicable (Error Theory)** (Confidence: High)

Strictly speaking, error theory eliminates the category of normative reasons altogether. If all moral judgments are false, then there are no moral reasons. The question "are reasons internal or external?" presupposes that there are reasons, which error theory denies.

However, the argument's diagnostic implications are externalist:
- The critiqued (realist) position is strongly externalist — categorical reasons are precisely reasons that bind regardless of the agent's psychology.
- The constructive (expressivist) position implies a kind of internalism — what feels like normativity is actually the projection of internal attitudes outward.
- If one asks the internalism/externalism question about the *felt* normativity that survives the error theory, it is internalist (the felt grip comes from within the agent's attitudes), but this is not "genuine" normativity on Mackie's account.

### Bindingness Mechanism

**Critique Target: Irreducible Normative Fact** (Confidence: High)

The argument critiques the bindingness mechanism of realist normativity: categorical bindingness as irreducible normative fact. For the realist, the regress stops at "this is just what the normative fact is." Mackie's challenge is that this regress-stopper is metaphysically and epistemically "queer" — it postulates entities unlike anything else and modes of access unlike any ordinary epistemic faculty.

**Constructive Alternative: Social Practice / Attitude Projection** (Confidence: Medium)

Mackie's alternative bindingness mechanism is twofold:
1. **Social function**: Moral language binds because of its social role in coordinating behavior and regulating conflict. The "ought" is an instrument of social regulation.
2. **Psychological projection**: The *felt* bindingness is the projection of internal attitudes. We experience our own disapproval as if it were a property of the disapproved action.

**Regress Analysis (Constructive)**:
1. "You ought to keep your promises." Why?
2. "Because promise-keeping is a socially useful practice." Why should I care about social utility?
3. "Here, the regress stops at the agent's contingent social interests. There is no deeper normative fact — there is no categorical 'ought' at all. The felt ought is a projection."

**Evaluation**: Mackie's regress-stopper is eliminativist rather than justificatory. It does not *justify* the norm; it *explains away* the feeling of normative force. This is fundamentally different from the other examples in this set — it is a debunking account, not a grounding account.

### Normative Architecture

**Architecture Type: Network (Post-Error-Theory Reconstruction)**

After the error theory eliminates categorical normativity, the surviving normative architecture is a network of socially useful conventions, attitudinal projections, and instrumental norms — no foundational principle, no hierarchy, just the contingent patterns of human social and psychological life.

```
[NO NORMATIVE FOUNDATION]
├── Social Convention C1 (promise-keeping) → Felt reason to keep promises
├── Social Convention C2 (truth-telling) → Felt reason to tell truth
├── Projected Attitude A1 (disapproval of cruelty) → Felt wrongness of cruelty
└── ... (all "normative" claims are projections, conventions, or errors)
```

**Orphan claims**: In the post-error-theory picture, *all* normative claims are orphans — they have no genuine normative grounding, only causal explanations. This is not a defect; it is the point.

### Summary Assessment

This argument is the canonical error theory about categorical normativity. Its strength is the "argument from queerness," which presses a genuine metaphysical-epistemological challenge: if categorical normativity is real, it is unlike anything else, and we need an account of how we access it. Its weakness (as critics have noted) is that the queerness challenge may be overstated — physical reality is also "queer" in various ways (quantum mechanics, consciousness), and we accept it. The argument's success depends on whether one finds irreducible normative facts more mysterious than, say, irreducible physical facts.

The downstream metaethical implications are significant: error theory about normativity entails anti-realism in metaphysics (there are no moral facts), non-cognitivism in semantics (moral language is expressivist, though ordinary speakers don't realize it), and a projectivist moral psychology (moral judgment is the projection of attitudes). The entire metaethical landscape is reshaped by the elimination of normative reality.
```

---
