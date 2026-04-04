# DBT Micro-Nuggets Production Execution Master Prompt

Use this prompt with external code agents to implement a complete, tested dbt micro-nuggets lane for Data Engineering and interview preparation.

```text
You are a senior code agent working in this repo: D:\StudyBook

MISSION
Build a production-grade dbt micro-nuggets learning system for Data Engineering and interview prep.
It must be runnable by a beginner on Windows PowerShell with copy/paste commands.

PRIMARY TARGET LOCATION
Create everything under:
D:\StudyBook\tracks\11_batch_processing\micro_nuggets\dbt

MANDATORY PRE-WORK (DO THIS FIRST)
1) Discover existing connection proof conventions in this repo:
   - D:\StudyBook\poc\connection_proofs\python
   - Reuse existing env loading + secrets flow patterns.
2) Select default execution backend automatically (no user questions):
   Priority order:
   a) PostgreSQL (if local Docker/service reachable)
   b) Snowflake (if credentials + connectivity available)
   c) Databricks SQL (if host/token/http_path available)
   d) DuckDB local fallback (always available)
3) Implement setup so lane is runnable even when cloud services are unavailable.
   - If cloud unavailable, use DuckDB path and still complete all nuggets.
4) Build and run automated verification before delivery.

NON-NEGOTIABLE REQUIREMENTS
- Production-grade code quality.
- Idempotent setup/reset scripts.
- Clear error handling with exact actionable fix text.
- Every nugget prints meaningful success/failure output.
- Windows-first docs and commands.
- No hardcoded secrets.
- Use existing StudyBook env + machine config conventions.
- Keep files ASCII unless existing file requires otherwise.
- Add deep teachable comments in concept-heavy code/SQL.

SCOPE TO IMPLEMENT

A) Folder structure
D:\StudyBook\tracks\11_batch_processing\micro_nuggets\dbt\
  00_setup\
    00_prereq_check.py
    01_seed_lab.py
    99_reset_lab.py
  01_dbt_basics\
    01_project_init_and_profiles.py
    02_sources_and_staging.py
  02_modeling_and_materializations\
    01_views_tables_incremental.py
    02_ephemeral_and_ref_graph.py
  03_tests_and_quality\
    01_generic_tests.py
    02_custom_tests_and_data_contracts.py
  04_snapshots_and_scd\
    01_snapshots_scd2.py
  05_operations_and_deploy\
    01_run_build_seed_docs.py
    02_selectors_state_artifacts.py
  06_interview_drills\
    01_interview_drills.py
  07_mini_capstone\
    01_mini_capstone.py
  _dbt_lane_connect.py
  run_all_dbt_nuggets.py
  DBT_SPEEDY_STORY_AND_INTERVIEW.md
  DBT_GLOSSARY.md
  README.md

B) Required dbt project assets (inside lane)
- Full dbt project under the lane, including:
  - dbt_project.yml
  - profiles template (non-secret)
  - models/, snapshots/, tests/, macros/, seeds/
  - schema.yml docs/tests definitions
- Include cross-platform-safe pathing for Windows.

C) Preparatory stage (must be implemented and tested)
- Validate:
  - python + dbt package + adapter package
  - selected backend connectivity
- Seed realistic DE data:
  - raw events/orders/customers/products/payments
  - include late-arriving records + duplicate keys + updates for SCD snapshot demo
- Reset script must clean all created dbt artifacts/lab objects and be re-runnable.

D) Required concept coverage
Must include runnable nuggets for:
- dbt core workflow: seed, run, test, build, docs generate
- source() + staging layer
- ref() DAG lineage
- materializations: view, table, incremental, ephemeral
- incremental strategies + unique_key + on_schema_change
- snapshots for SCD Type 2
- generic tests (not_null, unique, relationships, accepted_values)
- custom tests + singular tests
- macros and Jinja basics (at least 2 practical macros)
- selectors + state-aware build basics
- data contracts/schema enforcement concepts
- mini-capstone with Bronze->Silver->Gold style model layers

E) Interview package (mandatory)
- Add concise interview Q&A covering:
  - dbt architecture and DAG
  - incremental vs full-refresh tradeoffs
  - snapshots vs MERGE SCD2
  - testing strategy and CI/CD
  - artifacts (manifest/run_results) and lineage
  - performance + cost controls

F) Story + glossary (mandatory)
- DBT_SPEEDY_STORY_AND_INTERVIEW.md:
  - coherent learning narrative from beginner to project-ready DE
- DBT_GLOSSARY.md:
  - plain-English terms with links to where each concept is shown

RUNNER + VALIDATION (MANDATORY)
1) Implement:
   D:\StudyBook\tracks\11_batch_processing\micro_nuggets\dbt\run_all_dbt_nuggets.py
   - One-line PASS/FAIL per nugget
   - Summary totals
   - Windows-safe stdout handling
   - Timeout handling
   - Distinguish SKIP vs FAIL when backend unavailable
2) Execute real validation commands before delivery:
   - setup, seed, run, test, snapshot, docs generate
   - full lane runner
3) If failures occur, fix and rerun until green (or provide exact external blocker evidence).

BEGINNER EXECUTION GUIDE (MANDATORY IN README)
Provide exact copy/paste commands:
1) open folder + activate env
2) install dbt dependencies/adapters
3) run setup
4) run one nugget
5) run all nuggets
6) reset lab
7) common failures + exact fixes

BACKEND STRATEGY REQUIREMENTS
- Auto-detect backend; print selected backend and why.
- Always include a guaranteed local fallback (DuckDB) so lane can run anywhere.
- Keep cloud-specific paths optional and clearly documented.

QUALITY BAR
- No TODO placeholders.
- No conceptual-only files without runnable demonstrations.
- No claims of success without command evidence.
- Ensure repeatable outputs and rerun safety.

DELIVERY FORMAT
At completion, provide:
1) full file tree created
2) module-by-module implementation summary
3) exact validation commands actually run
4) pass/fail table per script
5) known constraints and residual risks
6) recommended phase-2 expansion

WORK STYLE
- Make reasonable assumptions and proceed.
- Do not wait for optional clarifications.
- Deliver complete, tested, production-grade artifacts.
```
