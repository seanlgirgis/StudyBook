# Consumer Groups - Story Map

## 1. Story (newspaper routes)
A town prints one newspaper. One delivery team splits the neighborhood so each carrier takes a route. Another team delivers the same paper to a different audience and needs the full set too.

## 2. Core Concepts (street version)
- Consumer group = a team that shares the work.
- Partition = a slice of the topic log.
- Ownership = each partition is owned by exactly one consumer within a group.

## 3. Inside One Group (work sharing)
Consumers in the same group do not duplicate work. They split partitions and each reads only the partitions they own.

## 4. Across Different Groups (full stream)
Each group is independent. Two different groups can both read the full stream because each group has its own offsets.

## 5. Why Partitions Exist
Partitions let you scale out consumption. More partitions = more consumers can work in parallel.

## 6. Failure Mode (rebalance)
If a consumer stops, its partitions move to another consumer in the same group so the work keeps going.

## 7. Final Mental Model
A group is a delivery team. Partitions are routes. Inside a group, only one person owns a route. Across groups, everyone can deliver the same paper.

## 8. Run Order
1. c002_consumer_groups_demo.py
