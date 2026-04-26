Good call — time to move into the capstone 🚀

## 📁 Create the capstone directory

From your current project root:

```powershell
mkdir capstone
cd capstone
```

Your structure should now look like:

```text
01_aws_kinesis/
│
├── 01_streams_and_shards.py
├── 02_producer_patterns.py
├── 03_consumer_patterns.py
├── 04_firehose_delivery.py
├── 05_monitoring_and_alarms.py
│
└── capstone/
    └── (next files go here)
```

---

## 🎯 What’s coming next

Inside `capstone/`, we’ll build a **real system**, not just demos:

### 🏭 Toyota IoT Pipeline

* 20 sensors streaming data
* Real-time ingestion
* Anomaly detection
* Monitoring + health checks

---

## 👉 Next step

Say:

**`generate pipeline`**

That will create:

```
capstone/sensor_pipeline.py
```

This is the **most important file in the whole project** — it ties everything together like a real production system.
---
Excellent — the capstone pipeline is working end-to-end.

You validated:

* ✅ 2-shard Kinesis stream
* ✅ CloudWatch alarms
* ✅ 1000-record producer batch
* ✅ anomaly detection
* ✅ multi-shard consumer reads
* ✅ cleanup of alarms + stream

The results look healthy:

```text
Records sent       : 1000
Records failed     : 0
Anomalies detected : 106 (10.6%)
Hot shard risk     : No
```

That `10.6%` anomaly rate matches the intended ~10% anomaly simulation.

Next:

**generate tests**

---
This one’s straightforward — your code is fine, you’re just missing a dependency.

## ❌ Problem

```
ModuleNotFoundError: No module named 'moto'
```

## ✅ Fix

Install **moto with the right extras**:

```powershell
pip install "moto[kinesis,cloudwatch]"
```

If that gives issues on Windows (sometimes it does), use:

```powershell
pip install moto
```

---

## 🔁 Then rerun

```powershell
pytest capstone/test_capstone.py -v
```

---

## 🧠 What `moto` is (important for interviews)

`moto` is a **mock AWS library** that lets you:

* Fake Kinesis, S3, CloudWatch, etc.
* Run tests **without real AWS calls**
* Avoid cost + speed up tests

👉 Interview one-liner:

> “I use moto to mock AWS services in unit tests so tests run locally without hitting real infrastructure.”

---

## ⚠️ Common gotcha (you might hit next)

If you see:

```
ImportError: cannot import name 'mock_aws'
```

Run:

```powershell
pip install -U moto
```

---

## 🚀 After this

Once tests pass, you’re done with the full stack:

* Streams ✅
* Producers ✅
* Consumers ✅
* Firehose ✅
* Monitoring ✅
* Capstone pipeline ✅
* Tests ✅

👉 That’s a **complete production-grade streaming system**.

---

If tests fail after install, paste the error — we’ll fix it fast.


---

Perfect. ✅

You now have a complete AWS Kinesis learning project:

* 5 runnable tutorial files
* Self-cleaning AWS demos
* Capstone IoT pipeline
* 12 passing pytest/moto tests

The warnings are from `botocore`, not your code. You can ignore them.

Final status:

```text
12 passed
0 failed
```

This is interview-ready.
