# Kaggle Linking Guide -- AttentionBench

## Prerequisites

1. The repo `42euge/attention-bench` must be public on GitHub
2. All 4 task notebooks must be committed and pushed to `main`

## Step-by-Step: Create Each Kaggle Benchmark Task

For each task below, repeat these steps:

1. Go to https://www.kaggle.com/benchmarks/tasks/new
2. In the notebook editor: **File > Link to GitHub**
3. Select repo: `42euge/attention-bench`
4. Select the notebook path listed below
5. Set the task name as listed
6. Save and run to verify it executes without errors

> **Important:** Do NOT use `kaggle kernels push` -- that uploads to Kaggle Code, not Benchmarks.

---

### Task 1: Noise Filtering

- **Notebook path:** `tasks/noise_filtering/noise_filtering.ipynb`
- **Task name:** `Noise Filtering`
- **Expected runtime:** ~5-10 min (36 LLM calls)
- **Status:** Ready to link

### Task 2: Context Switching

- **Notebook path:** `tasks/context_switching/context_switching.ipynb`
- **Task name:** `Context Switching`
- **Expected runtime:** ~10-15 min (10 sequences, each with 60 items)
- **Status:** Ready to link

### Task 3: Change Blindness

- **Notebook path:** `tasks/change_blindness/change_blindness.ipynb`
- **Task name:** `Change Blindness`
- **Expected runtime:** ~5-10 min (45 LLM calls)
- **Status:** NEEDS RE-LINKING (path changed from earlier version). If previously linked, do **File > Link to GitHub** again to pull the updated path/content.

### Task 4: Mudsplash

- **Notebook path:** `tasks/mudsplash/mudsplash.ipynb`
- **Task name:** `Mudsplash`
- **Expected runtime:** ~5-10 min (45 LLM calls)
- **Status:** Ready to link

---

## After Linking All 4 Tasks

1. Go to https://www.kaggle.com/benchmarks/new
2. Create a new Benchmark named **AttentionBench**
3. Add all 4 tasks to the benchmark
4. Set benchmark to **private** (it will auto-publish after deadline)
5. Run the benchmark against available models to generate results

## Updating After Code Changes

When you push changes to GitHub:
1. Open each task's notebook on Kaggle
2. **File > Link to GitHub** -- it detects new commits and offers to pull
3. Re-run the task to regenerate results

## Linking Benchmark to Writeup

1. Go to your Kaggle Writeup
2. **Attachments > Add a link**
3. Paste the Benchmark URL
4. This is mandatory for submission
