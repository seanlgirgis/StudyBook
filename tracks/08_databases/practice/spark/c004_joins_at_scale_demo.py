# Story:
# Joins are cheap when matching keys live together. When they do not, data must move.
# At scale, that shuffle is the expensive part.


ORDERS = [
    {"order_id": "o1", "customer_id": "c1", "amount": 120.0},
    {"order_id": "o2", "customer_id": "c2", "amount": 85.0},
    {"order_id": "o3", "customer_id": "c1", "amount": 25.0},
    {"order_id": "o4", "customer_id": "c3", "amount": 200.0},
    {"order_id": "o5", "customer_id": "c2", "amount": 15.0},
]

CUSTOMERS = [
    {"customer_id": "c1", "name": "Ava", "tier": "gold"},
    {"customer_id": "c2", "name": "Ben", "tier": "silver"},
    {"customer_id": "c3", "name": "Cara", "tier": "gold"},
]


def _partition(rows, key_fn, num_partitions):
    partitions = [[] for _ in range(num_partitions)]
    for row in rows:
        key = key_fn(row)
        index = sum(ord(ch) for ch in key) % num_partitions
        partitions[index].append(row)
    return partitions


def _print_partitions(label, partitions):
    print(label)
    for index, rows in enumerate(partitions):
        print(f"Partition {index}:")
        for row in rows:
            print(f"  {row}")


def _local_join(orders_partition, customers_partition):
    customers_by_id = {row["customer_id"]: row for row in customers_partition}
    joined = []
    for order in orders_partition:
        customer = customers_by_id.get(order["customer_id"])
        if customer:
            joined.append({**order, **customer})
    return joined


def _shuffle_partitions(partitions, key_fn, num_partitions):
    new_partitions = [[] for _ in range(num_partitions)]
    movement = []
    for old_index, rows in enumerate(partitions):
        for row in rows:
            key = key_fn(row)
            new_index = sum(ord(ch) for ch in key) % num_partitions
            if new_index != old_index:
                movement.append((row, old_index, new_index))
            new_partitions[new_index].append(row)
    print("Rows moved between partitions:")
    for row, old_index, new_index in movement:
        print(f"  {row['order_id']} moved P{old_index} -> P{new_index}")
    if not movement:
        print("  (no movement, already co-partitioned)")
    return new_partitions


def run_joins_at_scale_demo():
    print("=" * 72)
    print("Scenario: join orders to customers in a partitioned system")

    print("=" * 72)
    print("Case A: co-partitioned by customer_id (local join)")
    orders_by_customer = _partition(ORDERS, lambda row: row["customer_id"], 3)
    customers_by_customer = _partition(CUSTOMERS, lambda row: row["customer_id"], 3)
    _print_partitions("Orders partitions:", orders_by_customer)
    _print_partitions("Customers partitions:", customers_by_customer)

    joined_local = []
    for index in range(3):
        joined_local.extend(_local_join(orders_by_customer[index], customers_by_customer[index]))

    print("Local join result:")
    for row in joined_local:
        print(row)

    print("=" * 72)
    print("Case B: partitions misaligned (shuffle before join)")
    orders_by_order_id = _partition(ORDERS, lambda row: row["order_id"], 3)
    _print_partitions("Orders partitions (by order_id):", orders_by_order_id)
    _print_partitions("Customers partitions (by customer_id):", customers_by_customer)

    print("Shuffle orders to align by customer_id:")
    shuffled_orders = _shuffle_partitions(orders_by_order_id, lambda row: row["customer_id"], 3)
    _print_partitions("Orders partitions after shuffle:", shuffled_orders)

    joined_shuffle = []
    for index in range(3):
        joined_shuffle.extend(_local_join(shuffled_orders[index], customers_by_customer[index]))

    print("Shuffled join result:")
    for row in joined_shuffle:
        print(row)

    print("=" * 72)
    print("Summary:")
    print("- Co-partitioned joins are local and cheaper.")
    print("- Misaligned joins require shuffling rows across partitions.")
    print("- Shuffles make joins at scale expensive.")


if __name__ == "__main__":
    run_joins_at_scale_demo()

# Takeaway: Joins are cheap when data is co-partitioned and expensive when a shuffle is required.