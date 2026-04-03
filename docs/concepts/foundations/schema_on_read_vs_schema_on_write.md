# Schema-on-Read vs Schema-on-Write

## Definition
Schema-on-write validates structure before storing data. Schema-on-read applies structure when querying data.

## Why It Matters
Bronze layers often lean schema-on-read; curated layers move to schema-on-write for reliability.

## Related
- [Medallion Architecture](../databases/medallion_architecture.md)
- [CDC](./cdc.md)
