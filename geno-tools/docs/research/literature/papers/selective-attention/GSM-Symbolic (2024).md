# GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in LLMs (2024)

#paper #literature #selective-attention

**Authors:** Mirzadeh et al. (Apple)
**Source:** arXiv:2410.05229 (ICLR 2025)

## Key Contribution
Shows LLMs exhibit high variance across symbolic instantiations of the same problem. A single "seemingly relevant but unnecessary" clause causes up to 65% performance drops.

## Problem Addressed
Are LLMs performing genuine reasoning or sophisticated pattern matching?

## Method
- Create symbolic templates of GSM8K problems with variable names/numbers
- Test with and without distractors (one added clause)
- Evaluate across SOTA models

## Key Results
- Up to 65% performance drops from a single distractor clause
- High variance across instantiations suggests pattern-matching, not reasoning
- Even frontier models are vulnerable

## Relevance to Our Research
Demonstrates that adversarial noise (plausible but unnecessary context) is the hardest filtering challenge — directly motivating our adversarial noise type.

## Links
- Related: [[GSM-IC (2023)]], [[Adversarial Noise]], [[Distractor Robustness]]
