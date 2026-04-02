All 10 nuggets are written. Here's a full summary of what was created:

---

### Files created under `D:\StudyBook\tracks\08_databases\micro_nuggets\snowflake\`

```
_sf_connect.py                   ← shared connection helper (all nuggets import this)

00_setup/
  00_prereq_check.py             ← Python version, packages, credentials, live ping
  01_connection.py               ← minimal open/query/close pattern + CURRENT_* functions
  02_session_context.py          ← USE commands, SHOW WAREHOUSES, SHOW SCHEMAS
  99_reset_lab.py                ← drop all NUGGET_* objects; supports --dry-run

02_ddl_basics/
  01_create_db_schema.py         ← CREATE SCHEMA, INFORMATION_SCHEMA.SCHEMATA
  02_create_table.py             ← all major types: NUMBER, FLOAT, VARCHAR, BOOLEAN,
                                    DATE, TIMESTAMP_NTZ, VARIANT, AUTOINCREMENT,
                                    PERMANENT vs TRANSIENT tables
  03_clone_table.py              ← zero-copy clone, copy-on-write, storage metrics

03_dml_basics/
  01_insert_select.py            ← INSERT VALUES, INSERT INTO … SELECT,
                                    GENERATOR, UNIFORM, SEQ4, DATEADD
  02_merge.py                    ← full MERGE upsert + return counts, CDC pattern
  03_update_delete.py            ← simple + join-based UPDATE/DELETE,
                                    Time Travel audit after DML
```

### What's embedded in every file
- **Concept explanations** — the *why*, not just the *what*
- **Expected output** — exact sample output in the docstring so you can study without running
- **DE context** — how each feature is used in real pipelines
- **Common pitfalls** — e.g. missing WHERE in DELETE, FLOAT vs NUMBER for money
- **Cross-references** — "covered in depth in nugget 06" links the curriculum together
08_mini_capstone/
  01_stage_json_ingest.py        ← land local JSON into Snowflake stage
  02_copy_into_raw_variant.py    ← COPY INTO raw table (VARIANT payload)
  03_transform_curated_merge.py  ← MERGE into curated table
  04_stream_task_incremental.py  ← stream + task incremental wiring
  05_time_travel_recovery_demo.py← recovery demo with Time Travel/UNDROP
