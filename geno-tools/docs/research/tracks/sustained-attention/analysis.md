# Sustained Attention: Comprehensive Analysis

#attention #sustained-attention #analysis

## Overview

Sustained attention — the ability to maintain focus on a task over an extended period — is one of the most fundamental cognitive capacities. In human psychology, vigilance research dates back to Mackworth's (1948) studies of radar operators in WWII, where he documented the now-classic "vigilance decrement": a reliable decline in target detection over 30+ minutes of monotonous monitoring.

For LLMs, sustained attention maps to a different but analogous question: when a model must process many repeated sub-tasks within a single prompt, does its performance degrade as a function of the number of items processed? Unlike humans, LLMs do not experience fatigue or arousal fluctuations, but they do have architectural constraints — finite context windows, positional encoding limitations, and attention mechanisms that may distribute capacity unevenly across long sequences.

This analysis surveys existing work on LLM performance degradation over long contexts, identifies gaps in current benchmarking, catalogues unadapted cognitive paradigms from human sustained attention research, describes our vigilance_decrement task design, and proposes novel benchmark ideas for future development.

---

## Existing Work

### Summary Table

| Benchmark / Paper | Year | What It Tests | Key Finding | Limitation for Sustained Attention |
|---|---|---|---|---|
| Needle in a Haystack (NIAH) | 2023 | Single fact retrieval from long context | Performance varies by position and depth | Single retrieval, not sustained processing |
| Lost in the Middle | 2024 | Multi-document QA with varying gold position | U-shaped accuracy curve (primacy + recency) | Confounds position with attention; single query |
| RULER | 2024 | Long-context capability across 13 tasks | Effective context << claimed context for most models | Focused on retrieval, not repeated processing |
| BABILong | 2024 | Reasoning over long documents | Performance degrades with document length | Reasoning confound; not isolated attention |
| S-NIAH / Multi-NIAH | 2024 | Multiple needle retrieval | Performance drops with more needles | Closer to divided attention than sustained |
| GSM-Infinity | 2025 | Math with irrelevant context padding | Math accuracy drops with context length | Selective attention (filtering), not sustained |
| Context Rot | 2025 | Universal degradation analysis | Three mechanisms: positional, dilution, distraction | Comprehensive but not task-repetition focused |
| Multi-Instance Processing | 2026 | Batch processing of identical tasks | Instance count matters more than context length | Closest to vigilance; limited task variety |
| Intelligence Degradation | 2025 | IQ-test performance vs. context length | Measured IQ drops with longer contexts | Confounds task difficulty with context effects |

### Detailed Notes

#### Needle in a Haystack (NIAH)
- **Origin:** Greg Kamradt (2023), popularized as a simple long-context stress test
- **Method:** Hide a single fact ("needle") in a long document ("haystack"), query for it
- **Relevance:** Established that position within context affects retrieval, but tests a single retrieval event — no sustained processing component

#### Lost in the Middle
- **Citation:** Liu et al. (2024). "Lost in the Middle: How Language Models Use Long Contexts." arXiv:2307.03172
- **Method:** Multi-document QA where the gold document is placed at varying positions (1st, 5th, 10th, 15th, 20th)
- **Key finding:** U-shaped performance — best when gold doc is first or last, worst in the middle. GPT-3.5-turbo showed 30%+ accuracy drops for middle positions.
- **Relevance to sustained attention:** Demonstrates positional bias but confounds it with attention. The model only answers one question — it does not sustain processing across the full context.

#### RULER
- **Citation:** Hsieh et al. (2024). "RULER: What's the Real Context Size of Your Long-Context Language Models?" arXiv:2404.06654
- **Method:** 13 tasks across 4 categories (retrieval, multi-hop, aggregation, QA) at context lengths from 4K to 128K
- **Key finding:** Most models' effective context is far shorter than claimed. Llama-3-8B-80K drops to near-random at 32K despite 80K claimed context.
- **Relevance:** Shows context length degrades performance, but tasks are single-query; doesn't test repeated identical processing.

#### BABILong
- **Citation:** Kuratov et al. (2024). "BABILong: Testing the Limits of LLMs in Long Document Understanding." arXiv:2406.10149
- **Method:** Embeds bAbI reasoning tasks in long natural-language documents (up to 1M tokens)
- **Key finding:** Even RAG-augmented models struggle beyond 32K context; only specialized architectures (Mamba, RWKV) maintain performance
- **Relevance:** Tests reasoning-in-context but confounds reasoning difficulty with attention demands

