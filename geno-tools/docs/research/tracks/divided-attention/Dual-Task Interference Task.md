# Dual-Task Interference Task

#attention #divided-attention #L3 #implementation

Implementation details for the dual_task_interference benchmark task in AttentionBench.

## Design
- 3 passages (fusion reactor, ocean cleanup, quantum computing)
- 4 comprehension questions per passage
- 2 counting targets per passage (common words: "the", "of")
- 3 conditions: single_comprehension, single_counting, dual (both)
- Total: 12 single-comp + 6 single-count + 24 dual = 42 items

## Scoring
- Single comprehension: (0 or 1, 1) — answer match
- Single counting: (0 or 1, 1) — count within ±1
- Dual: (0-2, 2) — score both answer and count
- Dual-task cost = single accuracy − dual accuracy

## Response Parsing
- `extract_answer()`: finds "Answer: ..." pattern
- `extract_count()`: finds "Count: N" or "N occurrences/times"
- Both strip thinking tags first

## Expected Patterns
- Single tasks should be near-ceiling for frontier models
- Dual-task should show measurable cost
- Asymmetric interference: counting likely suffers more than comprehension
- Model-dependent: some architectures may handle dual-task better

## Links
- Up: [[Dual-Task Interference]]
- Related: [[Attentional Blink Task]], [[Noise Filtering Task]]
