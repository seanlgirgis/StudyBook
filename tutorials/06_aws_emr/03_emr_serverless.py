# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : 03_emr_serverless.py
# Covers  : EMR Serverless applications, job runs, lifecycle, and cost estimation
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket
# Run     : python 03_emr_serverless.py
# ============================================================

from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError


# Environment variables used by this file:
# - AWS_REGION: AWS region where EMR Serverless runs, for example us-east-1.
# - AWS_PROFILE: Optional named AWS CLI profile for local development.
# - EMR_S3_BUCKET: S3 bucket for scripts, logs, input, and output.
# - EMR_SUBNET_ID: Required by tutorial standard; not directly used by simple serverless demo.
# - EMR_SERVERLESS_ROLE_ARN: IAM role ARN used by EMR Serverless job runs.
#
# Cost note:
# EMR Serverless charges for vCPU, memory, and storage resources consumed by jobs.
# Pre-initialized capacity can reduce cold starts but may accrue charges while idle.

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_PROFILE = os.environ.get("AWS_PROFILE")
EMR_S3_BUCKET = os.environ.get("EMR_S3_BUCKET")
EMR_SUBNET_ID = os.environ.get("EMR_SUBNET_ID")
EMR_SERVERLESS_ROLE_ARN = os.environ.get("EMR_SERVERLESS_ROLE_ARN")

VCPU_HOUR_USD = 0.052
MEMORY_GB_HOUR_USD = 0.0057


def get_boto3_session() -> boto3.session.Session:
    if AWS_PROFILE:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return boto3.Session(region_name=AWS_REGION)


def get_emr_serverless_client() -> Any:
    return get_boto3_session().client("emr-serverless")


def create_serverless_application(
    name: str,
    emr_version: str = "emr-6.15.0",
    pre_init_capacity: dict | None = None,
) -> str:
    """
    Create EMR Serverless application with Spark type. Return application_id.
    pre_init_capacity example: {"workerCount": 2, "workerConfiguration": {"cpu": "4vCPU", "memory": "16GB"}}
    If pre_init_capacity is None, no pre-initialized workers (cold start ~30s).
    Print ⚠️  COST WARNING if pre_init_capacity is set (workers charge when idle).
    """
    client = get_emr_serverless_client()
    application_name = f"{name}-{uuid4().hex[:8]}"

    request: dict[str, Any] = {
        "name": application_name,
        "releaseLabel": emr_version,
        "type": "SPARK",
        "tags": {
            "Project": "studybook",
            "Tutorial": "06_aws_emr",
            "ManagedBy": "03_emr_serverless.py",
        },
    }

    if pre_init_capacity:
        request["initialCapacity"] = {
            "Driver": pre_init_capacity,
            "Executor": pre_init_capacity,
        }

    response = client.create_application(**request)
    application_id = response["applicationId"]

    print(f"Created EMR Serverless application: {application_id}")

    if pre_init_capacity:
        print("⚠️  COST WARNING: EMR Serverless pre-initialized workers are configured and may accrue idle charges.")

    return application_id


def start_serverless_application(application_id: str) -> None:
    """
    Call start_application() and poll until state == STARTED.
    Poll every 10 seconds, timeout 300 seconds.
    """
    client = get_emr_serverless_client()

    try:
        client.start_application(applicationId=application_id)
    except ClientError as exc:
        message = exc.response.get("Error", {}).get("Message", "")
        if "already started" not in message.lower():
            raise

    start = time.time()
    timeout = 300

    while time.time() - start < timeout:
        response = client.get_application(applicationId=application_id)
        state = response["application"]["state"]
        print(f"Application {application_id}: {state}")

        if state == "STARTED":
            return

        if state in {"STOPPED", "TERMINATED"}:
            raise RuntimeError(f"Application reached unexpected state: {state}")

        time.sleep(10)

    raise TimeoutError(f"Application {application_id} did not START within {timeout} seconds.")


