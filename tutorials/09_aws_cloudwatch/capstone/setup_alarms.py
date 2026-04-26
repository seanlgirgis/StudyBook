# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : capstone/setup_alarms.py
# Covers  : Create capstone CloudWatch metric alarms and composite alarm
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python capstone/setup_alarms.py
# ============================================================

from __future__ import annotations

import os
import time
from typing import Any

import boto3
from botocore.exceptions import ClientError


NAMESPACE = os.getenv("CW_NAMESPACE", "StudyBook/CapstoneP")
LOG_GROUP = os.getenv("CW_LOG_GROUP_NAME", "/studybook/capstone/pipeline")
PIPELINE_NAME = "iot-ingest-hourly"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
CW_ALARM_SNS_ARN = os.getenv("CW_ALARM_SNS_ARN")


def get_cw_client() -> Any:
    """
    Create a CloudWatch client.

    WHY:
        Alarm setup should use the same profile and region as metric emission.
        Centralizing the client prevents silent cross-region mistakes.

    Args:
        None.

    Returns:
        Any: boto3 CloudWatch client.

    Raises:
        botocore.exceptions.BotoCoreError: If boto3 cannot create the client.
    """
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("cloudwatch")


def create_alarm(
    name: str,
    metric: str,
    threshold: float,
    comparison: str,
    eval_periods: int,
    period_s: int,
    statistic: str,
    treat_missing: str = "notBreaching",
) -> str:
    """
    Create one CloudWatch metric alarm for the capstone pipeline.

    WHY:
        Each alarm maps one operational symptom to a clear health signal:
        low output, errors, high duration, or high lag.

    Args:
        name (str): Alarm name.
        metric (str): Metric name in the capstone namespace.
        threshold (float): Numeric threshold.
        comparison (str): CloudWatch comparison operator.
        eval_periods (int): Evaluation periods required.
        period_s (int): Evaluation period in seconds.
        statistic (str): Statistic such as Average, Sum, or p90.
        treat_missing (str): Missing data behavior.

    Returns:
        str: Alarm name.

    Raises:
        ClientError: If PutMetricAlarm fails.
    """
    client = get_cw_client()
    actions = [CW_ALARM_SNS_ARN] if CW_ALARM_SNS_ARN else []

    request: dict[str, Any] = {
        "AlarmName": name,
        "AlarmDescription": f"Capstone alarm for {PIPELINE_NAME}: {metric}",
        "ActionsEnabled": bool(actions),
        "AlarmActions": actions,
        "OKActions": actions,
        "InsufficientDataActions": [],
        "Namespace": NAMESPACE,
        "MetricName": metric,
        "Dimensions": [{"Name": "PipelineName", "Value": PIPELINE_NAME}],
        "Threshold": threshold,
        "ComparisonOperator": comparison,
        "EvaluationPeriods": eval_periods,
        "DatapointsToAlarm": eval_periods,
        "Period": period_s,
        "TreatMissingData": treat_missing,
    }

    if statistic.startswith("p"):
        request["ExtendedStatistic"] = statistic
    else:
        request["Statistic"] = statistic

    try:
        client.put_metric_alarm(**request)
        print(f"Created alarm: {name}")
        print("⚠️  COST WARNING: CloudWatch Alarms cost about $0.10/month per alarm.")
        return name
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"Create alarm failed for {name}: {code}")
        raise


def create_composite_alarm(name: str, alarm_rule: str) -> str:
    """
    Create one CloudWatch composite alarm.

    WHY:
        Composite alarms reduce alert noise by combining multiple symptoms into
        one operator-facing health signal.

    Args:
        name (str): Composite alarm name.
        alarm_rule (str): Rule such as ALARM("a") OR ALARM("b").

    Returns:
        str: Composite alarm name.

    Raises:
        ClientError: If PutCompositeAlarm fails.
    """
    client = get_cw_client()
    actions = [CW_ALARM_SNS_ARN] if CW_ALARM_SNS_ARN else []

    try:
        client.put_composite_alarm(
            AlarmName=name,
            AlarmDescription=f"Composite health alarm for {PIPELINE_NAME}",
            AlarmRule=alarm_rule,
            ActionsEnabled=bool(actions),
            AlarmActions=actions,
            OKActions=actions,
            InsufficientDataActions=[],
        )
        print(f"Created composite alarm: {name}")
        print("⚠️  COST WARNING: CloudWatch Alarms cost about $0.10/month per alarm.")
        return name
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"Create composite alarm failed for {name}: {code}")
        raise


