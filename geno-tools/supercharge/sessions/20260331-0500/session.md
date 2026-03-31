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
