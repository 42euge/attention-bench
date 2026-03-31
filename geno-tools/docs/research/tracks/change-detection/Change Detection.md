# Change Detection

#attention #change-detection #L0

Can LLMs spot factual changes between two versions of a passage when separated by a disruption? Change blindness — failing to notice changes during brief interruptions — is one of the most striking demonstrations of attention limitations in human cognition. No existing benchmark tests this in LLMs.

## Key Concepts
- [[Textual Change Blindness]] — failing to detect modifications across a disruption
- [[Change Magnitude]] — minor detail changes vs. major causal claim changes
- [[Disruption Effects]] — how intervening text impairs change detection

## Existing Work
- No benchmark directly tests change blindness in LLMs (major gap)
- Adjacent: [[GSM-IC (2023)]], consistency/hallucination benchmarks, perturbation studies
- Closest cognitive science paradigm: Rensink et al. (1997) flicker paradigm

## Our Benchmark: Change Blindness
- [[Change Blindness Task]] — 5 passages × 2 change types × 3 disruptor levels + controls
- Metric: detection rate by change magnitude and disruption level
- Full detail: [[change-detection analysis]]

## Links
- Up: [[Research Overview]]
- Down: [[Textual Change Blindness]], [[Change Magnitude]], [[Disruption Effects]]
- Related: [[Selective Attention]], [[Sustained Attention]]
