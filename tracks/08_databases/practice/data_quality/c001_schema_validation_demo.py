# Story:
# A pipeline expects a stable schema before loading curated tables.
# Incoming batches are validated; bad rows are rejected.

EXPECTED_SCHEMA = {
    "order_id": str,
    "customer": str,
    "amount": float,
    "status": str,
}

GOOD_BATCH = [
    {"order_id": "o100", "customer": "Ava", "amount": 120.5, "status": "PAID"},
    {"order_id": "o101", "customer": "Ben", "amount": 85.0, "status": "PAID"},
]

BAD_BATCH = [
    {"order_id": "o102", "customer_name": "Cara", "amount": 200.0, "status": "PAID"},
    {"order_id": "o103", "customer": "Dee", "amount": "N/A", "status": "PAID"},
]


def _validate_row(row, schema):
    issues = []
    for field, field_type in schema.items():
        if field not in row:
            issues.append(f"missing {field}")
            continue

        value = row[field]
        if field_type is float:
            if not isinstance(value, (int, float)):
                issues.append(f"{field} not numeric")
        elif not isinstance(value, field_type):
            issues.append(f"{field} wrong type")

    extra = set(row.keys()) - set(schema.keys())
    if extra:
        issues.append(f"extra fields {sorted(extra)}")

    return issues


def validate_batch(rows, schema):
    failures = []
    for row in rows:
        issues = _validate_row(row, schema)
        if issues:
            failures.append({"row": row, "issues": issues})
    return failures


def run_schema_validation_demo():
    print("=" * 72)
    print("Scenario: schema validation for incoming batches")

    print("\nExpected schema:")
    for field, field_type in EXPECTED_SCHEMA.items():
        print(f"  {field}: {field_type.__name__}")

    print("\nBatch A (clean)")
    clean_failures = validate_batch(GOOD_BATCH, EXPECTED_SCHEMA)
    print("Failures:", clean_failures)
    print("Result:", "PASS" if not clean_failures else "FAIL")

    print("\nBatch B (bad data)")
    bad_failures = validate_batch(BAD_BATCH, EXPECTED_SCHEMA)
    print("Failures:")
    for failure in bad_failures:
        print(f"  {failure}")
    print("Result:", "PASS" if not bad_failures else "FAIL")

    print("\nSummary")
    print("- Schema validation checks required fields and types.")
    print("- Bad rows are rejected before loading curated tables.")


if __name__ == "__main__":
    run_schema_validation_demo()

# Takeaway: Validate schema early to prevent bad data from spreading.
