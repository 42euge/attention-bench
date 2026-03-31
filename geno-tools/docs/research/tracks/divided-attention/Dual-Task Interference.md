# Dual-Task Interference

#attention #divided-attention #L1

When humans perform two attention-demanding tasks concurrently, performance on one or both tasks degrades. This is one of the most robust findings in cognitive psychology, explained by capacity theories and bottleneck models.

## In Human Cognition
The psychological refractory period (PRP): when two tasks require responses in quick succession, the second response is delayed. This suggests a central processing bottleneck — some cognitive operations cannot run in parallel.

## LLM Analogue
Give the model two simultaneous tasks within a single prompt: (1) answer comprehension questions about a passage, and (2) count occurrences of a specific word. Compare single-task performance to dual-task performance. The difference is the dual-task cost.

## Key Papers
- Multi-Task Inference (arXiv:2402.11597, 2024): SOTA models can sometimes improve with multi-task prompts, but smaller models degrade
- Multi-Turn Loss (arXiv:2505.06120, 2025): 39% average drop in multi-turn conversations

## Links
- Up: [[Divided Attention]]
- Down: [[Dual-Task Interference Task]]
- Related: [[Attentional Blink]], [[Bottleneck Theory]]
