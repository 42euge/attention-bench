# AttentionBench

Benchmark for testing attention-like cognitive abilities in LLMs.

Part of the [Google DeepMind x Kaggle AGI Hackathon](https://www.kaggle.com/competitions/google-deepmind-agi-hackathon).

## Tasks

| Task | Description |
|---|---|
| **noise_filtering** | Extract answers from passages buried in increasing amounts of irrelevant text |
| **context_switching** | Measure accuracy cost of switching between task types within a sequence |
| **change_blindness** | Detect factual changes between two passage versions separated by filler content |
| **mudsplash** | Test whether emotionally salient distractors cause the model to miss factual changes |

Each task is a self-contained Kaggle notebook in `tasks/<task_name>/`.

## Writeup

See [writeup.md](writeup.md) for the full project writeup.

## Kaggle Benchmark

<!-- TODO: replace with actual URL once benchmark is public -->
[AttentionBench on Kaggle](https://www.kaggle.com/benchmarks/TODO)

## License

This project was created for the Google DeepMind x Kaggle AGI Hackathon.
