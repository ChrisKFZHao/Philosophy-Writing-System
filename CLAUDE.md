# CLAUDE.md

> **Project Status: Alpha** — All modules, agents, and skills are functional but have not undergone extensive field testing. Behavioral rules, workflows, and knowledge bases are subject to refinement.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Nature

This is a philosophical writing workflow project, not a code project. All files are text or PDF.

## Behavioral Rules

These rules apply to ALL interactions in this project. They are non-optional constraints on how Claude Code operates here.

### Rule 1: No Sycophancy — Conditional Socratic Engagement

Philosophical work is dialectical, but Socratic questioning is a tool to be deployed when needed, not a ritual to perform every time. The trigger is **vagueness**, not novelty.

**Step 0: Assess clarity before responding.**

When the user proposes a claim, insight, or argumentative direction, first assess: is this idea **clear** or **vague**?

Signs an idea is CLEAR (proceed directly — do NOT interrogate):
- The core claim can be stated in a single precise sentence.
- The logical structure (premises → inference → conclusion) is either stated or immediately recoverable.
- The target is specific: the user identifies what or whom they are arguing against.
- The user uses assertive language ("This is the case...", "The argument is...").
- Boundary conditions or scope are indicated or obviously implied.

Signs an idea is VAGUE (engage Socratic questioning BEFORE proceeding):
- The core claim uses metaphorical, multi-interpretable, or undefined terms.
- No premises or inferential steps are provided, and they are not recoverable from context.
- The target is unspecified: it's unclear what position or argument this is responding to.
- The user uses exploratory language ("Maybe...", "I feel like...", "Something like...").
- The idea could be interpreted in multiple incompatible ways, and the user hasn't chosen among them.

**When the idea is CLEAR:**
Acknowledge the claim, briefly confirm your understanding of its structure, then proceed to execution/writing. Do NOT fabricate objections for the sake of appearing rigorous. An idea can be clear and still be wrong — your job is not to judge correctness at this stage, but to judge *articulation*. A clearly stated wrong idea is actionable; a vaguely stated possibly-right idea is not.

**When the idea is VAGUE:**
1. **Interrogate**: What is the logical structure? What are the premises? What does it presuppose?
2. **Challenge**: What are the counterexamples? Edge cases? Possible objections?
3. **Stress-test**: Does this produce absurd consequences when generalized? Does it hold under extreme conditions?
4. **Alternative interpretations**: Are there other ways to explain the same phenomenon?

Only AFTER the user confirms, refines, or abandons the claim may you enter implementation/writing mode.

**Concrete signals to catch yourself:**
- About to say "that's a great/important/powerful insight" without having checked clarity first → stop. Assess, then respond.
- The user's idea feels intuitively right to you but you can't articulate its logical structure → it's vague. Question.
- The user said something in passing and you're about to run with it → check: did they actually assert this, or are they exploring?

### Rule 2: No Hallucinated Citations

Never generate unverified references, quotations, page numbers, or publication details. Specific rules:

- **No fabricated bibliographies**: Only cite works you have actually read — via PDF, notes, or reconstructed text present in this project. If you have not read it, explicitly mark it as "[source unverified]" or "[citation needed]".
- **No invented quotations**: Do not produce "As X argues in Y..." content unless you have actually read X's Y and can verify the quotation.
- **Distinguish "known" from "inferred"**: If you infer a philosopher's position or the existence of a source from general philosophical knowledge, use explicit hedging ("presumably...", "possibly...", "it is likely that...") and never mix this with assertive language.
- **Knowledge base exception**: Philosopher information in `.claude/references/philosophers-db/` has been curated and may be cited. But specific papers, page numbers, and quotations not in that database all require verification.

### Rule 3: Trigger-Based Version Management for Manuscripts

Version cuts are NOT automatic on every save. A new version is cut ONLY when one of three triggers fires:

1. **Post-review/commentary revision** — manuscript revised in response to reviewer or commentator feedback.
2. **New insight or idea** — a substantive new argument, distinction, or section is added.
3. **Compression or expansion** — significant size change; note "compact" or "expanded" in description.

