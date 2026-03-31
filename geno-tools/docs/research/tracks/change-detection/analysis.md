# Change Detection — Comprehensive Analysis

#attention #change-detection #analysis

## Overview

Change detection is the **least explored** attention sub-area for LLMs. While selective attention has NIAH and GSM-IC, sustained attention has vigilance/monitoring tasks, and divided attention has multi-task benchmarks, change detection has **no dedicated benchmark**. This is a major gap — and a major opportunity.

Change blindness is one of the most robust and dramatic findings in human attention research. People routinely fail to notice enormous changes in visual scenes — a person swapping identity mid-conversation, a gorilla walking through a basketball game, the color of a wall changing during a camera cut. The phenomenon reveals that our perception of the world is far less detailed than we assume: we do not maintain a rich, point-by-point representation of our environment, but instead rely on sparse, attention-gated sampling.

The question for LLMs is whether an analogous limitation exists. Models process text sequentially and maintain representations in context windows. When disruptive, unrelated text is inserted between two versions of a passage, does the model's representation of the first version degrade? Can it still detect changes? And critically: does the magnitude of the change interact with the amount of disruption in the same way it does for humans?

No one has asked these questions systematically. We aim to be the first.

---

## Adjacent Work

| Benchmark / Study | What It Tests | Why It's Not Change Detection |
|---|---|---|
| **NIAH (Needle in a Haystack)** | Retrieval of a planted fact from a long context | Tests recall, not comparison between two versions. No disruption manipulation. |
| **GSM-IC (Shi et al., 2023)** | Math problem solving with irrelevant context | Tests filtering of distractors during reasoning, not detection of changes across passages. |
| **Hallucination benchmarks** (HaluEval, TruthfulQA, FaithDial) | Whether models generate false information | Tests generation fidelity, not perceptual comparison. Model produces content rather than detecting differences. |
| **Perturbation studies** (TextFooler, BERT-Attack, adversarial NLI) | Robustness to input modifications | Tests whether model output changes when input is perturbed — opposite direction from our task (we test whether model *notices* the perturbation). |
| **RECALL (Liu et al., 2023)** | Long-context recall across positions | Tests whether models can retrieve information at various positions. Adjacent to disruption effects but no comparison task. |
| **ConFactCheck / FactCC** | Factual consistency between summary and source | Closest in spirit — comparing two texts for consistency — but focused on summarization fidelity, not controlled change detection with disruption manipulation. |
| **HalluLens** | Hallucination detection across domains | Tests detection of fabricated content, not detection of changes between two provided versions. |
| **LongBench / L-Eval** | Long-context understanding | General long-context benchmarks that include some comparison tasks but do not isolate change detection or manipulate disruption systematically. |
| **SummEdits (Laban et al., 2023)** | Detecting factual inconsistencies in edited summaries | Asks whether a summary is consistent with a document after editing. Related but no disruption manipulation, no magnitude control, no false-alarm measurement. |

**Key takeaway:** Several benchmarks touch on related capabilities (comparison, consistency checking, long-context recall), but none isolate the change detection phenomenon with controlled disruption and magnitude manipulations. The gap is clear and well-defined.

---

## Unadapted Cognitive Paradigms

These are established paradigms from human change blindness research that have not been adapted for LLM evaluation.

### 1. Flicker Paradigm (Rensink et al., 1997)
- **Human version:** Alternate between image A and image A' with a brief blank screen between them. Observers take surprisingly long to find the change.
- **Our adaptation:** Present passage A, then disruptor paragraph(s), then passage A' with one factual change. This is the core of our `change_blindness` task.
- **Status:** Adapted in our benchmark.

### 2. Mudsplash Paradigm (O'Regan et al., 1999)
- **Human version:** A change occurs simultaneously with "mudsplashes" — salient but irrelevant visual transients that capture attention away from the change location.
- **LLM analogue:** Present passage A and passage A' in sequence (no gap), but add salient, attention-grabbing content *within* the passage at locations away from the change. For example, insert a shocking statistic or emotionally charged sentence elsewhere in the text.
- **Status:** Untested. This would probe whether LLMs have "attentional capture" — whether salient content in one part of the text reduces detection of changes in another part.
- **Prediction:** Models may show reduced change detection when mudsplash content is present, especially if the mudsplash is topically related to the passage (creating interference).

### 3. Gradual Change
- **Human version:** Slowly alter an image over many seconds. Observers fail to notice even very large cumulative changes.
- **LLM analogue:** Present a long document where a fact gradually drifts across paragraphs. In paragraph 1, the population of a city is 2.3 million. In paragraph 5, it's mentioned as 2.4 million. In paragraph 12, it's 2.8 million. In paragraph 20, it's 3.5 million. Ask the model to verify consistency.
- **Status:** Untested. This would test whether models track factual consistency across a document or only compare adjacent mentions.
- **Prediction:** Models will catch large jumps but miss gradual drift, especially in longer documents.

