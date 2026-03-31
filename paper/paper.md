# AttentionBench: A Cognitive Science-Grounded Benchmark for Measuring Attention in Frontier Language Models

## Abstract

We introduce AttentionBench, a benchmark suite of 8 tasks spanning 4 attention sub-types from cognitive science: selective attention (noise filtering), sustained attention (vigilance decrement, continuous performance), divided attention (attentional blink, dual-task interference, context switching), and change detection (change blindness, mudsplash). Each task isolates a specific attentional mechanism by holding reasoning difficulty constant while parametrically varying attentional demands, using designs adapted from established clinical neuropsychology paradigms. Evaluating 8 models from 1B to frontier scale on the noise filtering and vigilance tasks, we find that adversarial noise — text containing plausible but incorrect answers — is the *only* noise type that discriminates between models, producing a clean scaling ladder in the Gemma family (1B: 0:1, 4B: 1:1, 12B: 10:1, 27B: 100:1 threshold). Unrelated and topically related noise, even at 100:1 ratios, barely affect any model above 4B parameters. This finding suggests that LLM "attention" is primarily a semantic discrimination problem, not a capacity problem. The full 8-task suite introduces Signal Detection Theory decomposition, attentional blink measurement, dual-task cost quantification, and change detection with metacognitive calibration — capabilities no existing LLM benchmark measures.

## 1. Introduction

As large language models are deployed in complex real-world tasks — analyzing lengthy documents, processing multi-source information, maintaining consistency across extended interactions — their ability to attend to relevant information amid noise becomes critical. Yet our understanding of *how* and *when* models lose attentional focus remains shallow.

Existing benchmarks suffer from fundamental confounds. Needle-in-a-Haystack [1] is saturated for frontier models [2]. RULER [3] blends reasoning with retrieval. "Lost in the Middle" [4] does not separate attentional failure from positional encoding artifacts. GSM-DC [5] and NoisyBench [6] conflate task difficulty with noise-filtering difficulty. More fundamentally, no benchmark measures attention as a *multidimensional cognitive ability* — the way it is understood in cognitive science.

In human cognition, attention is not monolithic. It comprises at least four sub-types [7, 8]: selective attention (filtering signal from noise), sustained attention (maintaining focus over time), divided attention (managing concurrent demands), and the ability to detect changes in the environment. Each has distinct failure modes, neural substrates, and clinical assessments. Yet LLM evaluation treats "attention" as a single capability, if it measures it at all.

We address this with AttentionBench: 8 tasks spanning 4 attention sub-types, each adapted from an established cognitive science paradigm. By holding task difficulty constant while varying attentional load, any performance degradation is attributable to attentional — not reasoning — failure.

Our contributions:

- A benchmark suite of 8 tasks measuring 4 attention sub-types, each grounded in a clinical neuropsychology paradigm (dichotic listening, Mackworth clock, RSVP, PRP, task-switching, flicker, mudsplash).
- The finding that **adversarial noise is the sole discriminator** of selective attention — unrelated and related noise fail to separate any model above 4B parameters, even at 100:1 ratios.
- Evidence of a **log-linear scaling law**: adversarial attention threshold scales log-linearly with model size across the Gemma family (1B–27B).
- Novel measurement capabilities for LLMs: Signal Detection Theory decomposition, attentional blink curves, dual-task interference costs, and confidence-calibrated change detection.
- A contamination-resistant, fully procedural dataset of ~2,800 items with deterministic generation.

## 2. Benchmark Design

| Sub-type | Task | Paradigm | Key Metric | Items |
|----------|------|----------|------------|-------|
| Selective | Noise Filtering | Dichotic listening | Attention threshold (noise ratio at 80%) | 180 |
| Sustained | Vigilance Decrement | Mackworth clock | Decay onset; d', criterion by position | 900 |
| Sustained | Continuous Performance | CPT-AX | Hit rate, FA rate, d', lure commissions | 800 |
| Divided | Attentional Blink | RSVP | T2|T1 accuracy by lag; blink magnitude | 120 |
| Divided | Dual-Task Interference | PRP | Dual-task cost; asymmetric interference | 42 |
| Divided | Context Switching | Task-switching | Switch cost (pure vs. mixed) | 600 |
| Change Det. | Change Blindness | Flicker | Detection rate × magnitude × disruption; ECE | 45 |
| Change Det. | Mudsplash | Mudsplash | Attentional capture effect by disruptor type | 45 |

