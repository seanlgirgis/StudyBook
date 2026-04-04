"""
06_interview_drills/01_interview_drills.py — Top 15 dbt Interview Q&A.

Prints 15 interview-ready Q&A covering all major dbt topics.
Use this as a rapid review before interviews.

Topics:
  - dbt architecture and DAG
  - ref() vs source()
  - Materialization tradeoffs
  - Incremental on_schema_change options
  - Snapshots vs MERGE SCD2
  - Testing strategy and CI/CD
  - Artifacts and lineage
  - Performance and cost controls
  - Macros and Jinja
  - dbt Cloud vs Core

Run:
    python 06_interview_drills/01_interview_drills.py
"""
from __future__ import annotations

import sys

# UTF-8 stdout for Windows console (cp1252 doesn't support arrows/special chars)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

QA = [
    (
        "Q1. What is dbt and what problem does it solve?",
        """dbt (data build tool) is a transformation framework that turns raw SQL SELECT
statements into a fully-orchestrated, tested, documented data pipeline.
It solves the "raw SQL chaos" problem: without dbt, analysts run ad-hoc scripts
with no dependency management, no tests, no documentation, and no version control
integration. dbt brings software engineering practices (version control, CI/CD,
testing, modular code) to analytics engineering."""
    ),
    (
        "Q2. What is the dbt DAG and why does it matter?",
        """The DAG (Directed Acyclic Graph) is the execution dependency graph dbt builds
from ref() calls. Each ref('model_name') in a SQL file creates a directed edge
from the upstream model to the current model. dbt performs a topological sort
so that models run in the correct order — no manual orchestration needed.
The DAG is also the foundation for impact analysis (what breaks if I change X?)
and for state-based CI/CD (what changed vs last run?)."""
    ),
    (
        "Q3. What is the difference between ref() and source()?",
        """ref('model_name') references another dbt MODEL — it generates the correct
schema-qualified name at runtime (dev vs prod) and creates a DAG dependency.
source('schema', 'table') references an EXTERNAL/RAW table not owned by dbt.
Rule of thumb: use source() ONLY in the staging layer; use ref() everywhere else.
source() also enables source freshness checks (warn/error if data is stale)."""
    ),
    (
        "Q4. When would you choose incremental over table materialization?",
        """Use incremental when: (1) the table is large (millions+ rows), (2) data is
append-only or has a clear watermark column (event_ts, created_at), and
(3) rebuilding from scratch each run is too expensive. Use table when data
is small enough to rebuild cheaply, or when historical corrections happen
frequently (incremental won't reprocess old rows by default). Incremental
saves cost; table guarantees correctness. When in doubt, start with table."""
    ),
    (
        "Q5. What are the four on_schema_change options for incremental models?",
        """"ignore" (default): new columns in model SQL are silently dropped from inserts.
"fail": dbt errors if the model SQL adds/removes columns — forces explicit migration.
"append_new_columns": new columns added to target table; old rows get NULL for them.
"sync_all_columns": adds new AND removes dropped columns — destructive, use carefully.
In practice: "append_new_columns" is safest for additive schema changes in prod."""
    ),
    (
        "Q6. What is a dbt snapshot and how does it differ from a SCD2 MERGE?",
        """A dbt snapshot automatically implements SCD Type 2 — it adds dbt_valid_from,
dbt_valid_to, dbt_scd_id, and dbt_updated_at columns to track historical changes.
strategy='check' detects changes by comparing column values; strategy='timestamp'
uses an updated_at column. vs MERGE SCD2: with raw SQL MERGE you write and maintain
complex MATCHED/NOT MATCHED logic; dbt handles that for you and integrates with
the DAG, docs, and tests. Snapshots are idempotent; manual MERGEs often aren't."""
    ),
    (
        "Q7. What is the difference between dbt run, dbt test, and dbt build?",
        """dbt run: executes model SQL (creates views/tables/incremental updates).
dbt test: runs all generic and singular tests; returns non-zero if any fail.
dbt build: runs seed + run + test + snapshot in DAG order. Crucially, build
tests EACH node before moving to its downstream dependents — if stg_customers
tests fail, fct_orders won't run. In CI/CD, prefer dbt build for safety;
use dbt run during development for speed."""
    ),
    (
        "Q8. What are the four built-in generic tests in dbt?",
        """not_null: asserts a column contains no NULL values.
unique: asserts all values in a column are distinct.
relationships: asserts a column's values all exist in a referenced table (FK check).
accepted_values: asserts all values fall within a defined set (enum check).
These are defined in schema.yml and dbt generates the SQL automatically.
Each test is just a SELECT — it FAILS if the SELECT returns any rows."""
    ),
    (
        "Q9. What is a singular test and when do you use it?",
        """A singular test is a raw SQL file in the tests/ directory that selects VIOLATION
rows. If the query returns any rows, the test fails. Use singular tests for
business-logic assertions that generic tests can't express: "no payment amount
exceeds the order total", "no user has two active subscriptions", "no order date
is in the future". They use ref() so they work across dev/prod schemas.
Generic tests scale across all models; singular tests express one-off rules."""
    ),
    (
        "Q10. How does dbt handle dev vs prod environments?",
        """Profiles.yml defines multiple targets (dev, prod). In dev, dbt appends your
username to the schema: schema=dbt_lab → schema=dbt_lab_your_name, preventing
dev runs from overwriting prod tables. ref() resolves to the current target's
schema automatically. For CI/CD, set --target prod to build into prod schemas.
Use environment variables ({{ env_var('DBT_TARGET') }}) for dynamic target selection.
dbt Cloud manages target selection per job automatically."""
    ),
    (
        "Q11. What is manifest.json and why is it critical for CI/CD?",
        """manifest.json is a JSON artifact generated by every dbt compile/run/build command.
It contains every node (model, test, seed, snapshot, macro) with its compiled SQL,
configuration, tags, and DAG dependencies (depends_on.nodes). CI/CD tools use it
to compare "what changed" between runs (state:modified). Observability tools (dbt
Cloud, elementary, Lightdash, re_data) read manifest.json to build lineage graphs.
Always store manifest.json as a CI artifact for the next run's state comparison."""
    ),
    (
        "Q12. Explain state:modified and when to use it in CI/CD.",
        """state:modified compares the current manifest.json to a "previous" one (typically
the last successful prod run's artifact). Models whose SQL or config changed are
selected. dbt build --select state:modified+ runs changed models AND all their
downstream dependents. This is the production CI/CD pattern: instead of rebuilding
200 models, only rebuild the 3 that changed + their 5 dependents. Reduces CI time
from 2 hours to 10 minutes on large projects. Requires storing manifest.json
as an artifact after each successful prod run."""
    ),
    (
        "Q13. What is a dbt macro and when would you create one?",
        """A macro is a Jinja2 function defined in the macros/ directory and callable from
any model, test, or other macro. Use macros for: repeated SQL patterns (cents_to_dollars,
generate_surrogate_key), cross-database compatibility (date_trunc works differently
in Snowflake vs BigQuery), and dynamic SQL generation. Built-in macros: ref(),
source(), this (current model's relation), is_incremental(). Third-party macros from
packages like dbt-utils extend the library. Macros are compiled at parse time — they
must be valid Jinja2."""
    ),
    (
        "Q14. What are the pros and cons of dbt Cloud vs dbt Core?",
        """dbt Core (open source): free, runs anywhere (local, CI/CD, any Python env),
full feature set. Cons: you manage orchestration (Airflow, Prefect), no built-in
IDE, no managed job scheduling, no native state management UI.
dbt Cloud: managed SaaS, built-in IDE, job scheduler, CI integration, state
management, SSO, audit logs, Explorer (lineage UI). Cons: paid tier for
most features, vendor lock-in for orchestration. Most small teams start with
Core + GitHub Actions; large enterprise teams use Cloud for governance + IDE."""
    ),
    (
        "Q15. How would you optimize a dbt project that takes 4 hours to run?",
        """(1) Use state:modified+ in CI to only rebuild changed models (~80% time reduction).
(2) Identify the slowest models via run_results.json execution_time; optimize their SQL.
(3) Convert large table materializations to incremental where append semantics apply.
(4) Increase threads in profiles.yml (threads: 8+) for parallel model execution.
(5) Use defer in dev to avoid rebuilding unchanged upstream models.
(6) Partition large incremental models by date (warehouse-specific config).
(7) Remove unused columns from wide models to reduce bytes scanned.
(8) Use dbt build --select tag:daily only for daily models; run hourly models hourly."""
    ),
]


def main() -> int:
    print("=" * 70)
    print("  dbt Interview Drills — Top 15 Q&A")
    print("=" * 70)
    print()
    print("  Use this as a rapid review. Each answer is 2-4 sentences,")
    print("  interview-ready. Read aloud for best retention.")
    print()

    for i, (question, answer) in enumerate(QA, 1):
        print("-" * 70)
        print(f"\n  {question}\n")
        # Indent each answer line for readability
        for line in answer.strip().splitlines():
            print(f"  {line}")
        print()

    print("-" * 70)
    print(f"\n  Total: {len(QA)} questions covered")
    print()
    print("  STUDY TIP: For each answer, practice saying it out loud in 30 seconds.")
    print("  Then check: did you cover the key terms? The tradeoffs? An example?")
    print()
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