### 4. Inattentional Blindness (Simons & Chabris, 1999)
- **Human version:** While performing a demanding primary task (counting basketball passes), observers fail to notice an unexpected event (gorilla walking through the scene).
- **LLM analogue:** Give the model a demanding primary task (e.g., "count all instances of the word 'the' in this passage and also summarize the main argument") while embedding an unexpected, conspicuous anomaly in the text (e.g., a sentence in a foreign language, a passage about an entirely different topic, an obviously false claim).
- **Status:** Untested. This would test whether task focus creates blind spots.
- **Prediction:** Models under heavy task load may miss anomalies that they would easily catch if asked to look for them.

### 5. Metacognitive Prediction of Change Blindness
- **Human version:** Ask people to predict whether they would notice changes. People dramatically overestimate their change detection ability.
- **LLM analogue:** Before presenting the change detection task, ask the model: "If I showed you two versions of a passage separated by unrelated text, and one detail was changed, how confident are you that you would detect it?" Then actually test it.
- **Status:** Untested. This would probe metacognitive calibration — a cross-cutting theme with the Metacognition track.
- **Prediction:** Models will express high confidence but show imperfect detection, especially for minor changes with high disruption. The gap between predicted and actual performance is itself a metric.

---

## Gap Analysis: Why Has No One Done This?

Several factors explain why change detection remains untested in LLMs:

1. **Visual origins.** Change blindness is traditionally a visual phenomenon. Researchers studying LLMs may not think to adapt visual attention paradigms to text. The conceptual bridge requires cross-disciplinary thinking.

2. **Assumption of perfect memory.** There is a widespread (and partially correct) assumption that LLMs have "perfect memory" within their context window — they can attend to any token. This leads people to assume change detection would be trivial. But attention mechanisms are not uniform, and the effective representation of earlier content may degrade as the context grows.

3. **Focus on generation, not perception.** Most LLM benchmarks test *output quality* (can the model produce good text, answer questions, solve problems). Change detection is a *perceptual* task — it tests what the model notices, not what it generates. This is a less common evaluation paradigm.

4. **No obvious practical application.** Benchmarks often follow applications: summarization, QA, coding, math. "Can the model spot a changed detail after reading unrelated text?" doesn't map to an obvious product use case — but it maps directly to a cognitive capability that matters for reliability and trustworthiness.

5. **Difficulty of principled design.** A good change detection benchmark requires careful control of many variables: passage content, change location, change magnitude, disruptor content, disruptor length, and control conditions. This is more complex than many benchmark designs and requires experimental psychology expertise.

---

## Our Approach: The change_blindness Task

### Design Rationale

We adapted the flicker paradigm because it is:
- The most well-established change blindness paradigm
- Naturally translatable to text (passage → disruption → modified passage)
- Allows clean manipulation of two key variables: change magnitude and disruption level
- Includes control conditions for measuring false alarms

### Structure

**5 base passages** spanning diverse domains (solar energy, marine biology, archaeology, neuroscience, climate science). Domain diversity prevents any single knowledge bias from dominating results.

