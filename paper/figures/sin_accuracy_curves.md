# Figure 1: Signal-in-Noise Accuracy by Noise Ratio and Type

**Description:** Three-panel line chart (one per noise type) showing accuracy (y-axis, 0-100%) vs noise ratio (x-axis, log-scaled: 0:1, 1:1, 5:1, 10:1, 25:1, 50:1, 100:1) for all 8 models.

**Panel A — Unrelated Noise:** All lines except gemma-3-1b remain flat near 100% across all ratios. gemma-3-1b declines from ~80% at 1:1 to ~40% at 100:1. The panel is visually uninteresting — a cluster of flat lines at the top.

**Panel B — Related Noise:** Nearly identical to Panel A. gemma-3-1b shows slightly earlier decline (drops below 80% at 10:1 vs 5:1 for unrelated). All other models remain at ceiling.

**Panel C — Adversarial Noise:** This panel tells the story. Clear fan-out pattern:
- gemma-3-1b: starts below 80% even at 0:1 baseline, drops to ~0% by 25:1
- gemma-3-4b: drops sharply from ~80% at 1:1 to ~40% by 10:1
- gemma-3-12b: holds until 10:1, then drops to ~60% at 25:1+
- deepseek-r1-0528: holds until 50:1, drops at 100:1
- gemma-3-27b, claude-haiku-4-5, gemini-2.5-flash, claude-opus-4-6: flat at ~100% across all ratios

**Key visual:** The contrast between Panels A/B (no discrimination) and Panel C (clear scaling ladder) is the paper's central finding.
