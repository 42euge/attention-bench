# Disruption Effects

#attention #change-detection #L2

How does intervening text between two passage versions affect change detection? In our benchmark, we test 0, 1, and 3 disruptor paragraphs.

## Mechanism
Disruptor paragraphs are unrelated content inserted between Version A and Version B. They serve as the textual analogue of the visual "blank" in the flicker paradigm. More disruptors should:
1. Increase the distance between the two versions in the model's context window
2. Add competing information that may overwrite or interfere with the representation of Version A
3. Test whether the model maintains a detailed enough representation to compare against

## False Alarm Rate
Control items present identical passages (Version A twice) with varying disruptors. If models report changes that don't exist, that's a false alarm — indicates the model is guessing rather than carefully comparing.

## Expected Patterns
- 0 disruptors: highest detection (direct comparison possible)
- 1 disruptor: moderate drop (some memory interference)
- 3 disruptors: largest drop (significant interference)
- False alarm rate should increase with more disruptors

## Links
- Up: [[Change Detection]]
- Related: [[Change Magnitude]], [[Positional Bias]]
