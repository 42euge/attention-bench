# Context Switching — Design Review

**Reviewed:** 2026-03-31 ~05:30 UTC

## 1. Passage/Stimulus Quality

**Rating: Good**

- Three task types are well-chosen and clearly distinct: number extraction, country identification, misspelling detection.
- Each task type has meaningful template variety (15 number templates, 8 city templates, 8 spelling templates).
- Task cues ([NUMBER], [COUNTRY], [SPELLING]) are explicit, removing ambiguity about what's being asked.
- 30 city-country pairs span all continents — good diversity.
- 30 misspelling pairs are common English misspellings — unambiguous ground truth.

**Concerns:**
- **City-country ambiguity:** "Seoul" -> "South Korea" is clear, but the `check_answer` uses substring matching. If a model answers "Korea" for "South Korea", `exp in act` is False (because "south korea" is not in "korea"). This would be a **false negative**. Similarly, "Czech Republic" — if a model says "Czechia", it fails. These are real risks with a handful of the 30 pairs.
- **Misspelling task clarity:** The prompt says "Identify the misspelled word", and the expected answer is the misspelled form (e.g., "exmained"). A model might reasonably answer with the correct spelling ("examined") or say "exmained (should be examined)". The substring match `exp in act` would catch the latter, but the former would be a false negative. This is a meaningful scoring risk.

## 2. Scoring Logic

**Rating: Adequate, with known risks**

- `strip_thinking()` handles reasoning model preambles. Good.
- `parse_numbered_answers()` correctly handles `1.`, `1)`, `1:`, `1-` formats. Falls back to raw lines.
- `check_answer()` does case-insensitive, substring, and comma-stripped matching.

**False negative risks:**
1. **"Korea" vs "South Korea"**: Model answers "Korea", expected is "South Korea". `"south korea" in "korea"` = False. **False negative.**
2. **"Czechia" vs "Czech Republic"**: Different strings entirely. **False negative.**
3. **Misspelling correct form:** If model identifies the misspelled word by giving the correction ("examined" instead of "exmained"), it fails. **Significant false negative risk** — this is arguably the most natural response.
4. **Number format:** Model might answer "1234" for expected "1,234". The comma-stripping handles this. OK.
5. **60 items in one response:** Parsing 60 numbered answers is ambitious. If the model's formatting drifts (e.g., grouping answers, adding explanations), parsing could fail for many items. **Moderate risk of systematic parsing failures.**

**Missing from CS that NF has:** The `exp_core` stripping of "approximately/about" prefixes. Not critical here since answers are exact, but inconsistent.

## 3. Analysis Quality

**Rating: Mixed**

**Good:**
- Groups by condition and shows mean accuracy — the right primary metric.
- Computes switch cost (pure baseline minus alternating/random) — the key theoretical metric.
- Bar chart with clear color coding (blue for pure, orange for alternating, red for random).
- Baseline line drawn for visual reference.

**Problem:**
- The "Per-Task-Type Accuracy in Mixed Conditions" analysis block tries to access `row["response"]` and re-parse the response. This field may not exist in the `results` dataframe depending on how `kbench` returns data. If the response is stored as `row["output"]` or similar, this **silently produces empty results** (the `parse_numbered_answers` gets an empty string and returns all empty strings, scoring 0 across the board). This is a **likely bug** that would produce misleading per-task-type breakdowns.
- Even if `response` is available, re-parsing the response independently is fragile — it should use the same parsed answers from the initial scoring.

## 4. Item Count

**Rating: WEAK — Primary Concern**

- **10 total sequences** (2 variants x 5 conditions).
- Only **2 sequences per condition**. With 60 items each, that's 120 items per condition, which sounds OK at the item level.
- But the **statistical unit is the sequence**, not the individual item (items within a sequence are not independent — they share the same model call, same context window, same parsing). So n=2 per condition is insufficient for any statistical test.
- No error bars are meaningful with n=2.

**Recommendation:** Increase to at least 4-5 variants (20-25 sequences). This gives n=4-5 per condition, enough for basic significance testing. The data generation is cheap — it's just template instantiation.

## 5. What Would Make It Stronger

### Quick wins (should do):
1. **Increase variants to 5+:** Change `for variant_idx in range(2)` to `range(5)` for 25 sequences. Minimal effort, major improvement to statistical power.
2. **Fix per-task-type analysis:** Either remove the broken analysis block or fix the response field name. Currently it likely produces misleading output.
3. **Add misspelling scoring fallback:** Accept the correct spelling as an alternative answer for the misspelling task (if model says "examined" instead of "exmained", count it as correct).
4. **Add country aliases:** Handle "Korea"/"South Korea", "Czechia"/"Czech Republic" pairs.

### Medium effort:
5. **Add switch-vs-repeat item-level analysis:** Within the random condition, compare accuracy on items that are switches (different task type from previous) vs repeats (same task type as previous). The `is_switch` flag is already computed but never used in analysis. This is the most interesting theoretical metric — it directly measures the switch cost at the item level.
6. **Vary sequence length:** Currently fixed at 60 items. Testing with 20, 40, 60, 80 items would show whether sequence length modulates switch cost (fatigue/accumulation effects).

### Design strengths to highlight:
- The three conditions (pure/alternating/random) are a clean experimental design borrowed from cognitive psychology.
- The task cue system is clever — it controls for instruction comprehension and isolates the switching cost.
- The `is_switch` flag enables fine-grained analysis if properly used.
- 60 items per sequence is long enough to see real switching effects.

## Bugs Found

1. **Per-task-type analysis likely broken:** `row.get("response", "")` — field name may not match kbench output schema. Needs verification or removal.
2. **Country name aliases missing:** "South Korea" vs "Korea", "Czech Republic" vs "Czechia" will produce false negatives.
3. **Misspelling task scoring:** Accepting only the misspelled form (not the correct spelling) as the answer is fragile.

## Summary

| Dimension | Rating | Notes |
|---|---|---|
| Stimulus quality | Good | Clear task types, good variety, explicit cues |
| Scoring logic | Adequate | Risks with country names and misspelling answers |
| Analysis | Mixed | Primary metrics good, per-task breakdown likely broken |
| Item count | Weak | Only 2 variants (n=2 per condition) |
| Overall | Needs fixes | Increase variants, fix scoring edge cases, fix analysis bug |
