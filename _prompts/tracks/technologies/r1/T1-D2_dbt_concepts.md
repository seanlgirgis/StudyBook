# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R1\\T1-D2_dbt_concepts.md

SAVE AS: dbt_concepts.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

ROLE: You are a senior Data Engineer writing a reference guide for an engineer preparing
for Staff DE interviews at a financial institution. Precise, dense, no filler.

TASK: Generate dbt_concepts.md — a concept reference covering 8 core dbt abstractions,
each in one tight paragraph, followed by a Citi narrative tie-in.

DATASET CONTEXT — do not deviate:
- Citi narrative: dbt project citi_dbt, staging model stg_alerts, mart model mart_alert_summary

STRUCTURE — produce exactly these sections in order:

# dbt — Core Concepts

## 1. Model
One paragraph. Cover: a .sql file containing a single SELECT statement, dbt compiles it and
executes it as a view or table in the warehouse, models are composable via ref(),
each model = one relation in the target schema, naming convention staging/marts/intermediate.
End with: "stg_alerts.sql and mart_alert_summary.sql are two models — one staging, one mart."

## 2. Source
One paragraph. Cover: raw tables not created by dbt, declared in sources.yml, accessed via source()
macro which generates the correct schema-qualified reference, sources can have freshness checks,
separates dbt-managed relations from external ones.
End with: "alerts and endpoints are sources — dbt does not own them; the DE team loads them via Airflow."

## 3. ref()
One paragraph. Cover: the core dbt macro for referencing other models, generates the correct
schema-qualified table/view name at compile time, enables lineage tracking, dbt infers run order
from ref() calls (no manual dependency declaration needed).
End with: "mart_alert_summary references stg_alerts via {{ ref('stg_alerts') }} — dbt runs stg_alerts first automatically."

## 4. Materialization
One paragraph. Cover: how dbt persists a model — view (default, recomputed on query), table (full
rebuild each run), incremental (append/merge new rows only), ephemeral (CTE, never persists).
When to use each. Incremental models use is_incremental() macro and an on_schema_change setting.
End with: "mart_alert_summary uses materialized='table' — rebuilt nightly by Airflow; stg_alerts is a view."

## 5. Test
One paragraph. Cover: generic tests (unique, not_null, accepted_values, relationships) declared in
YAML, singular tests = custom SQL in tests/ folder, dbt test runs all and fails on any assertion violation,
test results logged per model per column.
End with: "alert_id has unique + not_null; severity has accepted_values ['LOW','MEDIUM','HIGH','CRITICAL'] — dbt test catches bad ETL immediately."

## 6. Lineage Graph
One paragraph. Cover: dbt generates a DAG of model dependencies from ref() calls, visible in dbt docs,
enables impact analysis (if source changes, which models break?), lineage is automatic — no manual wiring.
End with: "The citi_dbt lineage: alerts (source) → stg_alerts → mart_alert_summary — visible in dbt docs serve."

## 7. Macro
One paragraph. Cover: Jinja2 functions that generate SQL, built-ins (ref, source, config, is_incremental),
custom macros in macros/ folder, packages (dbt-utils) add community macros,
macros enable DRY SQL (e.g., a single macro for date spine generation used across 10 models).
End with: "{{ config(materialized='table') }} is a macro call — it sets the materialization strategy at compile time."

## 8. dbt Cloud vs dbt Core
One paragraph. Cover: dbt Core is the open-source CLI (what we use), dbt Cloud adds a scheduler,
IDE, CI integration, and hosted docs, dbt Cloud jobs = Airflow alternative for pure-dbt pipelines,
pricing: dbt Core free forever, dbt Cloud team plan per seat.
End with: "The learning stack uses dbt Core — for production at Citi, dbt Cloud jobs or Airflow + dbt CLI are both valid patterns."

---

## Quick Reference Table

| Concept | One-line definition | Citi example |
|---------|---------------------|--------------|
| Model | SELECT file compiled to a relation | stg_alerts.sql, mart_alert_summary.sql |
| Source | External raw table declared in YAML | alerts, endpoints |
| ref() | Macro to reference another model | {{ ref('stg_alerts') }} |
| Materialization | How dbt persists a model | view / table / incremental |
| Test | Assertion on column values | unique, not_null, accepted_values |
| Lineage Graph | Auto-generated DAG from ref() calls | alerts → stg → mart |
| Macro | Jinja2 function generating SQL | {{ config() }}, {{ is_incremental() }} |
| dbt Cloud | Hosted dbt with scheduler + IDE | dbt Core used in this stack |

---

## Interview Flashcards

**Q: What is the difference between a source and a model in dbt?**
A: A source is a raw table that dbt does not create — declared in sources.yml and accessed via
source(). A model is a SELECT statement that dbt compiles and materializes. Sources are inputs;
models are outputs. The lineage graph connects them.

**Q: When would you use an incremental model instead of a table?**
A: When the table is large and a full rebuild is too slow or expensive. Incremental models append
or merge only new/changed rows using is_incremental() logic. Trade-off: incremental models can
accumulate incorrect rows if the merge logic is wrong — full refresh is safer for correctness.

**Q: How does dbt determine run order?**
A: From ref() calls. dbt builds a DAG of all models by following ref() dependencies — no manual
ordering needed. Models with no dependencies run first; models that ref() others run after.

**Q: What is a generic test vs a singular test?**
A: Generic tests (unique, not_null, accepted_values, relationships) are declared in YAML and applied
to columns. Singular tests are custom SQL files in the tests/ folder — any query that returns rows
fails. Use singular tests for business logic that generic tests cannot express.

**Q: What does dbt compile do?**
A: dbt compile resolves all Jinja macros (ref, source, config, is_incremental) and writes the
final SQL to the target/compiled/ folder without executing it. Useful for debugging — you can read
exactly what SQL dbt will run before committing to dbt run.

CONSTRAINTS:
- Each concept: exactly one paragraph, 4-6 sentences, no bullets inside
- Citi tie-in is the last sentence of each paragraph
- Table: valid GFM pipe table
- No filler phrases

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.


