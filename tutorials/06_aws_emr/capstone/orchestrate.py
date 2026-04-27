# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : capstone/orchestrate.py
# Covers  : Upload process_logs.py, run EMR Serverless job, monitor, estimate cost
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket | EMR role
# Run     : python capstone/orchestrate.py
# ============================================================

from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_PROFILE = os.environ.get("AWS_PROFILE")
EMR_S3_BUCKET = os.environ.get("EMR_S3_BUCKET")
EMR_SERVERLESS_ROLE_ARN = os.environ.get("EMR_SERVERLESS_ROLE_ARN")

EMR_VERSION = "emr-6.15.0"
APP_NAME = f"studybook-log-processor-{uuid4().hex[:8]}"

VCPU_HOUR_USD = 0.052
MEMORY_GB_HOUR_USD = 0.0057

_LAST_APPLICATION_ID: str | None = None


def get_boto3_session() -> boto3.session.Session:
    if AWS_PROFILE:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return boto3.Session(region_name=AWS_REGION)


def get_s3_client() -> Any:
    return get_boto3_session().client("s3")


def get_emr_serverless_client() -> Any:
    return get_boto3_session().client("emr-serverless")


def create_serverless_application(name: str, emr_version: str = EMR_VERSION) -> str:
    client = get_emr_serverless_client()
    response = client.create_application(
        name=name,
        releaseLabel=emr_version,
        type="SPARK",
        tags={
            "Project": "studybook",
            "Tutorial": "06_aws_emr",
            "ManagedBy": "capstone/orchestrate.py",
        },
    )
    return response["applicationId"]


def start_serverless_application(application_id: str) -> None:
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
) -> str:
    client = get_emr_serverless_client()
    response = client.start_job_run(
        applicationId=application_id,
        executionRoleArn=role_arn,
        name=f"process-weblogs-{uuid4().hex[:8]}",
        jobDriver={
            "sparkSubmit": {
                "entryPoint": script_s3,
                "entryPointArguments": args,
            }
        },
        configurationOverrides={
            "monitoringConfiguration": {
                "s3MonitoringConfiguration": {
                    "logUri": f"s3://{EMR_S3_BUCKET}/emr-serverless-logs/"
                }
            }
        },
        tags={
            "Project": "studybook",
            "Tutorial": "06_aws_emr",
        },
    )
    return response["jobRunId"]


def wait_for_job(application_id: str, job_run_id: str, timeout: int = 900) -> dict:
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
        "application_id": application_id,
        "job_run_id": job_run_id,
        "state": job_run.get("state", "UNKNOWN"),
        "duration_seconds": duration_seconds,
        "total_vcpu_hours": total_vcpu_hours,
        "total_memory_gb_hours": total_memory_gb_hours,
        "estimated_cost_usd": estimated_cost,
    }


def setup(bucket: str) -> tuple[str, str]:
    """
    Upload capstone/process_logs.py to s3://{bucket}/emr-scripts/process_logs.py.
    Return (script_s3_uri, input_s3_uri).
    """
    local_script = Path(__file__).resolve().parent / "process_logs.py"
    script_key = "emr-scripts/process_logs.py"

    print(f"Uploading script to s3://{bucket}/{script_key}")
    get_s3_client().upload_file(str(local_script), bucket, script_key)

    script_s3_uri = f"s3://{bucket}/{script_key}"
    input_s3_uri = f"s3://{bucket}/raw/weblogs/weblogs.csv"
    return script_s3_uri, input_s3_uri


