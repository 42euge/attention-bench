# Tasks

## Active
- [ ] fix parsing bugs and re-run with higher ratios (50:1, 100:1)
- [ ] analyze results & discriminatory power (v4 data in results/v4_multi_model/)

## Backlog
- [ ] write up (max 1,500 words)
- [ ] create cover image & media
- [ ] submit on Kaggle

## Done

- [x] run v4 multi-model benchmark (27 models, 1134 LLM calls, 70min runtime — found ceiling effect + parsing bugs)
- [x] run against multiple frontier models
- [x] implement benchmark with kaggle-benchmarks SDK (attention_selective + attention_sustained tasks, answer parsing, flexible matching)
- [x] build dataset with verifiable answers (180 SIN items + 6 vigilance items = 186 total)
- [x] design task types with difficulty scaling (SIN: 6 ratios × 3 noise types; VIG: 3 task types × normal/oddball)
- [x] define benchmark hypothesis (attentional failure vs reasoning failure, isolated by constant task difficulty)
- [x] review track research notes and pick benchmark concept (AttentionBench: Signal-in-Noise Titration + Vigilance Decrement)
- [x] setup repo (requirements.txt, kaggle-benchmarks SDK, project skeleton)
