# Story:
# Snowflake schema normalizes dimensions into sub-dimensions.
# Queries need extra joins compared to a star schema.


FACT_SALES = [
    {"sale_id": 1, "customer_id": "C1", "product_id": "P1", "date_id": "D1", "amount": 120},
    {"sale_id": 2, "customer_id": "C2", "product_id": "P2", "date_id": "D1", "amount": 80},
    {"sale_id": 3, "customer_id": "C1", "product_id": "P2", "date_id": "D2", "amount": 200},
]

DIM_CUSTOMER = {
    "C1": {"name": "Ava", "segment": "consumer"},
    "C2": {"name": "Ben", "segment": "business"},
}

# Product dimension is normalized into category and department.
DIM_PRODUCT = {
    "P1": {"product": "Notebook", "category_id": "CAT1"},
    "P2": {"product": "Headphones", "category_id": "CAT2"},
}

DIM_CATEGORY = {
    "CAT1": {"category": "office", "department_id": "DEP1"},
    "CAT2": {"category": "electronics", "department_id": "DEP2"},
}

DIM_DEPARTMENT = {
    "DEP1": {"department": "business supplies"},
    "DEP2": {"department": "tech"},
}

DIM_DATE = {
    "D1": {"date": "2024-01-05", "month": "2024-01"},
    "D2": {"date": "2024-01-06", "month": "2024-01"},
}


def _print_snowflake_schema():
    print("[FACT] sales (hub)")
    for row in FACT_SALES:
        print(row)
    print("[DIM] customers")
    for key, row in DIM_CUSTOMER.items():
        print(f"  {key} -> {row}")
    print("[DIM] products")
    for key, row in DIM_PRODUCT.items():
        print(f"  {key} -> {row}")
    print("[DIM] categories")
    for key, row in DIM_CATEGORY.items():
        print(f"  {key} -> {row}")
    print("[DIM] departments")
    for key, row in DIM_DEPARTMENT.items():
        print(f"  {key} -> {row}")
    print("[DIM] dates")
    for key, row in DIM_DATE.items():
        print(f"  {key} -> {row}")


def join_snowflake():
    # Join fact -> product -> category -> department (extra hops).
    enriched = []
    for fact in FACT_SALES:
        customer = DIM_CUSTOMER[fact["customer_id"]]
        product = DIM_PRODUCT[fact["product_id"]]
        category = DIM_CATEGORY[product["category_id"]]
        department = DIM_DEPARTMENT[category["department_id"]]
        date = DIM_DATE[fact["date_id"]]
        enriched.append(
            {
                "sale_id": fact["sale_id"],
                "amount": fact["amount"],
                "customer": customer["name"],
                "segment": customer["segment"],
                "product": product["product"],
                "category": category["category"],
                "department": department["department"],
                "month": date["month"],
            }
        )
    return enriched


def summarize_by_category(enriched_rows):
    totals = {}
    for row in enriched_rows:
        totals[row["category"]] = totals.get(row["category"], 0) + row["amount"]
    return totals


def run_snowflake_schema_demo():
    print("Snowflake schema demo: normalized dimensions")
    print("Step 1: show snowflake tables")
    _print_snowflake_schema()

    print("Step 2: join fact to dimensions (extra hops)")
    enriched = join_snowflake()
    for row in enriched:
        print(row)

    print("Step 3: analytics query (total sales by category)")
    totals = summarize_by_category(enriched)
    for category, total in totals.items():
        print(f"  category={category} total={total}")

    print("Summary")
    print("Snowflake normalizes dimensions, so queries use more joins than star.")


if __name__ == "__main__":
    run_snowflake_schema_demo()

# Takeaway:
# Snowflake schema reduces duplication but adds join depth.
