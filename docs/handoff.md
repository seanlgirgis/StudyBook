# StudyBook — Comprehensive Handoff

**Path:** `D:\Workarea\StudyBook`
**Status:** Active canonical runtime — primary DE/AI study, POC, and research hub
**Venv:** `C:\py_venv\proj_educate`
**Last reviewed:** 2026-04-27

---

## 1. What This Repository Is

StudyBook is Sean's canonical Data Engineering and AI learning runtime. It serves as:

- **Study environment** — coding challenges (166+), LeetCode practice, interview prep guides
- **Tutorial lab** — 47 runnable tutorials across AWS, PySpark, Airflow, Docker, databases, streaming
- **Research/POC workspace** — connection proofs for all cloud platforms and Docker services
- **Micro-nuggets library** — short 5–10 min runnable learning modules (PostgreSQL 16/16 pass, Databricks, Snowflake, MongoDB)
- **Agent-driven runtime** — full autonomous agent protocol with durable memory, approval matrix, and task register
- **Migration target** — controlled shift/lift from legacy `D:\Workspace` into standardized tracks

Sibling repos (separate git histories, managed together):
- `D:\Workarea\jobsearch` — job search pipeline
- `D:\Workarea\seanlgirgis.github.io` — public portfolio site

---

## 2. Quick Start

### Every session — run first
```powershell
cd D:\Workarea\StudyBook
.\env_setter.ps1 -NonInteractive        # preferred for agent/scripted runs
# or
.\env_setter.ps1                        # interactive fallback (prompts passphrase if seed missing)
```

### Orient yourself
```powershell
Get-Content .\agents\shared\context_index.md -TotalCount 200
Get-Content .\agents\shared\open_loops.md -TotalCount 100
```

### New machine setup (first time only)
```powershell
.\scripts\env\bootstrap_all.ps1         # guided full setup
# then register seed so passphrase never needs typing again:
$env:STUDYBOOK_SECRET_PASSPHRASE = "<your-passphrase>"
.\scripts\env\register_secret_seed.ps1 -NonInteractive -Force
```

---

## 3. Environment Architecture

### env_setter.ps1 — what it does
`env_setter.ps1` is not a simple activate script. It:
1. Forces **Microsoft JDK 17** onto PATH (strips Oracle Java 8 shim paths that hijack `java.exe`) — critical for PySpark
2. Delegates to `scripts/env/env_core.ps1` → `Invoke-StudyBookEnvBootstrap`
3. Detects machine (`COMPUTERNAME` or `STUDYBOOK_MACHINE` override)
4. Loads `config/env/base.psd1` + `config/machines/<machine>.psd1`
5. Activates venv at path from merged config (`C:\py_venv\proj_educate`)
6. Resolves secret passphrase (order: env var → DPAPI seed file → interactive prompt)
7. Decrypts `config/secrets/*.enc.json` → exports to process env vars
8. Adds `scripts/` to PATH

### Machine profiles
| Machine | Profile file |
|---------|-------------|
| ASUS PC | `config/machines/asuspc.psd1` |
| Dell laptop | `config/machines/dell-laptop.psd1` |
| New machine | run `.\scripts\env\init_machine_profile.ps1` |

### Secrets system (DPAPI-encrypted)
All secrets live in `config/secrets/*.enc.json` — encrypted, committed to git. Plaintext never committed.

| Task | Command |
|------|---------|
| Update a secret | `.\scripts\env\set_secret.ps1 -Machine asuspc -Entry "KEY=VALUE"` |
| Update sensitive secret (masked) | `.\scripts\env\set_secret.ps1 -Machine asuspc -PromptSecretKey "TOKEN"` |
| Register seed (one-time) | `$env:STUDYBOOK_SECRET_PASSPHRASE="..."; .\scripts\env\register_secret_seed.ps1 -NonInteractive -Force` |
| Remove seed | `.\scripts\env\remove_secret_seed.ps1 -Force` |
| Full setup | `.\scripts\env\bootstrap_all.ps1` |
| OpenAI local fallback | `.\scripts\env\set_openai_key_local.ps1` |

Seed file: `config/secrets/.local/studybook.secret.seed.dpapi.json` — gitignored, machine/user-bound, not portable.

> **Important:** DPAPI seed is `CurrentUser`-scoped. If you switch Windows users or run elevated, seed decrypt may fail. Use the OpenAI local fallback in that case.

---

## 4. Repository Scale (as of 2026-04-26)

| Area | Files | Dirs |
|------|-------|------|
| `coding_challenges/` | ~908 | ~251 |
| `data/` | ~877 | ~350 |
| `tracks/` | ~665 | ~203 |
| `playground/` | ~214 | ~5 |
| `docs/` | ~112 | ~14 |
| `tutorials/` | ~150 | ~42 |

