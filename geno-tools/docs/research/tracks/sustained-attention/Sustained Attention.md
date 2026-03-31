# Sustained Attention

#attention #sustained-attention #L0

Does accuracy decay when LLMs must maintain focus over many repeated sub-tasks? Sustained attention (vigilance) tests whether models show the classic human vigilance decrement — declining performance over prolonged, monotonous tasks.

## Key Concepts
- [[Vigilance Decrement]] — accuracy decline over repeated identical tasks
- [[Positional Bias]] — U-shaped performance curves (lost-in-the-middle)
- [[Monotony and Automaticity]] — performance under underload conditions

## Existing Work
- [[Lost in the Middle (2024)]] — landmark finding on positional degradation
- [[RULER (2024)]] — long-context evaluation revealing effective vs. claimed context size
- [[BABILong (2024)]] — reasoning in long documents
- [[Multi-Instance Processing (2026)]] — instance count matters more than context length
- [[Context Rot (2025)]] — universal degradation across 18 frontier models

## Our Benchmark: Vigilance Decrement
- [[Vigilance Decrement Task]] — 100 identical sub-tasks in a single prompt
- 3 task types × 2 variants (normal + oddball) = 6 items
- Metric: decay onset (position where accuracy drops below 95%)
- Full detail: [[sustained-attention analysis]]

## Links
- Up: [[Research Overview]]
- Down: [[Vigilance Decrement]], [[Positional Bias]], [[Monotony and Automaticity]]
- Related: [[Selective Attention]], [[Divided Attention]]
