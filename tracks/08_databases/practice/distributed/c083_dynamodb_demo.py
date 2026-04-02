# Story:
# DynamoDB routes items by partition key and orders them by sort key.
# This demo shows good access patterns, point reads, and why GSIs exist.

import hashlib
import bisect


NODES = ["p1", "p2", "p3", "p4"]


def _hash_key(key):
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()
    return int(digest, 16)


class Partition:
    def __init__(self, name):
        self.name = name
        self.items_by_pk = {}
        self.gsi_status = {}

    def put_item(self, item, sk_field):
        pk = item["customer_id"]
        rows = self.items_by_pk.setdefault(pk, [])
        positions = [existing[sk_field] for existing in rows]
        idx = bisect.bisect_left(positions, item[sk_field])
        rows.insert(idx, item)

        status = item["status"]
        status_rows = self.gsi_status.setdefault(status, [])
        status_rows.append(item)

    def read_partition(self, pk):
        return list(self.items_by_pk.get(pk, []))

    def point_read(self, pk, sk_field, sk_value):
        for item in self.items_by_pk.get(pk, []):
            if item[sk_field] == sk_value:
                return item
        return None

    def scan_by_status(self, status):
        matches = []
        partitions_scanned = 0
        for pk, rows in self.items_by_pk.items():
            partitions_scanned += 1
            for item in rows:
                if item["status"] == status:
                    matches.append(item)
        return matches, partitions_scanned

    def gsi_query_status(self, status):
        return list(self.gsi_status.get(status, []))


class Table:
    def __init__(self, nodes):
        self.partitions = [Partition(name) for name in nodes]

    def _partition_for_key(self, pk):
        idx = _hash_key(pk) % len(self.partitions)
        return self.partitions[idx], idx

    def put_item(self, item, sk_field):
        partition, _ = self._partition_for_key(item["customer_id"])
        partition.put_item(item, sk_field)

    def query_customer(self, pk):
        partition, _ = self._partition_for_key(pk)
        return partition.read_partition(pk), partition.name

    def point_get(self, pk, sk_field, sk_value):
        partition, _ = self._partition_for_key(pk)
        return partition.point_read(pk, sk_field, sk_value), partition.name

    def scan_status(self, status):
        matches = []
        partitions_scanned = 0
        partitions_touched = 0
        for partition in self.partitions:
            part_matches, scanned = partition.scan_by_status(status)
            if scanned > 0:
                partitions_touched += 1
            partitions_scanned += scanned
            matches.extend(part_matches)
        return matches, partitions_touched, partitions_scanned

    def gsi_query(self, status):
        matches = []
        partitions_touched = 0
        for partition in self.partitions:
            part_matches = partition.gsi_query_status(status)
            if part_matches:
                partitions_touched += 1
            matches.extend(part_matches)
        return matches, partitions_touched


def _print_items(label, items):
    print(label)
    for item in items:
        print(f"  {item['customer_id']} | {item['order_ts']} | {item['status']} | {item['total']} | {item['region']}")


def run_dynamodb_demo():
    table = Table(NODES)

    items = [
        {"customer_id": "cust-1", "order_ts": 1, "order_id": "o-101", "status": "placed", "total": 42, "region": "us"},
        {"customer_id": "cust-1", "order_ts": 3, "order_id": "o-103", "status": "shipped", "total": 18, "region": "us"},
        {"customer_id": "cust-1", "order_ts": 2, "order_id": "o-102", "status": "packed", "total": 33, "region": "us"},
        {"customer_id": "cust-2", "order_ts": 1, "order_id": "o-201", "status": "shipped", "total": 70, "region": "eu"},
        {"customer_id": "cust-3", "order_ts": 1, "order_id": "o-301", "status": "placed", "total": 12, "region": "apac"},
        {"customer_id": "cust-2", "order_ts": 2, "order_id": "o-202", "status": "shipped", "total": 25, "region": "eu"},
    ]

    print("=" * 72)
    print("Table: Orders (pk=customer_id, sk=order_ts)")

    sample_key = "cust-1"
    partition, idx = table._partition_for_key(sample_key)
    print(f"Partition for {sample_key}: {partition.name} (index {idx})")
    partition_again, _ = table._partition_for_key(sample_key)
    print(f"Same key routes consistently: {partition_again.name}")

    for item in items:
        table.put_item(item, "order_ts")

    print("=" * 72)
    print("Scenario A: Good query (orders for one customer)")
    rows, partition_name = table.query_customer("cust-1")
    print(f"Partition touched: {partition_name}")
    _print_items("Ordered orders for cust-1:", rows)

    print("=" * 72)
    print("Scenario B: Point read (pk + sk)")
    order, partition_name = table.point_get("cust-1", "order_ts", 2)
    print(f"Partition touched: {partition_name}")
    print(f"Point read result: {order}")

    print("=" * 72)
    print("Scenario C: Bad query (status = shipped across all customers)")
    matches, partitions_touched, partitions_scanned = table.scan_status("shipped")
    print(f"Partitions touched: {partitions_touched} / {len(NODES)}")
    print(f"Partitions scanned: {partitions_scanned}")
    print(f"Matches found: {len(matches)}")
    print("Warning: This requires a scan without a GSI.")

    print("=" * 72)
    print("Scenario D: GSI-like query on status")
    matches, partitions_touched = table.gsi_query("shipped")
    print(f"Partitions touched by GSI: {partitions_touched} / {len(NODES)}")
    print(f"Matches found: {len(matches)}")
    print("GSI makes the query targeted instead of a full scan.")


if __name__ == "__main__":
    run_dynamodb_demo()

# Takeaway:
# Model around access patterns; GSIs exist to fix new query needs.
