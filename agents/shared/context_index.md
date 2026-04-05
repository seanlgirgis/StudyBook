# Context Index

Purpose: compact durable memory map for fast session bootstrap.

## Project North Star

- Build `D:\StudyBook` as the canonical, reproducible DE/AI runtime repo.
- Execute migration as controlled shift/lift from `D:\Workspace`.
- Keep autonomy high with explicit safety guardrails and durable run artifacts.

## Canonical Control Files

- `AGENTS.md`
- `CONTROL_PROTOCOL.md`
- `agents/shared/pending_task.md`
- `agents/shared/agent_status.md`
- `agents/shared/task_register.md`
- `agents/shared/open_loops.md`
- `agents/shared/decision_log.md`
- `agents/shared/parking_lot.md`
- `agents/shared/approval_matrix.md`
- `agents/shared/command_allowlist.md`
- `agents/shared/user_profile.md` ← **User context & working style**
- `docs/adr/ADR-INDEX.md`

## Current Working Agreements

- Use `Allowed Scope: bounded` by default for velocity.
- Use `Reasoning Depth: deep` for migration and architecture decisions.
- Stop only for high-risk ambiguity, not for routine implementation details.
- Canonical runtime target is `D:\StudyBook` (deprecated path deleted).
- Standing owner directive (2026-04-02): treat encrypted StudyBook secrets as system of record for sensitive values; use seed-backed secret updates by default and avoid storing sensitive values in tracked files/chat.
- **Seed-backed secrets (2026-04-02): Passphrase entered ONCE per machine during seed registration. NEVER ask user for passphrase again - env_setter.ps1 auto-loads from DPAPI-encrypted seed file.**
- **Job-site credential canon (2026-04-04): use `JOBSITE_<SITEKEY>_{URL,USER,PASSWORD}` keys via `agents/skills/jobsite-login-secrets` scripts; avoid ad-hoc keys like `SAPSF_*` to prevent retrieval mismatches.**

## Portable Environment Files

- `env_setter.ps1`
- `scripts/env/env_core.ps1`
- `scripts/env/bootstrap_all.ps1`
- `scripts/env/register_secret_seed.ps1`
- `scripts/env/remove_secret_seed.ps1`
- `scripts/env/package_aws_credentials.ps1`
- `scripts/env/restore_aws_credentials.ps1`
- `config/env/base.psd1`
- `config/machines/asuspc.psd1`
- `config/machines/dell-laptop.psd1`
- `docs/PORTABLE_ENV.md`
- `config/secrets/shared.secrets.enc.json`
- `config/secrets/asuspc.secrets.enc.json`
- `config/secrets/dell-laptop.secrets.enc.json`
- `config/secrets/workspace-import.sources.md`
- `docs/operations/secrets_workflow.md`
- `docs/operations/aws_credentials_workflow.md`

## Infra Reproducibility Files

- `_infra/docker/docker-compose.yml`
- `_infra/docker/core.yml`
- `_infra/docker/streaming.yml`
- `_infra/docker/pipeline.yml`
- `_infra/docker/observability.yml`
- `_infra/env/.env.example`
- `_infra/scripts/infra_up.ps1`
- `_infra/scripts/infra_down.ps1`
- `_infra/scripts/infra_seed.ps1`
- `_infra/scripts/infra_health.ps1`
- `_infra/seeds/seed_core.py`
- `_infra/seeds/seed_tech_telemetry.py`
- `_infra/README.md`

## ZeroToHero Program Files

- `docs/programs/zero_to_hero/EXECUTION_SYSTEM.md`
- `docs/programs/zero_to_hero/MIGRATION_BOARD.md`
- `docs/programs/zero_to_hero/TALKS_WITH_CLAUDE_EXTRACT_AND_SHIFT_LIFT_PLAN.md`
- `docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md`

## Coding Challenges Migration Memory

- M-002/M-002b completed on 2026-04-02 via:
  - `scripts/migration/run_m002_coding_assets.ps1 -Execute -DeleteSource`
- Canonical coding root:
  - `D:\StudyBook\coding_challenges`
- Migration evidence run:
  - `D:\StudyBook\coding_challenges\_migration_meta\run_20260402_113935`
- Emergency rollback snapshot:
  - `C:\Users\shareuser\migration_backups\m002_backup_20260402_113935`
- Authoritative runbook:
  - `docs/programs/zero_to_hero/CODING_ASSETS_MIGRATION_SOLUTION.md`
- First planning outputs for study execution:
  - `coding_challenges/STUDY_MANUAL_V1.md`
  - `coding_challenges/ROADMAP_DRAFT_V1.md`

## Technologies + Interview + ML_AI Migration Memory

- Combined wave completed on 2026-04-02 via:
  - `scripts/migration/run_m011_m013_m008_mlai.ps1 -Execute -DeleteMlAiSource`
- Evidence run:
  - `D:\StudyBook\temp\migration_meta\run_20260402_121903`
- Coverage:
  - `M-011` Technologies notebooks (`54`)
  - `M-013` Technologies prompts R1/R2/R3 (`88`)
  - `M-008` DE interview notebooks (`21`)
  - `M-015` ML_AI pack files (`26`), source deleted
- Safety gates:
  - `secret_hits=0`
  - conflict-safe duplicates captured in `conflicts_report.md` (`__dupNNN` suffixing)
