# Story:
# QUALIFY filters rows after window functions are computed.


ROWS = [
    {"customer": "Ava", "date": "2024-01-03", "amount": 120},
    {"customer": "Ava", "date": "2024-01-20", "amount": 60},
    {"customer": "Ava", "date": "2024-01-10", "amount": 80},
    {"customer": "Ben", "date": "2024-01-07", "amount": 50},
    {"customer": "Ben", "date": "2024-01-21", "amount": 90},
    {"customer": "Ben", "date": "2024-01-05", "amount": 200},
    {"customer": "Cara", "date": "2024-01-02", "amount": 40},
]


def _sorted_rows(rows):
    return sorted(rows, key=lambda r: (r["customer"], r["date"]))


def naive_where_style(rows, min_amount):
    return [row for row in rows if row["amount"] >= min_amount]


def with_row_number(rows):
    result = []
    for customer in sorted({row["customer"] for row in rows}):
        customer_rows = [row for row in rows if row["customer"] == customer]
        customer_rows = sorted(customer_rows, key=lambda r: r["date"], reverse=True)
        for index, row in enumerate(customer_rows, start=1):
            result.append({**row, "row_number": index})
    return result


def qualify_latest(rows):
    return [row for row in rows if row["row_number"] == 1]


def run_qualify_demo():
    print("=" * 72)
    print("Raw dataset:")
    for row in _sorted_rows(ROWS):
        print(row)

    print("=" * 72)
    print("Scenario A: WHERE-style filtering (wrong goal)")
    filtered = naive_where_style(ROWS, 100)
    for row in filtered:
        print(row)
    print("This filters amounts, not 'latest per customer'.")

    print("=" * 72)
    print("Scenario B: Window calculation (row_number by customer, latest first)")
    numbered = with_row_number(ROWS)
    for row in numbered:
        print(row)

    print("=" * 72)
    print("Scenario C: QUALIFY-style filtering (row_number = 1)")
    qualified = qualify_latest(numbered)
    for row in qualified:
        print(row)

    print("=" * 72)
    print("Scenario D: Subquery equivalent (compute then filter)")
    subquery_like = qualify_latest(with_row_number(ROWS))
    for row in subquery_like:
        print(row)

    print("=" * 72)
    print("Interpretation:")
    print("- WHERE runs before window logic, so it cannot filter by row_number.")
    print("- QUALIFY filters after row_number exists, keeping only the latest per customer.")
    print("- The subquery approach matches QUALIFY but is more verbose.")


if __name__ == "__main__":
    run_qualify_demo()

# Takeaway:
# QUALIFY is post-window filtering.