Same-day triggers are merged into a single version. The version description lists all triggers included.

**File conventions:**
- `{topic}-draft.txt` — working draft. Freely overwritten within a session. Never versioned.
- `{topic}-v{N}.txt` — cut version. Created from `-draft.txt` when a trigger fires.
- `{topic}-review-v{N}.txt` — review report for round N.
- `manuscript/VERSIONS.md` — centralized version history for all manuscripts. Every cut version MUST be documented here with date, triggers, and description.

**Process:** When a trigger fires, copy `{topic}-draft.txt` to `{topic}-v{N}.txt`, then document the new version in `VERSIONS.md`. The `-draft.txt` persists as the working copy for the next round — it is never deleted or reset.

## Directory Structure

```
bibliography/  Reference storage (PDF, BibTeX, etc.)
manuscript/    Draft manuscripts in plain text (.txt)
paper/         Final papers as LaTeX source (.txt)
.claude/       Claude Code project configuration, Skills, knowledge base
  ├── skills/        Philosophical analysis skills (standalone .md files)
  ├── agents/        Philosophy-specialized agents (writing, review, commentary, orchestration)
  ├── commands/      User-triggered commands (thin wrappers)
  ├── references/    Knowledge dependencies (glossaries, argument form library)
  ├── shared/        Cross-skill data contracts (JSON Schema)
  └── ARCHITECTURE.md  Complete system architecture document
```

## Workflow Conventions

### Manuscripts (manuscript/)
- Plain text writing; no markup languages
- Filenames use English kebab-case of the paper topic
- Each revision round saves as a new file; old files add a version suffix
- Writing in Chinese

### Papers (paper/)
- Store complete LaTeX source with `.txt` extension
- When compiling PDF, temporarily copy `.txt` to `.tex` then compile

### Bibliography (bibliography/)

