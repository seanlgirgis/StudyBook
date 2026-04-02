# Distributed Partitioning — Story Map

## 1. Story (warehouse with multiple rooms / bins)
One warehouse room cannot hold every box. So you split into rooms and label which room holds which boxes.

## 2. Core Concepts (street version)
- Partitioning = split rows across buckets.
- Router = rule that picks the bucket.
- Key decides the destination.

## 3. What Partitioning Is
A horizontal split of one dataset across multiple shards.

## 4. Why Distributed Systems Partition Data
Storage and traffic scale by spreading the load across machines.

## 5. Good Routing vs Bad Routing
Good routing spreads keys evenly and lets you hit one shard per key.
Bad routing piles many keys onto one shard.

## 6. What Skew / Hot Partitions Mean
One shard gets hammered while others sit idle. That shard becomes the bottleneck.

## 7. What Partitioning Does NOT Solve
It does not remove coordination, joins, or cross-shard complexity.

## 8. Final Mental Model
Many rooms, one label rule. If the rule is bad, one room burns.

## 9. Run Order
1. c080_partitioning_demo.py
