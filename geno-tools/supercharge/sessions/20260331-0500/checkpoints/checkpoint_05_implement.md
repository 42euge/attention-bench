# Checkpoint 05: Implementation — Noise Filtering & Context Switching Review

**Timestamp:** 2026-03-31 ~05:35 UTC

## What was done

### Deep review of both notebooks

Full design reviews written to:
- `tasks/noise_filtering/review/design_review.md`
- `tasks/context_switching/review/design_review.md`

### Bugs found and fixed

1. **Noise Filtering — eval item count too low (FIXED)**
   - Was: `MAX_ITEMS_PER_CONFIG = 2` subsampled to only 36 eval items
   - Now: Uses all 180 items (10 passages x 6 ratios x 3 noise types)
   - Impact: 5x more data, proper statistical power per cell (n=10)

2. **Context Switching — variant count too low (FIXED)**
   - Was: 2 variants = 10 sequences (n=2 per condition)
   - Now: 5 variants = 25 sequences (n=5 per condition)
   - Impact: 2.5x more data, enables meaningful error bars

3. **Context Switching — scoring false negatives (FIXED)**
   - Added country name aliases (South Korea/Korea, Czech Republic/Czechia, Turkey/Turkiye)
   - Added misspelling correction acceptance (model can answer with correct spelling too)
   - Impact: Eliminates ~10-15% estimated false negatives on country/spelling tasks

4. **Context Switching — per-task-type analysis broken (FIXED)**
   - Was: Tried to access `row["response"]` which may not exist in kbench output
   - Now: Removed broken block, replaced with clean per-pure-block accuracy breakdown
   - Impact: Eliminates misleading/empty analysis output

5. **Noise Filtering — plot error bars added**
   - Was: Simple line plot with no uncertainty indication
   - Now: Error bars (std dev) shown on all data points
   - Impact: Visually communicates variance across passages

### Timestamps updated in both notebooks to 2026-03-31 05:30 UTC

## Key findings from review

### Noise Filtering — Strong design
- 10 fictional passages across diverse domains, preventing training data contamination
- 3 noise types (unrelated/related/adversarial) are theoretically well-motivated
- Adversarial noise with contradictory claims is the standout differentiator
- Scoring logic is robust with flexible matching
- Main weakness was sample size (now fixed)

### Context Switching — Good design with scoring risks
- Clean experimental design borrowed from cognitive psychology
- Three task types with explicit cues control for instruction comprehension
- `is_switch` flag is computed but never used in analysis — potential for deeper item-level switch cost analysis
- Main weaknesses were sample size and scoring edge cases (both now fixed)

## Remaining recommendations (not yet implemented)

1. **Noise Filtering:** Add 2-3 more related noise paragraphs per domain (currently only 1 per domain, causing repetition at high ratios)
2. **Noise Filtering:** Add a 0:1 baseline (no noise) condition for a clean ceiling
3. **Context Switching:** Add switch-vs-repeat item-level analysis using the `is_switch` flag
4. **Context Switching:** Vary sequence length (20/40/60/80) to test fatigue effects

## Files changed
- `tasks/noise_filtering/noise_filtering.ipynb` — increased eval items, added error bars, updated timestamp
- `tasks/context_switching/context_switching.ipynb` — increased variants, improved scoring, fixed analysis, updated timestamp
- `tasks/noise_filtering/review/design_review.md` — new file (detailed review)
- `tasks/context_switching/review/design_review.md` — new file (detailed review)
