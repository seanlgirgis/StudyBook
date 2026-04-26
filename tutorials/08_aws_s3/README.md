# AWS S3 Data Engineering Tutorial

This directory contains a hands-on tutorial for learning AWS S3 from a Data Engineering perspective. The scripts are designed to be run sequentially, demonstrating real-world S3 interactions, security best practices, and pipeline patterns using `boto3`.

## Prerequisites

Before running the scripts, ensure you have initialized your Python environment and set the necessary environment variables. The tutorial assumes you are using the `study` AWS profile.

```powershell
# Navigate to the tutorial directory
cd D:\Workarea\StudyBook\tutorials\08_aws_s3

# Load the StudyBook Python environment
..\..\env_setter.ps1 -NonInteractive

# Set the AWS Profile and generate a unique bucket name for the session
$env:AWS_PROFILE = "study"
$env:S3_BUCKET_NAME = "aws-s3-tutorial-study-$(Get-Random)"
```

**Important:** Keep this terminal session open to run all Phase 1 scripts, as they share the `$env:S3_BUCKET_NAME` variable.

---

## Phase 1: Core S3 Setup Scripts

Run these scripts from the `tutorials/08_aws_s3` directory.

### 1. Fundamentals (`01_s3_fundamentals.py`)
```powershell
python setup\01_s3_fundamentals.py
```
**What it does:** 
Creates your S3 bucket, enables versioning, and demonstrates how to upload files with metadata and tags. It also shows how to paginate through objects and download them. 
**Takeaway:** Never hardcode credentials; always use metadata/tags for tracking data lineage and cost allocation.

### 2. Multipart Uploads & Streaming (`02_s3_multipart_and_streaming.py`)
```powershell
python setup\02_s3_multipart_and_streaming.py
```
**What it does:** 
Generates a synthetic file and uploads it using both manual multipart logic and the automated `boto3.s3.transfer.TransferConfig`. It also demonstrates streaming lines from an object without downloading the entire file into memory.
**Takeaway:** Use `TransferConfig` for large pipeline files to leverage automated concurrency and retries. Stream files for memory-safe processing.

### 3. Security and Access (`03_s3_security_and_access.py`)
```powershell
python setup\03_s3_security_and_access.py
```
**What it does:** 
Evaluates the bucket's security posture. It enables "Block Public Access", applies default server-side encryption (SSE-S3/KMS), and attaches a bucket policy enforcing HTTPS/TLS. Finally, it generates presigned URLs for temporary, secure data access.
**Takeaway:** S3 buckets should be locked down by default. Use presigned URLs for temporary vendor/partner access rather than long-lived IAM keys.

### 4. Lifecycle and Cost Management (`04_s3_lifecycle_and_cost.py`)
```powershell
python setup\04_s3_lifecycle_and_cost.py
```
**What it does:** 
Configures lifecycle rules to automatically transition older files to cheaper storage tiers (like Glacier) and calculates estimated costs based on storage classes.
**Takeaway:** Automated lifecycle rules are crucial for cost-effective data lakes. Storing old, rarely accessed data in `STANDARD` is an expensive anti-pattern.

### 5. Event Notifications & Patterns (`05_s3_event_notifications_and_patterns.py`)
```powershell
python setup\05_s3_event_notifications_and_patterns.py
```
**What it does:** 
Demonstrates the "Copy-on-Ingest" lakehouse pattern (moving data from `raw/` to `bronze/`), explains how to design optimal S3 prefixes (e.g., partitioned by year/month/day), and shows how to configure S3 Inventory.
**Takeaway:** Prefix design is critical for performance. Prefer partitioned prefixes and S3 Inventory over brute-force `list_objects_v2` calls.

---

## Phase 2: Capstone Project

The Capstone project simulates an end-to-end pipeline ingestion scenario. To avoid conflicts with the previous bucket, we generate a new bucket specifically for the capstone.

```powershell
# Set a new bucket name for the capstone
$env:S3_BUCKET_NAME = "aws-s3-tutorial-capstone-study-$(Get-Random)"

# Create infrastructure (Bucket, Security, Lifecycle)
python capstone\setup.py

# Ingest sample data
python capstone\ingest.py

# Validate the pipeline
python capstone\test_capstone.py

# Destroy the capstone infrastructure (cleans up all versions and buckets)
python capstone\cleanup.py
```

## Cleanup Note
If you stop testing halfway through Phase 1, you can cleanly delete your bucket using Python (this is necessary because versioning is enabled, meaning standard `aws s3 rb --force` will fail):

```powershell
python -c "import os, boto3; s3=boto3.resource('s3'); b=s3.Bucket(os.getenv('S3_BUCKET_NAME')); b.object_versions.delete(); b.delete()"
```
