You are generating a self-directed Data Engineering interview-prep tutorial.

The output must be COMPLETE, FULLY RUNNABLE, and TEACHABLE. Do not create placeholders, TODOs, ellipses, `pass`, or intentionally incomplete code. Generate one file at a time and wait for the user to say "next".

All files must be written as if they will be saved under:
D:\Workarea\StudyBook\tutorials\17_postgresql\

TOPIC: PostgreSQL for Data Engineers
SLUG: 17_postgresql
PRIORITY: Capital One MUST
INFRASTRUCTURE: Docker Postgres or existing postgresql://studybook:studybook@localhost:5432/studybook; psycopg3

============================================================
CODING STANDARDS — MANDATORY
============================================================

- Python 3.11+ compatible.
- Use type hints on every function.
- Use f-strings.
- Prefer small, testable functions.
- Avoid hidden global state except clear constants.
- No notebooks.
- No TODO, no pass, no placeholder implementation.
- Every generated file must be complete and runnable.
- Keep examples realistic for Data Engineering interviews.
- Use deterministic seeds for generated data.
- Do not require paid/cloud resources in unit tests unless explicitly called out.


============================================================
README REQUIREMENTS — MANDATORY
============================================================

Generate TWO README files for every topic.

1. Main `README.md` at the topic root.

The main README must be professional, interview-oriented, and include:

- `# <Topic Name>`
- `## What This Covers`
- `## Why This Matters in Interviews`
- `## Key Concepts`
- `## Hands-On Walkthrough`
  - Explain each generated tutorial file in order.
  - Explain what the learner should run and what output means.
- `## Common Interview Questions`
  - Include 8 to 12 practical interview questions.
  - Include strong answer guidance after each question.
- `## Deep Dive Talking Points`
  - Senior-level details, tradeoffs, edge cases, and production concerns.
- `## How This Shows Up in Production`
- `## Commands`
  - Include exact PowerShell commands to install dependencies and run tests.
- `## What To Say In An Interview`
  - Include a 60-90 second spoken explanation.

2. Capstone `capstone/README.md`.

The capstone README must be system-design and interview-story oriented, and include:

- `# Capstone: <Name>`
- `## Scenario`
- `## Architecture Overview`
  - Describe the architecture in words.
- `## Data Flow`
- `## Design Decisions`
- `## Tradeoffs`
- `## Scaling Considerations`
- `## Failure Modes`
- `## Security / Governance Notes`
- `## Interview Questions`
  - Include 8 to 12 scenario-based questions with answer guidance.
- `## How To Explain This Capstone In An Interview`
  - Include a step-by-step narrative.

The README files are not optional. Generate them before the capstone code if requested.


============================================================
TEACHING CODE REQUIREMENTS — MANDATORY
============================================================

Every Python file must include:

1. A file header docstring:

```
"""
FILE: <filename>
TOPIC: <topic>
PURPOSE: <what this file teaches>
COVERS: <concept list>
INTERVIEW FOCUS: <what to say in an interview>
"""
```

2. Teachable comments.

Comments must explain WHY, not just WHAT. Include comments like:

```
# INTERVIEW TIP:
# In an interview, emphasize that this step protects downstream consumers
# from schema drift and silent data quality failures.
```

3. Learning-oriented print statements.

Each script should print:
- What it is doing
- Why the step matters
- What interview concept the learner should remember

4. `main()` function.

Every tutorial file must have a runnable `main()` and:

```
if __name__ == "__main__":
    main()
```

5. Tests must validate business behavior, not just file existence.

Use deterministic sample data and exact assertions where possible.

============================================================
TUTORIAL FILES TO GENERATE
============================================================
Generate these files in order. For each file, include the exact functions listed. You may add helper functions only if they are useful and fully implemented.

===== FILE 01: 01_connections_and_schema.py =====
PURPOSE: Connect to Postgres and create schemas/tables idempotently.
COVERS: psycopg3, transactions, DDL, connection strings

