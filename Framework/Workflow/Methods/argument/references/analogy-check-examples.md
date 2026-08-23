# Analogy Check — examples (conditional reference for method.argument.analogy-check)

> Loaded only when the consuming mode's live ambiguity or the user's explicit request requires it; never loaded by default with the method file.

# Analogy Analysis Examples

> This document demonstrates the practical application of analogical argument analysis across classic philosophical analogies. Each example shows the complete input-to-output process.

---

## Example 1: Paley's Watchmaker Analogy (Design Argument)

### Input

> In crossing a heath, suppose I pitched my foot against a stone, and were asked how the stone came to be there; I might possibly answer, that, for anything I knew to the contrary, it had lain there forever... But suppose I had found a watch upon the ground, and it should be inquired how the watch happened to be in that place; I should hardly think of the answer I had before given, that for anything I knew, the watch might have always been there. ... For this reason, and for no other, viz. that, when we come to inspect the watch, we perceive that its several parts are framed and put together for a purpose. ... [The inference] is inevitable, that the watch must have had a maker ... [E]very indication of contrivance, every manifestation of design, which existed in the watch, exists in the works of nature; with the difference, on the side of nature, of being greater or more, and that in a degree which exceeds all computation.
>
> -- William Paley, *Natural Theology* (1802)

The argument infers from the evident design in a watch (source) to the existence of design in the universe (target), and concludes that the universe, like the watch, must have an intelligent designer.

### Output

```
## Analogy Analysis Report

### Analogy Summary

Paley argues that the natural world exhibits the same marks of design and contrivance as a watch, and that the inference from design to a designer — which is irresistible in the case of the watch — applies with equal (indeed greater) force to the natural world. The source domain is a mechanical artifact (a watch), the target domain is the natural universe, the shared property is the appearance of purposive organization of parts, and the projected property is the existence of an intelligent designer.

### Source–Target Mapping Table

Object/Entity Mappings:
  Watch                     →  Universe (or parts of nature, e.g., the eye)
  Watchmaker                →  Divine Creator
  Watch parts (gears, etc.) →  Natural parts (organisms, organs)

Attribute/Property Mappings:
  Exhibits complexity        →  Exhibits complexity
  Parts serve functions      →  Parts serve functions
  Adjustment of means to ends →  Adjustment of means to ends

First-Order Relational Mappings (R1):
  Parts are arranged such that each contributes to a function
    →  Organs are arranged such that each contributes to an organism's survival

Higher-Order Relational Mappings (R2):
  Functional arrangement of parts → explanatory necessity of a designer (in S)
    →  Functional arrangement of parts → explanatory necessity of a designer (in T)

Projected Property (P*):
  The existence of an intelligent designer who arranged the parts for a purpose.

### Analogy Type Classification

- **Illustrative vs. Argumentative:** Argumentative. Paley uses the watch explicitly as a premise for the existence of a divine designer; the analogy is meant to license an inference.
- **A Priori vs. Empirical:** Empirical. The inference depends on the contingent, empirically observable fact that functional complexity in artifacts is invariably produced by intelligent agents, and on the empirical claim that nature exhibits the same kind of functional complexity.
- **Formal vs. Material:** Material. The shared properties (functional arrangement, complexity, adaptation of means to ends) are substantively connected to the projected property (designer) through the causal principle that purposive organization requires a purposive organizer.
- **Hesse's Taxonomy:**
  - Positive analogy: complexity, functional arrangement, adaptation of means to ends
  - Negative analogy: artifact vs. organism (watches are manufactured; organisms grow), material composition (metal vs. organic tissue), temporal origin (watches have a known origin; the universe's origin is contested)
  - Neutral analogy: whether the designer is singular, benevolent, or still active

### Relevance Assessment

**Connecting principle identified:** Functional complexity of the kind exhibited by artifacts is invariably and uniquely produced by intelligent agency. In the source domain (the watch), the prior association is well-established: we know from universal experience that watches are products of deliberate design, and we have no counter-instances of functionally complex artifacts arising without design.

**Connection type:** Causal/functional. The shared properties (functional arrangement of parts) are the effect of a cause (intelligent design) in the source domain, and the argument projects that the same causal relation holds in the target domain.

**Strength of connecting principle:** The principle is inductively robust within the artifact domain: all known watches, and indeed all known complex functional artifacts, are products of design. However, the principle's extension to the biological domain is precisely what is at issue. The analogy's force depends on whether nature's functional complexity is sufficiently similar to artifactual functional complexity to warrant the same causal inference. If organisms and their parts can be explained by natural selection — a non-intentional mechanism that produces functional complexity without a designer — then the connecting principle, while true of artifacts, does not apply to organisms. The prior association holds in the source but the potential for generalization is blocked.

### Disanalogy Detection and Impact Analysis

| Disanalogy | Severity | Impact |
|------------|----------|--------|
| Artifacts are manufactured; organisms reproduce and grow | Defeating (post-Darwin) | Natural selection provides an alternative causal mechanism for the production of functional complexity that does not require a designer. This disanalogy severs the inferential link: the reason we infer a designer for watches is that we know of no alternative mechanism for producing artifactual functional complexity, but we do know of an alternative mechanism for biological functional complexity. |
| Watches have a known temporal origin; the universe's origin is unknown | Weakening | The analogy would be stronger if both source and target had known origins, but this difference does not independently defeat the inference. |
| Watches are composed of inert matter; organisms are composed of living matter | Irrelevant | The compositional difference does not interact with the inferential pathway. The question is whether functional complexity can arise without design, not what the functionally complex things are made of. |
| The universe contains suffering and imperfection; watches (ideally) do not | Weakening | If the designer is supposed to be omnibenevolent, this disanalogy is significant. But if the conclusion is merely that *some* designer exists (not necessarily benevolent), this disanalogy is less damaging. Paley's argument does not require benevolence. |

### Counter-Analogy Audit

**Counter-Analogy 1 (Hume's alternative):** A living organism (e.g., a vegetable) as the source domain. Living things exhibit functional organization but arise from generation and growth rather than from a designer's intervention. If the universe is more like a living organism than a watch, then the inference to a transcendent designer is blocked.

- *Plausibility:* The organism shares the cited properties (functional complexity, adaptation of parts to ends) but lacks the projected property (an external designer).
- *Relevance:* The inferential pathway is the same: functional complexity requires explanation. The counter-analogy shows that functional complexity can be explained by immanent causal processes (growth, reproduction) without a designer.
- *Dialectical burden:* The counter-analogy shifts the burden to Paley to explain why the universe is more like a watch than like an organism. Hume's extended critique in the *Dialogues* presses precisely this point.

**Counter-Analogy 2 (Darwinian):** The eye as the source domain, but explained by natural selection. The eye exhibits functional complexity that, prior to Darwin, seemed to require a designer. But the theory of natural selection provides a non-intentional mechanism that produces the same functional complexity. The "watch" analogy is retroactively undermined because the biological domain that was supposed to be its target is now known to operate by different causal principles.

### Argumentative Force Assessment

**Grade: Merely Rhetorical (post-Darwin).** Prior to Darwin, the analogy was Strong: the prior-association condition was satisfied (all known instances of functional complexity were products of design), and no alternative mechanism had been demonstrated. Post-Darwin, the analogy is undermined by a defeating disanalogy: natural selection shows that biological functional complexity arises without a designer. The connecting principle (functional complexity → designer) holds for artifacts but does not generalize to organisms, because the causal mechanism in the target domain differs from the causal mechanism in the source domain. The analogy retains rhetorical force — it is vivid, intuitive, and still deployed in popular apologetics — but it carries no genuine argumentative weight for a reader who accepts evolutionary biology.

### Fallacy Cross-Reference

The post-Darwin deployment of this analogy may commit the **fallacy of suppressed disanalogy**: the proponent fails to acknowledge the relevant and significant difference between artifactual and biological functional complexity — namely, that the latter is explained by natural selection. If the proponent is aware of the Darwinian explanation and suppresses it, the argument is fallacious. If the proponent is unaware of it, the argument is merely unsound rather than fallacious.

### Dialectical Impact and Recommendations

**For the proponent:** The analogy cannot be repaired by tinkering with the mapping. The defeating disanalogy is fundamental: the target domain operates by causal principles that differ from those in the source domain. The proponent might attempt to defend the analogy by arguing that natural selection itself requires a designer (e.g., to set the laws of nature or to guide the process), but this shifts the argument from analogical inference to an independent argument about the origin of laws. The proponent would do better to abandon the analogy and argue directly for design on other grounds (e.g., fine-tuning, cosmological arguments).

**For the respondent:** The most efficient line of attack is the Darwinian disanalogy: point out that the functional complexity of biological systems is explained by natural selection, a mechanism with no analogue in the source domain. The respondent can also deploy Hume's organism counter-analogy to show that the inference from functional complexity to a designer is not inevitable — there are perfectly coherent alternative explanatory frameworks. The respondent does not bear the burden of proving that the Darwinian explanation is correct; it suffices to show that the analogy's inference is blocked by a plausible alternative mechanism.
```

