# Bottleneck Theory

#attention #divided-attention #L1

The idea that certain cognitive operations have limited capacity and create processing bottlenecks when multiple tasks compete for the same resources.

## Classical Models
- **Early selection** (Broadbent 1958): filter applied before semantic processing
- **Late selection** (Deutsch & Deutsch 1963): all stimuli processed, filter at response
- **Capacity theory** (Kahneman 1973): shared pool of attention resources
- **Central bottleneck** (Pashler 1994): response selection is serial

## LLM Relevance
Transformer models process all tokens in parallel via self-attention, but:
- Generation is autoregressive (inherently serial at output)
- Attention heads have finite capacity per layer
- The "retrieval head" finding (Wu et al. 2024, arXiv:2404.15574) shows <5% of attention heads handle long-range retrieval — a potential bottleneck

## Testing Predictions
If LLMs have attention bottlenecks, dual-task interference should show:
- Asymmetric costs (one task suffers more than the other)
- Cost that scales with task difficulty
- Architecture-dependent effects (different models, different bottlenecks)

## Links
- Up: [[Divided Attention]]
- Related: [[Dual-Task Interference]], [[Attentional Blink]]
