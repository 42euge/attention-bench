# AttentionBench

## Why This Exists

Current LLM benchmarks conflate attention failures with reasoning failures. When a model gets a question wrong in a long context, is it because it couldn't *find* the relevant information, or because it couldn't *reason* about it? We can't tell — and that matters for understanding where these models actually break down.

AttentionBench isolates the attentional component by holding task difficulty constant. Every question is trivially easy in isolation — a simple factual lookup or pattern match. The only thing that changes is how much irrelevant information surrounds it, or how many repetitions precede it. Any performance degradation is therefore purely attentional, not cognitive.

This is grounded in the cognitive science distinction between **selective attention** (filtering signal from noise, as in the Cocktail Party Effect or Stroop Task) and **sustained attention** (maintaining focus over time, as in vigilance decrement research). Both are well-studied in humans but poorly measured in LLMs. (see research: [[Attention Track]], [[Selective Attention]], [[Sustained Attention]])

## What It Does

AttentionBench produces **186 benchmark items** across two dimensions, designed to answer: *at what point does a model lose attentional focus, and what kind of noise causes it?*

**Dimension 1 — Signal-in-Noise Titration (180 items):** Embeds a short fictional passage with 5 Q&A pairs inside increasing amounts of noise. Measures the **attention threshold** — the noise:signal ratio where accuracy drops below 80%. Three noise types test different failure modes: unrelated filler, same-domain distractors, and adversarial near-answers.

**Dimension 2 — Vigilance Decrement (6 items):** Presents 100 identical, trivially easy subtasks in sequence. Measures whether accuracy degrades as a function of position — do models get sloppy after 50+ repetitions? An "oddball" variant tests inattentional blindness by inserting one different task type mid-sequence.

The key metric isn't pass/fail — it's **where** the model breaks. A model that maintains 100% accuracy at 25:1 noise but drops at 50:1 is meaningfully different from one that drops at 10:1.

## What the Datasets Look Like

### Signal-in-Noise (`data/signal_in_noise.json`)

180 items. Each combines one of 10 fictional passages with a noise configuration:

```json
{
  "task_id": "sin_passage_02_related_r5",
  "dimension": "selective",
  "passage_id": "passage_02",
  "domain": "architecture",
  "noise_type": "related",
  "noise_ratio": 5,
  "num_questions": 5,
  "prompt": "Below is a collection of text passages...[interleaved signal + noise]...\n\nQuestions:\n1. Who designed the Solheim Bridge?\n2. What is the main span length?...",
  "answers": ["Maren Lindqvist", "524 meters", "173 meters", "288", "2.8 billion Norwegian kroner"]
}
```

**The matrix:** 10 passages × 6 noise ratios (1:1, 5:1, 10:1, 25:1, 50:1, 100:1) × 3 noise types = 180 items.

**Noise types differ in what makes them distracting:**
- `unrelated` — Cross-domain filler paragraphs (marine biology noise around an architecture passage)
- `related` — Same-domain content that doesn't answer the questions (other bridges when asking about the Solheim Bridge)
- `adversarial` — Plausible-but-wrong answers to the actual questions (a different architect name, a different span length)

**Prompt construction:** The signal passage is split into ~3-sentence chunks and interleaved with noise chunks. At 1:1 ratio, the prompt is ~3,200 characters. At 100:1 ratio, it balloons to ~123,000 characters — a genuine stress test of context window attention.

**All 10 passages are fictional** across 10 domains (marine biology, architecture, astronomy, chemistry, ancient history, linguistics, geology, music, botany, meteorology). This eliminates training data contamination — a model can't succeed by recalling memorized facts.

### Vigilance (`data/vigilance.json`)

6 items. Three task types, each in normal and oddball variants:

```json
{
  "task_id": "vig_country_identification_normal",
  "dimension": "sustained",
  "task_type": "country_identification",
  "variant": "normal",
  "num_subtasks": 100,
  "prompt": "For each item below, identify the country...\n\nItem 1: The opera house in Mumbai reopened...\nItem 2: The technology startup scene in Tbilisi...\n...",
  "answers": ["India", "Georgia", "Thailand", "Gabon", "Mozambique", ...],
  "oddball_position": null
}
```

**Task types (all trivially easy in isolation):**
| Task | What it asks | Example | Answer |
|------|-------------|---------|--------|
| Country Identification | Name the country from a city/cultural reference | "The opera house in Mumbai reopened..." | India |
| Number Extraction | Pull out the number from a sentence | "Volunteers planted 55,230 trees..." | 55,230 |
| Misspelling Detection | Spot the intentionally misspelled word | "It was sufficent..." | sufficent |

**Oddball variant:** At a random position (40-70), one subtask switches to a different task type. For example, in a country identification sequence, item 48 suddenly asks for a number instead. The prompt warns this might happen. Tests whether the model stays alert or falls into autopilot.

### Manifest (`data/manifest.json`)

Summary metadata:

