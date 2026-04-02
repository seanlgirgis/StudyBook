SAVE AS: cicd_data_nuggets.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets.

TASK: Generate 12 CI/CD for data gotcha nuggets. Cover: flaky data tests caused by non-deterministic row ordering (ORDER BY missing in test query), GE expectations silently passing on empty datasets (expect_table_row_count_to_be_between with min=0), dbt incremental model CI always runs in full-refresh mode (state:modified+ doesn't catch config-only changes), GE checkpoint performance degrading on large tables (profiling entire table instead of a sample), GitHub Actions secrets not available in fork PRs (security restriction breaks contributor workflows), dbt test failures not blocking CD when --defer flag is misused, expectations drift after schema evolution (suite not updated when new columns added), blue-green swap leaving stale connections on the old schema (connection pooling not respecting alias change), secrets hardcoded in workflow YAML showing in git blame, dbt singular tests that pass locally but fail in CI due to search_path differences, GE Data Docs not regenerating after expectation suite updates (stale HTML served), matrix CI strategy missing the production Python version (testing 3.10/3.11 but prod runs 3.9).

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

