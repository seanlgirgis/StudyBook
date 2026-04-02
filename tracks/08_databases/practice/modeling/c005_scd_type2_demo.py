# Story:
# SCD Type 2 keeps history by creating a new dimension row on change.
# Facts join to the version that was current at the time of the fact.


DIM_CUSTOMER = [
    {
        "customer_id": "C1",
        "name": "Ava",
        "segment": "consumer",
        "effective_start": "2024-01-01",
        "effective_end": "2024-01-31",
        "current_flag": False,
    },
    {
        "customer_id": "C1",
        "name": "Ava",
        "segment": "business",
        "effective_start": "2024-02-01",
        "effective_end": "9999-12-31",
        "current_flag": True,
    },
]

FACT_SALES = [
    {"sale_id": 1, "customer_id": "C1", "sale_date": "2024-01-10", "amount": 120},
    {"sale_id": 2, "customer_id": "C1", "sale_date": "2024-02-10", "amount": 80},
]


def _print_dimension():
    print("[DIM] customers (type 2 history)")
    for row in DIM_CUSTOMER:
        print(row)


def _version_for(customer_id, sale_date):
    # Find the dimension version that was current at the time.
    for row in DIM_CUSTOMER:
        if row["customer_id"] != customer_id:
            continue
        if row["effective_start"] <= sale_date <= row["effective_end"]:
            return row
    return None


def _join_facts_to_dimension():
    joined = []
    for fact in FACT_SALES:
        version = _version_for(fact["customer_id"], fact["sale_date"])
        joined.append(
            {
                "sale_id": fact["sale_id"],
                "sale_date": fact["sale_date"],
                "amount": fact["amount"],
                "customer": version["name"],
                "segment": version["segment"],
                "current_flag": version["current_flag"],
            }
        )
    return joined


def run_scd_type2_demo():
    print("SCD Type 2 demo: preserve history")
    print("Step 1: dimension with history rows")
    _print_dimension()

    print("Step 2: facts join to the right version")
    for row in _join_facts_to_dimension():
        print(row)

    print("Summary")
    print("Type 2 keeps history so old facts see old attributes.")


if __name__ == "__main__":
    run_scd_type2_demo()

# Takeaway:
# SCD Type 2 adds new rows and preserves history.