---

## Example 2: Mill's Argument from Analogy for Other Minds

### Input

> I conclude that other human beings have feelings like me, because, first, they have bodies like me, which I know, in my own case, to be the antecedent condition of feelings; and because, secondly, they exhibit the acts, and other outward signs, which in my own case I know by experience to be caused by feelings. ... [T]his argument is exactly of the form of an analogical inference. ... I am conscious in myself of a series of facts connected by a certain law of causation. ... I observe a similar series of facts in another; and, because the two series agree in many respects, I infer that they agree in all.
>
> -- John Stuart Mill, *An Examination of Sir William Hamilton's Philosophy* (1865)

### Output

```
## Analogy Analysis Report

### Analogy Summary

Mill argues that we are justified in believing that other human beings have minds (thoughts, feelings, sensations) by analogical inference from our own case. The source domain is one's own mind–body connection (I observe that my bodily states and behaviors are correlated with and caused by mental states), and the target domain is other human bodies (which exhibit bodily states and behaviors similar to mine). The inference is that the same causal relation — behavior as an effect of mental states — holds for others as it does for oneself.

### Source–Target Mapping Table

Object/Entity Mappings:
  My body                    →  Other human bodies
  My mind (known directly)   →  Other minds (inferred)
  My behaviors               →  Others' behaviors

Attribute/Property Mappings:
  Has a physical body        →  Has a physical body
  Exhibits goal-directed behavior → Exhibits goal-directed behavior

First-Order Relational Mappings (R1):
  My mental states cause my bodily behavior
    →  Their mental states cause their bodily behavior
  My bodily states (injury, etc.) cause my mental states (pain, etc.)
    →  Their bodily states cause their mental states

Higher-Order Relational Mappings (R2):
  The same causal law that connects my mind to my body connects their minds to their bodies.

Projected Property (P*):
  The existence of mental states (consciousness, feelings, sensations, thoughts) in other human beings.

### Analogy Type Classification

- **Illustrative vs. Argumentative:** Argumentative. Mill presents this as the rational basis for the belief in other minds; it is not merely an illustration of a conclusion reached on other grounds.
- **A Priori vs. Empirical:** Empirical. The inference depends on the contingent, empirically knowable correlation between mental states and bodily states in one's own case, and on the contingent similarity between one's own body and behavior and others' bodies and behavior.
- **Formal vs. Material:** Material. The connection between the shared properties (bodily similarity, behavioral similarity) and the projected property (mental states) is causal and nomological.
- **Hesse's Taxonomy:**
  - Positive analogy: physical body, observable behavior, structural similarity of behavior patterns
  - Negative analogy: direct access to one's own mental states but only indirect access to others'; qualitative differences in behavior across individuals
  - Neutral analogy: the qualitative character of others' mental states (are their pains like my pains?)

### Relevance Assessment

**Connecting principle identified:** Similar effects have similar causes. The similarity of others' bodily behavior to my own, combined with the fact that in my own case such behavior is caused by mental states, licenses the inference that others' behavior is likewise caused by mental states.

**Connection type:** Causal. In the source domain (my own case), mental states are causally responsible for bodily behavior. The analogy projects that the same causal relation obtains in the target domain.

**Strength of connecting principle:** The principle is a standard canon of inductive reasoning (Mill's own Method of Agreement). However, there is a special problem: the source domain consists of a single instance — one's own case. The prior association, while correct in that one instance, is established only in that instance, and the argument projects from a single case to all other cases. This is the structural weakness of the argument: it has the form of an analogical inference but the epistemic basis of an induction from a sample of one. The prior-association condition is satisfied — in my own case, behavior and mental states are causally connected — but the potential for generalization faces a deeper challenge: can a single instance support generalization to an entire population?

### Disanalogy Detection and Impact Analysis

| Disanalogy | Severity | Impact |
|------------|----------|--------|
| I have direct (privileged) access to my own mental states but not to others' | Defeating (for strong conclusions) | This disanalogy does not block the inference — the argument does not claim that we know others' minds with the same certainty as our own — but it limits the analogy's ambition. Mill himself acknowledges that the analogical inference yields only probability, not certainty. |
| The source domain is a single instance; the target domain comprises billions | Weakening | The inference from one case to many is structurally weak. A single correlation between behavior and mental states in one case does not, by itself, provide a robust basis for generalizing to all cases. |
| Behavioral variation across individuals (others do not behave exactly as I do) | Irrelevant | The analogy requires similarity, not identity. Variations in behavior are compatible with the same underlying causal structure. |
| The possibility of a "zombie" (physical duplicate without consciousness) | Weakening | If philosophical zombies are conceivable, then behavioral similarity does not entail mental similarity, and the analogical inference is underdetermined. However, most participants in this debate do not treat the mere conceivability of zombies as defeating the everyday inference to other minds. |

### Counter-Analogy Audit

**Counter-Analogy 1 (The solipsist's challenge):** A sophisticated automaton that mimics human behavior without consciousness. If such a thing is possible, then behavioral similarity is not a reliable indicator of mental states. The counter-analogy is structurally relevant — it shares the cited properties (behavioral similarity) with the target but lacks the projected property (mental states).

- *Plausibility:* Current robots do not exhibit the full range of human behavioral complexity, so the counter-analogy is not yet empirically compelling. But as AI advances, its plausibility increases.
- *Relevance:* The counter-analogy tracks the same inferential pathway: behavioral similarity is supposed to warrant the inference to mental states. If there can be behavioral similarity without mental states, the analogy's inference is not logically compelled.

**Counter-Analogy 2 (The inference to animal minds):** If behavioral similarity warrants the inference to mental states for other humans, does it also warrant the inference for non-human animals? Animals exhibit behavioral patterns that resemble human behavior (e.g., pain behavior when injured). If the analogical inference is sound for humans, parity reasoning compels its extension to animals with comparable behavioral complexity. This counter-analogy does not undermine the original analogy; rather, it shows that the analogy has broader implications than Mill may have intended, and it tests the proponent's willingness to accept the full scope of the inferential principle.

### Argumentative Force Assessment

**Grade: Moderate.** The prior-association condition is satisfied: in my own case, behavioral similarity and mental states are causally connected. However, the argument is structurally weak for two reasons. First, it reasons from a single instance — the sample size is one, which is the weakest possible basis for an inductive generalization. Second, the projected property (conscious mental states) is not directly observable in the target domain, which means the conclusion cannot be independently verified; this is not a defect of the analogy per se but a feature of the epistemic situation. The analogy provides *some* rational support for the belief in other minds — it is better than a mere guess — but it does not compel assent. Most philosophers treat the problem of other minds as an instance where analogy is the best we can do, not where it is especially strong. The analogy's force is supplemented (in ordinary life) by an instinctive, non-inferential disposition to attribute mental states to others, so the analogy is not the sole basis for the belief.

### Fallacy Cross-Reference

The argument does not commit a fallacy. It is a weak inference, but not fallaciously weak. Mill is explicit about its limitations and does not claim more than the analogy can deliver. The argument does not suppress a defeating disanalogy (the privileged-access problem is acknowledged), and it does not rely on a single atypical instance (one's own case, while singular, is the only directly accessible case and hence not "atypical" in a way that distorts the inference).

### Dialectical Impact and Recommendations

**For the proponent:** The analogy can be strengthened by adding instances — for example, by noting that not only my own behavior but also the behavior of others I observe *and independently confirm* to have mental states (e.g., through testimony) follows the same pattern. This increases the sample size and partially addresses the single-instance problem. The proponent can also argue that the inference to other minds is an inference to the best explanation rather than a pure analogy: the hypothesis that others have minds best explains the observed behavioral complexity, and competing explanations (automata, Cartesian evil demons) are less parsimonious.

**For the respondent:** The most efficient line of attack is the single-instance problem: the analogy extrapolates from one case, which is inductively insufficient. However, the respondent should recognize that rejecting the analogical inference leaves them with no alternative basis for the belief in other minds (except perhaps a direct perceptual or instinctive account), so the cost of rejection is high.
```

