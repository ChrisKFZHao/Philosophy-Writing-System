---
name: phil-natural-kind-analyze
description: "Natural Kind Analysis — analyze arguments concerning natural kind classification; evaluate kind essentialism, HPC theory, and conventionalist approaches"
---

# Natural Kind Analysis

## Overview

Arguments about natural kinds appear across an extraordinarily wide range of philosophical subfields — philosophy of science (Are chemical elements natural kinds? Are biological species natural kinds?), metaphysics (Do natural kinds have essences? Are natural kinds real or conventional?), philosophy of biology (Are species individuals or kinds? Does the species concept admit of pluralism?), philosophy of mind (Are mental states natural kinds? Are emotions natural kinds?), and philosophy of social science (Are race and gender natural kinds? Social kinds?). In every case, the notion of a "natural kind" does significant argumentative work, but what exactly the argument means by "natural kind" is often left underspecified.

This skill analyzes natural kind classification arguments by diagnosing the implicit theory of kinds the argument presupposes, evaluating whether the kind classifications are adequate to the argument's purposes, assessing cross-domain consistency (does the argument treat kinds uniformly across different domains?), and evaluating kind-based inferences (does the inference from "X is a member of kind K" to some conclusion hold under the presupposed theory of kinds?). It answers the question: "When the argument classifies X as a natural kind K, or draws inferences from kind membership, what theory of natural kinds makes these claims true, and are the inferences justified?"

The skill is essential within the metaphysics pipeline because natural kind claims are among the most consequential metaphysical commitments an argument can make — they determine what exists (ontological commitment to kinds qua entities), what is necessary (kind essentialism grounds de re necessity), what is projectible (kinds support inductive inference), and what is explanatory (kinds figure in scientific explanations). Before evaluating whether an argument's kind-based inferences are sound, one must understand what the argument means by "natural kind" and whether that conception can bear the inferential weight placed upon it.

## Input

**Required:**
- `argument-reconstruction report` (from `phil-argument-reconstruct`): Provides the argument in standard premise-conclusion form, including where natural kind claims appear, what inferential role they play, and what kind-based conclusions are drawn. The reconstruction identifies kind terms and kind-membership claims in the argument's logical structure.

**Optional:**
- `conceptual-analysis report` (from `phil-conceptual-analysis`): Natural kind terms often function as concepts within philosophical arguments, and the conceptual analysis may identify conceptual connections between kind terms and other concepts. This helps determine whether the argument treats kind classification as conceptual (true by definition) or empirical (true by discovery).
- `essentialist-claim analysis report` (from `phil-essence-detect`): Natural kind essentialism is a species of essentialist claim. If the essentialist claim analysis report is available, it identifies which properties the argument treats as essential to the kind, and which essence framework (modal, definitional, constitutive) is presupposed. This directly informs the kind theory diagnosis (essentialist kinds vs HPC kinds vs conventional kinds).

## Output

**Natural Kind Analysis Report** — structured analysis containing the following sections:

### Section 1: Kind Claims Catalog

A numbered list (KC1, KC2, ..., KCn) cataloging every natural kind claim in the argument:

| Field | Description |
|-------|-------------|
| `claim_id` | Unique identifier: KC1, KC2, ..., KCn |
| `kind_term` | The term claimed to designate a natural kind: "water," "tiger," "electron," "gold," "species," "emotion," "race," etc. |
| `domain` | The domain of the kind claim: `physics`, `chemistry`, `biology`, `psychology`, `social_science`, `mathematics`, `metaethics`, `metaphysics`, `everyday_objects`, `other` |
| `classification_claim` | What the argument asserts about kind classification: "X is a natural kind," "X is not a natural kind," "K is a natural kind and L is not," "all Xs belong to kind K," etc. |
| `kind_theory_hint` | Preliminary diagnostic hint: does the argument's language suggest a particular theory of kinds? Keywords: "essence" suggests essentialism; "cluster" or "homeostatic" or "property cluster" suggests HPC; "constructed" or "social" suggests conventionalism; "useful" or "pragmatic" suggests practical kind theory; "many" classifications suggests pluralism |
| `structural_role` | How the kind claim functions in the argument: `direct_premise`, `inferred_conclusion`, `definitional_stipulation`, `background_framework`, `suppressed_premise` |

### Section 2: Kind Theory Diagnosis

Diagnosis of which theory of natural kinds the argument presupposes:

