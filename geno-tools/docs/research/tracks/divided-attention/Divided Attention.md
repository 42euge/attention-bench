# Divided Attention

#attention #divided-attention #L0

Can LLMs split focus across concurrent demands without interference? Divided attention tests whether models can perform multiple tasks simultaneously — detecting targets in rapid sequences (attentional blink) and performing comprehension + counting concurrently (dual-task interference).

## Key Concepts
- [[Attentional Blink]] — temporal recovery after detecting a first target
- [[Dual-Task Interference]] — performance cost of concurrent task demands
- [[Bottleneck Theory]] — serial processing limitations in parallel task execution

## Existing Work
- [[Multi-Task Inference (2024)]] — can LLMs follow multiple instructions at once?
- [[Multi-Turn Conversation Loss (2025)]] — 39% performance drop in multi-turn vs single-turn
- Limited direct testing of divided attention in LLMs

## Our Benchmarks
- [[Attentional Blink Task]] — dual-target detection across lags 1-8
- [[Dual-Task Interference Task]] — comprehension + counting simultaneously
- Full detail: [[divided-attention analysis]]

## Links
- Up: [[Research Overview]]
- Down: [[Attentional Blink]], [[Dual-Task Interference]], [[Bottleneck Theory]]
- Related: [[Selective Attention]], [[Sustained Attention]]
