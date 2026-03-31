# Monotony and Automaticity

#attention #sustained-attention #L1

Two competing theories explain human vigilance decrement — overload (resource depletion) and underload (mindlessness from monotony). Both may apply to LLMs.

## Overload Theory
Performance degrades because sustained monitoring depletes attentional resources. Predicts: harder tasks -> faster decrement.

## Underload Theory
Performance degrades because monotonous tasks fail to maintain arousal/engagement. Predicts: easier tasks -> faster decrement (the "monotony effect").

## LLM Implications
- If LLMs show worse degradation on easy monotonous tasks, the underload model applies
- If degradation is worse on harder tasks, the overload model applies
- A 2x2 factorial design (easy/hard x monotonous/varied) could adjudicate
- The "Repeat Curse" (arXiv:2504.14218) shows LLMs generate repetitive content in enumerative tasks — suggestive of automaticity

## Oddball Detection
Our vigilance_decrement task includes oddball variants — a single unexpected task type at a random position. This tests whether automated processing causes the model to miss unexpected stimuli, analogous to inattentional blindness.

## Links
- Up: [[Sustained Attention]]
- Related: [[Vigilance Decrement]], [[Change Detection]]
