# Working in This Repo

## Setup

```bash
# Clone and enter
git clone <repo-url> && cd attention-bench

# Create virtual environment
python3 -m venv venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up Kaggle credentials (needed for evaluation, not generation)
cp .env.example .env
# Edit .env with your KAGGLE_USERNAME and KAGGLE_KEY
```

## Running

### Generate the dataset
```bash
python3 src/generate.py
```
Outputs `data/signal_in_noise.json`, `data/vigilance.json`, and `data/manifest.json`. Deterministic — running twice produces identical output.

### Run the benchmark on Kaggle
Upload `notebooks/kaggle_benchmark.ipynb` to Kaggle or use `/gt-upload-kaggle-bench`. The notebook is self-contained: it downloads the generation code, produces data, and runs evaluation.

### Analyze results
```bash
python3 src/analyze.py --results results/<results-file>.json
```

## Common Tasks

### Adding a new passage (Signal-in-Noise)
1. In `src/generate.py`, add to the `PASSAGES` list — a dict with `domain`, `text` (~200 words, fictional), and `questions` (5 Q&A pairs with unambiguous answers)
2. Add corresponding noise content: `related_noise` (same-domain paragraphs) and `adversarial_noise` (plausible wrong answers for each question)
3. Re-run `python3 src/generate.py` to regenerate data
4. The item count will increase by 18 (6 ratios × 3 noise types)

### Adding a new vigilance task type
1. In `src/generate.py`, add a new generator function following the pattern of `generate_country_items()`, `generate_number_items()`, or `generate_misspelling_items()`
2. Register it in the task type list
3. Each task type produces 2 items (normal + oddball), each with 100 subtasks

### Adjusting noise ratios
The ratios `[1, 5, 10, 25, 50, 100]` are defined in `src/generate.py`. Changing these affects all passages uniformly. Consider the prompt size implications — 100:1 already produces ~123K character prompts.

## Conventions

- **All signal content is fictional** — never use real facts that could be in training data
- **Answers must be unambiguous** — single correct answer, no room for interpretation
- **Generation is deterministic** — always use seeded RNG so datasets are reproducible
- **Answer matching is flexible** — case-insensitive, substring, number format normalization. Don't rely on exact string equality.
