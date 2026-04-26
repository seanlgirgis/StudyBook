You are generating a self-directed Data Engineering interview-prep tutorial.

The output must be COMPLETE, FULLY RUNNABLE, and TEACHABLE. Do not create placeholders, TODOs, ellipses, `pass`, or intentionally incomplete code. Generate one file at a time and wait for the user to say "next".

All files must be written as if they will be saved under:
D:\Workarea\StudyBook\tutorials\41_snowflake_pyiceberg\

TOPIC: Snowflake and PyIceberg Integration Concepts
SLUG: 41_snowflake_pyiceberg
PRIORITY: Advanced Cloud SHOULD
INFRASTRUCTURE: Local SQL/PyIceberg concepts; no Snowflake account required by tests

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

===== FILE 01: 01_snowflake_external_tables.py =====
PURPOSE: Generate Snowflake external table SQL.
COVERS: stages, file formats, external tables

EXACT FUNCTION SIGNATURES:
    def create_stage_sql(stage_name: str, url: str, storage_integration: str) -> str:
    def create_file_format_sql(format_name: str) -> str:
    def create_external_table_sql(table_name: str, stage_name: str) -> str:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 02: 02_snowflake_iceberg_tables.py =====
PURPOSE: Teach Snowflake-managed Iceberg concepts.
COVERS: catalog integration, external volumes, Iceberg table SQL

EXACT FUNCTION SIGNATURES:
    def create_external_volume_sql(volume_name: str, storage_location: str) -> str:
    def create_catalog_integration_sql(integration_name: str) -> str:
    def create_iceberg_table_sql(table_name: str, external_volume: str, catalog: str) -> str:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 03: 03_pyiceberg_catalog_basics.py =====
PURPOSE: Build local PyIceberg catalog config examples.
COVERS: catalogs, namespaces, table identifiers

EXACT FUNCTION SIGNATURES:
    def build_sql_catalog_config(uri: str, warehouse: str) -> dict:
    def table_identifier(namespace: str, table_name: str) -> str:
    def explain_catalog_choice(catalog_type: str) -> str:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 04: 04_schema_evolution_interop.py =====
PURPOSE: Explain schema evolution between systems.
COVERS: add columns, compatibility, contracts

EXACT FUNCTION SIGNATURES:
    def build_schema_change_plan(old_columns: list[str], new_columns: list[str]) -> dict[str, list[str]]:
    def snowflake_add_column_sql(table_name: str, column_name: str, data_type: str) -> str:
    def validate_backward_compatible_change(plan: dict[str, list[str]]) -> bool:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 05: 05_governance_cost_tradeoffs.py =====
PURPOSE: Compare warehouse and lakehouse tradeoffs.
COVERS: governance, cost, performance, ownership boundaries

EXACT FUNCTION SIGNATURES:
    def compare_query_engine_tradeoffs() -> pd.DataFrame:
    def recommend_engine(use_case: str) -> str:
    def estimate_storage_duplication_risk(copies: int, tb: float) -> str:

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
CAPSTONE SCENARIO: Design interoperability between Snowflake analytics and Iceberg-style lakehouse tables.

--- capstone/brief.md ---
Write a concise business scenario, learner tasks, expected deliverables, and success criteria.

--- capstone/README.md ---
Generate the capstone README using the mandatory capstone README requirements above.

--- capstone/snowflake_iceberg_design.py ---
EXACT FUNCTION SIGNATURES:
    def build_interop_sql_assets(config: dict) -> dict[str, str]:
    def build_pyiceberg_config(config: dict) -> dict:
    def validate_interop_design(sql_assets: dict[str, str], iceberg_config: dict) -> dict[str, bool]:
    def produce_architecture_summary(config: dict) -> list[str]:
REQUIREMENTS:
- Must be runnable and importable.
- Must include interview-focused comments.
- Must use deterministic inputs for local testing.

--- capstone/test_capstone.py ---
Create pytest tests with these exact business expectations:
- assert stage SQL contains CREATE STAGE
- assert Iceberg SQL contains EXTERNAL_VOLUME
- assert catalog config has uri and warehouse
- assert backward-compatible add column passes
- assert design validation passes

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
