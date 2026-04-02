# DynamoDB — Story Map

## 1. Story (mailroom with labeled bins)
A mailroom has bins labeled by recipient. Every envelope with the same label goes to the same bin. If you want one person's mail, it is fast. If you want all mail with a red stamp, every bin must be opened.

## 2. Core Concepts (street version)
- Partition key chooses the bin.
- Sort key orders items inside the bin.
- Access patterns decide the bin labels.

## 3. What DynamoDB is
A key-value / document-style distributed store built for predictable access patterns at massive scale.

## 4. Partition key and sort key
Partition key routes items to a partition. Sort key orders items within that partition for range reads.

## 5. Why access patterns come first
You model data around the questions you will ask. If the pattern is not modeled, you pay with scans or extra indexes.

## 6. What GSIs are (simple intuition only)
Global Secondary Indexes are extra lookup tables that let you query by a different key.

## 7. What DynamoDB is great at
- Low-latency point reads
- Predictable, partition-based queries
- Automatic scaling and high availability

## 8. What DynamoDB is bad at
- Ad-hoc queries across many partitions
- Joins and multi-table analytics

## 9. Hot partition warning
If one partition key gets too much traffic, it becomes a hotspot and throttles performance.

## 10. Final mental model
Bins in a mailroom. Pick the right label, and it is instant. Pick the wrong question, and you open every bin.

## 11. Run Order
1. c083_dynamodb_demo.py
