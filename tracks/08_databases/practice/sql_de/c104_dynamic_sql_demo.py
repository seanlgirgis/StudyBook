# Story:
# Dynamic SQL builds query text at runtime. Use allowlists and parameters.

ALLOWED_COLUMNS = {"customer_id", "region", "total_spend"}
ALLOWED_FILTERS = {"region", "min_spend"}


def build_unsafe_query(request):
    # Dangerous: direct string concatenation with user input.
    select_clause = ", ".join(request["columns"])
    where_clause = " AND ".join(
        f"{key} = '{value}'" for key, value in request["filters"].items()
    )
    return f"SELECT {select_clause} FROM customer_rollup WHERE {where_clause};"


def build_safe_query(request):
    # Safe pattern: allowlist columns and parameterize values.
    safe_columns = [c for c in request["columns"] if c in ALLOWED_COLUMNS]
    select_clause = ", ".join(safe_columns) if safe_columns else "customer_id"

    filters = []
    params = {}
    for key, value in request["filters"].items():
        if key not in ALLOWED_FILTERS:
            continue
        if key == "min_spend":
            filters.append("total_spend >= :min_spend")
            params["min_spend"] = value
        elif key == "region":
            filters.append("region = :region")
            params["region"] = value

    where_clause = " AND ".join(filters) if filters else "1 = 1"
    query = f"SELECT {select_clause} FROM customer_rollup WHERE {where_clause};"
    return query, params


def run_dynamic_sql_demo():
    request = {
        "columns": ["customer_id", "region", "total_spend; DROP TABLE users;--"],
        "filters": {"region": "Northeast", "min_spend": 100, "ignore": "x' OR '1'='1"},
    }

    print("=" * 72)
    print("Raw request inputs:")
    print(request)

    print("=" * 72)
    print("Unsafe query string (do NOT do this):")
    print(build_unsafe_query(request))

    print("=" * 72)
    print("Safe query template (allowlisted columns + parameters):")
    safe_query, safe_params = build_safe_query(request)
    print(safe_query)

    print("=" * 72)
    print("Safe parameter payload:")
    print(safe_params)

    print("=" * 72)
    print("Interpretation:")
    print("- Unsafe concatenation lets attacker input change SQL structure.")
    print("- Safe construction picks known columns and binds values separately.")
    print("- Dynamic SQL is fine when you control the shape and parameters.")


if __name__ == "__main__":
    run_dynamic_sql_demo()

# Takeaway:
# Dynamic SQL needs allowlists and parameters.
