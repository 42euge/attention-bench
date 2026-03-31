# Competition Strategy Analysis — Cycle 4

## The 8 Tasks

| # | Task | What it tests | Independent variable | Items |
|---|---|---|---|---|
| 1 | **Noise Filtering** | Extract signal from noise | noise ratio (1x-100x), noise type (unrelated/related/adversarial) | ~36 eval items |
| 2 | **Change Blindness** | Detect changes across interruption | change type (minor/major/none) x disruptor count (0/1/3) | 45 items |
| 3 | **Mudsplash** | Detect changes when disruptor is salient | change type x disruptor type (neutral/emotional/task-relevant) | 45 items |
| 4 | **Attentional Blink** | Dual-target detection at varying lags | lag (1-8 items between T1 and T2) | ~120 items |
| 5 | **Context Switching** | Task-switch cost across task types | condition (pure/alternating/random), 60 items per sequence | 10 sequences |
| 6 | **Continuous Performance** | Sustained target detection (CPT) | 200-item sequence, target freq 15%, lure category | 4 sequences |
| 7 | **Dual-Task Interference** | Concurrent comprehension + counting | single vs dual condition | ~54 items |
| 8 | **Vigilance Decrement** | Accuracy decay over 100 repeated sub-tasks | position in sequence, oddball/SDT variants | multiple sequences |

---

## Q1: Discriminatory Power Ranking

Ranked from most to least likely to show meaningful performance gradients across models:

### Tier 1 — Strong discriminatory power

**1. Noise Filtering** — BEST candidate. Six noise ratios (1x to 100x) across three noise types create an 18-point difficulty grid. Weak models will collapse at lower ratios; strong models will maintain accuracy deeper. The 100x ratio is extreme enough that even frontier models should degrade. The adversarial noise type (domain-relevant confounders) adds a second dimension that tests selective vs. sustained attention differently. This task most cleanly maps difficulty to a continuous parameter.

**2. Context Switching** — Strong candidate. The pure-vs-alternating-vs-random design creates a clean 3-level gradient, and per-task-type analysis within mixed conditions reveals which task types suffer most. Switch costs are well-established in human cognition and the question is whether weaker models show larger costs. The 60-item sequences are long enough to stress the context window. Risk: strong models may show zero switch cost, collapsing the gradient at the top.

**3. Change Blindness** — Good candidate after the latest rewrite (code/ticket passages + relaxed scoring). The 2x3 factorial design (change type x disruptor count) creates a clear gradient. However, the initial Kaggle run showed no disruptor effect — the unrelated standup/Slack/wiki disruptors may be too easy to ignore. Whether the code-passage rewrite fixes this is untested.

### Tier 2 — Moderate discriminatory power

**4. Vigilance Decrement** — Interesting concept but risky. The hypothesis is that accuracy decays over position in a 100-item sequence. If LLMs process all tokens equally (no serial bottleneck), there may be no decrement at all, and the task produces a flat line with no gradient. The SDT and oddball variants add interest but increase complexity.

**5. Mudsplash** — Similar structure to Change Blindness but varies disruptor *type* instead of *count*. The emotional/task-relevant disruptors are the unique hook. Risk: LLMs may be completely immune to emotional content (no amygdala to hijack), producing flat results. Task-relevant disruptors are more promising since they could genuinely confuse the model. If emotional disruptors show no effect, the task loses half its novelty.

**6. Continuous Performance (CPT)** — 200-item YES/NO classification with low target frequency. The d'/sensitivity metric is rigorous, and lure commission rates are interesting. But parsing 200 YES/NO answers reliably is fragile. Risk: parsing failures dominate over genuine attention effects. Also, the task is essentially "classify each sentence" — LLMs may nail this trivially.

### Tier 3 — Weak discriminatory power

**7. Attentional Blink** — The human analogue requires temporal processing constraints that LLMs don't have. LLMs see all items simultaneously in the context — there's no "recovery time" after detecting T1. The lag variable may have no effect at all, producing a flat curve. Unless the specific category-search mechanism creates a genuine interference effect, this task may show ceiling performance across all lags.

**8. Dual-Task Interference** — Comprehension + counting on the same passage. Counting word occurrences ("the", "of") is inherently hard for LLMs regardless of dual-task load, so the single-counting baseline may already be low. The dual-task cost may be swamped by the counting difficulty floor. Also, 3 passages with 4 questions each gives thin statistical power.

---

## Q2: Novelty Ranking

"What can this benchmark tell us about model behavior that we could not see before?"

### Most novel