def submit_serverless_job(
    application_id: str,
    role_arn: str,
    script_s3: str,
    args: list[str],
    spark_conf: dict[str, str] | None = None,
    job_name: str = "emr-serverless-job",
) -> str:
    """
    Submit a job run. Return job_run_id.
    spark_conf keys become --conf entries in sparkSubmitParameters.
    Print: Submitted job {job_name} → {job_run_id}
    """
    client = get_emr_serverless_client()

    spark_parameters: list[str] = []
    if spark_conf:
        for key, value in spark_conf.items():
            spark_parameters.extend(["--conf", f"{key}={value}"])

    response = client.start_job_run(
        applicationId=application_id,
        executionRoleArn=role_arn,
        name=f"{job_name}-{uuid4().hex[:8]}",
        jobDriver={
            "sparkSubmit": {
                "entryPoint": script_s3,
                "entryPointArguments": args,
                "sparkSubmitParameters": " ".join(spark_parameters),
            }
        },
        configurationOverrides={
            "monitoringConfiguration": {
                "s3MonitoringConfiguration": {
                    "logUri": f"s3://{EMR_S3_BUCKET}/emr-serverless-logs/"
                    if EMR_S3_BUCKET
                    else "s3://example-bucket/emr-serverless-logs/"
                }
            }
        },
        tags={
            "Project": "studybook",
            "Tutorial": "06_aws_emr",
        },
    )

    job_run_id = response["jobRunId"]
    print(f"Submitted job {job_name} → {job_run_id}")
    return job_run_id


def wait_for_job(
    application_id: str,
    job_run_id: str,
    timeout: int = 600,
) -> dict:
    """
    Poll get_job_run() every 15 seconds.
    Print progress: Job {job_run_id}: PENDING → RUNNING → SUCCESS/FAILED
    Return final job_run dict.
    Raise RuntimeError on FAILED with error message from response.
    """
    client = get_emr_serverless_client()
    start = time.time()
    last_state = ""

    print(f"Job {job_run_id}: ", end="", flush=True)

    while time.time() - start < timeout:
        response = client.get_job_run(applicationId=application_id, jobRunId=job_run_id)
        job_run = response["jobRun"]
        state = job_run["state"]

        if state != last_state:
            print(f"{state} → ", end="", flush=True)
            last_state = state

        if state in {"SUCCESS", "FAILED", "CANCELLING", "CANCELLED"}:
            print()
            if state != "SUCCESS":
                message = job_run.get("stateDetails", "No failure details provided.")
                raise RuntimeError(f"Job {job_run_id} failed with state {state}: {message}")
            return job_run

        time.sleep(15)

    print()
    raise TimeoutError(f"Job {job_run_id} did not finish within {timeout} seconds.")


def get_job_details(application_id: str, job_run_id: str) -> dict:
    """
    Return dict with:
      {
        "job_run_id": str,
        "state": str,
        "duration_seconds": float,
        "total_vcpu_hours": float,
        "total_memory_gb_hours": float,
        "estimated_cost_usd": float,
        "cost_breakdown": str,
      }
    """
    client = get_emr_serverless_client()
    response = client.get_job_run(applicationId=application_id, jobRunId=job_run_id)
    job_run = response["jobRun"]

    created_at = job_run.get("createdAt")
    ended_at = job_run.get("endedAt") or datetime.now(timezone.utc)

    duration_seconds = 0.0
    if created_at:
        duration_seconds = max((ended_at - created_at).total_seconds(), 0.0)

    usage = job_run.get("totalResourceUtilization", {})

    total_vcpu_hours = float(
        usage.get("vCPUHour")
        or usage.get("vCPUHours")
        or usage.get("totalVCPUHour")
        or 0.0
    )
    total_memory_gb_hours = float(
        usage.get("memoryGBHour")
        or usage.get("memoryGBHours")
        or usage.get("totalMemoryGBHour")
        or 0.0
    )

    estimated_cost = (total_vcpu_hours * VCPU_HOUR_USD) + (total_memory_gb_hours * MEMORY_GB_HOUR_USD)

    return {
        "job_run_id": job_run_id,
        "state": job_run.get("state", "UNKNOWN"),
        "duration_seconds": round(duration_seconds, 2),
        "total_vcpu_hours": round(total_vcpu_hours, 4),
        "total_memory_gb_hours": round(total_memory_gb_hours, 4),
        "estimated_cost_usd": round(estimated_cost, 4),
        "cost_breakdown": (
            f"vCPU ${total_vcpu_hours * VCPU_HOUR_USD:.4f} + "
            f"memory ${total_memory_gb_hours * MEMORY_GB_HOUR_USD:.4f}"
        ),
    }


