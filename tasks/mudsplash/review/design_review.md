# Mudsplash -- Design Review

**Reviewer:** Claude Opus 4.6 (Cycle 6 Implementer)
**Date:** 2026-03-31

## Summary

Mudsplash is the most novel task in the benchmark suite. It tests attentional capture -- whether emotionally salient or semantically confusing disruptors cause LLMs to miss factual changes between two passage versions. The concept maps directly to the visual cognition "mudsplash" paradigm (O'Regan et al., 1999).

## Passage Quality: Strong

The 5 passages cover diverse scientific domains (volcanology, oceanography, radio astronomy, glaciology, epidemiology). Each is fictional but realistic, with:
- Named researchers and specific institutions
- Multiple numeric details providing natural targets for changes
- Self-consistent internal logic

Minor changes are clean numeric swaps (47->23, 28->14, 2.4->5.1 billion, 120k->85k, 240k->160k). Major changes are semantic contradictions that reverse the meaning of a claim. Both types are unambiguous and verifiable.

**Verdict:** Would be compelling to a competition judge. The passages feel like real scientific reporting, not toy examples.

## Disruptor Quality: Improved (was the main weakness)

### Neutral disruptors: Good
Genuinely bland. Shipping containers, composting, library cataloguing. No emotional valence, no domain overlap. Solid baseline.

### Emotional disruptors: Strong
Genuinely shocking content -- chemical plant explosion killing 47 workers, school bus plunging off bridge with children, deadly waterborne pathogen. These are viscerally attention-grabbing. The BREAKING/URGENT/ALERT framing adds urgency.

Note: the first emotional disruptor mentions "47 workers" which could theoretically interfere with the volcano passage's "47 micro-tremors." This is actually a nice accidental feature -- it creates a small amount of numeric interference even in the emotional condition.

### Task-relevant disruptors: Significantly strengthened

**Previous design (weakness):** Three generic science disruptors randomly assigned to passages. A volcanic monitoring disruptor might appear with the vaccine passage, providing only topical adjacency rather than genuine semantic interference. Two passages (glacier, vaccine) had no matched disruptor at all.

**Current design (fix applied):** Five passage-matched disruptors, one per passage. Each disruptor:
1. Discusses the exact same scientific domain
2. Deliberately includes the exact numbers being changed in the passage (e.g., the submarine disruptor mentions both "28 vent clusters" and "14" after correction)
3. Introduces plausible skepticism about the methodology used in the passage
4. Uses similar scientific register and naming conventions

This creates genuine semantic interference -- the model must distinguish between claims made in the passage and claims made in the disruptor, while both discuss the same quantities. This is much more powerful than mere topical adjacency.

**Verdict:** The contrast between disruptor types is now compelling. A judge would immediately see why task-relevant should cause more capture than emotional, and both more than neutral.

## Scoring: Correct

Two-tier approach from Cycle 3 fix:
1. Extract old/new values from expected string, check if both key numbers appear in response
2. Fall back to word overlap (50% threshold per side)
3. NO CHANGE is a simple substring check

This handles both numeric changes (minor) and semantic changes (major) appropriately.

## Analysis: Adequate

The analysis cells compute:
- Detection rate pivot table (change_type x disruptor_type)
- Attentional capture effect deltas (neutral - emotional, neutral - task_relevant)
- False alarm rates by disruptor type
- Grouped bar chart visualization

The false alarm rate for task-relevant disruptors in the no-change condition is an especially valuable metric -- it shows whether the model hallucinates a change that was only mentioned in the disruptor.

## Item Count

45 items (5 passages x 3 change types x 3 disruptor types). Matches the change_blindness task's sample size. Sufficient for showing trends, though per-cell counts are small (5 items per cell).

## Changes Made

1. **Added 2 new task-relevant disruptors** for glacier and vaccine passages (previously missing)
2. **Changed task-relevant disruptor structure** from list (random assignment) to dict (passage-matched)
3. **Enhanced all task-relevant disruptors** to include the exact numbers being changed, maximizing semantic interference
4. **Updated data generation loop** to use passage-matched lookup for task-relevant disruptors
5. **Updated timestamp** to 2026-03-31 05:30 UTC

## Risk Assessment

- **Low risk:** Passage-matched disruptors might make the task *too hard* for weaker models, potentially causing floor effects. However, the neutral baseline should still show reasonable detection, so the attentional capture delta remains interpretable.
- **Design strength:** The task-relevant disruptors now function as a genuine confound rather than just context. This is what makes mudsplash the most novel task in the suite -- it tests whether models can compartmentalize information sources under semantic pressure.
