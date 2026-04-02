# Story:
# Star schema centers a fact table and connects to multiple dimensions.
# Analytics joins the fact to dimensions to produce summaries.


FACT_SALES = [
    {"sale_id": 1, "customer_id": "C1", "product_id": "P1", "date_id": "D1", "amount": 120},
    {"sale_id": 2, "customer_id": "C2", "product_id": "P2", "date_id": "D1", "amount": 80},
    {"sale_id": 3, "customer_id": "C1", "product_id": "P2", "date_id": "D2", "amount": 200},
]

DIM_CUSTOMER = {
    "C1": {"name": "Ava", "segment": "consumer"},
    "C2": {"name": "Ben", "segment": "business"},
}

DIM_PRODUCT = {
    "P1": {"product": "Notebook", "category": "office"},
    "P2": {"product": "Headphones", "category": "electronics"},
}

DIM_DATE = {
    "D1": {"date": "2024-01-05", "month": "2024-01"},
    "D2": {"date": "2024-01-06", "month": "2024-01"},
}


def _print_star_schema():
    print("[FACT] sales (hub)")
    for row in FACT_SALES:
        print(row)
    print("[DIM] customers (spoke)")
    for key, row in DIM_CUSTOMER.items():
        print(f"  {key} -> {row}")
    print("[DIM] products (spoke)")
    for key, row in DIM_PRODUCT.items():
        print(f"  {key} -> {row}")
    print("[DIM] dates (spoke)")
    for key, row in DIM_DATE.items():
        print(f"  {key} -> {row}")


def join_star():
    # Join the fact hub to each dimension spoke.
    enriched = []
    for fact in FACT_SALES:
        customer = DIM_CUSTOMER[fact["customer_id"]]
        product = DIM_PRODUCT[fact["product_id"]]
        date = DIM_DATE[fact["date_id"]]
        enriched.append(
            {
                "sale_id": fact["sale_id"],
                "amount": fact["amount"],
                "customer": customer["name"],
                "segment": customer["segment"],
                "product": product["product"],
                "category": product["category"],
                "month": date["month"],
            }
        )
    return enriched


def summarize_by_category(enriched_rows):
    totals = {}
    for row in enriched_rows:
        totals[row["category"]] = totals.get(row["category"], 0) + row["amount"]
    return totals


def run_star_schema_demo():
    print("Star schema demo: fact hub + dimension spokes")
    print("Step 1: show schema tables")
    _print_star_schema()

    print("Step 2: join fact to dimensions (star shape)")
    enriched = join_star()
    for row in enriched:
        print(row)

    print("Step 3: analytics query (total sales by category)")
    totals = summarize_by_category(enriched)
    for category, total in totals.items():
        print(f"  category={category} total={total}")

    print("Summary")
    print("Star schema joins one fact to many dimensions for fast analytics.")


if __name__ == "__main__":
    run_star_schema_demo()

# Takeaway:
# Star schema is a hub-and-spoke model for analytics queries.
