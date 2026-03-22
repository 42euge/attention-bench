"""AttentionBench task definitions using kaggle-benchmarks SDK.

Two task types:
1. attention_selective — Signal-in-Noise (SIN) selective attention
2. attention_sustained — Vigilance Decrement sustained attention
"""

import json
import re
from pathlib import Path

import pandas as pd

try:
    import kaggle_benchmarks as kbench
except ImportError:
    kbench = None
    print(
        "kaggle_benchmarks not installed. "
        "Install from https://github.com/Kaggle/kaggle-benchmarks"
    )

DATA_DIR = Path(__file__).parent.parent / "data"


def load_sin_data() -> pd.DataFrame:
    """Load Signal-in-Noise dataset."""
    with open(DATA_DIR / "signal_in_noise.json") as f:
        return pd.DataFrame(json.load(f))


def load_vigilance_data() -> pd.DataFrame:
    """Load Vigilance dataset."""
    with open(DATA_DIR / "vigilance.json") as f:
        return pd.DataFrame(json.load(f))


def parse_numbered_answers(response: str, count: int) -> list[str]:
    """Parse numbered answers from model response.

    Handles formats like:
        1. answer
        1) answer
        1: answer
        or just one answer per line
    """
    lines = response.strip().split("\n")
    answers = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Strip numbering prefix: "1. ", "1) ", "1: ", etc.
        cleaned = re.sub(r"^\d+[\.\)\:]\s*", "", line)
        if cleaned:
            answers.append(cleaned)

    # If we got more than expected, truncate; if fewer, pad with empty
    while len(answers) < count:
        answers.append("")

    return answers[:count]


def check_answer(expected: str, actual: str) -> bool:
    """Check if actual answer matches expected, with flexible matching."""
    expected_lower = expected.lower().strip()
    actual_lower = actual.lower().strip()

    # Exact match
    if expected_lower == actual_lower:
        return True

    # Expected is contained in actual
    if expected_lower in actual_lower:
        return True

    # Strip common prefixes/suffixes for number matching
    # Handle "approximately 7 minutes" matching "7 minutes"
    expected_core = re.sub(r"^(approximately|about|roughly|around)\s+", "", expected_lower)
    if expected_core in actual_lower:
        return True

    # Handle number formatting: "2,400" matches "2400" or "2,400"
    expected_digits = re.sub(r"[,\s]", "", expected_lower)
    actual_digits = re.sub(r"[,\s]", "", actual_lower)
    if expected_digits == actual_digits and expected_digits:
        return True

    return False


# ============================================================
# SDK Task Definitions
# ============================================================

if kbench is not None:

    @kbench.task(name="attention_selective")
    def attention_selective(llm, prompt: str, answers: str, num_questions: int) -> tuple[int, int]:
        """Signal-in-Noise selective attention task.

        Returns (correct, total) for the question set.
        """
        response = llm.prompt(prompt)
        # answers is JSON-encoded list
        expected = json.loads(answers) if isinstance(answers, str) else answers
        num_q = int(num_questions)
        parsed = parse_numbered_answers(response, num_q)

        correct = sum(
            1 for exp, act in zip(expected, parsed)
            if check_answer(exp, act)
        )
        return (correct, num_q)

    @kbench.task(name="attention_sustained")
    def attention_sustained(llm, prompt: str, answers: str, num_subtasks: int) -> tuple[int, int]:
        """Vigilance Decrement sustained attention task.

        Returns (correct, total) for the full sequence.
        """
        response = llm.prompt(prompt)
        expected = json.loads(answers) if isinstance(answers, str) else answers
        num_sub = int(num_subtasks)
        parsed = parse_numbered_answers(response, num_sub)

        correct = sum(
            1 for exp, act in zip(expected, parsed)
            if check_answer(exp, act)
        )
        return (correct, num_sub)


def prepare_sin_eval_df() -> pd.DataFrame:
    """Prepare SIN data for SDK evaluation."""
    df = load_sin_data()
    # Convert answers list to JSON string for SDK compatibility
    df["answers"] = df["answers"].apply(json.dumps)
    return df[["task_id", "prompt", "answers", "num_questions"]]


def prepare_vigilance_eval_df() -> pd.DataFrame:
    """Prepare vigilance data for SDK evaluation."""
    df = load_vigilance_data()
    df["answers"] = df["answers"].apply(json.dumps)
    return df[["task_id", "prompt", "answers", "num_subtasks"]]


def run_evaluation(models: list[str] | None = None, dimension: str = "both",
                   n_jobs: int = 2):
    """Run benchmark evaluation against specified models.

    Args:
        models: List of model identifiers. If None, uses default LLM.
        dimension: "selective", "sustained", or "both"
        n_jobs: Parallel jobs for evaluation
    """
    if kbench is None:
        print("kaggle_benchmarks SDK required for evaluation.")
        return

    llms = [kbench.llms[m] for m in models] if models else [kbench.llm]
    results = {}

    if dimension in ("selective", "both"):
        print("Evaluating Signal-in-Noise (selective attention)...")
        sin_df = prepare_sin_eval_df()
        runs = attention_selective.evaluate(
            llm=llms,
            evaluation_data=sin_df,
            n_jobs=n_jobs,
        )
        results["selective"] = runs.as_dataframe()
        print(f"  {len(results['selective'])} results collected.")

    if dimension in ("sustained", "both"):
        print("Evaluating Vigilance Decrement (sustained attention)...")
        vig_df = prepare_vigilance_eval_df()
        runs = attention_sustained.evaluate(
            llm=llms,
            evaluation_data=vig_df,
            n_jobs=n_jobs,
        )
        results["sustained"] = runs.as_dataframe()
        print(f"  {len(results['sustained'])} results collected.")

    return results


if __name__ == "__main__":
    # Quick local test without SDK
    print("AttentionBench task definitions loaded.")
    print(f"SIN items: {len(load_sin_data())}")
    print(f"Vigilance items: {len(load_vigilance_data())}")
    print("\nTo run evaluation, use run_evaluation() with kaggle_benchmarks SDK.")
