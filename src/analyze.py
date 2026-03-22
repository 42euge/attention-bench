"""Analyze AttentionBench results for discriminatory power.

Computes key metrics:
- Signal-in-Noise: attention threshold per model (noise ratio at 80% accuracy)
- Vigilance: decay onset per model (position where accuracy drops below 95%)
- Cross-model discrimination (performance spread)
"""

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).parent.parent / "results"
DATA_DIR = Path(__file__).parent.parent / "data"


# ============================================================
# Signal-in-Noise Analysis
# ============================================================

def analyze_sin(results_df: pd.DataFrame) -> pd.DataFrame:
    """Analyze Signal-in-Noise results.

    Expects columns: model, task_id, noise_type, noise_ratio, correct, total
    Returns per-model metrics including attention threshold.
    """
    results_df["accuracy"] = results_df["correct"] / results_df["total"]

    grouped = results_df.groupby(
        ["model", "noise_type", "noise_ratio"]
    )["accuracy"].mean().reset_index()

    # Compute attention threshold: highest ratio with >= 80% accuracy
    thresholds = []
    for (model, ntype), grp in grouped.groupby(["model", "noise_type"]):
        grp_sorted = grp.sort_values("noise_ratio")
        threshold = 0
        for _, row in grp_sorted.iterrows():
            if row["accuracy"] >= 0.80:
                threshold = row["noise_ratio"]
        thresholds.append({
            "model": model,
            "noise_type": ntype,
            "attention_threshold": threshold,
            "min_accuracy": grp_sorted["accuracy"].min(),
            "max_accuracy": grp_sorted["accuracy"].max(),
        })

    return pd.DataFrame(thresholds)


def sin_accuracy_curve(results_df: pd.DataFrame) -> pd.DataFrame:
    """Get accuracy by noise ratio for plotting."""
    results_df["accuracy"] = results_df["correct"] / results_df["total"]
    return results_df.groupby(
        ["model", "noise_type", "noise_ratio"]
    )["accuracy"].mean().reset_index()


# ============================================================
# Vigilance Analysis
# ============================================================

def analyze_vigilance_positions(response_text: str, answers: list[str],
                                 num_subtasks: int) -> list[bool]:
    """Parse response and return per-position correctness."""
    lines = response_text.strip().split("\n")
    parsed = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        cleaned = re.sub(r"^\d+[\.\)\:]\s*", "", line)
        if cleaned:
            parsed.append(cleaned)

    while len(parsed) < num_subtasks:
        parsed.append("")

    results = []
    for exp, act in zip(answers, parsed[:num_subtasks]):
        exp_lower = exp.lower().strip()
        act_lower = act.lower().strip()
        match = (exp_lower in act_lower) or (exp_lower == act_lower)
        if not match:
            exp_digits = re.sub(r"[,\s]", "", exp_lower)
            act_digits = re.sub(r"[,\s]", "", act_lower)
            match = (exp_digits == act_digits and exp_digits != "")
        results.append(match)

    return results


def compute_decay_metrics(position_correct: list[bool],
                           window: int = 10) -> dict:
    """Compute vigilance decay metrics from position-level results.

    Returns:
        overall_accuracy: float
        decay_onset: int (first window where accuracy < 95%), -1 if none
        accuracy_by_decile: list of 10 floats
        rolling_accuracy: list of floats (window-size rolling average)
    """
    n = len(position_correct)
    arr = np.array(position_correct, dtype=float)

    overall = arr.mean()

    # Accuracy by decile (10 equal bins)
    decile_size = n // 10
    deciles = []
    for i in range(10):
        start = i * decile_size
        end = start + decile_size if i < 9 else n
        deciles.append(float(arr[start:end].mean()))

    # Rolling accuracy
    rolling = []
    for i in range(n - window + 1):
        rolling.append(float(arr[i:i+window].mean()))

    # Decay onset: first window position where rolling accuracy < 0.95
    decay_onset = -1
    for i, acc in enumerate(rolling):
        if acc < 0.95:
            decay_onset = i
            break

    return {
        "overall_accuracy": float(overall),
        "decay_onset": decay_onset,
        "accuracy_by_decile": deciles,
        "rolling_accuracy": rolling,
    }


def analyze_vigilance(results: list[dict]) -> pd.DataFrame:
    """Analyze vigilance results across models.

    Expects list of dicts with: model, task_type, variant, position_correct
    Returns per-model vigilance metrics.
    """
    metrics = []
    for r in results:
        decay = compute_decay_metrics(r["position_correct"])
        metrics.append({
            "model": r["model"],
            "task_type": r["task_type"],
            "variant": r["variant"],
            **decay,
        })

    return pd.DataFrame(metrics)


# ============================================================
# Cross-model Discrimination
# ============================================================

def compute_discrimination(metric_df: pd.DataFrame,
                            model_col: str = "model",
                            metric_col: str = "attention_threshold") -> dict:
    """Compute discrimination metrics across models."""
    per_model = metric_df.groupby(model_col)[metric_col].mean()

    spread = per_model.max() - per_model.min()
    cv = per_model.std() / per_model.mean() if per_model.mean() > 0 else 0

    return {
        "metric": metric_col,
        "num_models": len(per_model),
        "spread": float(spread),
        "coefficient_of_variation": float(cv),
        "per_model": per_model.to_dict(),
        "mean": float(per_model.mean()),
        "std": float(per_model.std()),
    }


def print_summary(sin_thresholds: pd.DataFrame | None = None,
                   vig_metrics: pd.DataFrame | None = None):
    """Print a human-readable summary of benchmark results."""
    if sin_thresholds is not None:
        print("=" * 60)
        print("SIGNAL-IN-NOISE: Attention Thresholds")
        print("=" * 60)
        pivot = sin_thresholds.pivot_table(
            index="model", columns="noise_type",
            values="attention_threshold", aggfunc="mean"
        )
        print(pivot.to_string())
        print()

        disc = compute_discrimination(sin_thresholds)
        print(f"Spread: {disc['spread']:.1f}")
        print(f"CV: {disc['coefficient_of_variation']:.2f}")

    if vig_metrics is not None:
        print("\n" + "=" * 60)
        print("VIGILANCE: Decay Metrics")
        print("=" * 60)
        for _, row in vig_metrics.iterrows():
            print(f"\n{row['model']} — {row['task_type']} ({row['variant']})")
            print(f"  Overall accuracy: {row['overall_accuracy']:.1%}")
            print(f"  Decay onset: {row['decay_onset']}")
            print(f"  Accuracy by decile: {[f'{d:.0%}' for d in row['accuracy_by_decile']]}")


if __name__ == "__main__":
    print("Analysis module loaded.")
    print("Use analyze_sin() and analyze_vigilance() with evaluation results.")
    print("Use print_summary() for human-readable output.")
