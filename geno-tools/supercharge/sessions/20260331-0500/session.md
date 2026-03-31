# Supercharge Session — 2026-03-31 05:00 UTC

**Duration:** 8 hours (16 cycles)
**Scope:** All 8 tasks across attention benchmark
**Goal:** Get all tasks running on Kaggle with good discriminatory power

---

## Cycle 1 — PLAN (05:00 UTC)

**State assessment:**
- 8 task notebooks exist, all self-contained with timestamps
- Only `change_blindness` is linked on Kaggle (ran once, scoring was too strict, now has code/ticket passages)
- 7 tasks have never been linked to Kaggle
- 0 reviews exist
- Folder structure is set up: each task has docs/, results/, review/
- The `change_blindness` Kaggle notebook path changed (moved into subfolder) — needs re-linking

**Priority ranking:**
1. P0: Fix change_blindness — re-link on Kaggle, verify new code passages + scoring work
2. P1: Review change_blindness results from last run (already pulled data available)
3. P2: Audit all other 7 notebooks for common issues (llm= bug was fixed, but check for other problems)
4. P3: Pick 2-3 most promising tasks and prepare them for Kaggle linking
5. P4: Research — are there improvements to make based on competition criteria?

**Sprint 1 plan (cycles 1-4):**
- Cycle 1: Plan (this) + review change_blindness last run
- Cycle 2: Implement — audit and fix all 7 remaining notebooks
- Cycle 3: Implement — create docs for top 3 tasks, prepare for Kaggle
- Cycle 4: Evaluate — pull change_blindness results if re-run, assess all task readiness

## Cycle 3 — IMPLEMENT (06:00 UTC)

**Completed:**
- Fixed mudsplash scoring: same false-negative pattern as change_blindness (strict "changed to" split + exact substring). Now uses number-aware matching + 50% word-overlap fallback.
- Created docs for top 3 tasks: noise_filtering, context_switching, dual_task_interference (following change_blindness.md format).
- Committed and pushed (7bacf26).

**Key decisions:**
- Top 3 tasks chosen for docs: noise_filtering (6 noise ratios x 3 types = rich gradient), context_switching (pure/alt/random = clear switch cost signal), dual_task_interference (single vs dual = clean comparison).
- Mudsplash was the only notebook flagged in cycle 2 audit for scoring strictness — now fixed.

## Cycle 4 — PLAN (06:20 UTC)

**Strategy research completed.** Key decision: **cut from 8 to 4 tasks.**

Final four (ranked by discriminatory power × novelty):
1. **Noise Filtering** — best gradient (6 ratios × 3 noise types), cleanest design
2. **Context Switching** — strong gradient (pure/alt/random), agent-relevant
3. **Change Blindness** — novel code-review framing, needs re-validation
4. **Mudsplash** — most novel question (emotional attentional capture)

Cut: attentional_blink (no temporal bottleneck), dual_task_interference (thin data), continuous_performance (parsing fragility), vigilance_decrement (overlaps noise_filtering).

**Sprint 2 plan (cycles 5-8): Get all 4 final tasks running on Kaggle**
- Cycle 5: Implement — ensure noise_filtering and context_switching passages are strong, check scoring
- Cycle 6: Implement — ensure mudsplash passages/disruptors are compelling
- Cycle 7: Evaluate — review any Kaggle results available
- Cycle 8: Plan — writeup strategy, multi-model evaluation plan

## Cycle 6 — IMPLEMENT (06:40 UTC)

**Completed:**
- Deep review of mudsplash notebook
- Found and fixed significant weakness: task-relevant disruptors were randomly assigned and generic. Now passage-matched with embedded changed values for genuine semantic interference.
- Created docs/mudsplash.md and review/design_review.md
- Committed and pushed (09246fb)

**Key improvement:** Task-relevant disruptors now mention the exact numbers being changed in the passage (e.g., "28 vent clusters" when the change is 28→14). This creates real confusion rather than just topical adjacency.

## Cycle 5 — IMPLEMENT (06:30 UTC)

**Completed:**
- Deep review of noise_filtering and context_switching notebooks
- Noise filtering: critical fix — eval items increased 36→180 (was discarding 80% of data). Error bars added to plot.
- Context switching: variants 2→5 (5 per condition), country alias scoring fixed (Korea/South Korea etc.), misspelling scoring accepts correct spelling, broken analysis cell removed.
- Design reviews written for both tasks.
- Committed and pushed (afafae1).

## Cycle 7-8 — PLAN + IMPLEMENT (07:00 UTC)

**All 4 final tasks are now polished:**
1. ✅ Noise Filtering — 180 items, strong gradient, fixed eval count
2. ✅ Context Switching — 25 sequences, scoring fixes, clean design
3. ✅ Change Blindness — code/ticket passages, relaxed scoring
4. ✅ Mudsplash — passage-matched disruptors with embedded changed values

