# Lost in the Middle: How Language Models Use Long Contexts (2024)

#paper #literature #sustained-attention

**Authors:** Liu et al.
**Source:** arXiv:2307.03172 (TACL 2024)

## Key Contribution
Landmark finding: LLMs show U-shaped performance — best when relevant info is at beginning or end, worst in the middle. 30%+ accuracy drops for middle-positioned information.

## Problem Addressed
How do LLMs actually use information across their context window?

## Method
- Multi-document QA: place relevant document at different positions among 20 docs
- Key-value retrieval: vary position of target key-value pair
- Test across multiple models and context lengths

## Key Results
- U-shaped accuracy curve (primacy + recency effects)
- Performance drops 30%+ in middle positions
- Consistent across model families
- Even models with long context windows show this effect

## Limitations
- Doesn't isolate sustained attention from positional encoding bias
- RoPE-based models may show this due to attention decay, not attention failure

## Relevance to Our Research
Major confound for vigilance measurement. Our vigilance_decrement task must control for positional effects. The Multi-Instance Processing paper (Chen 2026) helps by showing instance count matters independently.

## Links
- Related: [[Positional Bias]], [[RULER (2024)]], [[Context Rot (2025)]]
