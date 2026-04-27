Below are two files to create in:

```powershell
D:\Workarea\StudyBook\tutorials\06_aws_emr
```

---

## `README.md`

````markdown
# AWS EMR for Data Engineers

This tutorial teaches AWS EMR from a data engineering perspective, moving from classic EMR clusters to EMR Serverless, Spark job submission, cost optimization, monitoring, and debugging.

The tutorial is designed for interview preparation and real-world AWS practice.

---

## What You Will Learn

By the end of this tutorial, you will understand:

- What AWS EMR is and when to use it
- How EMR clusters are structured
- How to submit PySpark jobs to EMR
- How EMR Serverless differs from classic EMR clusters
- How to estimate and reduce EMR cost
- How to monitor EMR workloads
- How to debug failed Spark jobs
- How to clean up AWS resources safely

---

## Files

| File | Purpose |
|---|---|
| `01_emr_cluster_basics.py` | EMR cluster creation, inspection, instance sizing, and termination |
| `02_spark_jobs_on_emr.py` | Submit PySpark jobs to an existing EMR cluster |
| `03_emr_serverless.py` | EMR Serverless application lifecycle and job cost estimation |
| `04_cost_optimization.py` | Offline cost calculator for Spot, On-Demand, and Serverless |
| `05_monitoring_and_bootstrap.py` | Bootstrap actions, CloudWatch metrics, alarms, and Spark log parsing |
| `cleanup_tutorial_resources.py` | Cleanup helper for resources created by the first five tutorials |
| `capstone/` | End-to-end EMR Serverless log processing project |

---

## Required Environment Variables

For offline demos, no AWS variables are required.

For live AWS demos, use:

```powershell
$env:AWS_PROFILE="study"
$env:AWS_REGION="us-east-1"
$env:EMR_S3_BUCKET="your-existing-bucket"
$env:EMR_SUBNET_ID="subnet-xxxxxxxx"
$env:EMR_EC2_KEY_PAIR="optional-key-pair"
$env:EMR_CLUSTER_ID="j-xxxxxxxxxxxxx"
$env:EMR_SERVERLESS_ROLE_ARN="arn:aws:iam::<account-id>:role/<role-name>"
$env:SNS_TOPIC_ARN="arn:aws:sns:us-east-1:<account-id>:<topic-name>"
````

---

## Recommended Run Order

### 1. EMR Cluster Basics

```powershell
python .\01_emr_cluster_basics.py
```

Without `EMR_S3_BUCKET` and `EMR_SUBNET_ID`, this runs safely in demo mode.

If those variables are set, it can create a real EMR cluster.

---

### 2. Spark Jobs on EMR

```powershell
python .\02_spark_jobs_on_emr.py
```

Without `EMR_CLUSTER_ID` and `EMR_S3_BUCKET`, this prints the generated PySpark job and does not submit anything.

If those variables are set, it submits a Spark step to an existing EMR cluster.

---

### 3. EMR Serverless

```powershell
python .\03_emr_serverless.py
```

Without `EMR_SERVERLESS_ROLE_ARN` and `EMR_S3_BUCKET`, this runs in simulated mode.

If those variables are set, it can create and start an EMR Serverless application, then clean it up.

---

### 4. Cost Optimization

```powershell
python .\04_cost_optimization.py
```

This is offline-only. It creates no AWS resources.

It compares:

* EMR Cluster On-Demand
* EMR Cluster Spot
* EMR Serverless

---

### 5. Monitoring and Bootstrap

```powershell
python .\05_monitoring_and_bootstrap.py
```

By default, this runs safely and demonstrates:

* Bootstrap script generation
* Spark log error parsing
* Debugging checklist

If `EMR_CLUSTER_ID`, `EMR_STEP_ID`, `EMR_S3_BUCKET`, or `SNS_TOPIC_ARN` are set, it can inspect logs or create CloudWatch alarms.

---

## Cleanup

Run this after experimenting with the first five tutorial files:

```powershell
python .\cleanup_tutorial_resources.py
```

This cleanup script attempts to remove:

* EMR clusters tagged or named for this tutorial
* EMR Serverless applications named `studybook-emr-serverless-*`
* CloudWatch alarms named `emr-*-low-memory` or `emr-*-high-pending`
* S3 tutorial prefixes:

  * `emr-scripts/`
  * `emr-logs/`
  * `emr-serverless-logs/`
  * `sample/category_output/`

The capstone has its own cleanup:

```powershell
python .\capstone\cleanup.py
```

---

## Cost Safety Notes

AWS EMR can create billable resources.

Always remember:

* EMR clusters use EC2 instances and can become expensive if left running
* EMR Serverless charges while jobs run
* Pre-initialized EMR Serverless capacity can charge while idle
* S3 objects and logs remain until deleted
* CloudWatch alarms may create small monitoring charges
* Always run cleanup after live demos

Expected cleanup confirmation:

```text
✅ Cleanup complete. No ongoing charges.
```

---

## Interview Talking Points

### What is EMR?

AWS EMR is a managed big data platform for running frameworks such as Spark, Hive, Hadoop, and Presto on AWS.

### EMR Cluster vs EMR Serverless

Use EMR clusters when you need full control over infrastructure, long-running workloads, custom networking, or custom bootstrap configuration.

Use EMR Serverless when you want to run batch jobs without managing clusters.

### Why use Spot instances?

Spot instances can significantly reduce EMR cluster cost, especially for fault-tolerant Spark workloads.

### Why use S3 for logs?

S3 keeps logs available after clusters terminate, which is critical for debugging failed jobs.

### What causes Spark jobs to fail on EMR?

Common causes include:

* S3 permission errors
* missing input data
* executor out-of-memory errors
* shuffle failures
* bad partitioning
* skewed data
* insufficient IAM role permissions

### What is the most important production habit?

Always design cleanup and cost controls before running live infrastructure.

---

## Suggested Next Steps

After finishing the first five tutorials:

1. Run the capstone
2. Add Glue Data Catalog integration
3. Query processed Parquet with Athena
4. Add Terraform for repeatable infrastructure
5. Add CloudWatch dashboards and alerts

````

---

## `cleanup_tutorial_resources.py`

```python
# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : cleanup_tutorial_resources.py
# Covers  : Cleanup resources created by tutorials 01-05
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket
# Run     : python cleanup_tutorial_resources.py
# ============================================================