| Theory | Core Claim | Diagnostic Indicators |
|--------|-----------|----------------------|
| **Kind Essentialism (Kripke/Putnam)** | Natural kinds have essences — a set of properties necessary and sufficient for kind membership — discoverable by science. Kind terms are rigid designators. "Water is essentially H2O." | The argument treats kind membership as a matter of possessing an essence, discovered by science. Kind terms are used as rigid designators. The argument draws necessary conclusions from kind membership. Microstructural or hidden-structure essentialism. |
| **Homeostatic Property Cluster (Boyd)** | Natural kinds are clusters of properties maintained in homeostasis by underlying causal mechanisms. No single property is necessary; the cluster is projectible and supports induction. Kind boundaries may be vague. | The argument treats kinds as property clusters stabilized by causal mechanisms. It acknowledges that kind membership may be a matter of degree and that properties in the cluster may vary across instances. Appeals to homeostatic mechanisms. |
| **Promiscuous Realism (Dupré)** | There are many equally legitimate ways to classify the world into kinds — different classification schemes serve different purposes, and there is no uniquely correct classification. Kinds are real but not unique. | The argument acknowledges or endorses multiple cross-cutting classifications. It resists the claim that there is one uniquely correct way to carve nature at its joints. Pluralism about kinds. |
| **Conventionalism (Hacking, Goodman)** | Kind classifications are human constructions — they reflect our interests, practices, and conventions, not mind-independent structures in the world. Kinds are made, not found. | The argument treats kind classifications as historically or socially contingent. It emphasizes the role of human interests and practices in classification. It may appeal to Goodman's "new riddle of induction" to challenge the projectibility of kinds. |
| **Causal Network Theory (Khalidi)** | Natural kinds are nodes in causal networks — they are identified by their causal roles, not by intrinsic essences. Kind membership is a matter of occupying a particular position in a causal structure. | The argument identifies kinds by their causal roles and relations. It resists essentialism but also resists conventionalism — kinds are real because they are causally efficacious. Appeals to causal networks and causal homeostatics. |
| **Historical Kinds (Millikan)** | Some kinds (especially biological species) are individuated by their historical origins and lineages, not by intrinsic properties or essences. Kind membership is a matter of historical connection. | The argument appeals to historical or etiological criteria for kind membership. It treats kind membership as dependent on lineage or origin. Common in philosophy of biology (species as individuals, historical kinds). |
| **Practical Kind Theory** | Kinds are classifications that serve practical purposes — they are valued for specific epistemic or practical goals, and their legitimacy is relative to those goals. Neither fully realistic nor fully conventional. | The argument ties kind classifications to specific purposes or interests. It resists the claim that there is a fact of the matter about kind membership independent of purpose. Pragmatic orientation. |

**Diagnostic procedure:**

1. **Lexical scan**: Tabulate kind-related vocabulary. "Essence," "real essence," "necessary and sufficient conditions," "microstructural essence" suggests kind essentialism. "Cluster," "homeostatic," "property cluster," "causal mechanism," "projectible" suggests HPC. "Constructed," "social kind," "convention," "interests," "history" suggests conventionalism. "Pluralism," "many classifications," "cross-cutting" suggests promiscuous realism. "Causal role," "causal network," "node" suggests causal network theory. "Lineage," "origin," "historical" suggests historical kinds.

2. **Criteria test**: What does the argument treat as criteria for kind membership? Necessary and sufficient intrinsic properties suggest essentialism. Cluster of co-occurring properties stabilized by mechanisms suggests HPC. Historical lineage suggests historical kinds. Causal role suggests causal network theory. Social or practical function suggests conventionalism or practical kind theory. No privileged criteria, multiple equally valid criteria suggest promiscuous realism.

3. **Uniqueness test**: Does the argument treat kind classifications as unique (there is one correct classification) or plural (many equally correct classifications)? Unique classification suggests essentialism, HPC (typically), causal network theory (typically). Plural classifications suggest promiscuous realism, conventionalism (some forms), practical kind theory (some forms).

4. **Realism test**: Does the argument treat kinds as mind-independent features of reality or as human constructions? Mind-independent suggests essentialism, HPC, causal network theory, historical kinds (typically). Human-constructed suggests conventionalism, practical kind theory (some forms).

5. **Modal test**: What modal force does the argument attribute to kind membership? Metaphysical necessity suggests kind essentialism ("necessarily, water is H2O"). Nomic necessity (laws of nature) suggests HPC or causal network theory (homeostatic mechanisms support nomic regularities). Contingent, no modal force beyond actual regularity suggests conventionalism or practical kind theory.

**Output**: A theory diagnosis specifying the primary theory of kinds, the evidential basis (lexical, criteria, uniqueness, realism, modal tests), any secondary or internally inconsistent theory commitments, and whether the argument's kind theory is consistent across different kinds in different domains.

### Section 3: Classification Adequacy Assessment

Evaluate whether the kind classifications asserted by the argument are adequate — do the kinds do the work the argument demands of them?

**Assessment dimensions:**

#### Dimension 1: Membership Criteria Adequacy

For each kind claim, determine whether the presupposed theory of kinds provides adequate criteria for kind membership. Under essentialism: Are the essential properties specified? If the argument claims "K is a natural kind" without specifying the essence of K, the classification is underdetermined. If the essence is specified, are there counterexamples — things that satisfy the essence definition but are intuitively not members, or things that are intuitively members but do not satisfy the essence definition? Under HPC: Is the property cluster described? Is the homeostatic mechanism identified? HPC requires both a cluster specification and a causal mechanism that maintains the cluster. Without the mechanism, the HPC claim is incomplete. Under historical kinds: Is the historical lineage specified? Without lineage specification, historical kind classification is underdetermined. Under conventionalism or practical kinds: Are the conventions or purposes specified?

#### Dimension 2: Projectibility Assessment

