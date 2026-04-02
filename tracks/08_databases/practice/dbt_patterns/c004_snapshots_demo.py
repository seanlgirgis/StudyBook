# Story:
# The business updates customer plans. If we overwrite, we lose the history.
# Snapshots keep the past and mark what is current.


SOURCE_RUN_1 = [
    {"customer_id": "C01", "plan": "basic", "city": "Austin", "updated_at": "2024-01-05"},
    {"customer_id": "C02", "plan": "pro", "city": "Denver", "updated_at": "2024-01-05"},
    {"customer_id": "C03", "plan": "basic", "city": "Miami", "updated_at": "2024-01-05"},
]

SOURCE_RUN_2 = [
    {"customer_id": "C01", "plan": "pro", "city": "Austin", "updated_at": "2024-02-01"},
    {"customer_id": "C02", "plan": "pro", "city": "Denver", "updated_at": "2024-02-01"},
    {"customer_id": "C03", "plan": "basic", "city": "Orlando", "updated_at": "2024-02-01"},
]


def _print_rows(label, rows):
    print(label)
    for row in rows:
        print(row)


def _type1_overwrite(target_rows, source_rows):
    # Type 1 = overwrite; only the latest state is kept.
    return [row.copy() for row in source_rows]


def _snapshot_scd2(snapshot_rows, source_rows, run_date):
    # Type 2 snapshot = preserve history with valid_from/valid_to/current.
    next_rows = [row.copy() for row in snapshot_rows]
    current_by_key = {row["customer_id"]: row for row in next_rows if row["is_current"]}

    for source in source_rows:
        customer_id = source["customer_id"]
        tracked_values = (source["plan"], source["city"])
        current_row = current_by_key.get(customer_id)

        if current_row:
            current_values = (current_row["plan"], current_row["city"])
            if tracked_values == current_values:
                continue
            current_row["valid_to"] = run_date
            current_row["is_current"] = False

        next_rows.append(
            {
                "customer_id": customer_id,
                "plan": source["plan"],
                "city": source["city"],
                "valid_from": run_date,
                "valid_to": None,
                "is_current": True,
            }
        )
        current_by_key[customer_id] = next_rows[-1]

    return next_rows


def run_snapshots_demo():
    print("=" * 72)
    print("Scenario: customer plans change, but we must preserve history")
    _print_rows("Source run 1:", SOURCE_RUN_1)

    print("=" * 72)
    print("Type 1 overwrite = only the latest row survives")
    type1_table = _type1_overwrite([], SOURCE_RUN_1)
    _print_rows("Type 1 table after run 1:", type1_table)

    print("=" * 72)
    print("Type 2 snapshot = history rows with valid_from/valid_to/current")
    snapshot_table = _snapshot_scd2([], SOURCE_RUN_1, "2024-01-05")
    _print_rows("Snapshot table after run 1:", snapshot_table)

    print("=" * 72)
    print("Run 2 arrives with changes")
    _print_rows("Source run 2:", SOURCE_RUN_2)

    print("=" * 72)
    print("Type 1 overwrite (run 2) loses history")
    type1_table = _type1_overwrite(type1_table, SOURCE_RUN_2)
    _print_rows("Type 1 table after run 2:", type1_table)

    print("=" * 72)
    print("Type 2 snapshot (run 2) preserves old and new versions")
    snapshot_table = _snapshot_scd2(snapshot_table, SOURCE_RUN_2, "2024-02-01")
    _print_rows("Snapshot table after run 2:", snapshot_table)

    print("=" * 72)
    print("Summary:")
    print("- Type 1 overwrite keeps only the latest state.")
    print("- Type 2 snapshot preserves history with valid_from/valid_to.")
    print("- Unchanged rows do not create new history records.")


if __name__ == "__main__":
    run_snapshots_demo()

# Takeaway: Snapshots keep historical truth by expiring old rows instead of overwriting them.