---

## 5. Working Areas

### 5A. Coding Challenges (`coding_challenges/`)
166+ Jupyter notebooks (0001–0166+) covering arrays, sliding window, two pointers, linked lists, trees, graphs, dynamic programming, monotonic stacks, heaps, and more.

**Index system (CSV-first):**
| Command | Purpose |
|---------|---------|
| `.\refresh_index_and_push.ps1` | Refresh `index.csv` → git workflow |
| `.\search_index.ps1 <needle> [-Limit n]` | Search index by keyword/number |
| `.\index_cli.ps1 <add\|update\|delete\|find\|show\|open> ...` | Full CRUD on index |
| `.\run_index_ui.ps1` | Local Streamlit UI on `localhost:8501` |
| `.\run_index_ui_docker.ps1 -Action up\|down\|logs\|restart` | Dockerized Streamlit UI |

Key files: `coding_challenges/index.csv`, `STUDY_MANUAL_V1.md`, `ROADMAP_DRAFT_V1.md`

**Assessment / interview training:**
- `coding_challenges/_assessment_training/` — mock assessment harnesses (Two Sum, Valid Parentheses, 347, LIS, MinStack, etc.)
- `coding_challenges/leetcode/` — organized LeetCode solutions
- `coding_challenges/guides/` — study guides with anchor navigation

### 5B. Tracks (`tracks/`)
Canonical learning tracks by domain:

| Track | Domain |
|-------|--------|
| `07_cloud/` | AWS cloud fundamentals |
| `08_databases/` | Databases (with micro-nuggets) |
| `10_streaming/` | Streaming (Kafka, Kinesis) |
| `11_batch_processing/` | Batch (Spark, Glue) |
| `12_orchestration/` | Orchestration (Airflow, Step Functions) |
| `22_ml_platform/` | ML platforms (SageMaker, Databricks) |
| `29_observability/` | Observability (CloudWatch, OpenSearch) |
| `30_system_design/` | System design patterns |

**Micro-nuggets** (`tracks/08_databases/micro_nuggets/`) — 5–10 min runnable modules:

| Lane | Status | Notes |
|------|--------|-------|
| `postgresql/` | ✅ 16/16 PASS | Full lane: core SQL → CTEs → modeling → DE patterns → performance → transactions → data quality → interview drills → capstone |
| `databricks/` | ✅ validated | MERGE/CDC, Time Travel, OPTIMIZE/Z-ORDER, Bronze→Silver→Gold pipeline |
| `snowflake/` | ✅ validated | DDL basics, DML basics, connection setup |
| `mongodb/` | ✅ 26 nuggets | Atlas Search requires manual index creation in Atlas UI |

### 5C. Tutorials (`tutorials/`)
47 deep-dive tutorial folders. Each has runnable scripts, Docker where needed, and a `prompt_READY_TO_PASTE.md` for AI context loading.

**Active / recently worked:**

| Tutorial | Status |
|----------|--------|
| `02_PySpark_Docker/` | Active — Docker Spark cluster lessons 1–7 validated |
| `03_apache_airflow_docker/` | Active — Airflow Docker zero-to-hero pack, DAG basics, XComs |
| `06_aws_emr/` | Active — EMR Serverless capstone (LOOP-161 open: capstone support files pending) |
| `16_aws_iam/` | Active — STS, permission boundaries, IAM tutorials |
| `36_docker/` | Active — Docker teaching pack bundle 01 |

> **Note:** `02_PySpark_Docker/` and `02_pyspark/` both exist. They are different content: `02_PySpark_Docker` is the Docker cluster lab; `02_pyspark` is local PySpark. The duplicate prefix is known — see pruning doc.

Full list: `01_aws_kinesis`, `02_PySpark_Docker`, `02_pyspark`, `03_apache_airflow_docker`, `04_aws_step_functions`, `05_delta_lake`, `06_aws_emr`, `07_aws_glue`, `08_aws_s3`, `09_aws_cloudwatch`, `10_python_logging`, `11_dbt`, `12_parquet`, `13_python_concurrency`, `14_encryption`, `15_data_anonymization_pii`, `16_aws_iam`, `17_postgresql`, `18_sql_patterns`, `19_python_testing`, `20_pydantic`, `21_aws_redshift`, `22_aws_athena`, `23_sqlalchemy`, `24_pandas`, `25_numpy`, `26_polars`, `27_duckdb`, `28_data_stubbing`, `29_streamlit`, `30_fastapi`, `31_aws_lambda`, `32_aws_dynamodb`, `33_aws_msk_kafka`, `34_aws_bedrock`, `35_terraform`, `36_docker`, `37_cicd`, `38_aws_ecs`, `39_aws_cloudformation`, `40_opensearch`, `41_snowflake_pyiceberg`, `42_aws_lambda_de`, `43_terraform_de`, `44_pyiceberg`, `45_great_expectations`, `46_cicd_data`, `47_redis_de`

