# Attention Benchmark

## Track

**Attention**: Can the model focus on what matters and ignore what doesn't?

## Competition Context

This benchmark is part of the Google DeepMind x Kaggle AGI Hackathon. Read the full competition rules and context in:

- `../../competition-info/overview.md` — competition overview and motivation
- `../../competition-info/evaluation.md` — evaluation criteria and scoring weights
- `../../competition-info/submission.md` — submission requirements and writeup template
- `../../competition-info/tracks.md` — all track descriptions, example evaluation targets, and prizes

## Research

Prior research notes for this track and related ideas are in:

- `../../research/attention/` — track-specific research notes and benchmark ideas
- `../../research/concepts/` — cross-cutting concepts
- `../../research/reference/` — reference materials

## Key Principles

- The benchmark must isolate a specific cognitive ability within the Attention track
- Tasks must have verifiably correct answers (no ambiguity)
- Must show discriminatory power: a meaningful gradient of performance across models
- Answer the question: "What can this benchmark tell us about model behavior that we could not see before?"

## Architecture

### Kaggle Benchmarks structure

Kaggle Benchmarks has two entities:
- **Tasks** — individual evaluation notebooks, each with a `@kbench.task` decorator
- **Benchmarks** — collections of tasks grouped together

We create one Task per notebook, then group them into a single Benchmark.

### Task notebooks must be self-contained

Each notebook in `tasks/` is a standalone Kaggle kernel. It must:
- Generate its own data inline (fixed seed for reproducibility)
- Define its own helper functions (parsing, answer checking)
- Define exactly one `@kbench.task` function
- Run `.evaluate(llm=kbench.llm, evaluation_data=df)` against the default model
- Include analysis/plotting at the end

**Do NOT** create shared libraries, external data dependencies, or combined benchmark notebooks. Each task notebook must run independently on Kaggle with zero external files.

### What NOT to create

- No `src/` modules or shared code — inline everything per notebook
- No combined "master" benchmark notebook — Kaggle groups tasks into benchmarks via the UI
- No `notebooks/` directory — all task notebooks live in `tasks/`
- No external JSON data files that notebooks depend on — generate data inline

### Deploying to Kaggle

The repo must be public on GitHub. To deploy task notebooks:

1. Create a Task at https://www.kaggle.com/benchmarks/tasks/new
2. In the Kaggle notebook editor: **File → Link to GitHub** → select the notebook from `42euge/attention-bench`
3. To pull updates after pushing to GitHub: **File → Link to GitHub** again — it detects new commits and offers to pull

The `kaggle kernels push` CLI uploads to Kaggle **Code** (regular notebooks), NOT to Benchmarks. Do not use it for benchmark tasks.

### Passage style

Keep passages short and everyday (bakery, bridge, farm — not dense scientific text). A human should be able to read a passage and verify the change in under 10 seconds.
