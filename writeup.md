# AttentionBench: Do LLMs Have Attention Failures?

## 1. Project Name

**AttentionBench** -- Probing Human-Like Attention Failures in Large Language Models

## 2. Your Team

Eugenio Pastoral

## 3. Problem Statement

Transformers have no attentional bottleneck. Every token attends to every other token; there is no serial spotlight, no limited-capacity buffer, no moment where information goes unprocessed. In theory, a transformer should never "miss" anything in its context window. So why would we test LLMs for attention failures?

Because attention is not just about input access -- it is about *selective processing under cognitive load*. Humans fail not because they cannot see, but because they cannot prioritize. The question is whether LLMs, despite architectural advantages, face analogous prioritization failures when the demands of a task exceed what uniform token-level processing can handle.

Cognitive psychology offers precise paradigms for probing this: change blindness (Rensink et al., 1997), task-switching cost (Monsell, 2003), signal detection under noise (Broadbent, 1958), and attentional capture by salient distractors (O'Regan et al., 1999). Each reveals a different failure mode of selective processing. We adapt all four for LLMs.

The benchmark answers a question that existing evaluations cannot: **where exactly do LLM attention mechanisms break, and do the failure patterns resemble human cognition or reveal fundamentally different processing?**

## 4. Task & Benchmark Construction

Each task isolates one facet of attention using a factorial experimental design with controlled independent variables.

### Task 1: Noise Filtering (Selective Attention)

Grounded in Broadbent's (1958) filter theory of attention and signal detection theory. In humans, selective attention degrades when distractors are semantically similar to the target. We test whether LLMs show the same pattern. Factual passages are embedded within noise at six ratios (1:1 to 100:1 noise-to-signal). Three noise types create distinct filtering demands: **unrelated** noise (different domains), **related** noise (topically similar but irrelevant), and **adversarial** noise (sentences that directly contradict the passage). The key hypothesis: noise *type* matters more than noise *quantity* -- adversarial noise should degrade accuracy at far lower ratios than unrelated noise, mirroring the human finding that semantic similarity between target and distractors drives interference.

**Design:** 10 passages x 4 questions x 3 noise types x 6 ratios = 720 items (subsampled to 36 per run).

### Task 2: Context Switching (Attention Shifting)

Based on the task-switching paradigm (Monsell, 2003). Humans show reliable "switch costs" -- slower and less accurate responses immediately after changing tasks, even with advance warning. We test whether LLMs show an analogous cost despite having no reconfiguration delay. The model receives a 60-item sequence tagged with task cues: [NUMBER], [COUNTRY], or [SPELLING]. Three conditions vary switching frequency: **pure blocks**, **predictable alternation** (ABCABC), and **random switching**. All items include explicit cues, so the model always knows which task to perform. The question is whether switching *itself* imposes a cost -- and if so, whether predictability mitigates it, as it does in humans.

**Design:** 5 sequences x 2 variants x 60 items = 600 items scored across 10 sequences.

### Task 3: Change Blindness (Sustained Attention)

Adapted from Rensink et al. (1997), who showed that humans fail to detect even large visual changes when a brief disruption masks the transient signal. We translate this to text: the model sees two versions of a code snippet or engineering ticket, separated by 0, 1, or 3 unrelated disruptors (standup notes, Slack messages). Changes are either **minor** (a number tweak: `max_retries=3` to `5`), **major** (a logic bug: `raise` to `return {}`), or **none** (control). The code-review framing makes this directly relevant to AI-assisted development: can your AI reviewer catch subtle bugs when distracted by interleaved context?

**Design:** 5 passages x 3 change types x 3 disruptor levels = 45 items.

### Task 4: Mudsplash (Attentional Capture Resistance)

Named after O'Regan et al. (1999), who demonstrated that attention-grabbing "mudsplashes" divert human attention and mask concurrent changes. We test a genuinely novel question: are LLMs susceptible to attentional capture by emotionally salient content? Five scientific passages are shown in two versions with an interlude. The interlude is either **neutral** (bland filler), **emotional** (shocking breaking-news content -- chemical explosions, deadly pathogens), or **task-relevant** (domain-matched commentary containing the exact numbers being changed). LLMs have no amygdala -- if emotional content still disrupts performance, it reveals something unexpected about how these models allocate processing.

**Design:** 5 passages x 3 change types x 3 disruptor types = 45 items.

## 5. Dataset

**Total evaluation items:** 726 across four tasks (36 + 600 + 45 + 45). All data is generated inline within each notebook using fixed random seeds for full reproducibility -- no external data files. Passage domains span code snippets (Python retry logic, LRU caches, rate limiters), engineering tickets (database migrations, search features), and scientific text (volcanology, deep-sea exploration, radio astronomy, glaciology, vaccine trials). Code-based passages were chosen for Change Blindness because they provide unambiguous "ground truth" changes that any reviewer can verify in seconds.

## 6. Technical Details

**Scoring:** No task relies on brittle exact-string matching. Noise Filtering and Context Switching use number normalization and substring matching. Change Blindness and Mudsplash use a two-tier approach: first checking whether both old and new key values appear in the response, then falling back to word-overlap matching (50%+ meaningful-word threshold). NO CHANGE responses are detected via substring matching. This flexible approach ensures that correct answers are credited regardless of phrasing.

**Reasoning model compatibility:** All tasks call `strip_thinking()` to remove `<think>...</think>` tags before scoring, ensuring chain-of-thought reasoning models (e.g., Gemini 2.5 Flash Thinking) are scored on their final answers, not their intermediate reasoning.

**Evaluation framework:** Built on the kaggle-benchmarks SDK. Each notebook defines one `@kbench.task` function and runs `.evaluate()` with the Kaggle-provided LLM. Notebooks are fully self-contained and run independently on Kaggle infrastructure.

## 7. Results, Insights, and Conclusions

[PLACEHOLDER: Noise filtering accuracy curves -- accuracy by noise type x noise ratio.]

**Expected pattern:** Adversarial noise causes steeper accuracy drops than unrelated noise at equivalent ratios. We predict a crossover point where adversarial noise at 10x outperforms unrelated noise at 50x, demonstrating that semantic interference dominates over sheer volume.

[PLACEHOLDER: Context switching cost table -- accuracy by condition (pure/alternating/random).]

**Expected pattern:** Measurable switch cost from pure to random conditions, with predictable alternation falling between. We predict asymmetric costs across task types -- spelling tasks (requiring character-level inspection) may suffer most from switching.

[PLACEHOLDER: Change blindness detection rates -- change type x disruptor count.]

**Expected pattern:** Minor changes show a larger detection drop with increasing disruptors than major changes. At 3 disruptors, we predict minor-change detection falls below 50% while major changes remain above 80%, revealing a severity-dependent attention threshold.

[PLACEHOLDER: Mudsplash capture effect -- detection rate by disruptor type.]

**Expected pattern:** Task-relevant disruptors (containing the exact numbers being changed) cause the largest accuracy drop by creating genuine source confusion. Emotional disruptors may or may not affect LLMs -- either result is informative. If emotional content degrades performance despite LLMs having no affective system, it suggests these models have learned human-like salience weightings from training data.

[PLACEHOLDER: Cross-model comparison -- which models degrade gracefully vs. show cliff-edge failure?]

**So what?** If LLMs show attention failures -- even without a biological attentional bottleneck -- the implications extend beyond benchmarking. For agent architectures, it means that interleaving multiple tool outputs may degrade reasoning quality in ways that are invisible to standard evaluations. For AI-assisted code review, it means that surrounding a subtle bug with enough context can make it effectively invisible to the model. For long-context applications, it means that the *content* of the context window matters as much as its *length*. These findings reframe attention not as a hardware limitation unique to biological brains, but as a fundamental challenge of selective processing that any sufficiently complex information-processing system must confront.

## 8. Organizational Affiliations

Independent researcher.

## 9. References & Citations

- Morris, M. R., et al. (2023). "Levels of AGI: Operationalizing Progress on the Path to AGI." Google DeepMind. arXiv:2311.02462.
- Rensink, R. A., O'Regan, J. K., & Clark, J. J. (1997). "To see or not to see: The need for attention to perceive changes in scenes." *Psychological Science*, 8(5), 368-373.
- O'Regan, J. K., Rensink, R. A., & Clark, J. J. (1999). "Change-blindness as a result of 'mudsplashes'." *Nature*, 398(6722), 34.
- Monsell, S. (2003). "Task switching." *Trends in Cognitive Sciences*, 7(3), 134-140.
- Broadbent, D. E. (1958). *Perception and Communication*. Pergamon Press.
