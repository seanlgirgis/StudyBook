# ============================================================
# Topic   : Delta Lake for Data Engineers
# File    : 02_time_travel_and_versioning.py
# Covers  : Time travel, versioning, history, restore, diff
# Prereqs : pip install deltalake pandas pyarrow
# Run     : python 02_time_travel_and_versioning.py
# ============================================================

from deltalake import DeltaTable, write_deltalake
import pandas as pd
from pathlib import Path
import os
import random
from datetime import datetime, timezone


def get_output_dir() -> Path:
    """Return platform output dir. Create if missing."""
    default = Path("C:/tmp/studybook/delta" if os.name == "nt" else "/tmp/studybook/delta")
    out = Path(os.getenv("OUTPUT_DIR", str(default)))
    out.mkdir(parents=True, exist_ok=True)
    return out


def generate_customers(n: int, seed: int) -> pd.DataFrame:
    """Generate deterministic customer data."""
    random.seed(seed)

    regions = ["NA", "EU", "APAC", "LATAM"]

    data = []
    for i in range(n):
        cid = f"CUST-{i:06d}"
        spend = round(random.uniform(100, 50000), 2)

        data.append(
            {
                "customer_id": cid,
                "name": f"Customer {i}",
                "region": random.choice(regions),
                "spend": spend,
            }
        )

    return pd.DataFrame(data)


def setup_versioned_table(path: Path) -> None:
    """
    Create 4 versions of the table.

    WHY multiple versions:
    Delta keeps every commit. This enables auditing, rollback, and debugging.
    """
    if path.exists():
        import shutil
        shutil.rmtree(path)

    # v0
    df0 = generate_customers(500, seed=1)
    write_deltalake(str(path), df0, mode="overwrite")
    print("Created version 0")

    # v1
    df1 = generate_customers(200, seed=2)
    write_deltalake(str(path), df1, mode="append")
    print("Created version 1")

    # v2 (simulate update via overwrite)
    df_full = DeltaTable(str(path)).to_pandas()

    idx = random.sample(range(len(df_full)), 50)
    df_full.loc[idx, "region"] = "UPDATED"

    write_deltalake(str(path), df_full, mode="overwrite")
    print("Created version 2 (overwrite update)")

    # v3
    df3 = generate_customers(100, seed=3)
    write_deltalake(str(path), df3, mode="append")
    print("Created version 3")


def read_version(path: Path, version: int) -> pd.DataFrame:
    """
    Read a specific version.

    WHY:
    "What did data look like at version X?" → time travel.
    """
    dt = DeltaTable(str(path))
    dt.load_as_version(version)
    df = dt.to_pandas()

    print(f"Version {version}: {len(df)} rows")
    return df
    

def read_at_timestamp(path: Path, timestamp: str) -> pd.DataFrame:
    """
    Read table at a timestamp.

    WHY:
    Regulatory auditing (e.g., GDPR, finance).
    """
    dt = DeltaTable(str(path))

    try:
        dt.load_as_version(timestamp)
        df = dt.to_pandas()
        print(f"Read at {timestamp}: {len(df)} rows")
        return df
    except Exception:
        raise ValueError(f"Timestamp {timestamp} is before table creation or invalid")


def get_table_history(path: Path) -> pd.DataFrame:
    """
    Return commit history.

    WHY:
    Full audit trail of all writes.
    """
    dt = DeltaTable(str(path))
    history = pd.DataFrame(dt.history())

    if not history.empty:
        print(f"{'version':<8} | {'timestamp':<20} | {'operation':<10} | {'added':<5} | {'removed':<5}")
        print("-" * 70)

        for _, row in history.iterrows():
            print(
                f"{row['version']:<8} | "
                f"{str(row['timestamp']):<20} | "
                f"{row['operation']:<10} | "
                f"{row.get('numAddedFiles', 0):<5} | "
                f"{row.get('numRemovedFiles', 0):<5}"
            )

    return history


def diff_versions(path: Path, v1: int, v2: int) -> dict:
    """
    Compare two versions.

    WHY:
    Understand data drift, debugging pipelines.
    """
    df1 = read_version(path, v1)
    df2 = read_version(path, v2)

    rows_added = max(0, len(df2) - len(df1))
    rows_removed = max(0, len(df1) - len(df2))

    result = {
        "v1_rows": len(df1),
        "v2_rows": len(df2),
        "rows_added": rows_added,
        "rows_removed": rows_removed,
    }

    print(f"Diff v{v1} → v{v2}: {result}")
    return result


def restore_to_version(path: Path, version: int) -> None:
    """
    Restore table to a previous version.

    WHY:
    Recovery from bad writes without needing backups.
    """
    dt = DeltaTable(str(path))

    before_rows = len(dt.to_pandas())
    before_version = dt.version()

    dt.restore(version)

    dt_after = DeltaTable(str(path))
    after_rows = len(dt_after.to_pandas())
    after_version = dt_after.version()

    print(f"Before restore: version={before_version}, rows={before_rows}")
    print(f"After restore:  version={after_version}, rows={after_rows}")


def main():
    path = get_output_dir() / "customers_versioned"

    print("\n=== SETUP 4 VERSIONS ===")
    setup_versioned_table(path)

    print("\n=== TABLE HISTORY ===")
    get_table_history(path)

    print("\n=== TIME TRAVEL BY VERSION ===")
    for v in [0, 1, 2, 3]:
        read_version(path, v)

    print("\n=== DIFF VERSIONS 0 vs 3 ===")
    diff = diff_versions(path, 0, 3)
    print(diff)

    print("\n=== RESTORE TO VERSION 1 ===")
    restore_to_version(path, version=1)

    dt = DeltaTable(str(path))
    print(f"After restore: version={dt.version()}, rows={len(dt.to_pandas())}")


if __name__ == "__main__":
    main()