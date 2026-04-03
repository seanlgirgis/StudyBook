# Possible Micro-Nuggets To Create (Databases)

Current lanes already present:
- `postgresql`
- `mongodb`
- `snowflake`
- `databricks`
- `databricks_bridge`

## Priority Candidates

1. `mysql`
2. `sqlserver`
3. `oracle`
4. `redis_for_de`
5. `elasticsearch_for_de`
6. `clickhouse`
7. `duckdb`
8. `bigquery`
9. `redshift`
10. `cassandra`

## Per-Lane Nugget Menu (Reusable Template)

1. `00_setup/00_prereq_check.py`
2. `00_setup/01_seed_lab.py`
3. `01_core_sql_or_api/01_connection.py`
4. `01_core_sql_or_api/02_crud_or_select.py`
5. `02_modeling_and_schema/01_schema_design.py`
6. `02_modeling_and_schema/02_constraints_or_validation.py`
7. `03_query_patterns/01_joins_or_lookups.py`
8. `03_query_patterns/02_window_or_aggregation.py`
9. `04_de_patterns/01_upsert_merge.py`
10. `04_de_patterns/02_scd_type2_or_history.py`
11. `05_reliability/01_transactions_or_consistency.py`
12. `05_reliability/02_recovery_or_replay.py`
13. `06_performance/01_indexing_or_partitioning.py`
14. `06_performance/02_query_tuning.py`
15. `07_security_and_governance/01_roles_grants.py`
16. `07_security_and_governance/02_masking_or_policies.py`
17. `08_interview_drills/01_interview_drills.py`
18. `09_mini_capstone/01_mini_capstone.py`

## Database-Specific Advanced Ideas

- `postgresql_advanced`: MVCC internals, locks, VACUUM, replication basics.
- `mongodb_advanced`: shard keys, chunk balancing, transaction retry logic.
- `snowflake_advanced`: tasks/streams orchestration, resource monitors, cost governance.
- `databricks_sql_advanced`: warehouse tuning, Photon, Unity Catalog security labs.
- `cdc_patterns`: Debezium + sink merge patterns.
- `data_quality_with_gx`: Great Expectations checks against each engine.
