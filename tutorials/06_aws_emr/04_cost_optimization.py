# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : 04_cost_optimization.py
# Covers  : Spot instances, autoscaling, rightsizing, and EMR cost comparison
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket
# Run     : python 04_cost_optimization.py
# ============================================================

from __future__ import annotations

import os
from typing import Any


# Environment variables used by this file:
# - AWS_REGION: AWS region used for cost assumptions, for example us-east-1.
# - AWS_PROFILE: Optional named AWS CLI profile for local development.
# - EMR_S3_BUCKET: Required by tutorial standard; not used by this offline cost calculator.
# - EMR_SUBNET_ID: Required by tutorial standard; not used by this offline cost calculator.
#
# Cost note:
# This file does not create AWS resources. It teaches cost tradeoffs offline.
# Prices are representative us-east-1 examples for learning, not live billing quotes.

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_PROFILE = os.environ.get("AWS_PROFILE")
EMR_S3_BUCKET = os.environ.get("EMR_S3_BUCKET")
EMR_SUBNET_ID = os.environ.get("EMR_SUBNET_ID")


ON_DEMAND_PRICES_USD = {
    "m5.xlarge": 0.192,
    "m5.2xlarge": 0.384,
    "m5.4xlarge": 0.768,
    "r5.2xlarge": 0.504,
    "r5.4xlarge": 1.008,
    "r5.8xlarge": 2.016,
    "c5.4xlarge": 0.680,
    "c5.9xlarge": 1.530,
}

VCPU_HOUR_USD = 0.052
MEMORY_GB_HOUR_USD = 0.0057


def get_spot_discount_pct(instance_type: str) -> float:
    if instance_type.startswith("r5."):
        return 70.0
    if instance_type.startswith("m5."):
        return 75.0
    if instance_type.startswith("c5."):
        return 60.0
    return 60.0


def calculate_cluster_cost(
    instance_type: str,
    core_count: int,
    hours: float,
    use_spot: bool = True,
) -> dict:
    """
    Return cost breakdown dict:
      {
        "instance_type": str,
        "core_count": int,
        "hours": float,
        "on_demand_price_per_hour": float,
        "spot_discount_pct": float,
        "spot_price_per_hour": float,
        "total_on_demand_usd": float,
        "total_spot_usd": float,
        "recommended_usd": float,
        "savings_vs_on_demand_usd": float,
      }
    Use these representative us-east-1 prices (hardcode):
      m5.xlarge: $0.192/hr, m5.2xlarge: $0.384/hr, m5.4xlarge: $0.768/hr,
      r5.2xlarge: $0.504/hr, r5.4xlarge: $1.008/hr, r5.8xlarge: $2.016/hr,
      c5.4xlarge: $0.680/hr, c5.9xlarge: $1.530/hr
    Spot discount: 70% for r5, 75% for m5, 60% for c5.
    Master node always ON_DEMAND. Core nodes use spot if use_spot=True.
    """
    if instance_type not in ON_DEMAND_PRICES_USD:
        known = ", ".join(sorted(ON_DEMAND_PRICES_USD))
        raise ValueError(f"Unknown instance_type {instance_type}. Known values: {known}")

    if core_count < 1:
        raise ValueError("core_count must be >= 1")

    if hours <= 0:
        raise ValueError("hours must be > 0")

    on_demand_price = ON_DEMAND_PRICES_USD[instance_type]
    spot_discount_pct = get_spot_discount_pct(instance_type)
    spot_price = on_demand_price * (1 - spot_discount_pct / 100)

    master_cost = on_demand_price * hours
    core_on_demand_cost = on_demand_price * core_count * hours
    core_spot_cost = spot_price * core_count * hours

    total_on_demand = master_cost + core_on_demand_cost
    total_spot = master_cost + core_spot_cost
    recommended = total_spot if use_spot else total_on_demand
    savings = total_on_demand - recommended

    return {
        "instance_type": instance_type,
        "core_count": core_count,
        "hours": hours,
        "on_demand_price_per_hour": round(on_demand_price, 4),
        "spot_discount_pct": spot_discount_pct,
        "spot_price_per_hour": round(spot_price, 4),
        "total_on_demand_usd": round(total_on_demand, 4),
        "total_spot_usd": round(total_spot, 4),
        "recommended_usd": round(recommended, 4),
        "savings_vs_on_demand_usd": round(savings, 4),
    }


