# PySpark Docker Tutorial - Collaboration Grounding (You + Codex + ChatGPT)

## Mission

Build a complete, educational, and fully documented PySpark tutorial under:

`D:\Workarea\StudyBook\tutorials\02_PySpark_Docker`

The tutorial must be beginner-friendly, runnable, and interview-focused.

## Team Roles

- You (Owner): set priorities, run scripts, ask for deeper explanations.
- Codex: implement files in repo, keep structure clean, maintain technical docs.
- ChatGPT: provide conceptual explanations, analogies, recap quizzes, and interview Q&A drills.

## Collaboration Workflow (for each lesson)

1. Build or update one lesson file.
2. Run it and capture important outputs.
3. Explain what happened in plain language.
4. Inspect Spark UI behavior (when relevant).
5. Document key takeaways and troubleshooting notes.
6. Move to the next lesson only after the current lesson is clear.

## Learning Outcomes

This track should cover:

1. SparkSession basics
2. Lazy evaluation
3. DataFrames
4. SQL and temp views
5. Joins
6. Broadcast joins
7. Shuffle behavior
8. Partitioning
9. Caching and persistence
10. Data skew
11. File formats
12. Bronze/Silver/Gold ETL
13. Execution plans
14. Spark UI analysis

## Technical Context

This Docker-first path replaces fragile local Windows Spark setups affected by:

- Java PATH conflicts
- Python worker crashes
- winutils/HADOOP friction
- unstable local mode behavior

Default assumptions:

- Spark master: `spark://localhost:7077`
- Spark UI: `http://localhost:8080` or `http://localhost:8086`

## Required Project Structure

```text
02_PySpark_Docker/
  README.md
  requirements.txt
  chat.md
  common/
    spark_session.py
  01_cluster_connection.py
  02_dataframe_operations.py
  03_sql_and_views.py
  04_joins_and_broadcast.py
  05_shuffle_partitions_cache.py
  06_bronze_silver_gold_pipeline.py
  07_spark_ui_experiments.py
```

## Build Standards

- Every script must be runnable.
- Use `finally: spark.stop()` in each runnable file.
- Avoid placeholders and TODOs.
- Prefer DataFrame-native operations over Python UDFs in early lessons.
- Use moderate data sizes (100k-500k rows).
- Include `explain(True)` where educationally relevant.
- Print clear section headers and what to observe.

## Documentation Standards

Every lesson should include:

- Lesson purpose
- Concepts taught
- Runnable command
- Expected output highlights
- Plan reading guide (`explain` interpretation)
- Spark UI checks (if relevant)
- Common failure modes + fixes
- Interview-style recap questions

## Phased Implementation Plan

### Phase 1 (implemented first)

- `README.md`
- `requirements.txt`
- `common/spark_session.py`
- `01_cluster_connection.py`

### Phase 2

- `02_dataframe_operations.py`
- `03_sql_and_views.py`

### Phase 3

- `04_joins_and_broadcast.py`
- `05_shuffle_partitions_cache.py`

### Phase 4

- `06_bronze_silver_gold_pipeline.py`
- `07_spark_ui_experiments.py`

## Run Sequence

```powershell
python -u .\01_cluster_connection.py
python -u .\02_dataframe_operations.py
python -u .\03_sql_and_views.py
python -u .\04_joins_and_broadcast.py
python -u .\05_shuffle_partitions_cache.py
python -u .\06_bronze_silver_gold_pipeline.py
python -u .\07_spark_ui_experiments.py
```

## Definition Of Done (Tutorial Quality)

- All lesson scripts run successfully against Docker Spark.
- README provides setup + troubleshooting + learning path.
- Each lesson explains both code behavior and Spark engine behavior.
- Spark UI is actively used for at least one dedicated lesson.
- The track is usable for interview prep (concept + explanation depth).

## Next Build Instruction For Codex

Implement Phase 2 next:

- Create `02_dataframe_operations.py` and `03_sql_and_views.py`.
- Keep both files educational and fully documented in-code (concise section comments + clear print guidance).
- Do not generate Phase 3 or 4 files yet.
