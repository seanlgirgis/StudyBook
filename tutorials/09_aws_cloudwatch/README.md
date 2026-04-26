# 09_aws_cloudwatch — README

---

## 1. Prerequisites

Run these in PowerShell before anything:

```powershell
..\..\env_setter.ps1 -NonInteractive
$env:AWS_PROFILE = "study"
$env:AWS_REGION = "us-east-1"
$env:CW_NAMESPACE = "StudyBook/Pipeline"
$env:CW_LOG_GROUP_NAME = "/studybook/pipeline"
```

**Note:**
`CW_ALARM_SNS_ARN` is optional — alarms will still work without notifications.

---

## 2. Phase 1 — Setup Scripts

### File 01 — Custom Metrics

```powershell
python .\setup\01_custom_metrics.py
```

**What it does:**
Emits custom CloudWatch metrics (single, batch, and statistic sets), then queries them and calculates cost impact.

**Key takeaway:**
Metrics = *namespace + name + dimensions* — cardinality drives cost.

---

### File 02 — Logs & Insights

```powershell
python .\setup\02_log_groups_and_insights.py
```

**What it does:**
Creates log groups, emits structured JSON logs, and runs CloudWatch Logs Insights queries.

**Key takeaway:**
Structured logs turn debugging into querying — Logs Insights is your SQL for logs.

---

### File 03 — Alarms

```powershell
python .\setup\03_alarms_and_composite_alarms.py
```

**What it does:**
Creates metric alarms and a composite alarm to simulate real pipeline health alerting.

**Key takeaway:**
Composite alarms reduce noise — alert on *combined signals*, not single spikes.

---

### File 04 — Dashboards & EMF

```powershell
python .\setup\04_dashboards_and_embedded_metrics.py
```

**What it does:**
Emits EMF metrics via logs and builds a CloudWatch dashboard programmatically.

**Key takeaway:**
EMF = metrics via logs → avoids PutMetricData cost and simplifies instrumentation.

---

### File 05 — Containers & Lambda Monitoring

```powershell
python .\setup\05_container_and_lambda_monitoring.py
```

**What it does:**
Creates metric filters, demonstrates Lambda metrics retrieval, builds ECS queries, and calculates CloudWatch costs.

**Key takeaway:**
You can extract metrics from logs retroactively — observability without code changes.

---

## 3. Phase 2 — Capstone

Run in this exact order:

```powershell
python capstone\emit_pipeline_metrics.py
python capstone\setup_alarms.py
python capstone\build_dashboard.py
python capstone\insights_queries.py
python capstone\capstone.py
python capstone\test_capstone.py
python capstone\cleanup.py
```

---

## 4. Emergency Cleanup

If anything crashes or leaves resources behind:

```powershell
python -c "
import os, boto3
cw = boto3.client('cloudwatch', region_name='us-east-1')
logs = boto3.client('logs', region_name='us-east-1')
for alarm in ['cw-records-low','cw-error-spike','cw-latency-high','cw-pipeline-unhealthy','capstone-records-low','capstone-errors','capstone-lag','capstone-unhealthy']:
    try: cw.delete_alarms(AlarmNames=[alarm]); print(f'Deleted alarm: {alarm}')
    except: pass
for group in ['/studybook/pipeline', '/studybook/capstone/pipeline']:
    try: logs.delete_log_group(logGroupName=group); print(f'Deleted log group: {group}')
    except: pass
for dash in ['studybook-pipeline', 'capstone-pipeline-health']:
    try: cw.delete_dashboards(DashboardNames=[dash]); print(f'Deleted dashboard: {dash}')
    except: pass
print('Emergency cleanup done.')
"
```

---

## Mental Model (Keep This)

CloudWatch = **4 layers**

1. **Metrics** → raw signals
2. **Logs** → detailed context
3. **Alarms** → decision layer
4. **Dashboards** → visualization layer

Everything in this tutorial maps to one of those layers.

---

## Final Thought

If you understand this directory end-to-end, you can walk into any **Data Engineering / Platform / SRE interview** and confidently explain:

* how pipelines are monitored
* how alerts are triggered
* how incidents are debugged
* how costs are controlled

That’s the real goal here.