from __future__ import annotations

import os
import time
from typing import Any

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_PROFILE = os.environ.get("AWS_PROFILE")
EMR_S3_BUCKET = os.environ.get("EMR_S3_BUCKET")

S3_PREFIXES = [
    "emr-scripts/",
    "emr-logs/",
    "emr-serverless-logs/",
    "sample/category_output/",
]

SERVERLESS_NAME_PREFIXES = [
    "studybook-emr-serverless-",
]

CLUSTER_NAME_PREFIXES = [
    "studybook-emr-basics-",
]

CLOUDWATCH_ALARM_PREFIXES = [
    "emr-",
]


def get_boto3_session() -> boto3.session.Session:
    if AWS_PROFILE:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return boto3.Session(region_name=AWS_REGION)


def get_emr_client() -> Any:
    return get_boto3_session().client("emr")


def get_emr_serverless_client() -> Any:
    return get_boto3_session().client("emr-serverless")


def get_s3_client() -> Any:
    return get_boto3_session().client("s3")


def get_cloudwatch_client() -> Any:
    return get_boto3_session().client("cloudwatch")


def delete_s3_prefix(bucket: str, prefix: str) -> int:
    s3 = get_s3_client()
    paginator = s3.get_paginator("list_objects_v2")
    deleted = 0

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        objects = [{"Key": item["Key"]} for item in page.get("Contents", [])]

        if not objects:
            continue

        s3.delete_objects(
            Bucket=bucket,
            Delete={"Objects": objects},
        )
        deleted += len(objects)

    return deleted


