# Database Design Field Guide

## Course status

- Platform: COMPLETE
- StudyBook package: COMPLETE
- Documentation: STRONG
- Lab: DEVELOPING
- Recall: DEVELOPING
- Interview readiness: NEEDS REPETITION

## Chapter guides

1. [Processing, Storing, and Organizing Data](chapter_01_processing_storing_and_organizing_data_field_guide.html)
2. [Database Schemas and Normalization](chapter_02_database_schemas_and_normalization_field_guide.html)
3. [Database Views](chapter_03_database_views_field_guide.html)
4. [Database Management](chapter_04_database_management_field_guide.html)
5. [SQL Quick Lookup](sql_quick_lookup.html)
6. [Lab Run Book](../lab/lab_run_book.md)

## Course big picture

Database design starts with workload and business rules. An operational database runs the current business through frequent, short transactions. An analytical database reorganizes historical data for scans, joins, and aggregation.

A sound design connects:

```text
requirements
→ workload
→ data model and grain
→ integrity and access
→ performance and freshness
→ operations and DBMS choice
```

## Core decision rules

### Operational database

Use an OLTP-oriented design when the system must create and update current records such as orders, payments, inventory, and accounts. Favor strong keys, constraints, normalized entities, concurrency, and predictable short transactions.

### Analytical database

Use an OLAP-oriented design when users need historical analysis and large aggregations. Favor explicit fact grain, dimensions, star/snowflake choices, and potentially materialized summaries.

### Normalize when

- duplicate facts can become inconsistent;
- updates affect shared entities;
- candidate keys and dependencies are clear;
- write correctness matters more than avoiding joins.

### Denormalize when

- repeated joins dominate a read-heavy workload;
- pipelines can keep duplicated values consistent;
- the performance gain is demonstrated, not assumed.

### Views

- Regular view: stored query, current at execution time.
- Materialized view: stored query result, faster reads but requires refresh.
- A view is an interface and possible security boundary, not automatically a performance optimization.

### Partitioning

Partition a very large table when filters and maintenance align with the partition key. Partitioning is not a replacement for indexes or good query design.

## Interview memory

**What is an operational database?**  
A database that supports current day-to-day business transactions. It is usually optimized for many short concurrent reads and writes, low latency, and strong integrity.

**What is the most important fact-table question?**  
“What does one row represent?” That sentence defines the grain and prevents mixed-level measures.

**How do you choose a DBMS?**  
Match workload, consistency, data model, query shape, scale, latency, operations, ecosystem, and team capability; then validate with representative tests.
