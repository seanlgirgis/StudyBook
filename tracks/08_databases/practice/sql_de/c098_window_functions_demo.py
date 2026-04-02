# Story:
# Window functions compute across related rows without collapsing them.
# This demo contrasts GROUP BY with window-style calculations.

from collections import defaultdict


ROWS = [
    {"customer": "Ava", "date": "2024-01-03", "amount": 120},
    {"customer": "Ava", "date": "2024-01-10", "amount": 80},
    {"customer": "Ava", "date": "2024-01-20", "amount": 60},
    {"customer": "Ben", "date": "2024-01-05", "amount": 200},
    {"customer": "Ben", "date": "2024-01-07", "amount": 50},
    {"customer": "Ben", "date": "2024-01-21", "amount": 90},
    {"customer": "Cara", "date": "2024-01-02", "amount": 40},
]


def _sorted_rows(rows):
    return sorted(rows, key=lambda r: (r["customer"], r["date"]))


def group_by_total(rows):
    totals = defaultdict(int)
    for row in rows:
        totals[row["customer"]] += row["amount"]
    return totals


def window_row_number(rows):
    result = []
    current_customer = None
    row_num = 0
    for row in _sorted_rows(rows):
        if row["customer"] != current_customer:
            current_customer = row["customer"]
            row_num = 0
        row_num += 1
        result.append({**row, "row_number": row_num})
    return result


def window_lag(rows):
    result = []
    current_customer = None
    prev_amount = None
    for row in _sorted_rows(rows):
        if row["customer"] != current_customer:
            current_customer = row["customer"]
            prev_amount = None
        result.append({**row, "prev_amount": prev_amount})
        prev_amount = row["amount"]
    return result


def window_running_total(rows):
    result = []
    current_customer = None
    running = 0
    for row in _sorted_rows(rows):
        if row["customer"] != current_customer:
            current_customer = row["customer"]
            running = 0
        running += row["amount"]
        result.append({**row, "running_total": running})
    return result


def run_window_demo():
    print("=" * 72)
    print("Raw dataset:")
    for row in _sorted_rows(ROWS):
        print(row)

    print("=" * 72)
    print("Scenario A: GROUP BY style totals (rows collapse)")
    totals = group_by_total(ROWS)
    for customer, total in totals.items():
        print(f"{customer} total={total}")

    print("=" * 72)
    print("Scenario B: ROW_NUMBER within each customer")
    for row in window_row_number(ROWS):
        print(row)

    print("=" * 72)
    print("Scenario C: LAG (previous order amount)")
    for row in window_lag(ROWS):
        print(row)

    print("=" * 72)
    print("Scenario D: Running total per customer")
    for row in window_running_total(ROWS):
        print(row)

    print("=" * 72)
    print("Interpretation:")
    print("- GROUP BY gives one row per customer, so order detail is lost.")
    print("- Window logic keeps every order and adds rank, previous value, and running totals.")
    print("- PARTITION BY is the customer neighborhood; ORDER BY is the date sequence.")


if __name__ == "__main__":
    run_window_demo()

# Takeaway:
# Window functions add context without collapsing rows.
