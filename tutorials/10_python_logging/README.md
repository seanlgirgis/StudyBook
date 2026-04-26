# 10_python_logging

## 1. Prerequisites

```bash
pip install structlog python-json-logger
```

Optional (used only in config examples in file 05):

```bash
pip install watchtower splunk-handler
```

Environment variable:

```bash
LOG_DIR   # optional — defaults to:
          # Windows: %LOCALAPPDATA%/studybook/logs
          # Linux/macOS: /tmp/studybook/logs
```

---

## 2. Phase 1 — Setup Scripts

### 01_logging_fundamentals.py

**Run:**

```bash
python 10_python_logging\01_logging_fundamentals.py
```

**What it does:**
Demonstrates Python’s stdlib logging system including loggers, handlers, formatters, levels, propagation, and rotating file handlers. Simulates a small pipeline and shows how logs flow through the system.

**Key takeaway:**
Logging is hierarchical and the effective level is controlled by both logger and handler — misunderstanding this causes most production logging bugs.

---

### 02_structured_json_logging.py

**Run:**

```bash
python 10_python_logging\02_structured_json_logging.py
```

**What it does:**
Implements structured JSON logging with correlation IDs (`run_id`), contextual metadata, and post-run analysis by parsing logs into Python objects.

**Key takeaway:**
Structured JSON logs + correlation IDs are essential for tracing a pipeline run across systems — plain text logs don’t scale.

---

### 03_structlog_advanced.py

**Run:**

```bash
python 10_python_logging\03_structlog_advanced.py
```

**What it does:**
Introduces `structlog` with processor pipelines, bound loggers, context propagation, and dual output modes (JSON for production, readable console for development).

**Key takeaway:**
`structlog` separates configuration from usage — bind context once, and every log automatically carries it.

---

### 04_logging_patterns_for_data_pipelines.py

**Run:**

```bash
python 10_python_logging\04_logging_patterns_for_data_pipelines.py
```

**What it does:**
Implements production-grade logging patterns including retries, batch progress tracking, slow query detection, audit logs, and a timing context manager.

**Key takeaway:**
Good logging answers operational questions: *Is it stuck? Where is it slow? Where did the data go?*

---

### 05_log_aggregation_and_ops.py

**Run:**

```bash
python 10_python_logging\05_log_aggregation_and_ops.py
```

**What it does:**
Covers log rotation, sampling strategies, schema contracts, and how logs would be shipped to systems like CloudWatch or Splunk.

**Key takeaway:**
At scale, logging is not just about emitting logs — it’s about controlling volume, enforcing structure, and integrating with observability systems.

---

## 3. Phase 2 — Capstone

Run in this exact order:

```bash
python capstone\pipeline_logger.py
python capstone\example_pipeline.py
pytest capstone\test_pipeline_logger.py -v
```

---

## 4. Why This Matters for Interviews

### What Toyota / Capital One Interviewers Look For

* You understand **structured logging + correlation IDs**, not just `print()` or basic logging
* You can explain **how logs flow in production systems** (pipeline → file → aggregator → dashboard)
* You know how to design logs for **debugging, monitoring, and auditing**, not just output messages

### Expected Answer Pattern

**Question:** *"How do you observe a production pipeline?"*

**Strong answer structure:**

1. **Structured Logging**

   * JSON logs with consistent schema
   * Correlation ID (`run_id`) for tracing

2. **Contextual Logging**

   * Include pipeline_name, stage, batch, query_id, etc.
   * Use LoggerAdapter or structlog binding

3. **Operational Signals**

   * Progress logs (batch %, ETA)
   * Slow query detection
   * Retry logging with attempts and delays
   * Audit logs for record counts

4. **Aggregation Layer**

   * Logs shipped to CloudWatch / Splunk / ELK
   * Queryable by fields (not string search)

5. **Volume Control**

   * Sampling DEBUG/INFO logs
   * Rotating file handlers
   * Separate performance logs

**Bottom line:**
You don’t just log — you design logs as a **system for observability**.
