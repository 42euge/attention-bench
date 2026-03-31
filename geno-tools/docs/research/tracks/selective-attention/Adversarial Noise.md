# Adversarial Noise

#attention #selective-attention #L2

The hardest form of selective attention filtering: noise that contains plausible-but-wrong answers to the questions being asked.

## What Makes It Hard
Unlike unrelated noise (easy to dismiss) or related noise (same domain but different facts), adversarial noise directly competes with correct answers. The model must not only find the signal but actively reject convincing alternatives.

## In Our Benchmark
The noise_filtering task uses adversarial noise paragraphs crafted per-passage — they reference the same entities, locations, and topics but with altered numbers, names, and causal claims. For example, if the passage says "Dr. Yamada discovered organisms at 2,400 meters," the adversarial noise says "Dr. Tanaka Hiroshi documented organisms at 3,100 meters."

## Expected Discrimination
Adversarial noise should produce the steepest accuracy curves across models — the threshold where performance drops below 80% should be much lower than for unrelated or related noise. Models with stronger selective attention will maintain higher thresholds.

## Links
- Up: [[Signal-to-Noise Filtering]]
- Related: [[Distractor Robustness]], [[GSM-IC (2023)]]