#### Context Rot
- **Citation:** Qiu et al. (2025). "Context Rot: How Long Contexts Degrade LLM Performance." arXiv:2502.XXXXX
- **Method:** Systematic evaluation across 18 frontier models on multiple tasks with controlled context expansion
- **Key findings:** Identified three degradation mechanisms:
  1. **Positional degradation** — performance varies by where information sits
  2. **Dilution** — relevant signal gets "diluted" by surrounding irrelevant content
  3. **Distraction** — irrelevant content actively interferes with reasoning
- **Relevance:** Most comprehensive degradation taxonomy, but focused on single-query tasks with varying context, not repeated task processing

#### Multi-Instance Processing
- **Citation:** Chen et al. (2026). "How Well Can LLMs Process Multiple Instances?" arXiv:2603.22608
- **Method:** Models process batches of 1-200 identical task instances in a single prompt. Tasks include sentiment analysis, NER, text classification.
- **Key findings:**
  - Performance degrades with instance count, even when context length is held constant
  - Instance count is a stronger predictor of degradation than total token count
  - Collapse is sudden rather than gradual for some models (cliff effect at ~100 instances)
  - Position effects: U-shaped for some tasks, linear decline for others
- **Relevance:** This is the closest existing work to our vigilance_decrement benchmark. However, it uses NLP tasks (sentiment, NER) rather than trivially easy cognitive tasks, and does not include oddball/surprise detection.

#### GSM-Infinity
- **Citation:** Zhang et al. (2025). "GSM-Infinity: How Do Your LLMs Deal with Novel and Dynamic Benchmarks?" arXiv:2502.XXXXX
- **Method:** GSM8K-style math problems with irrelevant context padding inserted between reasoning steps
- **Key finding:** Math accuracy drops significantly with padding, even when the math itself is unchanged
- **Relevance:** Tests selective attention (filtering noise) more than sustained attention, but demonstrates that irrelevant context degrades processing

#### Intelligence Degradation
- **Citation:** Du et al. (2025). "Intelligence Degradation: Exploring the Impact of Context Window Extension." arXiv:2503.XXXXX
- **Method:** IQ-test items administered at varying context lengths
- **Key finding:** Effective IQ drops measurably as context grows
- **Relevance:** Provocative framing but confounds multiple factors; not focused on sustained task repetition

---

## Unadapted Cognitive Paradigms

Human sustained attention research has developed several well-validated paradigms over 75+ years. None have been directly adapted for LLM evaluation.

### Continuous Performance Test (CPT)
- **Original:** Rosvold et al. (1956)
- **Procedure:** Participant views a stream of stimuli (letters, numbers, shapes) and responds to infrequent targets (e.g., press button when you see "X" after "A")
- **Measures:** Hit rate, false alarm rate, reaction time, d' (sensitivity), beta (criterion)
- **LLM adaptation:** Present a long sequence of items, ask the model to flag specific targets. Measure detection accuracy as a function of position in the sequence.
- **Challenge:** LLMs process the entire sequence at once (no temporal unfolding), so "time on task" must be operationalized as position in the sequence.

### Sustained Attention to Response Task (SART)
- **Original:** Robertson et al. (1997)
- **Procedure:** Respond to every stimulus EXCEPT rare targets (e.g., press for all digits except "3"). Tests inhibitory control after developing automatic responding.
- **Measures:** Commission errors (responding to no-go targets), omission errors
- **LLM adaptation:** Present 100 items, ask the model to process all of them except items matching a specific rule. Measure whether the model "automatically" processes the exception items instead of withholding.
- **Challenge:** The go/no-go distinction maps awkwardly to text generation. Could be adapted as "answer all questions except those about [topic]."

### Mackworth Clock Task
- **Original:** Mackworth (1948)
- **Procedure:** Watch a clock hand that moves in regular increments; detect rare double-jumps
- **Measures:** Detection rate over time, false alarms
- **LLM adaptation:** Present a long sequence of numbers or events with regular patterns; embed rare anomalies. Ask the model to identify all anomalies.
- **Relevance:** Directly tests vigilance in a signal-detection framework.

### Signal Detection Theory (SDT) Analysis
- **Framework:** Green & Swets (1966)
- **Application:** Decompose performance into:
  - **d' (sensitivity)** — ability to discriminate signal from noise, independent of response bias
  - **beta (criterion)** — tendency toward liberal or conservative responding
