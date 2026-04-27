# StudyBook Springboard

> Start here. Find what you need in under 10 seconds.
> **First command every session:** `. .\env_setter.ps1 -NonInteractive`

---

## I want to...

### Practice a coding problem
```
coding_challenges/          ← 166+ notebooks (0001–0166+)
coding_challenges/leetcode/ ← organized by topic
coding_challenges/_assessment_training/ ← mock interview harnesses
playground/                 ← active scratch space + session notes
```
```powershell
.\search_index.ps1 <topic or number>          # find a challenge fast
.\index_cli.ps1 find <keyword>                # CLI search
.\run_index_ui.ps1                            # Streamlit UI (localhost:8501)
.\run_index_ui_docker.ps1 -Action up          # Dockerized UI
.\refresh_index_and_push.ps1                  # rebuild index + git push
```

---

### Learn a technology (deep-dive tutorial)
```
tutorials/                  ← 49 runnable tutorial folders
```
| I want to learn... | Go to |
|--------------------|-------|
| PySpark on Docker cluster | `tutorials/02_PySpark_Docker/` |
| PySpark local | `tutorials/48_pyspark_local/` |
| Apache Airflow + Docker | `tutorials/03_apache_airflow_docker/` |
| AWS EMR Serverless | `tutorials/06_aws_emr/` |
| AWS Glue | `tutorials/07_aws_glue/` |
| AWS IAM + STS | `tutorials/16_aws_iam/` |
| AWS Kinesis | `tutorials/01_aws_kinesis/` |
| AWS S3 patterns | `tutorials/08_aws_s3/` |
| AWS Lambda | `tutorials/31_aws_lambda/` |
| AWS Redshift | `tutorials/21_aws_redshift/` |
| AWS Athena | `tutorials/22_aws_athena/` |
| AWS DynamoDB | `tutorials/32_aws_dynamodb/` |
| AWS MSK Kafka | `tutorials/33_aws_msk_kafka/` |
| AWS Bedrock | `tutorials/34_aws_bedrock/` |
| AWS Step Functions | `tutorials/04_aws_step_functions/` |
| AWS CloudFormation | `tutorials/39_aws_cloudformation/` |
| AWS ECS | `tutorials/38_aws_ecs/` |
| AWS CloudWatch | `tutorials/09_aws_cloudwatch/` |
| Delta Lake | `tutorials/05_delta_lake/` |
| dbt | `tutorials/11_dbt/` |
| Terraform | `tutorials/35_terraform/` |
| Docker fundamentals | `tutorials/36_docker/` |
| CI/CD | `tutorials/37_cicd/` |
| PostgreSQL patterns | `tutorials/17_postgresql/` |
| SQL patterns | `tutorials/18_sql_patterns/` |
| Parquet | `tutorials/12_parquet/` |
| Python concurrency | `tutorials/13_python_concurrency/` |
| Python testing | `tutorials/19_python_testing/` |
| Python logging | `tutorials/10_python_logging/` |
| Pydantic | `tutorials/20_pydantic/` |
| Pandas | `tutorials/24_pandas/` |
| Polars | `tutorials/26_polars/` |
| DuckDB | `tutorials/27_duckdb/` |
| SQLAlchemy | `tutorials/23_sqlalchemy/` |
| Streamlit | `tutorials/29_streamlit/` |
| FastAPI | `tutorials/30_fastapi/` |
| Great Expectations | `tutorials/45_great_expectations/` |
| OpenSearch | `tutorials/40_opensearch/` |
| Snowflake + PyIceberg | `tutorials/41_snowflake_pyiceberg/` |
| Redis | `tutorials/47_redis_de/` |
| Scala (patterns, case classes, Spark) | `tutorials/49_scala/` |
| Splunk (concepts, guide, DE patterns, vs ELK, Citi narrative) | `tutorials/50_splunk/` |
| Encryption | `tutorials/14_encryption/` |
| PII anonymization | `tutorials/15_data_anonymization_pii/` |
| Data stubbing | `tutorials/28_data_stubbing/` |

Each tutorial folder has a `prompt_READY_TO_PASTE.md` — paste it to an AI to load full context instantly.

---

