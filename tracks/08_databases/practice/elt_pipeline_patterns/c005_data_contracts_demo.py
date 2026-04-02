# Story:
# A producer publishes an orders feed. The data contract defines required fields
# and allowed status values. Consumers rely on that contract.

CONTRACT = {
    "required_fields": {"order_id", "customer", "amount", "status"},
    "allowed_status": {"PAID", "REFUND"},
}

GOOD_BATCH = [
    {"order_id": "o100", "customer": "Ava", "amount": 120.5, "status": "PAID"},
    {"order_id": "o101", "customer": "Ben", "amount": 85.0, "status": "REFUND"},
]

BAD_BATCH = [
    {"order_id": "o102", "customer_name": "Cara", "amount": 200.0, "status": "PAID"},
    {"order_id": "o103", "customer": "Dee", "amount": 42.0, "status": "PENDING"},
]


def _validate_batch(rows, contract):
    violations = []
    for row in rows:
        missing = contract["required_fields"] - set(row.keys())
        if missing:
            violations.append({"row": row, "issue": f"missing {sorted(missing)}"})
            continue

        if row["status"] not in contract["allowed_status"]:
            violations.append({"row": row, "issue": f"invalid status {row['status']}"})

    return violations


def _consume(rows):
    # Consumer assumes contract holds; computes paid revenue.
    revenue = 0.0
    for row in rows:
        if row["status"] == "PAID":
            revenue += float(row["amount"])
    return revenue


def run_data_contracts_demo():
    print("=" * 72)
    print("Scenario: data contracts (producer vs consumer)")

    print("\nBatch A: contract respected")
    violations = _validate_batch(GOOD_BATCH, CONTRACT)
    print("Violations:", violations)
    revenue = _consume(GOOD_BATCH)
    print(f"Consumer revenue: {revenue}")

    print("\nBatch B: contract broken")
    violations = _validate_batch(BAD_BATCH, CONTRACT)
    print("Violations:", violations)

    if violations:
        print("Consumer stops: contract violated")
    else:
        revenue = _consume(BAD_BATCH)
        print(f"Consumer revenue: {revenue}")

    print("\nSummary")
    print("- Data contract defines required fields and allowed values.")
    print("- Producers must publish to the contract; consumers trust it.")
    print("- Contract checks prevent silent downstream breakage.")


if __name__ == "__main__":
    run_data_contracts_demo()

# Takeaway: Contracts are shared promises; validation protects downstream users.
