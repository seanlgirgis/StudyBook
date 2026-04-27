# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : 05_monitoring_and_bootstrap.py
# Covers  : EMR monitoring, bootstrap actions, and debugging failed Spark steps
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket
# Run     : python 05_monitoring_and_bootstrap.py
# ============================================================

from __future__ import annotations

import gzip
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError


# Environment variables used by this file:
# - AWS_REGION: AWS region where EMR and CloudWatch run.
# - AWS_PROFILE: Optional named AWS CLI profile for local development.
# - EMR_S3_BUCKET: Bucket that stores EMR logs and bootstrap scripts.
# - EMR_SUBNET_ID: Required by tutorial standard; not directly used here.
# - EMR_CLUSTER_ID: Optional cluster ID for live metric/log demos.
# - EMR_STEP_ID: Optional failed step ID for live log lookup.
# - SNS_TOPIC_ARN: Optional SNS topic ARN for CloudWatch alarm notifications.
#
# Cost note:
# This file does not create EMR clusters. CloudWatch alarms can create small
# monitoring charges if you call setup_cloudwatch_alarms() in a live account.

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_PROFILE = os.environ.get("AWS_PROFILE")
EMR_S3_BUCKET = os.environ.get("EMR_S3_BUCKET")
EMR_SUBNET_ID = os.environ.get("EMR_SUBNET_ID")
EMR_CLUSTER_ID = os.environ.get("EMR_CLUSTER_ID")
EMR_STEP_ID = os.environ.get("EMR_STEP_ID")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")


BOOTSTRAP_SCRIPT = """#!/usr/bin/env bash
set -euo pipefail

echo "Starting EMR bootstrap package installation"

if [ "$#" -eq 0 ]; then
  echo "No packages provided. Nothing to install."
  exit 0
fi

python3 -m pip install --upgrade pip

for package in "$@"; do
  echo "Installing ${package}"
  python3 -m pip install "${package}"
done

echo "Bootstrap package installation complete"
"""


def get_boto3_session() -> boto3.session.Session:
    if AWS_PROFILE:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return boto3.Session(region_name=AWS_REGION)


def get_cloudwatch_client() -> Any:
    return get_boto3_session().client("cloudwatch")


def get_s3_client() -> Any:
    return get_boto3_session().client("s3")


def create_bootstrap_action(
    name: str,
    script_s3_path: str,
    args: list[str] | None = None,
) -> dict:
    """
    Return bootstrap action dict ready for BootstrapActions parameter in create_cluster.
    Example name: "Install Python packages"
    Example script: s3://bucket/scripts/bootstrap.sh
    Example args: ["pandas==2.0.0", "pyarrow==13.0.0"]
    Also generate the shell script content as a string constant BOOTSTRAP_SCRIPT that
    pip-installs the packages from args.
    """
    return {
        "Name": name,
        "ScriptBootstrapAction": {
            "Path": script_s3_path,
            "Args": args or [],
        },
    }


