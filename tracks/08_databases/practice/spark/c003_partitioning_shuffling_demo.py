# Story:
# Data feels fast when each partition works alone. Then a group-by forces a shuffle.
# Shuffles move rows between partitions and cost real time.


RAW_ORDERS = [
    {"order_id": "o1", "customer": "Ava", "amount": 120.0},
    {"order_id": "o2", "customer": "Ben", "amount": 85.0},
    {"order_id": "o3", "customer": "Ava", "amount": 25.0},
    {"order_id": "o4", "customer": "Cara", "amount": 200.0},
    {"order_id": "o5", "customer": "Ben", "amount": 15.0},
    {"order_id": "o6", "customer": "Drew", "amount": 40.0},
]


def _print_partitions(label, partitions):
    print(label)
    for index, rows in enumerate(partitions):
        print(f"Partition {index}:")
        for row in rows:
            print(f"  {row}")


def _partition_rows(rows, num_partitions):
    partitions = [[] for _ in range(num_partitions)]
    for row in rows:
        order_id = row["order_id"]
        partition_index = sum(ord(ch) for ch in order_id) % num_partitions
        partitions[partition_index].append(row)
    return partitions


def _narrow_filter(partitions, min_amount):
    print(f"Narrow filter: amount > {min_amount} (no movement)")
    new_partitions = []
    for rows in partitions:
        filtered = [row for row in rows if row["amount"] > min_amount]
        new_partitions.append(filtered)
    return new_partitions


def _shuffle_by_key(partitions, key_fn, num_partitions):
    print("Shuffle: regroup rows by key")
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
        print(f"  {row['order_id']} ({row['customer']}) moved P{old_index} -> P{new_index}")
    if not movement:
        print("  (no movement, keys already aligned)")

    return new_partitions


def _group_by_customer(partitions):
    totals = {}
    for rows in partitions:
        for row in rows:
            customer = row["customer"]
            totals[customer] = totals.get(customer, 0.0) + row["amount"]
    return totals


def run_partitioning_shuffling_demo():
    print("=" * 72)
    print("Scenario: compute revenue per customer in a partitioned system")
    partitions = _partition_rows(RAW_ORDERS, 3)
    _print_partitions("Initial partitions:", partitions)

    print("=" * 72)
    filtered = _narrow_filter(partitions, 50.0)
    _print_partitions("After narrow filter (same partitions):", filtered)

    print("=" * 72)
    shuffled = _shuffle_by_key(filtered, lambda row: row["customer"], 3)
    _print_partitions("After shuffle (repartition by customer):", shuffled)

    print("=" * 72)
    totals = _group_by_customer(shuffled)
    print("Final grouped totals:")
    for customer in sorted(totals):
        print(f"- {customer}: {totals[customer]}")

    print("=" * 72)
    print("Summary:")
    print("- Narrow transformations stay inside each partition.")
    print("- Shuffles move rows across the network to regroup by key.")
    print("- Shuffles are expensive compared to partition-local work.")


if __name__ == "__main__":
    run_partitioning_shuffling_demo()

# Takeaway: Partition-local work is cheap; shuffles move data and cost more.
