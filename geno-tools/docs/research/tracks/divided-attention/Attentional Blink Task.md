# Attentional Blink Task

#attention #divided-attention #L3 #implementation

Implementation details for the attentional_blink benchmark task in AttentionBench.

## Design
- Stream of 20 sentences per item
- T1 and T2 from different semantic categories (animals/cities/foods)
- Distractors from cross-domain topics (science, history, technology)
- Lags 1-8 (items between T1 and T2)
- 3 category pairs × 5 T1 variants × 8 lags = up to ~120 items

## Prompt Structure
"Below is a rapid stream of sentences. Two belong to specific categories: one about {cat1} (T1) and one about {cat2} (T2). Identify both targets."
Response format: T1: <verbatim> / T2: <verbatim>

## Scoring
- Parse T1 and T2 from response
- Substring matching (case-insensitive)
- Returns (correct, 2) where correct ∈ {0, 1, 2}
- Key analysis: T2|T1 accuracy as function of lag

## Expected Blink Curve
- If blink exists: T2 accuracy dips at lags 2-5, recovers at 6-8
- Lag-1 sparing: paradoxically high T2 accuracy at lag 1
- Blink magnitude: max accuracy drop from baseline

## Links
- Up: [[Attentional Blink]]
- Related: [[Dual-Task Interference Task]], [[Change Blindness Task]]
