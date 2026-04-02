# Story:
# Raw orders are messy. Analysts keep rebuilding cleanup logic in each report.
# dbt layering (staging -> intermediate -> marts) makes the warehouse predictable.

from datetime import datetime


RAW_ORDERS = [
    {"OrderID": " 1001 ", "CustID": " c01 ", "OrderDate": "2024/01/05", "AmountUSD": "$120.00", "Status": "PAID"},
    {"OrderID": "1002", "CustID": "C02", "OrderDate": "01-06-2024", "AmountUSD": "85", "Status": "paid"},
    {"OrderID": "1003", "CustID": "c01", "OrderDate": "2024-01-07", "AmountUSD": "25.00", "Status": "refund"},
    {"OrderID": "1004", "CustID": "C03 ", "OrderDate": "2024-01-07", "AmountUSD": None, "Status": "PAID"},
]


def _normalize_date(raw_value):
    for fmt in ("%Y/%m/%d", "%m-%d-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw_value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw_value


def _parse_amount(raw_value):
    if raw_value is None:
        return 0.0
    cleaned = str(raw_value).replace("$", "").replace(",", "").strip()
    return float(cleaned) if cleaned else 0.0


def _print_rows(label, rows):
    print(label)
    for row in rows:
        print(row)


def _print_table(label, table):
    print(label)
    for key in sorted(table):
        print(f"- {key}: {table[key]}")


def stage_orders(raw_rows):
    # Staging = source cleanup and standardization (consistent names + types).
    staged = []
    for row in raw_rows:
        staged.append(
            {
                "order_id": row["OrderID"].strip(),
                "customer_id": row["CustID"].strip().upper(),
                "order_date": _normalize_date(row["OrderDate"]),
                "amount_usd": _parse_amount(row["AmountUSD"]),
                "status": row["Status"].strip().lower(),
            }
        )
    return staged


def build_intermediate_orders(staged_rows):
    # Intermediate = reusable transformation logic (business rules).
    intermediate = []
    for row in staged_rows:
        net_amount = 0.0
        if row["status"] == "paid":
            net_amount = row["amount_usd"]
        elif row["status"] == "refund":
            net_amount = -row["amount_usd"]
        intermediate.append(
            {
                **row,
                "is_refund": row["status"] == "refund",
                "net_amount_usd": net_amount,
            }
        )
    return intermediate


def mart_daily_revenue(intermediate_rows):
    # Marts = final consumer-facing tables for analytics/reporting.
    totals = {}
    for row in intermediate_rows:
        totals.setdefault(row["order_date"], 0.0)
        totals[row["order_date"]] += row["net_amount_usd"]
    return {date: round(amount, 2) for date, amount in totals.items()}


def mart_customer_summary(intermediate_rows):
    summary = {}
    for row in intermediate_rows:
        customer = row["customer_id"]
        summary.setdefault(customer, {"orders": 0, "net_spend_usd": 0.0})
        if row["status"] in ("paid", "refund"):
            summary[customer]["orders"] += 1
        summary[customer]["net_spend_usd"] += row["net_amount_usd"]
    for customer in summary:
        summary[customer]["net_spend_usd"] = round(summary[customer]["net_spend_usd"], 2)
    return summary


def _mart_daily_revenue_direct(raw_rows):
    # Mart built directly from raw: cleanup logic re-implemented (incomplete).
    totals = {}
    for row in raw_rows:
        date = _normalize_date(row["OrderDate"])
        amount = _parse_amount(row["AmountUSD"])
        totals.setdefault(date, 0.0)
        totals[date] += amount  # refunds treated as positive (wrong)
    return {date: round(amount, 2) for date, amount in totals.items()}


def _mart_customer_summary_direct(raw_rows):
    # Another mart built directly from raw with different cleanup assumptions.
    summary = {}
    for row in raw_rows:
        customer = row["CustID"].strip()  # no upper-casing
        summary.setdefault(customer, {"orders": 0, "gross_spend_usd": 0.0})
        if row["Status"].strip().lower() == "paid":
            summary[customer]["orders"] += 1
            summary[customer]["gross_spend_usd"] += _parse_amount(row["AmountUSD"])
    for customer in summary:
        summary[customer]["gross_spend_usd"] = round(summary[customer]["gross_spend_usd"], 2)
    return summary


def run_models_demo():
    print("=" * 72)
    print("Scenario: raw orders arrive messy and inconsistent")
    _print_rows("Raw source (ingested as-is):", RAW_ORDERS)

    print("=" * 72)
    print("Pain first: skipping layers mixes cleanup with business logic")
    raw_daily_revenue = _mart_daily_revenue_direct(RAW_ORDERS)
    raw_customer_summary = _mart_customer_summary_direct(RAW_ORDERS)
    _print_table("Mart A (raw daily revenue, refunds counted as positive):", raw_daily_revenue)
    _print_table("Mart B (raw customer summary, mixed casing):", raw_customer_summary)
    print("Two marts, two cleanup styles, and numbers drift.")

    print("=" * 72)
    print("Layer: STAGING = source cleanup and standardization")
    staged = stage_orders(RAW_ORDERS)
    _print_rows("Staged orders (cleaned columns, consistent types):", staged)

    print("=" * 72)
    print("Layer: INTERMEDIATE = reusable business logic")
    intermediate = build_intermediate_orders(staged)
    _print_rows("Intermediate orders (net_amount, is_refund):", intermediate)

    print("=" * 72)
    print("Layer: MARTS = final consumer-facing outputs")
    daily_revenue = mart_daily_revenue(intermediate)
    customer_summary = mart_customer_summary(intermediate)
    _print_table("Mart: daily revenue (net, analytics-ready):", daily_revenue)
    _print_table("Mart: customer summary:", customer_summary)

    print("=" * 72)
    print("Summary:")
    print("- Staging = clean and standardize once.")
    print("- Intermediate = reuse business logic everywhere.")
    print("- Marts = final tables for analysts and dashboards.")


if __name__ == "__main__":
    run_models_demo()

# Takeaway: Staging cleans sources, intermediate centralizes logic, marts publish consistent outputs.