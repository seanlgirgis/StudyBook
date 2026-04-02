# Story:
# Pivot turns row-shaped data into columns. Unpivot turns it back into rows.

RAW_SALES = [
    {"store": "North", "day": "Mon", "sales": 120},
    {"store": "North", "day": "Tue", "sales": 90},
    {"store": "North", "day": "Wed", "sales": 150},
    {"store": "South", "day": "Mon", "sales": 80},
    {"store": "South", "day": "Tue", "sales": 110},
    {"store": "South", "day": "Wed", "sales": 70},
]

DAYS = ["Mon", "Tue", "Wed"]


def pivot_sales(rows):
    # Anchor: one row per store. Recursive idea is not needed here; this is a rotation.
    by_store = {}
    for row in rows:
        by_store.setdefault(row["store"], {day: 0 for day in DAYS})
        by_store[row["store"]][row["day"]] += row["sales"]

    pivoted = []
    for store in sorted(by_store.keys()):
        pivoted.append({"store": store, **by_store[store]})
    return pivoted


def unpivot_sales(rows):
    # Take wide columns and turn them into (store, day, sales) rows.
    unpivoted = []
    for row in rows:
        store = row["store"]
        for day in DAYS:
            unpivoted.append({"store": store, "day": day, "sales": row[day]})
    return unpivoted


def run_pivot_unpivot_demo():
    print("=" * 72)
    print("Raw data (row-shaped):")
    for row in RAW_SALES:
        print(row)

    print("=" * 72)
    print("Scenario A: Pivot to cross-tab shape (stores as rows, days as columns)")
    pivoted = pivot_sales(RAW_SALES)
    for row in pivoted:
        print(row)

    print("=" * 72)
    print("Scenario B: Unpivot back to row shape")
    unpivoted = unpivot_sales(pivoted)
    for row in unpivoted:
        print(row)

    print("=" * 72)
    print("Interpretation:")
    print("- Pivot rotates rows into columns for human-friendly reporting.")
    print("- Unpivot restores the tall, row-oriented shape for analytics.")
    print("- The data is the same; only the shape changes.")


if __name__ == "__main__":
    run_pivot_unpivot_demo()

# Takeaway:
# Pivot = wide. Unpivot = tall.
