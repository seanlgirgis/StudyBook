# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : 01_emr_cluster_basics.py
# Covers  : Create, inspect, right-size, and terminate EMR clusters
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket
# Run     : python 01_emr_cluster_basics.py
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
# - AWS_REGION: AWS region where EMR runs, for example us-east-1.
# - AWS_PROFILE: Optional named AWS CLI profile for local development.
# - EMR_S3_BUCKET: S3 bucket for EMR logs.
# - EMR_SUBNET_ID: VPC subnet where EMR cluster instances launch.
# - EMR_EC2_KEY_PAIR: Optional EC2 key pair for SSH access.
#
# Cost note:
# EMR clusters create EC2 instances. Even short demos can cost money if
# clusters are left running. This tutorial uses TERMINATE_AT_TASK_COMPLETION
# and a finally cleanup path to reduce runaway spend risk.

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_PROFILE = os.environ.get("AWS_PROFILE")
EMR_S3_BUCKET = os.environ.get("EMR_S3_BUCKET")
EMR_SUBNET_ID = os.environ.get("EMR_SUBNET_ID")
EMR_EC2_KEY_PAIR = os.environ.get("EMR_EC2_KEY_PAIR")


def get_boto3_session() -> boto3.session.Session:
    if AWS_PROFILE:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return boto3.Session(region_name=AWS_REGION)


def get_emr_client() -> Any:
    return get_boto3_session().client("emr")


def create_emr_cluster(
    name: str,
    instance_type: str,
    core_count: int,
    emr_version: str,
    s3_bucket: str,
    subnet_id: str,
    ec2_key_pair: str | None = None,
) -> str:
    """
    Create an EMR cluster and return the cluster_id.
    - Uses TERMINATE_AT_TASK_COMPLETION to avoid dangling clusters.
    - Log URI: s3://{s3_bucket}/emr-logs/
    - One master node (ON_DEMAND) + core_count core nodes (SPOT preferred).
    - Print ⚠️  COST WARNING immediately after create_cluster call.
    - Returns cluster_id string.
    """
    emr = get_emr_client()
    cluster_name = f"{name}-{uuid4().hex[:8]}"

    ec2_attributes: dict[str, Any] = {"SubnetId": subnet_id}
    if ec2_key_pair:
        ec2_attributes["KeyName"] = ec2_key_pair

    response = emr.run_job_flow(
        Name=cluster_name,
        ReleaseLabel=emr_version,
        LogUri=f"s3://{s3_bucket}/emr-logs/",
        Applications=[
            {"Name": "Spark"},
            {"Name": "Hadoop"},
        ],
        Instances={
            "Ec2SubnetId": subnet_id,
            "Ec2KeyName": ec2_key_pair if ec2_key_pair else "",
            "KeepJobFlowAliveWhenNoSteps": False,
            "TerminationProtected": False,
            "InstanceGroups": [
                {
                    "Name": "Master node",
                    "Market": "ON_DEMAND",
                    "InstanceRole": "MASTER",
                    "InstanceType": instance_type,
                    "InstanceCount": 1,
                },
                {
                    "Name": "Core nodes",
                    "Market": "SPOT",
                    "InstanceRole": "CORE",
                    "InstanceType": instance_type,
                    "InstanceCount": core_count,
                },
            ],
        },
        JobFlowRole="EMR_EC2_DefaultRole",
        ServiceRole="EMR_DefaultRole",
        VisibleToAllUsers=True,
        ScaleDownBehavior="TERMINATE_AT_TASK_COMPLETION",
        AutoTerminationPolicy={"IdleTimeout": 3600},
        Tags=[
            {"Key": "Project", "Value": "studybook"},
            {"Key": "Tutorial", "Value": "06_aws_emr"},
            {"Key": "ManagedBy", "Value": "01_emr_cluster_basics.py"},
        ],
    )

    cluster_id = response["JobFlowId"]
    print(f"Created EMR cluster: {cluster_id}")
    print("⚠️  COST WARNING: EMR cluster EC2 instances are now running and accruing charges.")
    return cluster_id


