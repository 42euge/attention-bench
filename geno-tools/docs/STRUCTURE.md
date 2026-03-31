# Codebase Structure

## Directory Layout

```
attention-bench/
├── src/                        # Core logic
│   ├── generate.py             # Dataset generation — the heart of the repo
│   ├── benchmark.py            # Kaggle Benchmarks SDK task definitions
│   └── analyze.py              # Results analysis and discrimination metrics
├── data/                       # Generated datasets (output of generate.py)
│   ├── signal_in_noise.json    # 180 selective attention items (7.1 MB)
│   ├── vigilance.json          # 6 sustained attention items (66 KB)
│   └── manifest.json           # Dataset metadata summary
├── notebooks/
│   ├── kaggle_benchmark.ipynb  # Main benchmark notebook for Kaggle submission
│   └── explore.ipynb           # Data exploration and visualization
├── results/                    # Evaluation outputs (model scores, analysis)
├── geno-tools/
│   ├── labnotes/               # Development history and task tracking
│   │   ├── tasks.md
│   │   └── notes.md
│   └── docs/                   # This documentation
├── .env.example                # Template for Kaggle API credentials
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview
└── CLAUDE.md                   # AI assistant context and instructions
```

## Key Files

### Data Generation
- **`src/generate.py`** (1,192 lines) — Generates all benchmark data. Contains passage definitions, noise generation logic, vigilance task construction, and prompt assembly. Deterministic with seed. This is where the benchmark's intellectual design is implemented.

### SDK Integration
- **`src/benchmark.py`** — Defines two task types (`attention_selective`, `attention_sustained`) for the kaggle-benchmarks SDK. Handles answer parsing and flexible matching (case-insensitive, substring, number normalization).

### Analysis
- **`src/analyze.py`** — Computes discrimination metrics from evaluation results. Calculates attention thresholds, vigilance decay curves, accuracy by noise type/ratio, and generates visualizations.

### Evaluation
- **`notebooks/kaggle_benchmark.ipynb`** — The notebook submitted to Kaggle. Downloads generate.py, produces datasets, runs evaluation via SDK, and displays results. Self-contained for the Kaggle environment.

## Data Flow

```
[generate.py]
    │
    ├─→ Defines 10 fictional passages (hardcoded, ~200 words each)
    ├─→ Generates 5 Q&A pairs per passage (hardcoded, unambiguous answers)
    ├─→ Generates noise content:
    │     ├─ Unrelated: cross-domain paragraphs + general knowledge filler
    │     ├─ Related: same-domain paragraphs that don't answer the questions
    │     └─ Adversarial: plausible-but-wrong answers to the questions
    ├─→ Assembles prompts at 6 noise ratios (1:1 → 100:1)
    │     └─ Signal chunks interleaved with noise chunks
    ├─→ Generates 3 vigilance task types × 100 subtasks each
    │     └─ Normal variant + oddball variant (different task at random position)
    │
    ▼
[data/*.json]
    │
    ▼
[benchmark.py] ←── Kaggle Benchmarks SDK
    │
    ├─→ Loads items from JSON
    ├─→ Sends prompts to model via Kaggle proxy
    ├─→ Parses model responses (numbered lines)
    ├─→ Scores via flexible answer matching
    │
    ▼
[analyze.py]
    │
    ├─→ Computes attention threshold per passage × noise type
    ├─→ Computes vigilance decay (accuracy by decile)
    ├─→ Generates discrimination metrics across models
    │
    ▼
[results/]
```

## Dependencies

- **kaggle-benchmarks** — Kaggle's SDK for benchmark definition and evaluation. Provides the task registration API and model proxy for running evaluations.
- **matplotlib** — Visualization of accuracy curves and discrimination metrics in analysis.
- **python-dotenv** — Loads Kaggle API credentials from `.env` for notebook execution.