```
bibliography/
├── pdf/                              Original PDF files
├── analysis/                         Paired analysis files (one per reference)
│   └── {Author-Title}.analysis.txt
└── INDEX.md                          Reference inventory with analysis levels

Analysis levels (progressive, append-only):
  Level 1: Argument reconstruction (trigger: PDF added)
  Level 2: + Implicit premises, charity audit, conceptual analysis,
            distinction tracking (trigger: first citation in a manuscript)
  Level 3: + Dialectical mapping, ontological commitment, modal analysis,
            domain-specific skills (trigger: source becomes core target/dependency)

Citation Gate (Rule 2 enforcement):
  If a manuscript claim depends on analysis at Level N, but the source's
  .analysis.txt is only at Level N-1 or below → BLOCK and require analysis
  completion. No citation passes without a verified analysis backing it.


## Common Operations

- Read PDF references: `pdftotext "bibliography/xxx.pdf" -`
- Compile LaTeX in paper/ to PDF:
  ```bash
  cp paper/topic.txt paper/topic.tex && cd paper && pdflatex topic.tex && cd ..
  ```
- Count manuscript characters: `wc -m manuscript/topic.txt`

---

## Installed Skills

### Phase 1: Foundation (Complete)

| Skill | Command | Function | Version | Status |
|-------|---------|----------|---------|--------|
| Argument Reconstruction | `/phil-reconstruct` | Convert arguments in philosophical texts into standard premise-conclusion form; 7-step process; supports 10 argument types | v1.0.0 | ✅ Complete & Tested |
| Conceptual Analysis | `/phil-concepts` | Clarify philosophical concept definitions, necessary/sufficient conditions, case testing, distinction mapping, structure typing, and dimension analysis | v1.0.0 | ✅ Complete |
| Implicit Premise Detection | `/phil-premises` | Systematically detect unstated assumptions in philosophical arguments; 7 implicit premise types; includes certainty assessment and rejection impact analysis | v1.0.0 | ✅ Complete |
| Principle of Charity Check | `/phil-charity` | Audit argument reconstructions for adherence to the principle of charity; detect oversimplification and unfair interpretation; generate alternative readings | v1.0.0 | ✅ Complete |
| Modal Argument Analysis | `/phil-modal` | Evaluate the logical structure of possibility/necessity claims; detect modal scope ambiguity and conceivability leaps | v1.0.0 | ✅ Complete |
| Distinction Tracking | `/phil-distinctions` | Scan text for all conceptual distinctions; index, analyze function, check consistency, and map distinction networks | v1.0.0 | ✅ Complete |
| Counterexample Generation | `/phil-counterexample` | Construct counterexamples targeting argument reconstructions; 6 counterexample types; includes four-dimension evaluation and dialectical anticipation | v1.0.0 | ✅ Complete |
| Thought Experiment Analysis | `/phil-thought` | Deconstruct the structure, intuition mechanisms, and argumentative force of philosophical thought experiments | v1.0.0 | ✅ Complete |
| Dialectical Mapping | `/phil-dialectic` | Build thesis-objection-response dialectical trees; track argumentative attack-and-defense evolution | v1.0.0 | ✅ Complete |

### Phase 4: Metaphysics + Metaethics (Complete)

| Skill | Command | Function | Version | Status |
|-------|---------|----------|---------|--------|
| **Metaphysics P1** | | | | |
| Ontological Commitment Detection | `/phil-ontology` | Identify entity types and existence categories presupposed by arguments using Quinean criterion and ontological category taxonomy | v1.0.0 | ✅ Complete |
| Identity & Persistence Analysis | `/phil-identity` | Analyze identity conditions across time/worlds; evaluate endurance vs perdurance frameworks; detect fission/fusion/Theseus problems | v1.0.0 | ✅ Complete |
| Grounding/Constitution Analysis | `/phil-grounding` | Detect grounding, supervenience, realization, and constitution relations; map ontological dependence topology | v1.0.0 | ✅ Complete |
| Conceivability Argument Analysis | `/phil-conceivability` | Evaluate conceivability-to-possibility chain; analyze zombie arguments and modal epistemology | v1.0.0 | ✅ Complete |
| **Metaethics P1** | | | | |
| Moral Realism Analysis | `/phil-moral-realism` | Analyze moral realism/anti-realism/error theory/non-cognitivism arguments; map positions on the realism spectrum | v1.0.0 | ✅ Complete |
| Normativity Analysis | `/phil-normativity` | Analyze source/structure of normativity; classify categorical/hypothetical, internal/external reasons | v1.0.0 | ✅ Complete |
| Moral Semantics Analysis | `/phil-moral-semantics` | Analyze moral language; map cognitivism/expressivism/prescriptivism; evaluate Frege-Geach handling | v1.0.0 | ✅ Complete |
| Moral Psychology Analysis | `/phil-moral-psychology` | Analyze moral judgment–motivation relation; evaluate internalism/externalism, Humean theory, amoralist challenge | v1.0.0 | ✅ Complete |
| **Metaphysics P2** | | | | |
| Causal Claim Analysis | `/phil-causation` | Identify theoretical affiliations of causal claims; evaluate Humean vs anti-Humean; detect exclusion problems | v1.0.0 | ✅ Complete |
| Essentialist Claim Detection | `/phil-essence` | Detect essence/accident distinction use; analyze modal profiles using Finean and Kripkean frameworks | v1.0.0 | ✅ Complete |
| Natural Kind Analysis | `/phil-natural-kind` | Analyze natural kind classification; evaluate essentialism, HPC, promiscuous realism, conventionalism | v1.0.0 | ✅ Complete |
| **Metaethics P2** | | | | |
| Moral Disagreement Analysis | `/phil-moral-disagreement` | Evaluate arguments from moral disagreement; assess conciliationist challenges and convergence responses | v1.0.0 | ✅ Complete |
| Moral Epistemology Analysis | `/phil-moral-epistemology` | Evaluate moral knowledge claims; analyze intuitionist/coherentist/reliabilist pathways; assess evolutionary debunking | v1.0.0 | ✅ Complete |
| Moral Supervenience Analysis | `/phil-moral-supervenience` | Analyze moral-to-natural supervenience; evaluate Blackburn's challenge and realist/expressivist responses | v1.0.0 | ✅ Complete |

### Phase 4: New Knowledge Base

| File | Content |
|------|---------|
| `glossary-metaphysics.md` | Core metaphysics terminology (535 lines, 10 thematic clusters) |
| `metaphysical-distinctions.md` | 16 core metaphysical distinctions (686 lines) |
| `ontological-categories.md` | Hierarchical taxonomy of ontological categories (341 lines) |
| `causation-taxonomy.md` | 9 causal theory families with comparison tables (773 lines) |
| `glossary-metaethics.md` | Core metaethics terminology (402 lines, 7 thematic clusters) |
| `metaethical-distinctions.md` | 15 core metaethical distinctions (509 lines) |
| `moral-realism-taxonomy.md` | 12 positions on the realism spectrum (577 lines) |
| `normativity-taxonomy.md` | 10 normativity theories with comparison table (550 lines) |
| `argument-forms/` (15 new) | 9 metaphysics + 6 metaethics argument forms |

### Phase 4: New Infrastructure

| Component | Files |
|-----------|-------|
| JSON Schemas | `ontological-commitment-schema.json`, `grounding-relation-schema.json`, `moral-realism-schema.json`, `normativity-schema.json` |
| Agents | `metaphysician.md`, `metaethicist.md` |
| Commands | 14 new command files (1 per skill) |

### Phase 5: General Skills + Teaching Docs + Knowledge Base (Complete)

| Skill | Command | Function | Version | Status |
|-------|---------|----------|---------|--------|
| Analogy Argument Analysis | `/phil-analogy` | Map source-target correspondences in analogical arguments; evaluate relevance of shared properties; detect disanalogies; grade argumentative force | v1.0.0 | ✅ Complete |
| Parity / Similarity Check | `/phil-parity` | Test parity and relevant-similarity claims; evaluate companions-in-guilt arguments; detect false parity; assess slippery slope parity chains | v1.0.0 | ✅ Complete |
| Intuition Pump Analysis | `/phil-intuition` | Analyze intuition pumps and their dialectical role; reconstruct intuition→judgment chains; evaluate debunking susceptibility and framing effects | v1.0.0 | ✅ Complete |
| Methodology Analysis | `/phil-methodology` | Identify methodological commitments in philosophical arguments; classify methods (conceptual analysis, reflective equilibrium, genealogy, etc.); check consistency | v1.0.0 | ✅ Complete |
| Argument Contextualization | `/phil-context` | Situate arguments in debate traditions and intellectual landscapes; map rival positions; trace conceptual history; assess dialectical stakes | v1.0.0 | ✅ Complete |

### Phase 6: Writing & Review Agents (Complete)

| Agent | Command | Function | Version | Status |
|-------|---------|----------|---------|--------|
| Philosophy Writer | `/phil-write` | Generate philosophical manuscripts in three modes: outline (structured outline from analysis), draft (section-by-section with prose quality checks), revision (finding-triage and prioritized revision) | v1.0.0 | ✅ Complete |
| Philosophy Reviewer | `/phil-review` | Domain-specific peer review across 8 dimensions; supports standard review and perspective review (review as a Quinean, Lewisian, Kripkean, etc.) | v1.0.0 | ✅ Complete |
| Philosophy Commentator | `/phil-comment` | Critical engagement: unexamined assumptions, alternative interpretations, missing distinctions, undefended moves, hidden commitments, dialectical blind spots | v1.0.0 | ✅ Complete |
| Pipeline Orchestrator | `/phil-pipeline` | End-to-end 5-stage workflow: philosophical question → literature review → outline → draft → final manuscript with quality gates at each stage | v1.0.0 | ✅ Complete |

### Phase 5: New Knowledge Base

| File | Content |
|------|---------|
| `philosophers-db/` | Comprehensive philosopher reference database (49 philosophers across 3 domains) |
| `ARCHITECTURE.md` (recovered) | Complete system architecture document 0.1-alpha |

### Phase 5: Teaching Documentation

| Deliverable | Count | Description |
|-------------|-------|-------------|
| `examples.md` | 28 total (9 Phase 1-3 + 14 Phase 4 + 5 Phase 5) | 4-6 worked examples per skill with Input→Output format |
| `checklist.md` | 28 total (9 Phase 1-3 + 14 Phase 4 + 5 Phase 5) | Structured quality checklist per skill |

### Skill File Structure

Each Skill includes:
- `SKILL.md` (mandatory) — Primary definition (Overview, Input, Output, Methodological Basis, Steps, Quality Criteria)
- `examples.md` (recommended) — Representative examples
- `checklist.md` (recommended) — Quality checklist

---

## Knowledge Base

### Argument Form Library (references/argument-forms/)

26 argument forms with canonical definitions (11 general + 9 metaphysics + 6 metaethics):

**General (11):**
| File | Type | Core Structure |
|------|------|----------------|
| `modus-ponens.md` | Deductive | P→Q, P ∴ Q |
| `modus-tollens.md` | Deductive | P→Q, ¬Q ∴ ¬P |
| `reductio.md` | Deductive/Reductio | P → contradiction ∴ ¬P |
| `categorical-syllogism.md` | Deductive | A/E/I/O syllogism |
| `dilemma.md` | Deductive | P∨Q, P→R, Q→R ∴ R |
| `transcendental.md` | Transcendental | Y, ¬X→¬Y ∴ X |
| `definitional-argument.md` | Definitional | ∀x(X(x)↔φ(x)), φ(a) ∴ X(a) |
| `inductive-generalization.md` | Inductive | Sample → population generalization |
| `inference-to-best-explanation.md` | Abductive/IBE | O, H→O, ¬∃H' better ∴ H |
| `analogy.md` | Analogical | A:F,G; B:F ∴ B:G |
| `practical-reasoning.md` | Practical | Goal G, means M ∴ ought to do M |

**Metaphysics (9):**
| File | Type | Core Structure |
|------|------|----------------|
| `leibniz-law.md` | Deductive/Modal | a=b, F(a) ∴ F(b) |
| `conceivability-argument.md` | Modal/Abductive | Conceivable → Possible → Conclusion |
| `grounding-argument.md` | Metaphysical | X grounds Y → Y depends on X |
| `supervenience-argument.md` | Modal | B-properties fixed → A-properties fixed |
| `recombination-argument.md` | Modal/Combinatorial | Separable entities → separate worlds |
| `truthmaker-argument.md` | Metaphysical | Truth → existence of truthmaker |
| `sorites.md` | Paradox/Vagueness | Tolerance principle → contradiction |
| `four-dimensionalist.md` | Metaphysical | Temporary intrinsics → temporal parts |
| `mereological-argument.md` | Metaphysical | Composition conditions → existence of composites |

**Metaethics (6):**
| File | Type | Core Structure |
|------|------|----------------|
| `open-question-argument.md` | Semantic | Open question → non-naturalism |
| `queerness-argument.md` | Metaphysical/Epistemic | Queer entities → error theory |
| `companions-in-guilt.md` | Analogical | Morality shares feature F with X → keep both |
| `disagreement-argument.md` | Abductive/IBE | Persistent disagreement → anti-realism |
| `regress-argument.md` | Transcendental | Normative regress → constitutivism |
| `moral-supervenience.md` | Abductive/IBE | Supervenience → expressivist advantage |

### Data Contracts (shared/)

- `argument-schema.json` — Universal argument reconstruction data exchange format
- `concept-map-schema.json` — Conceptual analysis structured data contract
- `premise-audit-schema.json` — Implicit premise detection results contract
- `ontological-commitment-schema.json` — Ontological commitment detection results contract
- `grounding-relation-schema.json` — Grounding relation analysis contract
- `moral-realism-schema.json` — Moral realism stance analysis contract
- `normativity-schema.json` — Normative structure analysis contract

### Logical Jumps & Fallacies (references/)

- `fallacy-catalog.md` — Systematic catalog of logical jumps, inferential fallacies, and presupposition types
- `modal-logic-primer.md` — Modal logic foundational reference (K/T/S4/S5/B systems)
- `thought-experiment-templates.md` — Thought experiment typology (6 structural patterns)

---

## Architecture

The complete system architecture is defined in `ARCHITECTURE.md` at the project root (0.1-alpha), built atop `academic-research-skills` v3.15.0, adding an analytic philosophy methodology layer. Covers three subdomains: general analytic philosophy, metaphysics, and metaethics.

Build Roadmap:
```
Phase 1 ✅: phil-argument-reconstruct, phil-conceptual-analysis (Complete)
Phase 2 ✅: phil-premise-detect, phil-charity-check, phil-modal-arg, phil-distinction-track (Complete)
Phase 3 ✅: phil-counterexample, phil-thought-experiment, phil-dialectical-map (Complete)
Phase 4 ✅: Metaphysics + Metaethics Layer (14 Skills + 8 KB files + 15 argument forms + 4 schemas + 2 agents + 14 commands) (Complete)
         ✅ Metaphysics P1: ontological-commitment, identity-persistence, grounding-check, conceivability-arg
         ✅ Metaethics P1: moral-realism, normativity, moral-semantics, moral-psychology
         ✅ Metaphysics P2: causation-analyze, essence-detect, natural-kind-analyze
         ✅ Metaethics P2: moral-disagreement, moral-epistemology, moral-supervenience
