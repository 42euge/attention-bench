# Context Switching

## What it tests

Does switching between different task types within a single sequence reduce the model's accuracy? This tests executive control of attention — the cost of reconfiguring between task sets, analogous to human task-switch costs.

## The setup

The model receives a sequence of 60 items, each tagged with a task cue:

- **[NUMBER]** — extract the number from a sentence
- **[COUNTRY]** — identify the country of a referenced city
- **[SPELLING]** — find the misspelled word in a sentence

Three conditions control switching frequency:

- **Pure blocks** — all 60 items are the same task type (baseline, no switching)
- **Predictable alternation** — tasks cycle ABCABC... with explicit cues
- **Random switching** — task order is randomized with explicit cues

All items include explicit cues, so the model always knows which task to perform. The question is whether switching itself imposes a cost.

## What to expect when you run it

The notebook outputs accuracy by condition: **pure_number, pure_country, pure_spelling, alternating, random**.

**Good results look like:**
- Pure blocks should have the highest accuracy (no switching overhead)
- Alternating should be slightly lower (predictable switches still cost something)
- Random should be the lowest (unpredictable switches are hardest)
- The gap between pure and random is the "switch cost"

**What discriminates models:**
- Weak models show large switch costs (10%+ drop from pure to random)
- Strong models maintain accuracy across conditions (small or zero cost)
- Some models may show asymmetric costs — worse at one task type when switching

**Metrics printed:**
- Accuracy by condition (the main comparison)
- Switch cost: pure baseline minus alternating/random accuracy
- Per-task-type accuracy in mixed conditions

**Plot:** Bar chart showing accuracy by condition with switch cost annotation.

## Design

3 pure conditions + 1 alternating + 1 random = 5 sequences per variant, 2 variants = **10 sequences total**, each containing 60 items = **600 items scored**.

Scoring parses numbered answers and checks against expected values with number normalization and substring matching.
