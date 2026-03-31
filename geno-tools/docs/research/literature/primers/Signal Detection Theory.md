# Signal Detection Theory

#primer #literature #math

## Intuition
Signal Detection Theory (SDT) separates a detector's ability to discriminate signal from noise (sensitivity) from its tendency to say "yes" vs. "no" (response criterion/bias). Applied to vigilance: is a model missing targets because it can't detect them (sensitivity decline) or because it's become conservative (criterion shift)?

## The Math

$$d' = z(\text{Hit Rate}) - z(\text{False Alarm Rate})$$

Where:
- $d'$ (d-prime) = sensitivity — higher means better discrimination
- $z()$ = inverse normal CDF (z-score)
- Hit Rate = P(say "yes" | target present)
- False Alarm Rate = P(say "yes" | target absent)

Response criterion:
$$c = -\frac{1}{2}[z(\text{Hit Rate}) + z(\text{False Alarm Rate})]$$

Where $c > 0$ means conservative (biased toward "no"), $c < 0$ means liberal.

## Worked Example
A vigilance task with 100 items (80 targets, 20 non-targets):
- Model correctly identifies 72/80 targets (HR = 0.90)
- Model falsely flags 4/20 non-targets (FAR = 0.20)
- d' = z(0.90) - z(0.20) = 1.28 - (-0.84) = 2.12
- c = -0.5 × (1.28 + (-0.84)) = -0.22 (slightly liberal)

After 50 more items:
- HR drops to 0.75, FAR stays at 0.20
- d' = z(0.75) - z(0.20) = 0.67 - (-0.84) = 1.51
- Sensitivity declined (d' dropped from 2.12 to 1.51) while criterion stayed similar

## Where It Shows Up
- [[Vigilance Decrement]] — decompose accuracy decline into sensitivity vs. criterion
- [[Change Detection]] — false alarm rate in change blindness is a criterion measure
- Human vigilance research universally uses SDT

## Common Gotchas
- d' assumes normal distributions of signal and noise
- Floor/ceiling hit rates (0 or 1) produce infinite z-scores — use correction (e.g., 1/2N adjustment)
- d' is independent of criterion (that's the point)

## Links
- Related: [[Vigilance Decrement]], [[Change Blindness Task]]
