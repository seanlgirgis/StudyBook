# pipeline_logger — Reusable Logging Library

---

## 📌 Scenario

Modern data pipelines are not just about moving data — they must be **observable, debuggable, and auditable**.

In production environments, engineers need to answer questions like:

* *Which pipeline run failed?*
* *Where did records get dropped?*
* *Which stage is slow?*
* *Can I trace one run across all logs?*

Basic logging (`print`, simple logging) fails at scale because it lacks:

* structure
* context
* consistency
* machine-readability

This project solves that problem by building a **reusable logging library for data pipelines**.

---

## 🏗️ What Was Built

A complete, production-style logging system consisting of:

### 1. Core Library — `pipeline_logger.py`

A reusable module that provides:

* `get_pipeline_logger()`

  * Single entry point for creating pipeline-aware loggers
  * Injects:

    * `run_id`
    * `pipeline_name`
    * `environment`

* `PipelineLogger` (LoggerAdapter)

  * Automatically attaches context to every log line

* `log_stage()` (context manager)

  * Logs:

    * stage start
    * stage completion (with duration)
    * stage failure (with traceback)
  * Eliminates boilerplate try/except logic

* `log_dataframe_stats()`

  * Logs dataset shape and null counts
  * Detects silent data loss

* Environment-aware configuration:

  * `dev` → human-readable console logs
  * `staging` → JSON logs to stdout + file
  * `prod` → JSON logs to file + sampling

---

### 2. Example Pipeline — `example_pipeline.py`

A realistic 4-stage ETL pipeline:

* **extract**

  * generates 1000 records

* **validate**

  * removes 30 bad records → 970 remaining

* **transform**

  * enriches data with computed fields

* **load**

  * writes JSONL output

Includes:

* stage-level logging via `log_stage()`
* dataframe stats at each stage
* structured logging across entire pipeline
* post-run log summary
* failure simulation (`publish` stage)

---

### 3. Test Suite — `test_pipeline_logger.py`

Pytest-based validation covering:

* run_id injection in all logs
* stage timing correctness
* exception logging behavior
* JSON output validity
* pipeline_name consistency
* dataframe stats logging

---

## ▶️ How to Run

### 1. Run the library self-check

```bash
python capstone\pipeline_logger.py
```

---

### 2. Run the example pipeline

```bash
python capstone\example_pipeline.py
```

---

### 3. Run tests

```bash
pytest capstone\test_pipeline_logger.py -v
```

---

## ✅ Acceptance Criteria Checklist

* [x] All logs are structured (JSON in file)
* [x] Every log includes `run_id`, `pipeline_name`, `environment`
* [x] Stage lifecycle logging (start / complete / fail)
* [x] Duration tracking for every stage
* [x] Exception logging includes traceback
* [x] Dataframe stats logged at each stage
* [x] Log output is machine-parseable
* [x] Tests validate real behavior (not mocks)
* [x] No placeholders, TODOs, or incomplete code
* [x] Fully runnable end-to-end pipeline

---

## 🔁 How to Reuse in Other Tutorials

Use this exact 3-line import pattern:

```python
from pathlib import Path
import sys; sys.path.insert(0, str(Path(__file__).parent.parent / "capstone"))
from pipeline_logger import get_pipeline_logger, log_stage
```

### Minimal usage example:

```python
logger = get_pipeline_logger("my-pipeline")

with log_stage(logger, "extract"):
    # your logic here
    pass
```

---

## 🧠 Key Design Insights

### 1. Logging is a SYSTEM, not a print statement

Good logging is designed for:

* debugging
* monitoring
* alerting
* auditing

---

### 2. Context is everything

Without:

* `run_id`
* `stage`
* `pipeline_name`

Logs are just noise.

---

### 3. Structured logs > text logs

JSON logs enable:

* filtering
* aggregation
* dashboards
* alerting systems

---

### 4. Context managers beat boilerplate

`log_stage()` replaces:

```python
try:
    ...
except:
    ...
finally:
    ...
```

with:

```python
with log_stage(logger, "stage"):
    ...
```

---

### 5. Tests prove observability

Testing logging behavior ensures:

* no silent regressions
* consistent schema
* production reliability

---

## 🚀 Final Result

You now have:

* A **reusable logging library**
* A **working ETL pipeline using it**
* A **test suite validating behavior**

This is no longer “practice code” — it is:

> **Production-grade observability infrastructure for data pipelines**
