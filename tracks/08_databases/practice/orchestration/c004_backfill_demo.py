# Story:
# A daily sales pipeline missed two days. The dashboard is wrong until backfill repairs history.


def _run_interval(task, date_label, mode):
    print(f"[RUN] {task} {date_label} ({mode})")


def _show_missing(expected, completed):
    missing = [d for d in expected if d not in completed]
    print("Expected intervals:", expected)
    print("Completed intervals:", sorted(completed))
    print("Missing intervals:", missing)
    return missing


def run_backfill_demo():
    print("=" * 72)
    print("Scenario: daily sales aggregates with missed historical days")
    print("Regular run = current date on schedule.")
    print("Backfill = catch-up for old intervals only.")

    expected_intervals = ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
    completed_intervals = {"2024-01-01", "2024-01-04", "2024-01-05"}

    print("=" * 72)
    print("Normal scheduled runs (current time):")
    _run_interval("daily_sales", "2024-01-04", "scheduled")
    _run_interval("daily_sales", "2024-01-05", "scheduled")

    print("=" * 72)
    print("State before backfill:")
    missing = _show_missing(expected_intervals, completed_intervals)
    print("Downstream report completeness:", "incomplete (gaps)")

    print("=" * 72)
    print("Backfill plan: target only missing dates/partitions")
    backfill_targets = missing
    print("Backfill targets:", backfill_targets)
    for date_label in backfill_targets:
        _run_interval("daily_sales", date_label, "backfill")
        completed_intervals.add(date_label)

    print("=" * 72)
    print("Why not replay everything?")
    print("- Replaying all history is wasteful and can re-trigger downstream side effects.")
    print("- We only rerun missing or bad intervals.")

    print("=" * 72)
    print("State after backfill:")
    _show_missing(expected_intervals, completed_intervals)
    print("Downstream report completeness:", "complete (no gaps)")

    print("=" * 72)
    print("Summary:")
    print("- Scheduled runs handle current time.")
    print("- Backfills repair historical gaps.")
    print("- Scope selection keeps backfills safe and fast.")


if __name__ == "__main__":
    run_backfill_demo()

# Takeaway: Backfill targets missing history without confusing it with current runs.
