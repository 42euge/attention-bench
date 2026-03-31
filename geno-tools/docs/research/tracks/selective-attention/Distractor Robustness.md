# Distractor Robustness

#attention #selective-attention #L1

How well can models maintain correct reasoning when presented with misleading or irrelevant context alongside the actual task?

## Definition
Distractor robustness measures the delta between a model's performance on a clean task vs. the same task with added distractors. A perfectly robust model shows zero delta; real models show significant degradation.

## Key Findings
- GSM-IC: adding 1-2 irrelevant sentences causes 20-40% accuracy drops on grade-school math
- GSM-Symbolic: a single "seemingly relevant but unnecessary" clause causes up to 65% drops
- GSM-DC (2025): controlled symbolic reasoning graphs show sensitivity to both reasoning path selection and arithmetic accuracy
- Distractor Injection Attacks (2025, arXiv:2510.16259): adversarial reasoning tasks can hijack model focus

## Cognitive Load Theory Connection
[[CogniLoad (2025)]] applies Cognitive Load Theory to LLMs — separating intrinsic difficulty (the task itself) from extraneous load (distractors). Found that task length is the dominant constraint, with U-shaped responses to distractor density.

## Links
- Up: [[Selective Attention]]
- Down: [[GSM-IC (2023)]], [[GSM-Symbolic (2024)]]
- Related: [[Signal-to-Noise Filtering]], [[Adversarial Noise]]