def calculate_serverless_cost(
    vcpu_hours: float,
    memory_gb_hours: float,
) -> dict:
    """
    Return:
      {
        "vcpu_hours": float,
        "memory_gb_hours": float,
        "vcpu_cost_usd": float,
        "memory_cost_usd": float,
        "total_usd": float,
        "cost_per_hour_equivalent": float,
      }
    """
    if vcpu_hours < 0:
        raise ValueError("vcpu_hours must be >= 0")

    if memory_gb_hours < 0:
        raise ValueError("memory_gb_hours must be >= 0")

    vcpu_cost = vcpu_hours * VCPU_HOUR_USD
    memory_cost = memory_gb_hours * MEMORY_GB_HOUR_USD
    total = vcpu_cost + memory_cost

    active_hours = max(vcpu_hours / 4, 1.0)

    return {
        "vcpu_hours": round(vcpu_hours, 4),
        "memory_gb_hours": round(memory_gb_hours, 4),
        "vcpu_cost_usd": round(vcpu_cost, 4),
        "memory_cost_usd": round(memory_cost, 4),
        "total_usd": round(total, 4),
        "cost_per_hour_equivalent": round(total / active_hours, 4),
    }


def estimate_serverless_usage(job_hours: float, data_size_gb: float) -> tuple[float, float]:
    if data_size_gb <= 50:
        average_vcpu = 4
        average_memory_gb = 16
    elif data_size_gb <= 500:
        average_vcpu = 16
        average_memory_gb = 64
    else:
        average_vcpu = 64
        average_memory_gb = 256

    return average_vcpu * job_hours, average_memory_gb * job_hours


def compare_options(job_hours: float, data_size_gb: float) -> None:
    """
    Print a formatted cost comparison table for three job sizes.
    For each of: small (2 m5.xlarge cores), medium (4 m5.4xlarge cores), large (8 r5.4xlarge cores):
      - EMR Cluster (On-Demand)
      - EMR Cluster (Spot)
      - EMR Serverless (estimated vcpu/memory from data_size_gb)
    Show winner with ★ symbol.
    """
    profiles = [
        ("Small", "m5.xlarge", 2),
        ("Medium", "m5.4xlarge", 4),
        ("Large", "r5.4xlarge", 8),
    ]

    options: list[dict[str, Any]] = []

    for size_name, instance_type, core_count in profiles:
        on_demand = calculate_cluster_cost(instance_type, core_count, job_hours, use_spot=False)
        spot = calculate_cluster_cost(instance_type, core_count, job_hours, use_spot=True)

        options.append(
            {
                "profile": size_name,
                "option": "EMR Cluster On-Demand",
                "cost": on_demand["total_on_demand_usd"],
                "details": f"{core_count} cores + 1 master, {instance_type}",
            }
        )
        options.append(
            {
                "profile": size_name,
                "option": "EMR Cluster Spot",
                "cost": spot["total_spot_usd"],
                "details": f"{core_count} Spot cores + 1 On-Demand master, {instance_type}",
            }
        )

    vcpu_hours, memory_gb_hours = estimate_serverless_usage(job_hours, data_size_gb)
    serverless = calculate_serverless_cost(vcpu_hours, memory_gb_hours)
    options.append(
        {
            "profile": "Serverless",
            "option": "EMR Serverless",
            "cost": serverless["total_usd"],
            "details": f"{vcpu_hours:.1f} vCPU-hr, {memory_gb_hours:.1f} GB-hr",
        }
    )

    winner_cost = min(row["cost"] for row in options)

    print(f"\nCost Comparison: {job_hours} hours, {data_size_gb}GB")
    print("=" * 108)
    print(f"{'Winner':7} | {'Profile':10} | {'Option':22} | {'Cost USD':10} | Details")
    print("-" * 108)

    for row in options:
        winner = "★" if row["cost"] == winner_cost else ""
        print(
            f"{winner:7} | "
            f"{row['profile']:10} | "
            f"{row['option']:22} | "
            f"${row['cost']:<9.4f} | "
            f"{row['details']}"
        )


def build_instance_fleet_config(
    on_demand_capacity: int,
    spot_capacity: int,
    instance_types: list[str],
) -> dict:
    """
    Return boto3-ready InstanceFleets config dict.
    Each instance type weighted equally.
    SpotSpecification: AllocationStrategy = "CAPACITY_OPTIMIZED"
    OnDemandSpecification: AllocationStrategy = "LOWEST_PRICE"
    """
    if on_demand_capacity < 0:
        raise ValueError("on_demand_capacity must be >= 0")

    if spot_capacity < 0:
        raise ValueError("spot_capacity must be >= 0")

    if not instance_types:
        raise ValueError("instance_types must contain at least one instance type")

    return {
        "InstanceFleetType": "CORE",
        "Name": "Core fleet with On-Demand baseline and Spot scale-out",
        "TargetOnDemandCapacity": on_demand_capacity,
        "TargetSpotCapacity": spot_capacity,
        "InstanceTypeConfigs": [
            {
                "InstanceType": instance_type,
                "WeightedCapacity": 1,
                "BidPriceAsPercentageOfOnDemandPrice": 100.0,
            }
            for instance_type in instance_types
        ],
        "LaunchSpecifications": {
            "SpotSpecification": {
                "TimeoutDurationMinutes": 10,
                "TimeoutAction": "SWITCH_TO_ON_DEMAND",
                "AllocationStrategy": "CAPACITY_OPTIMIZED",
            },
            "OnDemandSpecification": {
                "AllocationStrategy": "LOWEST_PRICE",
            },
        },
    }