def run_pipeline(
    role_arn: str,
    bucket: str,
) -> dict:
    """
    Full pipeline:
      1. create_serverless_application(APP_NAME, EMR_VERSION)
      2. start_serverless_application(application_id)
      3. setup(bucket) → script_uri, input_uri
      4. output_uri = f"s3://{bucket}/processed/weblogs/"
      5. submit_serverless_job(application_id, role_arn, script_uri, [input_uri, output_uri])
      6. wait_for_job(application_id, job_run_id, timeout=900)
      7. details = get_job_details(application_id, job_run_id)
      8. Print cost report
      9. Return details
    """
    global _LAST_APPLICATION_ID

    application_id = create_serverless_application(APP_NAME, EMR_VERSION)
    _LAST_APPLICATION_ID = application_id
    print(f"Created EMR Serverless application: {application_id}")

    start_serverless_application(application_id)
    print("⚠️  COST WARNING: EMR Serverless application is now running and may accrue charges.")

    script_uri, input_uri = setup(bucket)
    output_uri = f"s3://{bucket}/processed/weblogs/"

    job_run_id = submit_serverless_job(
        application_id=application_id,
        role_arn=role_arn,
        script_s3=script_uri,
        args=[input_uri, output_uri],
    )
    print(f"Submitted job run: {job_run_id}")

    wait_for_job(application_id, job_run_id, timeout=900)
    details = get_job_details(application_id, job_run_id)
    details["script_uri"] = script_uri
    details["input_uri"] = input_uri
    details["output_uri"] = output_uri

    print_cost_report(details)
    return details


def _cost_line(label: str, value: str) -> str:
    body = f"{label:<16}{value}"
    return f"║ {body:<36} ║"


def print_cost_report(details: dict) -> None:
    """
    Print formatted cost report:
      ╔══════════════════════════════════════╗
      ║     EMR Serverless Cost Report       ║
      ╠══════════════════════════════════════╣
      ║ Duration:        XX.X seconds        ║
      ║ vCPU-hours:      X.XXXX              ║
      ║ Memory GB-hours: XX.XXXX             ║
      ║ Total cost:      $X.XXXX             ║
      ╚══════════════════════════════════════╝
    """
    duration = float(details.get("duration_seconds", 0.0))
    vcpu_hours = float(details.get("total_vcpu_hours", 0.0))
    memory_hours = float(details.get("total_memory_gb_hours", 0.0))
    total_cost = float(details.get("estimated_cost_usd", 0.0))

    print("╔══════════════════════════════════════╗")
    print("║     EMR Serverless Cost Report       ║")
    print("╠══════════════════════════════════════╣")
    print(_cost_line("Duration:", f"{duration:.1f} seconds"))
    print(_cost_line("vCPU-hours:", f"{vcpu_hours:.4f}"))
    print(_cost_line("Memory GB-hours:", f"{memory_hours:.4f}"))
    print(_cost_line("Total cost:", f"${total_cost:.4f}"))
    print("╚══════════════════════════════════════╝")


def stop_and_delete_application(application_id: str) -> None:
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


def main() -> None:
    """
    Gate on EMR_SERVERLESS_ROLE_ARN and EMR_S3_BUCKET.
    If not set: print setup instructions and exit.
    Otherwise run run_pipeline() in try/finally, call stop_and_delete_application() in finally.
    """
    details: dict[str, Any] | None = None

    if not EMR_SERVERLESS_ROLE_ARN or not EMR_S3_BUCKET:
        print("Set required environment variables first:")
        print('  $env:EMR_SERVERLESS_ROLE_ARN="arn:aws:iam::<account-id>:role/<role-name>"')
        print('  $env:EMR_S3_BUCKET="your-existing-bucket"')
        print('  $env:AWS_REGION="us-east-1"')
        print('  $env:AWS_PROFILE="your-profile-name"')
        return

    try:
        details = run_pipeline(role_arn=EMR_SERVERLESS_ROLE_ARN, bucket=EMR_S3_BUCKET)
        print(f"Input URI  : {details['input_uri']}")
        print(f"Output URI : {details['output_uri']}")
        print(f"Job State  : {details['state']}")
    finally:
        application_id = (
            details.get("application_id")
            if details
            else _LAST_APPLICATION_ID
        )
        if application_id:
            stop_and_delete_application(application_id)


if __name__ == "__main__":
    main()
