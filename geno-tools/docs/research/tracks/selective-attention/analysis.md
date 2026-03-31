# Selective Attention: Full Analysis

#attention #selective-attention #analysis

## Overview

Selective attention — the ability to focus on task-relevant information while filtering out irrelevant or misleading content — is one of the most fundamental cognitive capacities. In humans, it has been studied for decades through paradigms like the Stroop task, dichotic listening, and visual search. For LLMs, selective attention manifests as the ability to maintain accurate reasoning and information extraction when the input context contains noise, distractors, or adversarial content designed to mislead.

This sub-area of AttentionBench asks: **How does model performance degrade as the ratio of noise to signal increases, and does the type of noise matter?**

The answer has direct practical implications. Real-world LLM inputs — retrieved documents, user-provided context, web pages, multi-turn conversations — are rarely clean. Understanding how models handle noisy inputs is essential for predicting reliability in deployment.

---

## Landscape of Existing Benchmarks

| Benchmark | Year | Domain | What It Tests | Key Finding | Limitation |
|---|---|---|---|---|---|
| **GSM-IC** (Shi et al.) | 2023 | Math (GSM8K) | Performance drop from adding irrelevant sentences to math word problems | 20-40% accuracy drops from 1-2 irrelevant sentences; models attend to irrelevant info even when clearly off-topic | Binary (clean vs. distracted); single noise level; math-only |
| **GSM-Symbolic** (Mirzadeh et al.) | 2024 | Math (symbolic) | Sensitivity to symbolic variations and added clauses | Up to 65% drop from a single unnecessary clause; questions pattern matching vs. genuine reasoning | Focuses on math reasoning fragility; single distractor level |
| **GSM-DC** (Zhang et al.) | 2025 | Math (directed graphs) | Controlled reasoning with distractors via symbolic computation graphs | Distractors impair both reasoning path selection and arithmetic accuracy; separates two failure modes | Synthetic math domain; doesn't test information extraction |
| **CogniLoad** (Kaiser et al.) | 2025 | Reading comprehension | Cognitive Load Theory applied to LLMs — intrinsic vs. extraneous load | U-shaped distractor response; task length is dominant constraint; some models improve with moderate distractors | Focused on reading comprehension; binary noise categorization |
| **Needle in a Haystack** (Kamradt) | 2024 | Retrieval | Finding a specific fact embedded in long context | Performance varies by position and context length; "lost in the middle" effect | Single needle; uniform filler; no adversarial content; tests retrieval not filtering |
| **DENIAHL** (Levy et al.) | 2025 | Retrieval (adversarial) | Needle-in-haystack with distracting needles that share surface features | Models struggle when distractors are semantically similar to the target; tests precision of retrieval | Single-fact retrieval; doesn't test comprehension or multi-question extraction |
| **Distractor Injection Attacks** (arXiv:2510.16259) | 2025 | Adversarial reasoning | Hijacking model reasoning via injected adversarial distractors | Adversarial reasoning paths can redirect model conclusions even when correct info is present | Attack-focused; not a benchmark per se |

---

## Gap Analysis

### What existing work measures well
- **Binary distractor sensitivity**: GSM-IC and GSM-Symbolic clearly demonstrate that models are sensitive to added context. This is well-established.
- **Long-context retrieval**: NIAH and DENIAHL test whether models can find specific facts in long documents.
- **Math reasoning fragility**: GSM-DC provides fine-grained analysis of how distractors break mathematical reasoning.

### What is NOT being measured
1. **Graduated noise ratios**: No existing benchmark systematically varies the noise-to-signal ratio across a wide range (1:1 to 100:1). Existing work is binary (clean vs. distracted) or uses a small number of fixed levels.

2. **Noise type taxonomy**: No benchmark compares unrelated, related, and adversarial noise within the same experimental framework. CogniLoad distinguishes intrinsic vs. extraneous load but doesn't further categorize noise types.

3. **Attention threshold as a metric**: No existing benchmark defines or measures the noise ratio at which performance degrades below a threshold. This is a novel metric that provides a single, interpretable number per model per noise type.