### 5D. Infrastructure (`_infra/`)
Fully containerized Docker Compose environment.

| Stack | File | Services |
|-------|------|---------|
| Core | `docker/core.yml` | PostgreSQL, Redis, base services |
| Streaming | `docker/streaming.yml` | Kafka, Zookeeper |
| Pipeline | `docker/pipeline.yml` | Spark master/workers, Airflow |
| Observability | `docker/observability.yml` | Grafana, Prometheus, etc. |
| Full | `docker/docker-compose.yml` | All stacks combined |

**Infrastructure scripts:**
```powershell
.\scripts\infra_up.ps1        # start all services
.\scripts\infra_down.ps1      # stop all services
.\scripts\infra_seed.ps1      # seed test data
.\scripts\infra_health.ps1    # health check
.\seeds\seed_core.py          # Python seeding script
```

Credentials for Docker services live in `_infra/env/.env.local` (gitignored).

### 5E. Connection Proofs (`poc/connection_proofs/`)
Proof-of-connection scripts for all cloud platforms and local Docker services.

| Runner | Coverage |
|--------|---------|
| `Run-AllDockerProofs.ps1` | All Docker service proofs |
| `Run-CoreDockerProofs.ps1` | Core stack proofs |
| `Run-StreamingDockerProofs.ps1` | Kafka/streaming proofs |
| `Run-PipelineDockerProofs.ps1` | Spark/Airflow proofs |
| `Run-ObservabilityDockerProofs.ps1` | Grafana/monitoring proofs |
| `poc/connection_proofs/python/` | AWS, Azure, Databricks, Snowflake, MongoDB, GCP |

### 5F. Playground & Interview Prep
- `playground/` — active LeetCode prep workspace, session handoffs, progress trackers
  - `THURSDAY_CODING_TEST_PROGRESS.md` — active session-to-session coding test tracker
  - `claude_progress.md` — historical progress notes
  - `studyGuide/` — study guide notebooks
- `interview/` — 10 deep-dive interview prep notebooks (DE behavioral guides, cloud platforms, distributed systems, ML pipeline, data quality, orchestration, system design)

### 5G. Other Notable Areas
- `HorizonScale/` — forecasting and capacity engineering project (has own env_setter, models, data)
- `jobdatabrain-tagger/` — job data brain tagger POC (background DB updater, data sources, dictionary)
- `_prompts/` — prompt library: `tracks/` (current), `legacy/` (migrated from Workspace)
- `scripts/` — utility scripts: env management, migration, audio generation, job rendering, ADR tools
- `data/jobs/` — 65 job application folders (job search pipeline output — see pruning doc)
- `data/master/` — master data assets
- `data/vectorstore/` — FAISS vector index
- `docs/programs/zero_to_hero/` — migration program board, execution system, cloud account registry
- `docs/adr/` — Architecture Decision Records
- `docs/operations/` — secrets workflow, AWS credentials workflow
- `docs/manuals/` — generated study manuals

---

## 6. Agent Infrastructure

### Startup order (mandatory before any agent work)
Read these files in order:
1. `CONTROL_PROTOCOL.md`
2. `agents/shared/context_index.md`
3. `agents/shared/open_loops.md`
4. `agents/shared/approval_matrix.md`
5. `agents/shared/command_allowlist.md`
6. `docs/adr/ADR-INDEX.md`
7. `agents/shared/pending_task.md` (if present)
8. `agents/shared/agent_status.md` (if present)
9. `agents/shared/decision_log.md` (if present)

### Agent memory files (`agents/shared/`)
| File | Purpose |
|------|---------|
| `context_index.md` | Compact durable memory map — start here |
| `open_loops.md` | Incomplete work items (163 loops tracked, most closed) |
| `agent_status.md` | Overwritten every run — factual outcome summary |
| `task_register.md` | All tasks: in_progress / done / blocked |
| `decision_log.md` | Durable architectural decisions |
| `approval_matrix.md` | What agent can do autonomously vs must ask |
| `command_allowlist.md` | Allowed shell commands |
| `pending_task.md` | Current active task contract |
| `parking_lot.md` | Out-of-scope findings parked for later |
| `user_profile.md` | Sean's career identity, preferences, working style |
| `daily_todo.json` | Daily task list |

### Task contract format (CONTROL_PROTOCOL.md §6)
Every task needs: `Task ID` (`TB-YYYYMMDD-XX`), `Task Type`, `Goal`, `Non-Goals`, `Allowed Scope` (`strict`/`bounded`), `Validation Commands`, `Definition of Done`, `Reasoning Depth`, `Risk Level`.

