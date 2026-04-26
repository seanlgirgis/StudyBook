You are generating a self-directed Data Engineering interview-prep tutorial.

The output must be COMPLETE, FULLY RUNNABLE, and TEACHABLE. Do not create placeholders, TODOs, ellipses, `pass`, or intentionally incomplete code. Generate one file at a time and wait for the user to say "next".

All files must be written as if they will be saved under:
D:\Workarea\StudyBook\tutorials\22_aws_athena\

TOPIC: AWS Athena for Data Engineers
SLUG: 22_aws_athena
PRIORITY: Capital One SHOULD
INFRASTRUCTURE: AWS concepts + local SQL generation; optional boto3; no live queries required by tests

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

===== FILE 01: 01_external_table_ddl.py =====
PURPOSE: Create Athena external table DDL.
COVERS: Glue catalog, external tables, SerDe, S3 locations

EXACT FUNCTION SIGNATURES:
    def build_parquet_external_table_ddl(database: str, table: str, s3_location: str) -> str:
    def build_json_external_table_ddl(database: str, table: str, s3_location: str) -> str:
    def validate_s3_location(s3_location: str) -> bool:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 02: 02_partitioning_and_projection.py =====
PURPOSE: Teach partitions and partition projection.
COVERS: partition pruning, projection, MSCK REPAIR tradeoffs

EXACT FUNCTION SIGNATURES:
    def build_partitioned_table_ddl(database: str, table: str, s3_location: str) -> str:
    def build_partition_projection_properties(start_date: str) -> dict[str, str]:
    def build_msck_repair_sql(database: str, table: str) -> str:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 03: 03_query_cost_controls.py =====
PURPOSE: Estimate Athena scan cost and teach cost controls.
COVERS: bytes scanned, compression, columnar formats

EXACT FUNCTION SIGNATURES:
    def estimate_athena_query_cost(bytes_scanned: int, price_per_tb: float = 5.0) -> float:
    def recommend_file_format(row_oriented: bool, nested_data: bool) -> str:
    def build_selective_query(table: str, columns: list[str], partition_filter: str) -> str:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 04: 04_ctas_and_views.py =====
PURPOSE: Use CTAS and views for curated datasets.
COVERS: CTAS, materialization, views, result location

EXACT FUNCTION SIGNATURES:
    def build_ctas_parquet_sql(source_table: str, target_table: str, s3_location: str) -> str:
    def build_view_sql(view_name: str, source_table: str) -> str:
    def validate_ctas_sql(sql: str) -> bool:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 05: 05_boto3_athena_runner.py =====
PURPOSE: Run Athena queries safely when env vars are configured.
COVERS: boto3 start_query_execution, polling, safe skip

EXACT FUNCTION SIGNATURES:
    def start_athena_query(query: str, database: str, output_location: str, profile_name: str | None = None) -> str:
    def poll_query_status(query_execution_id: str, profile_name: str | None = None) -> str:
    def format_query_results(rows: list[dict]) -> list[dict]:

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
CAPSTONE SCENARIO: Build an Athena-based lakehouse query layer over partitioned S3 data.

--- capstone/brief.md ---
Write a concise business scenario, learner tasks, expected deliverables, and success criteria.

--- capstone/README.md ---
Generate the capstone README using the mandatory capstone README requirements above.

--- capstone/athena_lakehouse.py ---
EXACT FUNCTION SIGNATURES:
    def build_lakehouse_ddl(database: str, bucket: str) -> list[str]:
    def build_cost_optimized_queries(database: str) -> dict[str, str]:
    def validate_lakehouse_sql(sql_statements: list[str]) -> dict[str, bool]:
    def estimate_query_suite_cost(scan_bytes_by_query: dict[str, int]) -> dict[str, float]:
REQUIREMENTS:
- Must be runnable and importable.
- Must include interview-focused comments.
- Must use deterministic inputs for local testing.

--- capstone/test_capstone.py ---
Create pytest tests with these exact business expectations:
- assert table DDL contains EXTERNAL TABLE and STORED AS PARQUET
- assert partition projection properties include projection.enabled
- assert cost estimate for 1 TB equals 5.0
- assert CTAS writes PARQUET
- assert capstone validation passes

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