- **For LLMs:** If we include both target-present and target-absent trials, we can compute d' and beta at each position in the sequence, revealing whether degradation is due to reduced sensitivity or criterion shift.

---

## Gap Analysis

| Gap | Description | Addressed By |
|---|---|---|
| No direct vigilance test | No benchmark presents 50-200 identical sub-tasks and measures positional accuracy | Our vigilance_decrement task |
| Confounded position effects | Existing work confounds position, context length, and task difficulty | Multi-Instance Processing partially addresses; our task uses trivially easy sub-tasks |
| No oddball/surprise detection | No benchmark tests whether models notice unexpected items amid routine processing | Our oddball variant |
| No SDT decomposition | No work decomposes LLM degradation into sensitivity vs. criterion components | Proposed LLM-CPT benchmark |
| No monotony manipulation | No benchmark varies task monotony independent of difficulty | Proposed monotony x difficulty factorial |
| No adaptive measurement | No benchmark finds the exact capacity threshold per model | Proposed adaptive staircase |
| No error taxonomy | Degradation studies report accuracy but not error types (drift, skip, copy, format) | Our per-position error analysis |

---

## Our Approach: The Vigilance Decrement Task

### Design Rationale

The core insight is that sustained attention in LLMs should be tested with tasks that are trivially easy in isolation, so that any performance degradation can be attributed to the sustained processing demand rather than intrinsic task difficulty. We chose three task types that frontier models solve at near-100% accuracy when presented individually:

1. **Country identification** — given a sentence mentioning a city, name the country
2. **Number extraction** — extract the number from a templated sentence
3. **Misspelling detection** — identify the misspelled word in a sentence

### Structure

Each item contains 100 sub-tasks presented sequentially in a single prompt, with the instruction to answer all 100 in numbered format. The model receives:

```
You will be given 100 tasks. Answer each one on a separate line, numbered 1-100.

1. In which country is the city of Lyon? → [answer]
2. In which country is the city of Tokyo? → [answer]
...
100. In which country is the city of Nairobi? → [answer]
```

### Variants

- **Normal (3 items):** All 100 sub-tasks are the same type
- **Oddball (3 items):** 99 sub-tasks are the same type, but one (at a random position between 40-70) is a different type. The prompt includes a note: "Note: the task type may change for some items."

### Scoring

Responses are parsed by matching `N. answer` or `N: answer` patterns. Each answer is scored with flexible matching:
- Case-insensitive comparison
- Substring matching (e.g., "France" matches "The answer is France")
- Number normalization (e.g., "42" matches "forty-two")

### Metrics

Primary:
- **Accuracy by decile** — accuracy for positions 1-10, 11-20, ..., 91-100
- **Decay onset** — first decile where accuracy drops below 95%
- **Total accuracy** — overall proportion correct

Secondary:
- **Oddball detection rate** — accuracy on the oddball item specifically
- **Error type distribution** — categorization of errors (wrong answer, skipped, format error, adjacent copy)
- **Recovery after oddball** — does accuracy change in positions after the oddball?

### How It Addresses Gaps

- **Direct vigilance test:** 100 identical sub-tasks, measuring position-dependent accuracy
- **Controlled difficulty:** Tasks are trivially easy, isolating sustained processing demand
- **Oddball detection:** Tests whether automated processing causes models to miss unexpected stimuli
- **Error taxonomy:** Per-position scoring enables detailed error analysis
- **Confound management:** Instance count is the primary variable; context length is a secondary effect

---

## Novel Benchmark Ideas

### 1. LLM Continuous Performance Test (LLM-CPT)

**Concept:** Adapt the human CPT for LLMs. Present a sequence of 500+ stimuli (words, numbers, short phrases). The model must:
- Respond "YES" to target stimuli (e.g., any animal name)
- Respond "NO" to all others

**Measurement:** Hit rate, false alarm rate, d', and beta computed in sliding windows of 50 stimuli. This enables SDT decomposition of degradation — is the model becoming less sensitive (lower d') or more conservative/liberal (shifting beta)?

**Advantage over current task:** Enables signal detection analysis; includes both signal-present and signal-absent trials.

**Difficulty:** Requires very long output generation; some models may truncate.

### 2. SART Analog (Inhibitory Sustained Attention)

**Concept:** Present 200 items where the model must perform a simple operation (e.g., "add 1 to the number"). For 10% of items, a specific cue indicates the model should NOT perform the operation but instead output "SKIP."