def get_cluster_metrics(
    cluster_id: str,
    minutes: int = 60,
) -> dict:
    """
    Pull CloudWatch metrics for the cluster (namespace: AWS/ElasticMapReduce):
      - YARNMemoryAvailablePercentage (avg)
      - ContainerPendingRatio (max)
      - HDFSUtilization (max)
      - CoreNodesRunning (max)
    Return dict: {metric_name: {"avg": float, "max": float, "min": float}}
    Use period=300 (5-min granularity).
    """
    cloudwatch = get_cloudwatch_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)

    metric_names = [
        "YARNMemoryAvailablePercentage",
        "ContainerPendingRatio",
        "HDFSUtilization",
        "CoreNodesRunning",
    ]

    results: dict[str, dict[str, float]] = {}

    for metric_name in metric_names:
        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/ElasticMapReduce",
            MetricName=metric_name,
            Dimensions=[{"Name": "JobFlowId", "Value": cluster_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average", "Maximum", "Minimum"],
        )

        datapoints = response.get("Datapoints", [])

        if not datapoints:
            results[metric_name] = {"avg": 0.0, "max": 0.0, "min": 0.0}
            continue

        averages = [float(point.get("Average", 0.0)) for point in datapoints]
        maximums = [float(point.get("Maximum", 0.0)) for point in datapoints]
        minimums = [float(point.get("Minimum", 0.0)) for point in datapoints]

        results[metric_name] = {
            "avg": round(sum(averages) / len(averages), 4),
            "max": round(max(maximums), 4),
            "min": round(min(minimums), 4),
        }

    return results


def read_s3_text_or_missing(bucket: str, key: str) -> str:
    s3 = get_s3_client()

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read()

        if key.endswith(".gz"):
            return gzip.decompress(body).decode("utf-8", errors="replace")

        return body.decode("utf-8", errors="replace")
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in {"NoSuchKey", "404", "NoSuchBucket"}:
            return "Not available yet"
        raise


def find_failed_step_logs(
    cluster_id: str,
    step_id: str,
    log_bucket: str,
) -> dict:
    """
    Construct expected S3 paths for step logs:
      stderr: s3://{log_bucket}/emr-logs/{cluster_id}/steps/{step_id}/stderr.gz
      stdout: s3://{log_bucket}/emr-logs/{cluster_id}/steps/{step_id}/stdout.gz
      controller: s3://{log_bucket}/emr-logs/{cluster_id}/steps/{step_id}/controller.gz
    Attempt to download and decompress each.
    Return: {"stderr": str, "stdout": str, "controller": str}
    If a file doesn't exist: set value to "Not available yet"
    """
    base_key = f"emr-logs/{cluster_id}/steps/{step_id}"

    keys = {
        "stderr": f"{base_key}/stderr.gz",
        "stdout": f"{base_key}/stdout.gz",
        "controller": f"{base_key}/controller.gz",
    }

    return {
        name: read_s3_text_or_missing(log_bucket, key)
        for name, key in keys.items()
    }


def parse_spark_log_for_errors(log_content: str) -> list[dict]:
    """
    Scan log_content for known error patterns. Return list of findings:
      [
        {"type": "OOM", "line": 142, "message": "java.lang.OutOfMemoryError: GC overhead limit exceeded", "suggestion": "Increase executor memory with --conf spark.executor.memory=8g"},
        {"type": "SHUFFLE", "line": 891, "message": "org.apache.spark.shuffle.FetchFailedException", "suggestion": "Increase spark.reducer.maxReqsInFlight and spark.shuffle.io.retryWait"},
        {"type": "PARTITION", "line": 203, "message": "Job aborted due to stage failure: Total size of serialized results...", "suggestion": "Reduce spark.driver.maxResultSize or increase partition count"},
      ]
    Patterns to detect (use re.search):
      - "OutOfMemoryError" → type OOM
      - "FetchFailedException" → type SHUFFLE
      - "Total size of serialized results" → type PARTITION
      - "FileNotFoundException" → type FILE_NOT_FOUND
      - "AccessDeniedException" → type PERMISSIONS
    """
    patterns = [
        (
            "OOM",
            r"OutOfMemoryError",
            "Increase executor memory with --conf spark.executor.memory=8g and reduce shuffle pressure.",
        ),
        (
            "SHUFFLE",
            r"FetchFailedException",
            "Increase shuffle retry settings and check executor loss, Spot interruption, or network instability.",
        ),
        (
            "PARTITION",
            r"Total size of serialized results",
            "Avoid collecting large results to the driver; increase partition count or write results to S3.",
        ),
        (
            "FILE_NOT_FOUND",
            r"FileNotFoundException",
            "Validate the S3 input path, partition discovery, and upstream data availability.",
        ),
        (
            "PERMISSIONS",
            r"AccessDeniedException",
            "Check the EMR EC2 instance profile or EMR Serverless job role S3 permissions.",
        ),
    ]

    findings: list[dict] = []

    for line_number, line in enumerate(log_content.splitlines(), start=1):
        for finding_type, pattern, suggestion in patterns:
            if re.search(pattern, line):
                findings.append(
                    {
                        "type": finding_type,
                        "line": line_number,
                        "message": line.strip(),
                        "suggestion": suggestion,
                    }
                )

    return findings


def setup_cloudwatch_alarms(
    cluster_id: str,
    sns_topic_arn: str,
) -> list[str]:
    """
    Create two CloudWatch alarms. Return list of alarm names created.
    Alarm 1: YARNMemoryAvailablePercentage < 10% for 10 minutes → notify SNS
      AlarmName: f"emr-{cluster_id}-low-memory"
    Alarm 2: ContainerPendingRatio > 0.75 for 5 minutes → notify SNS
      AlarmName: f"emr-{cluster_id}-high-pending"
    """
    cloudwatch = get_cloudwatch_client()

    alarms = [
        {
            "AlarmName": f"emr-{cluster_id}-low-memory",
            "AlarmDescription": "EMR cluster has very low available YARN memory.",
            "MetricName": "YARNMemoryAvailablePercentage",
            "Threshold": 10.0,
            "ComparisonOperator": "LessThanThreshold",
            "EvaluationPeriods": 2,
            "Period": 300,
            "Statistic": "Average",
            "Unit": "Percent",
        },
        {
            "AlarmName": f"emr-{cluster_id}-high-pending",
            "AlarmDescription": "EMR cluster has high pending container pressure.",
            "MetricName": "ContainerPendingRatio",
            "Threshold": 0.75,
            "ComparisonOperator": "GreaterThanThreshold",
            "EvaluationPeriods": 1,
            "Period": 300,
            "Statistic": "Maximum",
            "Unit": "None",
        },
    ]

    created: list[str] = []

    for alarm in alarms:
        cloudwatch.put_metric_alarm(
            AlarmName=alarm["AlarmName"],
            AlarmDescription=alarm["AlarmDescription"],
            ActionsEnabled=True,
            AlarmActions=[sns_topic_arn],
            MetricName=alarm["MetricName"],
            Namespace="AWS/ElasticMapReduce",
            Statistic=alarm["Statistic"],
            Dimensions=[{"Name": "JobFlowId", "Value": cluster_id}],
            Period=alarm["Period"],
            EvaluationPeriods=alarm["EvaluationPeriods"],
            Threshold=alarm["Threshold"],
            ComparisonOperator=alarm["ComparisonOperator"],
            Unit=alarm["Unit"],
            TreatMissingData="notBreaching",
        )
        created.append(alarm["AlarmName"])

    print("⚠️  COST WARNING: CloudWatch alarms are now configured and may accrue monitoring charges.")
    return created


def print_bootstrap_demo() -> None:
    print("\nBootstrap Script Content")
    print("=" * 72)
    print(BOOTSTRAP_SCRIPT)

    action = create_bootstrap_action(
        name="Install Python packages",
        script_s3_path="s3://example-bucket/scripts/bootstrap.sh",
        args=["pandas==2.0.0", "pyarrow==13.0.0"],
    )

    print("\nBootstrap Action Dict")
    print("=" * 72)
    print(action)


def print_findings_table(findings: list[dict]) -> None:
    print("\nParsed Spark Log Findings")
    print("=" * 120)

    if not findings:
        print("No known Spark failure patterns detected.")
        return

    print(f"{'Type':14} | {'Line':5} | {'Message':45} | Suggestion")
    print("-" * 120)

    for finding in findings:
        message = finding["message"]
        if len(message) > 45:
            message = f"{message[:42]}..."
        print(
            f"{finding['type']:14} | "
            f"{finding['line']:<5} | "
            f"{message:45} | "
            f"{finding['suggestion']}"
        )


def print_debugging_checklist() -> None:
    checklist = [
        "OOM errors: increase executor memory, reduce skew, and avoid wide collect() calls.",
        "Shuffle failures: check executor loss, Spot interruptions, retry settings, and partition sizing.",
        "File not found: verify S3 paths, partition dates, and upstream job completion.",
        "Access denied: validate IAM role permissions for input, output, logs, and KMS keys.",
        "Pending containers: inspect YARNMemoryAvailablePercentage and scale core/task capacity.",
        "Slow jobs: inspect shuffle size, data skew, small files, and Spark UI stage timelines.",
    ]

    print("\nEMR Debugging Checklist")
    print("=" * 72)
    for index, item in enumerate(checklist, start=1):
        print(f"{index}. {item}")


def main() -> None:
    print("AWS EMR Monitoring and Bootstrap")
    print("=" * 72)

    print_bootstrap_demo()

    sample_log = """
25/04/27 10:00:01 INFO SparkContext: Running Spark version 3.5.0
25/04/27 10:00:05 INFO DAGScheduler: Got job 0 with 200 output partitions
25/04/27 10:01:12 ERROR Executor: java.lang.OutOfMemoryError: GC overhead limit exceeded
25/04/27 10:01:13 INFO TaskSetManager: Lost task 14.0 in stage 3.0
25/04/27 10:02:42 ERROR TaskSetManager: org.apache.spark.shuffle.FetchFailedException: Failed to connect
25/04/27 10:03:00 INFO SparkContext: Invoking stop() from shutdown hook
"""

    findings = parse_spark_log_for_errors(sample_log)
    print_findings_table(findings)

    if AWS_REGION and EMR_CLUSTER_ID:
        print("\nCluster Metrics")
        print("=" * 72)
        metrics = get_cluster_metrics(EMR_CLUSTER_ID)
        for metric_name, stats in metrics.items():
            print(f"{metric_name:36}: avg={stats['avg']} max={stats['max']} min={stats['min']}")
    else:
        print("\nSet AWS_REGION and EMR_CLUSTER_ID to pull live CloudWatch metrics.")

    if EMR_CLUSTER_ID and EMR_STEP_ID and EMR_S3_BUCKET:
        logs = find_failed_step_logs(EMR_CLUSTER_ID, EMR_STEP_ID, EMR_S3_BUCKET)
        print("\nFailed Step Log Availability")
        print("=" * 72)
        for name, content in logs.items():
            print(f"{name:12}: {content[:500]}")
    else:
        print("Set EMR_CLUSTER_ID, EMR_STEP_ID, and EMR_S3_BUCKET to inspect failed step logs.")

    if EMR_CLUSTER_ID and SNS_TOPIC_ARN:
        alarm_names = setup_cloudwatch_alarms(EMR_CLUSTER_ID, SNS_TOPIC_ARN)
        print("\nCreated CloudWatch Alarms")
        print("=" * 72)
        for alarm_name in alarm_names:
            print(alarm_name)
    else:
        print("Set EMR_CLUSTER_ID and SNS_TOPIC_ARN to create CloudWatch alarms.")

    print_debugging_checklist()


if __name__ == "__main__":
    main()