#!/usr/bin/env python3
"""
Run-all is intentionally disabled for Spark Structured Streaming nuggets.

These scripts include client/server style Spark jobs and child JVM processes
that may not terminate cleanly in batch-runner mode on Windows.
"""
from __future__ import annotations

import sys


def main() -> int:
    print("run_all is not acceptable for this Spark Structured Streaming lane.")
    print("Reason: these nuggets use client/server-style Spark execution,")
    print("and batch run-all can hang on long-lived JVM child processes.")
    print("")
    print("Use one-by-one execution instead:")
    print("  python .\\00_setup\\00_prereq_check.py")
    print("  python .\\00_setup\\01_seed_lab.py")
    print("  python .\\01_streaming_basics\\01_streaming_basics.py")
    print("  python .\\02_event_time_and_windows\\01_event_time_watermark.py")
    print("  python .\\03_stateful_processing\\01_stateful_processing.py")
    print("  python .\\04_reliability_and_recovery\\01_reliability_and_recovery.py")
    print("  python .\\05_kafka_to_lake_patterns\\01_kafka_to_lake.py")
    print("  python .\\06_operations_and_tuning\\01_operations_and_tuning.py")
    print("  python .\\07_interview_drills\\01_interview_drills.py")
    print("  python .\\08_mini_capstone\\01_mini_capstone.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