### Autonomy defaults
- Modify up to 8 related files per run
- Run required validation commands
- Complete up to 3 tightly related subtasks
- **Stop and ask** for: destructive actions, credential changes, external system writes

---

## 7. Open Loops (as of 2026-04-27)

Items still `open` or `in_progress` in `agents/shared/open_loops.md`:

| Loop | Item | Next Action |
|------|------|-------------|
| LOOP-005 | Cloud secret routing + migration sanitization gate | Continue provider secret mapping |
| LOOP-007 | MongoDB credential rotation — not yet in encrypted secrets | Run bootstrap encryption, rotate Atlas password |
| LOOP-008 | GCP key placeholder normalization | Decide if legacy path still required |
| LOOP-023 | `__dupNNN` files in `_prompts/legacy/technologies/` (88 files) | Review conflicts_report.md, decide keep vs dedupe |
| LOOP-025 | Migration board reconciliation for M-003/M-012 | Decide on remaining D:\Workspace\Technologies assets |
| LOOP-098 | DPAPI seed decrypt mismatch in specific shell context | Re-register or repair machine-local seed |
| LOOP-107 | Thursday coding test prep continuity | Continue appending outcomes to `playground/THURSDAY_CODING_TEST_PROGRESS.md` |
| LOOP-161 | EMR capstone support files missing | Add `cleanup.py`, `test_capstone.py` under `tutorials/06_aws_emr/capstone/` |

---

## 8. Merging New Content In

Use this decision tree when adding study material from another repo or source:

```
New content to add?
│
├── Coding challenge / LeetCode?
│   └── → coding_challenges/  (use index_cli.ps1 to register)
│
├── Technology deep-dive / runnable tutorial?
│   └── → tutorials/<next_number>_<tech_name>/
│       Add: README.md, prompt_READY_TO_PASTE.md, lesson scripts
│
├── 5–10 min runnable learning module?
│   └── → tracks/08_databases/micro_nuggets/<tech>/  (for DB topics)
│       or tracks/<relevant_track>/micro_nuggets/
│
├── Interview prep guide?
│   └── → interview/  (Jupyter notebook format preferred)
│
├── Research / experimental POC?
│   └── → poc/  (or poc/connection_proofs/ if proving connectivity)
│
├── Prompt / AI context file?
│   └── → _prompts/tracks/<topic>/  (canonical)
│       NOT legacy/ — that's for migrated Workspace content only
│
├── Study notes / roadmaps?
│   └── → docs/  or docs/programs/
│
└── Cloud infra / Docker service?
    └── → _infra/docker/ (add to appropriate compose stack)
        Document in _infra/README.md
```

**Before merging from another repo:**
1. Check `docs/programs/zero_to_hero/MIGRATION_BOARD.md` — task may already exist
2. Use a migration script under `scripts/migration/` if batch-moving files
3. Run secret scan: `git grep -r "password\|secret\|token\|key" <folder>` before committing
4. Register task in `agents/shared/task_register.md`

---

## 9. Critical File Index

| File | Why It Matters |
|------|---------------|
| `SPRINGBOARD.md` | **Start here** — purpose-driven navigation hub ("I want to...") |
| `CONTROL_PROTOCOL.md` | Agent operating rules — 15 clauses |
| `env_setter.ps1` | Mandatory session bootstrap — Java, venv, secrets |
| `agents/shared/context_index.md` | Fast session orientation — read first |
| `agents/shared/open_loops.md` | Incomplete work tracker |
| `agents/shared/user_profile.md` | Sean's career data, working style, preferences |
| `docs/PORTABLE_ENV.md` | Machine setup guide |
| `docs/operations/secrets_workflow.md` | Full secrets system documentation |
| `docs/programs/zero_to_hero/MIGRATION_BOARD.md` | Migration wave tracker |
| `coding_challenges/index.csv` | Source of truth for all coding challenges |
| `coding_challenges/STUDY_MANUAL_V1.md` | Coding study guide |
| `_infra/README.md` | Docker service dictionary |
| `scripts/env/bootstrap_all.ps1` | New machine guided setup |
| `docs/handoff.md` | This file |
| `docs/pruning_and_duplicates.md` | Known duplicates and cleanup candidates |

---

## 10. Pruning & Cleanup

See `docs/pruning_and_duplicates.md` for a full analysis of:
- Binary files tracked in git (`index.xlsx`, `StudyBook.lnk`)
- 88 `__dupNNN` files in `_prompts/legacy/`
- 46 `prompt_READY_TO_PASTE.md` copies across tutorials
- 217 `.docx` binaries in `data/jobs/`
- Temp migration artifacts
- Duplicate-numbered tutorials (`02_PySpark_Docker` vs `02_pyspark`)

---
*Last fully reviewed: 2026-04-27*
