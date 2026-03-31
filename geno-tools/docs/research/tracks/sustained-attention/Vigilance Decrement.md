# Vigilance Decrement

#attention #sustained-attention #L1

The decline in detection performance over time during prolonged monitoring tasks. In human cognition, this is one of the most robust findings in attention research, first documented by Mackworth (1948) in WWII radar operators.

## Definition
Vigilance decrement is the decline in hit rate (or increase in miss rate) for target detection as time-on-task increases. In human studies, performance typically drops 10-15% over 30 minutes of sustained monitoring.

## In LLMs
No existing benchmark directly tests vigilance decrement. Adjacent findings:
- Chen et al. (2026, arXiv:2603.22608) found performance collapse when processing 100+ identical instances
- "Lost in the Middle" shows positional degradation but confounds attention with position
- Context Rot (2025) documents universal degradation with length, identifying three mechanisms

## Unadapted Cognitive Paradigms
- **Continuous Performance Test (CPT)** — respond to targets among non-targets over extended periods
- **SART** — withhold response to rare stimuli after developing automatic response pattern
- **Mackworth Clock Task** — detect rare signals during monotonous monitoring
- **Signal Detection Theory (SDT)** — decompose performance into sensitivity (d') vs. criterion (beta)

## Links
- Up: [[Sustained Attention]]
- Down: [[Vigilance Decrement Task]]
- Related: [[Positional Bias]], [[Monotony and Automaticity]]
