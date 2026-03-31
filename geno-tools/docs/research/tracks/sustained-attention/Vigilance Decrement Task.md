# Vigilance Decrement Task

#attention #sustained-attention #L3 #implementation

Implementation details for the vigilance_decrement benchmark task in AttentionBench.

## Design
- 100 identical, trivially easy sub-tasks in a single prompt
- 3 task types: country identification, number extraction, misspelling detection
- 2 variants per type: normal (all same) + oddball (one unexpected task at random position 40-70)
- Total: 6 items, each containing 100 sub-tasks

## Task Types
1. **Country ID** — sentence mentions a city, answer with the country (from 98 city-country pairs)
2. **Number extraction** — extract the number from a sentence (20 context templates)
3. **Misspelling detection** — identify the misspelled word (50 misspelling pairs, 20 templates)

## Scoring
- Parse 100 numbered answers per response
- Flexible matching: case-insensitive, substring, number normalization
- Returns (correct, total) tuple
- Key analysis: accuracy by decile position (1-10, 11-20, ..., 91-100)

## Oddball Variant
One sub-task at a random position (40-70) is a different task type. Tests whether the model notices and correctly handles the unexpected item. The prompt includes a note about possible task-type changes.

## Expected Patterns
- Accuracy should be near-perfect for early positions
- Degradation expected in later positions (especially 70-100)
- Oddball detection rate expected to decrease with later position
- Error types: drift, skipping, off-by-one, adjacent copying, format degradation

## Links
- Up: [[Vigilance Decrement]]
- Related: [[Noise Filtering Task]], [[Attentional Blink Task]]
