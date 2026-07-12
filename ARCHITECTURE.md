# Analytic Philosophy Writing System — Architecture Document

> **Version**: 0.3-alpha &emsp; **Status**: Alpha
>
> **Built atop `academic-research-skills` (v3.15.0)**
> This system does not re-implement ARS's existing capabilities (literature search, paper writing, peer review, citation verification). Instead, it layers on top of ARS an **analytic-philosophy-specific methodological layer**.
>
> **Subdomain Coverage**: General Analytic Philosophy · Metaphysics · Metaethics

---

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [ARS Gap Analysis](#2-ars-gap-analysis)
3. [Directory Tree](#3-directory-tree)
4. [Layered Architecture](#4-layered-architecture)
5. [Dependency Graph](#5-dependency-graph)
6. [Research Flow](#6-research-flow)
7. [Skill Taxonomy](#7-skill-taxonomy)
8. [Naming Conventions](#8-naming-conventions)
9. [File Conventions](#9-file-conventions)
10. [Extensibility](#10-extensibility)

---

## 1. Design Principles

### 1.1 Modularity
Each Skill performs exactly one reusable piece of philosophical analysis. "Swiss Army knife"-style skills are prohibited.

### 1.2 Composability
Skills compose naturally into analysis pipelines. Each Skill has a well-defined input/output contract.

### 1.3 Separation of Concerns
- Argument reconstruction is not conceptual analysis, is not objection generation, is not writing.
- The argument-analysis layer is strictly separated from the text-generation layer.
- Metaphysical analysis tools are independent of ethical analysis tools.

### 1.4 Scalability
The architecture supports adding dozens of future Skills without major redesign. Methodological depth takes priority over functional breadth.

### 1.5 Maintainability
- Each Skill is responsible only for itself.
- No duplicated logic, no duplicated prompts.
- When philosophical methodology changes, only the relevant dependency library needs updating — Skills themselves need not be rewritten.

### 1.6 Philosophy-Specificity
The system is optimized for **analytic philosophy**, not general academic writing. Each Skill encourages:
- **Explicit argument reconstruction**: Transform text into standard premise-conclusion form
- **Principle of charity**: Construct the strongest version before evaluation
- **Dialectical analysis**: Thesis → objection → response cyclic structure
- **Implicit premise detection**: Uncover hidden assumptions
- **Counterexample generation**: Construct and evaluate counterexamples
- **Conceptual clarification**: Distinguish concepts, draw distinctions — not merely summarize
- **Ontological commitment explicitation**: Reveal the entities and categories presupposed by an argument

---

## 2. ARS Gap Analysis

### 2.1 What ARS Already Covers (Not Re-implemented)

| Capability | ARS Skill / Mode | Status |
|------|------------------|------|
| Deep literature search | `deep-research` | Direct invocation |
| Systematic literature review | `deep-research systematic-review` | Direct invocation |
| Full paper writing | `academic-paper full` | Direct invocation |
| Outline generation | `academic-paper outline-only` | Direct invocation |
| Abstract generation (bilingual CN/EN) | `academic-paper abstract-only` | Direct invocation |
| Format conversion (LaTeX/DOCX) | `academic-paper format-convert` | Direct invocation |
| Peer review simulation | `academic-paper-reviewer` | Direct invocation |
| Citation verification | `academic-paper citation-check` | Direct invocation |
| Revision coaching | `academic-paper revision-coach` | Direct invocation |
| Rebuttal audit | `academic-paper rebuttal-audit` | Direct invocation |
| AI usage disclosure | `academic-paper disclosure` | Direct invocation |
| Full pipeline orchestration | `academic-pipeline` | Direct invocation |
| Compliance checks | compliance checks | Direct invocation |

### 2.2 Analytic-Philosophy-Specific Capabilities (New Additions Required)

| Capability | Description | Priority | Subdomain |
|------|------|--------|--------|
| Argument reconstruction | Convert natural-language arguments into standard form | P0 | General |
| Principle of charity check | Assess whether the reconstruction is the strongest interpretation | P0 | General |
| Implicit premise detection | Discover hidden assumptions in arguments | P0 | General |
| Counterexample generation | Construct counterexamples targeting premises/conclusions | P0 | General |
| Conceptual analysis | Distinction drawing, necessary/sufficient condition analysis | P0 | General |
| Dialectical mapping | Thesis-objection-response structural analysis | P1 | General |
| Thought experiment analysis | Deconstruct the structure and force of thought experiments | P1 | General |
| Distinction tracking | Identify and track conceptual distinctions in a text | P1 | General |
| Modal argument analysis | Evaluate possibility/necessity claims | P1 | Metaphysics |
| Analogy assessment | Evaluate the relevance and strength of analogical reasoning | P1 | General |
| **Ontological commitment detection** | **Identify the entity types and existence categories presupposed by an argument** | **P1** | **Metaphysics** |
| **Identity and persistence analysis** | **Analyze identity conditions across time and possible worlds** | **P1** | **Metaphysics** |
| **Grounding / constitution analysis** | **Detect grounding, supervenience, and realization relations** | **P1** | **Metaphysics** |
| **Conceivability argument analysis** | **Evaluate conceivability-to-possibility inferences (zombie arguments, etc.)** | **P1** | **Metaphysics** |
| Reasoning parity check | Detect inconsistent application of principles | P1 | General |
| Intuition pump detection | Identify rhetorical appeals to intuition | P1 | General |
| **Causal claim analysis** | **Evaluate Humean vs. anti-Humean readings of causal claims** | **P2** | **Metaphysics** |
| **Essentialist claim detection** | **Detect and evaluate use of the essence/accident distinction in arguments** | **P2** | **Metaphysics** |
| **Natural kind and property analysis** | **Analyze arguments concerning natural kinds and the universals/tropes debate** | **P2** | **Metaphysics** |
| **Moral realism argument analysis** | **Structured analysis of moral realism/anti-realism/error theory/non-cognitivism arguments** | **P1** | **Metaethics** |
| **Normativity analysis** | **Categorical/hypothetical imperatives, internal/external reasons, sources and structure of normativity** | **P1** | **Metaethics** |
| **Moral semantics analysis** | **Cognitivism/expressivism/prescriptivism; truth-aptness of moral language** | **P1** | **Metaethics** |
| **Moral psychology analysis** | **The relation between moral judgment and motivation (internalism/externalism); the amoralist and weakness of will** | **P1** | **Metaethics** |
| **Moral disagreement argument analysis** | **Arguments from moral disagreement and their implications for realism/anti-realism** | **P2** | **Metaethics** |
| **Moral epistemology analysis** | **The possibility of moral knowledge; intuitionist and coherentist justificatory pathways** | **P2** | **Metaethics** |
| **Moral supervenience analysis** | **The supervenience of moral properties on natural properties and its metaphysical implications** | **P2** | **Metaethics** |
| Philosophical methodology reflection | Methodological awareness — reflective equilibrium, transcendental arguments, etc. | P2 | General |
| Intellectual history contextualization | Situate an argument within its history-of-ideas lineage | P2 | General |
| Argument mapping visualization | Generate dialectical tree diagrams | P2 | General |

> **Bolded rows** are metaphysics- and metaethics-specific new skills.

---

## 3. Directory Tree

```
.claude/
├── skills/
│   ├── phil-argument-reconstruct/    # Argument reconstruction
│   ├── phil-charity-check/           # Principle of charity check
│   ├── phil-premise-detect/          # Implicit premise detection
│   ├── phil-counterexample/          # Counterexample generation and evaluation
│   ├── phil-conceptual-analysis/     # Conceptual analysis
│   ├── phil-dialectical-map/         # Dialectical mapping
│   ├── phil-thought-experiment/      # Thought experiment analysis
│   ├── phil-distinction-track/       # Distinction tracking
│   ├── phil-modal-arg/               # Modal argument analysis
│   ├── phil-analogy-check/           # Analogical argument evaluation
│   ├── phil-parity-check/            # Reasoning parity check
│   ├── phil-intuition-pump/          # Intuition pump detection
│   ├── phil-methodology/             # Philosophical methodology reflection
│   ├── phil-contextualize/           # Intellectual history contextualization
│   ├── phil-citation-extract/        # [New] Citation extraction and role classification
│   │
│   ├── phil-ontological-commitment/  # [New] Ontological commitment detection
│   ├── phil-identity-persistence/    # [New] Identity and persistence analysis
│   ├── phil-grounding-check/         # [New] Grounding / constitution analysis
│   ├── phil-conceivability-arg/      # [New] Conceivability argument analysis
│   ├── phil-causation-analyze/       # [New] Causal claim analysis
│   ├── phil-essence-detect/          # [New] Essentialist claim detection
│   ├── phil-natural-kind-analyze/    # [New] Natural kind and property analysis
│   │
│   ├── phil-moral-realism/            # [New] Moral realism argument analysis
│   ├── phil-normativity/              # [New] Normativity analysis
│   ├── phil-moral-semantics/          # [New] Moral semantics analysis
│   ├── phil-moral-psychology/         # [New] Moral psychology analysis
│   ├── phil-moral-disagreement/       # [New] Moral disagreement argument analysis
│   ├── phil-moral-epistemology/       # [New] Moral epistemology analysis
│   └── phil-moral-supervenience/      # [New] Moral supervenience analysis
│
├── agents/
│   ├── metaphysician.md              # [New] Metaphysical analyst (ontology-focused)
│   ├── metaethicist.md               # [New] Metaethical analyst (moral language / norm analysis)
│   ├── phil-writer.md                # [Phase 6] Philosophy writer (outline/draft/revision)
│   ├── phil-reviewer.md              # [Phase 6] Philosophy reviewer (8-dimension + perspective)
│   ├── phil-commentator.md           # [Phase 6] Philosophy commentator (critical/response/position)
│   ├── phil-orchestrator.md          # [Phase 6] Pipeline orchestrator (5-stage workflow)
│   └── phil-tutor.md                 # [New] Tutor agent — dialogic reading mentor (Socratic + recommendations)
│
├── references/
│   ├── glossary-metaethics.md        # Metaethics terminology glossary
│   ├── glossary-metaphysics.md       # [New] Core metaphysics terminology glossary
│   ├── fallacy-catalog.md            # Formal / informal fallacy catalog
│   ├── thought-experiment-templates.md # Thought experiment typology
│   │                                  #   (including metaphysical subtypes)
│   ├── metaphysical-distinctions.md  # [New] Core metaphysical distinctions catalog
│   ├── ontological-categories.md     # [New] Ontological category taxonomy
│   ├── modal-logic-primer.md         # [New] Modal logic foundational reference
│   ├── causation-taxonomy.md         # [New] Causal theory taxonomy
│   ├── metaethical-distinctions.md   # [New] Core metaethical distinctions catalog
│   ├── moral-realism-taxonomy.md     # [New] Moral realism spectrum
│   ├── normativity-taxonomy.md       # [New] Normativity theory taxonomy
│   ├── argument-forms/               # Standard argument form library
│   │   ├── modus-ponens.md
│   │   ├── modus-tollens.md
│   │   ├── reductio.md
│   │   ├── transcendental.md
│   │   ├── leibniz-law.md            # [New] Leibniz's Law argument
│   │   ├── conceivability-argument.md # [New] Conceivability argument
│   │   ├── grounding-argument.md     # [New] Grounding argument
│   │   ├── supervenience-argument.md # [New] Supervenience argument
│   │   ├── recombination-argument.md # [New] Recombination argument
│   │   ├── truthmaker-argument.md    # [New] Truthmaker argument
│   │   ├── sorites.md                # [New] Sorites paradox
│   │   ├── four-dimensionalist.md    # [New] Four-dimensionalist argument
│   │   ├── mereological-argument.md  # [New] Mereological argument
│   │   ├── open-question-argument.md # [New] Open question argument (Moore)
│   │   ├── queerness-argument.md     # [New] Argument from queerness (Mackie)
│   │   ├── companions-in-guilt.md    # [New] Companions in guilt argument
│   │   ├── disagreement-argument.md  # [New] Disagreement argument
│   │   ├── regress-argument.md       # [New] Normative regress (Korsgaard)
│   │   └── moral-supervenience.md    # [New] Moral supervenience argument
│   └── philosophers-db/             # Philosopher archives (directory)
│       ├── INDEX.md                  # Alphabetical index + cross-references
│       ├── general/                  # General Philosophy (17 philosophers)
│       ├── metaphysics/              # Metaphysics (14 philosophers)
│       └── metaethics/               # Metaethics (17 philosophers)
│
├── commands/
│   ├── reconstruct.md                 # phil:reconstruct — Full-dimension text understanding (9-20 skills)
│   ├── evaluate.md                    # phil:evaluate — Multi-angle parallel critique (7 skills)
│   ├── review.md                      # phil:review — Peer review agent (8 dimensions)
│   ├── write.md                       # phil:write — Philosophy writer agent (outline/draft/revision)
│   ├── comment.md                     # phil:comment — Deep commentary agent (argument details)
│   ├── pipeline.md                    # phil:pipeline — Full pipeline orchestrator (5 stages)
│   └── tutor.md                       # [New] phil:tutor — Dialogic reading mentor (Socratic + recommendations)
│
│
├── shared/
│   ├── argument-schema.json          # Argument formalization contract
│   ├── dialectical-tree-schema.json  # Dialectical tree contract
│   ├── concept-map-schema.json       # Concept mapping contract
│   ├── premise-audit-schema.json     # Implicit premise audit contract
│   ├── analysis-report-schema.json   # Integrated analysis report contract
│   ├── ontological-commitment-schema.json  # [New] Ontological commitment contract
│   ├── grounding-relation-schema.json      # [New] Grounding relation contract
│   ├── moral-realism-schema.json            # [New] Moral realism stance contract
│   ├── normativity-schema.json              # [New] Normative structure contract
│   ├── citation-extract-schema.json         # [New] Citation extract data contract
│   └── templates/
│       ├── argument-reconstruction.md # Argument reconstruction report template
│       ├── premise-audit.md           # Premise audit template
│       ├── conceptual-analysis.md     # Conceptual analysis template
│       ├── dialectical-map.md         # Dialectical mapping template
│       └── ontological-audit.md       # Ontological audit template
│
└── memory/                           # Project memory (Claude persistent memory)
    ├── project-context.md
    └── philosopher-notes/             # Long-term accumulated philosophical notes
```

### 3.1 Rationale for This Organization

- **`skills/`**: Each Skill is an independent callable unit corresponding to one philosophical analysis methodology.
- **`agents/`**: Cross-Skill orchestration agents (self-contained complex dialogue strategies), separated from individual Skills.
- **`references/`**: Knowledge dependencies — not embedded in the Skills themselves, to avoid prompt bloat.
- **`commands/`**: User entry points — thin wrappers that point to a Skill or Agent.
- **`shared/`**: Cross-Skill shared data contracts (schemas and templates).

---

## 4. Layered Architecture

### Layer 0: Knowledge Base
**Rationale**: Philosophical analysis depends on substantial domain knowledge (argument forms, concepts, intellectual history) that must be separated from prompt logic for maintainability.

**When Used**: All downstream analysis skills may reference this layer.

**Contents** (organized into three clusters: General, Metaphysics, and Metaethics):

```
General Knowledge Cluster:
  ├── references/fallacy-catalog.md
  ├── references/argument-forms/ (general subset)
  ├── references/thought-experiment-templates.md (general subset)
  └── references/philosophers-db/ (general subset)

Metaphysics Knowledge Cluster:
  ├── references/glossary-metaphysics.md          # Core terminology
  ├── references/metaphysical-distinctions.md     # Core distinctions
  ├── references/ontological-categories.md        # Ontological categories
  ├── references/modal-logic-primer.md            # Modal logic
  ├── references/causation-taxonomy.md            # Causal theories
  ├── references/argument-forms/ (metaphysics subset)
  ├── references/thought-experiment-templates.md (metaphysics subset)
  └── references/philosophers-db/ (metaphysician subset)

Metaethics Knowledge Cluster:
  ├── references/glossary-metaethics.md           # Core terminology
  ├── references/metaethical-distinctions.md      # Core distinctions
  ├── references/moral-realism-taxonomy.md        # Realism spectrum
  ├── references/normativity-taxonomy.md          # Normativity theories
  ├── references/argument-forms/ (metaethics subset)
  ├── references/thought-experiment-templates.md (metaethics subset)
  └── references/philosophers-db/ (metaethicist subset)
```

#### Metaphysics Knowledge Dependency Details

| Knowledge File | Content | Referenced By |
|---------|------|---------|
| `glossary-metaphysics.md` | Ontology, entity, trope, universal, essence, accident, grounding, supervenience, realization, composition, persistence, transworld identity, possible world, causation, law of nature, disposition, category | All metaphysics skills |
| `metaphysical-distinctions.md` | Endurance/perdurance, presentism/eternalism, concrete/abstract, realism/anti-realism, reductionist/non-reductionist, Humean/anti-Humean, sparse/abundant properties, categorical/dispositional, grounded/autonomous, necessary/contingent, a priori/a posteriori, analytic/synthetic | `phil-distinction-track`, `phil-conceptual-analysis` |
| `ontological-categories.md` | Aristotelian categories, Quinean ontological commitment, Lewisian natural properties, mereological basic axioms, category ontology, fundamental/derivative levels | `phil-ontological-commitment` |
| `modal-logic-primer.md` | Basic axioms of modal systems (S4/S5/K, etc.), possible-world semantics, rigid designation, a priori vs. necessary distinction, two-dimensional semantics, counterfactual conditionals | `phil-modal-arg`, `phil-conceivability-arg`, `phil-essence-detect` |
| `causation-taxonomy.md` | Humean regularity theory, counterfactual theory (Lewis), interventionism (Woodward), capacity theory (Cartwright), process theory, causal exclusion problem, epiphenomenal causation, causal overdetermination | `phil-causation-analyze` |

#### Metaethics Knowledge Dependency Details

| Knowledge File | Content | Referenced By |
|---------|------|---------|
| `glossary-metaethics.md` | Moral realism, anti-realism, error theory, non-cognitivism, expressivism, cognitivism, internalism, externalism, categorical imperative, hypothetical imperative, motivational internalism, motivational externalism, reasons internalism, reasons externalism, fittingness, normative force, thick/thin concepts, supervenience, Humean theory of motivation, anti-Humeanism | All metaethics skills |
| `metaethical-distinctions.md` | Realism/anti-realism, cognitivism/non-cognitivism, internalism/externalism, naturalism/non-naturalism, reductionism/non-reductionism, analytic/synthetic naturalism, radical/moderate expressivism, constitutive/normative | `phil-moral-realism`, `phil-moral-semantics`, `phil-normativity` |
| `moral-realism-taxonomy.md` | Moorean non-naturalism, Cornell realism, Jacksonian analytic functionalism, Railtonian reductive naturalism, Scanlonian quietist realism, Enochian robust realism, Mackie-style error theory, Joycean fictionalism, Blackburn-style quasi-realism, Gibbard-style normative expressivism | `phil-moral-realism` |
| `normativity-taxonomy.md` | Korsgaardian constitutivism, Smithian rationalism, Williams-style reasons internalism, Parfit-style reasons externalism, Scanlonian reasons fundamentalism, Darwallian second-person standpoint, Finlay-style telic semantics, Schroeder-style Humean reductionism | `phil-normativity`, `phil-moral-psychology` |

#### New Argument Forms in Detail (Metaphysics)

| Argument Form | Core Structure | Typical Use |
|---------|---------|---------|
| **Leibniz's Law** (leibniz-law) | Indiscernibility of identicals + discernibility of non-identicals | Philosophy of mind (counter to zombie argument), entity distinction arguments |
| **Conceivability argument** (conceivability-argument) | Conceivable ⇒ metaphysically possible ⇒ conclusion | Chalmers's zombie argument, the hard problem of consciousness |
| **Grounding argument** (grounding-argument) | X grounds Y ⇒ Y depends on X for its existence ⇒ ... | Supervenience arguments, realization arguments, reductionism/anti-reductionism |
| **Supervenience argument** (supervenience-argument) | B supervenes on A ⇒ if A does not vary, B cannot vary ⇒ ... | Philosophy of mind, moral metaphysics, aesthetics |
| **Recombination argument** (recombination-argument) | Reductive basis for modal realism | Lewis's modal realism, Humean supervenience |
| **Truthmaker argument** (truthmaker-argument) | Truth requires existence-conditions ⇒ commit to X as truthmaker | Truths about the past/future, negative truths, moral truths |
| **Sorites** (sorites) | n grains are not a heap → n+1 are also not → ... | Vagueness, persistence conditions, composition |
| **Four-dimensionalist argument** (four-dimensionalist) | Temporal parts + spatial analogy ⇒ cosmological perspective | Persistence, personal identity, Theseus's ship |
| **Mereological argument** (mereological-argument) | Formalization of part-whole relations | The Special Composition Question, nihilism |

#### New Argument Forms in Detail (Metaethics)

| Argument Form | Core Structure | Typical Use |
|---------|---------|---------|
| **Open question argument** (open-question-argument) | For any natural property N, "X is good iff X is N" → "But is X that is N good?" remains a meaningful open question → goodness ≠ any natural property | Moore against the naturalistic fallacy (*Principia Ethica*) |
| **Argument from queerness** (queerness-argument) | If moral facts exist → they must be non-natural entities with intrinsic normativity → such entities are ontologically queer → moral facts do not exist | Mackie's error theory (*Ethics: Inventing Right and Wrong*) |
| **Companions in guilt** (companions-in-guilt) | Domain X shares feature F with the moral domain → if one rejects moral reality because of F → must also reject X → X is clearly legitimate → the challenge to morality fails | Against Mackie's error theory (mathematics/modal companions) |
| **Disagreement argument** (disagreement-argument) | There is widespread, persistent moral disagreement → this disagreement is best explained by anti-realism → moral realism fails | Mackie's argument from relativity; epistemic peer challenge from disagreement |
| **Normative regress** (regress-argument) | The source of normativity demands further norm → regress → unless a "constitutive standard" blocks the regress | Korsgaard's constitutivism (*The Sources of Normativity*) |
| **Moral supervenience argument** (moral-supervenience) | Moral properties supervene on natural properties → if natural properties held fixed while moral properties varied → incoherent → supervenience requires explanation → challenges non-reductive realism | Blackburn's supervenience challenge; part of Mackie's queerness argument |

### Layer 1: Analytic Skills
**Rationale**: The core methodology of analytic philosophy — each skill corresponds to one independent method of philosophical analysis.

**When Used**: When the user needs to analyze a text, invoked by the upper orchestration layer or directly.

**Contents** (P0 — Core, subdomain-general):

| Skill | Function | Knowledge Dependencies Referenced |
|------|------|---------------|
| `phil-argument-reconstruct` | Transform natural-language arguments into standard premise-conclusion form | All argument-forms |
| `phil-charity-check` | Construct the strongest version of an argument, then evaluate | — |
| `phil-premise-detect` | Discover hidden assumptions, implicit premises, unstated presuppositions | `fallacy-catalog`, all argument-forms |
| `phil-counterexample` | Construct counterexamples targeting premises or the entire reasoning | All argument-forms |
| `phil-conceptual-analysis` | Necessary/sufficient condition analysis, dimension extraction | `glossary-*`, `metaphysical-distinctions` |
| `phil-citation-extract` | Extract and classify citations from a text by argumentative role, cross-reference with bibliography | `bibliography/INDEX.md` |

**Contents** (P1 — Extended, including metaphysics- and metaethics-specific):

| Skill | Function | Domain Knowledge Referenced | Subdomain |
|------|------|---------------|--------|
| `phil-dialectical-map` | Thesis-objection-response structural analysis | — | General |
| `phil-thought-experiment` | Evaluate the logical structure and argumentative force of thought experiments | `thought-experiment-templates` (per-domain subsets) | General |
| `phil-distinction-track` | Identify and track key conceptual distinctions | `metaphysical-distinctions`, `metaethical-distinctions` | General |
| `phil-modal-arg` | Evaluate possibility/necessity claims; analyze modal reasoning | `modal-logic-primer` | General / Metaphysics |
| `phil-analogy-check` | Assess the relevance and strength of analogical reasoning | All argument-forms | General |
| `phil-parity-check` | Check consistency of principle application across cases | — | General |
| **`phil-ontological-commitment`** | **Detect the existence commitments presupposed by an argument** | `ontological-categories`, `glossary-metaphysics` | **Metaphysics** |
| **`phil-identity-persistence`** | **Analyze identity conditions and persistence across time/worlds** | `modal-logic-primer`, `metaphysical-distinctions` | **Metaphysics** |
| **`phil-grounding-check`** | **Analyze grounding, supervenience, realization, and other meta-ontological relations** | `glossary-metaphysics`, `ontological-categories` | **Metaphysics** |
| **`phil-conceivability-arg`** | **Evaluate the conceivability → possibility → actuality chain** | `modal-logic-primer`, all metaphysical argument-forms | **Metaphysics** |
| **`phil-moral-realism`** | **Analyze moral realism/anti-realism/error theory/non-cognitivism arguments** | `moral-realism-taxonomy`, `glossary-metaethics` | **Metaethics** |
| **`phil-normativity`** | **Analyze the source and structure of normativity; categorical/hypothetical imperatives** | `normativity-taxonomy`, `glossary-metaethics` | **Metaethics** |
| **`phil-moral-semantics`** | **Analyze moral language — cognitivism/expressivism/prescriptivism** | `glossary-metaethics`, `metaethical-distinctions` | **Metaethics** |
| **`phil-moral-psychology`** | **Analyze the moral judgment–motivation relation — internalism/externalism debates** | `glossary-metaethics`, `normativity-taxonomy` | **Metaethics** |
| `phil-intuition-pump` | Identify rhetorical appeals to intuition | `fallacy-catalog` | General |
| **`phil-causation-analyze`** | **Identify the theoretical affiliation and assess the strength of causal claims** | `causation-taxonomy`, `glossary-metaphysics` | **Metaphysics** (P2) |
| **`phil-essence-detect`** | **Detect the use of the essence/accident distinction** | `modal-logic-primer`, `glossary-metaphysics` | **Metaphysics** (P2) |
| **`phil-natural-kind-analyze`** | **Analyze arguments concerning natural kind classification** | `glossary-metaphysics`, `ontological-categories` | **Metaphysics** (P2) |
| **`phil-moral-disagreement`** | **Evaluate arguments from moral disagreement and their implications for realism** | `glossary-metaethics`, `moral-realism-taxonomy` | **Metaethics** (P2) |
| **`phil-moral-epistemology`** | **The possibility of moral knowledge — intuitionism/coherentism/reliabilism** | `glossary-metaethics`, `metaethical-distinctions` | **Metaethics** (P2) |
| **`phil-moral-supervenience`** | **Supervenience of moral properties on natural properties and the explanatory burden** | `glossary-metaethics`, `glossary-metaphysics` | **Metaethics** (P2) |
| `phil-methodology` | Methodological reflection | All references, `philosophers-db` | General (P2) |
| `phil-contextualize` | Intellectual history contextualization | `philosophers-db`, ARS `deep-research` | General (P2) |

### Layer 2: Orchestration Layer
**Rationale**: A single analytical method is often insufficient — the user needs a complete analysis pipeline. The orchestration layer composes Layer 1 analytic skills into end-to-end workflows.

**When Used**: When the user invokes `phil:reconstruct（分析）+ phil:evaluate（评价）` or when an Agent auto-schedules.

**Contents**:
- `commandsphil:reconstruct（分析）+ phil:evaluate（评价）.md` — Orchestration entry point, invokes the following workflow:

**Metaphysics-Enhanced Orchestration**: When `phil-analyze` detects metaphysical features in the text (ontological language, modal operators, identity statements, causal assertions), it automatically incorporates the relevant metaphysical skills into the pipeline.

**Metaethics-Enhanced Orchestration**: When `phil-analyze` detects metaethical features in the text (moral language analysis, normative statements, realism/anti-realism claims, motivational internalism/externalism language), it automatically incorporates the relevant metaethical skills into the pipeline.

### Layer 3: Agent Layer (Dialogic Agents)
**Rationale**: Some philosophical analysis methods are better suited to dialogue (Socratic, dialectical) than to one-off analysis reports.

**When Used**: When the user needs interactive exploration of philosophical questions.

**Contents**:
- **`agents/metaphysician.md`** — **Metaphysical analyst: Socratic dialogue specialized in ontological commitments, conceivability reasoning, grounding relations, and other meta-metaphysical questions**
- **`agents/metaethicist.md`** — **Metaethical analyst: Socratic dialogue specialized in moral realism, normative reasons, moral semantics, and other metaethical questions**
- **`agents/phil-writer.md`** — **[Phase 6] Philosophy writer: generates manuscripts in three modes (outline/draft/revision) with 7 philosophy-aware prose standards**
- **`agentsphil:reviewer.md`** — **[Phase 6] Philosophy reviewer: evaluates manuscripts across 8 review dimensions; supports standard and perspective-specific reviews**
- **`agentsphil:commentator.md`** — **[Phase 6] Philosophy commentator: critical engagement identifying assumptions, missing distinctions, hidden commitments, and dialectical blind spots**
- **`agents/phil-orchestrator.md`** — **[Phase 6] Pipeline orchestrator: coordinates the 5-stage writing pipeline (question → literature → outline → draft → final) with quality gates**
- **`agents/phil-tutor.md`** — **[New] Tutor agent: dialogic reading mentor — asks about the user's reading, probes understanding Socratically, identifies gaps, and recommends literature with individualized rationale**

### Layer 4: Cross-Layer Interface (ARS Bridge)
**Rationale**: The analysis outputs of this system must flow into ARS's writing pipeline to produce papers.

**When Used**: When transitioning from the analysis phase to the writing phase.

**Bridge Mechanisms**:
- Analysis report (this system) → Paper outline (ARS `academic-paper plan`)
- Analysis report (this system) → Paper body (ARS `academic-paper full`)
- Concept map (this system) → Literature review (ARS `deep-research lit-review`)
- Dialectical tree (this system) → Revision strategy (ARS `revision-coach`)
- Ontological commitment audit (this system) → Ontological presupposition statement in paper introduction (ARS `academic-paper`)
- Metaethical stance audit (this system) → Metaethical presupposition statement in paper methodology (ARS `academic-paper`)

### Layer 5: Writing and Production Layer (Phase 6)
**Rationale**: The analysis outputs from Layers 0-2 require philosophy-specialized writing, review, and commentary agents to produce publishable manuscripts. Generic academic writing tools (ARS) lack the domain-specific standards needed for philosophical prose — argument integrity, conceptual precision, modal accuracy, dialectical transparency.

**When Used**: When transitioning from analysis to production — generating outlines, drafting manuscripts, reviewing for philosophical rigor, and managing the full writing pipeline.

**Contents**:
- `agentsphil:writer.md` — Philosophy writer agent with three modes:
  - **Outline mode**: Transforms analysis outputs (argument reconstructions, concept maps, dialectical trees) into structured paper outlines with thesis, section plan, distinction inventory, and objection mapping.
  - **Draft mode**: Section-by-section manuscript drafting with 7 philosophy-aware prose standards (argument transparency, conceptual precision, modal accuracy, dialectical positioning, distinction preservation, counterexample resilience, ontological explicitness).
  - **Revision mode**: Prioritized revision based on reviewer findings (structural → conceptual → dialectical → modal → stylistic) with change tracking.
- `agentsphil:reviewer.md` — Philosophy reviewer agent with two modes:
  - **Standard review**: 8-dimension evaluation (argument validity, charity, conceptual clarity, modal rigor, counterexample resilience, dialectical completeness, ontological commitment transparency, methodological consistency) with severity grading and revision priority matrix.
  - **Perspective review**: Review from a specified philosophical stance (Quinean, Lewisian, Kripkean, Finean, Mackiean, Expressivist, etc.), distinguishing perspective-dependent from perspective-neutral findings.
- `agentsphil:commentator.md` — Philosophy commentator agent with three modes:
  - **Critical commentary**: Identifies unexamined assumptions, alternative interpretations, missing distinctions, undefended inferences, hidden commitments, and dialectical blind spots.
  - **Response paper**: Writes a response from a specified philosophical position.
  - **Dialectical positioning**: Situates work within the broader debate landscape and intellectual lineage.
- `agents/phil-orchestrator.md` — Pipeline orchestrator coordinating the full 5-stage workflow:
  - Stage 1: Philosophical question formulation (dialogic agent Socratic clarification)
  - Stage 2: Literature review and analysis (phil-* analysis chain + ars-deep-research)
  - Stage 3: Outline refinement (phil-writer outline mode + optional phil-reviewer structural check)
  - Stage 4: Draft generation (phil-writer draft mode with section-boundary quality checks)
  - Stage 5: Final manuscript (phil-reviewer → phil-writer revision → loop until quality threshold met)
  
  Each stage has a quality gate with explicit pass/fail criteria. The orchestrator recommends advance/revise/return; the user decides.

**Relationship to ARS Bridge (Layer 4)**: Layer 5 handles the core philosophical writing, review, and commentary. The ARS Bridge (Layer 4) remains available for supplementary infrastructure: literature search (`ars-deep-research`), format conversion (`ars-format-convert`), citation verification (`ars-citation-check`). Layer 5 agents are designed to function without ARS but can optionally invoke ARS capabilities for specific tasks.

```
┌─────────────────────────────────────────────────────┐
│  Layer 5: Writing & Production (Phase 6)            │
│   phil-writer  phil-reviewer  phil-commentator      │
│   phil-orchestrator (5-stage pipeline)              │
├─────────────────────────────────────────────────────┤
│  Layer 4: ARS Bridge  ──  analysis → ARS pipeline  │
├─────────────────────────────────────────────────────┤
│  Layer 3: Dialogic Agents                           │
│   metaphysician (metaphysical dialogue)             │
│   metaethicist (metaethical dialogue)                │
├─────────────────────────────────────────────────────┤
│  Layer 2: Orchestration                             │
│   phil-analyze (composes Layer 1)                    │
├─────────────────────────────────────────────────────┤
│  Layer 1: Analytic Skills                           │
│   ┌───────────────────    ┌──────────────────────┐  │
│   │ General Analysis     │ Metaphysical Analysis │  │
│   │ reconstruct          │ ontological-commitment│  │
│   │ charity              │ identity-persistence  │  │
│   │ premise-detect       │ grounding-check       │  │
│   │ counterexample       │ conceivability-arg    │  │
│   │ conceptual-analysis  │ causation-analyze     │  │
│   │ dialectical-map      │ essence-detect        │  │
│   │ thought-experiment   │ natural-kind-analyze  │  │
│   │ distinction-track    │                       │  │
│   │ modal-arg            │                       │  │
│   │ analogy-check        │                       │  │
│   │ parity-check         │                       │  │
│   │ intuition-pump       │                       │  │
│   │ methodology          │                       │  │
│   │ contextualize        │                       │  │
│   └───────────────────    └──────────────────────┘  │
│   ┌────────────────────────────────────────────────┐ │
│   │ Metaethical Analysis                           │ │
│   │ moral-realism        normativity               │ │
│   │ moral-semantics      moral-psychology          │ │
│   │ moral-disagreement   moral-epistemology        │ │
│   │ moral-supervenience                            │ │
│   └────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│  Layer 0: Knowledge Base                            │
│   ┌───────────────    ┌─────────────────────────┐   │
│   │ General Knowledge│ Metaphysical Knowledge   │   │
│   │ fallacy-catalog  │ glossary-metaphysics     │   │
│   │ fallacy-catalog  │ metaphysical-distinctions│   │
│   │ argument-forms   │ ontological-categories   │   │
│   │ (general subset) │ modal-logic-primer       │   │
│   │                 │ causation-taxonomy       │   │
│   │                 │ argument-forms (metaphys) │   │
│   │                 │ argument-forms (metaeth)  │   │
│   └───────────────    └─────────────────────────┘   │
│   ┌────────────────────────────────────────────┐    │
│   │ Metaethical Knowledge                      │    │
│   │ glossary-metaethics                        │    │
│   │ metaethical-distinctions                   │    │
│   │ moral-realism-taxonomy                     │    │
│   │ normativity-taxonomy                       │    │
│   └────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────┤
│  ARS Layer (Existing, Not Re-implemented)            │
│   deep-research  academic-paper  reviewer  pipeline │
└─────────────────────────────────────────────────────┘
```

---

## 5. Dependency Graph

### 5.1 General Skill Dependencies

```
phil-charity-check
    ↑ depends on [phil-argument-reconstruct] output as input

phil-premise-detect
    ↑ depends on [phil-argument-reconstruct] output
    ↑ references [references/fallacy-catalog.md]

phil-counterexample
    ↑ depends on [phil-argument-reconstruct] output (needs standard form)
    ↑ depends on [phil-premise-detect] output (knows which premises are vulnerable)
    ↑ references [references/argument-forms/] (counterexample strategy varies by form)

phil-conceptual-analysis
    ↑ independent (accepts text/concept as input)
    ↑ references [references/glossary-*.md]
    ↑ references [references/metaphysical-distinctions.md]

phil-dialectical-map
    ↑ depends on [phil-argument-reconstruct] (needs thesis set)
    ↑ optionally depends on [phil-conceptual-analysis] (tracks conceptual evolution)

phil-distinction-track
    ↑ depends on [phil-conceptual-analysis] for conceptual distinction capability
    ↑ or runs independently
    ↑ references [references/metaphysical-distinctions.md]

phil-thought-experiment
    ↑ depends on [phil-argument-reconstruct] (thought experiments require argument extraction)
    ↑ references [references/thought-experiment-templates.md]

phil-modal-arg
    ↑ depends on [phil-argument-reconstruct] (needs logical form)
    ↑ references [references/argument-forms/]
    ↑ references [references/modal-logic-primer.md]

phil-analogy-check
    ↑ independent (but can compose with [phil-argument-reconstruct])
    ↑ references [references/argument-forms/]

phil-parity-check
    ↑ depends on [phil-argument-reconstruct] (needs standard forms of multiple arguments)

phil-intuition-pump
    ↑ independent (text scan)
    ↑ references [references/fallacy-catalog.md]

phil-methodology
    ↑ depends on [phil-argument-reconstruct] (needs to know argument type to assess method)
    ↑ references [references/philosophers-db/]

phil-contextualize
    ↑ independent (externally knowledge-intensive)
    ↑ depends on ARS [deep-research] for literature support
```

### 5.2 Metaphysics-Specific Skill Dependencies

```
phil-ontological-commitment
    ↑ depends on [phil-argument-reconstruct] (needs standard form to extract commitments)
    ↑ depends on [phil-premise-detect] (hidden premises often contain key commitments)
    ↑ references [references/ontological-categories.md]
    ↑ references [references/glossary-metaphysics.md]

phil-identity-persistence
    ↑ depends on [phil-argument-reconstruct] (needs standard form of identity claims)
    ↑ depends on [phil-modal-arg] (transworld identity depends on modal reasoning)
    ↑ references [references/modal-logic-primer.md]
    ↑ references [references/metaphysical-distinctions.md]

phil-grounding-check
    ↑ depends on [phil-argument-reconstruct] (grounding claims need explicitation)
    ↑ references [references/glossary-metaphysics.md]
    ↑ references [references/ontological-categories.md]

phil-conceivability-arg
    ↑ depends on [phil-modal-arg] (conceivability is a modal concept)
    ↑ depends on [phil-argument-reconstruct] (needs standard form of inferential chain)
    ↑ references [references/modal-logic-primer.md]
    ↑ references [references/argument-forms/conceivability-argument.md]

phil-causation-analyze    (P2)
    ↑ depends on [phil-argument-reconstruct]
    ↑ references [references/causation-taxonomy.md]
    ↑ references [references/glossary-metaphysics.md]

phil-essence-detect       (P2)
    ↑ depends on [phil-modal-arg] (essence is a modal concept)
    ↑ depends on [phil-conceptual-analysis]
    ↑ references [references/modal-logic-primer.md]
    ↑ references [references/glossary-metaphysics.md]

phil-natural-kind-analyze  (P2)
    ↑ depends on [phil-conceptual-analysis]
    ↑ depends on [phil-essence-detect]
    ↑ references [references/glossary-metaphysics.md]
    ↑ references [references/ontological-categories.md]
```

### 5.3 Metaethics-Specific Skill Dependencies

```
phil-moral-realism
    ↑ depends on [phil-argument-reconstruct] (needs standard form of moral realism/anti-realism arguments)
    ↑ depends on [phil-premise-detect] (moral arguments often contain implicit metaethical presuppositions)
    ↑ references [references/moral-realism-taxonomy.md]
    ↑ references [references/glossary-metaethics.md]
    ↑ references [references/metaethical-distinctions.md]

phil-normativity
    ↑ depends on [phil-argument-reconstruct] (normative statements need explicitation)
    ↑ references [references/normativity-taxonomy.md]
    ↑ references [references/glossary-metaethics.md]

phil-moral-semantics
    ↑ depends on [phil-conceptual-analysis] (moral concepts require a semantic analysis framework)
    ↑ depends on [phil-argument-reconstruct] (Frege-Geach problem, etc., require argument structure)
    ↑ references [references/glossary-metaethics.md]
    ↑ references [references/metaethical-distinctions.md]

phil-moral-psychology
    ↑ depends on [phil-argument-reconstruct] (motivational internalism/externalism arguments need standard form)
    ↑ references [references/glossary-metaethics.md]
    ↑ references [references/normativity-taxonomy.md]

phil-moral-disagreement  (P2)
    ↑ depends on [phil-argument-reconstruct] (disagreement arguments need structural analysis)
    ↑ depends on [phil-moral-realism] (how disagreement bears on realist stances)
    ↑ references [references/glossary-metaethics.md]
    ↑ references [references/argument-forms/disagreement-argument.md]

phil-moral-epistemology  (P2)
    ↑ depends on [phil-moral-realism] (the possibility of moral knowledge depends on one's realist stance)
    ↑ depends on [phil-conceptual-analysis]
    ↑ references [references/glossary-metaethics.md]
    ↑ references [references/metaethical-distinctions.md]

phil-moral-supervenience  (P2)
    ↑ depends on [phil-moral-realism] (the significance of the supervenience problem depends on one's metaethical stance)
    ↑ depends on [phil-grounding-check] (supervenience is a special form of grounding)
    ↑ references [references/glossary-metaethics.md]
    ↑ references [references/glossary-metaphysics.md]
```

### 5.4 Metaethics Skill Cross-Domain Connections

```
Core Dependency Chain (Metaethics Analysis):

Raw Text (metaethical argument)
   ↓
phil-argument-reconstruct  ←── [argument-forms/metaethics subset]
   ↓
   ├──→ phil-moral-realism       ←── [realism spectrum, glossary, distinctions]
   │      ↓
   │      ├──→ phil-moral-disagreement  ←── [disagreement argument template]
   │      ├──→ phil-moral-epistemology  ←── [glossary, distinctions]
   │      └──→ phil-moral-supervenience ←── [glossary, grounding analysis]
   ├──→ phil-moral-semantics     ←── [glossary, distinctions]
   │      ↓
   │      └──→ phil-moral-realism (semantic commitments → realist stance)
   ├──→ phil-normativity         ←── [normativity taxonomy, glossary]
   │      ↓
   │      └──→ phil-moral-psychology (normative reasons → motivation)
   └──→ phil-moral-psychology    ←── [glossary, normativity taxonomy]
          ↓
phil-dialectical-map  ←── [integrates metaethical dialectical structure]
   ↓
phil-conceptual-analysis  ←── [metaethical-distinctions]
   ↓
phil-distinction-track
   ↓
ARS Bridge → Paper writing
```

### 5.5 Metaphysics Skill Cross-Domain Connections

```
Core Dependency Chain (Metaphysics Analysis):

Raw Text (metaphysical argument)
   ↓
phil-argument-reconstruct  ←── [argument-forms/metaphysics subset]
   ↓
   ├──→ phil-modal-arg   ←── [modal-logic-primer]
   │      ↓
   │      ├──→ phil-conceivability-arg  ←── [conceivability argument template]
   │      ├──→ phil-identity-persistence ←── [metaphysical distinctions]
   │      └──→ phil-essence-detect      ←── [modal logic]
   ├──→ phil-ontological-commitment ←── [ontological categories, glossary]
   ├──→ phil-grounding-check        ←── [glossary, categories]
   ├──→ phil-causation-analyze      ←── [causal taxonomy]
   └──→ phil-natural-kind-analyze   ←── [conceptual analysis → essence detection]
          ↓
phil-dialectical-map  ←── [integrates metaphysical dialectical structure]
   ↓
phil-conceptual-analysis  ←── [metaphysical-distinctions]
   ↓
phil-distinction-track
   ↓
ARS Bridge → Paper writing
```

### 5.6 Skills Kept Independent

The following skills have **no direct dependencies** between each other, preserving independence for maintainability:
- Within the general layer: consistent with the above
- Metaphysics layer: `phil-ontological-commitment` ↔ `phil-causation-analyze` (ontological commitment is independent of causal analysis)
- Metaphysics layer: `phil-conceivability-arg` ↔ `phil-grounding-check` (conceivability is not grounding)
- Cross-layer: `phil-causation-analyze` ↔ `phil-parity-check` (causal analysis is independent of reasoning parity)
- Metaethics layer: `phil-moral-realism` ↔ `phil-moral-psychology` (realist stance is independent of moral motivation analysis)
- Metaethics layer: `phil-moral-semantics` ↔ `phil-normativity` (semantic analysis is independent of normativity analysis)
- Cross-domain: `phil-moral-supervenience` ↔ `phil-grounding-check` (moral supervenience is a special case of grounding analysis but not directly dependent)

Independence means: rewriting one Skill will not break another.

---

## 6. Research Flow

### 6.1 Complete Analytic Philosophy Writing Pipeline (with Metaphysics and Metaethics Branches)

```
Phase 1: Reading and Comprehension
┌──────────────────────────────────────────────────────────┐
│  Read PDF / Text                                         │
│    ↓                                                     │
│  Text classifier: detect domain features                 │
│  Metaphysical: (ontological language? modal operators?   │
│                identity statements? causal assertions?)  │
│  Metaethical: (moral language analysis? normative        │
│                statements? realism/anti-realism claims?  │
│                motivational language?)                   │
│    ↓                           ↓                          │
│  [phil-contextualize]    ARS: deep-research               │
│  Intellectual history     Background literature search    │
│  contextualization        (optional)                      │
│  (optional)                                               │
└──────────────────────────────────────────────────────────┘
          ↓
Phase 1b: Tutoring and Reading Guidance (optional, invoked via phil:tutor)
┌──────────────────────────────────────────────────────────┐
│  [phil:tutor]           Socratic dialogue about the text  │
│    → Ask what user is reading and thinking                │
│    → Probe understanding, identify blind spots            │
│    → Recommend literature tailored to gaps                │
│    → Plan next steps (read more? run phil:reconstruct?)   │
│    ↕                                                     │
│  (Internal: may invoke phil-citation-extract to mine      │
│   citation candidates from the user's current text)       │
└──────────────────────────────────────────────────────────┘
          ↓
Phase 2: Argument Analysis
┌──────────────────────────────────────────────────────────┐
│  [phil-argument-reconstruct]    Argument reconstruction   │
│                                 → standard form           │
│    ↓                                                     │
│  [phil-charity-check]          Principle of charity audit │
│    ↓                                                     │
│  [phil-premise-detect]         Implicit premise detection │
│    ↓                                                     │
│  [phil-modal-arg]              Modal argument analysis    │
│    ↓               ↓                                     │
│  ┌──────────────────────────────────────┐                │
│  │ Metaphysics Branch (activated when   │                │
│  │ relevant features detected)          │                │
│  │                                      │                │
│  │  [phil-ontological-commitment]       │                │
│  │  Ontological commitment detection    │                │
│  │  → ontological category              │                │
│  │     classification                    │                │
│  │                                      │                │
│  │  [phil-identity-persistence]         │                │
│  │  Cross-time/world identity condition │                │
│  │  analysis                            │                │
│  │                                      │                │
│  │  [phil-conceivability-arg]           │                │
│  │  Conceivability → possibility        │                │
│  │  chain evaluation                    │                │
│  └──────────────────────────────────────┘                │
└──────────────────────────────────────────────────────────┘
          ↓
Phase 3: Conceptual Analysis
┌──────────────────────────────────────────────────────────┐
│  [phil-conceptual-analysis]    Conceptual clarification   │
│                                 and distinctions          │
│    ↓                                                     │
│  [phil-distinction-track]      Track key distinctions     │
│    ↓                                                     │
│  ┌──────────────────────────────────────┐                │
│  │ Metaphysics Branch (optional)         │                │
│  │                                      │                │
│  │  [phil-grounding-check]              │                │
│  │  Grounding/supervenience/            │                │
│  │  realization relation analysis       │                │
│  │                                      │                │
│  │  [phil-essence-detect] (P2)          │                │
│  │  Essentialist claim detection        │                │
│  │  and analysis                        │                │
│  │                                      │                │
│  │  [phil-natural-kind-analyze] (P2)    │                │
│  │  Natural kind classification         │                │
│  │  argument analysis                   │                │
│  └──────────────────────────────────────┘                │
│  ┌──────────────────────────────────────┐                │
│  │ Metaethics Branch (optional)          │                │
│  │                                      │                │
│  │  [phil-moral-realism]                │                │
│  │  Moral realism/anti-realism          │                │
│  │  argument analysis                   │                │
│  │                                      │                │
│  │  [phil-moral-semantics]              │                │
│  │  Moral language and semantic         │                │
│  │  analysis                            │                │
│  │                                      │                │
│  │  [phil-normativity]                  │                │
│  │  Sources and structure of            │                │
│  │  normativity analysis                │                │
│  │                                      │                │
│  │  [phil-moral-psychology]             │                │
│  │  Moral judgment–motivation           │                │
│  │  relation analysis                   │                │
│  └──────────────────────────────────────┘                │
│    ↓                                                     │
│  [phil-thought-experiment]     Thought experiment        │
│                                 analysis                  │
│    ↓                                                     │
│  [phil-intuition-pump]         Intuition pump detection  │
│    ↓                                                     │
│  [phil-analogy-check]          Analogical argument       │
│                                 evaluation                │
│    ↓                                                     │
│  [phil-causation-analyze] (P2) Causal claim analysis     │
└──────────────────────────────────────────────────────────┘
          ↓
Phase 4: Critical Evaluation
┌──────────────────────────────────────────────────────────┐
│  [phil-counterexample]         Counterexample generation  │
│                                 and evaluation            │
│    ↓                                                     │
│  [phil-parity-check]           Reasoning parity check     │
│    ↓                                                     │
│  [phil-dialectical-map]        Dialectical tree:         │
│                                 objection-response        │
│                                 structure                 │
│    ↓                                                     │
│  [phil-methodology]            Methodological reflection  │
│                                 (optional)                │
└──────────────────────────────────────────────────────────┘
          ↓
Phase 5: Integrated Report
┌──────────────────────────────────────────────────────────┐
│  Generate analysis report (including ontological audit   │
│  section)                                                │
│    ↓                                                     │
│  [phil-dialectical-map]        Visualize dialectical     │
│                                 structure                 │
└──────────────────────────────────────────────────────────┘
          ↓
Phase 6: Writing & Production (5-Stage Pipeline)
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Stage 1: 哲学提问 (Question Formulation)                │
│  ┌────────────────────────────────────────────────────┐  │
│  │ metaphysician / metaethicist (Socratic dialogue)   │  │
│  │ → Refined question + sub-questions + scope        │  │
│  └────────────────────────────────────────────────────┘  │
│    ↓                                                     │
│  Stage 2: 参考文献阅读与分析 (Literature & Analysis)      │
│  ┌────────────────────────────────────────────────────┐  │
│  │ ars-deep-research → phil-reconstruct →             │  │
│  │ phil-charity → phil-premises → phil-dialectic →    │  │
│  │ phil-contextualize → domain-specific phil-* skills │  │
│  │ → Literature package + dialectical map             │  │
│  └────────────────────────────────────────────────────┘  │
│    ↓                                                     │
│  Stage 3: 打磨大纲 (Outline Refinement)                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │ phil-writer (outline mode) → Detailed outline      │  │
│  │   with thesis, section plan, distinction inventory │  │
│  │ Optional: phil-reviewer structural check           │  │
│  └────────────────────────────────────────────────────┘  │
│    ↓                                                     │
│  Stage 4: 生成初稿 (Draft Generation)                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │ phil-writer (draft mode) → Section-by-section      │  │
│  │   with prose quality checks at each boundary       │  │
│  │ → Complete manuscript draft + Notes to Self        │  │
│  └────────────────────────────────────────────────────┘  │
│    ↓                                                     │
│  Stage 5: 生成终稿 (Final Manuscript)                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │ phil-reviewer (standard + optional perspective)    │  │
│  │   → phil-writer (revision mode) → loop until       │  │
│  │   all fatal findings resolved                      │  │
│  │ Optional: phil-commentator critical engagement     │  │
│  │ → Final manuscript + review reports + revision log │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  Quality Gates: Explicit pass/fail at each stage.        │
│  Orchestrator recommends; user decides.                  │
└──────────────────────────────────────────────────────────┘
```

### 6.2 Fast Paths

```
Fast Metaphysics Analysis:
  Text → [phil-ontological-commitment] → Ontological commitment report
      → [phil-conceivability-arg]      → Conceivability chain evaluation

Fast Identity Analysis:
  Identity claim → [phil-identity-persistence] → Persistence condition report
                 → [phil-modal-arg]            → Transworld identity evaluation

Fast Grounding Analysis:
  Grounding/supervenience statement → [phil-grounding-check] → Relation topology map

Fast Metaethics Analysis:
  Moral argument → [phil-moral-realism]    → Realist stance analysis
                → [phil-moral-semantics]   → Semantic structure evaluation

Fast Normativity Analysis:
  Ought/reason claim → [phil-normativity]    → Normative structure analysis
                     → [phil-moral-psychology] → Motivation/reason relation evaluation
```

### 6.3 Entry Points per Skill

| User Need | Triggering Command | Skill Used |
|---------|---------|-----------|
| "Reconstruct this argument" | `phil:reconstruct` | `phil-argument-reconstruct` |
| "Check the principle of charity" | `phil:reconstruct` | `phil-charity-check` |
| "Find hidden premises" | `phil:reconstruct` | `phil-premise-detect` |
| "Generate counterexamples" | `phil:evaluate` | `phil-counterexample` |
| "Analyze this concept" | `phil:reconstruct` | `phil-conceptual-analysis` |
| "Analyze this thought experiment" | `phil:reconstruct` | `phil-thought-experiment` |
| "Draw a dialectical tree" | `phil:evaluate` | `phil-dialectical-map` |
| "Track key distinctions" | `phil:reconstruct` | `phil-distinction-track` |
| "Perform a full analysis of this text" | `phil:reconstruct（分析）+ phil:evaluate（评价）` | Orchestration of all Layer 1 Skills |
| **"Check ontological commitments"** | **`phil:reconstruct`** | **`phil-ontological-commitment`** |
| **"Analyze identity conditions"** | **`phil:reconstruct`** | **`phil-identity-persistence`** |
| **"Analyze grounding relations"** | **`phil:reconstruct`** | **`phil-grounding-check`** |
| **"Evaluate a conceivability argument"** | **`phil:reconstruct`** | **`phil-conceivability-arg`** |
| **"Analyze causal claims"** | **`phil:reconstruct`** | **`phil-causation-analyze`** |
| **"Detect essentialism"** | **`phil:reconstruct`** | **`phil-essence-detect`** |
| **"Analyze natural kind arguments"** | **`phil:reconstruct`** | **`phil-natural-kind-analyze`** |
| **"Analyze moral realist stance"** | **`phil:reconstruct`** | **`phil-moral-realism`** |
| **"Analyze normative claims"** | **`phil:reconstruct`** | **`phil-normativity`** |
| **"Analyze moral language"** | **`phil:reconstruct`** | **`phil-moral-semantics`** |
| **"Analyze moral motivation"** | **`phil:reconstruct`** | **`phil-moral-psychology`** |
| **"Analyze moral disagreement"** | **`phil:reconstruct`** | **`phil-moral-disagreement`** |
| **"Analyze moral knowledge"** | **`phil:reconstruct`** | **`phil-moral-epistemology`** |
| **"Analyze moral supervenience"** | **`phil:reconstruct`** | **`phil-moral-supervenience`** |
| **"Write an outline for this analysis"** | **`phil:write outline`** | **`phil-writer`** |
| **"Draft this paper"** | **`phil:write draft`** | **`phil-writer`** |
| **"Revise based on reviewer feedback"** | **`phil:write revision`** | **`phil-writer`** |
| **"Review this manuscript"** | **`phil:review`** | **`phil-reviewer`** |
| **"Comment on this argument"** | **`phil:comment`** | **`phil-commentator`** |
| **"Run the full writing pipeline"** | **`phil:pipeline`** | **`phil-orchestrator`** |
| **"Discuss my reading and get recommendations"** | **`phil:tutor`** | **`phil-tutor`** (agent) + `phil-citation-extract` (skill) |

---

## 7. Skill Taxonomy

### 7.1 Classification by Analytic Dimension

| Category | Rationale | Skills Included |
|------|---------|------------|
| **Reading** | Transform text into analyzable structured input | `phil-argument-reconstruct`, `phil-contextualize`, `phil-citation-extract` |
| **Reasoning Analysis** | Check the quality, completeness, and fairness of reasoning | `phil-charity-check`, `phil-premise-detect`, `phil-parity-check`, `phil-modal-arg`, `phil-analogy-check` |
| **Conceptual Analysis** | Clarify and distinguish core philosophical concepts | `phil-conceptual-analysis`, `phil-distinction-track`, `phil-intuition-pump` |
| **Critical Evaluation** | Generate and assess objections | `phil-counterexample`, `phil-thought-experiment`, `phil-dialectical-map` |
| **Metaphysical Analysis** | Uncover and assess ontological commitments, grounding relations, identity conditions, modal reasoning | `phil-ontological-commitment`, `phil-identity-persistence`, `phil-grounding-check`, `phil-conceivability-arg`, `phil-causation-analyze`, `phil-essence-detect`, `phil-natural-kind-analyze` |
| **Metaethical Analysis** | Analyze moral realist stances, normative structures, moral semantics, moral psychology | `phil-moral-realism`, `phil-normativity`, `phil-moral-semantics`, `phil-moral-psychology`, `phil-moral-disagreement`, `phil-moral-epistemology`, `phil-moral-supervenience` |
| **Methodology** | Reflect on and situate philosophical methods | `phil-methodology` |
| **Writing** | Transform analysis into papers | `phil-writer` (outline/draft/revision), `phil-orchestrator` (pipeline coordination) |
| **Review** | Evaluate manuscripts for philosophical rigor | `phil-reviewer` (8-dimension standard + perspective review) |
| **Commentary** | Critical engagement beyond review | `phil-commentator` (assumptions, distinctions, blind spots, positioning) |
| **Citation** | Citation management | ARS [`citation-check`] (not re-implemented) |
| **Translation** | Multilingual output | ARS [`abstract-only`] (not re-implemented) |
| **Project Management** | Pipeline orchestration | ARS [`academic-pipeline`] (not re-implemented) |
| **Orchestration** | Composition of cross-Layer 1 skills | `phil-analyze`, Agents |

### 7.2 Classification by Methodological Depth

| Level | Description | Skills |
|------|------|--------|
| **Descriptive** | Describe what arguments, concepts, and commitments are present in the text | `phil-argument-reconstruct`, `phil-contextualize`, `phil-distinction-track`, `phil-ontological-commitment`, `phil-essence-detect`, `phil-moral-realism`, `phil-moral-semantics`, `phil-citation-extract` |
| **Normative** | Evaluate whether an argument succeeds | `phil-charity-check`, `phil-premise-detect`, `phil-modal-arg`, `phil-parity-check`, `phil-analogy-check`, `phil-intuition-pump`, `phil-counterexample`, `phil-thought-experiment`, `phil-conceivability-arg`, `phil-grounding-check`, `phil-identity-persistence`, `phil-causation-analyze`, `phil-natural-kind-analyze`, `phil-normativity`, `phil-moral-psychology`, `phil-moral-disagreement`, `phil-moral-epistemology`, `phil-moral-supervenience` |
| **Generative** | Generate new arguments or new objections | `phil-counterexample`, `phil-dialectical-map` |
| **Meta-level** | Reflect on methodology itself | `phil-methodology` |

### 7.3 Classification by Domain

| Domain Coverage | Skills |
|---------|--------|
| **General** (cross-subdomain) | `phil-argument-reconstruct`, `phil-charity-check`, `phil-premise-detect`, `phil-counterexample`, `phil-conceptual-analysis`, `phil-dialectical-map`, `phil-thought-experiment`, `phil-distinction-track`, `phil-analogy-check`, `phil-parity-check`, `phil-intuition-pump`, `phil-methodology`, `phil-contextualize`, `phil-citation-extract` |
| **Metaphysics** (including modality) | `phil-modal-arg`, `phil-ontological-commitment`, `phil-identity-persistence`, `phil-grounding-check`, `phil-conceivability-arg`, `phil-causation-analyze`, `phil-essence-detect`, `phil-natural-kind-analyze` |
| **Metaethics** | `phil-moral-realism`, `phil-normativity`, `phil-moral-semantics`, `phil-moral-psychology`, `phil-moral-disagreement`, `phil-moral-epistemology`, `phil-moral-supervenience` |
| **Reserved** (architecturally accommodable) | `phil-ethics-ai`, `phil-political-arg`, `phil-phenomenology`, `phil-existential`, `phil-action-theory`, `phil-epistemology` |

---

## 8. Naming Conventions

### 8.1 Skill Naming

```
Format: phil-<domain>-<verb>
Prefix: phil-  (denotes analytic philosophy domain)
Verbs: check, detect, track, map, analyze, reconstruct, etc.

The domain is a singular noun + verb that further specifies the analytic action:

General Skills:
  phil-argument-reconstruct    ✅
  phil-charity-check           ✅
  phil-premise-detect          ✅
  phil-counterexample          ✅ (not phil-counterexample-generate)
  phil-conceptual-analysis     ✅
  phil-dialectical-map         ✅
  phil-thought-experiment      ✅
  phil-distinction-track       ✅
  phil-modal-arg               ✅ (abbreviated for modal argument)
  phil-analogy-check           ✅
  phil-parity-check            ✅
  phil-intuition-pump          ✅
  phil-methodology             ✅ (no verb, as it is a domain)
  phil-contextualize           ✅ (verb form)

Metaphysics Skills:
  phil-ontological-commitment  ✅ (domain: ontological commitment)
  phil-identity-persistence    ✅ (domain: identity and persistence)
  phil-grounding-check         ✅ (domain: grounding/constitution)
  phil-conceivability-arg      ✅ (abbreviated: conceivability argument)
  phil-causation-analyze       ✅ (domain: causation)
  phil-essence-detect          ✅ (domain: essence/accident)
  phil-natural-kind-analyze    ✅ (domain: natural kinds)

Metaethics Skills:
  phil-moral-realism           ✅ (domain: moral realism)
  phil-normativity             ✅ (domain: normativity)
  phil-moral-semantics         ✅ (domain: moral semantics)
  phil-moral-psychology        ✅ (domain: moral psychology)
  phil-moral-disagreement      ✅ (domain: moral disagreement)
  phil-moral-epistemology      ✅ (domain: moral epistemology)
  phil-moral-supervenience     ✅ (domain: moral supervenience)

Counterexamples (do not use):
  phil-whole-paper-analyze     ❌ Too large, violates modularity
  phil-arg-check               ❌ Too vague, unclear function
  phil-good-writing            ❌ Not philosophy-specific
  phil-metaphysics-everything  ❌ Metaphysics Swiss Army knife
  phil-reality-scan            ❌ Too abstract, no methodological literature support
```

### 8.2 Directory Naming

```
skills/            → lowercase, kebab-case
agents/            → lowercase, kebab-case
references/        → lowercase, kebab-case
commands/          → lowercase, kebab-case
shared/            → lowercase, kebab-case

Subdirectories:
  argument-forms/ → plural noun (contains general + metaphysical argument forms)
  philosophers-db/ → plural noun (contains ethicists + metaphysicians)
  templates/       → plural noun
```

### 8.3 File Naming

```
Skill main file:       SKILL.md           (fixed)
Skill examples:        examples.md        (optional, fixed name)
Skill templates:       templates.md       (optional, fixed name)
Skill checklist:       checklist.md       (optional, fixed name)
Schema files:          <name>.schema.json (JSON Schema)
Template files:        <name>.md          (Markdown template)
Glossary files:        glossary-<domain>.md
Argument form files:   <form-name>.md     (e.g., conceivability-argument.md)
Distinction catalogs:  metaphysical-distinctions.md  (plural noun)
Taxonomies:            <domain>-taxonomy.md / <domain>-categories.md
Primer references:     <domain>-primer.md
```

### 8.4 Command Naming

```
Format: phil:<action>  (namespace: phil)

Commands (6 composite commands):
  phil:reconstruct    Full-dimension text understanding (9-20 skills, mixed serial/parallel)
  phil:evaluate       Multi-angle parallel critique (7 skills, fully parallel)
  phil:review         Peer review (phil-reviewer agent, 8 dimensions)
  phil:write          Philosophy writing (phil-writer agent, outline/draft/revision)
  phil:comment        Deep commentary (phil-commentator agent, 6 critical dimensions)
  phil:pipeline       Full pipeline (phil-orchestrator agent, 5 stages)

Underlying 28 skills remain invocable via the Skill tool.
Rules:
  - Keep short (ease of user input)
  - Do not conflict with ARS's ars-* commands
```

---

## 9. File Conventions

### 9.1 Mandatory SKILL.md Structure

Every `SKILL.md` must contain the following sections (in fixed order):

```markdown
---
description: <one-sentence description>
domain: <subdomain: general | metaphysics | ethics | ...>
---
```

### 9.2 Conventions for Metaphysics Knowledge Files

Glossary files (`glossary-metaphysics.md`):

```markdown
---
name: <English term name>
chinese: <Chinese translation>
type: <concept type: core-distinction | relation | entity-type | thesis>
related: [<related terms>]
---

<Concise explanation of the definition and core literature, emphasizing the term's technical usage in analytic philosophy>

**Classic source**: <original proponent, year>
**Locus of controversy**: <current state of philosophical debate>
**Role in arguments**: <what kind of arguments this term typically appears in>
```

### 9.3 Responsibilities per Reference File

| File | Mandatory | Content |
|------|--------|------|
| `SKILL.md` | **Mandatory** | Primary definition, see §9.1 structure |
| `examples.md` | Recommended | 3-5 representative examples demonstrating the full input → analysis → output process |
| `templates.md` | Optional | Structural template for output reports |
| `checklist.md` | Optional | Self-check checklist for users |
| `notes.md` | Optional | Maintainer notes, methodological literature citations |

Metaphysics knowledge dependency files:

| File | Description | Maintenance Frequency |
|------|------|---------|
| `glossary-metaphysics.md` | Core metaphysical term definitions | Semi-annual update |
| `metaphysical-distinctions.md` | Key conceptual distinctions (e.g., endurantism/perdurantism) | Annual update |
| `ontological-categories.md` | Ontological category taxonomy and commitment analysis framework | Annual update |
| `modal-logic-primer.md` | Foundations of modal logic and metaphysical applications | Updated as logic advances |
| `causation-taxonomy.md` | Genealogy and comparison of causal theories | Annual update |

### 9.4 Schema Conventions

All cross-Skill data exchange contracts are defined as JSON Schema (`shared/*.schema.json`), following these rules:

1. **Every Schema has a `$id`**, formatted as `phil:<name>:<version>`
2. **Backward compatible**: New fields must be optional
3. **Incompatible changes**: Increment the version number; retain the old Schema for at least one version cycle
4. **Schema separated from implementation**: `shared/*.schema.json` is the specification; Skills reference it

New Metaphysics Schemas:

| Schema File | Purpose | Primary Fields |
|------------|------|---------|
| `ontological-commitment-schema.json` | Structured representation of ontological commitments | entity-type, category, quantification-context, modal-status, source-premise |
| `grounding-relation-schema.json` | Structured representation of grounding/supervenience relations | relation-type, relata, direction, modality, scope, evidence |

---

## 10. Extensibility

### 10.1 Standard Workflow for Adding a New Skill

```
Step 1: Confirm no duplication exists
  → Check whether ARS already has an equivalent capability
  → Check whether existing phil-* Skills overlap
  → If overlap exists, extend the existing Skill instead of creating a new one

Step 2: Determine domain affiliation
  → General skill → place in the general analysis layer
  → Metaphysical skill → place in the metaphysical analysis layer, ensure correct knowledge dependencies are referenced
  → Other philosophical subdomain → create a corresponding knowledge cluster + Skill layer

Step 3: Establish directory structure
  → Create skills/phil-<domain>/
  → Write SKILL.md (must include all §9.1 sections)
  → Write examples.md (recommended)
  → If new knowledge dependencies exist, create or update the corresponding files under references/

Step 4: Registration
  → Update this ARCHITECTURE.md:
      - §3 Directory Tree
      - §4 Layered Architecture (determine its layer)
      - §5 Dependency Graph
      - §6 Research Flow
      - §7 Taxonomy tables (analytic dimension + methodological depth + domain)
  → Create commands/<domain>.md under one of the 6 composite commands or as a new command in the phil: namespace
  → Update the Skills overview in CLAUDE.md

Step 5: Dependency check
  → If the new Skill requires new domain knowledge (glossaries, form libraries):
      - Add the corresponding knowledge file under references/
      - Note the reference in SKILL.md
  → If the new Skill requires a new data contract:
      - Add a schema.json under shared/
  → If the new Skill's output needs to be passed to ARS:
      - Document this in the "Interface with ARS" section of SKILL.md
```

### 10.2 Domain Knowledge Cluster Extension Rules

Each new philosophical subdomain follows the same knowledge dependency pattern:

```
Criteria for adding a new subdomain X:
  1. At least 3-5 unique concepts not coverable by existing glossaries
  2. At least 2-3 unique argument forms
  3. At least 1-2 signature thought experiments

Files to create:
  references/glossary-<X>.md          # Glossary (mandatory)
  references/<X>-distinctions.md      # Core distinctions (recommended)
  references/argument-forms/<X-forms> # New argument forms (recommended)
  references/philosophers-db/<X>.md   # Representative philosophers (recommended)
```

### 10.3 Versioning Strategy

```
Skill-level versioning:
  phil-<domain>/
    ├── SKILL.md               # Version noted in file header comment
    └── CHANGELOG.md           # Traceable changes (optional, recommended)

Knowledge dependency file versioning:
  Metaphysical knowledge dependencies follow Skill versions, not independent versions.
  However, for major changes (e.g., a metaphysical paradigm shift), add a date stamp
  to the filename:
    glossary-metaphysics-2026.md

Change types:
  Minor: Fixing phrasing, updating examples, correcting methodological descriptions
        → Do not modify the SKILL.md header version; update CHANGELOG if present
  Medium: Adding optional steps, adding new output fields
        → Increment patch version
  Major: Changing core methodology, modifying input/output contracts
        → Increment minor version; update all dependent dependency graphs
```

### 10.4 Maintenance Guidelines

```
Routine maintenance:
  - Quarterly: Check whether references/ glossaries need updating
  - Each time methodological literature is updated: Update the "Methodological Basis" section of the corresponding SKILL.md
  - Each time ARS is upgraded: Check whether the ARS Bridge needs adjustment
  - Semi-annually: Check whether newly emerged core distinctions should be added to metaphysical-distinctions.md
  - Annually: Reassess coverage of new theories in causation-taxonomy.md

Deprecation strategy:
  - When a Skill's methodology is shown to be problematic:
    1. Add `deprecated: true` flag to SKILL.md header
    2. Add a Note explaining the alternative
    3. Retain for at least 3 months for migration
    4. Thereafter delete and update ARCHITECTURE.md

Conflict resolution:
  - When two Skills produce conflicting outputs (e.g., conceptual analysis and intuition pump yield different judgments about the same concept):
    → This is a normal phenomenon in analytic philosophy (philosophical disagreement)
    → Present both views faithfully in the report; do not suppress either
    → Document the known disagreement in SKILL.md
  - Metaphysical disagreements (e.g., different ontological stances yielding different evaluations of the same argument):
    → Clearly label in the report which metaphysical presuppositions the evaluation depends on
    → Provide dual evaluation pathways: "if you hold presupposition X" / "if you hold presupposition Y"
```

### 10.5 ARS Version Tracking

This system depends on ARS v3.15.0. When ARS is upgraded:

```yaml
Compatibility matrix:
  ARS v3.15.x:  Fully compatible
  ARS v3.14.x:  Compatible (no breaking changes)
  ARS v3.13.x:  Compatible (no breaking changes)
  ARS < v3.13:  Must check whether Bridge interfaces have changed
  ARS v4.x:     Must reassess the Bridge layer
```

Checklist:
- [ ] Have the command names invoked by the Bridge layer changed?
- [ ] Have the Bridge layer's input/output contracts changed?
- [ ] Do newly added ARS capabilities fill gaps in this system? (If so, mark the corresponding Skill as deprecated)

### 10.6 Future Extension Directions (Reserved But Not Implemented)

```
Reserved Skill names (accommodable by current architecture without modification):
  phil-ethics-ai                AI ethics analysis
  phil-political-arg            Political philosophy argument analysis
  phil-epistemology             Epistemology analysis (requires epistemology knowledge cluster)
  phil-action-theory            Action theory analysis (requires action-theory knowledge cluster)
  phil-phenomenology            Phenomenology analysis (requires references layer extension)
  phil-existential              Existentialist analysis (same as above)

Reserved Metaphysical Extensions (new references needed):
  phil-free-will-analyze        Free will argument analysis (requires free-will-debate.md)
  phil-time-analyze             Philosophy of time argument analysis (requires philosophy-of-time.md)
  phil-space-analyze            Philosophy of space argument analysis (requires philosophy-of-space.md)
  phil-reductionism-check       Reductionism/emergentism analysis (requires reduction-emergence.md)

Reserved Capabilities (new references needed to support):
  formal-logic-translate        Translate natural-language arguments into first-order logic (requires logic-symbols.md)
  decision-theory-analyze       Decision-theoretic presupposition analysis (requires decision-theory.md)
```

---

## Appendix A: Comparison with Existing Skills (Avoiding Duplication)

| This System's Skill | ARS Equivalent? | Distinction |
|-------------|----------------|------|
| `phil-argument-reconstruct` | ARS's analysis/draft summarizes but does **not do explicit formalization** | This system produces a **standard form** as a numbered premise-conclusion list |
| `phil-charity-check` | ARS has no equivalent | Peculiar to analytic philosophy |
| `phil-premise-detect` | ARS has no equivalent | Peculiar to analytic philosophy |
| `phil-counterexample` | ARS does "rebuttal-audit" but evaluates existing objections, does not generate new counterexamples | This system constructs counterexamples from scratch |
| `phil-conceptual-analysis` | ARS does summarization, not deep necessary/sufficient condition analysis of concepts | Peculiar to analytic philosophy |
| `phil-dialectical-map` | ARS has no equivalent | Peculiar to analytic philosophy |
| `phil-thought-experiment` | ARS has no equivalent | Peculiar to analytic philosophy |
| `phil-distinction-track` | ARS has no equivalent | Peculiar to analytic philosophy |
| `phil-modal-arg` | ARS has no equivalent | Peculiar to analytic philosophy |
| `phil-analogy-check` | ARS does general reasoning checks but no dedicated analogy analysis | Peculiar to analytic philosophy |
| `phil-parity-check` | ARS has no equivalent | Peculiar to analytic philosophy |
| `phil-intuition-pump` | ARS has no equivalent | Peculiar to analytic philosophy |
| `phil-methodology` | ARS does PRISMA/RAISE compliance (natural-science methodology) | Philosophical methodology (reflective equilibrium, transcendental arguments, etc.) |
| `phil-contextualize` | ARS `deep-research` provides **timelines/relevance** but not intellectual history | This system focuses on the intellectual lineage of philosophers |
| **`phil-ontological-commitment`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaphysics** |
| **`phil-identity-persistence`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaphysics** |
| **`phil-grounding-check`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaphysics** |
| **`phil-conceivability-arg`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaphysics** |
| **`phil-causation-analyze`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaphysics** |
| **`phil-essence-detect`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaphysics** |
| **`phil-natural-kind-analyze`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaphysics** |
| **`phil-moral-realism`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaethics** |
| **`phil-normativity`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaethics** |
| **`phil-moral-semantics`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaethics** |
| **`phil-moral-psychology`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaethics** |
| **`phil-moral-disagreement`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaethics** |
| **`phil-moral-epistemology`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaethics** |
| **`phil-moral-supervenience`** | **ARS has no equivalent** | **Peculiar to analytic philosophy / metaethics** |

---

## Appendix B: Cross-System Data Flow

```
User Input (text / PDF / question)
    │
    ▼
┌────────────────────────────────────────────────────┐
│  This System (Analytic Philosophy Layer)            │
│                                                    │
│  Input: Philosophical texts, argumentative passages,│
│         conceptual statements                      │
│         (including metaphysical arguments,          │
│         ontological statements, modal reasoning)    │
│                                                    │
│  Output: Structured analysis report + ontological  │
│          audit report                              │
│          - Argument form (numbered premise-         │
│            conclusion list)                        │
│          - Dialectical tree (objection-response     │
│            structure)                              │
│          - Concept map (distinction tracking)       │
│          - Ontological commitment inventory         │
│            (entity types, ontological categories)   │
│          - Grounding relation topology map          │
│          - Conceivability-possibility chain         │
│            evaluation                              │
│          - Transworld identity condition analysis   │
│                                                    │
│  Format: Markdown + JSON Schema                    │
│                                                    │
│  Core methodology: Explicit formalization,          │
│    principle of charity, conceptual distinctions,   │
│    ontological commitment analysis, modal           │
│    reasoning evaluation                            │
└────────────────────┬───────────────────────────────┘
                     │ Analysis report + ontological audit
                     ▼
┌────────────────────────────────────────────────────┐
│  ARS (General Academic Layer)                      │
│                                                    │
│  Input: Analysis report (this system) → Paper      │
│         outline / draft                            │
│         Ontological audit → Presupposition         │
│         statement section of paper                 │
│                                                    │
│  Output: Complete paper, review report, revision    │
│          plan                                      │
│  Format: LaTeX / Markdown / BibTeX                 │
│                                                    │
│  Core methodology: Systematic literature search,   │
│    writing pipeline, citation verification          │
└────────────────────────────────────────────────────┘
                     │ Final paper
                     ▼
              Publication target
```

---

## Appendix C: Metaphysics Knowledge Dependency Quick Reference

### C.1 Core Metaphysical Distinctions at a Glance

| Distinction | Opposing Views | Specific Question | Skills Involved |
|------|---------|---------|---------|
| Endurance/Perdurance | Endurantism vs Perdurantism | How do objects persist across time? | `phil-identity-persistence` |
| Presentism/Eternalism | Presentism vs Eternalism | Do non-present times exist? | `phil-identity-persistence`, `phil-modal-arg` |
| Concrete/Abstract | Concrete vs Abstract | Do abstract entities exist? | `phil-ontological-commitment` |
| Humean/Anti-Humean | Humean vs Anti-Humean | Are laws of nature supervenient or primitive? | `phil-causation-analyze`, `phil-grounding-check` |
| Categorical/Dispositional | Categorical vs Dispositional | Are properties pure "ways things are" or "tendencies to behave"? | `phil-natural-kind-analyze` |
| Sparse/Abundant | Sparse vs Abundant | Which properties are "natural"? | `phil-ontological-commitment` |
| Necessity/Contingency | Necessity vs Contingency | What must be the case? | `phil-modal-arg`, `phil-essence-detect` |
| Reduction/Non-Reduction | Reduction vs Non-Reduction | Can X be fully reduced to Y? | `phil-grounding-check`, `phil-causation-analyze` |

### C.2 Metaphysical Argument Forms at a Glance

| Argument Type | Structural Expression | Famous Case |
|---------|-----------|---------|
| Leibniz's Law | a = b → ∀F(Fa ↔ Fb); ¬(Fa ↔ Fb) → a ≠ b | Identity arguments in philosophy of mind |
| Conceivability argument | ◇Conceivable(p) → ◇Possible(p) → Conclusion | Chalmers's zombie argument |
| Grounding argument | X grounds Y; Y exists; therefore X exists | Fine's logic of ground |
| Supervenience argument | B supervenes on A; when A is fixed B is fixed | Mental causation exclusion |
| Recombination argument | Logically and spatially recombinable → possible | Lewis's modal realism |
| Truthmaker argument | "Truths about the past" require past entities | Armstrong's truthmaker argument |
| Sorites | F(a₁), a₁ ~ a₂, F(a₂), ... → paradox | Heaps, personal identity, vagueness |
| Mereological argument | Part-whole relation axioms P(x,y) | Van Inwagen's Special Composition Question |
| Transcendental argument | Without presupposing X, experience would be impossible → X exists | Kant/Strawson's spatial argument |

### C.3 Important Thought Experiments (Metaphysics)

| Thought Experiment | Proponent | Core Dispute | Skills Involved |
|---------|--------|---------|---------|
| Zombie | Chalmers (1996) | Does consciousness supervene on the physical? | `phil-conceivability-arg`, `phil-thought-experiment` |
| Swampman | Davidson (1987) | Historical conditions of identity | `phil-identity-persistence` |
| Ship of Theseus | Plutarch / Hobbes | Identity across time | `phil-identity-persistence` |
| Statue and Clay | Gibbard (1975) | Identity of coincident objects | `phil-identity-persistence`, `phil-grounding-check` |
| Twin Earth | Putnam (1975) | Meaning externalism, natural kinds | `phil-natural-kind-analyze`, `phil-conceptual-analysis` |
| Experience Machine | Nozick (1974) | Is pleasure the only intrinsic value? | `phil-thought-experiment` |
| Mary's Room | Jackson (1982) | The existence of qualia | `phil-thought-experiment`, `phil-conceivability-arg` |
| Fission | Parfit (1984) | Personal identity | `phil-identity-persistence` |
| Gappy Marble | Lewis (1986) | Possible individuals and properties | `phil-modal-arg` |
| Brain-in-a-Vat | Putnam (1981) | Skepticism and semantics | `phil-thought-experiment`, `phil-modal-arg` |

---

## Appendix D: Metaethics Knowledge Dependency Quick Reference

### D.1 Core Metaethical Distinctions at a Glance

| Distinction | Opposing Views | Specific Question | Skills Involved |
|------|---------|---------|---------|
| Realism/Anti-Realism | Realism vs Anti-Realism | Do moral facts/properties exist? | `phil-moral-realism` |
| Cognitivism/Non-Cognitivism | Cognitivism vs Non-Cognitivism | Do moral judgments express beliefs (truth-apt)? | `phil-moral-semantics` |
| Internalism/Externalism | Internalism vs Externalism | Do moral judgments necessarily involve motivation? | `phil-moral-psychology` |
| Naturalism/Non-Naturalism | Naturalism vs Non-Naturalism | Can moral properties be reduced to natural properties? | `phil-moral-realism`, `phil-moral-supervenience` |
| Reductionism/Non-Reductionism | Reductionism vs Non-Reductionism | Can moral properties be reduced to another level? | `phil-moral-supervenience` |
| Expressivism/Descriptivism | Expressivism vs Descriptivism | Is the function of moral language to express attitudes or describe facts? | `phil-moral-semantics` |
| Reasons Internalism/Externalism | Reasons Internalism vs Externalism | Do reasons for action depend on the agent's motivational set? | `phil-normativity` |
| Constitutivism/Normativism | Constitutivism vs Normativism | Does normativity derive from the constitutive conditions of action? | `phil-normativity` |

### D.2 Metaethical Argument Forms at a Glance

| Argument Type | Structural Expression | Famous Case |
|---------|-----------|---------|
| Open question argument | For any natural property N, Q(Is Good ≡ N) remains an open question | Moore, *Principia Ethica* (1903) |
| Argument from queerness | If moral facts exist ⇒ they are ontologically queer ⇒ they do not exist | Mackie, *Ethics* (1977) |
| Companions in guilt | If morality is rejected because of F ⇒ must reject mathematics (which also has F) ⇒ therefore cannot reject | Against Mackie's error theory |
| Disagreement argument | Widespread persistent disagreement → anti-realism → reject moral facts | Mackie; Doris & Plakias (2008) |
| Normative regress | The source of normativity demands a higher-order norm → regress → a constitutive standard is needed | Korsgaard, *Sources of Normativity* (1996) |
| Moral supervenience argument | Moral properties supervene on natural properties → explanatory burden → challenges non-reductive realism | Blackburn (1971); Mackie (1977) |

### D.3 Important Thought Experiments (Metaethics)

| Thought Experiment | Proponent | Core Dispute | Skills Involved |
|---------|--------|---------|---------|
| Open question argument | Moore (1903) | Moral properties are irreducible to natural properties | `phil-moral-realism`, `phil-moral-semantics` |
| Companions in Guilt | Developed by multiple authors | If one rejects realism about morals, must reject other domains | `phil-moral-realism` |
| Moral disagreement scenarios | Mackie (1977) | Persistent cross-cultural disagreement threatens the uniqueness explanation for moral reality | `phil-moral-disagreement`, `phil-moral-realism` |
| The Amoralist | Brink (1989) | The amoralist understands moral judgments but is not motivationally driven → against motivational internalism | `phil-moral-psychology` |
| Normative regress | Korsgaard (1996) | Normative justification must terminate somewhere — constitutive standards or voluntary choice | `phil-normativity` |
| Frege-Geach problem | Geach (1965) | Can non-cognitivism explain the logical behavior of moral judgments in conditional contexts? | `phil-moral-semantics` |
| Moral Twin Earth | Horgan & Timmons (1991) | Two communities use different natural properties to refer to "good" → against naturalism | `phil-moral-realism`, `phil-moral-semantics` |

---

*Document version 0.3-alpha · Last updated 2026-07-12 · Merge: phil:tutor tutor agent + citation-extract skill; audit fix: schema wiring, dead link repair, agent pruning, hook removal*
*Built on academic-research-skills v3.15.0*
*Phase 4 additions: Metaphysics + Metaethics knowledge dependency layers*
*Phase 5 additions: 5 general Skills + 28 examples.md + 28 checklist.md + philosophers-db*
*Phase 6 additions: 4 production agents + 4 commands + 5-stage writing pipeline*
*Gap closure (historical): 3 dialogic agents + 2 schemas + 5 templates + philosophers-db/ directory + phil:reconstruct（分析）+ phil:evaluate（评价）*
*Phase 7 (v0.3-alpha): Schema full wiring (11 schemas), agent pruning (9→6), INDEX link repair, hook removal, convention unification*

