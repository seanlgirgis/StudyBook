# Story:
# A lakehouse table accumulates many small files. Compaction rewrites them
# into fewer larger files to speed up scans.

SMALL_FILES = [
    {"file": "part-001.parquet", "rows": 100},
    {"file": "part-002.parquet", "rows": 120},
    {"file": "part-003.parquet", "rows": 90},
    {"file": "part-004.parquet", "rows": 110},
]


def scan_cost(files):
    # Simplified cost: each file has fixed overhead + rows.
    overhead = 5 * len(files)
    rows = sum(f["rows"] for f in files)
    return overhead + rows


def compact(files):
    total_rows = sum(f["rows"] for f in files)
    return [{"file": "compacted-001.parquet", "rows": total_rows}]


def run_compaction_demo():
    print("=" * 72)
    print("Scenario: compaction and optimization")

    print("\nBefore compaction")
    for f in SMALL_FILES:
        print(f"  {f}")
    before_cost = scan_cost(SMALL_FILES)
    print(f"Scan cost estimate: {before_cost}")

    print("\nAfter compaction")
    compacted = compact(SMALL_FILES)
    for f in compacted:
        print(f"  {f}")
    after_cost = scan_cost(compacted)
    print(f"Scan cost estimate: {after_cost}")

    print("\nSummary")
    print("- Many small files add overhead per file.")
    print("- Compaction rewrites them into fewer larger files.")
    print("- Optimization improves scan efficiency.")


if __name__ == "__main__":
    run_compaction_demo()

# Takeaway: Compaction reduces file overhead and speeds up queries.
