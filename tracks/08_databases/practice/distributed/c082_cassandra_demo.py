# Story:
# Cassandra routes rows by partition key and sorts them by clustering key.
# This demo shows good (single-partition) queries vs bad (cross-partition) queries.

import hashlib
import bisect


NODES = ["node-a", "node-b", "node-c", "node-d"]
REPLICATION_FACTOR = 2


def _hash_key(key):
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()
    return int(digest, 16)


class Node:
    def __init__(self, name):
        self.name = name
        self.partitions = {}

    def insert_row(self, partition_key, row, clustering_key):
        rows = self.partitions.setdefault(partition_key, [])
        positions = [existing[clustering_key] for existing in rows]
        idx = bisect.bisect_left(positions, row[clustering_key])
        rows.insert(idx, row)

    def read_partition(self, partition_key):
        return list(self.partitions.get(partition_key, []))

    def scan_by_event_type(self, event_type):
        matches = []
        partitions_scanned = 0
        for partition_key, rows in self.partitions.items():
            partitions_scanned += 1
            for row in rows:
                if row["event_type"] == event_type:
                    matches.append(row)
        return matches, partitions_scanned


class Cluster:
    def __init__(self, node_names, replication_factor):
        self.nodes = [Node(name) for name in node_names]
        self.rf = replication_factor

    def _owners(self, partition_key):
        start = _hash_key(partition_key) % len(self.nodes)
        owners = []
        for offset in range(self.rf):
            owners.append(self.nodes[(start + offset) % len(self.nodes)])
        return owners

    def write(self, row):
        partition_key = row["customer_id"]
        owners = self._owners(partition_key)
        for owner in owners:
            owner.insert_row(partition_key, row, "event_ts")
        return owners

    def read_partition(self, partition_key):
        owners = self._owners(partition_key)
        primary = owners[0]
        return owners, primary.read_partition(partition_key)

    def query_by_event_type(self, event_type):
        matches = []
        nodes_touched = 0
        partitions_scanned = 0
        for node in self.nodes:
            node_matches, scanned = node.scan_by_event_type(event_type)
            if scanned > 0:
                nodes_touched += 1
            partitions_scanned += scanned
            matches.extend(node_matches)
        return matches, nodes_touched, partitions_scanned


def _print_rows(label, rows):
    print(label)
    for row in rows:
        print(f"  {row['customer_id']} | {row['event_ts']} | {row['event_type']} | {row['payload']}")


def run_cassandra_demo():
    cluster = Cluster(NODES, REPLICATION_FACTOR)

    print("=" * 72)
    print("Cluster nodes:", ", ".join(NODES))
    print(f"Replication factor: {REPLICATION_FACTOR}")

    rows = [
        {"customer_id": "cust-1", "event_ts": 3, "event_type": "view", "payload": "item-3"},
        {"customer_id": "cust-2", "event_ts": 1, "event_type": "purchase", "payload": "item-9"},
        {"customer_id": "cust-1", "event_ts": 1, "event_type": "signup", "payload": "email"},
        {"customer_id": "cust-3", "event_ts": 2, "event_type": "refund", "payload": "order-7"},
        {"customer_id": "cust-1", "event_ts": 2, "event_type": "view", "payload": "item-1"},
        {"customer_id": "cust-2", "event_ts": 2, "event_type": "refund", "payload": "order-2"},
    ]

    print("=" * 72)
    print("Writing rows (partition key = customer_id, clustering = event_ts)")
    sample_key = "cust-1"
    owners = cluster._owners(sample_key)
    print(f"Partition owners for {sample_key}: {', '.join(node.name for node in owners)}")
    owners_again = cluster._owners(sample_key)
    print(f"Same key routes consistently: {', '.join(node.name for node in owners_again)}")

    for row in rows:
        cluster.write(row)

    print("=" * 72)
    print("Scenario A: Good query (single partition)")
    owners, partition_rows = cluster.read_partition("cust-1")
    print("Primary owner:", owners[0].name)
    print("Replicas:", ", ".join(node.name for node in owners))
    _print_rows("Ordered rows for cust-1:", partition_rows)

    print("=" * 72)
    print("Scenario B: Bad query (cross-partition)")
    matches, nodes_touched, partitions_scanned = cluster.query_by_event_type("refund")
    print(f"Event type search: refund")
    print(f"Nodes touched: {nodes_touched} / {len(NODES)}")
    print(f"Partitions scanned: {partitions_scanned}")
    print(f"Matches found: {len(matches)}")
    print("Warning: This pattern scans many partitions and does not fit Cassandra well.")


if __name__ == "__main__":
    run_cassandra_demo()

# Takeaway:
# Model queries around the partition key; cross-partition scans are expensive.
