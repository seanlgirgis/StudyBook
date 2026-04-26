# AWS Tutorial — Known Gotchas & Required Rules
# Last updated: 2026-04-26
# Source: Lessons learned running 08_aws_s3 tutorials against real AWS account
#
# INCLUDE THIS SECTION IN EVERY AWS TUTORIAL PROMPT sent to ChatGPT.
# Paste it right before the ===== START ===== line.

===== AWS GOTCHAS — APPLY TO ALL FILES =====

## CLEANUP — NON-NEGOTIABLE (read this first)

Runaway AWS costs are a real risk. Every resource created during a tutorial MUST be
deleted before the script exits. These rules are MANDATORY, not suggestions.

### Rule C1 — Every main() that creates resources uses try/finally
The cleanup() function MUST be called in a finally block so it runs even if the
script crashes mid-way. There are NO exceptions to this rule.

```python
def main():
    resources = []
    try:
        resource_id = create_something()
        resources.append(resource_id)
        # ... rest of demo ...
    finally:
        cleanup(resources)  # always runs, even on exception
```

### Rule C2 — Every file that creates resources has its own cleanup() function
Do not rely on a separate cleanup.py to clean up what a setup file created.
Each file cleans up after itself in its own finally block.

### Rule C3 — Cleanup must be idempotent and silent on "already deleted"
Cleanup should not crash if the resource was already deleted (e.g., script run twice).
Always catch ResourceNotFoundException / NoSuchBucket / NoSuchEntity and continue.

```python
def cleanup_bucket(bucket_name):
    try:
        s3_resource = boto3.resource("s3")
        s3_resource.Bucket(bucket_name).object_versions.delete()
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Deleted bucket: {bucket_name}")
    except ClientError as e:
        if e.response["Error"]["Code"] in ("NoSuchBucket", "404"):
            print(f"Bucket already gone: {bucket_name}")
        else:
            raise
```

### Rule C4 — Print a COST WARNING when any billable resource is created
Immediately after creating any resource that incurs ongoing cost, print a warning.

```python
print(f"⚠️  COST: Kinesis stream '{stream_name}' is now running. Charges apply.")
print(f"    Run cleanup() or this script will delete it automatically at exit.")
```

### Rule C5 — Per-service dangerous resources (know these by heart)

| Service | Resource | Why dangerous | Cleanup method |
|---|---|---|---|
| Kinesis | Stream | $0.015/shard/hour — never idle | `delete_stream(StreamName=name)` |
| EMR | Cluster | $0.10-$5+/hour per instance | `terminate_job_flows([cluster_id])` |
| Glue | Job run | $0.44/DPU-hour, 2 DPU minimum | `delete_job(JobName=name)` |
| RDS | Instance | Hourly even when idle | `delete_db_instance(SkipFinalSnapshot=True)` |
| SageMaker | Endpoint | Hourly even with 0 traffic | `delete_endpoint(EndpointName=name)` |
| Step Functions | State machine | No ongoing cost but clean hygiene | `delete_state_machine(stateMachineArn=arn)` |
| CloudWatch | Log group | $0.50/GB ingestion + storage | `delete_log_group(logGroupName=name)` |
| CloudWatch | Alarms | $0.10/alarm/month | `delete_alarms(AlarmNames=[name])` |
| CloudWatch | Dashboard | $3/dashboard/month | `delete_dashboards(DashboardNames=[name])` |
| S3 | Versioned bucket | Versions accumulate silently | `object_versions.delete()` then `delete_bucket()` |
| IAM | Role/Policy | No cost but pollutes account | `delete_role` + detach policies first |

### Rule C6 — capstone/cleanup.py must delete EVERYTHING the capstone created
The capstone cleanup.py is the "nuclear option" — run it and the AWS account is
returned to exactly the state it was in before. It must:
- Delete all resources created by setup.py, ingest.py, and any other capstone files
- Use object_versions.delete() for any versioned S3 bucket
- Handle "already deleted" without crashing
- Print a confirmation line for each deleted resource
- End with: `print("✅ All capstone resources deleted. No ongoing charges.")`

### Rule C7 — Emergency one-liner in README.md
Every README.md must include an emergency cleanup one-liner for when you need
to stop immediately and kill everything:

```powershell
# Emergency cleanup — run this if the script crashes before cleanup() fires
python -c "
import os, boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket(os.getenv('S3_BUCKET_NAME', ''))
if bucket.name:
    bucket.object_versions.delete()
    bucket.delete()
    print('Bucket deleted')
"
```
(Adapt the one-liner to the specific resource type of the tutorial.)

---

## 1. S3 Select Deprecation
AWS deprecated S3 Select in mid-2024. On newly created buckets, `select_object_content`
raises `MethodNotAllowed`. Rule: never rely on S3 Select as a core mechanism.
If you must show it, ALWAYS wrap in try/except and degrade gracefully:
```python
try:
    response = s3.select_object_content(...)
except ClientError as e:
    if e.response["Error"]["Code"] == "MethodNotAllowed":
        print("WARNING: S3 Select is deprecated on this bucket. Skipping.")
        return ""
    raise
```

## 2. Versioned Bucket Cleanup
If a bucket has versioning enabled, `delete_object` creates delete markers —
old versions remain and accumulate cost. Standard `aws s3 rb --force` also fails.
Rule: ALL cleanup for versioned buckets MUST use:
```python
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket(BUCKET_NAME)
bucket.object_versions.delete()
s3_client.delete_bucket(Bucket=BUCKET_NAME)
```

## 3. Multipart Upload File Size
Generating 150MB synthetic files causes hangs on constrained connections.
Rule: use 15MB files and lower TransferConfig thresholds so multipart still triggers:
```python
config = TransferConfig(
    multipart_threshold=5 * 1024 * 1024,   # 5 MB
    multipart_chunksize=5 * 1024 * 1024,   # 5 MB per part
    max_concurrency=4,
    use_threads=True,
)
```

## 4. Resource Name Collisions
Hardcoded names cause `BucketAlreadyExists` or `EntityAlreadyExists` on re-runs.
Rule: always read from env vars with uuid fallback:
```python
import uuid
BUCKET_NAME = os.getenv("S3_BUCKET_NAME") or f"studybook-tutorial-{uuid.uuid4().hex[:8]}"
```

## 5. us-east-1 CreateBucket Quirk
Do NOT pass `CreateBucketConfiguration` for us-east-1. Required for all other regions.
```python
if region == "us-east-1":
    s3.create_bucket(Bucket=name)
else:
    s3.create_bucket(Bucket=name,
                     CreateBucketConfiguration={"LocationConstraint": region})
```

## 6. Optional Environment Variables
Gate optional features — do not crash if env var is absent:
```python
SQS_QUEUE_ARN = os.getenv("SQS_QUEUE_ARN")
if SQS_QUEUE_ARN:
    configure_sqs_notification(...)
else:
    print("Skipping SQS notification: SQS_QUEUE_ARN not set.")
```

## 7. AWS Profile
Local profile is `study`. Standard pattern:
```python
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
```

## 8. Environment Setup (before running any AWS tutorial)
```powershell
cd D:\Workarea\StudyBook\tutorials\NN_topic
..\..\env_setter.ps1 -NonInteractive
$env:AWS_PROFILE = "study"
$env:AWS_REGION  = "us-east-1"
```

===== END AWS GOTCHAS =====
