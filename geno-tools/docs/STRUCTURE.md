# Codebase Structure

## Directory Layout

```
attention-bench/
├── tasks/                      # One folder per benchmark task
│   ├── noise_filtering/
│   │   ├── noise_filtering.ipynb   # Self-contained Kaggle benchmark notebook
│   │   ├── docs/                   # Task documentation
│   │   ├── results/                # Raw outputs from Kaggle runs
│   │   └── review/                 # Review files with analysis and next steps
│   ├── context_switching/
│   ├── change_blindness/
│   ├── mudsplash/
│   ├── attentional_blink/          # Archived
│   ├── continuous_performance/     # Archived
│   ├── dual_task_interference/     # Archived
│   └── vigilance_decrement/        # Archived
├── community/                  # Community reference notebooks
├── media/                      # Images and video for submission
├── paper/                      # LaTeX paper and figures
├── geno-tools/
│   ├── labnotes/               # Development history and task tracking
│   ├── supercharge/            # Supercharge session logs
│   └── docs/                   # This documentation
├── .env.example                # Template for Kaggle API credentials
├── requirements.txt            # Python dependencies
├── writeup.md                  # Kaggle submission writeup
└── CLAUDE.md                   # AI assistant context and instructions
```

## Key Design Decisions

### Self-contained task notebooks

Each notebook in `tasks/<task_name>/` is a standalone Kaggle kernel. It:
- Generates its own data inline (fixed seed for reproducibility)
- Defines its own helper functions (parsing, answer checking)
- Defines exactly one `@kbench.task` function
- Runs `.evaluate(llm=[kbench.llm], evaluation_data=df)`

There is no shared `src/` directory, no external data files, and no combined benchmark notebook. Each task runs independently on Kaggle with zero external dependencies.

### Active vs archived tasks

The 4 active tasks (noise_filtering, context_switching, change_blindness, mudsplash) are deployed to Kaggle Benchmarks. The 4 archived tasks remain in the repo but are not part of the benchmark.

## Dependencies

- **kaggle-benchmarks** — Kaggle's SDK for benchmark definition and evaluation
- **matplotlib** — Visualization of accuracy curves and discrimination metrics
