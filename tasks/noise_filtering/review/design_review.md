# Noise Filtering — Design Review

**Reviewed:** 2026-03-31 ~05:30 UTC

## 1. Passage/Stimulus Quality

**Rating: Strong**

- 10 passages across diverse, interesting domains (marine biology, architecture, astronomy, chemistry, ancient history, linguistics, geology, music, botany, meteorology).
- All passages are fictional but internally consistent and richly detailed, making them compelling and varied.
- Each passage has 5 questions with unambiguous, extractive answers (numbers, proper nouns, specific terms). No judgment calls required — a judge would find these verifiably correct.
- Adversarial noise is well-designed: contains plausible but wrong details that directly contradict the target passage (e.g., different depths, different instrument names, different dates). This is the strongest differentiator in the task.

**Minor concern:** All passages are fictional. A judge might wonder if models could "hallucinate" correct answers from training data overlap. However, since the names/numbers/places are fabricated, this actually *prevents* training data contamination — a strength, not a weakness.

## 2. Scoring Logic

**Rating: Good, with minor risks**

- `strip_thinking()` correctly handles reasoning model preambles by splitting on `</think>`.
- `parse_numbered_answers()` handles multiple formats: `1.`, `1)`, `1:`, `1-`. Falls back to raw lines if no numbered format detected.
- `check_answer()` does case-insensitive matching, substring matching, and comma/whitespace normalization for numbers.
- Has an `exp_core` intermediate that strips "approximately/about/roughly/around" prefixes — useful for numeric answers.

**Potential false negatives:**
- If a model answers "luciferase K7" (without hyphen) for "luciferase-K7", substring match will catch it (exp in act). OK.
- If a model answers "about 2,400 meters" for "2,400 meters", the `exp_core` strip + substring catches this. OK.
- If a model writes an answer with extra context like "The answer is 2,400 meters", substring match catches it. OK.
- **Risk:** If a model writes "Maren Lindqvist of the firm Nordvik & Partners" for expected "Maren Lindqvist", the `exp in act` substring match will catch it. OK.
- **Risk:** If a model writes "287 pages" for expected "287", substring match catches it. OK.
- **Risk:** Numbers like "3,200" vs "3200" — the comma/whitespace stripping handles this. OK.

**Verdict:** Scoring logic is robust enough. Unlikely to produce significant false negatives.

## 3. Analysis Quality

**Rating: Good**

- Groups by noise_type x noise_ratio and shows accuracy heatmap — exactly the right primary analysis.
- Computes "attention threshold" (highest ratio with >=80% accuracy) per noise type — a clean, interpretable metric.
- 3-panel plot (one per noise type) with log-scale x-axis clearly shows the degradation curve.
- 80% threshold line is drawn for visual reference.
- A judge would understand the results at a glance.

**Suggestion:** Adding error bars or per-passage dots on the plot would show variance and strengthen the statistical story. Currently with only 2 items per config, there's no meaningful error bar to draw.

## 4. Item Count

**Rating: WEAK — Primary Concern**

- **180 items generated** (10 passages x 6 ratios x 3 noise types), but only **36 evaluated** (2 per config).
- At only 2 items per (noise_type, noise_ratio) cell, there is **no statistical significance** — a single fluke answer changes the cell accuracy by 10 percentage points (since each item has 5 questions, that's 50% swing per item).
- The competition weights "sufficient sample size" at 50% of dataset quality.

**Recommendation:** Remove the `MAX_ITEMS_PER_CONFIG = 2` subsample and evaluate all 180 items. This gives 10 items per cell (50 questions), which is much more defensible. The current subsampling throws away 80% of the carefully crafted data for no clear benefit. If runtime is a concern, even `MAX_ITEMS_PER_CONFIG = 5` (90 items) would be a significant improvement.

## 5. What Would Make It Stronger

### Quick wins (should do):
1. **Increase eval items:** Set `MAX_ITEMS_PER_CONFIG = 10` (or remove subsample entirely) to use all 180 items. This is the single highest-impact change.
2. **Add error bars to plot:** Show std dev or confidence intervals per cell.
3. **Add per-passage breakdown:** Show which passages are harder/easier — this provides interesting secondary analysis.

### Medium effort:
4. **Related noise pool is too small:** Each domain has only 1 related noise paragraph. At ratio 100:1, this paragraph gets repeated ~12 times, which makes the "related" condition less realistic. Adding 2-3 more related paragraphs per domain would help.
5. **Add a 0:1 (no noise) baseline condition:** Currently the lowest ratio is 1:1. A clean baseline with ratio=0 would make the degradation curve more interpretable and show the ceiling.

### Design strengths to highlight:
- The three noise types (unrelated/related/adversarial) are a strong theoretical contribution — they test different filtering demands.
- The interleaving strategy (noise paragraphs mixed between passage chunks) is more realistic than simply prepending/appending noise.
- The fictional passages prevent training data contamination.
- The log-scale ratio range (1 to 100) provides good dynamic range for finding the threshold.

## Summary

| Dimension | Rating | Notes |
|---|---|---|
| Passage quality | Strong | Diverse, detailed, unambiguous answers |
| Scoring logic | Good | Handles preambles, flexible matching |
| Analysis | Good | Clear metrics, interpretable plots |
| Item count | Weak | Only 36 eval items; should use all 180 |
| Overall | Good with one critical fix needed | Increase eval items to full 180 |
