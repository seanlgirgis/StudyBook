# Story:
# A team loads a customer snapshot each day. Full load rebuilds the table.
# Incremental load applies only the changes since yesterday.

DAY1_SNAPSHOT = [
    {"customer_id": "c001", "name": "Ava", "status": "active", "segment": "retail"},
    {"customer_id": "c002", "name": "Ben", "status": "active", "segment": "retail"},
    {"customer_id": "c003", "name": "Cara", "status": "active", "segment": "enterprise"},
]

DAY2_SNAPSHOT = [
    {"customer_id": "c001", "name": "Ava", "status": "active", "segment": "retail"},
    {"customer_id": "c002", "name": "Ben", "status": "inactive", "segment": "retail"},
    {"customer_id": "c004", "name": "Dee", "status": "active", "segment": "retail"},
]

# Derived changes between day1 and day2 (insert/update/delete)
DAY2_CHANGES = [
    {"op": "update", "customer_id": "c002", "status": "inactive"},
    {"op": "delete", "customer_id": "c003"},
    {"op": "insert", "customer_id": "c004", "name": "Dee", "status": "active", "segment": "retail"},
]


def _index_by_id(rows):
    return {row["customer_id"]: dict(row) for row in rows}


def _print_table(label, rows):
    print(label)
    for row in rows:
        print(f"  {row}")


def full_load(snapshot_rows):
    # Full load = replace the target with the latest snapshot.
    return [dict(row) for row in snapshot_rows]


def incremental_load(existing_rows, change_rows):
    # Incremental load = apply deltas to the existing target.
    target = _index_by_id(existing_rows)

    for change in change_rows:
        op = change["op"]
        customer_id = change["customer_id"]

        if op == "delete":
            target.pop(customer_id, None)
            continue

        if op == "insert":
            target[customer_id] = {
                "customer_id": customer_id,
                "name": change["name"],
                "status": change["status"],
                "segment": change["segment"],
            }
            continue

        if op == "update":
            if customer_id in target:
                target[customer_id].update(change)
                target[customer_id].pop("op", None)

    return list(target.values())


def _sorted(rows):
    return sorted(rows, key=lambda row: row["customer_id"])


def run_full_vs_incremental_demo():
    print("=" * 72)
    print("Scenario: full load vs incremental load")
    print("Day 1 snapshot arrives -> initial target table")

    day1_target = full_load(DAY1_SNAPSHOT)
    _print_table("Day 1 target:", _sorted(day1_target))

    print("\nDay 2 snapshot arrives -> full load rebuild")
    full_loaded = full_load(DAY2_SNAPSHOT)
    _print_table("Full load target:", _sorted(full_loaded))

    print("\nDay 2 deltas arrive -> incremental load apply")
    incremental_loaded = incremental_load(day1_target, DAY2_CHANGES)
    _print_table("Incremental target:", _sorted(incremental_loaded))

    print("\nCompare results")
    print(f"Full load count: {len(full_loaded)}")
    print(f"Incremental count: {len(incremental_loaded)}")
    print("Match:", _sorted(full_loaded) == _sorted(incremental_loaded))

    print("\nSummary")
    print("- Full load = replace the target with a complete snapshot.")
    print("- Incremental load = apply only the changes to yesterday's target.")
    print("- Both should converge to the same end state if deltas are correct.")


if __name__ == "__main__":
    run_full_vs_incremental_demo()

# Takeaway: Full loads rebuild from scratch; incremental loads apply deltas.
