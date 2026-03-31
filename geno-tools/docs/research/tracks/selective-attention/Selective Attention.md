# Selective Attention

#attention #selective-attention #L0

Can LLMs filter relevant information from noise? Selective attention tests whether models can extract signal when it's buried in distracting, misleading, or adversarial context — the cognitive equivalent of the cocktail party effect.

## Key Concepts
- [[Signal-to-Noise Filtering]] — extracting answers from noise-embedded passages
- [[Distractor Robustness]] — maintaining reasoning when irrelevant context is added
- [[Adversarial Noise]] — handling plausible-but-wrong competing information

## Existing Work
- [[GSM-IC (2023)]] — math with irrelevant context (Shi et al.)
- [[GSM-Symbolic (2024)]] — symbolic variations + distractors (Mirzadeh et al.)
- [[CogniLoad (2025)]] — cognitive load theory grounded benchmark
- [[Needle in a Haystack]] — information retrieval in long context

## Our Benchmark: Noise Filtering
- [[Noise Filtering Task]] — 10 passages × 6 noise ratios × 3 noise types
- Metric: attention threshold (noise ratio at 80% accuracy)
- Full detail: [[selective-attention analysis]]

## Links
- Up: [[Research Overview]]
- Down: [[Signal-to-Noise Filtering]], [[Distractor Robustness]], [[Adversarial Noise]]
- Related: [[Sustained Attention]], [[Change Detection]]