def stop_and_delete_application(application_id: str) -> None:
    """
    Stop application (wait for STOPPED state), then delete it.
    Catch ResourceNotFoundException silently.
    Print ✅ Cleanup complete. No ongoing charges.
    """
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
                print(f"Stopping application {application_id}: {state}")

                if state == "STOPPED":
                    break

                time.sleep(10)

        client.delete_application(applicationId=application_id)
        print("✅ Cleanup complete. No ongoing charges.")

    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in {"ResourceNotFoundException", "ValidationException"}:
            print("✅ Cleanup complete. No ongoing charges.")
            return
        raise


def print_comparison_table() -> None:
    rows = [
        ("Setup time", "~30 seconds", "5-10 minutes"),
        ("Min cost", "Per second", "Per hour"),
        ("Management", "Zero", "Full control"),
        ("Max scale", "Automatic", "Manual"),
        ("Best for", "Batch jobs", "Long-running"),
    ]

    print("\nEMR Serverless vs EMR Cluster")
    print("=" * 72)
    print(f"{'Dimension':18} | {'EMR Serverless':20} | {'EMR Cluster':20}")
    print("-" * 72)

    for dimension, serverless, cluster in rows:
        print(f"{dimension:18} | {serverless:20} | {cluster:20}")


def print_simulated_job_details() -> None:
    vcpu_hours = 1.25
    memory_gb_hours = 9.5
    estimated = (vcpu_hours * VCPU_HOUR_USD) + (memory_gb_hours * MEMORY_GB_HOUR_USD)

    details = {
        "job_run_id": "simulated-job-run",
        "state": "SUCCESS",
        "duration_seconds": 185.0,
        "total_vcpu_hours": round(vcpu_hours, 4),
        "total_memory_gb_hours": round(memory_gb_hours, 4),
        "estimated_cost_usd": round(estimated, 4),
        "cost_breakdown": f"vCPU ${vcpu_hours * VCPU_HOUR_USD:.4f} + memory ${memory_gb_hours * MEMORY_GB_HOUR_USD:.4f}",
    }

    print("\nSimulated EMR Serverless Job Details")
    print("=" * 72)
    for key, value in details.items():
        print(f"{key:24}: {value}")


def main() -> None:
    application_id: str | None = None

    print("AWS EMR Serverless")
    print("=" * 72)
    print_comparison_table()

    try:
        if EMR_SERVERLESS_ROLE_ARN and EMR_S3_BUCKET:
            application_id = create_serverless_application(
                name="studybook-emr-serverless",
                emr_version="emr-6.15.0",
                pre_init_capacity=None,
            )
            start_serverless_application(application_id)

            print(
                "\nLive application is ready. Submit a real script with "
                "submit_serverless_job(application_id, role_arn, script_s3, args)."
            )
            print("No job was submitted by default because this file has no input dataset dependency.")
        else:
            print(
                "\nSet EMR_SERVERLESS_ROLE_ARN and EMR_S3_BUCKET to run live demo.\n"
                "Using simulated output so you can learn the lifecycle without creating AWS resources."
            )
            print_simulated_job_details()
    finally:
        if application_id:
            stop_and_delete_application(application_id)


if __name__ == "__main__":
    main()