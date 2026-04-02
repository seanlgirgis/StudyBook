# Story:
# A lakehouse table uses a transaction log to commit file additions atomically.
# Readers use snapshots to see a consistent view, even with concurrent writers.

TRANSACTION_LOG = []
DATA_FILES = []


def _snapshot():
    if not TRANSACTION_LOG:
        return {"version": -1, "files": []}
    latest = TRANSACTION_LOG[-1]
    return {"version": latest["version"], "files": list(latest["files"])}


def _commit(new_files):
    current = _snapshot()
    next_version = current["version"] + 1
    merged = current["files"] + new_files
    TRANSACTION_LOG.append({"version": next_version, "files": merged})
    for f in new_files:
        DATA_FILES.append(f)
    print(f"COMMIT v{next_version}: add {new_files}")


def run_acid_on_object_storage_demo():
    print("=" * 72)
    print("Scenario: ACID on object storage (Delta Lake concepts)")

    print("\nWriter A commits new data files")
    _commit(["part-000.parquet", "part-001.parquet"])

    print("\nReader takes snapshot")
    snap1 = _snapshot()
    print(snap1)

    print("\nWriter B commits concurrently")
    _commit(["part-002.parquet"])

    print("\nReader re-reads snapshot (still consistent)")
    print(snap1)

    print("\nReader refreshes snapshot")
    snap2 = _snapshot()
    print(snap2)

    print("\nSummary")
    print("- Transaction log records atomic commits.")
    print("- Readers use snapshots for consistent views.")
    print("- Concurrent writers append new versions safely.")


if __name__ == "__main__":
    run_acid_on_object_storage_demo()

# Takeaway: Transaction logs + snapshots provide ACID-style behavior on object storage.