def wait_for_cluster(
    cluster_id: str,
    target_state: str = "WAITING",
    timeout: int = 600,
) -> dict:
    """
    Poll describe_cluster every 15 seconds until state == target_state or TERMINATED/FAILED.
    Raise TimeoutError if not reached within timeout seconds.
    Return final describe_cluster response.
    """
    emr = get_emr_client()
    start = time.time()
    terminal_states = {"TERMINATED", "TERMINATED_WITH_ERRORS"}

    while time.time() - start < timeout:
        response = emr.describe_cluster(ClusterId=cluster_id)
        cluster = response["Cluster"]
        state = cluster["Status"]["State"]

        print(f"Cluster {cluster_id}: {state}")

        if state == target_state:
            return response

        if state in terminal_states:
            reason = cluster["Status"].get("StateChangeReason", {})
            raise RuntimeError(f"Cluster reached terminal state {state}: {reason}")

        time.sleep(15)

    raise TimeoutError(f"Cluster {cluster_id} did not reach {target_state} within {timeout} seconds.")


def describe_cluster(cluster_id: str) -> None:
    """
    Print formatted cluster summary:
    - Cluster ID, Name, State, StateChangeReason
    - Master/Core/Task node counts and instance types
    - Creation time and elapsed time
    """
    emr = get_emr_client()
    response = emr.describe_cluster(ClusterId=cluster_id)
    cluster = response["Cluster"]

    instance_groups = emr.list_instance_groups(ClusterId=cluster_id).get("InstanceGroups", [])

    created_at = cluster["Status"]["Timeline"].get("CreationDateTime")
    elapsed = None
    if created_at:
        elapsed = datetime.now(timezone.utc) - created_at.astimezone(timezone.utc)

    print("\nEMR Cluster Summary")
    print("=" * 72)
    print(f"Cluster ID          : {cluster.get('Id')}")
    print(f"Name                : {cluster.get('Name')}")
    print(f"State               : {cluster.get('Status', {}).get('State')}")
    print(f"State reason        : {cluster.get('Status', {}).get('StateChangeReason', {})}")
    print(f"Created at          : {created_at}")
    print(f"Elapsed             : {elapsed}")

    print("\nInstance Groups")
    print("-" * 72)
    for group in instance_groups:
        print(
            f"{group.get('InstanceGroupType'):6} | "
            f"{group.get('InstanceType'):12} | "
            f"requested={group.get('RequestedInstanceCount')} | "
            f"running={group.get('RunningInstanceCount')} | "
            f"market={group.get('Market')}"
        )


def list_steps(cluster_id: str) -> list[dict]:
    """
    Return list of step dicts from list_steps() API.
    Print each step: Id, Name, Status.State, CreationDateTime.
    """
    emr = get_emr_client()
    response = emr.list_steps(ClusterId=cluster_id)
    steps = response.get("Steps", [])

    print("\nEMR Steps")
    print("=" * 72)
    if not steps:
        print("No steps found.")
        return steps

    for step in steps:
        timeline = step.get("Status", {}).get("Timeline", {})
        print(
            f"{step.get('Id')} | "
            f"{step.get('Name')} | "
            f"{step.get('Status', {}).get('State')} | "
            f"{timeline.get('CreationDateTime')}"
        )

    return steps


def terminate_cluster(cluster_id: str) -> None:
    """
    Terminate the cluster. Catch AlreadyTerminated errors silently.
    Print ✅ Cleanup complete. No ongoing charges. after confirmed.
    """
    emr = get_emr_client()

    try:
        emr.terminate_job_flows(JobFlowIds=[cluster_id])
        print(f"Termination requested for cluster: {cluster_id}")
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        message = exc.response.get("Error", {}).get("Message", "")
        if "InvalidRequestException" in code or "already terminated" in message.lower():
            print("✅ Cleanup complete. No ongoing charges.")
            return
        raise

    while True:
        try:
            response = emr.describe_cluster(ClusterId=cluster_id)
            state = response["Cluster"]["Status"]["State"]
            print(f"Cleanup check: cluster {cluster_id} is {state}")
            if state in {"TERMINATED", "TERMINATED_WITH_ERRORS"}:
                print("✅ Cleanup complete. No ongoing charges.")
                return
            time.sleep(15)
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code in {"InvalidRequestException", "ResourceNotFoundException"}:
                print("✅ Cleanup complete. No ongoing charges.")
                return
            raise