**2 change types per passage:**
- Minor: peripheral numerical or name change (e.g., a capacity figure, a researcher's name)
- Major: central causal claim reversal (e.g., the mechanism that explains the main finding)

**3 disruption levels:**
- 0 disruptors: direct comparison (baseline)
- 1 disruptor: moderate interference (~150 words of unrelated text)
- 3 disruptors: heavy interference (~450 words of unrelated text)

**Control conditions:** 3 per passage (one per disruption level) where Version A and Version B are identical. The model should respond "NO CHANGE." This measures false alarm rate — the tendency to report changes that don't exist, which increases signal-to-noise ratio and guards against models that always report a change.

**Total items:** 5 passages × (2 changes × 3 disruption levels + 3 controls) = 45

### Scoring

Binary correct/incorrect per item. For change items, the model must identify the specific change (mentioning both old and new values). For control items, the model must indicate no change was found. This prevents gaming through vague answers.

### Why This Design Has Discriminatory Power

The 2×3 factorial design (magnitude × disruption) creates a gradient:
- Easy: major change, 0 disruptors (most models should succeed)
- Medium: minor change with 0 disruptors, or major change with 3 disruptors
- Hard: minor change, 3 disruptors (tests the limit of attentional maintenance)

We expect frontier models to show a smooth degradation curve, mid-tier models to show a sharp cliff, and weaker models to fail even at moderate difficulty. The interaction pattern — how much disruption amplifies the magnitude effect — is the most diagnostic signal.

---

## Novel Ideas for Future Work

### Mudsplash Analogue
Insert attention-grabbing sentences (surprising statistics, emotional content, controversial claims) at locations *away from* the change site. Test whether these "mudsplashes" reduce change detection. This would probe whether LLMs have a form of attentional capture — whether salient content in one region reduces processing of content in another region.

**Design sketch:** Same 5 passages, but add 2 conditions: mudsplash-present and mudsplash-absent. The mudsplash is a single eye-catching sentence inserted in a paragraph far from the change. Compare detection rates.

### Gradual Fact Drift
Present a long document (~3000 words) where a specific fact gradually changes value across mentions. The first mention states X=100, subsequent mentions slowly drift to X=150. Ask the model to verify factual consistency.

**Why it matters:** This tests whether models track consistency across a document or only process each mention independently. Relevant to document editing, legal review, and scientific writing assistance.

### Attention-Manipulation Version
Before presenting the change detection task, give the model an instruction that focuses its attention on a specific aspect of the passage: "Pay close attention to the numerical figures" or "Focus on the causal relationships." Then test whether this instruction improves detection of changes to the targeted aspect and *reduces* detection of changes to the non-targeted aspect.

**Why it matters:** This would directly test whether LLM "attention" can be directed in the same way human attention can — and whether directed attention comes with the same cost (reduced detection of unattended changes).

### Metacognitive Change Blindness
Ask the model to predict its own change detection performance before testing it. Compare predicted vs. actual performance across conditions.

**Why it matters:** Overconfidence in change detection is one of the most robust metacognitive failures in humans. If LLMs show the same pattern (high predicted accuracy, lower actual accuracy, especially for minor changes), it reveals a metacognitive blind spot with practical implications for reliability.

### Multi-Change Detection
Present passages with 0, 1, 2, or 3 changes. Test whether finding one change causes "satisfaction of search" — stopping the search after finding the first change and missing subsequent ones. This is a well-known phenomenon in radiology (finding one lesion reduces detection of additional lesions).

---

## Cross-Cutting Themes

### Change Detection × Selective Attention
Selective attention tasks test filtering of irrelevant information. Change detection tests maintenance of a detailed representation across disruption. The interaction is clear: a model with strong selective attention might better encode the *relevant* details of Version A, making them more robust to disruption. Testing both in the same benchmark allows us to see whether these are independent capabilities or facets of the same underlying mechanism.

### Change Detection × Sustained Attention
Sustained attention (vigilance) tests performance maintenance over time/repetition. If we present many change detection items in sequence, does performance degrade on later items? This would be a vigilance decrement in change detection — a compound effect that tests two attention sub-areas simultaneously.

### Change Detection × Metacognition
The metacognitive change blindness paradigm described above bridges the Attention and Metacognition tracks. Models that are well-calibrated about their change detection limitations are more trustworthy than models that are confident but wrong.

### Change Detection × Context Window Architecture
Change detection performance may vary systematically with architecture. Models with different attention mechanisms (dense vs. sparse, local vs. global, sliding window vs. full) may show different disruption sensitivity curves. This could provide architectural insights — which attention designs best support change detection?

---

## Key Papers

- **Rensink, R. A., O'Regan, J. K., & Clark, J. J. (1997).** To see or not to see: The need for attention to perceive changes in scenes. *Psychological Science, 8*(5), 368-373. — The foundational flicker paradigm paper.

- **O'Regan, J. K., Rensink, R. A., & Clark, J. J. (1999).** Change-blindness as a result of 'mudsplashes'. *Nature, 398*, 34. — Introduced the mudsplash paradigm showing that attentional capture by transients prevents change detection.

- **Simons, D. J., & Chabris, C. F. (1999).** Gorillas in our midst: Sustained inattentional blindness for dynamic events. *Perception, 28*(9), 1059-1074. — The invisible gorilla study demonstrating inattentional blindness.

- **Simons, D. J., & Levin, D. T. (1998).** Failure to detect changes to people during a real-world interaction. *Psychonomic Bulletin & Review, 5*(4), 644-649. — Real-world change blindness during face-to-face conversation.

- **Simons, D. J., & Rensink, R. A. (2005).** Change blindness: Past, present, and future. *Trends in Cognitive Sciences, 9*(1), 16-20. — Comprehensive review of change blindness research.

- **Levin, D. T., Momen, N., Drivdahl, S. B., & Simons, D. J. (2000).** Change blindness blindness: The metacognitive error of overestimating change-detection ability. *Visual Cognition, 7*(1-3), 397-412. — People overestimate their own change detection ability.

- **Shi, F., Chen, X., Misra, K., Scales, N., Dohan, D., Chi, E., Schärli, N., & Zhou, D. (2023).** Large language models can be easily distracted by irrelevant context. *ICML 2023*. — GSM-IC benchmark showing LLMs are susceptible to irrelevant context in math problems.

- **Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024).** Lost in the middle: How language models use long contexts. *TACL*. — Positional biases in long-context processing, relevant to disruption effects.

- **Kamradt, G. (2023).** Needle in a haystack — pressure testing LLMs. — The NIAH evaluation framework for long-context retrieval.

- **Laban, P., Kryściński, W., Aber, D., & Xiong, C. (2023).** SummEdits: Measuring LLM ability at factual reasoning through the lens of summarization. *EMNLP 2023*. — Closest existing benchmark to change detection, testing whether models can identify factual inconsistencies in edited summaries.

---

## Changelog

- 2026-03-29: Initial analysis from full research sweep
