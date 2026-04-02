# Story:
# Orders reference customers. Referential checks ensure every order has a
# valid customer_id. Orphans are rejected until the parent exists.

CUSTOMERS = [
    {"customer_id": "c001", "name": "Ava"},
    {"customer_id": "c002", "name": "Ben"},
]

ORDERS_WITH_ORPHANS = [
    {"order_id": "o100", "customer_id": "c001", "amount": 120.5},
    {"order_id": "o101", "customer_id": "c999", "amount": 85.0},
    {"order_id": "o102", "customer_id": "c002", "amount": 42.0},
]

ORDERS_FIXED = [
    {"order_id": "o100", "customer_id": "c001", "amount": 120.5},
    {"order_id": "o101", "customer_id": "c003", "amount": 85.0},
    {"order_id": "o102", "customer_id": "c002", "amount": 42.0},
]

CUSTOMERS_UPDATED = [
    {"customer_id": "c001", "name": "Ava"},
    {"customer_id": "c002", "name": "Ben"},
    {"customer_id": "c003", "name": "Cara"},
]


def find_orphans(orders, customers):
    customer_ids = {row["customer_id"] for row in customers}
    orphans = []
    for order in orders:
        if order["customer_id"] not in customer_ids:
            orphans.append(order)
    return orphans


def run_referential_integrity_demo():
    print("=" * 72)
    print("Scenario: referential integrity checks")

    print("\nCheck 1: orders with missing parents")
    orphans = find_orphans(ORDERS_WITH_ORPHANS, CUSTOMERS)
    print("Orphans:")
    for orphan in orphans:
        print(f"  {orphan}")
    print("Result:", "PASS" if not orphans else "FAIL")

    print("\nCheck 2: corrected parents arrive")
    orphans_fixed = find_orphans(ORDERS_FIXED, CUSTOMERS_UPDATED)
    print("Orphans:", orphans_fixed)
    print("Result:", "PASS" if not orphans_fixed else "FAIL")

    print("\nSummary")
    print("- Referential integrity ensures child rows reference valid parents.")
    print("- Orphan rows are blocked until the parent data arrives.")


if __name__ == "__main__":
    run_referential_integrity_demo()

# Takeaway: Parent-child checks prevent orphan records in curated tables.
