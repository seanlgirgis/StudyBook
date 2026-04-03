# OPTIMIZE and Compaction

## Definition
Compaction rewrites many small files into fewer larger files. OPTIMIZE is the common Delta command for this.

## Why It Matters
It improves scan efficiency, lowers latency, and stabilizes performance over time.

## Related
- [Small Files Problem](./small_files_problem.md)
- [Z-ORDER](./z_order.md)
