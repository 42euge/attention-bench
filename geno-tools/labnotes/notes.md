# Lab Notes

## 2026-03-21 — Repo setup complete

Set up project skeleton with:
- `requirements.txt` (pandas, numpy, python-dotenv; SDK installed from source)
- `.env.example` with Kaggle model proxy config
- `src/benchmark.py` — task definition scaffold using kaggle-benchmarks SDK
- `src/generate.py` — dataset generation scaffold
- `src/analyze.py` — results analysis with discrimination metrics
- Updated README with setup instructions
- Updated `.gitignore` for venv, SDK clone, and benchmark artifacts

Key SDK notes: no PyPI package — must clone from github.com/Kaggle/kaggle-benchmarks and `pip install -e`. On Kaggle notebooks it's pre-installed. Tasks use `@kbench.task()` decorator, evaluation via `.evaluate()` with a DataFrame.

## 2026-03-21 — Benchmark concept selected: AttentionBench

### Decision

Combining two complementary attention concepts into a single unified benchmark:

1. **Signal-in-Noise Titration** (Selective Attention)
2. **Vigilance Decrement** (Sustained Attention)

### Rationale

- These two dimensions test **distinct, complementary** attention faculties — filtering distractions vs. maintaining focus over repetition.
- Both hold **task difficulty constant** so any performance degradation is purely attentional, not a reasoning failure.
- Each dimension yields a **single clear metric**: attention threshold (noise ratio at 80% accuracy) and decay onset position.
- Procedurally generated content makes the benchmark **contamination resistant**.
- High expected **discriminatory power** across frontier models — models likely vary in both noise tolerance and sustained focus.

### Dimension 1: Signal-in-Noise Titration

- Fixed ~200-word passage + 5 factual questions, embedded in increasing noise.
- Noise ratios: 1:1, 5:1, 10:1, 25:1, 50:1, 100:1.
- Noise types: (a) unrelated filler, (b) topically related, (c) adversarial near-miss.
- Noise placements: before, after, interleaved, surrounding.
- **Metric:** attention threshold — the noise ratio at which accuracy drops below 80%.

### Dimension 2: Vigilance Decrement

- 50–100 identical trivially-easy sub-tasks in a single prompt.
- Task types: country identification, number extraction, misspelling detection.
- **Metric:** decay onset position, accuracy-by-position curve.
- Oddball variant: one unexpected task type inserted at a random position.

### Benchmark hypothesis

"What can this benchmark tell us about model behavior that we could not see before?"

→ AttentionBench reveals **where and how** models lose attentional focus — whether from environmental noise (selective) or repetitive load (sustained). Current benchmarks conflate attention failures with reasoning failures; by holding task difficulty constant, we isolate the attentional component. This lets us answer: *Can models both filter distractions AND maintain focus over extended tasks?*

## 2026-03-21 — Benchmark hypothesis formalized

The concept selection entry above includes the full hypothesis. Key framing:
- **Null hypothesis:** LLM performance on factual questions is independent of surrounding noise volume and task repetition count.
- **Alternative:** Performance degrades as a function of noise ratio (selective) and task position (sustained), with the degradation profile varying across models.
- **Novel signal:** Separating attentional failure from reasoning failure by holding task difficulty constant.

## 2026-03-21 — Task types designed & dataset built

### Signal-in-Noise (180 items)
- 10 fictional passages (~200 words each) across 10 domains
- 5 factual Q&A per passage with unambiguous short answers
- All content fictional for contamination resistance
- 6 noise ratios × 3 noise types = 18 variants per passage
- Noise types: unrelated (cross-domain filler), related (same domain, different facts), adversarial (plausible wrong answers)
- Interleaved placement (noise chunks alternating with passage chunks)
- Prompt size range: 2.8K–129K characters

### Vigilance Decrement (6 items)
- 3 task types: country identification, number extraction, misspelling detection
- 100 sub-tasks per item, each trivially easy in isolation
- Normal variant + oddball variant (unexpected task type at random position 40–70)
- Oddball tests inattentional blindness under repetitive load

### Noise generation approach
- Unrelated: other passages + 15 dedicated filler paragraphs (diverse topics)
- Related: 1 same-domain paragraph per passage (10 total)
- Adversarial: 1 paragraph per passage with plausible-but-wrong answers (10 total)
- High ratios (50:1, 100:1) cycle through noise pool — repetition is acceptable

### SDK integration
- `attention_selective` task: returns (correct, 5) per SIN item
- `attention_sustained` task: returns (correct, 100) per vigilance item
- Answer checking: case-insensitive substring match + number format normalization
- Evaluation via `.evaluate()` with prepared DataFrames
