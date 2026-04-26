```markdown
# 🎓 Lecture: Building a Real-Time IoT Streaming Pipeline with AWS Kinesis

## 📍 Context

This capstone simulates a **Toyota manufacturing plant** where:

- 20 sensors stream data every second
- Data is processed in real-time
- Anomalies are detected
- System health is monitored

This is not a toy example — it mirrors real production systems.

---

## 🏗️ Architecture Overview

```

Sensor Producer
↓
Kinesis Data Stream (2 shards)
↓
Consumer (Anomaly Detection)
↓
(Optional) Firehose → S3
↓
CloudWatch Monitoring + Alarms

````

---

## 🔁 Data Flow Explained

### 1. Producer Layer

- Generates synthetic sensor readings:
  - temperature (°C)
  - pressure (PSI)
- Sends data using `PutRecords` (batching)
- Partition key = `sensor_id`

👉 Why?
- Preserves **ordering per sensor**
- Enables parallel processing across shards

---

### 2. Kinesis Data Stream

- 2 shards used
- Each shard supports:
  - 1 MB/sec write
  - 1000 records/sec
  - 2 MB/sec read

👉 Key concept:
> Shard count is determined by throughput requirements.

---

### 3. Consumer Layer

- Reads all shards using `TRIM_HORIZON`
- Decodes JSON payloads
- Detects anomalies

```python
value > threshold[type]
````

Thresholds:

* Temperature > 85°C
* Pressure > 120 PSI

---

### 4. Anomaly Detection

* ~10% of readings are intentionally anomalous
* Verified in run:

```
Anomalies detected: 106 (10.6%)
```

👉 This matches expected simulation — system is behaving correctly.

---

### 5. Monitoring Layer (CloudWatch)

Metrics tracked:

* `IteratorAgeMilliseconds` → consumer lag
* `WriteProvisionedThroughputExceeded` → throttling
* `IncomingBytes` → throughput

---

## 🚨 Alarm Design

Two alarms created:

### 1. Consumer Lag Alarm

```
IteratorAgeMilliseconds > 60,000 ms
```

👉 Meaning:

* Consumer is falling behind

---

### 2. Write Throttling Alarm

```
WriteProvisionedThroughputExceeded > 0 for 5 minutes
```

👉 Meaning:

* Not enough shards OR bad partition key

---

## ⚠️ Hot Shard Analysis

From your run:

```
Top shard usage: 60%
Hot shard risk: No
```

👉 Rule:

> Any shard receiving >60% traffic is risky

Why it matters:

* Causes throttling
* Reduces parallelism

---

## 📊 Consumer Behavior

Observed:

```
Read 100 records per shard batch
IteratorAgeMs initially > 0
Then drops to 0
```

👉 Interpretation:

* Consumer catches up successfully
* System is not backlogged

---

## 🧠 Key Engineering Insights

### 1. Partition Key is Critical

Controls:

* Data distribution
* Ordering guarantees

---

### 2. Kinesis is Pull-Based

* Consumers poll using shard iterators
* Not push-based like Kafka consumers

---

### 3. CloudWatch Metrics are Delayed

* Metrics may show `NO_DATA`
* This is normal in short-lived demos

---

### 4. Cleanup Must Be Guaranteed

All scripts use:

```python
try:
    ...
finally:
    cleanup()
```

👉 Prevents:

* Unexpected AWS charges
* Resource leaks

---

## 🧪 Testing Strategy

* Uses `moto` to mock AWS
* No real AWS calls in tests
* Fast + safe

Example:

```python
@mock_aws
def test_producer_send_batch_returns_stats():
```

---

## 🧠 Interview Takeaways

### ⭐ Core Concepts

* Kinesis scaling = shard math
* Partition key = distribution + ordering
* Iterator age = lag
* Hot shard = major failure mode

---

### 🔥 Common Questions

**Q: How do you scale Kinesis?**
→ Increase shards

**Q: What causes throttling?**
→ Hot partition key or insufficient shards

**Q: How do you fix hot shards?**
→ Hashing or salting partition keys

**Q: Kinesis vs Firehose?**
→ Streams = processing
→ Firehose = delivery

---

## 🚀 Final Summary

You built a system that:

* Ingests real-time data
* Processes it with low latency
* Detects anomalies
* Monitors system health
* Cleans up safely

---

## 🎯 One-Line Pitch

> “I designed and implemented a real-time IoT streaming pipeline using AWS Kinesis with anomaly detection, monitoring, and fault-safe cleanup.”

---

## 🏁 Status

```
Records sent       : 1000
Records failed     : 0
Anomalies detected : ~10%
Hot shard risk     : No
System health      : OK
```

---

This is production-grade thinking. 

```

---

## 💡 Why this is powerful

This file turns your project into:

- 📚 A teaching artifact  
- 💼 A portfolio piece  
- 🧠 An interview storytelling script  

---

If you want next level:
👉 I can turn this into a **system design whiteboard answer (FAANG style)** or **resume bullet points**.
```