**Measurement:** Commission errors (performing the operation when it should skip) as a function of position. Early positions should have high accuracy; later positions may show automatic responding that overrides the inhibition rule.

**Advantage:** Tests inhibitory control within sustained attention, a distinct cognitive component.

### 3. Monotony x Difficulty Factorial Design

**Concept:** 2x2 design crossing:
- **Monotony:** All 100 sub-tasks identical type vs. 10 different types cycling
- **Difficulty:** Trivially easy vs. moderately challenging sub-tasks

**Measurement:** Compare degradation slopes across conditions. If monotonous+easy shows the steepest decline, underload theory applies. If hard+monotonous shows steepest decline, overload theory applies.

**Advantage:** Adjudicates between competing theoretical accounts of LLM "vigilance decrement."

### 4. Rare Critical Signals

**Concept:** 200 routine sub-tasks with 3-5 "critical" items that require a different response. Critical items are signaled by a subtle cue (e.g., the sentence is in a slightly different format). Base rate: 2% critical items.

**Measurement:** Critical item detection rate as a function of position and number of preceding routine items. Analogous to rare-event detection in human vigilance (e.g., TSA screening, medical image reading).

**Advantage:** Tests real-world-relevant sustained attention failure mode — missing rare important events during routine processing.

### 5. Adaptive Staircase for Vigilance Capacity

**Concept:** Start with 10 sub-tasks, increase by 10 per trial, measuring accuracy at each level. Find the "vigilance threshold" — the number of sub-tasks at which accuracy drops below 90% for each model.

**Measurement:** Threshold instance count per model, enabling a single-number vigilance capacity metric.

**Advantage:** Efficient characterization of model-specific limits; creates a clear ranking metric.

**Implementation note:** Requires multiple API calls with increasing prompt lengths, so it is a multi-trial benchmark rather than a single-prompt task.

---

## Cross-Cutting Connections

### Sustained Attention <-> Selective Attention
- Selective attention tasks (e.g., noise_filtering) test filtering irrelevant information. Sustained attention tests maintaining performance over time. These interact: filtering may degrade over many repetitions, combining both demands.
- The oddball variant bridges these — it requires the model to selectively process an unexpected item while sustaining attention on routine items.

### Sustained Attention <-> Divided Attention
- Processing 100 sub-tasks in sequence is serial sustained attention. Processing them in a batched/interleaved format would be divided attention. Comparing serial vs. interleaved presentation could isolate the division cost.

### Sustained Attention <-> Inhibitory Control
- The SART analog directly combines sustained attention with inhibitory control (executive function). The oddball variant also requires flexible response when routine processing must be interrupted.

### Sustained Attention <-> Working Memory
- Each sub-task in the vigilance task requires minimal working memory (trivially easy). But the output format (maintaining numbered answers) creates a working memory demand that accumulates. Format degradation in later positions may reflect working memory overload rather than attention failure.

### Sustained Attention <-> Metacognition
- If models could self-monitor their vigilance state, they might flag uncertainty on later items. A metacognitive extension: ask the model to rate confidence on each sub-task. Do confidence ratings track actual accuracy decline?

---

## Key Papers

### Core Sustained Attention / Vigilance (LLM)

1. **Chen et al. (2026).** "How Well Can LLMs Process Multiple Instances?" arXiv:2603.22608
   - Multi-instance processing benchmark; instance count as primary degradation variable
   - Most directly relevant prior work to our vigilance_decrement task

2. **Qiu et al. (2025).** "Context Rot: How Long Contexts Degrade LLM Performance."
   - Three degradation mechanisms: positional, dilution, distraction
   - Universal across 18 frontier models

3. **Du et al. (2025).** "Intelligence Degradation: Exploring the Impact of Context Window Extension."
   - IQ-test performance drops with context length
   - Provocative framing of degradation as "intelligence loss"

### Positional Bias / Lost in the Middle

4. **Liu et al. (2024).** "Lost in the Middle: How Language Models Use Long Contexts." arXiv:2307.03172
   - U-shaped accuracy curve; 30%+ drops for middle positions
   - Landmark paper establishing positional bias in LLMs

5. **Zhang et al. (2024).** "Multi-Scale Positional Encoding (Ms-PoE)." NeurIPS 2024.
   - Mitigation for positional bias via multi-scale encoding

6. **Hsieh et al. (2024).** "RULER: What's the Real Context Size of Your Long-Context Language Models?" arXiv:2404.06654
   - Effective context << claimed context; 13 evaluation tasks