A central function of natural kinds is supporting inductive inference — if something is a member of kind K, we can project K-typical properties onto it. Evaluate whether the argument relies on kind membership to support inductive inferences, and whether the presupposed theory of kinds licenses the required projectibility. Essentialism licenses strong projectibility: if K has essence E, then all Ks have E. HPC licenses qualified projectibility: kind-typical properties are projectible to the extent that the homeostatic mechanism is stable. Conventionalism licenses only qualified projectibility relative to conventions. Historical kinds may not license strong projectibility: kind membership via lineage does not guarantee shared intrinsic properties. If the argument draws inductive inferences from kind membership that the presupposed theory cannot license, flag the projectibility gap.

#### Dimension 3: Explanatory Role Assessment

Natural kinds are often claimed to figure in scientific explanations — kind membership explains why things have the properties they do. Evaluate whether the argument treats kind membership as explanatory and whether the presupposed theory supports explanatory uses of kinds. Essentialism: kind essence explains kind-typical properties. HPC: the homeostatic mechanism explains why the cluster coheres. Causal network theory: the kind's causal role explains its properties. Conventionalism: kind membership does not explain anything — kinds are descriptive or pragmatic, not explanatory. If the argument relies on kind membership to do explanatory work that the presupposed theory cannot support, flag the explanatory gap.

#### Dimension 4: Boundary and Vagueness Assessment

