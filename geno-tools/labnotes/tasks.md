# Tasks

## Active
- [ ] run against multiple frontier models

## Backlog
- [ ] install kaggle-benchmarks SDK from source for local development
- [ ] analyze results & discriminatory power
- [ ] write up (max 1,500 words)
- [ ] create cover image & media
- [ ] submit on Kaggle

## Done

- [x] implement benchmark with kaggle-benchmarks SDK (attention_selective + attention_sustained tasks, answer parsing, flexible matching)
- [x] build dataset with verifiable answers (180 SIN items + 6 vigilance items = 186 total)
- [x] design task types with difficulty scaling (SIN: 6 ratios × 3 noise types; VIG: 3 task types × normal/oddball)
- [x] define benchmark hypothesis (attentional failure vs reasoning failure, isolated by constant task difficulty)
- [x] review track research notes and pick benchmark concept (AttentionBench: Signal-in-Noise Titration + Vigilance Decrement)
- [x] setup repo (requirements.txt, kaggle-benchmarks SDK, project skeleton)
