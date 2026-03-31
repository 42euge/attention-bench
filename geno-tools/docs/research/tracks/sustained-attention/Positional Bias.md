# Positional Bias

#attention #sustained-attention #L1

LLMs show systematic performance variation based on where information appears in the context — the "lost in the middle" phenomenon — which confounds sustained attention measurement.

## The U-Curve
Liu et al. (2024, arXiv:2307.03172) showed that when relevant information is placed at different positions in a long context, performance follows a U-shape: best at the beginning (primacy) and end (recency), worst in the middle. 30%+ accuracy drops for middle-positioned information.

## Mitigations
- Ms-PoE (Zhang et al. 2024, NeurIPS) — multi-scale positional encoding to reduce bias
- STRING (arXiv:2406.02536) — manipulates single hidden-state dimension
- Found in the Middle (arXiv:2403.04797) — RoPE adjustment for better middle-context use

## Implications for Sustained Attention
Positional bias is a CONFOUND for vigilance measurement. If sub-task accuracy drops at position 50-70, is that vigilance decrement or middle-position degradation? The multi-instance processing paper (Chen et al. 2026) shows instance count matters independently of context length — a critical finding.

## Links
- Up: [[Sustained Attention]]
- Related: [[Vigilance Decrement]], [[Lost in the Middle (2024)]]
