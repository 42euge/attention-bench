# Final Submission Review — AttentionBench

**Evaluator:** Supercharge Cycle 11
**Date:** 2026-03-31
**Verdict:** CONDITIONALLY READY — needs results filled in after Kaggle runs

---

## 1. Writeup (writeup.md)

### Word count: ~1,386 (PASS — under 1,500 limit)

### Template sections (all 9 present):
1. Project Name -- present
2. Your Team -- present
3. Problem Statement -- present, strong
4. Task & benchmark construction -- present, detailed
5. Dataset -- present
6. Technical details -- present
7. Results, insights, and conclusions -- present (with placeholders)
8. Organizational affiliations -- present
9. References & citations -- present

### PLACEHOLDERs: 5 total
All are clearly labeled `[PLACEHOLDER: ...]` in Section 7:
1. Noise filtering accuracy curves
2. Context switching cost table
3. Change blindness detection rates
4. Mudsplash capture effect
5. Cross-model comparison

These MUST be filled with actual results before submission. The "Expected pattern" text beneath each placeholder is well-written and can stay as hypothesis framing, but the placeholders themselves need real data or figures.

### References check:
All 5 references are real, well-cited papers:
- Morris et al. (2023) arXiv:2311.02462 -- Google DeepMind AGI levels paper. Real.
- Rensink et al. (1997) Psychological Science 8(5) -- canonical change blindness paper. Real.
- O'Regan et al. (1999) Nature 398(6722) -- mudsplash paper. Real.
- Monsell (2003) TICS 7(3) -- task switching review. Real.
- Broadbent (1958) Perception and Communication -- foundational selective attention book. Real.

### Grammar/clarity:
- Writing is excellent throughout. Clear, confident, well-structured.
- One minor note: "there is no serial spotlight, no limited-capacity buffer, no moment where information goes unprocessed" -- "where" could be "when" for temporal precision, but this is stylistic, not wrong.
- The "So what?" paragraph at the end of Section 7 is strong and ties the benchmark back to practical implications.
- No typos found.

**WRITEUP GRADE: A- (loses points only for unfilled placeholders, which is expected pre-run)**

---

## 2. README.md

- Clearly explains the project and its 4 tasks in a concise table.
- Links to writeup.
- Has a TODO placeholder for the Kaggle benchmark URL: `https://www.kaggle.com/benchmarks/TODO`
- Missing: no "Quick Start" or instructions for running locally (not required but would help community engagement).
- Missing: no cover image or visual hook for Kaggle community upvotes.

**README GRADE: B+ (functional but could be more inviting for community votes)**

---

## 3. Notebook Sanity Check (4 final notebooks)

### noise_filtering
- `@kbench.task(name="noise_filtering", ...)` -- matches folder name `tasks/noise_filtering/` ✓
- Description: "Find answers to questions about a passage buried in increasing amounts of noise text" -- clear ✓
- Title markdown: `> **Task name:** \`Noise Filtering\`` -- present ✓

### context_switching
- `@kbench.task(name="context_switching", ...)` -- matches folder name ✓
- Description: "Measure task-switching cost when alternating between number, country, and spelling tasks" -- clear ✓
- Title markdown: `> **Task name:** \`Context Switching\`` -- present ✓

### change_blindness
- `@kbench.task(name="change_blindness", ...)` -- matches folder name ✓
- Description: "Detect subtle factual changes between two passage versions separated by a disruptor paragraph" -- clear ✓
- Title markdown: `> **Task name:** \`Change Blindness\`` -- present ✓

### mudsplash
- `@kbench.task(name="mudsplash", ...)` -- matches folder name ✓
- Description: "Does salient/emotional disruptor content cause models to miss factual changes?" -- clear ✓
- Title markdown: `> **Task name:** \`Mudsplash\`` -- present ✓

**NOTEBOOKS GRADE: A (all 4 pass all checks)**

---

## 4. Docs Completeness

Each of the 4 final tasks has a `docs/<name>.md` file inside its task directory:
- `tasks/noise_filtering/docs/noise_filtering.md` ✓
- `tasks/context_switching/docs/context_switching.md` ✓
- `tasks/change_blindness/docs/change_blindness.md` ✓
- `tasks/mudsplash/docs/mudsplash.md` ✓

### Format consistency:
All 4 docs follow the same structure:
1. `# Task Name`
2. `## What it tests`
3. `## The setup`
4. `## What to expect when you run it` (with Good results / What discriminates / Metrics / Plot subsections)
5. `## Design`

Minor inconsistency: `change_blindness.md` uses slightly more casual language ("Can a model spot what changed between two versions of code or a ticket when there's unrelated stuff in between?") compared to the more formal tone of the others. Not a blocker.

Note: there is NO root-level `docs/` directory. The git status showed `docs/` as untracked, but it does not exist on disk. This appears to be a stale git index entry -- harmless.

**DOCS GRADE: A-**

