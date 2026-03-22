# AttentionBench

Kaggle benchmark for the **Attention** track of the Google DeepMind x Kaggle AGI Hackathon.

**Can models both filter distractions AND maintain focus over extended tasks?**

## What it measures

AttentionBench isolates two distinct attention faculties by holding task difficulty constant — any performance degradation is purely attentional, not a reasoning failure.

### Dimension 1: Signal-in-Noise Titration (Selective Attention)

A fixed ~200-word passage with 5 factual questions is embedded in progressively larger amounts of noise. Three noise types test different filtering challenges:

- **Unrelated** — random cross-domain filler text
- **Related** — same-domain content that doesn't answer the questions
- **Adversarial** — text containing plausible-but-wrong answers

Noise ratios: 1:1, 5:1, 10:1, 25:1, 50:1, 100:1

**Metric:** Attention threshold — the noise ratio at which accuracy drops below 80%.

### Dimension 2: Vigilance Decrement (Sustained Attention)

100 identical, trivially easy sub-tasks in a single prompt. Three task types:

- Country identification
- Number extraction
- Misspelling detection

Plus oddball variants with one unexpected task type at a random position.

**Metric:** Decay onset — the position where accuracy drops below 95%.

## Dataset

- 180 Signal-in-Noise items (10 passages × 6 ratios × 3 noise types)
- 6 Vigilance items (3 task types × normal/oddball)
- All passages are fictional for contamination resistance
- Generated deterministically from `src/generate.py`

## Setup

```bash
# Clone the kaggle-benchmarks SDK
git clone https://github.com/Kaggle/kaggle-benchmarks.git
pip install -e ./kaggle-benchmarks

# Install project dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MODEL_PROXY_API_KEY

# Generate dataset
python3 src/generate.py
```

Or use a [Kaggle notebook](https://www.kaggle.com/benchmarks/tasks/new) where the SDK is pre-installed.

## Structure

- `src/generate.py` — dataset generation (passages, noise, vigilance tasks)
- `src/benchmark.py` — task definitions using kaggle-benchmarks SDK
- `src/analyze.py` — results analysis & discrimination metrics
- `data/` — generated dataset files
- `results/` — model evaluation outputs
