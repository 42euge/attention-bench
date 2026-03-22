"""Parse Kaggle benchmark output and save structured results.

Usage:
    python src/parse_kaggle_output.py /tmp/kaggle-output

Reads the log file and any output files from a Kaggle benchmark run,
extracts all printed results, and saves structured data for analysis.
"""

import json
import sys
import re
import shutil
from pathlib import Path
from datetime import datetime

RESULTS_DIR = Path(__file__).parent.parent / "results"


def parse_log_file(log_path: Path) -> list[dict]:
    """Parse Kaggle JSON log file into structured entries."""
    with open(log_path) as f:
        logs = json.load(f)

    entries = []
    for entry in logs:
        data = entry.get("data", "").rstrip()
        if data:
            entries.append({
                "time": entry.get("time", 0),
                "stream": entry.get("stream_name", "stdout"),
                "text": data,
            })
    return entries


def extract_stdout(entries: list[dict]) -> str:
    """Get full stdout text from log entries."""
    return "\n".join(e["text"] for e in entries if e["stream"] == "stdout")


def extract_available_models(stdout: str) -> list[str]:
    """Extract model names from 'Available models: [...]' line."""
    match = re.search(r"Available models:\s*\[([^\]]+)\]", stdout)
    if match:
        raw = match.group(1)
        models = [m.strip().strip("'\"") for m in raw.split(",")]
        return [m for m in models if m]
    return []


def extract_sin_table(stdout: str) -> str:
    """Extract the Signal-in-Noise results table."""
    lines = stdout.split("\n")
    in_section = False
    table_lines = []
    for line in lines:
        if "Signal-in-Noise Results" in line:
            in_section = True
            table_lines.append(line)
            continue
        if in_section:
            if line.startswith("===") and "Attention Threshold" in line:
                break
            if line.startswith("===") and len(table_lines) > 1:
                break
            table_lines.append(line)
    return "\n".join(table_lines)


def extract_thresholds(stdout: str) -> list[dict]:
    """Extract attention threshold data from stdout."""
    thresholds = []
    lines = stdout.split("\n")
    in_section = False
    for line in lines:
        if "Attention Thresholds" in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("==="):
                break
            # Parse: "  model_name | noise_type | threshold = N:1"
            match = re.match(
                r"\s*(.+?)\s*\|\s*(\w+)\s*\|\s*threshold\s*=\s*(\d+):1",
                line
            )
            if match:
                thresholds.append({
                    "model": match.group(1).strip(),
                    "noise_type": match.group(2).strip(),
                    "threshold": int(match.group(3)),
                })
    return thresholds


def extract_vigilance_table(stdout: str) -> str:
    """Extract the Vigilance results section."""
    lines = stdout.split("\n")
    in_section = False
    table_lines = []
    for line in lines:
        if "Vigilance Results" in line:
            in_section = True
            table_lines.append(line)
            continue
        if in_section:
            if line.startswith("===") and "Vigilance" not in line:
                break
            table_lines.append(line)
    return "\n".join(table_lines)


def extract_stderr_errors(entries: list[dict]) -> list[str]:
    """Extract error messages from stderr."""
    errors = []
    for e in entries:
        if e["stream"] == "stderr" and ("error" in e["text"].lower() or "Error" in e["text"]):
            errors.append(e["text"])
    return errors


def save_results(output_dir: Path, run_label: str = None):
    """Parse Kaggle output dir and save structured results."""
    RESULTS_DIR.mkdir(exist_ok=True)

    if run_label is None:
        run_label = datetime.now().strftime("%Y%m%d_%H%M%S")

    run_dir = RESULTS_DIR / run_label
    run_dir.mkdir(exist_ok=True)

    # Find log file
    log_files = list(output_dir.glob("*.log"))
    if not log_files:
        print(f"ERROR: No .log file found in {output_dir}")
        return None

    log_path = log_files[0]
    print(f"Parsing log: {log_path.name}")

    # Parse logs
    entries = parse_log_file(log_path)
    stdout = extract_stdout(entries)

    # Save raw data
    shutil.copy(log_path, run_dir / "raw_log.json")
    (run_dir / "stdout.txt").write_text(stdout)

    # Extract structured data
    models = extract_available_models(stdout)
    thresholds = extract_thresholds(stdout)
    sin_table = extract_sin_table(stdout)
    vig_table = extract_vigilance_table(stdout)
    errors = extract_stderr_errors(entries)

    # Save structured results
    results = {
        "run_label": run_label,
        "parsed_at": datetime.now().isoformat(),
        "log_file": log_path.name,
        "available_models": models,
        "num_models": len(models),
        "thresholds": thresholds,
        "sin_table": sin_table,
        "vigilance_table": vig_table,
        "errors": errors,
        "num_log_entries": len(entries),
        "total_runtime_sec": entries[-1]["time"] if entries else 0,
    }
    (run_dir / "results.json").write_text(json.dumps(results, indent=2))

    # Copy any output files (CSVs, PNGs, JSONs besides the log)
    for f in output_dir.iterdir():
        if f.suffix in (".csv", ".png", ".json", ".ipynb") and f != log_path:
            shutil.copy(f, run_dir / f.name)

    # Print summary
    print(f"\n{'='*60}")
    print(f"RUN: {run_label}")
    print(f"{'='*60}")
    print(f"Models ({len(models)}): {models}")
    print(f"Runtime: {results['total_runtime_sec']:.0f}s")
    print(f"Log entries: {len(entries)}")
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors[:5]:
            print(f"  - {e[:200]}")

    print(f"\n--- SIN Results ---")
    print(sin_table or "(not found in logs)")

    print(f"\n--- Thresholds ---")
    for t in thresholds:
        print(f"  {t['model']:30s} | {t['noise_type']:12s} | {t['threshold']}:1")

    print(f"\n--- Vigilance ---")
    print(vig_table or "(not found in logs)")

    print(f"\nResults saved to: {run_dir}")
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/parse_kaggle_output.py <kaggle-output-dir> [run-label]")
        sys.exit(1)

    output_dir = Path(sys.argv[1])
    label = sys.argv[2] if len(sys.argv) > 2 else None
    save_results(output_dir, label)
