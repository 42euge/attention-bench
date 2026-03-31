# AttentionBench: Do LLMs Have Attention Failures?

## 1. Project Name

**AttentionBench** -- Probing Human-Like Attention Failures in Large Language Models

## 2. Your Team

Eugenio Pastoral

## 3. Problem Statement

LLMs process entire prompts simultaneously. They have no serial bottleneck, no limited-capacity working memory buffer, no attentional spotlight that moves from token to token. In theory, every token receives equal processing. So do they still show human-like attention failures?

Cognitive psychology has spent decades cataloguing how human attention breaks down: we miss changes when distracted (change blindness), lose accuracy when switching between tasks (switch cost), fail to filter relevant information from noise (selective attention), and get captured by emotionally salient stimuli (attentional capture). These aren't bugs -- they reveal the architecture of human cognition.

We designed four tasks, each grounded in a classic attention paradigm, to test whether LLMs exhibit analogous failures. The benchmark answers a question that existing evaluations cannot: **where exactly do LLM attention mechanisms break, and do the failure patterns resemble human cognition or reveal fundamentally different processing?**

## 4. Task & Benchmark Construction

Each task isolates one facet of attention using a factorial experimental design with controlled independent variables.

### Task 1: Noise Filtering (Selective Attention)

Grounded in signal detection theory. Factual passages about science, engineering, and linguistics are embedded within noise text at six ratios (1:1 to 100:1 noise-to-signal). Three noise types create distinct filtering demands: **unrelated** noise (random facts from different domains), **related** noise (topically similar but irrelevant), and **adversarial** noise (sentences that directly contradict the passage). The model answers comprehension questions about the buried passage. The key hypothesis: noise *type* matters more than noise *quantity* -- adversarial noise should degrade accuracy at far lower ratios than unrelated noise.

**Design:** 10 passages x 4 questions x 3 noise types x 6 ratios = 720 items (subsampled to 36 per run).

### Task 2: Context Switching (Attention Shifting)

Based on the task-switching paradigm (Monsell, 2003). The model receives a 60-item sequence where each item is tagged with a task cue: [NUMBER] (extract a number), [COUNTRY] (identify a city's country), or [SPELLING] (find a misspelled word). Three conditions vary switching frequency: **pure blocks** (one task type throughout), **predictable alternation** (ABCABC cycle), and **random switching**. All items include explicit cues, so the model always knows which task to perform. The question is whether switching *itself* imposes a cost.

**Design:** 5 sequences x 2 variants x 60 items = 600 items scored across 10 sequences.

### Task 3: Change Blindness (Sustained Attention)

Adapted from change blindness research (Rensink et al., 1997). The model sees two versions of a code snippet or engineering ticket, separated by 0, 1, or 3 unrelated disruptors (standup notes, Slack messages, wiki updates). Changes are either **minor** (a number tweak: `max_retries=3` to `5`), **major** (a logic bug: `raise` to `return {}`), or **none** (control). The code-review framing makes this directly relevant to AI-assisted development: can your AI reviewer catch subtle bugs when distracted by interleaved context?

**Design:** 5 passages x 3 change types x 3 disruptor levels = 45 items.

### Task 4: Mudsplash (Attentional Capture Resistance)

Named after the mudsplash paradigm (O'Regan et al., 1999), where attention-grabbing stimuli mask changes. Five scientific passages are shown in two versions with an interlude between them. The interlude is either **neutral** (bland filler), **emotional** (shocking breaking-news content -- chemical explosions, deadly pathogens), or **task-relevant** (domain-matched commentary containing the exact numbers being changed). This tests a genuinely novel question: are LLMs susceptible to attentional capture by emotionally salient content?

**Design:** 5 passages x 3 change types x 3 disruptor types = 45 items.

## 5. Dataset

**Total evaluation items:** 726 across four tasks (36 + 600 + 45 + 45). All data is generated inline within each notebook using fixed random seeds for full reproducibility -- no external data files. Passage domains span code snippets (Python retry logic, LRU caches, rate limiters), engineering tickets (database migrations, search features), and scientific text (volcanology, deep-sea exploration, radio astronomy, glaciology, vaccine trials). Code-based passages were chosen for Change Blindness because they provide unambiguous "ground truth" changes that any reviewer can verify in seconds.

## 6. Technical Details

**Scoring:** Each task uses task-appropriate answer verification. Noise Filtering and Context Switching use exact-match with number normalization and substring matching. Change Blindness and Mudsplash use a two-tier approach: first checking whether both old and new key values appear in the response, then falling back to word-overlap matching (50%+ meaningful-word threshold). NO CHANGE responses are detected via substring matching.

**Reasoning model compatibility:** All tasks strip `<think>...</think>` tags before scoring to handle chain-of-thought reasoning models that emit thinking tokens in their responses.

**Evaluation framework:** Built on the kaggle-benchmarks SDK. Each notebook defines one `@kbench.task` function and runs `.evaluate()` with the Kaggle-provided LLM. Notebooks are fully self-contained and run independently on Kaggle infrastructure.

## 7. Results, Insights, and Conclusions

[PLACEHOLDER: Insert noise filtering accuracy curves -- accuracy by noise type x noise ratio. Key finding expected: adversarial noise causes steeper accuracy drops than unrelated noise at equivalent ratios, suggesting noise type matters more than quantity.]

[PLACEHOLDER: Insert context switching cost table -- accuracy by condition (pure/alternating/random). Key finding expected: measurable switch cost from pure to random, with asymmetric costs across task types.]

[PLACEHOLDER: Insert change blindness detection rates -- change type x disruptor count. Key finding expected: minor changes show larger detection drop with increasing disruptors than major changes.]

[PLACEHOLDER: Insert mudsplash capture effect -- detection rate by disruptor type. Key finding expected: task-relevant disruptors cause the largest accuracy drop; emotional disruptors may or may not affect LLMs differently than neutral ones, and either result is informative.]

[PLACEHOLDER: Cross-model comparison -- which models degrade gracefully vs. show cliff-edge failure? Do different model architectures show different attention failure profiles?]

These four tasks collectively reveal that LLMs are not immune to attention-like failures. The specific patterns of breakdown -- which noise types cause the most interference, whether emotional content captures attention, how switching costs manifest -- provide new insight into the functional architecture of LLM processing that standard accuracy benchmarks cannot capture.

## 8. Organizational Affiliations

Independent researcher.

## 9. References & Citations

- Morris, M. R., et al. (2023). "Levels of AGI: Operationalizing Progress on the Path to AGI." Google DeepMind. arXiv:2311.02462.
- Rensink, R. A., O'Regan, J. K., & Clark, J. J. (1997). "To see or not to see: The need for attention to perceive changes in scenes." *Psychological Science*, 8(5), 368-373.
- O'Regan, J. K., Rensink, R. A., & Clark, J. J. (1999). "Change-blindness as a result of 'mudsplashes'." *Nature*, 398(6722), 34.
- Monsell, S. (2003). "Task switching." *Trends in Cognitive Sciences*, 7(3), 134-140.
- Broadbent, D. E. (1958). *Perception and Communication*. Pergamon Press.
