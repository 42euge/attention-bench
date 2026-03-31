# Change Blindness

## What it tests

Can a model spot what changed between two versions of code or a ticket when there's unrelated stuff in between?

## The setup

Two categories of passages:

**code-development** — actual code snippets:
- Retry logic, LRU cache, rate limiter
- Minor change = a number tweak (`max_retries=3` → `5`)
- Major change = a logic bug (`raise` → `return {}`, `popitem(last=False)` → `last=True`)

**code-task** — tickets/specs:
- Search feature, DB migration
- Minor change = an SLA number (`200ms` → `500ms`)
- Major change = a safety removal (feature flag → ship direct, keep fallback → drop immediately)

Between Version A and Version B, 0, 1, or 3 **disruptors** are inserted (standup notes, Slack messages, wiki updates — totally unrelated).

## What to expect when you run it

The notebook outputs a 3×3 table: **change type** (minor, major, none) × **disruptor count** (0, 1, 3).

**Good results look like:**
- `none` row should be ~100% — model correctly says NO CHANGE when nothing changed (low false alarm rate)
- `major` row should be higher than `minor` — logic bugs are easier to spot than number tweaks
- Numbers should drop as disruptors increase (0 → 1 → 3) — that's the "blindness" effect
- If there's no drop with disruptors, the task isn't hard enough for this model

**What discriminates models:**
- Weak models miss minor changes even with 0 disruptors
- Strong models maintain detection through 3 disruptors
- The interesting signal is the **drop** from 0 to 3 disruptors — how much does interference hurt?

**Metrics printed:**
- Detection rate by change type × disruptor count (the main table)
- False alarm rate (saying something changed when nothing did)
- Per-change-type baseline vs 3-disruptor comparison with the drop

**Plot:** Line chart showing detection rate vs disruptor count for minor, major, and false alarm.

## Design

5 passages × 3 change types (minor, major, none) × 3 disruptor levels (0, 1, 3) = **45 items total**.

Scoring checks if the model mentions the key values from both sides of the change (e.g., both "3" and "5" for `max_retries=3→5`). Falls back to word overlap matching for non-numeric changes.
