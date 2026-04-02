# Story:
# A big fact table needs a tiny lookup table. Shuffling the big side is expensive.
# Broadcasting the small side keeps the large data in place.


ORDERS = [
    {"order_id": "o1", "customer_id": "c1", "amount": 120.0},
    {"order_id": "o2", "customer_id": "c2", "amount": 85.0},
    {"order_id": "o3", "customer_id": "c1", "amount": 25.0},
    {"order_id": "o4", "customer_id": "c3", "amount": 200.0},
    {"order_id": "o5", "customer_id": "c2", "amount": 15.0},
    {"order_id": "o6", "customer_id": "c1", "amount": 75.0},
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


def _local_join(orders_partition, customers_lookup):
    joined = []
    for order in orders_partition:
        customer = customers_lookup.get(order["customer_id"])
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
        print("  (no movement, already aligned)")
    return new_partitions


def run_broadcast_joins_demo():
    print("=" * 72)
    print("Scenario: join a large orders table to a tiny customer lookup")

    print("=" * 72)
    orders_by_order_id = _partition(ORDERS, lambda row: row["order_id"], 3)
    _print_partitions("Orders partitions (large table):", orders_by_order_id)

    print("Small lookup table (customers):")
    for row in CUSTOMERS:
        print(f"  {row}")

    print("=" * 72)
    print("Case A: shuffle join (repartition the large table by customer_id)")
    shuffled_orders = _shuffle_partitions(orders_by_order_id, lambda row: row["customer_id"], 3)
    _print_partitions("Orders partitions after shuffle:", shuffled_orders)

    customers_by_customer = _partition(CUSTOMERS, lambda row: row["customer_id"], 3)
    joined_shuffle = []
    for index in range(3):
        customers_lookup = {row["customer_id"]: row for row in customers_by_customer[index]}
        joined_shuffle.extend(_local_join(shuffled_orders[index], customers_lookup))

    print("Shuffled join result:")
    for row in joined_shuffle:
        print(row)

    print("=" * 72)
    print("Case B: broadcast join (copy small table to every partition)")
    broadcast_lookup = {row["customer_id"]: row for row in CUSTOMERS}
    print("Broadcast lookup sent to each partition:")
    print(broadcast_lookup)

    joined_broadcast = []
    for index, partition in enumerate(orders_by_order_id):
        print(f"Join within partition {index} using broadcast lookup")
        joined_broadcast.extend(_local_join(partition, broadcast_lookup))

    print("Broadcast join result:")
    for row in joined_broadcast:
        print(row)

    print("=" * 72)
    print("Summary:")
    print("- Shuffle join moves the large table to align keys.")
    print("- Broadcast join copies the small table to every partition.")
    print("- Broadcasting is cheaper only when the small side fits everywhere.")


if __name__ == "__main__":
    run_broadcast_joins_demo()

# Takeaway: Broadcast joins avoid shuffling the big table when the other side is small.