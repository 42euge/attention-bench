# Figure 2: Attention Threshold Heatmap

**Description:** Heatmap with models on y-axis (ordered by overall performance) and noise types on x-axis. Cell values show the attention threshold (highest noise ratio at ≥80% accuracy). Color scale from red (0:1) through yellow (10:1) to green (100:1).

**Visual pattern:**
- The "Unrelated" and "Related" columns are almost entirely green (100:1), except gemma-3-1b (red/orange).
- The "Adversarial" column shows a clear gradient from red (gemma-3-1b, 0:1) through orange (gemma-3-4b, 1:1), yellow (gemma-3-12b, 10:1), light green (deepseek-r1-0528, 50:1) to dark green (remaining models, 100:1).
- The asymmetry between left two columns (uniform green) and right column (gradient) visually encodes the paper's thesis.

**Alternative representation:** Bar chart with grouped bars per model, three bars per group (one per noise type), showing the threshold value. The adversarial bars create a staircase pattern while unrelated/related bars are uniform.
