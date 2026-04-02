# Story:
# A team needs a revenue rollup. RDD-style code works but is verbose.
# DataFrame-style code is declarative and easier to optimize.


RAW_ORDERS = [
    {"order_id": "o1", "customer": "Ava", "amount": 120.0, "status": "paid"},
    {"order_id": "o2", "customer": "Ben", "amount": 85.0, "status": "paid"},
    {"order_id": "o3", "customer": "Ava", "amount": 25.0, "status": "refund"},
    {"order_id": "o4", "customer": "Cara", "amount": 200.0, "status": "paid"},
    {"order_id": "o5", "customer": "Ben", "amount": 15.0, "status": "paid"},
]


def _print_rows(label, rows):
    print(label)
    for row in rows:
        print(row)


def _rdd_filter(rows, min_amount):
    print("RDD filter: amount >", min_amount)
    return [row for row in rows if row["amount"] > min_amount and row["status"] == "paid"]


def _rdd_select(rows):
    print("RDD select: keep customer, amount")
    return [{"customer": row["customer"], "amount": row["amount"]} for row in rows]


def _rdd_aggregate(rows):
    print("RDD aggregate: sum amount by customer")
    totals = {}
    for row in rows:
        totals[row["customer"]] = totals.get(row["customer"], 0.0) + row["amount"]
    return totals


def _dataframe_filter(rows, min_amount):
    return [row for row in rows if row["amount"] > min_amount and row["status"] == "paid"]


def _dataframe_select(rows, columns):
    return [{col: row[col] for col in columns} for row in rows]


def _dataframe_groupby_sum(rows, key_col, value_col):
    totals = {}
    for row in rows:
        totals[row[key_col]] = totals.get(row[key_col], 0.0) + row[value_col]
    return totals


def run_dataframes_vs_rdds_demo():
    print("=" * 72)
    print("Scenario: compute paid revenue per customer from raw orders")
    _print_rows("Raw orders:", RAW_ORDERS)

    min_amount = 50.0

    print("=" * 72)
    print("Scenario A: RDD-style (manual, row-by-row, unstructured)")
    print("Pain first: every step is a separate pass you wire together.")
    rdd_filtered = _rdd_filter(RAW_ORDERS, min_amount)
    _print_rows("After RDD filter:", rdd_filtered)
    rdd_selected = _rdd_select(rdd_filtered)
    _print_rows("After RDD select:", rdd_selected)
    rdd_totals = _rdd_aggregate(rdd_selected)
    _print_rows("RDD totals (customer -> revenue):", sorted(rdd_totals.items()))

    print("=" * 72)
    print("Scenario B: DataFrame-style (column-aware, declarative)")
    print("Fix: express the intent once; the engine can optimize the plan.")
    print("DataFrame plan: filter(amount > 50 AND status = paid) -> select(customer, amount) -> groupby(customer).sum")
    df_filtered = _dataframe_filter(RAW_ORDERS, min_amount)
    df_selected = _dataframe_select(df_filtered, ["customer", "amount"])
    df_totals = _dataframe_groupby_sum(df_selected, "customer", "amount")
    _print_rows("DataFrame totals (customer -> revenue):", sorted(df_totals.items()))

    print("=" * 72)
    print("Summary:")
    print("- RDD = manual row operations, explicit steps, harder to optimize.")
    print("- DataFrame = column-aware, declarative intent, easier optimization.")


if __name__ == "__main__":
    run_dataframes_vs_rdds_demo()

# Takeaway: RDDs are low-level and verbose; DataFrames are structured and optimizable.