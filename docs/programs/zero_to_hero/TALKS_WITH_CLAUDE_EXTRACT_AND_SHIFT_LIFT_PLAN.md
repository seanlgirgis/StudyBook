# TalksWithClaude Value Extraction and Shift-Lift Placement Plan

## Scope
- Source transcript reviewed: `D:\StudyBook\temp\TalksWithClaude.md` (`7467` lines).
- Source workspace reviewed: `D:\Workspace`.
- Canonical target runtime repo: `D:\StudyBook`.
- Deprecated path note: `D:\ZeroToHero_DE_AI` was deleted and is no longer a valid target.

## High-Value Facts Extracted

### Proven Execution Signals
- Technologies R1 notebooks reported green with concrete outputs:
  - `kafka_intro.ipynb`
  - `spark_intro.ipynb`
  - `airflow_intro.ipynb`
  - `mlflow_intro.ipynb`
  - `splunk_intro.ipynb`
- Technologies R3 notebooks reported green (`44/44` cells) across:
  - `lambda_kappa_architecture.ipynb`
  - `streaming_pipeline_end2end.ipynb`
  - `batch_pipeline_end2end.ipynb`
  - `platform_decision_matrix.ipynb`
  - `modern_de_stack_2026.ipynb`
  - `system_design_streaming.ipynb`
  - `system_design_batch.ipynb`
  - `technologies_interview_sim.ipynb`
  - `technologies_interview_sim_production.ipynb`

### Critical Architecture Lessons
- Schema duality must be preserved:
  - Databases stack: `telemetry.*` with UUID-centric schema.
  - Technologies stack: `public.*` with simplified IDs/columns.
- `seed_tech_telemetry.py` is critical for Technologies notebook correctness.
- Spark on Windows requires explicit local compatibility handling.
- Airflow notebook interactions should be REST-oriented.

### Asset Volume (Workspace Snapshot)
- `D:\Workspace\Technologies` notebooks: `54`
- `D:\Workspace\Technologies\prompts`: `R0=6`, `R1=24`, `R2=53`, `R3=11`, `system=1`
- `D:\Workspace\Basics\Databases\prompts`: `R2=35`, `R3=20`
- `D:\Workspace\Basics\Databases` notebooks: `13`

## Shift-Lift Placement Plan (Workspace -> StudyBook)

### Class A: Infra and Seed Assets (First)

| Source | Target | Class | Status | Notes |
|---|---|---|---|---|
| `D:\Workspace\Technologies\_setup\docker-compose.technologies.yml` | `D:\StudyBook\_infra\docker\streaming.yml`, `pipeline.yml`, `observability.yml` | `migrate_with_adaptation` | done | Split by domain with stable service contract |
| `D:\Workspace\Basics\Databases\_setup\docker-compose.yml` | `D:\StudyBook\_infra\docker\core.yml` | `migrate_with_adaptation` | done | Core data services layer |
| `D:\Workspace\Basics\Databases\_setup\master_seed_data.py` | `D:\StudyBook\_infra\seeds\seed_core.py` | `migrate_with_adaptation` | done | Idempotent telemetry seed path |
| `D:\Workspace\Technologies\_setup\seed_tech_telemetry.py` | `D:\StudyBook\_infra\seeds\seed_tech_telemetry.py` | `migrate_as_is` | done | Deterministic tech seed retained |
| `D:\Workspace\Technologies\_setup\verify_tech_stack.py` + `verify_all.py` | `D:\StudyBook\_infra\scripts\infra_health.ps1` | `migrate_with_adaptation` | done | Unified health check with JSON output |

### Class B: Prompt Assets (Legacy First, Canonical Second)

| Source | Target | Class | Status | Notes |
|---|---|---|---|---|
| `D:\Workspace\Technologies\prompts\R1\*.md` | `D:\StudyBook\_prompts\legacy\technologies\R1\*.md` | `migrate_as_is` | todo | Preserve source prompt contracts |
| `D:\Workspace\Technologies\prompts\R2\*.md` | `D:\StudyBook\_prompts\legacy\technologies\R2\*.md` | `migrate_as_is` | todo | Keep before canonical refactor |
| `D:\Workspace\Technologies\prompts\R3\*.md` | `D:\StudyBook\_prompts\legacy\technologies\R3\*.md` | `migrate_as_is` | todo | Includes end-to-end prompt definitions |
| `D:\Workspace\Basics\Databases\prompts\R2\*.md` | `D:\StudyBook\_prompts\legacy\databases\R2\*.md` | `migrate_as_is` | todo | Databases deep-round source |
| `D:\Workspace\Basics\Databases\prompts\R3\*.md` | `D:\StudyBook\_prompts\legacy\databases\R3\*.md` | `migrate_as_is` | todo | Databases synthesis-round source |

