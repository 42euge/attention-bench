# Validation Report — Supercharge Cycle 8

**Date:** 2026-03-31 05:00 UTC

## Summary

All 4 task notebooks pass validation. No errors found.

| Task | Valid JSON | Imports OK | Data Gen OK | Items | Timestamp | Ready |
|------|-----------|-----------|-------------|-------|-----------|-------|
| noise_filtering | YES | YES | YES | 180 | 2026-03-31 05:30 UTC | YES |
| context_switching | YES | YES | YES | 25 | 2026-03-31 05:30 UTC | YES |
| change_blindness | YES | YES | YES | 45 | 2026-03-31 04:59 UTC | YES |
| mudsplash | YES | YES | YES | 45 | 2026-03-31 05:30 UTC | YES |

**Total items across all tasks: 295**

## Detail

### noise_filtering (180 items)
- **Structure:** 13 cells (title markdown, setup, helpers, passages, noise templates, datagen, task header, task def, eval header, eval, results header, analysis, plot)
- **Imports:** kaggle_benchmarks, pandas, numpy, json, re, random, subprocess, sys, matplotlib — all standard/allowed
- **Data gen:** 180 items = 10 passages x 3 noise types (unrelated, related, adversarial) x 6 noise ratios (1, 5, 10, 25, 50, 100)
- **Columns:** task_id, passage_id, domain, noise_type, noise_ratio, num_questions, prompt, answers

### context_switching (25 items)
- **Structure:** 12 cells (title markdown, setup, helpers, seed_data, datagen, task header, task def, eval header, eval, results header, analysis, plot)
- **Imports:** kaggle_benchmarks, pandas, numpy, json, re, random, subprocess, sys, matplotlib — all standard/allowed
- **Data gen:** 25 items = 5 variants x 5 conditions (pure_number, pure_country, pure_spelling, alternating, random), each sequence has 60 sub-items
- **Columns:** task_id, prompt, answers, task_types, is_switch, condition, variant, num_items

### change_blindness (45 items)
- **Structure:** 14 cells (title markdown, setup, helpers, datagen, overview, task header, task def, eval header, eval, results header, analysis, plot, calibration header, calibration analysis)
- **Imports:** kaggle_benchmarks, pandas, numpy, json, re, random, subprocess, sys, matplotlib — all standard/allowed
- **Data gen:** 45 items = 5 passages x 3 change types (minor, major, none) x 3 disruptor counts (0, 1, 3)
- **Categories:** 3 code-development passages, 2 code-task passages
- **Columns:** task_id, prompt, expected, passage_id, category, change_type, disruptor_count

### mudsplash (45 items)
- **Structure:** 11 cells (title markdown, setup, helpers, seed_data+datagen, task header, task def, eval header, eval, results header, analysis, plot)
- **Imports:** kaggle_benchmarks, pandas, numpy, json, re, random, subprocess, sys, matplotlib — all standard/allowed
- **Data gen:** 45 items = 5 passages x 3 change types (minor, major, none) x 3 disruptor types (neutral, emotional, task_relevant)
- **Columns:** task_id, prompt, expected, passage_id, change_type, disruptor_type

## Notes
- All notebooks use `strip_thinking()` helper to handle `</think>` tags
- All notebooks use `import subprocess, sys` for matplotlib installation (Kaggle-compatible)
- No local imports (no src/, no ../ references)
- change_blindness timestamp is slightly older (04:59 vs 05:30) but present and valid
- context_switching has 25 top-level items but each contains 60 sub-items (1,500 total sub-evaluations)
