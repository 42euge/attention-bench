# Change Magnitude

#attention #change-detection #L2

The size/importance of a change strongly predicts detection — major changes to central claims are detected more readily than minor numerical changes to peripheral details.

## Two Levels in Our Benchmark
1. **Minor changes** — a number or name is altered (e.g., "847 megawatts" → "634 megawatts")
2. **Major changes** — a causal claim is reversed (e.g., "low humidity and direct sunlight" → "persistent cloud cover and frequent rainfall")

## Expected Discrimination
- Major changes should be detected at much higher rates than minor changes
- The interaction between magnitude and disruption level is where model differences emerge
- Strong models should maintain detection even for minor changes with 3 disruptors
- Weak models should fail on minor changes even with 0 disruptors

## Connection to Cognitive Science
In human change blindness research, "marginal interest" changes (peripheral details) are missed 4× more often than "central interest" changes (main subjects). Our minor/major distinction maps directly to this.

## Links
- Up: [[Change Detection]]
- Related: [[Disruption Effects]], [[Textual Change Blindness]]
