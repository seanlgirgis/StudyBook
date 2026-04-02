# Story:
# A pipeline validates customer records for nulls and type mismatches.
# Clean rows pass, bad rows are flagged.

EXPECTED_TYPES = {
    "customer_id": str,
    "name": str,
    "age": int,
    "spend": float,
}

PASSING_ROWS = [
    {"customer_id": "c001", "name": "Ava", "age": 32, "spend": 120.5},
    {"customer_id": "c002", "name": "Ben", "age": 45, "spend": 85.0},
]

FAILING_ROWS = [
    {"customer_id": "c003", "name": None, "age": 27, "spend": 60.0},
    {"customer_id": "c004", "name": "Dee", "age": "unknown", "spend": 42.0},
    {"customer_id": None, "name": "Eli", "age": 29, "spend": "N/A"},
]


def _check_row(row):
    issues = []
    for field, field_type in EXPECTED_TYPES.items():
        value = row.get(field)
        if value is None:
            issues.append(f"{field} is null")
            continue

        if field_type is float:
            if not isinstance(value, (int, float)):
                issues.append(f"{field} type mismatch")
        elif not isinstance(value, field_type):
            issues.append(f"{field} type mismatch")

    return issues


def validate_rows(rows):
    results = []
    for row in rows:
        issues = _check_row(row)
        results.append({"row": row, "issues": issues, "status": "PASS" if not issues else "FAIL"})
    return results


def run_null_type_checks_demo():
    print("=" * 72)
    print("Scenario: null and type checks")

    print("\nPassing rows")
    passing_results = validate_rows(PASSING_ROWS)
    for result in passing_results:
        print(f"  {result}")

    print("\nFailing rows")
    failing_results = validate_rows(FAILING_ROWS)
    for result in failing_results:
        print(f"  {result}")

    print("\nSummary")
    print("- Null checks catch missing values in required fields.")
    print("- Type checks catch mismatched data types before loading.")


if __name__ == "__main__":
    run_null_type_checks_demo()

# Takeaway: Null and type checks protect downstream quality.
