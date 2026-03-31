# Figure 3: Adversarial Attention Threshold vs Model Size (Gemma Family)

**Description:** Log-log scatter plot with model parameters (x-axis, log scale: 1B, 4B, 12B, 27B) vs adversarial attention threshold (y-axis, log scale: 0.1, 1, 10, 100). Four data points for the Gemma family with a fitted line.

**Data points:**
- (1B, ~0.5) — fails at baseline, plotted at 0.5 for log scale
- (4B, 1)
- (12B, 10)
- (27B, 100)

**Fit:** Approximately log-linear: log₁₀(threshold) ≈ 2.5 × log₁₀(params) - 22.5

**Annotation:** Horizontal dashed lines showing where DeepSeek R1 (50:1) and frontier models (100:1+) fall relative to the Gemma trend line, suggesting that architectural differences and training data quality modulate the base scaling relationship.

**Key takeaway:** Each ~3× increase in parameters yields ~10× increase in adversarial noise tolerance.