---

## Example 3: Thomson's Violinist Analogy (Normative Analogy)

### Input

> You wake up in the morning and find yourself back to back in bed with an unconscious violinist. A famous unconscious violinist. He has been found to have a fatal kidney ailment, and the Society of Music Lovers has canvassed all the available medical records and found that you alone have the right blood type to help. They have therefore kidnapped you, and last night the violinist's circulatory system was plugged into yours, so that your kidneys can be used to extract poisons from his blood as well as your own. ... To unplug you would be to kill him. But never mind, it's only for nine months. ... [I]s it morally incumbent on you to accede to this situation?
>
> -- Judith Jarvis Thomson, "A Defense of Abortion" (1971)

The argument proceeds by analogy: the violinist scenario is relevantly similar to pregnancy resulting from rape, and the intuition that you are not morally obligated to remain plugged into the violinist supports the conclusion that abortion is permissible, at least in cases of rape.

### Output

```
## Analogy Analysis Report

### Analogy Summary

Thomson constructs a vivid source scenario (being involuntarily connected to a famous violinist who depends on your kidneys for nine months) and argues that it is analogous to pregnancy (the target). The shared features include: an innocent person's life depends on the continued use of another's body, the bodily use was imposed without consent, and terminating the bodily use results in the dependent person's death. From the intuition that unplugging oneself from the violinist is morally permissible (and not required), Thomson projects that abortion is likewise morally permissible — at minimum in cases where pregnancy results from rape, and arguably more broadly.

### Source–Target Mapping Table

Object/Entity Mappings:
  You (kidnapped person)     →  Pregnant woman
  The violinist              →  The fetus
  The Society of Music Lovers →  The rapist (in rape cases) or circumstance
  Your kidneys               →  The woman's uterus/body
  The hospital bed           →  The woman's body during pregnancy

Attribute/Property Mappings:
  Innocent person            →  Innocent being (the fetus is not at fault)
  Life depends on bodily use  →  Life depends on bodily use
  Bodily connection imposed without consent → Bodily connection imposed without consent

First-Order Relational Mappings (R1):
  Unplugging → violinist dies
    →  Aborting → fetus dies
  Remaining plugged → nine months of bodily burden
    →  Continuing pregnancy → nine months of bodily burden (and more)

Higher-Order Relational Mappings (R2):
  The right to bodily autonomy outweighs another's right to life when the bodily connection is involuntary.
    →  The right to bodily autonomy outweighs the fetus's right to life (at least in cases of involuntary pregnancy).

Projected Property (P*):
  It is morally permissible to terminate the bodily connection (i.e., to abort), at least in cases where the pregnancy is involuntary.

### Analogy Type Classification

- **Illustrative vs. Argumentative:** Argumentative. Thomson deploys the analogy to establish a moral conclusion (the permissibility of abortion). The intuition elicited by the source scenario is meant to directly support the normative claim about the target.
- **A Priori vs. Empirical:** Mixed. The moral premise (the right to bodily autonomy) is normative and evaluated a priori. But some features of the analogy (e.g., the nine-month duration, the nature of pregnancy's burdens) are empirical.
- **Formal vs. Material:** Material. The shared properties are substantively connected to the projected property through a normative principle concerning bodily autonomy.
- **Hesse's Taxonomy:**
  - Positive analogy: involuntary bodily connection, life-or-death stakes, finite duration, innocent dependent
  - Negative analogy: the violinist is a stranger, while the fetus is genetically related to the mother; the Society of Music Lovers is an identifiable agent, while pregnancy (in rape cases) involves a distinct kind of violation; kidneys vs. uterus (different bodily organs with different biological functions); the violinist is a fully developed adult while the fetus is an embryo/fetus at an early developmental stage
  - Neutral analogy: the exact scope of the conclusion (does the analogy extend to consensual pregnancy?)

### Relevance Assessment

**Connecting principle identified:** The right to control one's own body (bodily autonomy) is sufficiently strong that it is not overridden by another person's need for the use of that body, even when the other person's life is at stake, provided that the bodily connection was not voluntarily assumed. This principle is supported in the source scenario by the intuition that one is not obligated to remain plugged into the violinist.

**Connection type:** Functional/normative. The shared features (involuntary bodily connection, life-or-death dependency) are normatively relevant because they jointly satisfy the antecedent of a moral principle about bodily autonomy, and this principle yields the projected normative conclusion in both source and target.

**Strength of connecting principle:** The principle is widely (though not universally) accepted within liberal moral and political philosophy. It is challenged by those who hold that the right to life always outweighs the right to bodily autonomy, or who hold that the right to life can generate positive obligations (duties to rescue) that include the obligation to sustain another's life through bodily means. The analogy's dialectical effectiveness depends on the audience's prior acceptance of a robust right to bodily autonomy.

### Disanalogy Detection and Impact Analysis

| Disanalogy | Severity | Impact |
|------------|----------|--------|
| The fetus is the woman's biological offspring; the violinist is a stranger | Potentially Defeating (depending on parental obligation theory) | If parents have special obligations to their offspring that they do not have to strangers, then the fetus's status as one's biological child may generate obligations that the violinist's status as a stranger does not. Thomson anticipates this: she extends the analogy to cases of voluntary pregnancy by noting that one can acquire obligations through voluntary action (e.g., if you voluntarily plugged yourself into the violinist). But in rape cases, the parental obligation objection loses force because the pregnancy was not voluntarily assumed. |
| The violinist is an adult; the fetus is not yet a person (or has a different moral status) | Contested | If the fetus lacks full moral personhood, then the analogy overestimates the fetus's moral standing — the violinist is unquestionably a person, and the moral calculus changes if the fetus is not. Thomson grants the fetus full personhood for the sake of the argument, so this disanalogy is neutralized within the dialectic, but it is a live question outside it. |
| The Society of Music Lovers is a third-party agent; pregnancy (in rape) involves a different kind of violation | Irrelevant (within the analogy's scope) | The mechanism of involuntary bodily connection differs, but the relevant feature — involuntariness — is preserved. The difference in the identity of the causal agent does not affect the normative question of whether one may terminate the connection. |
| Nine months of kidney dialysis vs. nine months of pregnancy | Weakening | Pregnancy involves a broader and deeper set of burdens (hormonal changes, physical risks, social consequences, permanent bodily changes) than the violinist scenario acknowledges. However, this disanalogy may strengthen the pro-abortion conclusion: if the lesser burden does not obligate, the greater burden surely does not. |
| "Unplugging" is passive; abortion is active | Historically significant but dialectically addressed | The doing/allowing distinction has been central to critiques of the analogy. Thomson addresses this by arguing that unplugging is an action, not a mere omission, and that even if there were a morally significant distinction, it would not justify a blanket prohibition on abortion. The debate remains live. |

### Counter-Analogy Audit

**Counter-Analogy 1 (The "people-seeds" analogy):** Thomson herself offers a counter-analogy for consensual pregnancy. People-seeds drift through the air and, if they land in your carpet, grow into children. You can take reasonable precautions (screens on windows), but sometimes a seed gets in anyway. The question is whether you may uproot the person-plant. This counter-analogy tests the extension of the violinist analogy to cases of consensual sex with contraception.

- *Plausibility:* There is no actual biological analogue to people-seeds, but the analogy is structurally clear and tests the same normative principle.
- *Relevance:* It tracks the same inferential pathway (bodily autonomy vs. life) but introduces a different kind of causal responsibility.

**Counter-Analogy 2 (The "drowning child" disanalogy):** If you encounter a drowning child in a shallow pond and can save them at minimal cost (muddy clothes), you are morally obligated to do so, even though you did not cause the child's predicament. This analogy is sometimes deployed against Thomson: it suggests that moral obligations can arise from need alone, without voluntary assumption. If the drowning child analogy is sound, then perhaps the pregnant woman does have an obligation to sustain the fetus.

- *Plausibility:* The drowning child analogy shares one feature (innocent life at stake, no voluntary assumption of obligation) but differs in a crucial respect: it does not involve sustained bodily intrusion. Saving a drowning child is a one-time action; sustaining a pregnancy is a nine-month bodily process. This disanalogy limits the counter-analogy's force against Thomson.
- *Relevance:* It challenges the connecting principle (no obligation without voluntary assumption) by providing a counterexample. But because of the bodily-autonomy disanalogy, it may not successfully block Thomson's argument.

### Argumentative Force Assessment

**Grade: Strong (within its limited scope).** The analogy is well-constructed and survives many standard objections, largely because Thomson anticipated and preemptively addressed them. The prior-association condition is satisfied: the connection between involuntary bodily connection and the absence of an obligation to sustain another's life is supported by a widely endorsed normative principle. The remaining disanalogies (parental obligation, fetal personhood, the doing/allowing distinction) are contested in ways that turn on deeper normative and metaphysical commitments rather than on structural defects in the analogy. The analogy does not establish its conclusion deductively — no analogical argument does — but it substantially shifts the dialectical burden: the respondent must either identify a principled, non-ad-hoc distinction between the violinist case and pregnancy, or concede that abortion is permissible. The analogy's scope is limited: it applies most clearly to pregnancy resulting from rape, and Thomson requires additional argumentative resources to extend it to consensual pregnancy. Within that limited scope, the analogy is dialectically weighty.

### Fallacy Cross-Reference

The analogy does not commit a fallacy. Thomson is explicit about the limits of the analogy, acknowledges potential disanalogies, and develops the argument through a series of increasingly nuanced analogies rather than resting everything on a single, underdescribed comparison. The argument is a model of careful analogical reasoning and is not vulnerable to any of the standard false-analogy subcategories.

### Dialectical Impact and Recommendations

**For the proponent:** The analogy is already well-developed, but the proponent can strengthen it by explicitly articulating the normative principle (the right to bodily autonomy and its limits) and defending it independently of the analogy. The doing/allowing objection remains the most significant challenge and requires sustained engagement.

**For the respondent:** The most promising lines of attack are: (1) the parental-obligation disanalogy — argue that biological parenthood generates obligations beyond those owed to strangers, even in involuntary cases; (2) the fetal-personhood disanalogy — argue that Thomson's granting of full personhood to the fetus distorts the moral calculus; (3) the doing/allowing distinction — argue that abortion is an active killing, not a passive withdrawal of support. The respondent should not attempt to dismiss the analogy wholesale; it is too well-constructed for that. Instead, they should argue that the analogy's scope does not extend as far as Thomson claims.
```

