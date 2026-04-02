# Story:
# Rebuilding an entire model daily is expensive. Incremental models load only the change.


RAW_SOURCE_DAY_1 = [
    {
        "order_id": "1001",
        "customer_id": "c01",
        "order_date": "2024-01-05",
        "amount_usd": "120.00",
        "updated_at": "2024-01-05T08:00:00",
    },
    {
        "order_id": "1002",
        "customer_id": "c02",
        "order_date": "2024-01-05",
        "amount_usd": "85.00",
        "updated_at": "2024-01-05T09:00:00",
    },
    {
        "order_id": "1003",
        "customer_id": "c01",
        "order_date": "2024-01-05",
        "amount_usd": "25.00",
        "updated_at": "2024-01-05T10:00:00",
    },
]

RAW_SOURCE_DAY_2 = [
    {
        "order_id": "1001",
        "customer_id": "c01",
        "order_date": "2024-01-05",
        "amount_usd": "120.00",
        "updated_at": "2024-01-05T08:00:00",
    },
    {
        "order_id": "1002",
        "customer_id": "c02",
        "order_date": "2024-01-05",
        "amount_usd": "80.00",
        "updated_at": "2024-01-06T08:00:00",
    },
    {
        "order_id": "1003",
        "customer_id": "c01",
        "order_date": "2024-01-05",
        "amount_usd": "25.00",
        "updated_at": "2024-01-05T10:00:00",
    },
    {
        "order_id": "1004",
        "customer_id": "c03",
        "order_date": "2024-01-06",
        "amount_usd": "200.00",
        "updated_at": "2024-01-06T09:00:00",
    },
    {
        "order_id": "1005",
        "customer_id": "c01",
        "order_date": "2024-01-04",
        "amount_usd": "40.00",
        "updated_at": "2024-01-06T10:00:00",
    },
]


def _normalize_customer(raw_value):
    return raw_value.strip().upper()


def _parse_amount(raw_value):
    return round(float(raw_value), 2)


def _print_rows(label, rows):
    print(label)
    for row in rows:
        print(row)


def _transform_order(row):
    # The model applies consistent typing and normalization.
    return {
        "order_id": row["order_id"],
        "customer_id": _normalize_customer(row["customer_id"]),
        "order_date": row["order_date"],
        "amount_usd": _parse_amount(row["amount_usd"]),
        "updated_at": row["updated_at"],
    }


def full_refresh(source_rows):
    # Full refresh = recompute everything from scratch.
    return [_transform_order(row) for row in source_rows]


def incremental_append_only(target_rows, source_rows, last_updated_at):
    # Naive incremental = only append rows newer than the boundary.
    changed_rows = [row for row in source_rows if row["updated_at"] > last_updated_at]
    return target_rows + [_transform_order(row) for row in changed_rows]


def incremental_merge(target_rows, source_rows, last_updated_at):
    # Safer incremental = update/replace affected business keys.
    changed_rows = [row for row in source_rows if row["updated_at"] > last_updated_at]
    by_order_id = {row["order_id"]: row for row in target_rows}
    for row in changed_rows:
        by_order_id[row["order_id"]] = _transform_order(row)
    return [by_order_id[key] for key in sorted(by_order_id.keys())]


def run_incremental_models_demo():
    print("=" * 72)
    print("Scenario: daily order model rebuilds everything")
    _print_rows("Raw source (day 1):", RAW_SOURCE_DAY_1)

    print("=" * 72)
    print("Full refresh on day 1 = build the model from scratch")
    target_table = full_refresh(RAW_SOURCE_DAY_1)
    _print_rows("Target table after full refresh:", target_table)

    print("=" * 72)
    print("Day 2 arrives: new orders + a corrected row + a late arrival")
    _print_rows("Raw source (day 2):", RAW_SOURCE_DAY_2)

    last_updated_at = max(row["updated_at"] for row in target_table)
    changed_rows = [row for row in RAW_SOURCE_DAY_2 if row["updated_at"] > last_updated_at]
    changed_order_ids = {row["order_id"] for row in changed_rows}

    print("=" * 72)
    print("Boundary for incremental = max loaded updated_at")
    print(f"Last updated_at in target: {last_updated_at}")
    print(f"Changed order_ids: {sorted(changed_order_ids)}")
    print(f"Full refresh scans {len(RAW_SOURCE_DAY_2)} rows.")
    print(f"Incremental scans {len(changed_rows)} rows.")

    print("=" * 72)
    print("Case A: naive incremental (append-only)")
    naive_target = incremental_append_only(target_table, RAW_SOURCE_DAY_2, last_updated_at)
    _print_rows("Target after naive incremental:", naive_target)
    print("Notice order_id 1002 appears twice with two amounts.")

    print("=" * 72)
    print("Case B: safer incremental (merge/upsert by business key)")
    corrected_target = incremental_merge(target_table, RAW_SOURCE_DAY_2, last_updated_at)
    _print_rows("Target after corrected incremental:", corrected_target)
    print("Order_id 1002 is replaced, late order 1005 is included once.")

    print("=" * 72)
    print("Full refresh truth check (recompute everything)")
    full_refresh_day_2 = full_refresh(RAW_SOURCE_DAY_2)
    _print_rows("Full refresh output:", full_refresh_day_2)

    print("=" * 72)
    print("Summary:")
    print("- Full refresh = recompute every row.")
    print("- Incremental = process only new/changed scope.")
    print("- Append-only can be wrong when changes arrive late.")
    print("- Merge/upsert keeps incremental runs correct and cheaper.")


if __name__ == "__main__":
    run_incremental_models_demo()

# Takeaway: Incremental models save cost by loading change, but must update changed keys safely.