### Do a quick micro-nugget (5–10 min runnable module)
```
tracks/08_databases/micro_nuggets/
```
| Topic | Status | Lane |
|-------|--------|------|
| PostgreSQL | ✅ 16/16 PASS | `micro_nuggets/postgresql/` → `run_all_postgresql_nuggets.py` |
| Databricks | ✅ validated | `micro_nuggets/databricks/` → Bronze→Silver→Gold, MERGE, Time Travel |
| Snowflake | ✅ validated | `micro_nuggets/snowflake/` → DDL, DML, connection setup |
| MongoDB | ✅ 26 nuggets | `micro_nuggets/mongodb/` → `run_all_mongodb_nuggets.py` |

---

### Spin up or manage Docker infrastructure
```
_infra/                     ← all Docker compose stacks
```
```powershell
.\_infra\scripts\infra_up.ps1       # start all services
.\_infra\scripts\infra_down.ps1     # stop all services
.\_infra\scripts\infra_health.ps1   # check service health
.\_infra\scripts\infra_seed.ps1     # seed test data
```
| Stack | File | What it runs |
|-------|------|-------------|
| Core | `_infra/docker/core.yml` | PostgreSQL, Redis |
| Streaming | `_infra/docker/streaming.yml` | Kafka, Zookeeper |
| Pipeline | `_infra/docker/pipeline.yml` | Spark, Airflow |
| Observability | `_infra/docker/observability.yml` | Grafana, Prometheus |
| All | `_infra/docker/docker-compose.yml` | Everything |

Credentials: `_infra/env/.env.local` (gitignored)

---

### Prove a cloud or service connection
```
poc/connection_proofs/          ← proof scripts for every platform
poc/connection_proofs/python/   ← AWS, Azure, Databricks, Snowflake, MongoDB, GCP
```
```powershell
.\poc\connection_proofs\Run-AllDockerProofs.ps1         # all Docker services
.\poc\connection_proofs\Run-CoreDockerProofs.ps1        # core stack only
.\poc\connection_proofs\Run-StreamingDockerProofs.ps1   # Kafka
.\poc\connection_proofs\Run-PipelineDockerProofs.ps1    # Spark + Airflow
```

---

### Find or use a prompt
```
_prompts/tracks/        ← canonical prompts by topic (use these)
_prompts/legacy/        ← migrated Workspace prompts (reference only)
```
Each tutorial also has its own `prompt_READY_TO_PASTE.md` for localized context.

---

### Prep for an interview
```
interview/              ← 10 deep-dive behavioral + technical guides (Jupyter)
coding_challenges/_assessment_training/   ← mock harnesses (Two Sum, LIS, MinStack, etc.)
playground/studyGuide/  ← study guide notebooks with anchor navigation
```
Key interview guides:
- `de_interview_data_pipeline_design_guide.ipynb`
- `de_interview_distributed_systems_guide.ipynb`
- `de_interview_cloud_data_platforms_guide.ipynb`
- `de_interview_behavioral_aws_migration_guide.ipynb`
- `de_interview_ml_pipeline_guide.ipynb`

---

### Resume agent work / continue from last session
```powershell
Get-Content .\agents\shared\context_index.md -TotalCount 200   # memory map
Get-Content .\agents\shared\open_loops.md -TotalCount 100      # open work
Get-Content .\agents\shared\agent_status.md                    # last run outcome
Get-Content .\agents\shared\pending_task.md                    # active task (if any)
```
Agent startup order: `CONTROL_PROTOCOL.md` → `context_index.md` → `open_loops.md` → `approval_matrix.md` → `command_allowlist.md` → `docs/adr/ADR-INDEX.md`

---

### Track active work and todos
```
agents/shared/open_loops.md       ← 163 loops tracked, 8 still open
agents/shared/task_register.md    ← all tasks: in_progress / done / blocked
agents/shared/daily_todo.json     ← today's task list
agents/shared/parking_lot.md      ← out-of-scope findings parked for later
playground/THURSDAY_CODING_TEST_PROGRESS.md  ← active coding test tracker
```

---

### Merge new content in
| What you have | Where it goes |
|---------------|--------------|
| Coding challenge / LeetCode | `coding_challenges/` → register with `.\index_cli.ps1 add ...` |
| Technology tutorial | `tutorials/<next_number>_<tech_name>/` |
| 5–10 min runnable module | `tracks/08_databases/micro_nuggets/<tech>/` |
| Interview prep guide | `interview/` (Jupyter notebook) |
| Research / POC | `poc/` |
| Prompt | `_prompts/tracks/<topic>/` |
| Study notes / roadmaps | `docs/` |
| Docker service | `_infra/docker/` + document in `_infra/README.md` |

See `docs/handoff.md §8` for the full merge decision tree and migration checklist.

---