---

## 5. Repository Structure

### Clean structure:
```
tasks/
  noise_filtering/      ← FINAL
  context_switching/     ← FINAL
  change_blindness/      ← FINAL
  mudsplash/            ← FINAL
  attentional_blink/    ← STALE (cut task)
  continuous_performance/ ← STALE (cut task)
  dual_task_interference/ ← STALE (cut task)
  vigilance_decrement/  ← STALE (cut task)
```

### Issues found:

**STALE TASK DIRECTORIES (4):** `attentional_blink`, `continuous_performance`, `dual_task_interference`, `vigilance_decrement` are cut tasks that still exist in the repo. These are untracked (not committed), so they will not appear on Kaggle/GitHub, but they clutter the local workspace.

**STALE DATA FILES:** `data/` directory contains JSON files for cut tasks (`attentional_blink.json`, `continuous_performance.json`, `dual_task_interference.json`) plus a `_generate_datasets.py` and `README.md`. All untracked.

**`results/` directories:** `v3_single_model/`, `v4_multi_model/`, `v5_orthogonal/` -- old result runs. Untracked.

**`paper/` directory:** Contains a LaTeX paper with build artifacts (`.aux`, `.log`, `.bbl`, etc.). The `.gitignore` covers some of these but `paper.tex`, `paper.pdf`, `paper.md`, `references.bib`, `figures/` are not ignored. All untracked.

**`community/` directory:** Contains community analysis notebooks (`gsm_ic_distraction.ipynb`, `needle_in_haystack.ipynb`). Untracked.

**`media/video/`:** Contains a Manim video (`final_video.mp4`, `scene.py`, `transcript.md`). Partially gitignored.

### .gitignore coverage:
- Covers Python artifacts, virtualenvs, DS_Store, .env, kaggle-benchmarks SDK, task/run JSON files ✓
- Covers Manim `media/video/media/` build artifacts ✓
- Covers some LaTeX artifacts ✓
- Does NOT cover: stale task directories, stale data files, community notebooks, paper source files, results directories. However, since none of these are staged/committed, they won't appear in the submission.

**REPO STRUCTURE GRADE: B (functional but cluttered locally; clean on remote)**

---

## 6. What's Missing — Pre-Submission Checklist

### MUST DO (manual, blocking):

1. **Run all 4 notebooks on Kaggle** and collect results
   - Each notebook must be run through the Kaggle Benchmarks platform
   - Verify each notebook runs without errors end-to-end

2. **Fill in the 5 PLACEHOLDERs in writeup.md** with actual results
   - Insert accuracy tables/numbers from Kaggle runs
   - Replace `[PLACEHOLDER: ...]` markers with real data
   - Keep the "Expected pattern" analysis, update if results differ from predictions

3. **Update README.md** Kaggle benchmark URL
   - Replace `https://www.kaggle.com/benchmarks/TODO` with actual URL

4. **Create/upload Kaggle Benchmark**
   - Link all 4 task notebooks to the benchmark
   - Set benchmark to private until deadline
   - Verify the benchmark page looks correct

5. **Upload writeup to Kaggle** as the competition submission writeup

6. **Cover image for media gallery** -- competition says cover image is required
   - Currently no cover image exists in the repo

### SHOULD DO (improves quality):

7. **Clean up stale directories** locally (or add to .gitignore):
   - `tasks/{attentional_blink,continuous_performance,dual_task_interference,vigilance_decrement}/`
   - `data/` (stale JSON files)
   - `results/v3_single_model/`, `results/v4_multi_model/`, `results/v5_orthogonal/`

8. **Add a results figure to README.md** after runs complete -- a single chart showing the key finding would dramatically improve community appeal and upvotes.

9. **Tone consistency in change_blindness docs** -- minor, optional.

### RISKS:

- **Discriminatory power (15% of score):** Until notebooks are run on Kaggle, we don't know if the tasks actually produce a meaningful gradient across models. The experimental designs are sound, but if all models score 100% or 0% on any task, that task fails the discriminatory power criterion.
- **Word count margin:** At ~1,386 words, the writeup has ~114 words of margin. Filling in 5 placeholders with actual numbers will likely add 100-200 words. This could push over 1,500 if not careful. Recommend keeping placeholder replacements brief (tables or bullet points, not prose).
- **Community upvotes (15% of score):** The README is functional but not visually compelling. A cover image and a "hero" result chart would significantly help.

---

## Summary

| Area | Grade | Status |
|---|---|---|
| Writeup | A- | 5 placeholders need results |
| README | B+ | TODO URL, no cover image |
| Notebooks (4) | A | All pass sanity checks |
| Docs (4) | A- | Complete, consistent format |
| Repo structure | B | Clean on remote, cluttered locally |

**Overall: The benchmark is well-designed, well-written, and structurally sound. The sole blocker is running notebooks on Kaggle and filling in results. Everything else is polish.**