**Next priority:** All 4 need Kaggle runs. User must manually create Tasks and link notebooks via File → Link to GitHub. Preparing everything to make that as easy as possible.

## Cycle 8 — EVALUATE (07:20 UTC)

**Validation results — all 4 pass:**
| Task | Items | Timestamp | Ready |
|------|-------|-----------|-------|
| noise_filtering | 180 | 2026-03-31 05:30 UTC | YES |
| context_switching | 25 (×60 sub-items) | 2026-03-31 05:30 UTC | YES |
| change_blindness | 45 | 2026-03-31 04:59 UTC | YES |
| mudsplash | 45 | 2026-03-31 05:30 UTC | YES |

Total: 295 top-level items. All notebooks parse, generate data, and import correctly.

**Sprint 2 complete.** All 4 final tasks are polished and validated.

---

## Sprint 3 — Polish and Prepare (cycles 9-12)

**Blocker:** Kaggle results require user to manually link notebooks. Can't proceed with results-dependent work.

**Available work:**
- Cycle 9: Writeup quality pass — strengthen the narrative, add more cognitive science depth
- Cycle 10: Create media assets (competition requires cover image)
- Cycle 11: Final end-to-end review of everything
- Cycle 12: Update CLAUDE.md, clean up repo, prepare summary for user

## Cycle 9 — IMPLEMENT (07:30 UTC)

**Completed:**
- Writeup strengthened from 1,110 → 1,386 words (114 under limit)
- Added cognitive science citations (Broadbent 1958, Monsell 2003, Rensink et al. 1997, O'Regan et al. 1999)
- Added expected result patterns for each task
- Added "so what?" conclusion connecting to agent architectures and code review
- Committed and pushed (c7d62ec)

## Cycle 10 — IMPLEMENT (07:45 UTC)

**Completed:**
- CLAUDE.md updated with final 4 tasks table, archived 4 noted
- STRUCTURE.md rewritten for current repo layout
- README.md created with project overview and task table
- .gitignore added, all untracked files committed
- Committed and pushed (0ded657)

## Cycle 11 — EVALUATE (08:00 UTC)

**Final quality gate — grades:**
| Area | Grade |
|---|---|
| Writeup | A- (1,386 words, all sections, real citations) |
| README | B+ (functional, needs cover image) |
| Notebooks | A (all validated, correct structure) |
| Docs | A- (all 4 present, consistent format) |
| Repo | B (clean remote, some local stale files) |

**Sole blocker:** 5 [PLACEHOLDER] markers in writeup need real Kaggle results.

## Cycle 12 — WRAP-UP (08:15 UTC)

### Session Summary

**11 cycles completed** (of 16 planned). Stopped early — all available work is done. Remaining work requires user action (Kaggle linking + runs).

### What was accomplished

1. **Strategy:** Analyzed all 8 tasks against competition criteria. Cut to 4 strongest tasks.
2. **Quality:** Audited all 8 notebooks. Fixed scoring bugs in change_blindness and mudsplash. Fixed eval item count in noise_filtering (36→180). Fixed scoring edge cases in context_switching.
3. **Mudsplash improvement:** Restructured task-relevant disruptors from random to passage-matched with embedded changed values — genuine semantic interference.
4. **Documentation:** Created docs for all 4 final tasks. Design reviews for all 4.
5. **Writeup:** 1,386-word draft with cognitive science citations, expected results, and "so what?" framing.
6. **Repo:** README, updated CLAUDE.md, cleaned STRUCTURE.md, .gitignore, all files committed.
7. **Validation:** All 4 notebooks pass parse/import/data-gen checks. 295 total items.
8. **Artifacts:** Competition strategy, Kaggle linking guide, notebook audit, validation report, final review.

### What the user needs to do

**Must-do (in order):**
1. Create 4 Kaggle Benchmark Tasks at https://www.kaggle.com/benchmarks/tasks/new
2. For each, File → Link to GitHub → select the notebook:
   - `tasks/noise_filtering/noise_filtering.ipynb`
   - `tasks/context_switching/context_switching.ipynb`
   - `tasks/change_blindness/change_blindness.ipynb` (re-link — path changed)
   - `tasks/mudsplash/mudsplash.ipynb`
3. Run all 4 and wait for results
4. Run `/gt-kaggle-benchmarks-task-review <task_name>` for each to pull and analyze results
5. Fill in the 5 [PLACEHOLDER] markers in writeup.md with real data
6. Create a Benchmark grouping all 4 tasks
7. Create a cover image for the media gallery
8. Submit

**See also:** `geno-tools/supercharge/sessions/20260331-0500/artifacts/kaggle_linking_guide.md` for detailed step-by-step.

### Risks
- Discriminatory power unknown until Kaggle runs complete
- Writeup has 114 words of headroom — keep placeholder replacements concise
- If any task shows flat results across models, may need to iterate on that task's design
