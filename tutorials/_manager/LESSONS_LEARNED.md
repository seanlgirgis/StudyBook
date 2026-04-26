# Lessons Learned — Tutorial Execution
# Updated as real problems are found during testing.
# Apply these before generating any new tutorial prompt.

---

## 2026-04-26 - State Sync Lessons

### L7: Status labels must include verification source

When marking a tutorial as "working", always tag the source:

- `independently verified` (this session run output exists), or
- `user-reported working` (owner confirmed, not re-run now).

This prevents accidental over-claiming in manager docs.

### L8: Two PySpark tracks are intentional and must stay distinct

- `02_pyspark` is the canonical local `local[*]` track.
- `02_PySpark_Docker` is a valid Docker/Spark-cluster variant.

Do not mark `02_PySpark_Docker` as duplicate/archive candidate unless owner asks.

### L9: Manager docs should be regenerated from repo scan, not old narrative

`HANDOFF_REPORT.md`, `ROADMAP.md`, and `PROJECT_STATE.md` can drift quickly.
Use folder/file scan outputs as first source of truth, then merge owner-provided run status.

---

## CLEANUP POLICY — NON-NEGOTIABLE (2026-04-26)

Runaway AWS costs are a real risk. The following rules apply to every AWS tutorial.

### The five cleanup rules

**C1 — try/finally in every main()**
```python
def main():
    created = []
    try:
        r = create_resource()
        created.append(r)
        # demo code ...
    finally:
        cleanup(created)   # runs even if demo crashes
```

**C2 — Each file cleans up its own resources**
Do not rely on a separate cleanup.py for resources created in a setup file.
Every file is self-contained: creates → demos → deletes.

**C3 — Idempotent cleanup (never crash on "already deleted")**
```python
except ClientError as e:
    if e.response["Error"]["Code"] in ("NoSuchBucket", "ResourceNotFoundException", "404"):
        print(f"Already gone: {name}")
    else:
        raise
```

**C4 — Cost warning on creation**
```python
print(f"⚠️  COST: Kinesis stream '{name}' is running. Charges apply until deleted.")
```

**C5 — Confirm at end**
```python
print("✅ Cleanup complete. No ongoing charges.")
```

### Dangerous resources (charge while idle)

| Resource | Cost | Must-delete method |
|---|---|---|
| Kinesis Stream | $0.015/shard/hr | `delete_stream(StreamName=name)` |
| EMR Cluster | $0.10–$5+/hr | `terminate_job_flows([cluster_id])` |
| Glue Job Run | $0.44/DPU-hr | `delete_job(JobName=name)` |
| CloudWatch Alarm | $0.10/alarm/mo | `delete_alarms(AlarmNames=[name])` |
| CloudWatch Dashboard | $3/dashboard/mo | `delete_dashboards(DashboardNames=[name])` |
| CloudWatch Log Group | $0.50/GB ingest | `delete_log_group(logGroupName=name)` |
| S3 Versioned Bucket | versions accumulate | `object_versions.delete()` → `delete_bucket()` |

### Emergency one-liner (when script crashes before cleanup fires)
Add this to every README.md — adapt resource type per topic:
```powershell
python -c "import os,boto3; b=boto3.resource('s3').Bucket(os.getenv('S3_BUCKET_NAME','')); b.object_versions.delete(); b.delete(); print('done')"
```

---

## 2026-04-26 — From 08_aws_s3 execution

### L1: S3 Select is deprecated (AWS, mid-2024)
**Symptom:** `ClientError: MethodNotAllowed` on `select_object_content`
**Fix:** Wrap in try/except, catch `MethodNotAllowed`, print warning and return gracefully.
**Applies to:** Any tutorial that touches S3 Select (08_aws_s3 file 05, any Athena/Glue tutorial).

### L2: Versioned bucket cleanup requires boto3.resource
**Symptom:** `BucketNotEmpty` when calling `delete_bucket` on a versioned bucket.
**Why:** `delete_object` in a versioned bucket creates delete markers, not permanent deletes.
**Fix:** Use `boto3.resource("s3").Bucket(name).object_versions.delete()` then `delete_bucket()`.
**Applies to:** Every cleanup.py that touches a versioned S3 bucket.
**Quick command:**
```python
python -c "import os, boto3; s3=boto3.resource('s3'); b=s3.Bucket(os.getenv('S3_BUCKET_NAME')); b.object_versions.delete(); b.delete()"
```

