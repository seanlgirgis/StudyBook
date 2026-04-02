# Story:
# Fact tables store measurable events. Dimension tables store descriptive context.
# Reporting joins facts to dimensions to explain the numbers.


FACT_SALES = [
    {"sale_id": 1, "customer_id": "C1", "product_id": "P1", "amount": 120},
    {"sale_id": 2, "customer_id": "C2", "product_id": "P2", "amount": 80},
    {"sale_id": 3, "customer_id": "C1", "product_id": "P2", "amount": 200},
]

DIM_CUSTOMER = {
    "C1": {"name": "Ava", "segment": "consumer"},
    "C2": {"name": "Ben", "segment": "business"},
}

DIM_PRODUCT = {
    "P1": {"product": "Notebook", "category": "office"},
    "P2": {"product": "Headphones", "category": "electronics"},
}


def _print_facts():
    print("[FACT] sales events")
    for row in FACT_SALES:
        print(row)


def _print_dimensions():
    print("[DIM] customers")
    for key, row in DIM_CUSTOMER.items():
        print(f"  {key} -> {row}")
    print("[DIM] products")
    for key, row in DIM_PRODUCT.items():
        print(f"  {key} -> {row}")


def join_for_reporting():
    # Join facts to dimensions to add descriptive context.
    enriched = []
    for fact in FACT_SALES:
        customer = DIM_CUSTOMER[fact["customer_id"]]
        product = DIM_PRODUCT[fact["product_id"]]
        enriched.append(
            {
                "sale_id": fact["sale_id"],
                "amount": fact["amount"],
                "customer": customer["name"],
                "segment": customer["segment"],
                "product": product["product"],
                "category": product["category"],
            }
        )
    return enriched


def summarize_by_category(enriched_rows):
    totals = {}
    for row in enriched_rows:
        totals[row["category"]] = totals.get(row["category"], 0) + row["amount"]
    return totals


def run_fact_vs_dimension_demo():
    print("Fact vs Dimension demo: events + context")
    print("Step 1: show raw facts (measures only)")
    _print_facts()

    print("Step 2: show dimensions (descriptive attributes)")
    _print_dimensions()

    print("Step 3: join facts to dimensions for reporting")
    enriched = join_for_reporting()
    for row in enriched:
        print(row)

    print("Step 4: aggregate with context (revenue by category)")
    totals = summarize_by_category(enriched)
    for category, total in totals.items():
        print(f"  category={category} total={total}")

    print("Summary")
    print("Facts hold measures. Dimensions explain them.")


if __name__ == "__main__":
    run_fact_vs_dimension_demo()

# Takeaway:
# Facts are measurable events; dimensions give descriptive context.
