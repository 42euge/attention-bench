# Change Blindness — Detail Tracking Across Disruptions

## What it tests

Can a model detect subtle factual changes between two versions of a passage when separated by an unrelated "disruptor" paragraph? This mirrors the human phenomenon of **change blindness** — failing to notice changes when they coincide with a visual interruption.

## Design

### Stimulus structure

Each trial presents two versions of a factual passage (Version A → Version B). Between them, 0, 1, or 3 unrelated "disruptor" paragraphs may be inserted as an interlude.

```
=== VERSION A ===
<original passage>

=== INTERLUDE ===        ← 0, 1, or 3 disruptor paragraphs
<unrelated text>

=== VERSION B ===
<passage with one change>
```

The model must identify what changed (or say "NO CHANGE" if nothing did).

### Independent variables (factorial)

| Variable | Levels | Purpose |
|---|---|---|
| **Change magnitude** | minor, major, none | Minor = a number or name swap. Major = a causal claim reversal. None = identical passages (control). |
| **Disruptor count** | 0, 1, 3 | More disruptors = more interference between encoding and comparison. |

This gives a 3×3 factorial = 9 conditions per passage.

### Passages

5 fictional-but-realistic passages across domains: solar energy, marine biology, archaeology, neuroscience, climate science. Each has a pre-written minor change (e.g., "847 megawatts → 634 megawatts") and major change (e.g., "low humidity and sunlight → persistent cloud cover and rainfall").

**Total items:** 5 passages × 9 conditions = 45 items.

### Disruptors

3 unrelated paragraphs (board games, Japanese joinery, helium supply) randomly sampled to fill the interlude. These are thematically unrelated to any passage, maximizing attentional interference.

## Task definition

```python
@kbench.task(name="change_blindness")
def change_blindness(llm, prompt, expected, change_type, disruptor_count) -> bool:
```

- Returns `True`/`False` (correct/incorrect)
- For "NO CHANGE" trials: checks if model output contains "no change"
- For change trials: splits expected answer on "changed to" and checks both old and new values appear in the response

## Metrics

| Metric | What it reveals |
|---|---|
| **Detection rate by change type** | Are major (causal) changes easier to spot than minor (numeric) ones? |
| **Detection rate by disruptor count** | Does interleaved text degrade change detection? |
| **False alarm rate** | Does the model hallucinate changes when none exist? |
| **Detection drop** | Baseline (0 disruptors) minus 3-disruptor accuracy — the "blindness" effect size |

## Confidence calibration (bonus)

Each prompt asks the model to self-rate confidence (1-5). This enables:
- **Reliability diagram** — actual accuracy vs. stated confidence
- **Expected Calibration Error (ECE)** — aggregate miscalibration score
- **Overconfidence rate** — wrong answers rated 4-5
- **Underconfidence rate** — correct answers rated 1-2

## Expected findings

- Minor changes should be harder to detect than major changes
- More disruptors should reduce detection rate (the change blindness effect)
- Weaker models may show higher false alarm rates
- Models may be systematically overconfident on wrong answers
