You are generating a self-directed Data Engineering interview-prep tutorial.

The output must be COMPLETE, FULLY RUNNABLE, and TEACHABLE. Do not create placeholders, TODOs, ellipses, `pass`, or intentionally incomplete code. Generate one file at a time and wait for the user to say "next".

All files must be written as if they will be saved under:
D:\Workarea\StudyBook\tutorials\21_aws_redshift\

TOPIC: AWS Redshift for Data Engineers
SLUG: 21_aws_redshift
PRIORITY: Capital One SHOULD
INFRASTRUCTURE: AWS concepts + local SQL generation; no live cluster required by tests

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
AWS CLEANUP RULES — MANDATORY FOR THIS TOPIC
============================================================

For any file that creates AWS resources:

- Use `AWS_PROFILE = os.getenv("AWS_PROFILE", "study")`
- Use `AWS_REGION = os.getenv("AWS_REGION", "us-east-1")`
- Use unique resource names with a short uuid suffix.
- Print a visible warning immediately after creating billable resources:
  `⚠️ COST WARNING: <resource> is billable until deleted.`
- Wrap resource creation and demo logic in `try/finally`.
- Call cleanup from `finally`.
- Cleanup must be idempotent and tolerate already-deleted resources.
- Print exactly:
  `✅ Cleanup complete. No ongoing charges.`
  as the last cleanup message.
- Optional AWS integrations must be gated by environment variables and must not crash when unset.
- Capstone tests should not require live AWS unless explicitly stated; prefer local builders, policy JSON, or mocked behavior.

============================================================
TUTORIAL FILES TO GENERATE
============================================================
Generate these files in order. For each file, include the exact functions listed. You may add helper functions only if they are useful and fully implemented.

===== FILE 01: 01_redshift_table_design.py =====
PURPOSE: Generate Redshift DDL for fact/dimension tables.
COVERS: dist keys, sort keys, encodings, star schema

EXACT FUNCTION SIGNATURES:
    def build_fact_transactions_ddl(schema_name: str) -> str:
    def build_dim_customer_ddl(schema_name: str) -> str:
    def explain_distribution_choice(table_name: str, dist_key: str) -> str:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 02: 02_copy_from_s3.py =====
PURPOSE: Build COPY commands and explain load options.
COVERS: COPY, IAM role, manifests, compression

EXACT FUNCTION SIGNATURES:
    def build_copy_command(schema_name: str, table_name: str, s3_path: str, iam_role_arn: str) -> str:
    def build_manifest_file(entries: list[str]) -> dict:
    def validate_copy_options(sql: str) -> bool:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 03: 03_merge_upsert_patterns.py =====
PURPOSE: Teach staging + merge patterns.
COVERS: MERGE, staging tables, idempotency

EXACT FUNCTION SIGNATURES:
    def build_staging_table_ddl(schema_name: str) -> str:
    def build_merge_sql(schema_name: str) -> str:
    def build_dedup_sql(schema_name: str, key_column: str, timestamp_column: str) -> str:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 04: 04_query_performance.py =====
PURPOSE: Generate optimization diagnostics.
COVERS: EXPLAIN, analyze, vacuum, sort keys

EXACT FUNCTION SIGNATURES:
    def build_analyze_command(schema_name: str, table_name: str) -> str:
    def build_vacuum_command(schema_name: str, table_name: str) -> str:
    def diagnose_query_plan(plan_text: str) -> dict[str, bool]:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 05: 05_workload_management_and_cost.py =====
PURPOSE: Explain WLM, concurrency scaling, and cost guardrails.
COVERS: WLM, queues, RA3, Spectrum tradeoffs

EXACT FUNCTION SIGNATURES:
    def recommend_workload_queue(query_type: str) -> str:
    def estimate_scan_cost_warning(table_size_gb: float, selectivity: float) -> str:
    def build_unload_command(query: str, s3_path: str, iam_role_arn: str) -> str:

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
CAPSTONE SCENARIO: Design a Redshift loading and optimization workflow for analytics tables.

--- capstone/brief.md ---
Write a concise business scenario, learner tasks, expected deliverables, and success criteria.

--- capstone/README.md ---
Generate the capstone README using the mandatory capstone README requirements above.

--- capstone/redshift_load_plan.py ---
EXACT FUNCTION SIGNATURES:
    def build_warehouse_ddl(schema_name: str) -> dict[str, str]:
    def build_daily_load_sql(schema_name: str, s3_path: str, iam_role_arn: str) -> list[str]:
    def build_maintenance_sql(schema_name: str) -> list[str]:
    def validate_load_plan(sql_statements: list[str]) -> dict[str, bool]:
REQUIREMENTS:
- Must be runnable and importable.
- Must include interview-focused comments.
- Must use deterministic inputs for local testing.

--- capstone/test_capstone.py ---
Create pytest tests with these exact business expectations:
- assert COPY command includes IAM_ROLE and FORMAT AS PARQUET
- assert fact DDL includes DISTKEY and SORTKEY
- assert MERGE SQL has matched and not matched branches
- assert maintenance SQL includes ANALYZE
- assert validation rejects wildcard insecure role placeholder

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
