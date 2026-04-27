````markdown
# Large-Scale Log Processing with EMR Serverless

## Scenario

You are a data engineer supporting a production web platform. The application emits high-volume access logs from APIs such as users, orders, products, payments, reports, and authentication endpoints.

Your task is to process **one week of simulated web server access logs** using **EMR Serverless PySpark**.

The pipeline will:

1. Generate **1,000,000 synthetic web access log records**
2. Upload raw logs to S3
3. Run a PySpark job on EMR Serverless
4. Filter only HTTP error responses
5. Aggregate error traffic by endpoint, status code, and hour
6. Write analytics-ready Parquet output back to S3
7. Report estimated EMR Serverless cost
8. Clean up generated S3 data and EMR Serverless applications

---

## Business Problem

Engineering leadership wants a daily reliability report that answers:

- Which endpoints are producing the most errors?
- Which status codes are most common?
- During which hours do failures spike?
- Are server-side errors slower than client-side errors?
- Can the job scale without managing a persistent EMR cluster?

This mirrors a real production data engineering pattern:

> Raw operational logs enter a data lake, Spark transforms them into aggregated facts, and analytics teams query the curated Parquet output.

---

## Architecture

```text
Local Python Generator
        |
        v
Synthetic CSV Logs
        |
        v
S3 raw/weblogs/
        |
        v
EMR Serverless PySpark Job
        |
        v
Filter status_code >= 400
        |
        v
Aggregate by date, endpoint, status_code, hour
        |
        v
S3 processed/weblogs/ as partitioned Parquet
````

---

## Input Dataset

The generator creates simulated web access logs with these fields:

| Field              | Description                                           |
| ------------------ | ----------------------------------------------------- |
| `timestamp`        | ISO 8601 timestamp spread across seven days           |
| `endpoint`         | API endpoint such as `/api/orders` or `/api/payments` |
| `method`           | HTTP method: GET, POST, PUT, DELETE                   |
| `status_code`      | Weighted status code distribution                     |
| `response_time_ms` | Simulated latency in milliseconds                     |
| `bytes_sent`       | Response payload size                                 |
| `user_agent`       | Simulated client user agent                           |
| `ip_address`       | Simulated source IP                                   |

Status code weighting:

```text
200 → 70%
201 → 10%
400 → 8%
404 → 5%
500 → 5%
503 → 2%
```

This means roughly **20% of the records are error records** and should survive the Spark filter.

---

## Transformation Logic

The PySpark processing job must:

1. Read raw CSV data from:

```text
s3://{EMR_S3_BUCKET}/raw/weblogs/
```

2. Parse `timestamp` into Spark timestamp type

3. Keep only error rows:

```text
status_code >= 400
```

4. Add derived columns:

| Column | Purpose                                  |
| ------ | ---------------------------------------- |
| `date` | Used for partitioning and daily analysis |
| `hour` | Used for hourly error trend analysis     |

5. Aggregate by:

```text
date, endpoint, status_code, hour
```

6. Produce:

| Metric            | Meaning                                    |
| ----------------- | ------------------------------------------ |
| `request_count`   | Number of error requests                   |
| `avg_response_ms` | Average response time for that error group |
| `total_bytes`     | Total bytes returned for that group        |

7. Write Parquet output partitioned by:

```text
date, status_code
```

---

## Expected Output Layout

```text
s3://{EMR_S3_BUCKET}/processed/weblogs/
  date=2026-04-21/
    status_code=404/
      part-....parquet
    status_code=500/
      part-....parquet
  date=2026-04-22/
    status_code=400/
      part-....parquet
```

Partitioning by `date` and `status_code` improves query pruning for common reliability questions such as:

```sql
WHERE date = '2026-04-22'
AND status_code = 500
```

---

## Files in This Capstone

| File                        | Purpose                                                                             |
| --------------------------- | ----------------------------------------------------------------------------------- |
| `capstone/generate_logs.py` | Generates 1M synthetic web log records and uploads them to S3                       |
| `capstone/process_logs.py`  | PySpark job executed by EMR Serverless                                              |
| `capstone/orchestrate.py`   | Creates EMR Serverless app, uploads script, submits job, monitors job, reports cost |
| `capstone/cleanup.py`       | Deletes capstone S3 objects and EMR Serverless apps                                 |
| `capstone/test_capstone.py` | Local tests for generation, aggregation logic, and cost formula                     |

---

## Required Environment Variables

```powershell
$env:AWS_REGION="us-east-1"
$env:AWS_PROFILE="your-profile-name"
$env:EMR_S3_BUCKET="your-existing-bucket"
$env:EMR_SERVERLESS_ROLE_ARN="arn:aws:iam::<account-id>:role/<emr-serverless-job-role>"
```

Optional:

```powershell
$env:EMR_SUBNET_ID="subnet-xxxxxxxx"
```

---

## Run Order

From:

```powershell
D:\Workarea\StudyBook\tutorials\06_aws_emr
```

Run:

```powershell
python .\capstone\generate_logs.py
python .\capstone\orchestrate.py
```

After validation, clean up:

```powershell
python .\capstone\cleanup.py
```

---

## Local Test Command

The tests do **not** require AWS or EMR.

Run:

```powershell
pytest .\capstone\test_capstone.py -v
```

The tests validate:

* Generated records contain required fields
* Batch generation returns the expected count
* Logs span multiple days
* Error status codes are present
* Aggregation logic is correct
* Cost formula is sane

---

## Cost and Safety Notes

This capstone prefers **EMR Serverless** because it avoids long-running cluster costs.

However, cost still exists when the job runs. EMR Serverless charges for compute resources consumed during job execution.

To avoid runaway spend:

* Do not configure pre-initialized capacity unless you need faster startup
* Keep generated data under a known S3 prefix
* Use `capstone/cleanup.py` after testing
* Confirm S3 raw and processed prefixes are deleted
* Confirm EMR Serverless applications with prefix `studybook-log-processor-` are removed

Expected cleanup confirmation:

```text
✅ Cleanup complete. No ongoing charges.
```

---

## Interview Talking Points

### Why EMR Serverless?

EMR Serverless is a good fit when jobs are periodic, batch-oriented, or unpredictable. You avoid managing EC2 clusters and only pay for job execution resources.

### Why Parquet?

Parquet is columnar, compressed, and efficient for analytics. It reduces scan cost and speeds up downstream queries compared with raw CSV.

### Why partition by date and status code?

Most operational queries filter by time window and error class. Partitioning by `date` and `status_code` lets engines skip irrelevant files.

### Why aggregate before writing?

Aggregating reduces output size and gives downstream users a clean reliability fact table instead of forcing everyone to rescan raw logs.

### What can go wrong?

Common production issues include:

* S3 permission errors
* Missing input prefixes
* Bad timestamp parsing
* Too many small files
* Skewed endpoints causing slow tasks
* Over-partitioned output
* EMR Serverless role missing read/write access
* Forgetting cleanup and leaving unnecessary data in S3

---

## Senior Data Engineer Takeaway

This capstone demonstrates more than running Spark.

It shows the full data engineering loop:

```text
generate data → land raw data → process with Spark → write optimized output → monitor cost → clean up resources
```

That is the core pattern behind many real lakehouse, observability, and batch analytics systems.

```
```