```json
{
  "benchmark": "AttentionBench",
  "version": "0.1.0",
  "dimensions": {
    "selective": {
      "name": "Signal-in-Noise Titration",
      "count": 180,
      "metric": "attention_threshold (noise ratio at 80% accuracy)"
    },
    "sustained": {
      "name": "Vigilance Decrement",
      "count": 6,
      "metric": "decay_onset (position where accuracy drops below 95%)"
    }
  },
  "total_items": 186
}
```

## Key Concepts

**Attention Threshold** — The noise:signal ratio at which a model's accuracy on the embedded questions drops below 80%. A higher threshold means better selective attention. This is the primary discriminatory metric — we expect meaningful spread across models here. (see research: [[Signal-in-Noise Titration]])

**Vigilance Decrement** — Performance degradation over repeated identical tasks. In humans, this kicks in after 15-20 minutes. In LLMs, we measure it by position within the sequence — does accuracy in items 80-100 differ from items 1-20? (see research: [[Vigilance Decrement]])

**Noise Salience** — Not all distractions are equal. Unrelated noise is easy to filter; adversarial noise (plausible wrong answers) exploits the model's tendency to pattern-match rather than verify. This three-tier design reveals *what kind* of noise each model is vulnerable to. (see research: [[Distractor Salience]])

**Inattentional Blindness** — The oddball task tests whether a model processing 100 identical items will notice when one is different. This is analogous to the "invisible gorilla" experiment in human attention research.

## Architecture

```
src/generate.py    →  data/signal_in_noise.json
(deterministic,       data/vigilance.json
 seeded RNG)          data/manifest.json
                          ↓
src/benchmark.py   →  Kaggle Benchmarks SDK tasks
(task definitions,     (attention_selective, attention_sustained)
 answer checking)         ↓
                      Model evaluation via Kaggle proxy
                          ↓
src/analyze.py     →  Discrimination metrics, accuracy curves
(results analysis)    results/
```

**Data generation** is fully deterministic — same seed produces identical datasets. No external data sources; all content is procedurally generated.

**Answer checking** uses flexible matching: case-insensitive, substring matching, number format normalization (handles commas, spaces). This prevents false negatives from formatting differences.

## Design Decisions

### Decision: Fictional passages only
- **Context:** Need to test whether models can *find* information, not *recall* it from training
- **Choice:** All 10 signal passages are invented (fictional organisms, fictional bridges, etc.)
- **Reasoning:** Eliminates contamination — a model that scores well genuinely attended to the context, not its parametric memory
- **Trade-offs:** Can't test attention on "real" tasks, but this is a feature not a bug for measuring pure attention

### Decision: Interleaved noise placement
- **Context:** Prior work (Lost in the Middle, Liu et al. 2024) showed models have strong positional biases — better at start/end, worse in the middle
- **Choice:** Split signal into chunks and interleave with noise, rather than placing signal as one block
- **Reasoning:** Prevents the model from exploiting positional heuristics. Attention must operate across the full context.
- **Trade-offs:** More complex prompt construction; harder to debug specific failures

### Decision: Three noise types as separate items (not combined)
- **Context:** Could have mixed noise types within a single item
- **Choice:** Each item has exactly one noise type at one ratio
- **Reasoning:** Allows clean attribution — when a model fails, we know *exactly* what kind of noise defeated it. Mixing would confound the signal.
- **Trade-offs:** 3x more items needed for the same passage coverage

### Decision: 100 subtasks per vigilance item
- **Context:** Need enough repetitions to observe decay, but not so many that the prompt exceeds context windows
- **Choice:** 100 subtasks per item (~10K characters)
- **Reasoning:** Sufficient to observe decay patterns (measured in deciles) while fitting comfortably in all frontier model context windows
- **Trade-offs:** May miss very late-onset decay that would appear at 200+ repetitions

## How It Fits In

This repo is one submission to the **Google DeepMind x Kaggle AGI Hackathon**, specifically the **Attention track**. The hackathon asks teams to build benchmarks that isolate specific cognitive abilities of frontier LLMs, based on DeepMind's "Measuring Progress Toward AGI: A Cognitive Framework."

The broader research context (in `../../research/attention/`) includes analysis of existing benchmarks (Needle in a Haystack, BABILong, GSM-DC, Context Rot) and their limitations — all of which motivated the specific design choices here. Key papers that informed the approach:

- **Lost in the Middle (Liu et al., 2024)** — 30%+ accuracy drops based on information position
- **Context Rot (Hong et al., 2025)** — 13.9-85% performance drops with increasing input length on trivial tasks
- **BABILong (Kuratov et al., 2024)** — LLMs utilize only 10-20% of their context window effectively
- **GSM-DC (2025)** — Models sensitive to irrelevant numerical context even when clearly unrelated

## Current Status

**Working:**
- Dataset generation (`src/generate.py`) — produces all 186 items deterministically
- Kaggle Benchmark notebook (`notebooks/kaggle_benchmark.ipynb`) — ready for SDK evaluation
- Analysis tools (`src/analyze.py`) — discrimination metrics and visualization

**In progress / planned:**
- Running evaluations across frontier models to measure discriminatory power
- Writeup for hackathon submission
- Refinement based on initial results (may need to adjust noise ratios or add more passages)