def build_autoscaling_policy(
    min_instances: int,
    max_instances: int,
    scale_out_metric: str = "YARNMemoryAvailablePercentage",
) -> dict:
    """
    Return boto3-ready AutoScalingPolicy dict with:
    - ScaleOut: when scale_out_metric < 15% for 5 minutes → add 2 instances
    - ScaleIn: when YARNMemoryAvailablePercentage > 75% for 5 minutes → remove 2 instances
    """
    if min_instances < 1:
        raise ValueError("min_instances must be >= 1")

    if max_instances < min_instances:
        raise ValueError("max_instances must be >= min_instances")

    return {
        "Constraints": {
            "MinCapacity": min_instances,
            "MaxCapacity": max_instances,
        },
        "Rules": [
            {
                "Name": "ScaleOutLowAvailableMemory",
                "Description": "Add capacity when YARN memory is constrained for five minutes.",
                "Action": {
                    "SimpleScalingPolicyConfiguration": {
                        "AdjustmentType": "CHANGE_IN_CAPACITY",
                        "ScalingAdjustment": 2,
                        "CoolDown": 300,
                    }
                },
                "Trigger": {
                    "CloudWatchAlarmDefinition": {
                        "ComparisonOperator": "LESS_THAN",
                        "EvaluationPeriods": 1,
                        "MetricName": scale_out_metric,
                        "Namespace": "AWS/ElasticMapReduce",
                        "Period": 300,
                        "Statistic": "AVERAGE",
                        "Threshold": 15.0,
                        "Unit": "PERCENT",
                    }
                },
            },
            {
                "Name": "ScaleInHighAvailableMemory",
                "Description": "Remove capacity when the cluster has sustained memory headroom.",
                "Action": {
                    "SimpleScalingPolicyConfiguration": {
                        "AdjustmentType": "CHANGE_IN_CAPACITY",
                        "ScalingAdjustment": -2,
                        "CoolDown": 300,
                    }
                },
                "Trigger": {
                    "CloudWatchAlarmDefinition": {
                        "ComparisonOperator": "GREATER_THAN",
                        "EvaluationPeriods": 1,
                        "MetricName": "YARNMemoryAvailablePercentage",
                        "Namespace": "AWS/ElasticMapReduce",
                        "Period": 300,
                        "Statistic": "AVERAGE",
                        "Threshold": 75.0,
                        "Unit": "PERCENT",
                    }
                },
            },
        ],
    }


def print_cost_optimization_tips() -> None:
    tips = [
        "Use EMR Serverless for irregular batch jobs so idle clusters do not sit online.",
        "Use Spot for core/task capacity, but keep a small On-Demand baseline for reliability.",
        "Right-size Spark executors before scaling hardware; bad partitioning wastes every node.",
        "Write logs to S3 and terminate clusters aggressively after steps finish.",
        "Use autoscaling for variable workloads, but set max capacity to prevent surprise spend.",
    ]

    print("\nCost Optimization Tips")
    print("=" * 72)
    for index, tip in enumerate(tips, start=1):
        print(f"{index}. {tip}")


def main() -> None:
    print("AWS EMR Cost Optimization")
    print("=" * 72)
    print("This script is offline-only. It creates no AWS resources and cannot accrue charges.")

    compare_options(2.0, 50)
    compare_options(8.0, 500)
    compare_options(24.0, 5000)

    print("\nInstance Fleet Config Example")
    print("=" * 72)
    fleet = build_instance_fleet_config(
        on_demand_capacity=2,
        spot_capacity=8,
        instance_types=["m5.4xlarge", "r5.4xlarge", "c5.4xlarge"],
    )
    print(fleet)

    print("\nAutoscaling Policy Example")
    print("=" * 72)
    policy = build_autoscaling_policy(min_instances=2, max_instances=12)
    print(policy)

    print_cost_optimization_tips()


if __name__ == "__main__":
    main()