# Multi-Instance Processing Degradation in LLMs (2026)

#paper #literature #sustained-attention

**Authors:** Chen et al.
**Source:** arXiv:2603.22608

## Key Contribution
Tests LLMs on repeated identical tasks (e.g., sentiment analysis of many reviews). Finds slight degradation for 20-100 instances, then PERFORMANCE COLLAPSE at larger counts. Instance count matters more than context length.

## Problem Addressed
Does LLM performance degrade when processing many identical task instances — the sustained attention question?

## Method
- Repeated identical task instances in a single prompt
- Varied instance count from 1 to 500+
- Controlled for context length vs. instance count

## Key Results
- Slight degradation at 20-100 instances
- Catastrophic collapse beyond ~100 instances
- Instance count has stronger effect than context length alone
- Architecture-dependent: Qwen3-4B stable vs. Gemma-3-4B collapses

## Relevance to Our Research
The most directly relevant paper for our vigilance_decrement task. Validates our 100-item design. Suggests we should look for model-specific collapse patterns.

## Links
- Related: [[Vigilance Decrement]], [[Lost in the Middle (2024)]], [[Context Rot (2025)]]