---

## Example 4: The Brain-as-Computer Analogy

### Input

> The brain is, in essence, an information-processing device — a biological computer. Neurons receive inputs, process signals, and produce outputs, much like the logic gates in a digital computer. Just as a computer's software can be understood independently of its hardware, so too can the mind be understood independently of the brain. Therefore, the study of cognition can proceed at the level of mental representations and computational processes without reference to neurobiology.

This is a composite argument drawing on the computational theory of mind (Putnam, Fodor, Pylyshyn). The analogy maps the structure and function of digital computers onto the structure and function of the brain, and projects the property of multiple realizability (and thus the autonomy of cognitive science from neuroscience) from the computer domain to the mental domain.

### Output

```
## Analogy Analysis Report

### Analogy Summary

The brain-as-computer analogy maps the functional architecture of digital computers (input processing, algorithmic transformation, output generation, hardware/software distinction) onto the human brain. The argument infers that cognition, like software, can be studied at a level of abstraction independent of its physical implementation — a conclusion that, if sound, would establish the autonomy of cognitive science from neuroscience.

### Source–Target Mapping Table

Object/Entity Mappings:
  Computer (hardware)        →  Brain
  Software (program)         →  Mind / cognitive processes
  Logic gates                →  Neurons
  Input devices              →  Sensory organs
  Output devices             →  Motor systems
  Memory (RAM, hard disk)    →  Memory (short-term, long-term)

Attribute/Property Mappings:
  Processes information      →  Processes information
  Executes algorithms        →  Executes cognitive operations
  Modular architecture        →  Functional modularity

First-Order Relational Mappings (R1):
  Input → processing → output
    →  Sensory input → cognitive processing → behavioral output
  Hardware implements software
    →  Brain implements mind

Higher-Order Relational Mappings (R2):
  Multiple realizability: same software can run on different hardware
    →  Same cognitive processes can be realized in different physical substrates
  Functional decomposition: complex processes are hierarchies of simpler operations
    →  Cognitive processes are decomposable into more basic operations

Projected Property (P*):
  The mind can be studied independently of the brain (the autonomy of cognitive science from neuroscience).

### Analogy Type Classification

- **Illustrative vs. Argumentative:** Argumentative. The analogy is offered as a reason to adopt a particular research program (classical computationalism) and to reject the reduction of cognitive science to neuroscience.
- **A Priori vs. Empirical:** Empirical. The inference depends on contingent facts about how brains process information and whether the brain genuinely instantiates the same formal properties as a digital computer. Whether the analogy succeeds is an empirical question.
- **Formal vs. Material:** Mixed. The analogy is formal in that it maps abstract functional structures (input-processing-output, decomposition hierarchy) onto each other. It is material in that it claims substantive similarity in causal processing (the brain really does compute).
- **Hesse's Taxonomy:**
  - Positive analogy: input-output structure, hierarchical organization, distinction between structure and function, information processing
  - Negative analogy: digital computers are serial (or at least discrete); brains are massively parallel and analog; computers are designed; brains evolved; transistors vs. neurons (different physical substrates with different computational properties); computers have a clear hardware/software distinction; in brains, structure and function are more entangled
  - Neutral analogy: whether cognitive processes are genuinely algorithmic; whether consciousness can be accounted for computationally

### Relevance Assessment

**Connecting principle identified:** If two systems share the same functional organization, then properties that hold of one system in virtue of that functional organization — including the property of being analyzable at multiple levels of abstraction — also hold of the other.

**Connection type:** Functional/structural. In the source domain (computers), the ability to study software independently of hardware is a consequence of the functional architecture (the hardware implements abstract computational operations that can be specified without reference to the physical substrate). The argument projects this property onto the brain.

**Strength of connecting principle:** The principle is well-established for the class of digital computers. The critical question is whether the brain genuinely shares the relevant functional architecture — specifically, whether it is a computational system of the right kind. The prior association holds in the source but its generalization to the target is contested.

### Disanalogy Detection and Impact Analysis

| Disanalogy | Severity | Impact |
|------------|----------|--------|
| Brains are analog, massively parallel systems; classical computers are digital and (in the original formulation) serial | Defeating (for classical computationalism) | The serial/digital architecture is central to the classical computational model's account of multiple realizability and the hardware/software distinction. If the brain's architecture is fundamentally different — analog, parallel, and continuous rather than digital, serial, and discrete — then the functional isomorphism required for the projection may not obtain. Connectionist models (neural networks) address some of this but at the cost of weakening the original analogy. |
| The brain has no clear hardware/software distinction | Defeating | In computers, the distinction between hardware and software is clear: software is a set of instructions, distinct from the physical machine that executes them. In the brain, "software" (cognitive processes) and "hardware" (neural structures) are far more entangled: learning changes synaptic connections, blurring the line between program and machine. If there is no genuine hardware/software distinction in the brain, the projected property (autonomy of cognitive science) is unsupported. |
| Computers are artifacts designed by intelligent agents; brains are products of evolution | Weakening | Evolution produces systems that are often less modular, less cleanly decomposable, and less elegantly organized than designed systems. The design/evolution difference may explain why the hardware/software distinction does not map cleanly onto the brain. |
| Neurons are not logic gates | Weakening | Neurons have complex, nonlinear dynamics; they are affected by neuromodulators, glial cells, and hormonal states. They do not simply perform logical operations in the way logic gates do. This weakens the claim of functional isomorphism at the lowest level of the mapping. |
| The analogy does not address consciousness (qualia) | Weakening | Even if the brain is computationally analogous to a computer, the analogy does nothing to explain phenomenal consciousness. If the conclusion of the argument (autonomy of cognitive science) is supposed to extend to the study of consciousness, this is a significant gap. If the argument's scope is limited to "mere" cognition (reasoning, memory, language), the gap is less damaging. |

### Counter-Analogy Audit

**Counter-Analogy 1 (The brain as an ecosystem):** The brain is more like an ecosystem — a complex, adaptive, self-organizing system in which the behavior of the whole emerges from nonlinear interactions among components, with no clear distinction between "software" and "hardware." Ecosystem dynamics are not usefully described as algorithmic computation, and the properties of ecosystems cannot be studied independently of their physical constituents.

- *Plausibility:* The ecosystem analogy shares some features with the brain (complexity, nonlinearity, emergence, self-organization) but lacks other features (input-output structure, representational content). It is partially plausible as a corrective to the computer analogy but does not capture everything.
- *Relevance:* It directly challenges the projection: if the brain is more like an ecosystem than a computer, then there is no basis for the autonomy-of-cognitive-science claim.

**Counter-Analogy 2 (The brain as a hydraulic system):** Freud's early model of the mind as a hydraulic system illustrates the danger of analogizing the mind to the dominant technology of the era. The hydraulic analogy was vivid but proved false. The present counter-analogy is genealogical: it suggests that the computer analogy is another instance of the same pattern — mapping the mind onto the era's characteristic technology — and is likely to meet the same fate.

- *Plausibility:* Historically accurate (there is a pattern of modeling the mind on contemporary technology).
- *Relevance:* This is a genealogical debunking argument rather than a direct counter-analogy. It does not show that the computer analogy is false, only that its appeal may be explained by cultural factors rather than genuine fit. It is dialectically weak but worth noting.

### Argumentative Force Assessment

**Grade: Weak (or Moderate, depending on formulation).** The analogy was Strong when first proposed (1960s–1970s) because it captured real and important functional similarities between brains and computers and opened a productive research program. However, subsequent developments in both computer science (connectionism, dynamical systems theory) and neuroscience (the complexity and non-modularity of neural processing) have revealed substantial disanalogies that weaken the original mapping. The hardware/software distinction — the lynchpin of the projected property — has no clear neural analogue, which means the prior-association condition, while satisfied in the source, fails to generalize. The analogy retains considerable heuristic value (it guides research questions in cognitive science) but its argumentative force — its ability to establish the autonomy of cognitive science from neuroscience as a matter of principle — is weak. A more cautious, connectionist, or dynamical-systems formulation of the analogy may fare better but at the cost of weakening the projected conclusion.

### Fallacy Cross-Reference

The analogy does not commit a fallacy when understood as a research heuristic. However, when deployed as an argument for the principled autonomy of cognitive science from neuroscience — without acknowledging the hardware/software disanalogy — it may commit the **fallacy of suppressed disanalogy**. The proponent who omits the fact that there is no clear neural analogue of the hardware/software distinction is suppressing a crucial disanalogy.

### Dialectical Impact and Recommendations

**For the proponent:** The analogy can be salvaged by qualifying the conclusion — arguing not for the principled autonomy of cognitive science but for the pragmatic utility of computational models in understanding cognition. The computational theory of mind need not depend on a strong isomorphism between brains and digital computers; it can be defended on the grounds that computational descriptions capture real patterns in cognitive processing, even if the implementation is not computer-like. The proponent should also engage with connectionist and dynamical-systems alternatives, showing where classical computational models outperform them.

**For the respondent:** The most efficient line of attack is the hardware/software disanalogy: point out that the brain does not exhibit the clean separation between program and machine that licenses the projected property. The respondent can also deploy the genealogical counter-analogy (brain as ecosystem, Freud's hydraulic model) to suggest that the computer analogy is driven by cultural availability rather than genuine fit. The respondent should acknowledge the analogy's heuristic value to avoid appearing dismissive of an entire research tradition.
```

