# AttentionBench — Explainer Video Transcript

<!-- segment: s01_hook -->
Large language models can reason through complex math, write code, and debate philosophy.

<!-- segment: s02_question -->
But can they focus?

<!-- segment: s03_problem -->
Current benchmarks test what models know, not how they pay attention. A model that aces every question might still fail when the answer is buried in noise, or when it needs to stay focused over a hundred items.

<!-- segment: s04_intro -->
AttentionBench is a cognitive-science-grounded benchmark that measures attention as a distinct cognitive ability in frontier language models.

<!-- segment: s05_four_types -->
We test four types of attention, each adapted from established paradigms in clinical neuropsychology.

<!-- segment: s06_selective -->
Selective attention: can the model filter signal from noise?

<!-- segment: s07_selective_demo -->
In our noise filtering task, a short passage with five factual questions is embedded in progressively larger amounts of noise — from equal parts signal and noise, all the way up to a hundred-to-one noise ratio. Three noise types test different challenges: unrelated filler, related content, and adversarial text with plausible wrong answers.

<!-- segment: s08_sustained -->
Sustained attention: can the model maintain focus over time?

<!-- segment: s09_sustained_demo -->
Our vigilance decrement task presents one hundred trivially easy sub-tasks in a single prompt — identify countries, extract numbers, spot misspellings. Each sub-task is near-perfect in isolation. The question is: does accuracy decay as the model processes more and more items? Using Signal Detection Theory, we decompose performance into sensitivity and response bias.

<!-- segment: s10_divided -->
Divided attention: can the model handle concurrent demands?

<!-- segment: s11_divided_demo -->
The attentional blink task hides two targets in a stream of twenty sentences. By varying the gap between targets, we measure whether models show a temporal recovery period — just like humans do after detecting the first target. The dual-task interference test requires simultaneous comprehension and counting within the same passage.

<!-- segment: s12_change -->
Change detection: can the model notice what changed?

<!-- segment: s13_change_demo -->
Two versions of a passage are presented with a subtle change — a number swap or a causal claim reversal — separated by disruptor paragraphs. In our mudsplash variant, emotionally shocking disruptors test whether salient content captures the model's attention away from the change.

<!-- segment: s14_key_insight -->
The key insight of AttentionBench: we hold task difficulty constant and vary only attentional load.

<!-- segment: s15_conclusion -->
This reveals failure modes invisible to conventional benchmarks. Eight tasks. Four attention types. One question: can your model focus on what matters?
