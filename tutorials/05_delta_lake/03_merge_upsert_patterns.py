# ============================================================
# Topic   : Delta Lake for Data Engineers
# File    : 03_merge_upsert_patterns.py
# Covers  : MERGE (upsert), conditional merge, SCD Type 2, delete
# Prereqs : pip install deltalake pandas pyarrow
# Run     : python 03_merge_upsert_patterns.py
# ============================================================

from deltalake import DeltaTable, write_deltalake
import pandas as pd
import pyarrow as pa
from pathlib import Path
import os
import random
import shutil
from datetime import datetime, timezone


def get_output_dir() -> Path:
    default = Path("C:/tmp/studybook/delta" if os.name == "nt" else "/tmp/studybook/delta")
    out = Path(os.getenv("OUTPUT_DIR", str(default)))
    out.mkdir(parents=True, exist_ok=True)
    return out


def generate_customers(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic customers.

    WHY deterministic:
    Repeatable merge scenarios are critical for testing idempotency.
    """
    random.seed(seed)
    regions = ["NA", "EU", "APAC", "LATAM"]
    tiers = ["BRONZE", "SILVER", "GOLD"]

    data = []
    for i in range(n):
        spend = round(random.uniform(100, 50000), 2)

        data.append(
            {
                "customer_id": f"CUST-{i:06d}",
                "name": f"Customer {i}",
                "region": random.choice(regions),
                "tier": random.choice(tiers),
                "annual_spend": spend,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    return pd.DataFrame(data)


def simple_upsert(path: Path, source_df: pd.DataFrame, merge_key: str = "customer_id") -> dict:
    """
    Basic MERGE: update all columns on match, insert on no match.

    WHY MERGE:
    Avoid rewriting the entire dataset. MERGE is the core pattern for CDC pipelines.
    """
    dt = DeltaTable(str(path))
    source = pa.Table.from_pandas(source_df, preserve_index=False)

    metrics = (
        dt.merge(
            source=source,
            predicate=f"target.{merge_key} = source.{merge_key}",
            source_alias="source",
            target_alias="target",
        )
        .when_matched_update_all()
        .when_not_matched_insert_all()
        .execute()
    )

    result = {
        "rows_matched": int(metrics.get("num_source_rows", len(source_df)))
        - int(metrics.get("num_target_rows_inserted", 0)),
        "rows_inserted": int(metrics.get("num_target_rows_inserted", 0)),
        "rows_updated": int(metrics.get("num_target_rows_updated", 0)),
    }

    print(f"Simple upsert result: {result}")
    return result


def conditional_merge(path: Path, source_df: pd.DataFrame, merge_key: str = "customer_id") -> dict:
    """
    Conditional MERGE: update only if annual_spend changed.

    WHY conditional:
    Avoids unnecessary rewrites when incoming CDC data has no meaningful change.
    This reduces file churn and write amplification.
    """
    dt = DeltaTable(str(path))
    source = pa.Table.from_pandas(source_df, preserve_index=False)

    metrics = (
        dt.merge(
            source=source,
            predicate=f"target.{merge_key} = source.{merge_key}",
            source_alias="source",
            target_alias="target",
        )
        .when_matched_update(
            updates={
                "annual_spend": "source.annual_spend",
                "updated_at": "source.updated_at",
            },
            predicate="source.annual_spend != target.annual_spend",
        )
        .when_not_matched_insert_all()
        .execute()
    )

    rows_updated = int(metrics.get("num_target_rows_updated", 0))
    rows_inserted = int(metrics.get("num_target_rows_inserted", 0))
    rows_skipped = len(source_df) - rows_updated - rows_inserted

    result = {
        "rows_updated": rows_updated,
        "rows_inserted": rows_inserted,
        "rows_skipped": rows_skipped,
    }

    print(f"Conditional merge result: {result}")
    return result


def implement_scd_type2(
    path: Path,
    source_df: pd.DataFrame,
    key_col: str = "customer_id",
    tracked_cols: list[str] | None = None,
) -> None:
    """
    Slowly Changing Dimension Type 2 pattern.

    Target schema includes:
      valid_from, valid_to, is_current

    WHY SCD Type 2:
    Instead of overwriting history, we close the old current record and insert a
    new current version. This preserves the full business timeline.
    """
    if tracked_cols is None:
        tracked_cols = ["annual_spend", "tier"]

    now = datetime.now(timezone.utc).isoformat()

    source = source_df.copy()
    source["valid_from"] = now
    source["valid_to"] = "9999-12-31"
    source["is_current"] = True

    source_arrow = pa.Table.from_pandas(source, preserve_index=False)

    change_predicate = " OR ".join(
        [f"source.{col} != target.{col}" for col in tracked_cols]
    )

    # Step 1:
    # Close current target records when tracked columns changed.
    # Delta does not physically delete old records here; it writes a new table version.
    close_metrics = (
        DeltaTable(str(path))
        .merge(
            source=source_arrow,
            predicate=f"target.{key_col} = source.{key_col} AND target.is_current = true",
            source_alias="source",
            target_alias="target",
        )
        .when_matched_update(
            updates={
                "valid_to": f"'{now}'",
                "is_current": "false",
            },
            predicate=change_predicate,
        )
        .execute()
    )

    # Step 2:
    # Insert rows that no longer have a current match after Step 1.
    # That includes new business keys and changed keys whose old records were closed.
    insert_metrics = (
        DeltaTable(str(path))
        .merge(
            source=source_arrow,
            predicate=f"target.{key_col} = source.{key_col} AND target.is_current = true",
            source_alias="source",
            target_alias="target",
        )
        .when_not_matched_insert_all()
        .execute()
    )

    closed = int(close_metrics.get("num_target_rows_updated", 0))
    inserted = int(insert_metrics.get("num_target_rows_inserted", 0))

    print(f"SCD Type 2 merge completed: closed_old_records={closed}, inserted_new_versions={inserted}")


def delete_matching_records(path: Path, ids_to_delete: list[str]) -> int:
    """
    Delete records by customer_id.

    WHY Delta delete:
    Delta records removed files in the transaction log. Physical cleanup happens
    later through VACUUM, which preserves time travel until retention expires.
    """
    dt = DeltaTable(str(path))

    quoted_ids = ", ".join([f"'{i}'" for i in ids_to_delete])
    predicate = f"customer_id IN ({quoted_ids})"

    metrics = dt.delete(predicate)

    deleted = int(metrics.get("num_deleted_rows", 0))
    print(f"Deleted {deleted} rows")

    return deleted


def main():
    path = get_output_dir() / "customers_scd"

    if path.exists():
        shutil.rmtree(path)

    df_init = generate_customers(1000)
    df_init["valid_from"] = "2024-01-01"
    df_init["valid_to"] = "9999-12-31"
    df_init["is_current"] = True

    write_deltalake(str(path), df_init, mode="overwrite")
    print(f"Initial load: {len(df_init)} customers")

    print("\n=== SIMPLE UPSERT ===")
    df_updates = generate_customers(200, seed=99)
    simple_upsert(path, df_updates)

    print("\n=== CONDITIONAL MERGE ===")
    df_spend_updates = generate_customers(100, seed=77)
    conditional_merge(path, df_spend_updates)

    print("\n=== SCD TYPE 2 ===")
    df_scd = generate_customers(50, seed=55)
    df_scd["annual_spend"] = df_scd["annual_spend"] * 1.5

    implement_scd_type2(
        path,
        df_scd,
        key_col="customer_id",
        tracked_cols=["annual_spend", "tier"],
    )

    print("\n=== DELETE ===")
    random.seed(42)
    ids_to_delete = [f"CUST-{i:06d}" for i in random.sample(range(1000), 10)]
    delete_matching_records(path, ids_to_delete)

    print("\n=== FINAL TABLE CHECK ===")
    dt = DeltaTable(str(path))
    df_final = dt.to_pandas()
    print(f"Current Delta version: {dt.version()}")
    print(f"Final row count: {len(df_final)}")
    print(f"Current records: {int(df_final['is_current'].sum())}")
    print(f"Historical records: {int((~df_final['is_current']).sum())}")


if __name__ == "__main__":
    main()