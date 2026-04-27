# ============================================================
# Topic   : Delta Lake for Data Engineers
# File    : 01_delta_basics_and_acid.py
# Covers  : Delta basics, ACID transactions, transaction log, atomicity, append
# Prereqs : pip install deltalake pandas pyarrow
# Run     : python 01_delta_basics_and_acid.py
# ============================================================

from deltalake import DeltaTable, write_deltalake
import pandas as pd
import os
import json
import random
import shutil
from pathlib import Path
from datetime import datetime, timedelta, timezone


def get_output_dir() -> Path:
    """Return platform output dir. Create if missing."""
    default = Path("C:/tmp/studybook/delta" if os.name == "nt" else "/tmp/studybook/delta")
    out = Path(os.getenv("OUTPUT_DIR", str(default)))
    out.mkdir(parents=True, exist_ok=True)
    return out


def generate_sensor_data(n_rows: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic sensor readings.

    WHY fixed seed:
    Reproducible data makes demos, tests, and interview explanations consistent.
    """
    random.seed(seed)

    plants = ["plant_A", "plant_B", "plant_C"]
    now = datetime.now(timezone.utc).replace(microsecond=0)

    rows = []
    for _ in range(n_rows):
        rows.append(
            {
                "sensor_id": f"sensor_{random.randint(0, 49):03d}",
                "plant": random.choice(plants),
                "value": round(random.uniform(15, 95), 3),
                "unit": "celsius",
                "ts": now - timedelta(seconds=random.randint(0, 86_400)),
            }
        )

    return pd.DataFrame(rows)


def create_delta_table(path: Path, df: pd.DataFrame) -> None:
    """
    Write df as a Delta table.

    WHY _delta_log:
    The transaction log IS the Delta table. Parquet files store data, but the JSON
    commit files define which Parquet files belong to the current snapshot.

    WHY atomicity:
    Delta writes data files first, then commits a JSON transaction. If the commit
    does not happen, readers ignore orphan files because they are not in the log.
    """
    if path.exists():
        shutil.rmtree(path)

    write_deltalake(str(path), df, mode="overwrite")

    log_dir = path / "_delta_log"
    json_files = sorted(log_dir.glob("*.json"))

    print(f"Table path: {path}")
    print(f"Delta log JSON files: {len(json_files)}")

    if json_files:
        print(f"\nFirst commit file: {json_files[0].name}")
        print("-" * 80)
        for line in json_files[0].read_text(encoding="utf-8").splitlines():
            print(json.dumps(json.loads(line), indent=2, default=str))
        print("-" * 80)


def read_delta_table(path: Path) -> pd.DataFrame:
    """
    Read the latest committed Delta snapshot.

    WHY snapshot isolation:
    Readers see one consistent table version. They do not see partial writes from
    concurrent writers because only committed transaction log versions are visible.
    """
    dt = DeltaTable(str(path))
    df = dt.to_pandas()

    print(f"Current version: {dt.version()}")
    print(f"Row count: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))

    return df


def inspect_transaction_log(path: Path) -> list[dict]:
    """
    Read all JSON commits from _delta_log and print a compact audit table.

    WHY transaction log:
    Delta gives an auditable history of writes. This is a key difference from
    unmanaged Parquet folders, where file changes alone do not explain intent.
    """
    log_dir = path / "_delta_log"
    json_files = sorted(log_dir.glob("*.json"))

    commits: list[dict] = []

    print(f"{'Version':<8} | {'Operation':<12} | {'Added':<6} | {'Removed':<7} | {'Timestamp'}")
    print("-" * 75)

    for file in json_files:
        version = int(file.stem)
        actions = [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()]

        operation = "UNKNOWN"
        timestamp = ""
        added = 0
        removed = 0

        for action in actions:
            if "commitInfo" in action:
                info = action["commitInfo"]
                operation = info.get("operation", "UNKNOWN")
                timestamp_ms = info.get("timestamp")
                if timestamp_ms:
                    timestamp = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat()
            elif "add" in action:
                added += 1
            elif "remove" in action:
                removed += 1

        commits.append(
            {
                "version": version,
                "operation": operation,
                "added_files": added,
                "removed_files": removed,
                "timestamp": timestamp,
                "actions": actions,
            }
        )

        print(f"{version:<8} | {operation:<12} | {added:<6} | {removed:<7} | {timestamp}")

    return commits


def demonstrate_atomicity(path: Path) -> None:
    """
    Show that a failed write leaves the committed table unchanged.

    WHY atomicity:
    Delta guarantees all-or-nothing commits. A bad write should not corrupt the
    latest readable snapshot.
    """
    before = DeltaTable(str(path))
    before_rows = len(before.to_pandas())
    before_version = before.version()

    print(f"Before failed write: version={before_version}, rows={before_rows}")

    bad_df = pd.DataFrame(
        {
            "sensor_id": ["sensor_bad"],
            "plant": ["plant_A"],
            "value": [{"not": "a float"}],  # intentionally incompatible with existing float column
            "unit": ["celsius"],
            "ts": [datetime.now(timezone.utc)],
        }
    )

    try:
        write_deltalake(str(path), bad_df, mode="append")
        print("Unexpected: bad write succeeded")
    except Exception as exc:
        print(f"Caught expected write failure: {type(exc).__name__}: {exc}")

    after = DeltaTable(str(path))
    after_rows = len(after.to_pandas())
    after_version = after.version()

    print(f"After failed write: version={after_version}, rows={after_rows}")

    assert before_rows == after_rows
    assert before_version == after_version

    print("Table unchanged after failed write — atomicity confirmed ✓")


def get_active_data_files(path: Path) -> set[str]:
    """
    Return active data files by reading Delta's latest snapshot.

    deltalake versions differ: older examples often show dt.files(),
    while delta-rs 1.5.x exposes file_uris().
    """
    dt = DeltaTable(str(path))
    return set(dt.file_uris())


def append_to_table(path: Path, df: pd.DataFrame) -> None:
    """
    Append new rows to the Delta table.

    WHY append is efficient:
    Delta does not rewrite existing Parquet files for a normal append. It adds new
    files and records those files in a new transaction log version.
    """
    before_dt = DeltaTable(str(path))
    before_rows = len(before_dt.to_pandas())
    before_version = before_dt.version()
    before_files = get_active_data_files(path)

    print(f"Before append: version={before_version}, rows={before_rows}, data_files={len(before_files)}")

    write_deltalake(str(path), df, mode="append")

    after_dt = DeltaTable(str(path))
    after_rows = len(after_dt.to_pandas())
    after_version = after_dt.version()
    after_files = get_active_data_files(path)

    print(f"After append:  version={after_version}, rows={after_rows}, data_files={len(after_files)}")
    print(f"Old data files still referenced: {before_files.issubset(after_files)}")

    newest_log = path / "_delta_log" / f"{after_version:020d}.json"
    print(f"\nNewest commit add actions from {newest_log.name}:")
    print("-" * 80)

    for line in newest_log.read_text(encoding="utf-8").splitlines():
        action = json.loads(line)
        if "add" in action:
            print(json.dumps(action["add"], indent=2, default=str))

    print("-" * 80)


def main():
    out = get_output_dir()
    path = out / "sensor_readings"

    print("\n=== CREATE DELTA TABLE ===")
    df1 = generate_sensor_data(1000)
    create_delta_table(path, df1)

    print("\n=== READ DELTA TABLE ===")
    read_delta_table(path)

    print("\n=== TRANSACTION LOG ===")
    inspect_transaction_log(path)

    print("\n=== ATOMICITY DEMO ===")
    demonstrate_atomicity(path)

    print("\n=== APPEND ===")
    df2 = generate_sensor_data(500, seed=99)
    append_to_table(path, df2)

    print("\n=== READ AFTER APPEND ===")
    read_delta_table(path)


if __name__ == "__main__":
    main()