---

## Example 5: A Merely Rhetorical Analogy

### Input

> The state is like a family. In a family, parents set rules for children, and children obey because they trust their parents' superior wisdom and goodwill. Children who disobey are disciplined — not out of malice, but out of love, to guide them toward better behavior. Just so, the state sets laws for its citizens, who should obey out of trust in their leaders' wisdom. Disobedience, like a child's tantrum, should be met with firm correction. Therefore, citizens have a moral obligation to obey all laws, even those they disagree with, and the state has a corresponding right to punish disobedience without being subject to democratic constraint.

This argument — a composite paternalistic analogy — maps the family onto the state and projects the authority relations of the family onto political authority.

### Output

```
## Analogy Analysis Report

### Analogy Summary

The argument maps the parent–child relationship onto the state–citizen relationship, inferring from the legitimate authority of parents over children to the legitimate authority of the state over citizens. The projected claim is that citizens have a blanket moral obligation to obey the law, grounded in the same kind of trust-based authority that children owe their parents, and that the state's right to punish is similarly grounded.

### Source–Target Mapping Table

Object/Entity Mappings:
  Parents                   →  The state / government / leaders
  Children                  →  Citizens
  Family                    →  Political community

Attribute/Property Mappings:
  Parents have superior wisdom → Leaders have superior wisdom
  Parents act from goodwill    → Leaders act from goodwill
  Children are immature        → Citizens are (implicitly) immature

First-Order Relational Mappings (R1):
  Parents set rules → children obey from trust
    →  State sets laws → citizens obey from trust
  Parents discipline disobedient children → state punishes disobedient citizens

Higher-Order Relational Mappings (R2):
  Authority relations in the family justify obedience → Authority relations in the state justify obedience.

Projected Property (P*):
  Citizens have a moral obligation to obey all laws, and the state has an unrestricted right to punish disobedience.

### Analogy Type Classification

- **Illustrative vs. Argumentative:** Argumentative (the analogy is presented as a reason for the conclusion).
- **A Priori vs. Empirical:** Empirical (the claimed similarities — that leaders have superior wisdom and goodwill — are empirical claims that may be false).
- **Formal vs. Material:** Material (the analogy claims substantive similarity of authority relations and psychological attitudes).
- **Hesse's Taxonomy:**
  - Positive analogy: both involve hierarchical authority relationships, rule-setting, and sanctions for noncompliance
  - Negative analogy: parents and children have a biological and nurturing relationship; states and citizens do not; children eventually mature into adults; citizens do not "mature out of" citizenship; parents know their children individually; states govern millions of strangers; families are small, intimate, and based on love; states are large, impersonal, and based on coercion; parents do not demand obedience to arbitrary rules; states may
  - Neutral analogy: (the negative analogy is so extensive that the neutral analogy is not the relevant category)

### Relevance Assessment

**Connecting principle attempted:** Hierarchical authority relationships grounded in superior wisdom and goodwill generate a moral obligation of obedience, regardless of the specific features of the relationship.

**Assessment of connection:** The prior-association condition is satisfied in the source (within functional families, children do have pro tanto obligations to obey their parents, grounded in the parents' superior knowledge and the children's dependence), but the generalization to the target fails catastrophically. The connecting principle is far too broad — it would justify any hierarchical relationship, no matter how oppressive, provided the superior party claims superior wisdom. Moreover, the features that ground parental authority in the source — intimacy, biological connection, the child's developmental immaturity, the parent's individualized knowledge of the child — are precisely the features absent from the state–citizen relationship. The analogy selects a thin structural similarity (hierarchy) while ignoring the features that actually ground the authority in the source.

### Disanalogy Detection and Impact Analysis

| Disanalogy | Severity | Impact |
|------------|----------|--------|
| Parents have a nurturing, biological relationship with their children; the state does not with citizens | Defeating | Parental authority is grounded partly in the intimate, caring, individualized relationship between parent and child. The state–citizen relationship lacks this grounding, so the inference from "parents have authority" to "the state has authority" is unsupported. |
| Children are developmentally immature and dependent; citizens are (presumptively) competent adults | Defeating | Parental authority is justified by the child's immaturity and incapacity for autonomous decision-making. Citizens are adults capable of reasoning about laws and policies. To treat citizens as children is to deny their moral and political autonomy — the very thing the argument is supposed to justify. |
| Families are small and intimate; states are large and impersonal | Defeating | The scale and anonymity of political society mean that leaders cannot have the kind of individualized knowledge of citizens that parents have of children. The epistemic basis for authority in the source does not transfer to the target. |
| Parents act from love and goodwill (in functional families); states often act from self-interest or ideology | Defeating | Even if states occasionally act from goodwill, this is not a structural feature of political power in the way that parental love is a structural feature of functional families. The analogy assumes away the defining problem of political philosophy (the abuse of power). |
| Adults can leave their family of origin; citizens cannot easily leave their state | Weakening | The asymmetry of exit options means that the analogy's presumption of a voluntary relationship is false in the political case. |

### Counter-Analogy Audit

**Counter-Analogy (The state as a protection racket):** The state is like a mafia protection racket. It demands payment (taxes) in exchange for protection (police, military), and it punishes those who refuse to pay. The mafia might claim to act in the "family's" interest, but the claim is a thin rationalization for extortion. The state differs from the mafia only in scale and in the legitimacy it claims — not in the structure of its demands. If the state is more like a protection racket than a family, then obedience is not morally obligatory but prudentially advisable under threat of force.

- *Plausibility:* A deliberately provocative counter-analogy, but it shares structural features (hierarchical authority, demand for compliance, punishment for noncompliance) with both the family analogy and the state. The point is that the structural features are too thin to support any normative conclusion — they are equally compatible with legitimate and illegitimate authority.
- *Relevance:* It demonstrates that the original analogy's structural features do not uniquely support the conclusion.
- *Dialectical burden:* The original proponent must explain what distinguishes the family analogy from the protection-racket analogy in a principled, non-ad-hoc way.

### Argumentative Force Assessment

**Grade: Merely Rhetorical.** The analogy has no genuine argumentative force. It maps a thin structural similarity (hierarchy, rule-setting, sanctions) while ignoring all the features that actually ground parental authority in the source domain. The projected property (blanket moral obligation to obey the state) is nowhere near supported by the analogy. The disanalogies are not merely numerous — they are defeating, because they sever the connection between the shared properties (hierarchical authority) and the projected property (moral obligation to obey). The analogy functions as political rhetoric — it exploits the warm, positive associations of the family to lend an unearned legitimacy to state authority — but it does not provide a rational basis for the conclusion. Stripping away the emotional resonance of the family metaphor leaves no inferential support for the conclusion whatsoever.

### Fallacy Cross-Reference

The argument commits the **fallacy of false analogy** under the subcategory of **faulty comparison**: it asserts a similarity (in the grounding of authority) that does not in fact obtain between family and state. It also commits the **fallacy of suppressed disanalogy**: the numerous, patent differences between family and state — adult autonomy, scale, intimacy, voluntariness — are not acknowledged or addressed. The argument may additionally commit the **fallacy of misleading vividness**: the warm, familiar image of the family is used to obscure the weakness of the inferential link.

### Dialectical Impact and Recommendations

**For the proponent:** The analogy cannot be repaired. The family and the state differ in too many respects that are directly relevant to the grounding of authority. The proponent should abandon the analogy and argue for political obligation on independent grounds (e.g., consent, fair play, natural duty). If the proponent wishes to retain the analogy for purely illustrative purposes — to help readers visualize the idea of benevolent authority — they should explicitly disclaim any argumentative force and present it as a metaphor, not an argument.

**For the respondent:** The respondent can dismiss the analogy with a brief explanation of the defeating disanalogies. The most efficient response is to point out the central fallacy: that the analogy treats citizens as children, thereby denying the very moral autonomy that any theory of political obligation must respect. The respondent need not engage extensively with the analogy; pointing to the adult/child disanalogy is sufficient. The respondent can also deploy the protection-racket counter-analogy to illustrate the emptiness of the structural mapping.
```