### Set up on a new machine
```powershell
.\scripts\env\bootstrap_all.ps1                             # guided full setup
$env:STUDYBOOK_SECRET_PASSPHRASE = "<your-passphrase>"
.\scripts\env\register_secret_seed.ps1 -NonInteractive -Force  # register seed once
.\env_setter.ps1 -NonInteractive                            # verify it works
```
Full guide: `docs/PORTABLE_ENV.md`
Secrets system: `docs/operations/secrets_workflow.md`

---

### Access a sibling repo
| Repo | Path | Purpose |
|------|------|---------|
| Job search pipeline | `D:\Workarea\jobsearch` | 5-step PS1 job application pipeline |
| Portfolio + blog | `D:\Workarea\seanlgirgis.github.io` | Public GitHub Pages site |

Cross-machine restore: `pwsh .\scripts\ops\restore_managed_repos.ps1`

---

### Run or work on an internal tool (Proj_development)
```
Proj_development/   ← small personal utilities, no separate repos
```
| Tool | Path | What it does |
|------|------|--------------|
| UniversalClipboardManager | `Proj_development/UniversalClipboardManager/` | PyQt6 global hotkey clipboard manager — auto-paste, JSON persistence, Windows startup |

**Launch clipboard manager:**
```powershell
cd D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager
.\launch_clipboard.bat
```
Hotkeys: `Ctrl+Shift+S` toggle window · `Ctrl+Alt+A` capture clipboard

**Install/reinstall Windows startup shortcut** (run once after any move):
```powershell
.\install_startup.ps1
```

---

### Work on learning content for the website
```
scripts/generate_audio.py       ← generate MP3 audio for learning pages
scripts/run_mission_audio.ps1   ← full audio mission runner
```
See `WEBSITE_AGENT_CONTEXT.md` at repo root for the full website agent context.

---

### Read a concept guide (explanation + interview Q&A)
```
docs/concepts/data_engineering_guides/   ← 35 first-swipe guides migrated from Capital One prep
```
| I want to understand... | Go to |
|------------------------|-------|
| Scala fundamentals + Spark | `00001.Scala.FS.md` + `00002.Scala.Q.md` |
| Kafka / real-time streaming | `00003.KafkaAndRealTimeStreaming.md` + `.Q.md` |
| MongoDB / NoSQL patterns | `00005.mongo.nosql.md` + `.Q.md` |
| Cassandra / wide-column NoSQL | `00007.Cassandra.nosql.md` + `.Q.md` |
| Distributed systems / microservices | `00009.Distributed_MicroServices.md` + `.Q.md` |
| Kubernetes | `00011.Kubernetes.md` + `.Q.md` |
| Apache Flink | `00014.Flink.md` + `.Q.md` |
| AWS EMR (concept) | `00016.EMR.md` + `.Q.md` |
| PySpark (concept) | `00020.PySpark.md` + `.Q.md` |
| Scala + Spark together | `00022.Scala_Spark.md` + `.Q.md` |
| Data Warehouses | `00026.DataWarehouses.md` + `.Q.md` |
| Data Lakes | `00028.DataLakes.md` + `.Q.md` |
| Data Lakehouses | `00030.DataLakehouses.md` + `.Q.md` |
| Hadoop ecosystem | `00032.Hadoop.md` + `.Q.md` |

Each guide pairs a `.md` (concept) with a `.Q.md` (interview Q&A).

---

## Key Docs

| Doc | Purpose |
|-----|---------|
| `docs/handoff.md` | Full operational reference — architecture, all areas, agent protocol |
| `docs/concepts/data_engineering_guides/` | 35 DE concept guides + Q&A (Scala, Kafka, NoSQL, distributed systems, lakes) |
| `docs/pruning_and_duplicates.md` | Cleanup tracker — what's been pruned, what's still open |
| `docs/PORTABLE_ENV.md` | Machine setup guide |
| `docs/operations/secrets_workflow.md` | DPAPI secrets system |
| `docs/programs/zero_to_hero/MIGRATION_BOARD.md` | Migration wave tracker |
| `docs/adr/ADR-INDEX.md` | Architecture Decision Records index |
| `coding_challenges/STUDY_MANUAL_V1.md` | Coding study manual |
| `_infra/README.md` | Docker service dictionary |
| `agents/STUDYBOOK_FAST_GUIDE.md` | Quick agent orientation |

---

*Keep this file flat and fast. If something doesn't fit in a one-liner, it belongs in `docs/handoff.md`.*
