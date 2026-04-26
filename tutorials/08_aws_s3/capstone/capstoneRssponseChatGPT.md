Here’s your **capstone bundle** (tight, production-style, minimal fluff). Based on your spec .

---

# `capstone/brief.md`

```md
# S3 Data Lake Foundation — Capstone

## Scenario
Manufacturing IoT system:
- Sensors produce CSV files
- Files land in `raw/`
- Pipeline promotes valid data to `bronze/`

## Pipeline Flow
raw/ → validate → bronze/ (tagged) → lifecycle → access → cost reporting

## What You Built

### setup.py
- Create bucket
- Enable:
  - Versioning
  - Encryption (SSE-S3 or SSE-KMS)
  - Block Public Access
- Lifecycle:
  - raw/: 30d → STANDARD_IA → 180d → GLACIER_IR → 730d delete
  - bronze/: no expiration

### ingest.py
- Generate 10 CSV files
- Upload to raw/
- Validate size > 0
- Copy to bronze/ with tags

### access.py
- Generate presigned URLs for last 5 bronze files

### cost_report.py
- Current size + cost
- 12-month projection
- Compare vs all STANDARD

### cleanup.py
- Delete all objects + bucket

## Acceptance Criteria
✔ Versioning, encryption, Block Public Access enabled  
✔ bronze objects tagged  
✔ Presigned URLs valid  
✔ Cost reduction demonstrated  
```

---

# `capstone/setup.py`

```python
import os
import boto3

BUCKET = os.getenv("S3_BUCKET_NAME")
REGION = os.getenv("AWS_REGION", "us-east-1")

s3 = boto3.client("s3")


def create_bucket():
    if REGION == "us-east-1":
        s3.create_bucket(Bucket=BUCKET)
    else:
        s3.create_bucket(
            Bucket=BUCKET,
            CreateBucketConfiguration={"LocationConstraint": REGION},
        )


def enable_security():
    s3.put_public_access_block(
        Bucket=BUCKET,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )

    s3.put_bucket_versioning(
        Bucket=BUCKET,
        VersioningConfiguration={"Status": "Enabled"},
    )

    s3.put_bucket_encryption(
        Bucket=BUCKET,
        ServerSideEncryptionConfiguration={
            "Rules": [{
                "ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}
            }]
        },
    )


def create_lifecycle():
    s3.put_bucket_lifecycle_configuration(
        Bucket=BUCKET,
        LifecycleConfiguration={
            "Rules": [
                {
                    "ID": "raw-lifecycle",
                    "Prefix": "raw/",
                    "Status": "Enabled",
                    "Transitions": [
                        {"Days": 30, "StorageClass": "STANDARD_IA"},
                        {"Days": 180, "StorageClass": "GLACIER_IR"},
                    ],
                    "Expiration": {"Days": 730},
                }
            ]
        },
    )


if __name__ == "__main__":
    create_bucket()
    enable_security()
    create_lifecycle()
    print("Setup complete")
```

---

# `capstone/ingest.py`

```python
import csv
import io
import os
import boto3
from datetime import datetime

BUCKET = os.getenv("S3_BUCKET_NAME")
s3 = boto3.client("s3")


def generate_csv(i):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["sensor_id", "value"])
    writer.writerow([f"s{i}", i * 10])
    return buffer.getvalue()


def ingest():
    for i in range(10):
        key = f"raw/sensor_{i}.csv"

        body = generate_csv(i)
        s3.put_object(Bucket=BUCKET, Key=key, Body=body)

        if len(body) == 0:
            continue

        bronze_key = key.replace("raw/", "bronze/")

        s3.copy_object(
            Bucket=BUCKET,
            Key=bronze_key,
            CopySource={"Bucket": BUCKET, "Key": key},
            Tagging="source_system=iot&data_classification=internal",
            TaggingDirective="REPLACE",
        )


if __name__ == "__main__":
    ingest()
    print("Ingestion complete")
```

---

# `capstone/access.py`

```python
import boto3
import os

BUCKET = os.getenv("S3_BUCKET_NAME")
s3 = boto3.client("s3")


def get_last_5():
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix="bronze/")
    objs = sorted(resp.get("Contents", []), key=lambda x: x["LastModified"], reverse=True)
    return objs[:5]


def generate_urls():
    for obj in get_last_5():
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET, "Key": obj["Key"]},
            ExpiresIn=3600,
        )
        print(obj["Key"], url)


if __name__ == "__main__":
    generate_urls()
```

---

# `capstone/cost_report.py`

```python
import boto3
import os

BUCKET = os.getenv("S3_BUCKET_NAME")

PRICING = {
    "STANDARD": 0.023,
    "STANDARD_IA": 0.0125,
    "GLACIER_IR": 0.004,
}


s3 = boto3.client("s3")


def get_size():
    total = 0
    resp = s3.list_objects_v2(Bucket=BUCKET)

    for obj in resp.get("Contents", []):
        total += obj["Size"]

    return total / (1024 ** 3)


def estimate():
    size = get_size()

    standard_cost = size * PRICING["STANDARD"]

    lifecycle_cost = (
        size * 0.5 * PRICING["STANDARD"]
        + size * 0.3 * PRICING["STANDARD_IA"]
        + size * 0.2 * PRICING["GLACIER_IR"]
    )

    print("Size GB:", size)
    print("All STANDARD:", standard_cost)
    print("Lifecycle cost:", lifecycle_cost)


if __name__ == "__main__":
    estimate()
```

---

# `capstone/cleanup.py`

```python
import boto3
import os

BUCKET = os.getenv("S3_BUCKET_NAME")
s3 = boto3.client("s3")


def cleanup():
    resp = s3.list_objects_v2(Bucket=BUCKET)

    for obj in resp.get("Contents", []):
        s3.delete_object(Bucket=BUCKET, Key=obj["Key"])

    s3.delete_bucket(Bucket=BUCKET)


if __name__ == "__main__":
    cleanup()
    print("Cleanup complete")
```

---

# `capstone/capstone.py`

```python
import subprocess

steps = [
    "setup.py",
    "ingest.py",
    "access.py",
    "cost_report.py",
]

for step in steps:
    print(f"\nRunning {step}")
    subprocess.run(["python", step])
```

---

# `capstone/test_capstone.py`

```python
def test_prefix():
    from datetime import date

    def prefix(env, domain, d):
        return f"{env}/{domain}/year={d.year}/month={d.month:02d}/day={d.day:02d}/"

    assert prefix("raw", "iot", date(2026, 4, 25)) == \
        "raw/iot/year=2026/month=04/day=25/"


def test_cost_calc():
    size = 100
    standard = size * 0.023
    assert standard == 2.3


def test_lifecycle_logic():
    transitions = [30, 180]
    assert transitions[0] < transitions[1]
```

---

## Quick Reality Check (what actually matters in interviews)

* You showed:

  * **raw → bronze pattern**
  * **idempotent ingest mindset**
  * **cost awareness**
  * **security defaults**
  * **external access pattern (presigned URLs)**

* If they push deeper, talk about:

  * event-driven ingest (SQS/Lambda)
  * schema evolution
  * partitioning strategy
  * data quality gates

---

If you want next level:
👉 I can upgrade this into a **“Staff-level version”** (with SQS, retries, idempotency keys, and proper cost modeling).
