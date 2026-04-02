# Story:
# SCD Type 1 overwrites the dimension row in place.
# Facts always resolve to the latest attributes, and history is lost.


FACT_SALES = [
    {"sale_id": 1, "customer_id": "C1", "amount": 120},
    {"sale_id": 2, "customer_id": "C1", "amount": 80},
]

DIM_CUSTOMER = {
    "C1": {"name": "Ava", "segment": "consumer"},
}


def _print_dimension(label):
    print(f"[DIM] customers {label}")
    for key, row in DIM_CUSTOMER.items():
        print(f"  {key} -> {row}")


def _join_facts_to_dimension():
    # Facts resolve to whatever the dimension shows right now.
    joined = []
    for fact in FACT_SALES:
        customer = DIM_CUSTOMER[fact["customer_id"]]
        joined.append(
            {
                "sale_id": fact["sale_id"],
                "amount": fact["amount"],
                "customer": customer["name"],
                "segment": customer["segment"],
            }
        )
    return joined


def run_scd_type1_demo():
    print("SCD Type 1 demo: overwrite in place")
    print("Step 1: dimension before change")
    _print_dimension("(before)")
    print("Facts joined to dimension (before)")
    for row in _join_facts_to_dimension():
        print(row)

    print("Step 2: overwrite dimension attribute")
    DIM_CUSTOMER["C1"]["segment"] = "business"
    _print_dimension("(after overwrite)")

    print("Step 3: facts now see latest value only")
    for row in _join_facts_to_dimension():
        print(row)

    print("Summary")
    print("Type 1 overwrites in place; old attribute values are lost.")


if __name__ == "__main__":
    run_scd_type1_demo()

# Takeaway:
# SCD Type 1 keeps only the latest attributes.
