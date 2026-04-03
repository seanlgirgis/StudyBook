# Databricks Bridge -- Micro-Nuggets

Data Engineering depth with cross-engine transfer from PostgreSQL/Snowflake.
Every nugget is runnable, prints PASS/FAIL, and teaches the **why** behind each concept.

---

## What This Module Covers

| Folder | Topic |
|--------|-------|
| `00_setup/` | Prerequisites, credential check, seed lab data, reset |
| `01_sql_foundations/` | JOINs, GROUP BY/HAVING, subqueries |
| `02_cte_and_windowing/` | CTEs, ROW_NUMBER/RANK/LAG/LEAD, advanced analytics |
| `03_delta_core/` | ACID, schema enforcement, Time Travel, OPTIMIZE/ZORDER |
| `04_de_patterns/` | Deduplication, MERGE, SCD2, incremental loads, late events |
| `05_performance_and_optimization/` | EXPLAIN, partitioning strategy |
| `06_governance_and_security/` | Unity Catalog, GRANT/REVOKE, INFORMATION_SCHEMA |
| `07_data_quality_and_testing/` | Null checks, FK checks, range validation, DQ results |
| `08_interview_drills/` | 10 runnable scenario Q&A |
| `09_mini_capstone/` | Bronze->Silver->Gold + failure simulation + Time Travel recovery |

---

## Prerequisites

1. Python 3.8 or higher
2. `databricks-sql-connector` and `requests` installed
3. Databricks workspace credentials set

---

## Step 1: Navigate to the folder

```powershell
cd D:\StudyBook\tracks\08_databases\micro_nuggets\databricks_bridge
```

---

## Step 2: Install dependencies

```powershell
pip install databricks-sql-connector requests
```

---

## Step 3: Set credentials

**Option A -- Environment variables (simplest):**
```powershell
$env:DATABRICKS_HOST  = "https://dbc-xxxx.cloud.databricks.com"
$env:DATABRICKS_TOKEN = "dapi..."
# Optional -- auto-discovered if omitted:
$env:DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/your-warehouse-id"
```

**Option B -- .env.local file:**
Add to `D:\StudyBook\_infra\env\.env.local` (gitignored):
```
DATABRICKS_HOST=https://dbc-xxxx.cloud.databricks.com
DATABRICKS_TOKEN=dapi...
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
```
Where to find HTTP Path: Databricks UI -> SQL Warehouses -> your warehouse -> Connection Details -> HTTP Path

**Option C -- Encrypted secrets (StudyBook system):**
Already configured if you set up the StudyBook secrets system.

---

## Step 4: Run prerequisite check

```powershell
python 00_setup\00_prereq_check.py
```

Expected output:
```
  [OK]  Python 3.x.x
  [OK]  databricks-sql-connector x.x.x
  [OK]  requests x.x.x
  [OK]  REST probe successful
  [OK]  SQL Warehouse connection successful
  All prerequisites met. Run 01_seed_lab.py next.
```

---

## Step 5: Seed the lab data

```powershell
python 00_setup\01_seed_lab.py
```

This creates the `nugget_lab.bridge_lab` schema and seeds:
- `customers` (20 rows)
- `products` (15 rows)
- `sales_orders` (50 rows)
- `events_stream` (30 rows)

Safe to rerun -- skips tables that already have data.

---

## Step 6: Run a single nugget

```powershell
python 01_sql_foundations\01_joins.py
python 03_delta_core\03_time_travel.py
python 09_mini_capstone\01_mini_capstone.py
```

---

## Step 7: Run all nuggets

```powershell
python run_all_databricks_bridge_nuggets.py
```

Expected output:
```
  PASS  00_setup/00_prereq_check.py                     ...s
  PASS  00_setup/01_seed_lab.py                          ...s
  PASS  01_sql_foundations/01_joins.py                   ...s
  ...
  Total: 22  |  Passed: 22  |  Failed: 0
  All nuggets passed! [OK]
```

---

## Step 8: Reset the lab (optional)

Drops all bridge_lab tables so you can start fresh:

```powershell
python 00_setup\99_reset_lab.py --confirm
```

Then re-seed:
```powershell
python 00_setup\01_seed_lab.py
```

---

## Common Errors and Fixes

### Error: `Missing Databricks credentials`
**Fix:** Set `DATABRICKS_HOST` and `DATABRICKS_TOKEN` environment variables (see Step 3).

### Error: `http_path missing`
**Fix:** Find your SQL Warehouse HTTP Path:
Databricks UI -> SQL Warehouses -> your warehouse -> Connection Details -> HTTP Path.
Set `$env:DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/your-id"`.

### Error: `Connection refused` or `timeout`
**Fix:**
1. Check the warehouse is running (or will auto-resume)
2. First query may take 30-90 seconds to start a stopped warehouse
3. Check `DATABRICKS_HOST` starts with `https://`

### Error: `Table not found` in most nuggets
**Fix:** Run `python 00_setup\01_seed_lab.py` first to create and seed the tables.

### Error: `CATALOG_NOT_FOUND: nugget_lab`
**Fix:** The `nugget_lab` catalog may not be created yet. Run:
```powershell
python 00_setup\01_seed_lab.py
```
This script creates the catalog and schema if they don't exist.

### Error: `PermissionDenied on GRANT`
**Fix:** Some GRANT operations require metastore admin. The nuggets gracefully
degrade when permissions are insufficient -- this is expected behavior, not a bug.

### Error: `DROP COLUMN not supported`
**Fix:** Some Delta runtime versions require column mapping to be enabled before
dropping columns. This is a known constraint. The nugget marks it as non-blocking.

---

## Reference Documents

| File | Contents |
|------|----------|
| `CROSS_ENGINE_SQL_MAP.md` | PostgreSQL -> Databricks SQL -> Snowflake equivalences |
| `DATABRICKS_BRIDGE_GLOSSARY.md` | Plain-English definitions of every term |
| `DATABRICKS_BRIDGE_SPEEDY_STORY_AND_INTERVIEW.md` | Story + 32 interview Q&A |

---

## Target Namespace

All bridge nuggets write to:
```
nugget_lab.bridge_lab.<table_name>
```

This is separate from the baseline `nugget_lab.default` schema used by
`tracks/08_databases/micro_nuggets/databricks/` to prevent conflicts.
