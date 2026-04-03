# Databricks Bridge Micro-Nuggets Production Execution Master Prompt

Use this prompt with external code agents to implement a complete, tested Databricks bridge micro-nuggets lane for Data Engineering and interview preparation.

```text
You are a senior code agent working in this repo: D:\StudyBook

MISSION
Build a production-grade Databricks micro-nuggets system focused on Data Engineering depth, interview readiness, and cross-engine transfer from PostgreSQL/Snowflake concepts.
This must be runnable by a beginner using Windows PowerShell.

PRIMARY TARGET LOCATION
Create everything under:
D:\StudyBook\tracks\08_databases\micro_nuggets\databricks_bridge

MANDATORY PRE-WORK (DO THIS FIRST)
1) Discover and reuse existing Databricks connection patterns already in repo:
   - D:\StudyBook\poc\connection_proofs\python\databricks_connection_proof.py
   - Existing Databricks nugget helpers under:
     D:\StudyBook\tracks\08_databases\micro_nuggets\databricks
2) Reuse repository env/secret conventions (no hardcoded creds):
   - DATABRICKS_HOST
   - DATABRICKS_TOKEN
   - DATABRICKS_HTTP_PATH (when SQL warehouse connector is used)
3) Build a preparatory stage that creates/validates all required schemas/tables and sample data.
   - Must be idempotent and safe to rerun.
4) Build and run full validation before claiming completion.

NON-NEGOTIABLE REQUIREMENTS
- Production-grade code quality and error handling.
- Every nugget is runnable and prints clear PASS/FAIL style outcomes.
- No secrets in code, docs, outputs, or commits.
- Windows-first command instructions.
- Idempotent setup/reset.
- Deterministic outputs where practical.
- Beginner-proof execution instructions.
- Teachable comments explaining WHY, not only WHAT.

SCOPE TO IMPLEMENT

A) Folder structure
D:\StudyBook\tracks\08_databases\micro_nuggets\databricks_bridge\
  00_setup\
  01_sql_foundations\
  02_cte_and_windowing\
  03_delta_core\
  04_de_patterns\
  05_performance_and_optimization\
  06_governance_and_security\
  07_data_quality_and_testing\
  08_interview_drills\
  09_mini_capstone\
  _db_bridge_connect.py
  run_all_databricks_bridge_nuggets.py
  DATABRICKS_BRIDGE_SPEEDY_STORY_AND_INTERVIEW.md
  DATABRICKS_BRIDGE_GLOSSARY.md
  README.md
  CROSS_ENGINE_SQL_MAP.md

B) Preparatory stage (must be implemented and tested)
Implement scripts in 00_setup:
1) 00_prereq_check.py
   - Python version
   - required packages
   - credential resolution source
   - live probe
2) 01_seed_lab.py
   - create/use catalog + schema for lab
   - create baseline Delta tables
   - seed realistic DE sample data
3) 99_reset_lab.py
   - safe reset of created lab objects only
All must be rerunnable.

C) Core concept coverage (must include these)
1) SQL foundations in Databricks SQL
   - joins, group by/having, subqueries
2) CTE + windowing
   - recursive alternatives if applicable
   - row_number, rank, dense_rank, lag/lead, running totals, frames
3) Delta Lake essentials
   - ACID behavior
   - schema enforcement/evolution
   - Time Travel
   - OPTIMIZE
   - Z-ORDER
4) DE patterns
   - deduplication
   - MERGE upsert
   - SCD Type 2
   - incremental loads
   - late-arriving events
5) Performance
   - explain plan interpretation
   - partitioning strategy
   - file size and compaction patterns
6) Governance/Security basics
   - Unity Catalog namespace usage
   - role/grant examples (safe/read-only style where needed)
7) Data quality
   - null, duplicate, key integrity checks
   - assertion-style test outputs
8) Interview drills
   - concise scenario questions with runnable model answers
9) Mini capstone
   - bronze -> silver -> gold flow using Delta tables
   - includes one failure simulation + recovery step

D) Cross-engine bridge requirement (MANDATORY)
Create CROSS_ENGINE_SQL_MAP.md mapping equivalent patterns:
- PostgreSQL -> Databricks SQL -> Snowflake SQL
Required sections:
- CTE and windowing equivalence
- Upsert/MERGE and SCD2
- Transactions and isolation caveats
- Explain/profile tooling equivalence
- Null and type behavior gotchas
Each mapping must link to at least one runnable nugget file.

RUNNER + VALIDATION (MANDATORY)
Implement:
D:\StudyBook\tracks\08_databases\micro_nuggets\databricks_bridge\run_all_databricks_bridge_nuggets.py
Requirements:
- deterministic script order
- one-line PASS/FAIL per script
- summary totals
- per-script timeout
- Windows-safe output encoding
- robust subprocess output handling

Must run full validation before delivery:
1) prereq check
2) setup/seed
3) full runner
4) reset check (optional but preferred)

If any test fails:
- fix
- rerun
- report final green state or exact external blocker evidence

BEGINNER EXECUTION GUIDE (MANDATORY IN README)
Provide exact copy/paste command blocks:
1) navigate folder
2) run prereq check
3) run setup/seed
4) run one nugget
5) run all nuggets
6) reset lab
7) common errors + direct fixes

INTERVIEW PACKAGE (MANDATORY)
In DATABRICKS_BRIDGE_SPEEDY_STORY_AND_INTERVIEW.md include:
- conceptual story from beginner to DE practitioner
- 30+ interview Q&A (short and strong answers)
- section explicitly on “PostgreSQL concept -> Databricks implementation”

GLOSSARY (MANDATORY)
DATABRICKS_BRIDGE_GLOSSARY.md:
- plain-English definitions
- include terms like: Delta log, OPTIMIZE, Z-ORDER, Unity Catalog, ACID, snapshot isolation, schema evolution, MERGE semantics
- each definition links to one nugget where used

QUALITY BAR
- No placeholders like TODO/LATER.
- No hardcoded absolute machine paths.
- No fake success claims.
- All outputs and docs consistent with actual code behavior.
- Keep files ASCII unless existing file requires otherwise.

DELIVERY FORMAT
At completion, provide:
1) full file tree created
2) what each module covers
3) commands executed for validation
4) pass/fail table with totals
5) known constraints/blockers (if any)
6) next recommended phase (only after successful delivery)

WORK STYLE
- Make reasonable assumptions and proceed.
- Do not pause for optional clarifications.
- Maintain momentum.
- Finish end-to-end with tested artifacts.
```
