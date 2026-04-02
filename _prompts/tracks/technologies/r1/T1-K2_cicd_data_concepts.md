# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R1\\T1-K2_cicd_data_concepts.md

SAVE AS: cicd_data_concepts.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

ROLE: You are a senior Data Engineer writing a reference guide for an engineer preparing
for Staff DE interviews at a financial institution. Precise, dense, no filler.

TASK: Generate cicd_data_concepts.md — a concept reference covering DataOps, CI/CD for data pipelines,
data quality testing, and data contracts.

DATASET CONTEXT — do not deviate:
- Citi narrative: dbt CI pipeline on GitHub Actions, Great Expectations on de_telemetry alerts

STRUCTURE — produce exactly these sections in order:

# CI/CD for Data — Core Concepts

## 1. DataOps
One paragraph. Cover: application of DevOps principles to data pipelines, key pillars:
automation (no manual steps), observability (metrics on pipeline health), collaboration (DE + ML + analytics),
testing (data quality gates), the goal: reduce time from raw data to trusted insight, reduce
mean time to detect (MTTD) data quality issues.
End with: "DataOps at Citi: every dbt PR triggers automated tests — severity validation catches NULL severities in 90 seconds, not 3 days in production."

## 2. Data Testing Pyramid
One paragraph. Cover: four levels — unit (SQL logic on mock data), integration (models against real DB),
data quality (assertions on source data), contract (schema agreements with producers),
testing cost increases bottom to top but so does confidence, most teams over-invest in unit and
under-invest in data quality and contracts.
End with: "The citi_dbt pipeline tests at all four levels: dbt unit tests, dbt build in CI (integration), GE checkpoint (data quality), dbt sources freshness (contract)."

## 3. Great Expectations
One paragraph. Cover: expectations = assertions on data columns/tables, suites = collections of expectations,
checkpoints = run a suite against a datasource and produce a validation result, data docs = HTML report
of all results, three context modes (ephemeral, file, cloud), expectations declared in code
(not in a UI) so they're version-controlled.
End with: "The citi_alerts_suite has 7 expectations — severity in [LOW,MEDIUM,HIGH,CRITICAL], alert_id unique and not null, row count between 1k and 100k. Any violation fails CI."

