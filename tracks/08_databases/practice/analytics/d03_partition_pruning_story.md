# Partition Pruning — Story Map

## 1. Story
You store receipts by month in labeled boxes. A request comes in for March. You should not open every box if the label already tells you which box matters.

## 2. Core Concepts (street version)
- Partitioning = split one big table into labeled chunks.
- Pruning = skip whole chunks before reading any rows.

## 3. What Partition Pruning Is
The engine looks at your filter, matches it to the partition labels, and simply never opens the irrelevant partitions.

## 4. Why It Matters For Analytics
Analytics scans lots of data. If you can skip 5 out of 6 months, you read less, pay less, and finish faster.

## 5. When Pruning Works
- Your query filters directly on the partition key.
- Example: `ts >= '2024-03-01' AND ts < '2024-04-01'`.

## 6. When Pruning Fails
- You do not filter on the partition key at all.
- You hide the key behind a function or expression that blocks pruning.
- Result: the engine has to open every partition.

## 7. Final Mental Model
Partitioning = put labels on boxes.
Pruning = read the label and walk past most boxes.

## 8. Run Order
1. c062_partition_pruning_demo.py