def cleanup_s3() -> int:
    if not EMR_S3_BUCKET:
        print("EMR_S3_BUCKET is not set. Skipping S3 cleanup.")
        return 0

    total = 0

    for prefix in S3_PREFIXES:
        count = delete_s3_prefix(EMR_S3_BUCKET, prefix)
        total += count
        print(f"Deleted {count} objects from s3://{EMR_S3_BUCKET}/{prefix}")

    return total


def terminate_matching_emr_clusters() -> int:
    emr = get_emr_client()
    terminated = 0

    active_states = [
        "STARTING",
        "BOOTSTRAPPING",
        "RUNNING",
        "WAITING",
    ]

    response = emr.list_clusters(ClusterStates=active_states)

    for cluster in response.get("Clusters", []):
        cluster_id = cluster["Id"]
        cluster_name = cluster["Name"]

        if not any(cluster_name.startswith(prefix) for prefix in CLUSTER_NAME_PREFIXES):
            continue

        print(f"Terminating EMR cluster: {cluster_name} ({cluster_id})")

        try:
            emr.terminate_job_flows(JobFlowIds=[cluster_id])
            terminated += 1
        except ClientError as exc:
            message = exc.response.get("Error", {}).get("Message", "").lower()
            if "already terminated" not in message:
                raise

    return terminated


def stop_and_delete_serverless_app(application_id: str) -> None:
    client = get_emr_serverless_client()

    try:
        response = client.get_application(applicationId=application_id)
        state = response["application"]["state"]

        if state not in {"STOPPED", "CREATED"}:
            client.stop_application(applicationId=application_id)

            start = time.time()
            while time.time() - start < 300:
                response = client.get_application(applicationId=application_id)
                state = response["application"]["state"]
                print(f"Stopping EMR Serverless app {application_id}: {state}")

                if state == "STOPPED":
                    break

                time.sleep(10)

        client.delete_application(applicationId=application_id)
        print(f"Deleted EMR Serverless app: {application_id}")

    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in {"ResourceNotFoundException", "ValidationException"}:
            return
        raise


def cleanup_serverless_apps() -> int:
    client = get_emr_serverless_client()
    paginator = client.get_paginator("list_applications")
    deleted = 0

    for page in paginator.paginate():
        for app in page.get("applications", []):
            app_name = app.get("name", "")
            app_id = app.get("id")

            if any(app_name.startswith(prefix) for prefix in SERVERLESS_NAME_PREFIXES):
                print(f"Cleaning EMR Serverless app: {app_name} ({app_id})")
                stop_and_delete_serverless_app(app_id)
                deleted += 1

    return deleted


def cleanup_cloudwatch_alarms() -> int:
    cloudwatch = get_cloudwatch_client()
    paginator = cloudwatch.get_paginator("describe_alarms")
    alarm_names: list[str] = []

    for page in paginator.paginate():
        for alarm in page.get("MetricAlarms", []):
            name = alarm.get("AlarmName", "")

            is_emr_alarm = (
                name.startswith("emr-")
                and (
                    name.endswith("-low-memory")
                    or name.endswith("-high-pending")
                )
            )

            if is_emr_alarm:
                alarm_names.append(name)

    deleted = 0

    for index in range(0, len(alarm_names), 100):
        batch = alarm_names[index:index + 100]
        if batch:
            cloudwatch.delete_alarms(AlarmNames=batch)
            deleted += len(batch)

    if deleted:
        print(f"Deleted CloudWatch alarms: {deleted}")
    else:
        print("Deleted CloudWatch alarms: 0")

    return deleted


def main() -> None:
    print("AWS EMR Tutorial Cleanup")
    print("=" * 72)

    total_s3 = cleanup_s3()
    total_clusters = terminate_matching_emr_clusters()
    total_apps = cleanup_serverless_apps()
    total_alarms = cleanup_cloudwatch_alarms()

    print("=" * 72)
    print(f"S3 objects deleted              : {total_s3}")
    print(f"EMR clusters termination started: {total_clusters}")
    print(f"EMR Serverless apps deleted     : {total_apps}")
    print(f"CloudWatch alarms deleted       : {total_alarms}")
    print("✅ Cleanup complete. No ongoing charges.")


if __name__ == "__main__":
    main()
````