### 2.1 Selective Attention: Noise Filtering

A ~200-word fictional passage with 5 factual questions is embedded in progressively larger noise at ratios from 1:1 to 100:1. Three noise types probe different filtering demands:

- **Unrelated**: Cross-domain filler (geology amid marine biology).
- **Related**: Same-domain text that does not answer the questions.
- **Adversarial**: Text containing plausible but incorrect answers (e.g., "3,100 meters" when the correct answer is "2,400 meters").

Signal and noise are interleaved in chunks to prevent positional heuristics [4]. At 100:1, prompts reach ~129K characters. The metric is **attention threshold**: the highest noise ratio where accuracy ≥ 80%.

### 2.2 Sustained Attention

**Vigilance Decrement.** 100 trivially easy sub-tasks (country identification, number extraction, misspelling detection) in a single prompt. Three variants: normal, oddball (one unexpected task type at position 40–70), and SDT (15% target-absent trials). SDT variants decompose performance into sensitivity (d') and criterion (c) by 10-item position window, revealing whether degradation reflects reduced sensitivity or shifted response bias.

**Continuous Performance Test (CPT).** 200-item sequences where the model classifies each sentence as TARGET or NON-TARGET. Low target frequency (~15%) creates monotony. Lure items from semantically similar categories (e.g., climate science lures for a weather target) test discrimination. Metrics: hit rate, false alarm rate, d', and lure commission rate.

### 2.3 Divided Attention

**Attentional Blink.** Adapted from the RSVP paradigm [9]. A stream of 20 sentences contains two targets from specified categories. The lag between targets varies from 1–8 items. The key measure is T2|T1 accuracy across lags — in human cognition, T2 detection drops sharply at lags 2–5 (the "blink") with paradoxical lag-1 sparing. This is the first text-based attentional blink task for LLMs.

**Dual-Task Interference.** The model simultaneously answers comprehension questions and counts word occurrences in the same passage. Single-task baselines (comprehension only, counting only) allow precise quantification of dual-task cost and asymmetric interference.

**Context Switching.** 60-item sequences alternating between number extraction, country identification, and misspelling detection. Three conditions — pure blocks, predictable alternation, random switching — measure task-switch cost.

### 2.4 Change Detection

**Change Blindness.** Two passage versions separated by 0–3 disruptor paragraphs. Changes range from minor (number swaps) to major (causal claim reversals). No-change controls measure false alarm rate. Confidence ratings (1–5) enable metacognitive calibration analysis via Expected Calibration Error (ECE).

**Mudsplash.** Same structure as change blindness, but the disruptor type varies: neutral (bland factual filler), emotional (shocking content — explosions, contamination), or task-relevant (domain-similar technical content). Measures whether salient disruptors cause models to miss changes — the LLM analogue of the visual "mudsplash" paradigm.

### 2.5 Community Benchmarks

We also provide Kaggle-ready reproductions of two related benchmarks: **GSM-IC** [10] (irrelevant context distraction in math) and **Needle-in-a-Haystack** [1] (long-context retrieval), enabling direct comparison with our tasks.

## 3. Results: Noise Filtering & Vigilance

We report results from multi-model evaluation of the two core tasks. The remaining 6 tasks are deployed on Kaggle Benchmarks and awaiting multi-model evaluation.

### 3.1 Evaluation Setup

We evaluated 8 models as an orthogonal set: four Gemma sizes (1B, 4B, 12B, 27B) as a controlled scaling ladder, three frontier models (Claude Opus 4-6, Claude Haiku 4-5, Gemini 2.5 Flash), and one reasoning model (DeepSeek R1). Evaluation used the Kaggle Benchmarks platform: 336 LLM calls completing in 14 minutes. Answer matching uses case-insensitive substring comparison with number normalization. Reasoning model responses are preprocessed to strip `<think>` blocks and preamble text.

### 3.2 Signal-in-Noise Results

**Table 1: Attention thresholds (highest noise ratio at ≥80% accuracy)**

| Model | Unrelated | Related | Adversarial |
|-------|-----------|---------|-------------|
| claude-opus-4-6 | **100:1** | **100:1** | **100:1** |
| claude-haiku-4-5 | **100:1** | **100:1** | **100:1** |
| gemini-2.5-flash | **100:1** | **100:1** | **100:1** |
| gemma-3-27b | **100:1** | **100:1** | **100:1** |
| deepseek-r1 | **100:1** | **100:1** | 50:1 |
| gemma-3-12b | **100:1** | **100:1** | 10:1 |
| gemma-3-4b | **100:1** | **100:1** | 1:1 |
| gemma-3-1b | 5:1 | 10:1 | 0:1 |

The results reveal a striking asymmetry. **Unrelated and related noise fail to discriminate**: every model above 1B achieves 100:1 for both types. **Adversarial noise is the sole discriminator**, with a clean gradient: 0:1 → 1:1 → 10:1 → 50:1 → 100:1 as model capability increases.

The Gemma family shows a log-linear scaling law: each ~3× increase in parameters yields ~10× increase in adversarial noise tolerance.

| Parameters | log₁₀ | Adversarial Threshold |
|------------|--------|-----------------------|
| 1B | 9.0 | 0:1 (baseline failure) |
| 4B | 9.6 | 1:1 |
| 12B | 10.1 | 10:1 |
| 27B | 10.4 | 100:1 |

Overall mean SIN accuracy: claude-opus-4-6 (100.0%), claude-haiku-4-5 (98.9%), deepseek-r1 (97.1%), gemma-3-27b (95.0%), gemini-2.5-flash (92.2%), gemma-3-12b (90.6%), gemma-3-4b (77.8%), gemma-3-1b (58.3%).

### 3.3 Vigilance Results

**Table 2: Vigilance accuracy (% of 100 sub-tasks). N=normal, O=oddball.**

| Model | Country (N) | Country (O) | Number (N) | Number (O) | Misspell (N) | Misspell (O) |
|-------|------------|------------|-----------|-----------|-------------|-------------|
| claude-opus-4-6 | 100 | 100 | 100 | 98 | 100 | 100 |
| claude-haiku-4-5 | 100 | 100 | 100 | 100 | 100 | 97 |
| gemini-2.5-flash | 100 | 100 | 100 | 91 | 100 | 96 |
| gemma-3-27b | 100 | 100 | 100 | 99 | 0* | 100 |
| deepseek-r1 | 100 | 100 | 96 | 88 | 100 | 100 |
| gemma-3-12b | 98 | 100 | 100 | 100 | 100 | 100 |
| gemma-3-4b | 91 | 96 | 72 | 32 | 0* | 0 |
| gemma-3-1b | 1 | 35 | 78 | 40 | 0* | 0 |

*Entries marked * reflect a task comprehension issue (see Section 4.4).*

Frontier models maintain near-perfect vigilance. The Gemma family shows clear differentiation: 1B catastrophic (21% mean), 4B partial (49%), 12B and 27B near-ceiling. DeepSeek R1 scores 88% on number oddball — the lowest among frontier models — suggesting chain-of-thought processing is disrupted by unexpected stimuli.

### 3.4 Cross-Dimensional Analysis

Models that resist adversarial noise generally maintain vigilance, with one exception: DeepSeek R1 achieves 97.1% SIN accuracy (third highest) but the most vigilance degradation among frontier models, suggesting chain-of-thought provides selective but not sustained attentional benefits.

## 4. Discussion

### 4.1 Adversarial Noise as Cognitive Discriminator

The central finding is that *type* of noise matters far more than *volume*. Models locate a 200-word passage within 20,000 words of unrelated text easily. But adversarial noise — plausible alternative answers — collapses performance in a size-dependent manner. Unrelated tokens receive low attention scores because they are semantically distant; adversarial tokens compete directly with correct answers in the attention distribution, requiring finer-grained semantic discrimination that scales with model size.

This parallels the "strong memory, weak control" finding [11], showing LLMs have enormous context capacity but struggle with *discriminating* between competing signals. The practical implication: a model handling 128K tokens of filler may still be fooled by a few adversarial sentences.

### 4.2 Scaling Laws for Attention

Within the Gemma family, the adversarial threshold follows approximately:

```
Threshold ≈ 10^(2.5 × log₁₀(N) - 22.5)
```

Each 3× parameter increase yields ~10× noise tolerance gain. This contrasts with non-adversarial noise, which shows a sharp phase transition (1B fails, 4B+ saturates) rather than gradual scaling.

### 4.3 Reasoning Models and Attention

DeepSeek R1's adversarial threshold (50:1) falls below gemma-3-27b (100:1). Investigation revealed R1's chain of thought explicitly considered adversarial values before settling on them as answers — the model *reasoned its way to the wrong answer*. This echoes NoisyBench's finding of inverse scaling [6]: more thinking can mean worse noise filtering.

### 4.4 The Case for Multidimensional Measurement

Our results from just two tasks already reveal that selective and sustained attention are partially dissociable: DeepSeek R1 excels at one but not the other. The full 8-task suite is designed to expose further dissociations. Do models that resist adversarial noise also resist attentional capture from emotional content (mudsplash)? Do models with high vigilance show attentional blink patterns? Does dual-task cost correlate with context-switching cost? These cross-task analyses will reveal whether LLM attention is a single capability or a bundle of separable faculties.

### 4.5 Limitations

**Ceiling effects.** Four models achieve the maximum adversarial threshold (100:1). Higher ratios are needed.

**Sample sizes.** With 2 passages per SIN configuration, thresholds are based on 10 questions per cell. The full benchmark includes more items per task.

**Task ambiguity.** Misspelling detection is ambiguous (return misspelled form vs. correct form). Gemma-3-27b and 4b chose the latter, inflating their error rates.

**Partial evaluation.** Results are reported for 2 of 8 tasks. The remaining tasks are deployed on Kaggle and awaiting multi-model evaluation.

## 5. Related Work

**Long-context retrieval.** NIAH [1] and RULER [3] measure retrieval but are saturated or conflate reasoning. Our noise filtering generalizes NIAH by parameterizing noise type and volume.

**Context degradation.** Context Rot [12] found coherent distractors hurt more than random noise — consistent with our adversarial finding. Du et al. [13] isolated length from distraction effects.

**Distractor sensitivity.** GSM-DC [5] and GSM-Symbolic [14] showed up to 65% drops from numerical distractors. We extend to factual retrieval and identify semantic similarity as the critical variable.

**Cognitive benchmarks.** The DeepMind framework [15] identifies attention as under-evaluated. De Langis et al. [11] found executive control deficits. NeuroCognition [16] applied cognitive batteries to LLMs. We contribute the first benchmark treating LLM attention as a multidimensional cognitive ability with distinct sub-types.

**Attentional paradigms.** No prior work adapts the attentional blink [9], mudsplash, or CPT paradigms for LLM evaluation. Our change blindness task with confidence calibration also introduces metacognitive measurement absent from existing benchmarks.

## 6. Conclusion

AttentionBench provides the first systematic measurement of attention as a multidimensional cognitive ability in LLMs: 8 tasks spanning selective, sustained, divided, and change-detection attention, each adapted from established cognitive science paradigms.

Results from the noise filtering and vigilance tasks reveal that adversarial noise is the critical discriminator — not volume but *semantic proximity* determines whether noise degrades performance. The adversarial attention threshold scales log-linearly with model size, and chain-of-thought reasoning does not prevent adversarial capture.

The full benchmark introduces measurement capabilities absent from existing LLM evaluation: Signal Detection Theory decomposition, attentional blink curves, dual-task interference quantification, and confidence-calibrated change detection. We release all 8 tasks as self-contained notebooks on Kaggle Benchmarks for multi-model evaluation by the community.

## References

[1] G. Kamradt, "Needle in a Haystack - Pressure Testing LLMs," 2023.

[2] H. Yen et al., "HELMET: How to Evaluate Long-context Language Models Effectively and Thoroughly," ICLR, 2025. arXiv:2410.02694.

[3] S. Hsieh et al., "RULER: What's the Real Context Size of Your Long-Context Language Models?" COLM, 2024. arXiv:2404.06654.

[4] N. F. Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," TACL, 2024. arXiv:2307.03172.

[5] X. Li et al., "GSM-DC: Distractor-Augmented Grade School Math," EMNLP, 2025. arXiv:2505.18761.

[6] "NoisyBench: Benchmarking the Robustness of Language Models to Input Noise," 2026. arXiv:2601.07226.

[7] M. I. Posner, "Orienting of attention," Quarterly Journal of Experimental Psychology, 1980.

[8] D. E. Broadbent, Perception and Communication, Pergamon Press, 1958.

[9] J. E. Raymond et al., "Temporary suppression of visual processing in an RSVP task: An attentional blink?" JEPHPP, 1992.

[10] F. Shi et al., "Large Language Models Can Be Easily Distracted by Irrelevant Context," ICML, 2023. arXiv:2302.00093.

[11] K. de Langis et al., "Strong Memory, Weak Control: LLMs Exhibit Human-Like Memory-Control Asymmetry," 2025. arXiv:2504.02789.

[12] R. Hong et al., "Context Rot," Chroma Research, 2025.

[13] H. Du et al., "Context Length Alone Does Not Hurt," EMNLP, 2025. arXiv:2510.05381.

[14] I. Mirzadeh et al., "GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in LLMs," ICLR, 2025. arXiv:2410.05229.

[15] R. Burnell et al., "Measuring Progress Toward AGI: A Cognitive Framework," Google DeepMind, 2026.

[16] "NeuroCognition: Adapting Neuropsychological Batteries for LLM Evaluation," 2026. arXiv:2603.02540.

## Appendix A: Example Prompt (Noise Filtering)

At 5:1 adversarial noise ratio, a ~200-word passage is split into 4 chunks and interleaved with 5 noise chunks (~1,000 words):

```
[Noise chunk 1] [Signal chunk 1] [Noise chunk 2]
[Signal chunk 2] [Noise chunk 3] [Signal chunk 3]
[Noise chunk 4] [Signal chunk 4] [Noise chunk 5]

Based on the passage above, answer these questions:
1. At what depth were the organisms discovered?
2. What enzyme is involved in the bioluminescence?
3. What is the name of the ROV used?
4. How long was the sample collection period?
5. What compound was named as the substrate?

Provide ONLY the answers, one per line, numbered 1-5.
```

Adversarial noise includes: "the organisms were found at a depth of 3,100 meters" and "the substrate was identified as bathozine" — plausible alternatives to "2,400 meters" and "kerovazine."

## Appendix B: Methodological Evolution

**v4** (27 models, 25:1 max): 20/27 models at ceiling → extended to 100:1.

**v5** (8 models, 100:1): DeepSeek R1's `<think>` blocks parsed as answers (1.1% accuracy artifact) → think-tag stripping.

**v6**: Preamble lines ("Here are the answers:") counted as answer #1 → require numbered prefix.

These iterations show that **evaluation methodology is as important as benchmark design**. Response format diversity across model families is a systematic challenge for automated LLM evaluation.

## Appendix C: Task Design Summaries

**Attentional Blink.** 20-sentence streams with two embedded targets from specified categories. Lag between targets varies 1–8. Tests whether models show the characteristic "blink" — temporary inability to detect T2 shortly after T1. 120 items across 3 category pairs.

**Dual-Task Interference.** Simultaneously answer comprehension questions and count word occurrences. Single-task baselines quantify dual-task cost. 42 items across 3 passages.

**Context Switching.** 60-item sequences alternating number extraction, country identification, and misspelling detection. Pure blocks vs. predictable alternation vs. random switching. 600 items.

**CPT.** 200-item target/non-target classification. 15% target rate, 5% semantically similar lures. SDT analysis. 800 items.

**Change Blindness.** Two passage versions with minor/major changes, separated by 0–3 disruptors. Confidence ratings enable ECE calibration. 45 items.

**Mudsplash.** Change detection with neutral, emotional, or task-relevant disruptors. Tests attentional capture. 45 items.
