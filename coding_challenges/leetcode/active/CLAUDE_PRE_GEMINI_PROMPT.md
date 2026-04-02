# CLAUDE PRE-GEMINI STUDY PLAN ENHANCER
# Version 1.0
# Usage: Paste this prompt to Claude Code, then give the study plan file path.
# Output: An enhanced study-plan-day-NN.md ready to feed Gemini.

---

## YOUR TASK

You are enhancing a raw study plan so that Gemini will produce a complete, staff-level study folder from it with zero ambiguity and no guessing.

The user will give you a file path like:
`<Project_Root>\outbox\study-plan-day-04.md`

You will:
1. Read the file completely
2. Extract everything Gemini needs (LC numbers, slugs, capstone integration, design pattern)
3. Write an ENHANCED version of the same file with a `## GENERATION METADATA` block prepended
4. Enrich 4 specific areas of the study plan content itself (see ENRICHMENT TASKS below)
5. Write the enhanced file back to the same path (overwrite)
6. Print a summary of what you added

---

## STEP 1: EXTRACT GENERATION METADATA

Read the study plan and extract/derive:

### a) LeetCode problems
Scan for `LC #` or `### LC #` patterns. For each problem found:
- Extract the LC number → zero-pad to 3 digits (LC #20 → `LC020`)
- Derive the slug: lowercase the title, replace spaces/special chars with underscores
  - "Valid Parentheses" → `valid_parentheses`
  - "Largest Rectangle in Histogram" → `largest_rectangle_in_histogram`
  - "N-th Tribonacci Number" → `nth_tribonacci_number`

### b) SQL slug
Look for the SQL section header (e.g., `## B. SQL — Complex JOINs`). Derive snake_case slug:
- "Complex JOINs" → `complex_joins`
- "Query Optimization" → `query_optimization`
- "GROUPING SETS / ROLLUP / CUBE" → `grouping_sets_rollup_cube`
- "CTEs and Subqueries" → `ctes_subqueries`

### c) Python slug
Look for the Python section header (e.g., `## C. Python — Decorators & Context Managers`):
- "Decorators & Context Managers" → `decorators_context_managers`
- "Generators & Iterators" → `generators_iterators`
- "Pydantic & Type System" → `pydantic_type_system`

### d) Tech slug
Look for the Technology/Architecture section (e.g., `## D. Technology — Pipeline Architecture`):
- "Pipeline Architecture: Lambda & Kappa" → `pipeline_architecture`
- "Apache Spark" → `apache_spark`
- "dbt (Data Build Tool)" → `dbt_data_build_tool`
- "Apache Kafka" → `kafka_streaming`
- "Apache Airflow" → `airflow_orchestration`

### e) Day number
Extract from file header or filename. Zero-pad to 2 digits.

### f) Capstone integration
This is the most important field — it forces Gemini to actually connect all 4 topics.
For each topic, write one sentence describing HOW it appears in the capstone:
- LeetCode: "Which specific LC pattern (e.g., LC739 sliding window max) is used for what specific capstone feature"
- SQL: "Which SQL pattern (e.g., anti-join) solves which data quality problem in the capstone"
- Python: "Which Python concept (e.g., @retry decorator) wraps which specific pipeline stage"
- Tech: "Which architectural pattern (e.g., Lambda architecture) shapes the overall capstone design"

If the connection isn't obvious from the study plan, use the following heuristics:
- Stack/monotonic → CPU spike detection using sliding window
- Binary search → config threshold lookup in O(log n)
- DP → max/min optimization over a time series
- Heap → top-N servers by utilization
- JOINs → gap detection (anti-join: servers missing from daily_metrics)
- Window functions → running totals, rankings, comparisons to group average
- Decorators → @timer, @retry wrapping each pipeline stage
- Generators → memory-efficient streaming of large event files
- Pydantic → boundary validation of incoming telemetry events
- Lambda/Kappa → overall pipeline architecture shape

### g) Design pattern
Select based on the Python topic:
| Python topic | Design pattern |
|---|---|
| Decorators & Context Managers | Pipeline Pattern with Decorator Pattern |
| Pydantic / Type System | Strategy Pattern with Repository Pattern |
| Generators / Iterators | Iterator Pattern with Pipeline Pattern |
| Concurrency / asyncio | Observer Pattern with Context Manager Pattern |
| Testing / pytest | Factory Pattern for test fixtures |

If none match, default to "Pipeline Pattern with Strategy Pattern for validation"

---

## STEP 2: WRITE THE GENERATION METADATA BLOCK

Write this exact YAML block immediately after the frontmatter `---` block and before the `# Study Day N:` header:

```
## GENERATION METADATA
```yaml
day: {NN}
output_dir: <Project_Root>\DaysStudy\Day-{NN}
theme: "{Topic1 from LeetCode section}, {Topic2 from SQL section}, {Topic3 from Python section}, {Topic4 from Tech section}"
leetcode:
  - id: LC{###}  slug: {snake_case_title}
  - id: LC{###}  slug: {snake_case_title}
  ... (one entry per problem found)
sql_slug: {derived_slug}
python_slug: {derived_slug}
tech_slug: {derived_slug}
capstone_name: {snake_case name derived from topic combination}
capstone_integration:
  - "{LeetCode algorithm} → {specific capstone feature it implements}"
  - "{SQL pattern} → {specific capstone data quality check it enables}"
  - "{Python concept} → {specific pipeline stage it decorates/wraps}"
  - "{Tech pattern} → {how it shapes overall capstone architecture}"
design_pattern: "{selected pattern from step 1g}"
shared_domain:
  entity: server_telemetry
  fields: [server_id, region, tier, avg_cpu, report_date, alert_count]
  primary_table: daily_metrics
  db_file: telemetry.db
  sample_cpu_values: [45.2, 78.1, 92.3, 55.0, 88.7, 34.1, 97.2, 61.5]
```
```

---

## STEP 3: ENRICH THE STUDY PLAN CONTENT (4 targeted areas)

After writing the metadata block, scan the study plan body and apply these enrichments:

### Enrichment A: LeetCode Bonus Variant Tags
For each LeetCode problem that does NOT already mention a bonus variant or follow-up problem, add a comment block immediately after the main solution:

```
> **BONUS VARIANT for Gemini:** Generate a bonus solution for `{bonus_name}`.
> Example: For LC#739 Daily Temperatures → bonus: "Implement for circular array (next greater element wraps around)"
> Example: For LC#84 Largest Rectangle → bonus: "Solve for Maximal Rectangle in Binary Matrix (LC#85)"
> Example: For LC#20 Valid Parentheses → bonus: "Minimum Add to Make Parentheses Valid (LC#921)"
```

Use this table to select the right bonus:
| LC | Bonus variant |
|---|---|
| LC020 Valid Parentheses | LC921 Minimum Add to Make Valid |
| LC155 Min Stack | Max Stack variant (track maximum instead) |
| LC739 Daily Temperatures | Next Greater Element II — circular array |
| LC853 Car Fleet | Car Fleet II — continuous distance |
| LC084 Largest Rectangle | LC085 Maximal Rectangle in Binary Matrix |
| LC704 Binary Search | LC33 Search in Rotated Sorted Array |
| LC153 Min in Rotated Array | LC154 with duplicates allowed |
| LC300 LIS | O(n log n) patience sorting variant |
| LC198 House Robber | LC213 House Robber II (circular) |
| LC322 Coin Change | LC518 Coin Change II (count combinations) |
| LC70 Climbing Stairs | LC746 Min Cost Climbing Stairs |

### Enrichment B: SQL Domain Anchoring
Find the first SQL code block and add a comment above it if it doesn't already reference the shared domain:

```sql
-- Domain: server_telemetry
-- Tables: servers(server_id, region, tier), daily_metrics(server_id, report_date, avg_cpu, alert_count)
-- All queries in this section use telemetry.db created by 00_setup_database.py
```

### Enrichment C: Capstone Connection Callout
After the last main section (before "Today's Key Interview Talking Points"), add:

```markdown
## Capstone Connection — How Today's Topics Integrate

| Topic | Capstone Role |
|-------|--------------|
| {LC pattern} | {specific function/class in capstone that uses it} |
| {SQL pattern} | {specific query in capstone that uses it} |
| {Python concept} | {specific decorator/class in capstone that uses it} |
| {Tech pattern} | {architectural shape of capstone — batch/stream/hybrid} |

> **Capstone name:** `{capstone_name}` — see `capstone/mini_project_brief.md`
> **Design pattern:** {design_pattern}
```

### Enrichment D: Interview Talking Points — Verify Depth
Scan all `**Interview Q&A:**` sections. For any Q&A answer that is a single sentence (< 50 words), expand it to at least 3 sentences using this format:
1. Direct answer (what)
2. Underlying principle (why)
3. Production/Citi context (when you'd use this in the real world)

If an answer already has 3+ sentences, leave it unchanged.

---

## STEP 4: WRITE AND CONFIRM

1. Write the enhanced file back to the original path (overwrite)
2. Print this confirmation:

```
ENHANCEMENT COMPLETE: {filepath}

GENERATION METADATA extracted:
  Day: {N}
  LeetCode: {LC###_slug × N problems}
  SQL slug: {slug}
  Python slug: {slug}
  Tech slug: {slug}
  Capstone name: {capstone_name}
  Design pattern: {pattern}

Enrichments applied:
  ✓/✗ Bonus variants added to {N} LeetCode problems
  ✓/✗ SQL domain anchor comment added
  ✓/✗ Capstone connection table added
  ✓/✗ Short Q&A answers expanded: {N} expanded

Ready to feed to Gemini with ENHANCED_MASTERPROMPT.md.
```

---

## STEP 5: UPDATE TRACKER

Edit `<Project_Root>\DaysStudy\TRACKER.md`:
- Find the row for Day {NN} (the day number from the study plan)
- Change `[ ]` to `[x]` in the **PRE** column only
- Leave GEMINI and POST columns unchanged

Print: `✓ Tracker updated: Day {NN} PRE marked [x]`

---

## NOW BEGIN

Read this file and enhance it:
`{PASTE STUDY PLAN FILE PATH HERE}`

Example: `<Project_Root>\outbox\study-plan-day-04.md`