Phase 5 ✅: Remaining General Skills + Examples + Checklists + Knowledge Base Completion (Complete)
         ✅ General Skills: analogy-check, parity-check, intuition-pump, methodology, contextualize
         ✅ Teaching Docs: 28 examples.md + 28 checklist.md
         ✅ Knowledge Base: philosophers-db, ARCHITECTURE.md recovery
Phase 6 ✅: Philosophy-Specialized Writing Agents + Pipeline Orchestration (Complete)
         ✅ Writing Agent: phil-writer (outline/draft/revision modes)
         ✅ Reviewer Agent: phil-reviewer (8 review dimensions + perspective simulation)
         ✅ Commentator Agent: phil-commentator (critical/response/positioning modes)
         ✅ Pipeline Orchestrator: phil-orchestrator (5-stage pipeline with quality gates)
```

---

## Current Outputs

| File | Content | Date |
|------|---------|------|
| `ARCHITECTURE.md` | 0.1-alpha Complete system architecture document | 2026-07-11 |
| `.claude/references/philosophers-db/` | Philosopher reference database (49 philosophers across 3 domains) | 2026-07-11 |
| `bibliography/analysis/Srinivasan-Anger.analysis.txt` | Srinivasan "Anger" full argument reconstruction report (Level 3) | 2026-07-10 |

## Current Progress

- ✅ Phases 1-6 fully complete + Gap Closure
- **28 Skills**, **33 Commands** (28 phil-* + 4 writing + `/phil-analyze`), **28 examples.md**, **28 checklist.md**
- **26 argument forms** (11 general + 9 metaphysics + 6 metaethics)
- **12 reference files** (8 glossaries/taxonomies + philosophers-db + 3 method references)
- **9 JSON schemas**, **9 agents** (5 dialogic + 4 writing/production)
- **5 report templates** (argument-reconstruction, premise-audit, conceptual-analysis, dialectical-map, ontological-audit)
- Total project: ~150+ files, ~38,000+ lines
- Phase 5 added: 5 Skills · 5 Commands · 28 teaching docs · philosophers-db · ARCHITECTURE.md recovery
- Phase 6 added: 4 Agents (writer, reviewer, commentator, orchestrator) · 4 Commands · 5-stage writing pipeline
- Gap closure: `/phil-analyze` · 3 dialogic agents · 2 schemas · 5 templates
