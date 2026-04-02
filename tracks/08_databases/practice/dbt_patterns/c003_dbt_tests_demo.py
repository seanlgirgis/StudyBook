# Story:
# The team trusts the warehouse, but silent data issues slip into dashboards.
# dbt tests make assumptions explicit and catch bad rows early.


CUSTOMERS = [
    {"customer_id": "C01", "name": "Ava"},
    {"customer_id": "C02", "name": "Ben"},
]

ORDERS_MODEL = [
    {
        "order_id": "1001",
        "customer_id": "C01",
        "status": "completed",
        "amount_usd": 120.0,
        "completed_at": "2024-01-05T12:00:00",
    },
    {
        "order_id": "1002",
        "customer_id": "C02",
        "status": "completed",
        "amount_usd": 85.0,
        "completed_at": None,
    },
    {
        "order_id": "1002",
        "customer_id": "C02",
        "status": "completed",
        "amount_usd": 85.0,
        "completed_at": "2024-01-05T12:05:00",
    },
    {
        "order_id": "1003",
        "customer_id": None,
        "status": "completed",
        "amount_usd": 60.0,
        "completed_at": "2024-01-05T12:10:00",
    },
    {
        "order_id": "1004",
        "customer_id": "C99",
        "status": "completed",
        "amount_usd": 40.0,
        "completed_at": "2024-01-05T12:20:00",
    },
    {
        "order_id": "1005",
        "customer_id": "C01",
        "status": "refunded",
        "amount_usd": -20.0,
        "completed_at": "2024-01-05T12:30:00",
    },
]


def _print_rows(label, rows):
    print(label)
    for row in rows:
        print(row)


def _run_test(name, offenders):
    if not offenders:
        print(f"[PASS] {name}")
        return
    print(f"[FAIL] {name}")
    print("Offending rows:")
    for row in offenders:
        print(row)


def _test_not_null(rows, column):
    return [row for row in rows if row.get(column) is None]


def _test_unique(rows, column):
    counts = {}
    for row in rows:
        value = row.get(column)
        counts[value] = counts.get(value, 0) + 1
    duplicates = {value for value, count in counts.items() if count > 1}
    return [row for row in rows if row.get(column) in duplicates]


def _test_accepted_values(rows, column, allowed):
    return [row for row in rows if row.get(column) not in allowed]


def _test_relationships(rows, column, reference_values):
    return [row for row in rows if row.get(column) not in reference_values]


def _test_completed_has_timestamp(rows):
    return [
        row
        for row in rows
        if row.get("status") == "completed" and not row.get("completed_at")
    ]


def _test_refunds_negative(rows):
    return [
        row
        for row in rows
        if row.get("status") == "refunded" and row.get("amount_usd", 0) >= 0
    ]


def run_dbt_tests_demo():
    print("=" * 72)
    print("Scenario: analysts trust the orders model, but hidden issues creep in")
    _print_rows("Model output (orders):", ORDERS_MODEL)

    print("=" * 72)
    print("Schema tests = structural/data contract expectations")
    _run_test("not_null(order_id)", _test_not_null(ORDERS_MODEL, "order_id"))
    _run_test("unique(order_id)", _test_unique(ORDERS_MODEL, "order_id"))
    _run_test(
        "accepted_values(status) in {completed, refunded}",
        _test_accepted_values(ORDERS_MODEL, "status", {"completed", "refunded"}),
    )
    customer_ids = {row["customer_id"] for row in CUSTOMERS}
    _run_test(
        "relationships(customer_id -> customers)",
        _test_relationships(ORDERS_MODEL, "customer_id", customer_ids),
    )

    print("=" * 72)
    print("Custom tests = business logic expectations")
    _run_test("completed orders must have completed_at", _test_completed_has_timestamp(ORDERS_MODEL))
    _run_test("refunds must be negative amounts", _test_refunds_negative(ORDERS_MODEL))

    print("=" * 72)
    print("Summary:")
    print("- Schema tests catch structural issues like nulls, duplicates, and bad relationships.")
    print("- Custom tests enforce business rules the warehouse depends on.")
    print("- dbt tests make assumptions explicit so broken data fails fast.")


if __name__ == "__main__":
    run_dbt_tests_demo()

# Takeaway: dbt tests turn hidden assumptions into explicit, enforceable checks.