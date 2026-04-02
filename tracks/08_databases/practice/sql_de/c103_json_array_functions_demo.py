# Story:
# JSON functions extract fields. Array functions explode lists into rows.

CUSTOMERS = [
    {
        "id": 1,
        "profile": {"name": "Ava", "city": "Austin"},
        "orders": [
            {"order_id": "o100", "amount": 120},
            {"order_id": "o101", "amount": 80},
        ],
    },
    {
        "id": 2,
        "profile": {"name": "Ben", "city": "Boston"},
        "orders": [
            {"order_id": "o200", "amount": 60},
            {"order_id": "o201", "amount": 140},
            {"order_id": "o202", "amount": 30},
        ],
    },
]


def extract_fields(rows):
    # JSON-style extraction: pull nested fields into flat columns.
    extracted = []
    for row in rows:
        extracted.append(
            {
                "customer_id": row["id"],
                "name": row["profile"]["name"],
                "city": row["profile"]["city"],
            }
        )
    return extracted


def explode_orders(rows):
    # Array-style explosion: one row per order item.
    exploded = []
    for row in rows:
        for order in row["orders"]:
            exploded.append(
                {
                    "customer_id": row["id"],
                    "name": row["profile"]["name"],
                    "order_id": order["order_id"],
                    "amount": order["amount"],
                }
            )
    return exploded


def summarize_by_customer(rows):
    summary = {}
    for row in rows:
        summary.setdefault(row["customer_id"], {"name": row["name"], "total": 0})
        summary[row["customer_id"]]["total"] += row["amount"]

    result = []
    for customer_id in sorted(summary.keys()):
        result.append(
            {
                "customer_id": customer_id,
                "name": summary[customer_id]["name"],
                "total_amount": summary[customer_id]["total"],
            }
        )
    return result


def run_json_array_demo():
    print("=" * 72)
    print("Raw nested data:")
    for row in CUSTOMERS:
        print(row)

    print("=" * 72)
    print("Scenario A: Extract JSON fields (name, city)")
    extracted = extract_fields(CUSTOMERS)
    for row in extracted:
        print(row)

    print("=" * 72)
    print("Scenario B: Explode order arrays into row form")
    exploded = explode_orders(CUSTOMERS)
    for row in exploded:
        print(row)

    print("=" * 72)
    print("Scenario C: Regroup after explosion (total spend per customer)")
    summarized = summarize_by_customer(exploded)
    for row in summarized:
        print(row)

    print("=" * 72)
    print("Interpretation:")
    print("- JSON functions extract nested fields into columns.")
    print("- Array functions turn list items into rows.")
    print("- After exploding, regroup to build clean summaries.")


if __name__ == "__main__":
    run_json_array_demo()

# Takeaway:
# Extract, explode, regroup.
