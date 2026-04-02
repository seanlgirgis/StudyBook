# Story:
# An Iceberg table uses metadata, manifests, and snapshots to track files.
# Queries read only the files listed in the active snapshot.

MANIFEST_V1 = [
    {"file": "data/part-000.parquet", "partition": "date=2026-03-27", "rows": 1200},
    {"file": "data/part-001.parquet", "partition": "date=2026-03-27", "rows": 1100},
]

MANIFEST_V2 = [
    {"file": "data/part-000.parquet", "partition": "date=2026-03-27", "rows": 1200},
    {"file": "data/part-001.parquet", "partition": "date=2026-03-27", "rows": 1100},
    {"file": "data/part-002.parquet", "partition": "date=2026-03-28", "rows": 900},
]

SNAPSHOTS = [
    {"id": 1, "schema": "v1", "partition": "date", "manifest": MANIFEST_V1},
    {"id": 2, "schema": "v2(add country)", "partition": "date", "manifest": MANIFEST_V2},
]


def list_files_for_snapshot(snapshot_id):
    snapshot = next(s for s in SNAPSHOTS if s["id"] == snapshot_id)
    return snapshot


def query_by_partition(snapshot_id, partition_value):
    snapshot = list_files_for_snapshot(snapshot_id)
    files = [
        f for f in snapshot["manifest"] if f["partition"] == f"date={partition_value}"
    ]
    return files


def run_iceberg_table_format_demo():
    print("=" * 72)
    print("Scenario: table formats (Iceberg concepts)")

    print("\nSnapshot 1 metadata")
    snapshot1 = list_files_for_snapshot(1)
    print(snapshot1)

    print("\nSnapshot 2 metadata (schema evolved)")
    snapshot2 = list_files_for_snapshot(2)
    print(snapshot2)

    print("\nQuery: date=2026-03-27 on snapshot 2")
    files = query_by_partition(2, "2026-03-27")
    for f in files:
        print(f"  {f}")

    print("\nSummary")
    print("- Metadata + manifests list the exact data files.")
    print("- Snapshots give time-travel and schema evolution history.")
    print("- Query engines read only relevant files, not the whole lake.")


if __name__ == "__main__":
    run_iceberg_table_format_demo()

# Takeaway: Iceberg tracks table state with metadata, manifests, and snapshots.