4. **Multi-question comprehension under noise**: NIAH tests single-fact retrieval. Our task requires answering 5 factual questions from a passage — testing whether models can maintain comprehensive understanding, not just locate a single fact.

5. **Non-mathematical domains**: GSM-IC/Symbolic/DC are all math. CogniLoad uses reading comprehension but with limited noise variation. There is room for fictional factual passages that avoid training data contamination.

6. **Interaction between noise type and noise ratio**: How does the *type* of noise change the shape of the degradation curve? Does adversarial noise cause a cliff-edge drop while unrelated noise causes gradual decline? No existing work characterizes these curves.

---

## Our Approach: Noise Filtering

### Design Philosophy
We treat selective attention as a psychophysics experiment: hold the signal constant, systematically vary the noise, and measure the response function. This yields interpretable curves and a single summary metric (attention threshold).

### Key Design Decisions

**Fictional passages**: All 10 signal passages describe fictional scenarios (underwater research stations, space missions, archaeological discoveries). This eliminates training data contamination — models cannot recall the "right" answer from pretraining.

**Three noise types with increasing difficulty**:
1. **Unrelated noise** — paragraphs from completely different domains (e.g., cooking recipes inserted into a passage about marine biology). Tests basic filtering.
2. **Related noise** — paragraphs from the same domain but containing different facts (e.g., other marine biology facts that don't answer the questions). Tests domain-level discrimination.
3. **Adversarial noise** — paragraphs that reference the same entities and topics but with altered facts (wrong numbers, swapped names, changed causal claims). Tests fact-level discrimination.

**Six noise ratios**: 1:1, 5:1, 10:1, 25:1, 50:1, 100:1 (noise paragraphs per signal paragraph). The wide range ensures we find the threshold for every model — even the most robust ones will degrade somewhere between 1:1 and 100:1.

**Interleaved presentation**: Signal is chunked into 3-sentence blocks and interleaved with noise paragraphs. This prevents models from simply reading the first or last block — they must integrate information scattered throughout the context.

### Metric: Attention Threshold

For each model and noise type, we fit the accuracy-vs-ratio curve and identify the **attention threshold** — the noise ratio at which accuracy first drops below 80%. This gives:
- A single number per (model, noise_type) combination
- Natural ordering: higher threshold = better selective attention
- Interpretable comparisons: "Model A maintains 80% accuracy at 25:1 adversarial noise; Model B drops below 80% at 5:1"

---

## Key Papers and Citations

### Primary References

**Shi, F., Chen, X., Misra, K., Scales, N., Dohan, D., Chi, E., Schärli, N., & Zhou, D. (2023).** Large Language Models Can Be Easily Distracted by Irrelevant Context. *ICML 2023*. arXiv:2302.00093.
- Introduced GSM-IC (Grade School Math with Irrelevant Context)
- Demonstrated that even state-of-the-art LLMs are significantly distracted by irrelevant information
- Found prompting strategies (e.g., "ignore irrelevant information") provide partial but incomplete mitigation

**Mirzadeh, I., Alizadeh, K., Shahrokhi, H., Tuzel, O., Bengio, S., & Farajtabar, M. (2024).** GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models. *Apple Research*. arXiv:2410.05229.
- Created symbolic templates from GSM8K to generate novel instances
- Showed performance varies significantly across different instantiations of the same template
- Added GSM-NoOp variant: a single unnecessary clause causes up to 65% performance drop
- Argues models rely on pattern matching rather than genuine mathematical reasoning

**Kaiser, K., Perez, G., Schmidt, R., & Tiede, C. (2025).** How Many Distractors Can LLMs Handle? Evaluating Cognitive Overload in Large Language Models. *arXiv:2025* (CogniLoad).
- Applied Cognitive Load Theory (Sweller, 1988) to LLM evaluation
- Separated intrinsic load (task difficulty) from extraneous load (distractors)
- Found U-shaped response: some models improve at moderate distractor levels before degrading
- Task length identified as the dominant constraint, more than distractor count

**Zhang, S., et al. (2025).** GSM-DC: Probing the Robustness of LLM Reasoning with Distractors in GSM Problems via Directed Acyclic Computation Graphs. *arXiv:2025*.
- Models math problems as directed acyclic computation graphs
- Separates "reasoning path selection" errors from "arithmetic execution" errors
- Distractors impair both, but path selection is more vulnerable

### Secondary References

**Kamradt, G. (2024).** Needle in a Haystack — Pressure Testing LLMs.
- Popularized long-context evaluation via single-fact retrieval
- Revealed position-dependent retrieval accuracy ("lost in the middle")

**Levy, M., Jacoby, A., & Goldberg, Y. (2025).** Same Task, More Tokens: the Impact of Input Length on the Reasoning Performance of Large Language Models. *ACL 2025*. arXiv:2402.14848.
- Demonstrated that increased input length alone (even padding) degrades reasoning

**DENIAHL (2025).** Distracting Needle in a Haystack variant.
- Added distracting needles with surface-level similarity to the target
- Showed retrieval precision degrades when distractors share features with the target

**Sweller, J. (1988).** Cognitive Load During Problem Solving: Effects on Learning. *Cognitive Science, 12*(2), 257-285.
- Foundational theory: working memory is limited; extraneous cognitive load impairs learning and performance
- Directly applicable to LLM context window as an analogue of working memory

---

## Noise Type Analysis and Expected Discrimination

### Unrelated Noise
- **Source**: Cross-domain paragraphs (cooking, sports, politics, etc.)
- **Expected curve**: Gradual, near-linear degradation. Models should easily distinguish signal from noise at low ratios. Degradation at high ratios comes from context window dilution and positional effects, not confusion.
- **Discrimination**: Low — most models should perform similarly. Useful as a baseline.

### Related Noise
- **Source**: Same-domain paragraphs with different facts (e.g., real marine biology for a fictional marine biology passage)
- **Expected curve**: Steeper than unrelated. Models must discriminate at the fact level, not the domain level. Some models may confuse related facts with signal facts.
- **Discrimination**: Moderate — should separate models that genuinely comprehend from those that pattern-match on domain keywords.

### Adversarial Noise
- **Source**: Per-passage crafted paragraphs referencing the same entities with altered facts
- **Expected curve**: Steep, possibly cliff-edge. Even at low ratios, models may latch onto adversarial alternatives. The threshold should be significantly lower than for other noise types.
- **Discrimination**: High — this is where we expect the most meaningful separation between models. Models with robust selective attention will maintain accuracy at ratios where weaker models fail completely.

### Cross-Type Analysis
The *difference* in attention thresholds across noise types is itself informative:
- Small gap (unrelated vs. adversarial): model has strong fact-level discrimination
- Large gap: model relies on domain-level filtering and fails when noise is domain-matched
- This gap metric could be a novel contribution — measuring not just absolute performance but the *specificity* of a model's attention mechanism

---

## Open Questions

1. **Does chain-of-thought help or hurt?** CoT might help models explicitly track which information is relevant, but it also increases the chance of attending to and reasoning about noise. Our benchmark should test both CoT and direct-answer modes.

2. **Position effects**: Does it matter where the signal blocks appear relative to noise? NIAH showed position effects for retrieval — do similar effects exist for comprehension under noise?

3. **Scaling with context window**: Models with larger context windows might handle high noise ratios better simply by having more "room." Is there a way to normalize for context window size?

4. **Few-shot vs. zero-shot**: Do examples of noise filtering in the prompt help models understand they should ignore noise? This could be a secondary axis of investigation.

5. **Noise coherence**: Our noise paragraphs are individually coherent. What happens with incoherent noise (random sentences, shuffled words)? Is coherent noise harder or easier to filter?

6. **Transfer to real-world tasks**: Does attention threshold on our synthetic benchmark predict performance on real-world noisy tasks (e.g., RAG with irrelevant retrieved documents)?

7. **Model size effects**: Do larger models within a family show better selective attention, or is this an architectural property? Initial results suggest reasoning models (o-series, DeepSeek-R1) may have qualitatively different attention profiles.

---

## Changelog

- 2026-03-29: Initial analysis from full research sweep