def create_all_alarms() -> list[str]:
    """
    Create all capstone alarms.

    WHY:
        A healthy pipeline needs coverage across volume, errors, duration, and lag.
        This set mirrors how real teams monitor hourly batch/stream hybrids.

    Args:
        None.

    Returns:
        list[str]: Created alarm names.

    Raises:
        ClientError: If alarm creation fails.
    """
    alarm_names: list[str] = []

    alarm_names.append(
        create_alarm(
            name="capstone-records-low",
            metric="records_out",
            threshold=7000,
            comparison="LessThanThreshold",
            eval_periods=2,
            period_s=300,
            statistic="Average",
        )
    )

    alarm_names.append(
        create_alarm(
            name="capstone-errors",
            metric="error_count",
            threshold=1,
            comparison="GreaterThanOrEqualToThreshold",
            eval_periods=1,
            period_s=300,
            statistic="Sum",
        )
    )

    alarm_names.append(
        create_alarm(
            name="capstone-duration-high",
            metric="duration_ms",
            threshold=30000,
            comparison="GreaterThanThreshold",
            eval_periods=2,
            period_s=300,
            statistic="p90",
        )
    )

    alarm_names.append(
        create_alarm(
            name="capstone-lag-high",
            metric="lag_seconds",
            threshold=300,
            comparison="GreaterThanThreshold",
            eval_periods=1,
            period_s=300,
            statistic="Maximum",
        )
    )

    alarm_names.append(
        create_composite_alarm(
            name="capstone-unhealthy",
            alarm_rule='ALARM("capstone-errors") OR ALARM("capstone-lag-high")',
        )
    )

    return alarm_names


def print_alarm_states(alarm_names: list[str]) -> None:
    """
    Print current state for each alarm.

    WHY:
        Newly created alarms often show INSUFFICIENT_DATA until evaluation catches
        up. Printing states teaches that delay explicitly.

    Args:
        alarm_names (list[str]): Alarm names to inspect.

    Returns:
        None.

    Raises:
        None.
    """
    client = get_cw_client()

    print("\nAlarm states")
    print("-" * 100)

    for name in alarm_names:
        try:
            response = client.describe_alarms(AlarmNames=[name])
            alarms = response.get("MetricAlarms", []) + response.get("CompositeAlarms", [])

            if not alarms:
                print(f"{name:<28} NOT_FOUND")
                continue

            alarm = alarms[0]
            state = alarm.get("StateValue", "UNKNOWN")
            reason = str(alarm.get("StateReason", ""))[:80]
            print(f"{name:<28} {state:<20} {reason}")

        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            print(f"{name:<28} READ_FAILED: {code}")


def delete_all_alarms(alarm_names: list[str]) -> None:
    """
    Delete all capstone alarms safely.

    WHY:
        Composite alarms reference metric alarms. AWS rejects deleting referenced
        metric alarms first, so the composite alarm must be deleted before metrics.

    Args:
        alarm_names (list[str]): Alarm names to delete.

    Returns:
        None.

    Raises:
        ClientError: If deletion fails unexpectedly.
    """
    client = get_cw_client()

    composite = [name for name in alarm_names if name == "capstone-unhealthy"]
    metric = [name for name in alarm_names if name not in composite]

    for batch in [composite, metric]:
        if not batch:
            continue

        try:
            client.delete_alarms(AlarmNames=batch)
            for name in batch:
                print(f"Deleted alarm if present: {name}")
            time.sleep(2)
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            if code in {"ResourceNotFoundException", "ResourceNotFound"}:
                continue
            print(f"Delete alarms failed: {code}")
            raise


def main() -> None:
    """
    Create capstone alarms and leave them for dashboard/orchestration.

    WHY:
        Unlike setup demos, capstone alarms intentionally remain after this script
        so capstone.py and cleanup.py can use them.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS API calls fail unexpectedly.
    """
    alarm_names = create_all_alarms()

    time.sleep(3)
    print_alarm_states(alarm_names)

    print("\n5 alarms created. Check AWS Console > CloudWatch > Alarms.")
    print("Run capstone/cleanup.py to remove all resources.")


if __name__ == "__main__":
    main()