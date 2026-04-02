# Story:
# Data vault separates business keys (hubs), relationships (links),
# and descriptive history (satellites).


HUB_CUSTOMER = [
    {"customer_id": "C1"},
]

HUB_PRODUCT = [
    {"product_id": "P1"},
]

LINK_SALE = [
    {"link_id": "L1", "customer_id": "C1", "product_id": "P1", "load_date": "2024-01-10"},
    {"link_id": "L2", "customer_id": "C1", "product_id": "P1", "load_date": "2024-02-10"},
]

SAT_CUSTOMER = [
    {"customer_id": "C1", "segment": "consumer", "effective_start": "2024-01-01", "effective_end": "2024-01-31"},
    {"customer_id": "C1", "segment": "business", "effective_start": "2024-02-01", "effective_end": "9999-12-31"},
]

SAT_PRODUCT = [
    {"product_id": "P1", "category": "office", "effective_start": "2024-01-01", "effective_end": "9999-12-31"},
]

SAT_SALE = [
    {"link_id": "L1", "amount": 120},
    {"link_id": "L2", "amount": 80},
]


def _print_vault_tables():
    print("[HUB] customers")
    for row in HUB_CUSTOMER:
        print(row)
    print("[HUB] products")
    for row in HUB_PRODUCT:
        print(row)
    print("[LINK] sales")
    for row in LINK_SALE:
        print(row)
    print("[SAT] customer history")
    for row in SAT_CUSTOMER:
        print(row)
    print("[SAT] product history")
    for row in SAT_PRODUCT:
        print(row)
    print("[SAT] sale details")
    for row in SAT_SALE:
        print(row)


def _sat_for(rows, key_name, key_value, as_of_date):
    for row in rows:
        if row[key_name] != key_value:
            continue
        if row["effective_start"] <= as_of_date <= row["effective_end"]:
            return row
    return None


def reconstruct_sales_view():
    # Reconstruct a usable view by joining hubs, links, and satellites.
    view = []
    for link in LINK_SALE:
        customer = _sat_for(SAT_CUSTOMER, "customer_id", link["customer_id"], link["load_date"])
        product = _sat_for(SAT_PRODUCT, "product_id", link["product_id"], link["load_date"])
        sale = next(row for row in SAT_SALE if row["link_id"] == link["link_id"])
        view.append(
            {
                "link_id": link["link_id"],
                "load_date": link["load_date"],
                "customer_id": link["customer_id"],
                "product_id": link["product_id"],
                "segment": customer["segment"],
                "category": product["category"],
                "amount": sale["amount"],
            }
        )
    return view


def run_data_vault_demo():
    print("Data vault demo: hubs, links, satellites")
    print("Step 1: show vault tables (separated)")
    _print_vault_tables()

    print("Step 2: reconstruct a usable view with history")
    for row in reconstruct_sales_view():
        print(row)

    print("Summary")
    print("Hubs store keys, links store relationships, satellites store history.")


if __name__ == "__main__":
    run_data_vault_demo()

# Takeaway:
# Data vault preserves history by keeping descriptive changes in satellites.
