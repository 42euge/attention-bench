# Noise Filtering Task

#attention #selective-attention #L3 #implementation

Implementation details for the noise_filtering benchmark task in AttentionBench.

## Design
- 10 fictional passages (~200 words each) with 5 factual Q&A pairs
- 6 noise ratios: 1:1, 5:1, 10:1, 25:1, 50:1, 100:1
- 3 noise types: unrelated, related, adversarial
- Total: 180 items (10 × 6 × 3), eval subset: 36 items (2 per config)

## Prompt Structure
Signal passage is chunked into 3-sentence blocks, interleaved with noise paragraphs. Questions appear after the full text block. Model must answer with numbered responses.

## Scoring
- Parse numbered answers from response (handles preamble, think-tags)
- Flexible matching: case-insensitive, substring, number normalization
- Returns (correct, total) tuple per item
- Metric: accuracy by (noise_type, noise_ratio) → attention threshold

## Key Implementation Details
- `strip_thinking()` removes `<think>` blocks from reasoning models
- `parse_numbered_answers()` handles various numbering formats (1. / 1) / 1: / 1-)
- `check_answer()` normalizes numbers, strips qualifiers like "approximately"
- Deterministic generation with seed=42

## Links
- Up: [[Signal-to-Noise Filtering]]
- Related: [[Vigilance Decrement Task]]
