# Story:
# A retailer lands daily files in staging, keeps a raw history, then curates it
# into analytics-ready tables.

INBOUND_FILES = [
    {
        "file_name": "orders_2026_03_26.csv",
        "rows": [
            {"order_id": "o100", "customer": "Ava", "amount": "120.50", "status": "PAID"},
            {"order_id": "o101", "customer": "Ben", "amount": "85", "status": "PAID"},
            {"order_id": "o102", "customer": "Ava", "amount": "-5", "status": "REFUND"},
            {"order_id": "o103", "customer": "", "amount": "42", "status": "PAID"},
        ],
    },
    {
        "file_name": "orders_2026_03_27.csv",
        "rows": [
            {"order_id": "o101", "customer": "Ben", "amount": "85", "status": "PAID"},
            {"order_id": "o104", "customer": "Cara", "amount": "200", "status": "PAID"},
            {"order_id": "o105", "customer": "Dee", "amount": "N/A", "status": "PAID"},
        ],
    },
]


def _print_rows(title, rows, limit=6):
    print(title)
    for row in rows[:limit]:
        print(f"  {row}")
    if len(rows) > limit:
        print(f"  ... ({len(rows) - limit} more)")


def stage_files(inbound_files):
    # Stage = landing zone. Keep file boundaries and raw text.
    staged = []
    for file in inbound_files:
        for row in file["rows"]:
            staged.append(
                {
                    "file_name": file["file_name"],
                    "raw_row": dict(row),
                    "ingest_ts": "2026-03-27T09:30:00Z",
                }
            )
    return staged


def raw_normalize(staged_rows):
    # Raw = standardized schema + minimal parsing. Preserve every row.
    raw = []
    for row in staged_rows:
        raw_row = row["raw_row"]
        raw.append(
            {
                "order_id": str(raw_row.get("order_id", "")).strip(),
                "customer": str(raw_row.get("customer", "")).strip(),
                "amount_text": str(raw_row.get("amount", "")).strip(),
                "status": str(raw_row.get("status", "")).strip().upper(),
                "source_file": row["file_name"],
                "ingest_ts": row["ingest_ts"],
            }
        )
    return raw


def curated_orders(raw_rows):
    # Curated = business rules, dedupe, and analytics-ready fields.
    curated = []
    seen = set()
    for row in raw_rows:
        if not row["order_id"] or not row["customer"]:
            continue
        if row["status"] != "PAID":
            continue
        try:
            amount = float(row["amount_text"])
        except ValueError:
            continue
        if amount <= 0:
            continue

        key = row["order_id"]
        if key in seen:
            continue
        seen.add(key)

        curated.append(
            {
                "order_id": row["order_id"],
                "customer": row["customer"],
                "amount": round(amount, 2),
                "order_date": row["source_file"].replace("orders_", "").replace(".csv", ""),
            }
        )
    return curated


def _curated_totals(curated_rows):
    totals = {}
    for row in curated_rows:
        totals[row["customer"]] = totals.get(row["customer"], 0.0) + row["amount"]
    return totals


def run_staging_raw_curated_demo():
    print("=" * 72)
    print("Scenario: staging -> raw -> curated ELT layers")
    print("Goal: keep raw history, then curate for analytics")

    print("\nLayer 1: STAGING (landing zone, no transforms)")
    staged = stage_files(INBOUND_FILES)
    _print_rows("Staged rows:", staged)
    print(f"Staged count: {len(staged)}")

    print("\nLayer 2: RAW (standardize schema, keep all rows)")
    raw = raw_normalize(staged)
    _print_rows("Raw rows:", raw)
    print(f"Raw count: {len(raw)}")

    print("\nLayer 3: CURATED (business rules, dedupe, ready for BI)")
    curated = curated_orders(raw)
    _print_rows("Curated rows:", curated)
    totals = _curated_totals(curated)
    print(f"Curated count: {len(curated)}")
    print("Curated totals (customer -> revenue):", sorted(totals.items()))

    print("\nSummary")
    print("- Staging = landed files, no change")
    print("- Raw = standardized columns, complete history")
    print("- Curated = validated, deduped, analytics-ready data")


if __name__ == "__main__":
    run_staging_raw_curated_demo()

# Takeaway: Use staged/raw/curated to separate landing, history, and business-ready data.
