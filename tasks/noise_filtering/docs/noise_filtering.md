# Noise Filtering

## What it tests

Can the model extract correct answers from a passage when it is progressively buried in irrelevant text? This tests selective attention — the ability to filter signal from noise at increasing noise-to-signal ratios.

## The setup

Factual passages (science, engineering, linguistics, etc.) are embedded in noise paragraphs. The model must answer comprehension questions about the passage despite the surrounding noise.

Three noise types test different filtering demands:

- **Unrelated** — random facts from completely different domains (easy to ignore)
- **Related** — topically similar but irrelevant sentences (harder to filter)
- **Adversarial** — sentences that directly contradict claims in the passage (designed to mislead)

Six noise ratios control difficulty: **1:1, 5:1, 10:1, 25:1, 50:1, 100:1** (noise words per signal word). At 100:1, the passage is buried in 100x its own length of noise text.

## What to expect when you run it

The notebook outputs an accuracy table: **noise type** (unrelated, related, adversarial) x **noise ratio** (1, 5, 10, 25, 50, 100).

**Good results look like:**
- High accuracy at low ratios (1:1, 5:1) across all noise types — the model can find the passage
- Gradual accuracy drop as ratio increases — that is the filtering threshold
- Unrelated noise should be easiest to ignore; adversarial should cause the steepest drop
- The "attention threshold" metric reports the highest ratio where the model still hits 80%+ accuracy

**What discriminates models:**
- Weak models lose accuracy even at 5:1 with adversarial noise
- Strong models maintain accuracy deep into 25:1 or 50:1
- The interesting signal is the **gap between noise types** — does adversarial noise hurt more than unrelated? How much?

**Metrics printed:**
- Accuracy by noise type x noise ratio (the main table)
- Per-noise-type accuracy curves
- Attention threshold per noise type (highest ratio at 80%+ accuracy)

**Plot:** Line chart showing accuracy vs noise ratio for each noise type.

## Design

10 passages x 4 questions each x 3 noise types x 6 noise ratios = **720 items total** (subsampled to 2 per config for evaluation = 36 items per run).

Scoring checks if the model's answer contains the expected value (with number normalization and substring matching).
