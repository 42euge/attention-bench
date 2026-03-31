# Dual-Task Interference

## What it tests

Can the model perform two attention-demanding tasks simultaneously without interference? This tests divided attention — the ability to maintain performance on a primary task (comprehension) while concurrently performing a secondary task (word counting).

## The setup

Three fictional passages (fusion reactor, ocean cleanup, quantum computing) each have 4 comprehension questions and 2 word-counting targets.

Three conditions:

- **Single comprehension** — answer a question about the passage (no counting)
- **Single counting** — count occurrences of a common word like "the" or "of" (no questions)
- **Dual task** — do both simultaneously: count the target word AND answer the question in a single response

The dual-task condition requires the model to track word counts while also understanding and extracting factual information from the same passage.

## What to expect when you run it

The notebook outputs accuracy by condition: **single_comprehension, single_counting, dual**.

**Good results look like:**
- Single-task conditions should both be high (the tasks are easy in isolation)
- Dual-task accuracy should be lower than either single-task baseline
- The gap is the "dual-task cost" — how much does concurrent processing hurt?

**What discriminates models:**
- Weak models show large dual-task costs (accuracy drops 20%+ when doing both)
- Strong models maintain near-single-task accuracy even in the dual condition
- Counting is typically harder than comprehension — look for asymmetric interference
- Some models may sacrifice counting accuracy to preserve comprehension, or vice versa

**Metrics printed:**
- Accuracy by condition (single comprehension, single counting, dual)
- Dual-task cost: drop from single-task baselines
- Per-passage breakdown

**Plot:** Bar chart comparing single-task vs dual-task accuracy.

## Design

3 passages x (4 single-comprehension + 2 single-counting + 4x2 dual) = 3 x 14 = **42 items total**.

Comprehension scoring uses substring matching with number normalization. Counting scoring allows +/-1 tolerance. Dual items score both components (2 points possible per item).