7. **Tang et al. (2024).** "Found in the Middle: How Language Models Use Long Contexts Better via Plug-and-Play Positional Encoding." arXiv:2403.04797
   - RoPE-based fix for middle-context degradation

8. **An et al. (2024).** "STRING: Make Large Language Models Say No to Middle Position Bias." arXiv:2406.02536
   - Single hidden-state dimension manipulation to reduce bias

### Long-Context Benchmarks

9. **Kuratov et al. (2024).** "BABILong: Testing the Limits of LLMs in Long Document Understanding." arXiv:2406.10149
   - bAbI reasoning tasks in long documents; up to 1M tokens

10. **Zhang et al. (2025).** "GSM-Infinity: How Do Your LLMs Deal with Novel and Dynamic Benchmarks?"
    - Math with irrelevant padding; selective attention confound

11. **Li et al. (2024).** "Needlebench: Can LLMs Do Retrieval and Reasoning in 1 Million Context Window?" arXiv:2407.11963
    - Extended NIAH with multi-needle and reasoning variants

### Repetition and Automaticity

12. **Xu et al. (2025).** "The Repeat Curse: LLMs' Repetitive Content in Enumerative Tasks." arXiv:2504.14218
    - LLMs generate repetitive outputs in listing tasks
    - Suggestive of automaticity / failure to maintain novel generation

### Human Sustained Attention (Foundational)

13. **Mackworth, N. H. (1948).** "The breakdown of vigilance during prolonged visual search." *Quarterly Journal of Experimental Psychology*, 1(1), 6-21.
    - Original vigilance decrement finding; WWII radar operators

14. **Rosvold, H. E. et al. (1956).** "A continuous performance test of brain damage." *Journal of Consulting Psychology*, 20(5), 343-350.
    - Original Continuous Performance Test (CPT)

15. **Robertson, I. H. et al. (1997).** "Oops!: Performance correlates of everyday attentional failures in traumatic brain injured and normal subjects." *Neuropsychologia*, 35(6), 747-758.
    - Sustained Attention to Response Task (SART)

16. **Green, D. M. & Swets, J. A. (1966).** *Signal Detection Theory and Psychophysics.* New York: Wiley.
    - SDT framework for decomposing detection performance

17. **Warm, J. S., Parasuraman, R., & Matthews, G. (2008).** "Vigilance requires hard mental work and is stressful." *Human Factors*, 50(3), 433-441.
    - Resource (overload) theory of vigilance decrement

18. **Manly, T. et al. (1999).** "The absent mind: Further investigations of sustained attention to response." *Neuropsychologia*, 37(6), 661-670.
    - Underload / mindlessness theory evidence

---

## Open Questions

1. **Is LLM "vigilance decrement" a real attention phenomenon or an artifact of positional encoding?**
   The multi-instance processing paper (Chen et al. 2026) suggests instance count matters beyond context length, but the mechanisms are unclear. Controlled experiments varying instance count while holding context length constant (via padding) could disambiguate.

2. **Do different architectures show different degradation profiles?**
   Transformer-based models (with quadratic attention) may degrade differently than SSM-based models (Mamba) or hybrid architectures. Our benchmark should include diverse architectures.

3. **Can chain-of-thought or scratchpad mitigate vigilance decrement?**
   If the model generates intermediate reasoning for each sub-task, does this prevent degradation? If so, it suggests the issue is output-side rather than attention-side.

4. **Is the oddball effect position-dependent?**
   Human vigilance research shows that oddball detection rates decline with time-on-task. If LLMs show the same pattern, it strengthens the analogy to human sustained attention.

5. **What is the relationship between model size and vigilance capacity?**
   Larger models may sustain attention longer. The multi-instance paper found model-specific thresholds — our benchmark should characterize this across model families.

6. **Do instruction-tuned models show different vigilance profiles than base models?**
   Instruction tuning may improve output formatting consistency, which could mask or mitigate apparent vigilance decrement. Base models may show more raw degradation.

7. **Is there a "warm-up" effect?**
   Some human vigilance studies show initial improvement before decrement. Do LLMs show higher accuracy on items 5-15 than items 1-5?

8. **Can we separate output degradation from attention degradation?**
   If the model's attention weights (in interpretability sense) remain stable but output formatting degrades, the issue is generation rather than attention. Probing internal representations at different positions could address this, though it requires model access beyond API.

---

## Changelog

- 2026-03-29: Initial analysis from full research sweep
