# PostgreSQL Micro-Nuggets

Quick, focused, runnable lessons on PostgreSQL for Data Engineering and interview prep.

Each nugget is a standalone Python script that:
- **Teaches one concept** with inline comments
- **Runs end-to-end** — no setup beyond prerequisites
- **Prints expected output** in the docstring so you can study without running
- **Builds on previous nuggets** — run them in order

---

## Structure

```
postgresql/
│
├── _pg_connect.py                      ← shared connection helper
├── run_all_postgresql_nuggets.py       ← one-command validation runner
│
├── 00_setup/
│   ├── 00_prereq_check.py              ← Python, psycopg2, credentials, live ping
│   └── 01_seed_lab.py                  ← Create tables, indexes, seed data (idempotent)
│
├── 01_sql_core/
│   ├── 01_joins.py                     ← INNER, LEFT, RIGHT, FULL OUTER, CROSS
│   ├── 02_aggregation.py               ← GROUP BY, HAVING, ROLLUP, CUBE, GROUPING SETS
│   └── 03_subqueries.py                ← Correlated, EXISTS, IN, ANY, ALL
│
├── 02_cte_and_windowing/
│   ├── 01_ctes.py                      ← Non-recursive + recursive CTEs, funnel analysis
│   ├── 02_window_functions.py          ← ROW_NUMBER, RANK, LAG/LEAD, running totals
│   └── 03_advanced_analytics.py        ← Cohort analysis, sessionization, top-N, YoY
│
├── 03_data_modeling/
│   ├── 01_keys_and_constraints.py      ← PK, FK, UNIQUE, CHECK, constraint violations
│   └── 02_normalization.py             ← 3NF vs denormalized, materialized views
│
├── 04_de_patterns/
│   └── 01_de_patterns.py               ← Dedup, upsert (ON CONFLICT), SCD Type 2
│
├── 05_performance_tuning/
│   └── 01_explain_and_indexes.py       ← EXPLAIN ANALYZE, B-tree, composite, anti-patterns
│
├── 06_transactions_and_concurrency/
│   └── 01_transactions.py              ← ACID, isolation levels, deadlock prevention
│
├── 07_data_quality_and_testing/
│   └── 01_data_quality.py              ← Nulls, duplicates, FK integrity, validity checks
│
├── 08_interview_drills/
│   └── 01_interview_drills.py          ← Second-highest, top-N, MoM growth, duplicates
│
└── 09_mini_capstone/
    └── 01_mini_capstone.py             ← Bronze→Silver→Gold pipeline with JSONB ingestion
```

---

## Prerequisites

1. **PostgreSQL running** (Docker recommended):
   ```powershell
   cd D:\StudyBook
   .\_infra\scripts\infra_up.ps1
   ```

2. **Python packages:**
   ```bash
   pip install psycopg2-binary
   ```

3. **Credentials** in `_infra/env/.env.local`:
   ```
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=de_admin
   POSTGRES_PASSWORD=DeAdmin2026!
   POSTGRES_DB=de_telemetry
   ```

---

## Running Order

```powershell
cd D:\StudyBook\tracks\08_databases\micro_nuggets\postgresql

# 1. Check prerequisites
python 00_setup/00_prereq_check.py

# 2. Seed lab environment (idempotent — safe to re-run)
python 00_setup/01_seed_lab.py

# 3. Run all nuggets
python run_all_postgresql_nuggets.py

# Or run individually:
python 01_sql_core/01_joins.py
python 02_cte_and_windowing/01_ctes.py
# ... etc
```

---

## Reset Lab

```powershell
# Drop everything and recreate from scratch
python 00_setup/01_seed_lab.py --reset
```

---

## Key Concepts Covered

| Module | Concepts | Interview Relevance |
|--------|----------|---------------------|
| SQL Core | Joins, aggregation, subqueries | ★★★★★ |
| CTEs & Windows | CTEs, ROW_NUMBER, LAG/LEAD, running totals | ★★★★★ |
| Data Modeling | PK/FK, constraints, normalization, mat. views | ★★★★ |
| DE Patterns | Dedup, upsert, SCD Type 2, incremental loads | ★★★★★ |
| Performance | EXPLAIN, indexes, anti-patterns | ★★★★ |
| Transactions | ACID, isolation levels, deadlocks | ★★★★ |
| Data Quality | Null checks, FK integrity, validity tests | ★★★ |
| Interview Drills | Second-highest, top-N, MoM growth | ★★★★★ |
| Capstone | Bronze→Silver→Gold, JSONB parsing | ★★★★ |

---

## PostgreSQL vs Other Databases

| Feature | PostgreSQL | MySQL | SQL Server | Snowflake |
|---------|-----------|-------|------------|-----------|
| **Upsert** | ON CONFLICT DO UPDATE | INSERT ... ON DUPLICATE KEY | MERGE | MERGE |
| **Window Functions** | Full support | 8.0+ | Full support | Full support |
| **Recursive CTEs** | WITH RECURSIVE | 8.0+ | Yes | Yes |
| **JSON** | JSONB (indexed) | JSON | JSON | VARIANT |
| **Materialized Views** | Yes (manual refresh) | No | Indexed views | Automatic |
| **Isolation Levels** | Read Committed, Repeatable Read, Serializable | Same | Same + Snapshot | Snapshot |
| **EXPLAIN** | EXPLAIN ANALYZE | EXPLAIN | Execution Plan | Query Profile |

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `connection refused` | PostgreSQL not running | `.\_infra\scripts\infra_up.ps1` |
| `password authentication failed` | Wrong password in .env.local | Check `_infra/env/.env.local` |
| `schema "pg_lab" does not exist` | Lab not seeded | `python 00_setup/01_seed_lab.py` |
| `relation does not exist` | Tables not created | Run seed script first |
| `deadlock detected` | Concurrent conflicting locks | Lock resources in consistent order |

---

Last updated: 2026-04-02
