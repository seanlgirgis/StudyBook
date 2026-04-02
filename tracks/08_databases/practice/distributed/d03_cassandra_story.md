# Cassandra — Story Map

## 1. Story (many service desks handling customer folders)
A company has many service desks. Each customer folder is assigned to one desk, and a couple of backup desks keep copies. If you ask about a single customer, the right desk can answer fast. If you ask for "all folders with a red stamp," every desk has to rummage.

## 2. Core Concepts (street version)
- Partition key chooses the desk.
- Clustering key orders papers inside that desk.
- Replicas are backup desks with the same folder.

## 3. What Cassandra is
A distributed-first database that spreads writes across nodes and stays available while scaling horizontally.

## 4. Why people use Cassandra
It absorbs huge write volume, stays up during failures, and scales by adding nodes.

## 5. Partition key and clustering key
Partition key routes data to a node. Clustering key sorts rows inside that partition for fast reads by order.

## 6. Replication + consistency levels (simple intuition)
Data is copied to multiple nodes. Reads can ask for ONE (fast) or QUORUM (safer) replicas to answer.

## 7. What Cassandra is great at
- High write throughput
- Always-on availability
- Predictable, partition-based reads

## 8. What Cassandra is bad at
- Ad-hoc queries across many partitions
- Joins and global aggregations without pre-modeling

## 9. Final mental model
Folders live at desks. The folder label (partition key) decides where it goes. Inside the folder, papers are sorted by time. Ask the right desk, and it is fast. Ask every desk, and it is painful.

## 10. Run Order
1. c082_cassandra_demo.py
