# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : 01_custom_metrics.py
# Covers  : Emit, batch, query, list, and cost custom CloudWatch metrics
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python 01_custom_metrics.py
# ============================================================

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
CW_NAMESPACE = os.getenv("CW_NAMESPACE", "StudyBook/Pipeline")


def get_cw_client() -> Any:
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("cloudwatch")


def put_metric_batch(namespace: str, metrics: list[dict[str, Any]]) -> None:
    if len(metrics) > 20:
        raise ValueError("Max 20 metrics per call")

    client = get_cw_client()
    client.put_metric_data(Namespace=namespace, MetricData=metrics)


def put_statistic_set(
    namespace: str,
    metric_name: str,
    dimensions: dict[str, str],
    sample_count: int,
    sum: float,
    min_val: float,
    max_val: float,
) -> None:
    client = get_cw_client()

    client.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                "MetricName": metric_name,
                "Dimensions": [
                    {"Name": k, "Value": v} for k, v in dimensions.items()
                ],
                "StatisticValues": {
                    "SampleCount": sample_count,
                    "Sum": sum,
                    "Minimum": min_val,
                    "Maximum": max_val,
                },
                "Unit": "Count",
                "Timestamp": datetime.now(timezone.utc),
            }
        ],
    )


def get_metric_statistics(
    namespace: str,
    metric_name: str,
    dimensions: dict[str, str],
    start: datetime,
    end: datetime,
    period_s: int,
    stat: str,
) -> list[dict[str, Any]]:
    client = get_cw_client()

    # FIX: build request dynamically (no empty lists allowed)
    request: dict[str, Any] = {
        "Namespace": namespace,
        "MetricName": metric_name,
        "Dimensions": [
            {"Name": k, "Value": v} for k, v in dimensions.items()
        ],
        "StartTime": start,
        "EndTime": end,
        "Period": period_s,
    }

    if stat.startswith("p"):
        request["ExtendedStatistics"] = [stat]
    else:
        request["Statistics"] = [stat]

    try:
        response = client.get_metric_statistics(**request)
    except ClientError as exc:
        print(exc.response["Error"]["Code"])
        raise

    rows = []
    for p in sorted(response.get("Datapoints", []), key=lambda x: x["Timestamp"]):
        val = p.get(stat)

        if val is None and stat.startswith("p"):
            val = p.get("ExtendedStatistics", {}).get(stat)

        rows.append(
            {
                "Timestamp": p["Timestamp"],
                "value": val,
                "Unit": p.get("Unit", ""),
            }
        )

    return rows


def list_metrics_in_namespace(namespace: str) -> list[dict[str, Any]]:
    client = get_cw_client()
    paginator = client.get_paginator("list_metrics")

    out = []
    for page in paginator.paginate(Namespace=namespace):
        for m in page.get("Metrics", []):
            out.append(
                {
                    "MetricName": m["MetricName"],
                    "Dimensions": m["Dimensions"],
                }
            )
    return out


def calculate_metric_cost(metric_count: int) -> dict[str, Any]:
    free = 10
    billable = max(0, metric_count - free)

    return {
        "free_tier": free,
        "billable": billable,
        "monthly_usd": billable * 0.30,
    }


def cleanup() -> None:
    print("No persistent resources.")
    print("✅ Cleanup complete. No ongoing charges.")


def main() -> None:
    dims = {"PipelineName": "studybook-demo"}

    try:
        now = datetime.now(timezone.utc)

        print("Emitting metrics...")
        print("⚠️ COST WARNING: custom metrics bill after 10")

        buffer: list[dict[str, Any]] = []

        for i in range(50):
            ts = now - timedelta(minutes=120 - i * 2)

            buffer.append(
                {
                    "MetricName": "records_processed",
                    "Value": float(800 + (i * 17) % 400),
                    "Unit": "Count",
                    "Dimensions": [{"Name": k, "Value": v} for k, v in dims.items()],
                    "Timestamp": ts,
                }
            )

            if len(buffer) == 20:
                put_metric_batch(CW_NAMESPACE, buffer)
                buffer = []

        if buffer:
            put_metric_batch(CW_NAMESPACE, buffer)

        print("Sending StatisticSet...")
        put_statistic_set(
            CW_NAMESPACE,
            "records_processed_batch",
            dims,
            1000,
            1000,
            1,
            1,
        )

        rows = get_metric_statistics(
            CW_NAMESPACE,
            "records_processed",
            dims,
            now - timedelta(hours=3),
            now + timedelta(minutes=5),
            3600,
            "Average",
        )

        print("\nResults:")
        for r in rows:
            print(r)

        print("\nMetrics list:")
        for m in list_metrics_in_namespace(CW_NAMESPACE):
            print(m["MetricName"])

        print("\nCost:")
        print(calculate_metric_cost(10))
        print(calculate_metric_cost(50))

    finally:
        cleanup()


if __name__ == "__main__":
    main()