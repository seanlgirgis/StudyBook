# PostgreSQL Micro-Nuggets Production Execution Master Prompt

Use this prompt with external code agents to implement a complete, tested PostgreSQL micro-nuggets lane for Data Engineering and interview preparation.

```text
You are a senior code agent working in this repo: D:\StudyBook

MISSION
Build a production-grade PostgreSQL micro-nuggets learning system for Data Engineering and interview prep.
This must be runnable by a beginner on Windows PowerShell with minimal confusion.

PRIMARY TARGET LOCATION
Create everything under:
D:\StudyBook\tracks\08_databases\micro_nuggets\postgresql

MANDATORY PRE-WORK (DO THIS FIRST)
1) Discover and reuse existing PostgreSQL connection proof(s) already in repo:
   - Search under: D:\StudyBook\poc\connection_proofs\python
   - Reuse existing connection conventions, env loading, host/port/user/password/db behavior.
2) Add a preparatory setup stage that can be run safely multiple times:
   - Create database objects required for all nuggets.
   - Populate realistic sample data for DE scenarios.
   - Must be idempotent (re-runnable without breaking state).
3) Build and run automated verification before delivery.
   - Do not claim done without executing tests/runs and sharing results.

NON-NEGOTIABLE REQUIREMENTS
- Production-grade code quality.
- Clear error handling with actionable messages.
- Idempotent setup/reset scripts.
- Every nugget must print meaningful success/failure output.
- Windows-first instructions (PowerShell commands).
- No secrets hardcoded; use existing env/secret flow in this repo.
- Keep files ASCII unless existing file requires otherwise.
- Include teachable comments for concept-heavy sections.
- Beginner-proof execution steps (assume user can follow commands but not debug internals).

SCOPE TO IMPLEMENT

A) Folder structure
D:\StudyBook\tracks\08_databases\micro_nuggets\postgresql\
  00_setup\
  01_sql_core\
  02_cte_and_windowing\
  03_data_modeling\
  04_de_patterns\
  05_performance_tuning\
  06_transactions_and_concurrency\
  07_data_quality_and_testing\
  08_interview_drills\
  09_mini_capstone\
  _pg_connect.py
  run_all_postgresql_nuggets.py
  POSTGRESQL_SPEEDY_STORY_AND_INTERVIEW.md
  POSTGRESQL_GLOSSARY.md
  README.md

B) Preparatory stage (must be implemented and tested)
- Create script(s) in 00_setup to:
  1. validate connectivity
  2. create schemas/tables/indexes
  3. seed realistic data (events/orders/customers/products/etc.)
  4. provide reset script to clean/reseed lab
- Add explicit "expected output" in comments/docs.

C) Required concept coverage
Must include runnable nuggets for:
- SQL foundations: joins, group by, subqueries, set ops
- CTEs: non-recursive + recursive
- Window functions: row_number, rank/dense_rank, lag/lead, running totals, partitions/frames
- Data modeling: keys, constraints, normalization/denormalization tradeoffs
- DE patterns:
  - deduplication
  - incremental loads
  - upsert (INSERT ... ON CONFLICT)
  - SCD Type 2 pattern
  - late-arriving data handling
- Performance:
  - EXPLAIN / EXPLAIN ANALYZE
  - index strategies (btree/composite/partial)
  - anti-patterns and fixes
  - VACUUM/ANALYZE basics
- Concurrency:
  - transactions
  - isolation levels
  - locks
  - deadlock demo + mitigation
- Data quality:
  - checks/assertions
  - null/duplicate/key integrity tests
- Mini capstone:
  - bronze -> silver -> gold style workflow using PostgreSQL tables/views/materialized views

D) Interview package (mandatory)
- Add interview Q&A with concise, strong answers.
- Include practical SQL interview prompts and model solutions.
- Cover CTE/windowing, indexing, ACID, isolation, deadlocks, upsert/SCD2, query optimization.

E) Story + glossary (mandatory)
- POSTGRESQL_SPEEDY_STORY_AND_INTERVIEW.md:
  - coherent learning narrative from beginner to DE-ready
  - where each nugget fits in real-world pipelines
- POSTGRESQL_GLOSSARY.md:
  - plain-English definitions for every key term used
  - include cross-links to nugget scripts where term is demonstrated

RUNNER + VALIDATION (MANDATORY)
1) Implement:
   D:\StudyBook\tracks\08_databases\micro_nuggets\postgresql\run_all_postgresql_nuggets.py
   - One-line PASS/FAIL per script
   - Summary totals
   - Safe console output for Windows encoding
   - Timeout handling
2) Run full validation yourself before delivery:
   - setup scripts
   - all nuggets through runner
3) Provide a final validation report with:
   - total scripts
   - passed/failed
   - exact failed scripts (if any)
   - fixes applied
4) If any test fails, fix and rerun until green (or clearly explain external blocker with evidence).

BEGINNER EXECUTION GUIDE (MANDATORY IN README)
Provide exact copy/paste commands in order:
1) how to open correct folder
2) how to run setup
3) how to run single nugget
4) how to run all nuggets
5) how to reset lab
6) common errors and exact fixes

QUALITY BAR
- Deterministic outputs where possible.
- No vague TODO placeholders.
- No "concept only" files without runnable code.
- No claims of success without command output evidence.

DELIVERY FORMAT
At completion, provide:
1) File tree created
2) What was implemented by module
3) Validation command list actually run
4) Validation results summary
5) Any residual risks/blockers
6) Suggested next phase (only after everything above is complete)

WORK STYLE
- Make reasonable assumptions and proceed.
- Do not stop for optional clarifications.
- Keep momentum and deliver fully working artifacts.
```