### L3: Multipart demo with 150MB file hangs
**Symptom:** Script hangs indefinitely during synthetic file generation or upload.
**Fix:** Use 15MB files. Lower `TransferConfig` thresholds to 5MB so multipart still triggers.
**Applies to:** Any tutorial demonstrating multipart uploads (S3, EMR, Glue).

### L4: Hardcoded resource names fail on re-run
**Symptom:** `BucketAlreadyExists` or `EntityAlreadyExists` on second run.
**Fix:** Always read names from env vars. Add `uuid`/`Get-Random` fallback.
**Applies to:** Every AWS tutorial that creates resources.

### L5: us-east-1 CreateBucket quirk
**Symptom:** `InvalidLocationConstraint` when creating bucket in us-east-1.
**Fix:** Do NOT pass `LocationConstraint` for us-east-1. All other regions require it.
**Applies to:** 08_aws_s3, any tutorial that creates S3 buckets.

### L6: Optional env vars must not crash
**Symptom:** `ValueError` or `TypeError` when SQS_QUEUE_ARN, SNS_TOPIC_ARN, etc. not set.
**Fix:** Gate optional features: `if SQS_QUEUE_ARN: ... else: print("Skipping...")`
**Applies to:** Any tutorial with optional integrations (notifications, alerts, etc.).

---

## General Rules Established

### R1: README.md is required for every topic
08_aws_s3 has a good README with prereqs, phase structure, exact commands, takeaways.
All future tutorials must include one. Add `"generate readme"` step between file 05 and capstone.

### R2: AWS Profile is "study"
Local AWS profile is `study`. Template previously said "may be None — use default". Fixed.
All AWS tutorials: `AWS_PROFILE = os.getenv("AWS_PROFILE", "study")`

### R3: env_setter.ps1 must be called before running AWS tutorials
```powershell
cd D:\Workarea\StudyBook\tutorials\NN_topic
..\..\env_setter.ps1 -NonInteractive
$env:AWS_PROFILE = "study"
```

### R4: Docker Kafka bootstrap is 29092, not 9092
The studybook_core stack maps the external listener to 29092. Template was wrong. Fixed.

### R5: Docker Postgres user is "studybook", not "postgres"
The studybook_core stack uses user=studybook, db=studybook, password=studybook. Fixed.

### R6: Save raw ChatGPT response as chatgpt_response.md in capstone/
Useful for debugging when generated code has issues. Keep it, rename consistently.

---

### R7: Cleanup is non-negotiable — runaway cost prevention
Every AWS tutorial file that creates resources MUST:
- Wrap demo code in try/finally with cleanup() in the finally block
- Have its own cleanup() — not rely on a separate file
- Catch "already deleted" errors silently
- Print ⚠️ COST WARNING after creating billable resources
- Print ✅ Cleanup complete. No ongoing charges. at end of cleanup()
The AWS_GOTCHAS.md has the full per-service dangerous resource table and patterns.

---

## Files Updated Based on These Lessons

| File | Change |
|---|---|
| `tutorials/_meta/AWS_GOTCHAS.md` | Created — paste into all AWS prompts; expanded with full cleanup policy |
| `tutorials/_meta/MASTER_PROMPT_TEMPLATE.md` | Fixed Docker ports/users, added README step, added hard cleanup rules to CODING STANDARDS |
| `tutorials/_manager/prompting_workflows/tutorials.md` | Added README step, AWS_GOTCHAS reference, updated directory structure |
| `tutorials/_manager/LESSONS_LEARNED.md` | Added cleanup policy section with C1-C5 rules and dangerous resource table |
| `tutorials/01_aws_kinesis/prompt.md` | Added CLEANUP RULES block to INFRASTRUCTURE NOTES |
| `tutorials/04_aws_step_functions/prompt.md` | Added CLEANUP RULES block to INFRASTRUCTURE NOTES |
| `tutorials/06_aws_emr/prompt.md` | Added CLEANUP RULES block to INFRASTRUCTURE NOTES |
| `tutorials/07_aws_glue/prompt.md` | Added CLEANUP RULES block to INFRASTRUCTURE NOTES |
| `tutorials/08_aws_s3/prompt.md` | Added CLEANUP RULES block to INFRASTRUCTURE NOTES |
| `tutorials/09_aws_cloudwatch/prompt.md` | Added CLEANUP RULES block to INFRASTRUCTURE NOTES |