## 4. dbt Tests as CI Gates
One paragraph. Cover: dbt test runs generic tests (unique, not_null, accepted_values, relationships)
and singular tests, dbt build = dbt run + dbt test in sequence (fail fast: if run fails, test
doesn't run), CI environment uses a separate schema (dbt_ci) to isolate from dev/prod,
test coverage: every model's primary key must have unique + not_null at minimum.
End with: "The GitHub Actions workflow runs dbt build --project-dir citi_dbt — models run and test in schema dbt_ci, never touching dbt_dev."

## 5. GitHub Actions for Data
One paragraph. Cover: YAML-defined workflow triggered on PR/push/schedule, services block for
Postgres sidecar (ephemeral test database), secrets for credentials (never hardcoded in YAML),
matrix strategy for testing multiple Python/dbt versions, workflow artifacts for GE data docs HTML.
End with: "The dbt_ci.yml workflow spins a fresh Postgres container, seeds test data, runs dbt build, runs GE checkpoint — all in 3-5 minutes per PR."

## 6. Data Contracts
One paragraph. Cover: formal agreement between data producer and consumer on schema, types, SLAs,
and semantics, violation = breaking change that requires coordination, dbt sources with freshness checks
= lightweight contract (if source hasn't updated in 24h, pipeline warns or fails), Soda Core and
dbt-contracts package for stricter enforcement, consumers declare what they need, producers
commit to providing it.
End with: "dbt source freshness on citi_telemetry.alerts: if the alerts table hasn't updated in 2 hours, dbt warns — the monitoring agent feeding it may have failed."

## 7. CI/CD Pipeline for Data — the Full Loop
One paragraph. Cover: developer writes dbt model → PR opened → GitHub Actions triggers (dbt build +
GE checkpoint) → all tests pass → PR merged → main branch triggers deployment (dbt run in prod schema) →
monitoring alerts if prod run fails → on-call investigates. The loop is 10-30 minutes from commit to production.
End with: "This is the Staff DE answer to 'how do you deploy data pipelines safely?': every change goes through CI, tested automatically, deployed via CD — no manual dbt run in prod."

## 8. Data Observability
One paragraph. Cover: monitoring data pipelines after deployment — volume checks (row count dropped 50%?),
freshness checks (table updated in last 2 hours?), schema change detection (column added/removed?),
distribution monitoring (severity distribution shifted?), tools: Monte Carlo, Acceldata, Metaplan,
dbt's built-in source freshness, Great Expectations scheduled checkpoints.
End with: "A scheduled GE checkpoint runs every 30 minutes on citi_telemetry.alerts — if row count drops below 1000, the monitoring system pages the Citi ops team."

---

## Quick Reference Table

| Concept | One-line definition | Citi example |
|---------|---------------------|--------------|
| DataOps | DevOps applied to data pipelines | Automated CI on every dbt PR |
| Testing Pyramid | Unit → Integration → Quality → Contract | dbt tests + GE + freshness |
| Great Expectations | Data assertions as version-controlled code | citi_alerts_suite, 7 expectations |
| dbt Tests | SQL assertions on model outputs | unique, not_null, accepted_values |
| GitHub Actions | Event-driven CI/CD workflow | PR → dbt build → GE → merge |
| Data Contract | Schema/SLA agreement producer↔consumer | dbt source freshness < 2h |
| CI/CD Loop | Commit → CI → deploy → monitor | 10-30 min commit to prod |
| Data Observability | Monitor pipelines post-deploy | Scheduled GE checkpoint |

---

## Interview Flashcards

**Q: What is the difference between a dbt test and a Great Expectations expectation?**
A: dbt tests run on dbt model outputs (tables/views that dbt created). They validate model logic —
unique keys, referential integrity, accepted values. Great Expectations runs on source data before
dbt touches it. If the source data is bad (nulls, wrong types), GE catches it before dbt even runs.
Both are needed: GE guards the input, dbt tests guard the output.

**Q: Why should data pipelines have CI/CD?**
A: Data bugs are silent — a pipeline that returns zero rows for HIGH severity alerts doesn't crash;
it just serves wrong results. Without CI, that bug reaches production and stays there until an analyst
notices 3 days later. With CI: the broken model fails dbt test in 90 seconds, the PR is blocked,
the bug never reaches production.

**Q: What is a data contract and why does it matter at scale?**
A: A data contract is a formal agreement between a data producer (team that writes the table) and
a data consumer (team that reads it). It covers schema, column semantics, SLAs (freshness), and
volume expectations. Without contracts, a producer renames a column and 10 downstream pipelines
silently break. With contracts, the change is a breaking change — versioned, communicated, coordinated.

**Q: How do you handle secrets in GitHub Actions?**
A: Store in GitHub repository or organization Secrets (Settings → Secrets). Reference in YAML as
${{ secrets.POSTGRES_PASSWORD }}. Never hardcode credentials in YAML — they end up in git history
and CI logs. For more complex secret management: AWS Secrets Manager + GitHub OIDC (no static keys).

**Q: What is data observability and how is it different from data testing?**
A: Testing runs at deployment time (CI/CD gate). Observability monitors continuously in production —
volume anomalies, freshness violations, schema drift, distribution shifts. Testing prevents known
bad states from deploying. Observability detects unknown bad states that emerge after deployment
(upstream data changes, model behavior drift, infrastructure issues).

CONSTRAINTS:
- Each concept: exactly one paragraph, 4-6 sentences, no bullets inside
- Citi tie-in is the last sentence of each paragraph
- Table: valid GFM pipe table
- No filler phrases

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.