Many kinds (especially biological and psychological kinds) have vague boundaries. Evaluate whether the argument treats kind boundaries as sharp or vague, and whether the presupposed theory accommodates the appropriate boundary conditions. Essentialism typically requires sharp boundaries (either you have the essence or you don't). HPC accommodates vague boundaries (property clusters can have borderline cases). Conventionalism: boundaries are as sharp or vague as conventions make them. If the argument treats kind boundaries as sharp in a domain where vagueness is widely acknowledged (e.g., biological species, mental disorders), flag the boundary problem.

**Output**: A classification adequacy assessment with each dimension rated for each kind claim, with justifications.

### Section 4: Cross-Domain Consistency Check

Arguments often classify kinds across multiple domains (e.g., "water, tigers, and electrons are all natural kinds"). But different domains may require different theories of kinds — what works for chemical kinds (sharp boundaries, microstructural essences) may not work for biological kinds (vague boundaries, historical individuation).

**Protocol:**

1. **Domain inventory**: List all domains in which the argument makes kind claims. For each domain, identify the relevant philosophical debates:
   - Chemistry: Chemical kinds defined by microstructure (H2O, Au with atomic number 79). Generally treated as paradigm natural kinds with sharp essences.
   - Biology: Are species natural kinds, individuals, or something else? The species problem is a central debate. Species essentialism is widely rejected among philosophers of biology; HPC, historical, and individual-based accounts are more common.
   - Physics: Are fundamental particles natural kinds? Generally treated as kinds with dispositional essences. But some interpretations of quantum mechanics challenge kind individuation.
   - Psychology: Are mental states/emotions natural kinds? Highly contested. Some argue for psychological kinds as HPC clusters; others argue for social construction.
   - Social kinds: Are race, gender, social class natural kinds? Almost universally rejected as natural kinds (though some argue for social kinds as a distinct category of real kinds, or for interactive kinds in Hacking's sense).
   - Medicine: Are diseases natural kinds? Contested. Some diseases (bacterial infections) may have microbial essences; others (mental disorders) are more like HPC clusters or practical kinds.

2. **Uniformity check**: Does the argument treat kinds uniformly across domains? If the argument says "water, tigers, and electrons are all natural kinds" and presupposes essentialism, does it apply essentialism to tigers? Biological species essentialism is widely rejected — does the argument acknowledge this?

3. **Domain-specific adequacy**: For each domain, assess whether the presupposed theory of kinds is adequate for that domain, given the relevant philosophical and scientific literature: essentialism for chemical kinds (generally adequate), essentialism for biological species (generally inadequate — species essentialism faces well-known objections), HPC for biological species (more adequate), HPC for psychological kinds (potentially adequate), conventionalism for social kinds (arguably more appropriate than essentialism), historical kinds for biological species (widely defended).

4. **Theory-switching detection**: Does the argument implicitly switch between theories of kinds when moving between domains? For example, treating chemical kinds as having essences while treating biological kinds as HPC clusters — without acknowledging the shift. This is not necessarily a problem (kind pluralism is a defensible position), but it should be detected and flagged if unacknowledged.

**Output**: A cross-domain consistency report with domain inventory, uniformity assessment, domain-specific adequacy ratings for each kind claim, and any theory-switching flagged.

## Methodological Foundations

This skill draws on eight foundational sources spanning the realist, pluralist, and conventionalist traditions in the philosophy of natural kinds:

1. **Kripke (1980) "Naming and Necessity" / Putnam (1975) "The Meaning of 'Meaning'"** — The Kripke-Putnam theory of natural kind terms as rigid designators. Natural kind terms (like "water," "tiger," "gold") are not synonymous with descriptions of their surface properties; they rigidly designate the kind whose underlying nature is discovered by science. "Water is H2O" is a necessary a posteriori truth. This framework establishes modal kind essentialism and the distinction between nominal essence (the stereotype) and real essence (the underlying nature). Twin Earth thought experiments demonstrate that kind membership is determined by underlying nature, not by surface properties or psychological states.

2. **Boyd (1991) "Realism, Anti-Foundationalism and the Enthusiasm for Natural Kinds" / Boyd (1999) "Homeostasis, Species, and Higher Taxa"** — The homeostatic property cluster (HPC) theory of natural kinds. Boyd argues that natural kinds are clusters of properties maintained in homeostasis by underlying causal mechanisms. Kind membership is a matter of participating in the homeostatic cluster, not of possessing an essence. The HPC theory accommodates the messiness of biological and social kinds — kind boundaries can be vague, kind-typical properties can vary, and kind membership is a matter of degree. The theory preserves realism about kinds without requiring necessary and sufficient conditions for membership.

3. **Dupré (1993) "The Disorder of Things: Metaphysical Foundations of the Disunity of Science"** — Promiscuous realism. Dupré argues that there are many equally legitimate ways to divide the world into kinds, corresponding to different interests, theoretical purposes, and explanatory projects. No single taxonomy is uniquely correct — nature is disordered, and order is imposed by our classifications. Promiscuous realism challenges the monistic assumption that there is one true taxonomy and supports kind pluralism across different sciences and contexts.

4. **Millikan (1999) "Historical Kinds and the 'Special Sciences'"** — Historical kinds. Millikan argues that some kinds — most prominently biological species — are individuated not by intrinsic properties or essences but by their historical origins and etiologies. Kind membership is a matter of being part of a historical lineage, and kind-typical properties are those that have been historically selected for. Historical kinds support a form of realism without essentialism, compatible with evolutionary biology's rejection of species essentialism.

5. **Khalidi (2013) "Natural Categories and Human Kinds: A Causal Approach"** — The causal network theory of natural kinds. Khalidi argues that natural kinds are nodes in causal networks — they are individuated by the causal relations they enter into, not by intrinsic essences. A kind is natural to the extent that it is causally homogeneous (its instances share causal properties) and causally integrated (it figures in a wide range of causal generalizations). This theory bridges the gap between realist and conventionalist approaches, treating kinds as real (because causally efficacious) but not essentially fixed (because causal roles can vary across contexts).

6. **Hacking (2007) "Natural Kinds: Rosy Dawn, Scholastic Twilight"** — A critical history of the natural kind concept. Hacking traces the evolution of the concept from Mill through Russell to Kripke and Putnam, and raises skeptical concerns about whether the concept of a "natural kind" is coherent or useful. He introduces the concept of "interactive kinds" (or "looping kinds") — classifications that interact with the things classified, such that the classified things change in response to being classified. This is particularly relevant to social kinds (race, gender, mental disorders) and challenges the straightforward application of natural kind theory to the human sciences.

7. **Ellis (2001) "Scientific Essentialism"** — Natural kind essentialism grounded in the dispositional essences of the fundamental kinds of physics and chemistry. Ellis argues that the laws of nature are grounded in the essential dispositional properties of natural kinds. An electron has its charge, spin, and mass essentially — these properties constitute what an electron is and ground the laws governing electron behavior. Scientific essentialism provides a realist, anti-Humean account of laws and kinds.

8. **Goodman (1955) "Fact, Fiction, and Forecast"** — The "new riddle of induction" challenges the projectibility of natural kind predicates. Goodman argues that the predicate "grue" (green if observed before time t, blue if observed after t) is extensionally equivalent to "green" for all past observations, but we project "green" and not "grue" into the future. What justifies this asymmetry? The answer cannot be "green is a natural kind predicate" unless we already have a theory of natural kinds. Goodman's challenge exposes the circularity lurking in attempts to ground induction in natural kinds, and is essential for evaluating any argument that treats natural kinds as the foundation for inductive inference.

## Steps

### Step 1: Identify Kind Classification Claims and Kind Terms

Conduct an exhaustive scan of the argument reconstruction report and original text for all kind classification claims.

**Detection protocol — scan for kind-classifying vocabulary:**
- "natural kind," "real kind," "genuine kind"
- "species" (in the generic sense of "kind" as well as the biological sense), "genus"
- "category," "taxonomic category," "classification"
- "carves nature at the joints" (Platonic idiom), "joints of nature"
- "is a type of," "is a kind of," "belongs to the category of"
- "in the same category as," "a different kind from"
- "projectible predicate," "projectible kind"

**Detection protocol — scan for kind terms (nouns claimed or assumed to designate kinds):**
- Scientific kind terms: "water," "gold," "electron," "Homo sapiens," "tiger"
- Psychological kind terms: "emotion," "belief," "pain," "intelligence"
- Social kind terms: "race," "gender," "marriage," "money"
- Metaphysical kind terms: "substance," "property," "event," "person"
- Everyday kind terms: "chair," "tree," "mountain"

For each kind term, determine: (a) Is it explicitly classified as a natural kind, or is this presupposed? (b) What is the domain? (c) Does the argument provide criteria for kind membership? (d) Does the argument distinguish natural kinds from other categories (artifacts, social kinds, nominal kinds)? (e) Does the argument invoke kind terms in a way that suggests they support inductive inference or explanation? (If yes, this indicates a kind claim even without explicit classification.)

**Output**: A complete catalog of kind classification claims (KC1...KCn), with each claim's kind term, domain, classification claim, kind theory diagnostic hint, and structural role in the argument.

### Step 2: Diagnose the Implicit Theory of Natural Kinds

Determine which theory of natural kinds the argument presupposes, applying the five diagnostic tests (lexical, criteria, uniqueness, realism, modal) as described in the Kind Theory Diagnosis section of the Output specification above.

**Additional diagnostic considerations:**

- **Twin Earth test applicability**: If the argument uses Twin Earth-style thought experiments (or appeals to the idea that kind membership is determined by underlying nature rather than surface properties), classify as kind essentialism (Kripke/Putnam). This is one of the strongest diagnostic indicators.
- **Homeostatic language**: If the argument uses language like "cluster," "homeostasis," "mechanism maintains," "causal feedback," classify as HPC.
- **Pluralist acknowledgment**: If the argument explicitly says "there are many ways to classify" or "different sciences use different taxonomies," consider promiscuous realism or kind pluralism.
- **Construction language**: If the argument says "we construct kinds," "classifications are social," "kinds are made not found," classify as conventionalism.
- **Historical individuation**: If the argument says kind membership depends on origin or lineage, classify as historical kinds.

**Output**: A theory diagnosis as specified in Section 2 of the Output specification, with evidence cited from the argument.

### Step 3: Evaluate Classification Adequacy

Evaluate the adequacy of the kind classifications using the four dimensions described in the Classification Adequacy Assessment section above: membership criteria adequacy, projectibility assessment, explanatory role assessment, and boundary/vagueness assessment.

**Additional adequacy considerations:**

- **Stereotype vs essence gap**: Under kind essentialism, the argument may rely on the stereotype (surface properties by which we identify the kind) while claiming to talk about the essence (the underlying nature). If the argument does not distinguish these, or if it draws conclusions about the essence from the stereotype without scientific investigation, flag the stereotype-essence gap.
- **Mechanism specification gap**: Under HPC, the argument must identify the homeostatic mechanism that maintains the property cluster. If it says "K is an HPC kind" without specifying the mechanism, the HPC claim is incomplete. The mechanism is what distinguishes HPC from mere coincidental property clustering.
- **Lineage specification gap**: Under historical kinds, the argument must specify the relevant lineage. "X is a member of historical kind K because of its origin" is incomplete without specifying what the origin is and how lineage is traced.

**Output**: A classification adequacy assessment as specified in Section 3 of the Output specification, with ratings and justifications for each dimension.

### Step 4: Assess Cross-Domain Consistency

Apply the cross-domain consistency protocol described in Section 4 of the Output specification. For each domain represented in the argument's kind claims, assess whether the presupposed theory of kinds is adequate for that domain.

**Domain-specific assessment guidelines:**

| Domain | Suitable Kind Theories | Unsuitable Kind Theories | Notes |
|--------|----------------------|-------------------------|-------|
| Chemistry | Essentialism (microstructural), HPC (qualified) | Conventionalism (counterintuitive — chemical kinds seem robustly real) | Chemical kinds are the paradigm case for essentialism. H2O, Au, NaCl have clear microstructural essences. |
| Fundamental Physics | Scientific essentialism, Causal network theory | Conventionalism, Historical kinds | Fundamental particle kinds may have dispositional essences. |
| Biology (species) | HPC, Historical kinds, Promiscuous realism, Species-as-individuals | Kind essentialism (widely rejected in philosophy of biology) | Biological species essentialism is rejected because species evolve, have vague boundaries, and exhibit variation. HPC, historical, and individual-based accounts are standard. |
| Biology (higher taxa) | HPC, Conventionalism (some argue higher taxa are less natural) | Kind essentialism | Higher taxa (genera, families) may be less clearly natural kinds than species. |
| Psychology | HPC (emotions as affect programs + social modulation), Causal network theory, Conventionalism (social construction of emotion) | Kind essentialism (psychological kinds rarely have sharp essences) | Mental disorder classification (DSM) is a central test case — are mental disorders HPC kinds, practical kinds, or social constructions? |
| Social kinds (race, gender) | Conventionalism, Practical kind theory, Interactive kinds (Hacking) | Kind essentialism (almost universally rejected for social kinds) | Social kinds are interactive — the classification affects the classified, blurring the line between natural and social. |
| Medicine | HPC (many diseases as syndromes), Essentialism (infectious diseases with microbial essences) | Conventionalism alone (undermines medical realism) | Disease classification is a mix — some diseases have microbial essences, others are syndromes (HPC). |
| Everyday objects | Conventionalism, Practical kind theory, Promiscuous realism | Kind essentialism (everyday objects likely do not have microstructural essences) | "Chair" is a functional kind, not a natural kind by most accounts. |

**Output**: A cross-domain consistency report with domain inventory, uniformity assessment, domain-by-domain adequacy analysis, and theory-switching detection.

### Step 5: Evaluate Kind-Based Inferences

Arguments often use kind membership to draw further conclusions. "X is a member of kind K, therefore X has property P" — this inference is licensed only if the presupposed theory of kinds supports the connection between K-membership and P. Systematically evaluate each kind-based inference in the argument.

**Inference evaluation protocol:**

For each inference of the form "X is K therefore X has P":

1. **Identify the inferential basis**: What justifies the inference from K-membership to P under the presupposed theory? Under essentialism: P is part of the essence of K. The inference is deductive: if X is K and P is essential to K, then X has P. Under HPC: P is part of the homeostatic property cluster that defines K. The inference is inductive and qualified: typically, Ks have P (but there may be exceptions). Under causal network theory: K's causal role includes producing P. The inference is causal: being K puts X in a causal network that produces P. Under historical kinds: P is typical of the lineage. The inference is statistical. Under conventionalism: P is associated with K by convention.

2. **Assess justification under the presupposed theory**: Given the theory's criteria for kind membership and the kind's properties, does the inference hold? Is P actually part of the essence / cluster / causal role / lineage / convention of K? Does the argument provide evidence that P belongs to the kind's defining features? Are there recognized exceptions — things that are clearly K but lack P, or things that have P but are clearly not K?

3. **Modal calibration check**: What modal force does the inference carry? "X is K, therefore X necessarily has P" requires kind essentialism with P as part of the essence. "X is K, therefore X typically/probably has P" is compatible with HPC or historical kinds. "X is K, therefore by convention we attribute P to X" is compatible with conventionalism. If the argument draws a modally strong conclusion from a modally weak kind theory, flag the modal calibration gap.

4. **Normative leap detection**: Does the argument infer normative conclusions from kind membership? "X is a person, therefore X has moral rights" — this infers a normative property (moral rights) from kind membership (person). Natural kind theories do not directly support normative inferences: even if "person" is a natural kind, moral rights are not part of the natural kind's essence (unless one is a naturalistic moral realist). Flag any unargued inference from descriptive kind membership to normative status.

5. **Circularity check**: Does the inference rely on a definition of K that already presupposes P? "X is water because X has the watery properties, and X dissolves salt because X is water" — if "watery properties" include dissolving salt, the inference is circular. Natural kind essentialism typically avoids this by distinguishing surface properties (the stereotype) from essential properties (the underlying nature discovered by science), but the distinction must be maintained.

**Additional inference patterns to detect and evaluate:**

- **Kind-to-property inference**: "X is K, therefore X has P." The standard pattern described above.
- **Property-to-kind inference**: "X has P, therefore X is K." This requires that P is sufficient for kind membership — a much stronger requirement than P being typical of K. Flag any inference from typical properties to kind membership without addressing the sufficiency condition.
- **Kind-to-existence inference**: "K is a natural kind, therefore Ks exist." This is straightforward under kind realism but requires defending realism about kinds.
- **Kind-to-necessity inference**: "X is K, therefore X is necessarily P." This requires that P is part of the essence of K — a strong modal claim.
- **Kind-to-explanation inference**: "X has P because X is K." This requires that kind membership explains P — plausible under essentialism and HPC, less plausible under conventionalism.
- **Cross-kind inference**: "X is K1, K1 is a natural kind, therefore K2 (which overlaps or is related to K1) is also a natural kind." Cross-kind inferences require justification of the relationship between K1 and K2.

**Output**: For each kind-based inference, a structured evaluation: the inferential basis under the presupposed theory, the justification assessment (justified / partially justified / unjustified / underdetermined), modal calibration, normative leap detection (if applicable), and circularity assessment.

### Step 6: Compile Report

Synthesize all findings from Steps 1-5 into the structured Natural Kind Analysis Report.

**Report structure:**

1. **Header**: Argument identifier, source text reference, date of analysis, analyst identifier. Cross-reference with any available dependent reports (essentialist claim analysis, conceptual analysis).

2. **Section 1: Kind Claims Catalog** — Numbered catalog (KC1...KCn), each with kind term, domain, classification claim, kind theory hint, and structural role. Include a summary table grouping claims by domain.

3. **Section 2: Kind Theory Diagnosis** — Primary theory with evidence from all five diagnostic tests (lexical, criteria, uniqueness, realism, modal). Secondary or inconsistent theory commitments flagged. Diagnostic narrative: why this theory best fits the argument, what the nearest alternative would look like, and whether the argument's conclusions depend on the choice of kind theory.

4. **Section 3: Classification Adequacy** — Four-dimension assessment (membership criteria, projectibility, explanatory role, boundary/vagueness) for each kind claim. Summary adequacy rating for each kind claim: `adequate`, `partially_adequate`, `inadequate`, `underdetermined`.

5. **Section 4: Cross-Domain Consistency** — Domain inventory, uniformity assessment, domain-by-domain adequacy analysis, theory-switching detection, and cross-domain consistency rating: `consistent`, `inconsistently_applied`, `appropriately_pluralistic`, `unacknowledged_pluralism`.

6. **Section 5: Kind-Based Inference Evaluation** — For each kind-based inference: the inference, inferential basis under the presupposed theory, justification assessment, modal calibration, normative leap status, and circularity check. Summary inference rating: `inferences_justified`, `partially_justified`, `inferences_unjustified`.

7. **Section 6: Alternative Kind Theories** — Evaluate how the argument would fare under alternative theories of kinds. Would the kind claims be stronger or weaker? Would kind-based inferences be more or less justified? Identify which alternative theory would most strengthen and which would most undermine the argument.

8. **Section 7: Dialectical Implications** — If the argument is advanced in a debate where the nature of kinds is contested (e.g., realism vs conventionalism about biological species, essentialism vs HPC about chemical kinds), what is the dialectical situation? Can an opponent challenge the argument by adopting a different theory of kinds? Is the argument robust across kind theories, or is it theory-dependent?

9. **Section 8: Recommendations** — Optional. If the argument's kind claims are vulnerable to classification inadequacy, cross-domain inconsistency, or unjustified kind-based inferences, suggest strategies: adopting a more appropriate kind theory for specific domains, providing evidence for the kind's defining features, limiting the modal force of kind-based inferences, or explicitly adopting kind pluralism where domain differences require it.

## Quality Criteria

1. **Kind Theory Identification with Evidence**: The kind theory diagnosis is argued for with specific evidence from the argument's language, criteria, uniqueness assumptions, realism commitments, and modal claims. Alternative plausible theories are considered and reasons for rejecting them (or noting ambiguity) are provided. The diagnosis is consistent across the argument, or inconsistencies are flagged.

2. **Classification Adequacy**: Each kind claim is assessed for adequacy under the presupposed theory. Membership criteria are checked for completeness; projectibility is assessed against the theory's resources; explanatory role is evaluated; boundary and vagueness issues are identified. Inadequacies are documented with specific reasoning.

3. **Cross-Domain Consistency**: The argument's kind claims are assessed across domains for consistency. Domain-specific adequacy is evaluated using the domain-specific guidelines. Theory-switching between domains is detected and evaluated — implicit switching (unacknowledged) is flagged as a problem; explicit switching (acknowledged pluralism) is noted as methodologically defensible.

4. **Inference Justification**: Every kind-based inference in the argument is evaluated. The inferential basis is identified under the presupposed theory. Justification is assessed against the theory's resources. Modal calibration is checked (strong conclusions from weak kind theories are flagged). Normative leaps are detected and flagged. Circularity is checked.

5. **Pluralism Awareness**: The report does not assume that kind monism (one correct theory of kinds, one correct classification) is mandatory. Kind pluralism — the view that different domains or different purposes warrant different theories of kinds — is a legitimate philosophical position. The report evaluates whether the argument's pluralism (if present) is well-motivated and consistently applied, or whether it functions as an ad hoc defense against classification difficulties.

6. **Biological Species Sensitivity**: Biological species classification is one of the most philosophically complex domains for natural kind theory, and special care is required. The report does not simply apply a general theory of kinds to biological species without considering the species problem. Species essentialism is flagged as a minority position in contemporary philosophy of biology; the report notes this and assesses whether the argument's species claims can be reinterpreted under HPC, historical, or individual-based theories.

## Relations to Other Skills

**Depends on:**
- `phil-argument-reconstruct`: The kind claims cannot be reliably cataloged without the standard-form reconstruction. The reconstruction identifies where kind terms appear and what inferential role kind claims play.
- `phil-conceptual-analysis` (optional): If the argument treats kind terms as concepts to be analyzed, the conceptual analysis report provides the conceptual structure. This helps determine whether the argument treats kind classification as conceptual (true by definition) or empirical (true by discovery).
- `phil-essence-detect` (optional): Natural kind essentialism is a species of essentialist claim. If the essentialist claim analysis report is available, it identifies which properties the argument treats as essential to the kind and which essence framework is presupposed. This directly informs the kind theory diagnosis, especially for essentialist and HPC theories.

**References (read-only):**
- `ontological-categories.md`: The taxonomy of ontological categories. The kind classification ("kind" as an ontological category) is part of this taxonomy, and the kind claims in the argument should be cross-referenced with the ontological category taxonomy to ensure consistency.
- `glossary-metaphysics.md`: Definitions of technical terms (essentialism, HPC, promiscuous realism, rigid designator, projectibility, homeostatic mechanism, lineage, historical kind, interactive kind, looping effect, etc.) used in the report.
- `causation-taxonomy.md`: Causal mechanisms are central to HPC and causal network theories of kinds. The causation taxonomy provides resources for analyzing the causal claims embedded in kind theories.

**Dependents (skills that use this skill's output):**
- `phil-essence-detect` (reverse dependency): The natural kind analysis report identifies which kind theory is presupposed, which informs the essentialist claim analysis of kind essences. If the kind theory is HPC, the essentialist analysis shifts from essentialist detection to cluster analysis.
- `phil-ontological-commitment`: The kind claims may generate ontological commitments (to kinds, to essences, to universal properties). The natural kind analysis report identifies which kinds are claimed to exist and under what theory, which the ontological commitment report can integrate into its broader ontology.

## Boundary Conditions

### 1. No Kind Claims

If the argument contains no kind classification language and draws no kind-based inferences, output:

> "No natural kind claims detected. This argument does not rely on natural kind classification. Natural kind analysis is not applicable."

Explain why: the argument's language and reconstructed structure contain no kind terms, kind classification claims, or kind-based inferences. Do not invent kind claims where none are present.

### 2. Social Kinds (Race, Gender, Class)

When the argument concerns race, gender, social class, or other socially constituted categories, the kind analysis must engage with the literature on social kinds specifically. Key considerations for social kinds include: looping effects (Hacking) — classifying people as "of kind K" changes how they are treated and how they understand themselves, which in turn changes the properties associated with K, creating a dynamic absent from non-social natural kinds; normative entanglement — social kind classifications are often normatively loaded, and the report should flag any normative entanglement; and naturalizing social kinds — arguments that treat social kinds as straightforward natural kinds (e.g., biological race realism) should be flagged as philosophically contentious and assessed against the extensive literature critiquing biological determinism about social categories.

### 3. Biological Species

When the argument concerns biological species classification, the kind analysis must engage with the species problem specifically. Key species concepts to reference: Biological Species Concept (Mayr) — species as interbreeding populations reproductively isolated from others; Phylogenetic Species Concept — species as lineages between speciation events; Ecological Species Concept — species as lineages occupying distinct ecological niches; Species as Individuals (Ghiselin, Hull) — species are not kinds at all but concrete historical individuals; Species as HPC kinds (Boyd) — species are HPC natural kinds. The report should check whether the argument acknowledges the species pluralism debate and whether its conclusions survive under alternative species concepts.

### 4. Normatively Loaded Kinds

If the argument classifies a normatively loaded category as a natural kind — e.g., "person" (with attendant moral status), "mental disorder" (with implications for treatment and responsibility), "intelligence" (with social policy implications) — flag the normative dimension. The classification of K as a natural kind carries implications for the relevant normative domain. This report identifies the normative implications and notes whether the argument's kind-theoretic claims are sufficient to support the normative conclusions. Normative inferences from descriptive kind claims require additional justification not provided by kind theory alone. This is especially important when the move from "K is a natural kind" to "we ought to treat Ks differently" is made without argument — natural kind status does not directly entail normative status.

### 5. Mathematical Kinds

If the argument classifies mathematical entities (numbers, sets, groups, topological spaces) as natural kinds, apply mathematical-kind-specific analysis. Whether mathematical kinds are natural kinds in the same sense as chemical or biological kinds is contested. Platonism may treat mathematical kinds as having essences (e.g., the number 2 is essentially the successor of 1), but the epistemology and metaphysics of mathematical kinds differ significantly from empirical natural kinds. Mathematical essentialism may be more defensible than biological essentialism (mathematical objects are not subject to evolution, do not have vague boundaries, and their essential properties are arguably knowable a priori), but this should be distinguished from scientific essentialism about empirical kinds.

## ARS Interface

The natural kind analysis report serves four primary functions within the broader Academic Research System (ARS).

**1. Academic Paper Integration**

The report can be passed to `ars academic-paper` as a "natural kind analysis" section suitable for inclusion in the argument-analysis or philosophical-background chapter. The structured format (kind claims catalog, theory diagnosis, classification adequacy, cross-domain consistency, inference evaluation) maps directly to academic prose. The section would typically read: "The argument relies on the classification of [K1, K2, ...] as natural kinds. This classification presupposes a [essentialist/HPC/conventionalist] theory of natural kinds, as evidenced by ... The classification is [adequate/inadequate] for the argument's purposes because ... The argument's kind-based inferences are [justified/partially justified/unjustified] under this theory because ..."

**2. Deep Research Integration**

The report informs `ars deep-research` by identifying which kind-classification debates the paper engages. If the report diagnoses kind essentialism, the module searches for Kripke, Putnam, essentialism about biological species, and critiques of essentialism. If the report diagnoses HPC, it searches for Boyd, HPC responses to essentialism, and applications of HPC to specific domains. If the report identifies species classification issues, it searches for the species problem literature. If the report identifies social kind issues, it searches for Hacking's interactive kinds and social ontology. This enables targeted literature discovery for each domain.

**3. Reviewer Integration**

When used with `ars reviewer` or `ars rebuttal-audit`, the natural kind analysis report identifies vulnerabilities that a philosophically sophisticated reviewer is likely to raise: classification inadequacy (if kind membership criteria are not specified), cross-domain inconsistency (if different domains are treated uniformly when domain-specific considerations require different treatment), unjustified kind-based inferences (if the argument draws conclusions from kind membership that the presupposed theory cannot license), and biological essentialism (if the argument applies essentialism to species without engaging with the species problem). The report enables preemptive addressing of these critiques.

**4. Cross-Skill Pipeline Integration**

The natural kind analysis report occupies a bridging position in the metaphysics pipeline. It receives inputs from the argument reconstruction (foundational structure), the conceptual analysis (concept-level kind claims), and the essentialist claim analysis (essence framework for kind essences). It provides outputs to the ontological commitment analysis (kind claims as ontological commitments) and the identity-persistence analysis (kind membership constrains identity and persistence). The report also has significant interfaces with philosophy of science, philosophy of biology, and social ontology, making it one of the most cross-disciplinary skills in the metaphysics pipeline.
