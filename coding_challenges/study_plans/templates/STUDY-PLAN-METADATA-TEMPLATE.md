# GENERATION METADATA TEMPLATE
# Copy the block below and paste it at the TOP of any study-plan-day-{N}.md file.
# Fill in all fields. Gemini reads this before writing a single file.
# The enhanced prompt (ENHANCED_MASTERPROMPT.md) enforces that Gemini follows it exactly.

---

## HOW TO USE

1. Copy the YAML block below
2. Paste it immediately after the frontmatter (---) in your study plan file
3. Fill in all fields for your day
4. When you run Gemini with the enhanced prompt, it will print a GENERATION PLAN before starting

---

## TEMPLATE (copy from here)

```yaml
## GENERATION METADATA
day: {N}                          # e.g. 04
output_dir: D:\Workspace\DaysStudyGemini2\Day-{N}
theme: "{Topic1}, {Topic2}, {Topic3}, {Topic4}"

leetcode:
  - id: LC{###}  slug: {snake_case_title}   # e.g. id: LC001  slug: two_sum
  - id: LC{###}  slug: {snake_case_title}
  - id: LC{###}  slug: {snake_case_title}
  - id: LC{###}  slug: {snake_case_title}
  - id: LC{###}  slug: {snake_case_title}

sql_slug: {snake_case_sql_topic}            # e.g. complex_joins, window_functions, ctes_subqueries
python_slug: {snake_case_python_topic}      # e.g. decorators_context_managers, generators_iterators
tech_slug: {snake_case_technology}          # e.g. pipeline_architecture, kafka_streaming, airflow_dags

capstone_name: {snake_case_capstone_name}   # e.g. telemetry_alert_pipeline

capstone_integration:
  - "{How LeetCode algorithm appears in capstone — be specific about which LC problem}"
  - "{How SQL pattern appears in capstone — reference the sql_slug}"
  - "{How Python concept appears in capstone — reference the python_slug}"
  - "{How technology concept appears in capstone — reference the tech_slug}"

design_pattern: "{Primary design pattern for real-world project and capstone}"
# Examples:
#   "Pipeline Pattern with Strategy Pattern for validation"
#   "Observer Pattern with Decorator Pattern for cross-cutting concerns"
#   "Repository Pattern with Factory Pattern for data source abstraction"

shared_domain:
  entity: server_telemetry          # keep this consistent across all days
  fields: [server_id, region, tier, avg_cpu, report_date, alert_count]
  primary_table: daily_metrics
  db_file: telemetry.db
  sample_cpu_values: [45.2, 78.1, 92.3, 55.0, 88.7, 34.1, 97.2, 61.5]
```

---

## FIELD REFERENCE

### `leetcode` — LC number rules
- Always 3 digits, zero-padded: `LC001`, `LC020`, `LC084`, `LC300`
- Slug is snake_case of the problem title: `two_sum`, `valid_parentheses`, `longest_increasing_subsequence`
- This produces file: `leetcode/LC001_two_sum_solved.py`

### `sql_slug` — common values by topic
| SQL Topic | slug |
|-----------|------|
| Complex JOINs (self, anti, cross) | `complex_joins` |
| Window Functions (RANK, LAG, LEAD) | `window_functions` |
| GROUPING SETS / ROLLUP / CUBE | `grouping_sets_rollup_cube` |
| CTEs and Subqueries | `ctes_subqueries` |
| Query Optimization | `query_optimization` |
| Recursive CTEs | `recursive_ctes` |
| Schema Design / Normalization | `schema_design` |

### `python_slug` — common values by topic
| Python Topic | slug |
|--------------|------|
| Decorators & Context Managers | `decorators_context_managers` |
| Generators & Iterators | `generators_iterators` |
| Pydantic & Type System | `pydantic_type_system` |
| Pandas Data Engineering | `pandas_data_engineering` |
| Concurrency (asyncio/threading) | `concurrency_asyncio` |
| Testing (pytest, fixtures, mocks) | `testing_pytest` |

### `tech_slug` — common values by technology
| Technology | slug |
|------------|------|
| Lambda/Kappa Architecture | `pipeline_architecture` |
| Apache Spark | `apache_spark` |
| dbt (Data Build Tool) | `dbt_data_build_tool` |
| Apache Kafka | `kafka_streaming` |
| Apache Airflow | `airflow_orchestration` |
| AWS Data Services | `aws_data_services` |
| Kubernetes for Data | `kubernetes_data_workloads` |

### `design_pattern` — common selections
| When to use | Pattern |
|-------------|---------|
| Multi-step data processing | `Pipeline Pattern` |
| Interchangeable validation rules | `Strategy Pattern` |
| Wrapping functions with behavior | `Decorator Pattern` |
| Guaranteed resource cleanup | `Context Manager Pattern` |
| Decoupled event handling | `Observer / Pub-Sub Pattern` |
| Building different pipeline configs | `Factory Pattern` |
| Abstracting data source | `Repository Pattern` |

---

## EXAMPLE — COMPLETED FOR DAY 03

```yaml
## GENERATION METADATA
day: 03
output_dir: D:\Workspace\DaysStudyGemini2\Day-03
theme: "Stack & Monotonic Patterns, Complex SQL JOINs, Python Decorators & Context Managers, Lambda/Kappa Architecture"
leetcode:
  - id: LC020  slug: valid_parentheses
  - id: LC155  slug: min_stack
  - id: LC739  slug: daily_temperatures
  - id: LC853  slug: car_fleet
  - id: LC084  slug: largest_rectangle_in_histogram
sql_slug: complex_joins
python_slug: decorators_context_managers
tech_slug: pipeline_architecture
capstone_name: telemetry_alert_pipeline
capstone_integration:
  - "Monotonic stack (LC739 pattern) for sliding window CPU anomaly detection over 5-minute windows"
  - "Anti-join SQL (complex_joins) to find servers missing from daily_metrics"
  - "@timer and @retry decorators wrapping each pipeline stage (decorators_context_managers)"
  - "Lambda architecture: batch SQL aggregates + speed layer streaming alerts (pipeline_architecture)"
design_pattern: "Pipeline Pattern with Decorator Pattern for cross-cutting concerns (timing, retry, logging)"
shared_domain:
  entity: server_telemetry
  fields: [server_id, region, tier, avg_cpu, report_date, alert_count]
  primary_table: daily_metrics
  db_file: telemetry.db
  sample_cpu_values: [45.2, 78.1, 92.3, 55.0, 88.7, 34.1, 97.2, 61.5]
```