EXACT FUNCTION SIGNATURES:
    def get_connection(dsn: str):
    def create_schema(conn, schema_name: str) -> None:
    def create_transactions_table(conn, schema_name: str) -> None:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 02: 02_bulk_load_copy.py =====
PURPOSE: Bulk load transaction records efficiently.
COVERS: COPY, batching, CSV staging, data types

EXACT FUNCTION SIGNATURES:
    def generate_transactions(row_count: int, seed: int = 42) -> list[dict]:
    def write_transactions_csv(rows: list[dict], path: str) -> str:
    def bulk_load_transactions(conn, schema_name: str, csv_path: str) -> int:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 03: 03_indexes_and_query_plans.py =====
PURPOSE: Create indexes and inspect query plans.
COVERS: B-tree, partial indexes, EXPLAIN ANALYZE

EXACT FUNCTION SIGNATURES:
    def create_transaction_indexes(conn, schema_name: str) -> None:
    def run_explain_analyze(conn, sql: str) -> list[str]:
    def summarize_plan(plan_lines: list[str]) -> dict[str, bool]:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 04: 04_upserts_and_deduplication.py =====
PURPOSE: Implement idempotent upsert patterns.
COVERS: ON CONFLICT, primary keys, staging tables

EXACT FUNCTION SIGNATURES:
    def create_staging_table(conn, schema_name: str) -> None:
    def upsert_transactions(conn, schema_name: str) -> int:
    def count_duplicate_transaction_ids(conn, schema_name: str) -> int:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 05: 05_partitioning_and_maintenance.py =====
PURPOSE: Demonstrate partitioning and maintenance concepts.
COVERS: range partitioning, vacuum/analyze, retention

EXACT FUNCTION SIGNATURES:
    def build_month_partition_sql(schema_name: str, month: str) -> str:
    def create_partitioned_events_table(conn, schema_name: str) -> None:
    def build_retention_delete_sql(schema_name: str, cutoff_date: str) -> str:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 06: README.md =====
Generate the main tutorial README using the mandatory README requirements above.

============================================================
CAPSTONE REQUIREMENTS
============================================================
CAPSTONE SCENARIO: Build a production-style relational ingestion and analytics workflow for transaction data.

--- capstone/brief.md ---
Write a concise business scenario, learner tasks, expected deliverables, and success criteria.

--- capstone/README.md ---
Generate the capstone README using the mandatory capstone README requirements above.

--- capstone/transaction_warehouse.py ---
EXACT FUNCTION SIGNATURES:
    def initialize_schema(conn, schema_name: str) -> None:
    def load_daily_transactions(conn, schema_name: str, rows: list[dict]) -> int:
    def calculate_daily_settlement(conn, schema_name: str) -> list[dict]:
    def run_quality_checks(conn, schema_name: str) -> dict[str, bool]:
REQUIREMENTS:
- Must be runnable and importable.
- Must include interview-focused comments.
- Must use deterministic inputs for local testing.

--- capstone/test_capstone.py ---
Create pytest tests with these exact business expectations:
- assert schema tables are created
- assert bulk load inserts expected row count
- assert duplicate transaction ids are removed
- assert daily settlement totals match fixture values
- assert quality checks all pass

Additional testing requirements:
- Use deterministic fixtures.
- Assert exact values where possible.
- Test edge cases and failure modes.
- Tests must run with `pytest capstone/test_capstone.py -v` from the topic folder unless the topic README specifies otherwise.

============================================================
GENERATION INSTRUCTIONS
============================================================

Generate ONE file at a time.

When first given this prompt, acknowledge the topic and wait.
When the user says `generate file 01`, generate only FILE 01.
When the user says `next`, generate the next file.
After tutorial files, generate README.md.
Then generate capstone/brief.md, capstone/README.md, capstone code files, and capstone/test_capstone.py.

Do not skip README files.
Do not combine multiple files unless explicitly asked.
Do not use placeholders.
Do not say "left as an exercise".
Do not omit imports.