def recommend_instance_type(
    data_size_gb: float,
    compute_vs_memory: str = "balanced",
) -> dict:
    """
    Return a recommendation dict:
      {
        "master": "m5.xlarge",
        "core": "r5.2xlarge",
        "task": "r5.4xlarge",  # spot
        "core_count": 4,
        "rationale": "Memory-heavy workload (>500GB) needs r5 family...",
        "estimated_cost_per_hour": 1.23,
      }
    Decision table:
      - <50GB  → m5.xlarge master, m5.xlarge core x2
      - 50-500GB → m5.2xlarge master, m5.4xlarge core x4
      - >500GB, balanced → r5.4xlarge master, r5.4xlarge core x6
      - >500GB, compute → c5.4xlarge master, c5.9xlarge core x6
      - >500GB, memory → r5.8xlarge master, r5.8xlarge core x8
    """
    prices = {
        "m5.xlarge": 0.192,
        "m5.2xlarge": 0.384,
        "m5.4xlarge": 0.768,
        "r5.4xlarge": 1.008,
        "r5.8xlarge": 2.016,
        "c5.4xlarge": 0.680,
        "c5.9xlarge": 1.530,
    }

    workload = compute_vs_memory.lower().strip()

    if data_size_gb < 50:
        master = "m5.xlarge"
        core = "m5.xlarge"
        task = "m5.xlarge"
        core_count = 2
        rationale = "Small batch workloads fit general-purpose m5 nodes without paying for oversized memory."
    elif data_size_gb <= 500:
        master = "m5.2xlarge"
        core = "m5.4xlarge"
        task = "m5.4xlarge"
        core_count = 4
        rationale = "Medium workloads benefit from larger m5 cores while staying cost-efficient."
    elif workload == "compute":
        master = "c5.4xlarge"
        core = "c5.9xlarge"
        task = "c5.9xlarge"
        core_count = 6
        rationale = "Large compute-heavy workloads favor c5 instances for CPU-dense Spark stages."
    elif workload == "memory":
        master = "r5.8xlarge"
        core = "r5.8xlarge"
        task = "r5.8xlarge"
        core_count = 8
        rationale = "Memory-heavy workloads above 500GB need r5 capacity to reduce shuffle and cache pressure."
    else:
        master = "r5.4xlarge"
        core = "r5.4xlarge"
        task = "r5.4xlarge"
        core_count = 6
        rationale = "Large balanced workloads usually need extra memory headroom for shuffle-heavy Spark jobs."

    estimated_cost = prices[master] + (prices[core] * core_count)

    return {
        "master": master,
        "core": core,
        "task": task,
        "core_count": core_count,
        "rationale": rationale,
        "estimated_cost_per_hour": round(estimated_cost, 3),
    }


def print_recommendations_table(recommendations: list[tuple[str, dict]]) -> None:
    print("\nEMR Instance Recommendations")
    print("=" * 120)
    print(
        f"{'Scenario':24} | {'Master':12} | {'Core':12} | "
        f"{'Task/Spot':12} | {'Cores':5} | {'$/hr':8} | Rationale"
    )
    print("-" * 120)

    for scenario, rec in recommendations:
        print(
            f"{scenario:24} | "
            f"{rec['master']:12} | "
            f"{rec['core']:12} | "
            f"{rec['task']:12} | "
            f"{rec['core_count']:<5} | "
            f"${rec['estimated_cost_per_hour']:<7} | "
            f"{rec['rationale']}"
        )


def main() -> None:
    cluster_id: str | None = None

    print("AWS EMR Cluster Basics")
    print("=" * 72)

    print(
        """
Cluster creation pattern explained:

- Master node coordinates the cluster.
- Core nodes store HDFS data and run Spark executors.
- Task nodes run compute only and are often good Spot candidates.
- Logs go to S3 so failures can be inspected after the cluster terminates.
- Auto-termination and try/finally cleanup reduce runaway cost risk.
"""
    )

    recommendations = [
        ("Small batch: 30GB", recommend_instance_type(30)),
        ("Medium compute: 300GB", recommend_instance_type(300, "compute")),
        ("Large memory: 1000GB", recommend_instance_type(1000, "memory")),
    ]
    print_recommendations_table(recommendations)

    try:
        if EMR_S3_BUCKET and EMR_SUBNET_ID:
            cluster_id = create_emr_cluster(
                name="studybook-emr-basics",
                instance_type="m5.xlarge",
                core_count=2,
                emr_version="emr-6.15.0",
                s3_bucket=EMR_S3_BUCKET,
                subnet_id=EMR_SUBNET_ID,
                ec2_key_pair=EMR_EC2_KEY_PAIR,
            )
            wait_for_cluster(cluster_id, "WAITING")
            describe_cluster(cluster_id)
            list_steps(cluster_id)
        else:
            print("\nSet EMR_S3_BUCKET and EMR_SUBNET_ID to run live demo")
    finally:
        if cluster_id:
            terminate_cluster(cluster_id)


if __name__ == "__main__":
    main()