### Class C: Executable Notebook Assets (Validated Priority)

| Source | Target | Class | Status | Notes |
|---|---|---|---|---|
| `D:\Workspace\Technologies\kafka_intro.ipynb` | `D:\StudyBook\tracks\10_streaming\r1\kafka_intro.ipynb` | `migrate_as_is` | todo | validated signal in transcript |
| `D:\Workspace\Technologies\spark_intro.ipynb` | `D:\StudyBook\tracks\11_batch_processing\r1\spark_intro.ipynb` | `migrate_as_is` | todo | validated signal in transcript |
| `D:\Workspace\Technologies\airflow_intro.ipynb` | `D:\StudyBook\tracks\12_orchestration\r1\airflow_intro.ipynb` | `migrate_as_is` | todo | keep REST-oriented interactions |
| `D:\Workspace\Technologies\mlflow_intro.ipynb` | `D:\StudyBook\tracks\22_ml_platform\r1\mlflow_intro.ipynb` | `migrate_as_is` | todo | validated signal in transcript |
| `D:\Workspace\Technologies\splunk_intro.ipynb` | `D:\StudyBook\tracks\29_observability\r1\splunk_intro.ipynb` | `migrate_as_is` | todo | validated signal in transcript |
| `D:\Workspace\Technologies\lambda_kappa_architecture.ipynb` | `D:\StudyBook\tracks\10_streaming\r3\lambda_kappa_architecture.ipynb` | `migrate_as_is` | todo | R3 validated set |
| `D:\Workspace\Technologies\streaming_pipeline_end2end.ipynb` | `D:\StudyBook\tracks\10_streaming\r3\streaming_pipeline_end2end.ipynb` | `migrate_as_is` | todo | R3 validated set |
| `D:\Workspace\Technologies\batch_pipeline_end2end.ipynb` | `D:\StudyBook\tracks\11_batch_processing\r3\batch_pipeline_end2end.ipynb` | `migrate_as_is` | todo | R3 validated set |
| `D:\Workspace\Technologies\platform_decision_matrix.ipynb` | `D:\StudyBook\tracks\30_system_design\r3\platform_decision_matrix.ipynb` | `migrate_as_is` | todo | R3 validated set |
| `D:\Workspace\Technologies\modern_de_stack_2026.ipynb` | `D:\StudyBook\tracks\30_system_design\r3\modern_de_stack_2026.ipynb` | `migrate_as_is` | todo | R3 validated set |
| `D:\Workspace\Technologies\system_design_streaming.ipynb` | `D:\StudyBook\tracks\30_system_design\r3\system_design_streaming.ipynb` | `migrate_as_is` | todo | R3 validated set |
| `D:\Workspace\Technologies\system_design_batch.ipynb` | `D:\StudyBook\tracks\30_system_design\r3\system_design_batch.ipynb` | `migrate_as_is` | todo | R3 validated set |
| `D:\Workspace\Technologies\technologies_interview_sim.ipynb` | `D:\StudyBook\interview\de_interview_sim.ipynb` | `migrate_with_adaptation` | todo | canonical naming |
| `D:\Workspace\Technologies\technologies_interview_sim_production.ipynb` | `D:\StudyBook\interview\de_interview_sim_production.ipynb` | `migrate_with_adaptation` | todo | explicit production variant |
| `D:\Workspace\Basics\Databases\*.ipynb` | `D:\StudyBook\tracks\08_databases\r1` and `r2` | `migrate_with_adaptation` | todo | place by topic and round |

### Class D: Keep Out of Migration

| Source | Rule | Reason |
|---|---|---|
| `D:\Workspace\Technologies\_setup\tech.env` | `archive_or_drop` | secret-bearing file |
| `D:\Workspace\Technologies\_setup\gcp_key.json` | `archive_or_drop` | credential file |
| `D:\Workspace\Technologies\_setup\gcp_key.json.json` | `archive_or_drop` | duplicate credential artifact |
| Any prompt/notebook with hardcoded passwords/tokens | `migrate_with_adaptation` | sanitize to env references |
| `D:\Workspace\Technologies\azure_de_intro_recreated.ipynb` | `archive_or_drop` | duplicate variant |

## Execution Order (No Calendar)
1. `BATCH-MIG-01A`: infra shift/lift (done)
2. `BATCH-MIG-02A`: validated notebook shift/lift
3. `BATCH-MIG-03A`: prompt shift/lift and canonical derivation
4. `BATCH-SEC-01`: secret scan/sanitization completion
5. `BATCH-VERIFY-01`: clean-shell reproducibility proof

## Immediate Next Slice
- Execute `M-011`: move validated Technologies notebooks into `D:\StudyBook\tracks` + `interview` and run smoke checks.
