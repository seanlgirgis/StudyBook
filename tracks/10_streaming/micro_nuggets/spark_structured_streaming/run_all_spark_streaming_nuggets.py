#!/usr/bin/env python3
"""
Run all Spark Structured Streaming micro-nuggets and report PASS/FAIL.

Usage:
    python run_all_spark_streaming_nuggets.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

NUGGET_DIR = Path(__file__).parent
TIMEOUT = 120  # seconds per script (Spark takes longer)

SCRIPTS = [
    "00_setup/00_prereq_check.py",
    "00_setup/01_seed_lab.py",
    "01_streaming_basics/01_streaming_basics.py",
    "02_event_time_and_windows/01_event_time_watermark.py",
    "03_stateful_processing/01_stateful_processing.py",
    "04_reliability_and_recovery/01_reliability_and_recovery.py",
    "05_kafka_to_lake_patterns/01_kafka_to_lake.py",
    "06_operations_and_tuning/01_operations_and_tuning.py",
    "07_interview_drills/01_interview_drills.py",
    "08_mini_capstone/01_mini_capstone.py",
]


def run_script(script_path: Path) -> tuple[bool, str, float]:
    """Run a single nugget script. Returns (passed, output_snippet, elapsed)."""
    start = time.perf_counter()
    try:
        # Use PYTHONIOENCODING to handle Spark's Unicode output
        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True, text=True, timeout=TIMEOUT,
            cwd=str(script_path.parent),
            env=env,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = time.perf_counter() - start
        passed = result.returncode == 0
        output = (result.stdout or "").strip()
        lines = output.splitlines()
        snippet = " | ".join(lines[-2:]) if lines else "(no output)"
        if result.stderr and not passed:
            err_lines = result.stderr.strip().splitlines()
            # Find the actual Python error (last traceback line)
            for line in reversed(err_lines):
                if line.strip().startswith(("Error:", "Exception:", "pyspark", "AttributeError", "SyntaxError", "UnicodeError")):
                    snippet = line.strip()[:120]
                    break
            else:
                snippet = err_lines[-1][:120] if err_lines else result.stderr[:120]
        return passed, snippet, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - start
        return False, f"TIMEOUT ({TIMEOUT}s)", elapsed
    except Exception as e:
        elapsed = time.perf_counter() - start
        return False, str(e)[:120], elapsed


def main():
    print("=" * 70)
    print("  Spark Structured Streaming — Full Validation")
    print("=" * 70)

    results = []
    for script_rel in SCRIPTS:
        script_path = NUGGET_DIR / script_rel
        if not script_path.exists():
            results.append((script_rel, False, "FILE NOT FOUND", 0))
            continue

        passed, snippet, elapsed = run_script(script_path)
        results.append((script_rel, passed, snippet, elapsed))

    print("\n" + "-" * 70)
    print(f"  {'Script':<55} {'Result':<6} {'Time':>6}")
    print("-" * 70)

    passed_count = 0
    failed = []
    for script_rel, passed, snippet, elapsed in results:
        status = "PASS" if passed else "FAIL"
        if passed:
            passed_count += 1
        else:
            failed.append(script_rel)
        print(f"  {script_rel:<55} {status:<6} {elapsed:>5.1f}s")
        if not passed:
            print(f"    → {snippet}")

    print("-" * 70)
    print(f"  Total: {len(results)}  |  Passed: {passed_count}  |  Failed: {len(failed)}")
    print("=" * 70)

    if failed:
        print("\n  Failed scripts:")
        for f in failed:
            print(f"    - {f}")
        sys.exit(1)
    else:
        print("\n  All nuggets passed! ✓")
        sys.exit(0)


if __name__ == "__main__":
    main()
