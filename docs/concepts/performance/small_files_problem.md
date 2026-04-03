# Small Files Problem

## Definition
Frequent small writes create many tiny files, increasing metadata overhead and scan inefficiency.

## Why It Matters
Query latency rises and compute cost increases due to file-open overhead.

## Related
- [OPTIMIZE and Compaction](./optimize_and_compaction.md)
- [Z-ORDER](./z_order.md)
