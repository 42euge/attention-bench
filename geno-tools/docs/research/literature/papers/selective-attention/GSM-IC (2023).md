# GSM-IC: Large Language Models Can Be Easily Distracted by Irrelevant Context (2023)

#paper #literature #selective-attention

**Authors:** Shi et al.
**Source:** arXiv:2302.00093 (ICML 2023)

## Key Contribution
Introduces GSM-IC (Grade School Math with Irrelevant Context) showing that adding irrelevant sentences to math problems causes dramatic performance drops in LLMs.

## Problem Addressed
Do LLMs actually reason through math problems, or are they pattern-matching? Adding irrelevant context tests robustness of reasoning.

## Method
- Take GSM8K problems and insert 1-2 irrelevant sentences
- Test across multiple LLMs
- Propose mitigations: self-consistency decoding, explicit "ignore irrelevant info" instructions

## Key Results
- 20-40% accuracy drops from adding irrelevant context
- Models attend to distractors even when they're semantically distant
- Self-consistency helps but doesn't fully mitigate

## Limitations
- Only math domain; unclear if findings generalize to QA, summarization
- Irrelevant sentences are clearly off-topic — adversarial/related noise not tested

## Relevance to Our Research
Foundational evidence that LLMs lack selective attention. Our noise_filtering task extends this by testing 3 noise types at 6 intensity levels with non-math content.

## Links
- Related: [[GSM-Symbolic (2024)]], [[Distractor Robustness]], [[CogniLoad (2025)]]