**1. Mudsplash** — No existing benchmark tests whether emotional/shocking content diverts LLM attention from a factual task. The question "are LLMs susceptible to attentional capture by emotionally salient content?" is genuinely new. Even a null result (they're immune) is an interesting finding about the nature of LLM processing vs. human cognition.

**2. Noise Filtering** — The 100x noise ratio regime is underexplored. Existing needle-in-a-haystack tests use uniform filler; this uses domain-relevant adversarial noise. The question "does noise *type* matter more than noise *quantity*?" has not been systematically studied.

**3. Change Blindness** — Code-review-as-attention-test is clever framing. The practical implication (can your AI code reviewer catch subtle bugs when distracted?) is immediately compelling. The minor-vs-major x disruptor design maps cleanly onto a real capability people care about.

**4. Context Switching** — Switch costs in LLMs are under-studied. The finding that random switching degrades accuracy more than predictable alternation would be novel and practically relevant for multi-tool agent architectures.

### Less novel

**5. Vigilance Decrement** — Position-dependent accuracy in long sequences has been studied via needle-in-a-haystack and "lost in the middle" papers. This adds a new angle (monotonous repeated tasks vs. retrieval) but the territory is partially charted.

**6. Continuous Performance (CPT)** — Signal detection on categorized sentences is essentially a classification task. The SDT framing is standard. Not highly novel.

**7. Attentional Blink** — Without genuine temporal constraints, this tests whether LLMs can find two targets in a list. That's been studied in various retrieval benchmarks.

**8. Dual-Task Interference** — Word counting + comprehension. Word counting is known to be hard for LLMs; dual-task setups have been explored in other benchmarks.

---

## Q3: Should We Cut to 3-4 Tasks?

**Yes. Cut to 4 tasks.**

### Reasoning

1. **Writeup is 1,500 words max.** Eight tasks at ~180 words each leaves zero room for introduction, methodology, insights, or conclusions. Four tasks at ~200 words each leaves ~700 words for framing, results synthesis, and the "what's new" narrative.

2. **Judges evaluate dataset quality at 50%.** Four polished tasks with proven discriminatory power beat eight tasks where half haven't been validated on Kaggle. The review of Change Blindness showed scoring issues — every untested task carries similar risk.

3. **Coherent narrative > breadth.** The writeup needs to answer "what can this benchmark tell us about model behavior that we could not see before?" A focused story about 4 complementary attention facets is more compelling than a survey of 8 loosely related tasks.

4. **Time is limited.** Each task needs Kaggle validation, scoring tuning, and multi-model results. Four tasks done well > eight tasks done poorly.

### The Final Four — Recommended

| Task | Why keep | Attention facet |
|---|---|---|
| **Noise Filtering** | Best discriminatory power, clean gradient, large parameter space | Selective attention (signal/noise separation) |
| **Context Switching** | Strong gradient, practical relevance for agents, well-designed | Attention shifting / cognitive flexibility |
| **Change Blindness** | Novel code-review framing, factorial design, practical relevance | Sustained attention / change detection |
| **Mudsplash** | Most novel question, unique emotional-capture angle | Attentional capture / distraction resistance |

### Why these complement each other

These four map onto the four evaluation targets listed in the track description:
- "Does the model get distracted by irrelevant but salient information?" -> **Mudsplash**
- "Does performance degrade as input length increases?" -> **Noise Filtering** (noise ratio as proxy for irrelevant length)
- "Can the model shift focus across sub-tasks without losing track?" -> **Context Switching**
- "Can it identify key information buried within large amounts of noise?" -> **Noise Filtering** (again) + **Change Blindness**

### What to cut

| Task | Why cut |
|---|---|
| Attentional Blink | LLMs lack temporal processing constraints; likely flat curve |
| Dual-Task Interference | Thin data (3 passages), counting baseline too hard |
| Continuous Performance | 200-item parsing fragility, likely trivial classification |
| Vigilance Decrement | Overlaps with Noise Filtering on sustained attention; may show no decrement |

**If you must keep 5**, add Vigilance Decrement — it's the most defensible of the cut list, and position-dependent accuracy is a clean story if the effect exists.

---

## Q4: What Makes the Writeup Compelling

### Structure (within 1,500 words)

1. **Hook (100 words):** "LLMs process entire prompts at once — they have no attentional bottleneck. Or do they? We designed four tasks that probe whether LLMs exhibit human-like attention failures: missing changes when distracted, losing accuracy when switching tasks, failing to filter noise, and being captured by emotionally salient content."

2. **Task & Benchmark Construction (400 words):** One paragraph per task. Emphasize the cognitive science analogue, the independent variable, and the factorial design. Name-drop the specific paradigms (change blindness, mudsplash, task-switching cost, signal-to-noise ratio).

3. **Dataset (150 words):** Total item counts, generation method (seed-based, reproducible), domain diversity (code snippets, scientific passages, engineering tickets). Mention the code-as-passage choice for Change Blindness — practical relevance to AI code review.

4. **Technical Details (200 words):** Scoring approach per task. Highlight the relaxed scoring (number matching + word overlap) for change detection tasks. Mention strip_thinking for reasoning model compatibility.

5. **Results & Insights (500 words):** This is where you win or lose.
   - Lead with the most dramatic finding (e.g., "accuracy drops 40% at 50x noise ratio with adversarial noise, but only 10% with unrelated noise — noise type matters more than quantity")
   - Show the context-switching cost table
   - Show whether emotional mudsplash content causes capture (even null result is interesting)
   - Compare across models: which models degrade gracefully vs. cliff-edge?
   - End with: "These tasks reveal that LLMs do have attentional limitations — they are not immune to distraction, they do lose accuracy when switching tasks, and they can be overwhelmed by noise. The specific patterns of failure differ from humans in revealing ways."

6. **References (50 words):** Cite the DeepMind AGI framework paper, 2-3 cognitive psychology papers for each paradigm.

### What judges want to see

Based on the evaluation criteria:

- **50% Dataset Quality:** Verifiably correct answers, sufficient sample size, clean code. Make sure every task has a "correct answer" that's unambiguous. Noise Filtering and Context Switching are cleanest here.

- **20% Writeup Quality:** The cognitive-science framing elevates this above "we made some LLM tests." Each task should explicitly state "in human cognition, X happens; we test whether LLMs show analogous X."

- **15% Discriminatory Power:** This is where Noise Filtering shines — show the degradation curve. If you can show different models degrade at different rates, that's the money shot.

- **15% Community Upvotes:** The code-review angle of Change Blindness and the "can LLMs be emotionally distracted?" angle of Mudsplash are the most tweet-able findings. These drive upvotes.

### Key risk

The biggest risk is that tasks that haven't been re-run on Kaggle since redesign may produce flat or broken results. Prioritize getting Kaggle runs for all four final tasks before writing the writeup. The writeup should be driven by actual results, not hypothesized ones.
