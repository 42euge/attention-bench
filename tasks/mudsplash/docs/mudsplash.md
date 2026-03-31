# Mudsplash

## What it tests

Are LLMs susceptible to attentional capture? When emotionally salient or semantically confusing content appears between two versions of a passage, does the model fail to notice factual changes?

This directly parallels the "mudsplash" paradigm in visual cognition research: attention-grabbing stimuli presented simultaneously with a change cause humans to miss the change entirely.

## The setup

Five fictional but realistic scientific passages (volcano monitoring, deep-sea submarine expedition, radio telescope discovery, glacier ice cores, malaria vaccine trial). Each passage is dense with specific numbers and factual claims.

Between Version A and Version B, one of three **disruptor types** is inserted as an interlude:

- **Neutral** -- bland factual filler (shipping containers, composting programs, library cataloguing). Baseline condition.
- **Emotional** -- shocking breaking-news content (chemical plant explosion, school bus crash, deadly pathogen). Tests whether emotional salience pulls attention away from the comparison task.
- **Task-relevant** -- passage-matched scientific commentary that discusses the same domain and includes the exact numbers being changed. Tests whether semantic interference causes the model to confuse the disruptor's claims with the passage content.

Three **change types** per passage:

- **Minor** -- a single number swap (e.g., "47 micro-tremors" to "23 micro-tremors")
- **Major** -- a semantic contradiction (e.g., "unique ecosystem of 156 species" to "completely barren")
- **None** -- identical passages (control for false alarms)

## What to expect when you run it

The notebook outputs a table: **change type** (minor, major, none) x **disruptor type** (neutral, emotional, task-relevant).

**Good results look like:**
- `none` row should be ~100% -- model correctly says NO CHANGE when nothing changed
- `major` should be higher than `minor` -- semantic contradictions are easier to spot than number swaps
- Neutral disruptors should yield the highest detection rate (baseline)
- Emotional and task-relevant disruptors should show a **drop** from baseline -- that is the attentional capture effect
- Task-relevant disruptors should cause the largest drop, since they create semantic interference with the exact values being compared

**What discriminates models:**
- Weak models miss minor changes even with neutral disruptors
- Strong models maintain detection across all disruptor types
- The key signal is the **delta** from neutral to emotional/task-relevant -- how much does attentional capture degrade performance?
- False alarm rate with task-relevant disruptors (saying something changed when it didn't, confused by the disruptor's claims) is an especially revealing metric

**Metrics printed:**
- Detection rate by change type x disruptor type (the main table)
- Attentional capture effect: accuracy drop from neutral to emotional and task-relevant, per change type
- False alarm rate by disruptor type

**Plot:** Grouped bar chart showing detection rate for minor/major changes and false alarm rate, across the three disruptor types.

## Design

5 passages x 3 change types (minor, major, none) x 3 disruptor types (neutral, emotional, task-relevant) = **45 items total**.

Task-relevant disruptors are passage-matched: each one discusses the same scientific domain as its target passage and deliberately includes the exact numbers that are being changed (e.g., the volcano disruptor mentions both "23" and "47" tremors). This maximizes semantic interference rather than just topical adjacency.

Scoring uses a two-tier approach: first checks if both the old and new key numbers appear in the response, then falls back to word overlap matching (at least 50% of meaningful words from each side of the change). NO CHANGE responses are matched by substring.
