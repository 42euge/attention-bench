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

## 2026-03-22 — Kaggle Benchmark Run v4 (Multi-Model)

- **Task**: `eugenio0/new-benchmark-task-0def0` (v4)
- **Status**: ERROR (evaluation completed, summary cell crashed)
- **Runtime**: 70 minutes (4,184 seconds)
- **Total LLM calls**: 1,134 (972 SIN + 162 vigilance)
- **Tokens**: 1,449,844 input + 119,678 output (SIN only)
- **Config**: 36 SIN items (MAX_ITEMS_PER_CONFIG=3, SKIP_HIGH_RATIOS=True, max ratio 25:1) + 6 vigilance items
- **Results saved**: `results/v4_multi_model/` (500 run JSON files + log)

### Available Models (27)

**Anthropic (7):** claude-haiku-4-5, claude-opus-4-1, claude-opus-4-5, claude-opus-4-6, claude-sonnet-4, claude-sonnet-4-5, claude-sonnet-4-6
**DeepSeek (3):** deepseek-r1-0528, deepseek-v3.1, deepseek-v3.2
**Google (10):** gemini-2.0-flash, gemini-2.0-flash-lite, gemini-2.5-flash, gemini-2.5-pro, gemini-3-flash-preview, gemini-3-pro-preview, gemini-3.1-flash-lite-preview, gemini-3.1-pro-preview, gemma-3-1b, gemma-3-4b, gemma-3-12b, gemma-3-27b
**Qwen (4):** qwen3-235b-a22b-instruct-2507, qwen3-coder-480b-a35b-instruct, qwen3-next-80b-a3b-instruct, qwen3-next-80b-a3b-thinking
**Other (1):** glm-5

### SIN Results — Overall Accuracy by Model

| Model | Accuracy | Imperfect Runs | Avg Latency |
|---|---|---|---|
| claude-opus-4-1 | 100.0% | 0/19 | 2,429ms |
| claude-opus-4-5 | 100.0% | 0/19 | 1,616ms |
| claude-opus-4-6 | 100.0% | 0/19 | 1,994ms |
| claude-sonnet-4-5 | 100.0% | 0/19 | 1,637ms |
| claude-sonnet-4-6 | 100.0% | 0/19 | 1,785ms |
| gemini-3.1-flash-lite-preview | 100.0% | 0/18 | 971ms |
| gemini-3.1-pro-preview | 100.0% | 0/18 | 19,484ms |
| qwen3-next-80b-a3b-instruct | 100.0% | 0/18 | 422ms |
| glm-5 | 100.0% | 0/18 | 24,454ms |
| claude-haiku-4-5 | 98.9% | 1/19 | 848ms |
| claude-sonnet-4 | 98.9% | 1/19 | 1,791ms |
| deepseek-v3.1 | 98.9% | 1/19 | 1,087ms |
| deepseek-v3.2 | 98.9% | 1/19 | 1,574ms |
| gemini-3-flash-preview | 98.9% | 1/18 | 5,337ms |
| gemini-3-pro-preview | 98.9% | 1/18 | 12,225ms |
| qwen3-235b-a22b-instruct | 98.9% | 1/18 | 518ms |
| gemma-3-27b | 97.8% | 1/18 | 1,821ms |
| gemini-2.0-flash | 96.8% | 3/19 | 771ms |
| gemini-2.0-flash-lite | 96.8% | 1/19 | 798ms |
| qwen3-coder-480b | 96.7% | 3/18 | 422ms |
| gemini-2.5-flash | 95.8% | 4/19 | 5,245ms |
| gemini-2.5-pro | 93.7% | 5/19 | 12,538ms |
| gemma-3-12b | 92.2% | 5/18 | 4,059ms |
| qwen3-thinking | 91.1% | 8/18 | 19,289ms |
| gemma-3-4b | 84.4% | 8/18 | 1,739ms |
| gemma-3-1b | 62.2% | 16/18 | 1,304ms |
| deepseek-r1-0528 | 1.1%* | 19/19 | 5,473ms |

*DeepSeek R1 accuracy is artificially 1.1% due to parsing bug — see below.

### SIN Thresholds (80% accuracy cutoff)

Most models hit 25:1 across all noise types (our max tested ratio). Differentiation only appears in smaller/weaker models:

| Model | Unrelated | Related | Adversarial |
|---|---|---|---|
| gemma-3-1b | 5:1 | 10:1 | **0:1** |
| gemma-3-4b | 25:1 | 25:1 | **1:1** |
| gemma-3-12b | 25:1 | 25:1 | **10:1** |
| gemini-2.0-flash-lite | 25:1 | 25:1 | **5:1** |
| All other models | 25:1 | 25:1 | 25:1 |

### Critical Bugs Found

1. **`<think>` tag parsing bug**: DeepSeek R1 (and partially Qwen3-thinking) use `<think>...</think>` chain-of-thought blocks. Our `parse_numbered_answers` function parses the thinking text as answers instead of stripping it first. R1's actual answers after `</think>` are correct. **Must fix before next run.**

2. **Summary cell TypeError**: `TypeError: '<' not supported between instances of 'OpenAI' and 'OpenAI'` — the `model_col` in the results DataFrame contains LLM proxy objects, not strings. The `unique()` call works but sorting/comparison fails. **Fix: convert model column to string.**

3. **No vigilance run files saved**: Only SIN `.run.json` files were output (500 files). Vigilance results were computed (162 results logged) but not serialized — likely the error in the summary cell prevented the vigilance task from writing output files, or the SDK doesn't serialize vigilance runs to separate files.

### Key Insights

1. **Ceiling effect at 25:1**: Most frontier models (20/27) hit 100% or near-100% at our max tested ratio. We're **not testing hard enough**. Must include 50:1 and 100:1 ratios to find where models break.

2. **Adversarial noise is the discriminator**: The only noise type that creates separation among frontier models is adversarial (plausible-but-wrong answers). Unrelated and related noise barely affect any model.

3. **Model size matters for adversarial**: Clear scaling trend in Gemma family: 1b (0:1) < 4b (1:1) < 12b (10:1) < 27b (25:1). This is the discriminatory power we're looking for.

4. **Thinking models need special handling**: Both DeepSeek R1 and Qwen3-thinking produce chain-of-thought that breaks our parser. This is a systematic bias against reasoning models.

5. **Speed vs accuracy tradeoff visible**: Fastest models (qwen3 ~422ms, gemini-2.0-flash ~771ms) aren't always most accurate. Slowest (glm-5 ~24s, gemini-3.1-pro ~19s) are 100% but at 30-50x latency cost.

### Next Run Changes

- [ ] **Strip `<think>` blocks** before parsing answers
- [ ] **Convert model column to string** in summary cell (fix TypeError)
- [ ] **Include 50:1 and 100:1 ratios** (set SKIP_HIGH_RATIOS=False) — this is where discrimination lives
- [ ] **Increase MAX_ITEMS_PER_CONFIG** to at least 5 for statistical significance
- [ ] **Save vigilance data** explicitly (write to JSON in a separate cell before summary)
- [ ] **Add model name as string** to results merge, not LLM object
