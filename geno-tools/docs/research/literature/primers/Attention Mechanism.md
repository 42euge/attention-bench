# Attention Mechanism

#primer #literature #math

## Intuition
The attention mechanism lets a model dynamically focus on different parts of its input when producing each output element. Instead of using a fixed representation, the model learns to "attend" to relevant positions — a computational analogue of human selective attention.

## The Math

Scaled dot-product attention:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Where:
- $Q$ = queries (what am I looking for?)
- $K$ = keys (what information is available?)
- $V$ = values (what content to retrieve)
- $d_k$ = key dimension (scaling factor prevents softmax saturation)

Multi-head attention runs $h$ parallel attention functions:
$$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O$$

## Connection to Cognitive Attention
- **Selective attention** ≈ attention weights concentrating on relevant tokens
- **Retrieval heads** (Wu et al. 2024) — <5% of heads handle long-range retrieval
- **Streaming heads** — attend only to recent tokens (recency bias)
- The softmax creates a competition: attending more to one position means less to others

## Where It Shows Up
- [[Retrieval Heads (2024)]] — identifies which heads perform the "attention" function
- [[Positional Bias]] — RoPE encodes position, causing attention decay with distance
- [[Signal-to-Noise Filtering]] — model must attend to signal tokens amid noise

## Links
- Related: [[Signal Detection Theory]], [[Bottleneck Theory]]
