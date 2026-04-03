# Idempotency

## Definition
An operation is idempotent if running it multiple times produces the same final result.

## Why It Matters
Retries are common in pipelines. Idempotency prevents duplicates and inconsistent outcomes.

## Related
- [CDC](./cdc.md)
- [MERGE](../databases/merge.md)