- Backup snapshot for ML_AI cutover:
  - `C:\Users\shareuser\migration_backups\ml_ai_backup_20260402_121903`
- Source decommission evidence for Technologies + DE interview migrated items:
  - `D:\StudyBook\temp\migration_meta\run_20260402_121903\delete_tech_deinterview_report.json`

## Snowflake Micro-Nuggets Memory

- Canonical lane created under:
  - `D:\StudyBook\tracks\08_databases\micro_nuggets\snowflake`
- Current scaffold status (2026-04-02):
  - dirs: `00_setup`, `02_ddl_basics`, `03_dml_basics`
  - files: `_sf_connect.py`, `summary.md` + 9 nugget scripts
- Intent: short 5-10 minute runnable learning nuggets with documentation-first style.

## Databricks Micro-Nuggets Memory

- Canonical lane created under:
  - `D:\StudyBook\tracks\08_databases\micro_nuggets\databricks`
- Current scaffold status (2026-04-02):
  - dirs: `00_setup`, `01_workspace_and_catalog`, `02_tables_and_delta`, `03_queries_and_optimization`, `04_mini_capstone`
  - files: `_db_connect.py`, `summary.md`, `DATABRICKS_SPEEDY_STORY_AND_INTERVIEW.md` + 9 nugget scripts
- Nuggets created:
  - `00_setup/00_prereq_check.py` — environment validation
  - `00_setup/01_connection.py` — minimal connection pattern
  - `00_setup/02_session_context.py` — USE CATALOG, SHOW SCHEMAS
  - `01_workspace_and_catalog/01_create_catalog_schema.py` — CREATE CATALOG/SCHEMA
  - `02_tables_and_delta/01_create_table.py` — Delta Lake tables, types
  - `02_tables_and_delta/02_insert_select.py` — INSERT, SELECT, JOINs, aggregations
  - `02_tables_and_delta/03_merge.py` — MERGE upsert, CDC, SCD Type 2
  - `03_queries_and_optimization/01_time_travel.py` — VERSION AS OF, RESTORE, VACUUM
  - `03_queries_and_optimization/02_optimize.py` — OPTIMIZE, Z-ORDER, data skipping
  - `04_mini_capstone/01_mini_capstone.py` — Bronze→Silver→Gold end-to-end pipeline
- Connection proof: `D:\StudyBook\poc\connection_proofs\python\databricks_connection_proof.py`
- Intent: short 5-10 minute runnable learning nuggets with inline teaching comments.
- Depth: covers MERGE/CDC, Time Travel, OPTIMIZE/Z-ORDER, three-layer pipeline pattern.

## PostgreSQL Micro-Nuggets Memory

- Canonical lane created under:
  - `D:\StudyBook\tracks\08_databases\micro_nuggets\postgresql`
- Full validation: **16/16 PASS** (2026-04-02)
- Structure:
  - `_pg_connect.py` — shared connection helper (reuses existing Docker PostgreSQL creds)
  - `00_setup/` — prereq check + idempotent seed (10 tables, 500+ rows)
  - `01_sql_core/` — joins, aggregation, subqueries
  - `02_cte_and_windowing/` — CTEs, window functions, advanced analytics
  - `03_data_modeling/` — keys/constraints, normalization vs denormalization
  - `04_de_patterns/` — dedup, upsert (ON CONFLICT), SCD Type 2
  - `05_performance_tuning/` — EXPLAIN ANALYZE, indexes, anti-patterns
  - `06_transactions_and_concurrency/` — ACID, isolation levels, deadlocks
  - `07_data_quality_and_testing/` — 10 data quality assertions
  - `08_interview_drills/` — second-highest, top-N, MoM growth, duplicates
  - `09_mini_capstone/` — Bronze→Silver→Gold with JSONB ingestion
  - `run_all_postgresql_nuggets.py` — one-command validation runner
  - `POSTGRESQL_SPEEDY_STORY_AND_INTERVIEW.md` — 8 deep interview Q&As
  - `POSTGRESQL_GLOSSARY.md` — 40+ term definitions with cross-links
  - `README.md` — beginner execution guide
- Credential source: reuses existing `_infra/env/.env.local` (POSTGRES_USER/PASSWORD/DB/PORT)
- Lab schema: `de_lab` (created idempotently by seed script)


## MongoDB Micro-Nuggets Memory

- Canonical lane validated under:
  - `D:\StudyBook\tracks\08_databases\micro_nuggets\mongodb`
- Coverage review recorded:
  - `tracks/08_databases/micro_nuggets/mongodb/MONGODB_COVERAGE_REVIEW.md`
- Verified on 2026-04-03:
  - script inventory (excluding `__pycache__`): `28` (`26` runnable nuggets + helper + lane runner)
  - topology display fix in `00_setup/02_session_context.py` (`_TOPO_NAMES` mapping)
  - Atlas Search zero-result guidance fix in `07_operations/02_atlas_search.py`
  - lane runner added: `run_all_mongodb_nuggets.py` (one-line PASS/FAIL per nugget + summary)
- Known expected limitation:
  - Atlas Search requires `default` search index on `nugget_lab.search_demo` in Atlas UI.
## Last Updated

- 2026-04-04



