# Change Blindness Task

#attention #change-detection #L3 #implementation

Implementation details for the change_blindness benchmark task in AttentionBench.

## Design
- 5 passages (solar, marine, archaeology, neuroscience, climate)
- Each has pre-crafted minor and major changes
- 3 disruptor levels: 0, 1, 3 paragraphs
- Control: identical passages (no-change condition for false alarm measurement)
- Total: 5 × (2 change types × 3 disruptor levels + 3 controls) = 45 items

## Prompt Structure
"Read Version A [and interlude] and Version B. What changed?"
- Change items: model must identify the specific detail that changed
- Control items: model must respond "NO CHANGE"

## Scoring
- Returns bool (correct/incorrect)
- For changes: checks if model mentions both old and new values
- For controls: checks if model says "no change"
- Answer normalization: lowercase, whitespace collapse

## Disruptor Pool
3 unrelated paragraphs (board games, Japanese joinery, helium supply) rotated across conditions. Chosen to be topically distant from all 5 passages.

## Links
- Up: [[Textual Change Blindness]]
- Related: [[Noise Filtering Task]], [[Vigilance Decrement Task]]
