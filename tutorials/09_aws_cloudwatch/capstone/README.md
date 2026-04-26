# 09_aws_cloudwatch — README

---

## 🔹 What This Project Is

This is a **production-style CloudWatch observability system** for a data pipeline.

It demonstrates how real platforms monitor pipelines using:

* Metrics (throughput, latency, errors, lag)
* Structured logs (JSON → queryable)
* Alarms (threshold + composite)
* Dashboards (visual health)
* Logs Insights (root-cause analysis)
* Cost-aware design

---

## 🔹 Resume-Ready Summary

Built an end-to-end CloudWatch observability framework for a data pipeline with custom metrics, structured logging, composite alarms, and automated dashboards; architected a reusable, cost-aware monitoring approach using metric cardinality design and enterprise-scale alerting patterns.

---

## 🔹 Project Structure

```
09_aws_cloudwatch/
│
├── README.md
│
├── setup/          ← Learning modules (isolated concepts)
│   ├── 01_custom_metrics.py
│   ├── 02_log_groups_and_insights.py
│   ├── 03_alarms_and_composite_alarms.py
│   ├── 04_dashboards_and_embedded_metrics.py
│   └── 05_container_and_lambda_monitoring.py
│
└── capstone/       ← Full system (production simulation)
    ├── emit_pipeline_metrics.py
    ├── setup_alarms.py
    ├── build_dashboard.py
    ├── insights_queries.py
    ├── capstone.py
    ├── cleanup.py
    └── test_capstone.py
```

---

## 🔹 Setup (one-time)

```powershell
..\..\env_setter.ps1 -NonInteractive
$env:AWS_PROFILE = "study"
$env:AWS_REGION = "us-east-1"
$env:CW_NAMESPACE = "StudyBook/CapstoneP"
$env:CW_LOG_GROUP_NAME = "/studybook/capstone/pipeline"
```

---

## 🔹 How to Run the Capstone (Recommended Path)

### Step-by-step (learning mode)

```powershell
python capstone\emit_pipeline_metrics.py
python capstone\setup_alarms.py
python capstone\build_dashboard.py
python capstone\insights_queries.py
python capstone\cleanup.py
```

---

### One-shot (full orchestration)

```powershell
python capstone\capstone.py
```

Then cleanup:

```powershell
python capstone\cleanup.py
```

---

## 🔹 What Each Capstone File Does

### `emit_pipeline_metrics.py`

* Simulates **24 hours of pipeline runs**
* Injects **2 failure windows**
* Emits:

  * metrics → CloudWatch
  * structured logs → Logs

👉 This is your **data source layer**

---

### `setup_alarms.py`

* Creates 4 metric alarms:

  * low output
  * errors
  * high duration
  * high lag
* Creates 1 composite alarm:

  * pipeline unhealthy

👉 This is your **decision layer**

---

### `build_dashboard.py`

* Builds a **5-widget dashboard**

  * throughput
  * duration (avg + p90)
  * errors
  * lag (single value)

👉 This is your **visualization layer**

---

### `insights_queries.py`

* Runs Logs Insights queries:

  * slow runs
  * error summary
  * throughput
  * lag trend

👉 This is your **investigation layer**

---

### `capstone.py`

* Orchestrates everything:

  * metrics → alarms → dashboard → queries
* Prints a final **health report**

👉 This is your **system workflow**

---

### `cleanup.py`

* Deletes:

  * alarms
  * dashboard
  * log group

👉 Prevents **ongoing AWS charges**

---

### `test_capstone.py`

* Runs **pure logic tests (no AWS calls)**
* Validates:

  * pipeline simulation
  * dashboard structure
  * cost calculations

Run:

```powershell
pytest capstone\test_capstone.py -v
```

---

## 🔹 Mental Model (Important)

CloudWatch = 4 layers

1. **Metrics** → signals
2. **Logs** → context
3. **Alarms** → decisions
4. **Dashboards** → visibility

Logs Insights = **debugging layer**

---

## 🔹 What You Should See

After running:

* Dashboard shows:

  * 24h data
  * 2 failure spikes

* Alarms:

  * may show `OK` if latest data is healthy (normal)

* Insights:

  * shows recent logs (CloudWatch indexing behavior)

---

## 🔹 Cost Awareness

Typical costs (approx):

* Metrics: $0.30 / metric / month (after 10 free)
* Logs: $0.50 / GB ingestion
* Dashboards: $3 / month
* Alarms: $0.10 / alarm / month

👉 Always run `cleanup.py`

---

## 🔹 Final Takeaway

This project demonstrates how real data platforms:

* detect failures (alarms)
* visualize health (dashboards)
* investigate issues (logs)
* control cost (design)

If you understand this end-to-end, you’re operating at a **Senior / Staff Data Engineer level** for observability.

---
