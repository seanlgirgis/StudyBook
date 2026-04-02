# Story:
# A pipeline ingests orders. Schema changes from v1 to v2 with a new column
# and a renamed field. Raw keeps both; curated adapts to keep BI stable.

RAW_V1 = [
    {"order_id": "o100", "customer": "Ava", "amount": "120.5"},
    {"order_id": "o101", "customer": "Ben", "amount": "85"},
]

RAW_V2 = [
    {"order_id": "o102", "customer_name": "Cara", "amount": "200", "currency": "USD"},
    {"order_id": "o103", "customer_name": "Dee", "amount": "60", "currency": "USD"},
]


def _print_rows(label, rows):
    print(label)
    for row in rows:
        print(f"  {row}")


def raw_union(v1_rows, v2_rows):
    # Raw layer: keep all columns as-is, even if schemas differ.
    return [dict(row) for row in v1_rows] + [dict(row) for row in v2_rows]


def curated_orders(raw_rows):
    # Curated layer: normalize schema evolution for downstream stability.
    curated = []
    for row in raw_rows:
        customer = row.get("customer") or row.get("customer_name")
        amount_text = row.get("amount")
        currency = row.get("currency", "USD")

        if not customer or amount_text is None:
            continue

        try:
            amount = float(amount_text)
        except ValueError:
            continue

        curated.append(
            {
                "order_id": row.get("order_id"),
                "customer": customer,
                "amount": amount,
                "currency": currency,
                "schema_version": "v2" if "customer_name" in row else "v1",
            }
        )
    return curated


def naive_downstream(raw_rows):
    # Downstream that expects v1 schema; breaks on v2 rows.
    broken = 0
    for row in raw_rows:
        if "customer" not in row:
            broken += 1
    return broken


def run_schema_evolution_demo():
    print("=" * 72)
    print("Scenario: schema evolution (v1 -> v2)")

    raw_rows = raw_union(RAW_V1, RAW_V2)
    _print_rows("Raw rows (mixed schemas):", raw_rows)

    broken = naive_downstream(raw_rows)
    print(f"\nNaive downstream breaks on rows: {broken}")

    curated = curated_orders(raw_rows)
    _print_rows("\nCurated rows (stable schema):", curated)

    print("\nSummary")
    print("- Schema evolution adds/renames fields in upstream data.")
    print("- Raw keeps everything; naive consumers can break.")
    print("- Curated adapts fields to keep a stable contract.")


if __name__ == "__main__":
    run_schema_evolution_demo()

# Takeaway: Raw preserves change; curated normalizes it for downstream stability.
