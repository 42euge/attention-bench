# Attentional Blink

#attention #divided-attention #L1

After detecting a first target (T1) in a rapid sequence, humans show a ~200-500ms window where a second target (T2) is missed. This benchmark tests whether LLMs show an analogous temporal recovery limitation.

## In Human Cognition
Raymond, Shapiro & Arnell (1992) discovered the attentional blink: when two targets appear in rapid serial visual presentation (RSVP), T2 detection drops dramatically at lags 2-5 (~200-500ms). Paradoxically, lag-1 sparing often occurs (T2 detected immediately after T1).

## LLM Analogue
Present a stream of sentences with two category targets (e.g., animals + cities) embedded among distractors. Vary the number of distractors between T1 and T2 (lag). If models show reduced T2 accuracy at short lags, they exhibit an attentional blink analog.

## Key Questions
- Do LLMs show the classic blink curve (dip at lags 2-5)?
- Is there lag-1 sparing?
- Does the blink depend on T1/T2 category similarity?

## Links
- Up: [[Divided Attention]]
- Down: [[Attentional Blink Task]]
- Related: [[Dual-Task Interference]], [[Selective Attention]]
