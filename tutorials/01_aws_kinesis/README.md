Here’s your complete **README.md** — clean, interview-focused, and aligned with everything you just built:

---

# 🚀 AWS Kinesis for Data Engineers (Hands-on Tutorial)

This project is a **production-style, end-to-end guide to AWS Kinesis**, built specifically for:

* 🎯 **Data Engineering interviews (Toyota-level prep)**
* 🧠 Deep understanding of **streaming systems**
* 🛠 Hands-on practice with **real AWS resources (boto3)**

All scripts are:

* ✅ Fully runnable
* ✅ Cost-safe (auto cleanup)
* ✅ Designed with real-world patterns

---

## 📂 Project Structure

```
01_streams_and_shards.py     → Stream creation, scaling, retention
02_producer_patterns.py      → Producers, batching, partition keys
03_consumer_patterns.py      → Consumers, shard iterators, lag
04_firehose_delivery.py      → Firehose → S3 delivery (optional)
05_monitoring_and_alarms.py  → Metrics, alarms, health report
capstone/
  sensor_pipeline.py         → End-to-end pipeline
  test_capstone.py           → pytest + moto tests
```

---

## ⚙️ Setup

### 1. Install dependencies

```bash
pip install boto3
```

### 2. Configure AWS

```bash
aws configure --profile study
```

### 3. Optional environment variables

```bash
export AWS_PROFILE=study
export AWS_REGION=us-east-1
```

---

## ⚠️ Cost Safety (IMPORTANT)

Every script:

* Uses **try/finally cleanup**
* Deletes all resources automatically
* Prints cost warnings like:

```
⚠️ COST: Kinesis stream ~$0.015/shard/hour
⚠️ COST: CloudWatch alarm ~$0.10/month
```

👉 You will NOT accidentally leave resources running.

---

## 🧠 What You’ll Learn (Core Concepts)

### 1. Kinesis Streams & Shards

* 1 shard supports:

  * **1 MB/sec writes**
  * **1000 records/sec**
  * **2 MB/sec reads**

👉 Key rule:

> Shard count = max(write MB/s, write records/s, read MB/s)

---

### 2. Producers (Critical for interviews)

You implemented:

* `PutRecord` → single record (ordering guaranteed)
* `PutRecords` → batch (up to 500 records)

#### Partition Key Strategies

| Strategy    | Pros              | Cons           |
| ----------- | ----------------- | -------------- |
| `entity_id` | Ordering          | Hot shard risk |
| `hashed`    | Even distribution | No ordering    |
| `salted`    | Handles hot keys  | No ordering    |

👉 Key takeaway:

> Partition key controls both ordering AND scaling.

---

### 3. Consumers

* Shard iterators:

  * `TRIM_HORIZON` → from beginning
  * `LATEST` → new data only

* Key metric:

  ```
  IteratorAgeMilliseconds
  ```

👉 Interview line:

> “High iterator age means the consumer is falling behind.”

---

### 4. Firehose (Managed Delivery)

* Sends data → **S3 / Redshift / OpenSearch**
* No consumer code required

#### Buffer tradeoffs

| Buffer | Files/hr | Size  | Latency |
| ------ | -------- | ----- | ------- |
| 30s    | 120      | small | low     |
| 300s   | 12       | large | high    |

👉 Key takeaway:

> Avoid small files for Athena performance.

---

### 5. Monitoring & Alarms

You implemented:

* Iterator lag alarm
* Write throttling alarm
* Shard utilization estimation
* Full health report

Example:

```
╔═══════════════════════════════════════╗
║  Kinesis Health Report               ║
╠═══════════════════════════════════════╣
║  Status:           ACTIVE             ║
║  Shards:           1                  ║
║  Iterator Age:     0 ms  ✓            ║
║  Write Throttled:  0     ✓            ║
║  Write Util:       ~12%  ✓            ║
╚═══════════════════════════════════════╝
```

👉 Key takeaway:

> Monitoring is what separates junior vs senior engineers.

---

## 🧪 Capstone Project

### 🚗 Toyota IoT Sensor Pipeline

Simulates:

* 20 sensors sending data every second
* Real-time ingestion + anomaly detection

### Architecture

```
Sensor Producer
    ↓
Kinesis Data Stream
    ↓
Consumer (detect anomalies)
    ↓
Firehose
    ↓
S3
```

---

## 🧠 Interview Cheat Sheet

### ⭐ Most Important Points

* Kinesis scaling = shard math
* Partition key = **distribution + ordering**
* Hot shard = biggest real-world problem
* Iterator age = consumer lag
* Firehose = managed delivery

---

### 🔥 Common Interview Questions

**Q: How do you scale Kinesis?**
→ Increase shard count

**Q: What causes throttling?**
→ Hot partition key or insufficient shards

**Q: How do you fix hot shards?**
→ Hashing or salting partition keys

**Q: Difference: Kinesis vs Kafka?**
→ Managed vs self-managed, shard vs partition

---

## ⚡ Key Insights You Discovered

* AWS APIs can be inconsistent (`OpenShardCount`)
* Metrics are delayed (CloudWatch lag)
* Cleanup must be **idempotent**
* Real systems require **monitoring + alerting**

👉 This is real-world engineering, not just tutorials. 

---

## 🚀 Next Steps

Run in order:

```
python 01_streams_and_shards.py
python 02_producer_patterns.py
python 03_consumer_patterns.py
python 04_firehose_delivery.py
python 05_monitoring_and_alarms.py
```

Then:

```
generate pipeline
generate tests
```

---

## 🎯 Final Thought

If you understand everything in this repo, you can confidently say:

> “I can design, build, scale, and monitor a real-time streaming pipeline on AWS.”

That’s exactly what interviewers are looking for.
