# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : 03_alarms_and_composite_alarms.py
# Covers  : Metric alarms, anomaly detection alarm pattern, and composite alarms
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python 03_alarms_and_composite_alarms.py
# ============================================================

from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
CW_NAMESPACE = os.getenv("CW_NAMESPACE", "StudyBook/Pipeline")
CW_LOG_GROUP_NAME = os.getenv("CW_LOG_GROUP_NAME", "/studybook/pipeline")
CW_ALARM_SNS_ARN = os.getenv("CW_ALARM_SNS_ARN")


def get_cw_client() -> Any:
    """
    Create a CloudWatch boto3 client.

    WHY:
        A single client factory keeps region/profile selection consistent across
        local demos, CI runs, and real AWS study accounts.

    Args:
        None.

    Returns:
        Any: boto3 CloudWatch client.

    Raises:
        botocore.exceptions.BotoCoreError: If boto3 cannot create a session/client.
    """
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("cloudwatch")


def _dimension_list(dimensions: dict[str, str]) -> list[dict[str, str]]:
    """
    Convert a dimension dictionary into CloudWatch's list format.

    WHY:
        CloudWatch uses dimensions as part of the metric identity. Keeping this
        conversion centralized prevents subtle mismatches between metric emission
        and alarm definitions.

    Args:
        dimensions (dict[str, str]): Dimension name/value pairs.

    Returns:
        list[dict[str, str]]: CloudWatch-formatted dimensions.

    Raises:
        None.
    """
    return [{"Name": key, "Value": value} for key, value in dimensions.items()]


def emit_synthetic_metrics(namespace: str, dimensions: dict[str, str]) -> None:
    """
    Emit synthetic metric data so alarms have signals to evaluate.

    WHY:
        Alarms do not become meaningful until CloudWatch receives datapoints for
        the exact namespace, metric name, and dimensions used by the alarm.

    Args:
        namespace (str): CloudWatch namespace.
        dimensions (dict[str, str]): Dimensions shared by demo metrics.

    Returns:
        None.

    Raises:
        ClientError: If PutMetricData fails.
    """
    client = get_cw_client()
    now = datetime.now(timezone.utc)

    metric_data: list[dict[str, Any]] = []

    for minutes_ago in [10, 5, 0]:
        timestamp = now - timedelta(minutes=minutes_ago)

        metric_data.extend(
            [
                {
                    "MetricName": "records_processed",
                    "Value": 450.0 if minutes_ago in {5, 0} else 950.0,
                    "Unit": "Count",
                    "Dimensions": _dimension_list(dimensions),
                    "Timestamp": timestamp,
                    "StorageResolution": 60,
                },
                {
                    "MetricName": "error_count",
                    "Value": 1.0 if minutes_ago == 0 else 0.0,
                    "Unit": "Count",
                    "Dimensions": _dimension_list(dimensions),
                    "Timestamp": timestamp,
                    "StorageResolution": 60,
                },
                {
                    "MetricName": "duration_ms",
                    "Value": 42000.0 if minutes_ago in {5, 0} else 12000.0,
                    "Unit": "Milliseconds",
                    "Dimensions": _dimension_list(dimensions),
                    "Timestamp": timestamp,
                    "StorageResolution": 60,
                },
            ]
        )

    for index in range(0, len(metric_data), 20):
        try:
            client.put_metric_data(
                Namespace=namespace,
                MetricData=metric_data[index : index + 20],
            )
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            print(f"PutMetricData failed: {code}")
            raise

    print("Synthetic alarm metrics emitted.")


def create_metric_alarm(
    name: str,
    namespace: str,
    metric: str,
    dimensions: dict[str, str],
    threshold: float,
    comparison: str,
    evaluation_periods: int,
    period_s: int,
    statistic: str,
    sns_arn: str | None = None,
) -> str:
    """
    Create a CloudWatch metric alarm.

    WHY:
        Metric alarms are the basic alerting primitive for pipelines. They turn
        raw operational measurements into explicit OK/ALARM/INSUFFICIENT_DATA
        states that humans and automation can respond to.

    Args:
        name (str): Alarm name.
        namespace (str): CloudWatch metric namespace.
        metric (str): Metric name.
        dimensions (dict[str, str]): Dimensions identifying the metric stream.
        threshold (float): Alarm threshold.
        comparison (str): Comparison operator, such as GreaterThanThreshold.
        evaluation_periods (int): Number of periods that must breach.
        period_s (int): Evaluation period in seconds.
        statistic (str): Statistic such as Average, Sum, or p90.
        sns_arn (str | None): Optional SNS topic ARN for notifications.

    Returns:
        str: Alarm ARN.

    Raises:
        ClientError: If PutMetricAlarm or DescribeAlarms fails.
    """
    client = get_cw_client()

    alarm_actions = [sns_arn] if sns_arn else []

    request: dict[str, Any] = {
        "AlarmName": name,
        "AlarmDescription": (
            f"StudyBook alarm for {metric}. "
            "Created by 03_alarms_and_composite_alarms.py"
        ),
        "ActionsEnabled": bool(alarm_actions),
        "AlarmActions": alarm_actions,
        "OKActions": alarm_actions,
        "InsufficientDataActions": [],
        "MetricName": metric,
        "Namespace": namespace,
        "Dimensions": _dimension_list(dimensions),
        "Period": period_s,
        "EvaluationPeriods": evaluation_periods,
        "DatapointsToAlarm": evaluation_periods,
        "Threshold": threshold,
        "ComparisonOperator": comparison,
        "TreatMissingData": "notBreaching",
    }

    if statistic.startswith("p"):
        request["ExtendedStatistic"] = statistic
    else:
        request["Statistic"] = statistic

    try:
        client.put_metric_alarm(**request)
        print(f"Created metric alarm: {name}")
        print("⚠️  COST WARNING: CloudWatch Alarms cost about $0.10/alarm/month.")

        response = client.describe_alarms(AlarmNames=[name])
        alarms = response.get("MetricAlarms", [])
        return alarms[0]["AlarmArn"] if alarms else name
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"Create metric alarm failed for {name}: {code}")
        raise


def create_anomaly_detection_alarm(
    name: str,
    metric_name: str,
    namespace: str,
    dimensions: dict[str, str],
    band_width: float = 2.0,
) -> str:
    """
    Create an anomaly detection alarm for a metric.

    WHY:
        Static thresholds are weak for pipelines with weekly or hourly patterns.
        Anomaly detection learns a baseline and alarms when values leave the
        expected band, which is better for variable-but-seasonal workloads.

    Args:
        name (str): Alarm name.
        metric_name (str): Metric name to monitor.
        namespace (str): CloudWatch namespace.
        dimensions (dict[str, str]): Metric dimensions.
        band_width (float): Width of anomaly detection band.

    Returns:
        str: Alarm ARN.

    Raises:
        ClientError: If anomaly detector or alarm creation fails.
    """
    client = get_cw_client()

    try:
        client.put_anomaly_detector(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=_dimension_list(dimensions),
            Stat="Average",
        )

        metric_id = "m1"
        expression_id = "ad1"

        client.put_metric_alarm(
            AlarmName=name,
            AlarmDescription=(
                "StudyBook anomaly detection alarm. "
                "Uses ANOMALY_DETECTION_BAND to adapt to normal patterns."
            ),
            ActionsEnabled=False,
            EvaluationPeriods=2,
            DatapointsToAlarm=2,
            ThresholdMetricId=expression_id,
            ComparisonOperator="GreaterThanUpperThreshold",
            TreatMissingData="notBreaching",
            Metrics=[
                {
                    "Id": metric_id,
                    "MetricStat": {
                        "Metric": {
                            "Namespace": namespace,
                            "MetricName": metric_name,
                            "Dimensions": _dimension_list(dimensions),
                        },
                        "Period": 300,
                        "Stat": "Average",
                    },
                    "ReturnData": True,
                },
                {
                    "Id": expression_id,
                    "Expression": f"ANOMALY_DETECTION_BAND({metric_id}, {band_width})",
                    "Label": f"{metric_name} expected band",
                    "ReturnData": True,
                },
            ],
        )

        print(f"Created anomaly detection alarm: {name}")
        print("⚠️  COST WARNING: CloudWatch Alarms cost about $0.10/alarm/month.")

        response = client.describe_alarms(AlarmNames=[name])
        alarms = response.get("MetricAlarms", [])
        return alarms[0]["AlarmArn"] if alarms else name
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"Create anomaly detection alarm failed for {name}: {code}")
        raise


def create_composite_alarm(
    name: str,
    alarm_rule: str,
    sns_arn: str | None = None,
) -> str:
    """
    Create a CloudWatch composite alarm.

    WHY:
        Composite alarms reduce alert noise. Instead of paging on every weak
        signal, teams can alert only when related alarms combine into a stronger
        failure condition.

    Args:
        name (str): Composite alarm name.
        alarm_rule (str): Rule like ALARM("a") OR ALARM("b").
        sns_arn (str | None): Optional SNS topic ARN for notifications.

    Returns:
        str: Composite alarm ARN.

    Raises:
        ClientError: If PutCompositeAlarm or DescribeAlarms fails.
    """
    client = get_cw_client()
    actions = [sns_arn] if sns_arn else []

    try:
        client.put_composite_alarm(
            AlarmName=name,
            AlarmDescription=(
                "StudyBook composite alarm. "
                "Combines lower-level pipeline health signals."
            ),
            ActionsEnabled=bool(actions),
            AlarmActions=actions,
            OKActions=actions,
            InsufficientDataActions=[],
            AlarmRule=alarm_rule,
        )

        print(f"Created composite alarm: {name}")
        print("⚠️  COST WARNING: CloudWatch Alarms cost about $0.10/alarm/month.")

        response = client.describe_alarms(AlarmNames=[name])
        alarms = response.get("CompositeAlarms", [])
        return alarms[0]["AlarmArn"] if alarms else name
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"Create composite alarm failed for {name}: {code}")
        raise


def get_alarm_state(alarm_name: str) -> dict[str, Any]:
    """
    Return current state information for one alarm.

    WHY:
        Alarm state is what operators care about during triage: OK, ALARM, or
        INSUFFICIENT_DATA. Scripts should expose that directly.

    Args:
        alarm_name (str): CloudWatch alarm name.

    Returns:
        dict[str, Any]: StateValue, StateReason, and StateUpdatedTimestamp.

    Raises:
        ClientError: If DescribeAlarms fails.
        ValueError: If the alarm is not found.
    """
    client = get_cw_client()

    try:
        response = client.describe_alarms(AlarmNames=[alarm_name])
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"DescribeAlarms failed for {alarm_name}: {code}")
        raise

    all_alarms = response.get("MetricAlarms", []) + response.get("CompositeAlarms", [])
    if not all_alarms:
        raise ValueError(f"Alarm not found: {alarm_name}")

    alarm = all_alarms[0]
    return {
        "StateValue": alarm.get("StateValue"),
        "StateReason": alarm.get("StateReason"),
        "StateUpdatedTimestamp": alarm.get("StateUpdatedTimestamp"),
    }


def get_alarm_history(alarm_name: str, days: int = 7) -> list[dict[str, Any]]:
    """
    Return alarm history entries for the last N days.

    WHY:
        Alarm history explains what changed and when. During incident review,
        this is the audit trail connecting metrics to alerts.

    Args:
        alarm_name (str): Alarm name.
        days (int): Number of days of history to retrieve.

    Returns:
        list[dict[str, Any]]: Alarm history items.

    Raises:
        ClientError: If DescribeAlarmHistory fails.
    """
    client = get_cw_client()
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)

    paginator = client.get_paginator("describe_alarm_history")
    history: list[dict[str, Any]] = []

    try:
        for page in paginator.paginate(
            AlarmName=alarm_name,
            StartDate=start,
            EndDate=end,
        ):
            history.extend(page.get("AlarmHistoryItems", []))
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"DescribeAlarmHistory failed for {alarm_name}: {code}")
        raise

    return history


def list_alarms_in_state(state: str = "ALARM") -> list[str]:
    """
    List alarms currently in a specific state.

    WHY:
        During incidents, teams often start with "what is currently alarming?"
        This helper gives that operational entry point directly.

    Args:
        state (str): Alarm state filter: OK, ALARM, or INSUFFICIENT_DATA.

    Returns:
        list[str]: Alarm names in the requested state.

    Raises:
        ClientError: If DescribeAlarms fails.
    """
    client = get_cw_client()
    paginator = client.get_paginator("describe_alarms")
    names: list[str] = []

    try:
        for page in paginator.paginate(StateValue=state):
            for alarm in page.get("MetricAlarms", []):
                names.append(alarm["AlarmName"])
            for alarm in page.get("CompositeAlarms", []):
                names.append(alarm["AlarmName"])
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"DescribeAlarms by state failed: {code}")
        raise

    return names


def delete_alarm(name: str) -> None:
    """
    Delete one CloudWatch alarm idempotently.

    WHY:
        Alarms are billable resources. Deleting them in tutorial cleanup prevents
        accidental monthly charges.

    Args:
        name (str): Alarm name.

    Returns:
        None.

    Raises:
        ClientError: If DeleteAlarms fails unexpectedly.
    """
    delete_alarms([name])


def delete_alarms(names: list[str]) -> None:
    """
    Delete CloudWatch alarms safely.

    WHY:
        Composite alarms depend on metric alarms. AWS will reject deleting a metric
        alarm while a composite alarm still references it, so composite alarms must
        be deleted first.

    Args:
        names (list[str]): Alarm names to delete.

    Returns:
        None.

    Raises:
        ClientError: If DeleteAlarms fails unexpectedly.
    """
    if not names:
        return

    client = get_cw_client()

    composite_names = [name for name in names if "unhealthy" in name or "composite" in name]
    metric_names = [name for name in names if name not in composite_names]

    ordered_batches = [composite_names, metric_names]

    for batch in ordered_batches:
        if not batch:
            continue

        try:
            client.delete_alarms(AlarmNames=batch)
            for name in batch:
                print(f"Deleted alarm if present: {name}")

            # Small pause lets CloudWatch detach composite dependencies.
            time.sleep(3)

        except ClientError as exc:
            code = exc.response["Error"]["Code"]

            if code in {"ResourceNotFoundException", "ResourceNotFound"}:
                continue

            print(f"DeleteAlarms failed: {code}")
            raise

def cleanup(alarm_names: list[str]) -> None:
    """
    Clean up alarms created by this demo.

    WHY:
        CloudWatch alarms are billable every month. Demo scripts must clean them
        even when earlier steps fail.

    Args:
        alarm_names (list[str]): Alarm names to delete.

    Returns:
        None.

    Raises:
        None.
    """
    try:
        delete_alarms(alarm_names)
    finally:
        print("✅  Cleanup complete. No ongoing charges.")


def print_alarm_states(alarm_names: list[str]) -> None:
    """
    Print current alarm states.

    WHY:
        Alarm state can lag metric emission. Printing states teaches the real AWS
        behavior: OK/ALARM/INSUFFICIENT_DATA may take evaluation time to settle.

    Args:
        alarm_names (list[str]): Alarm names to inspect.

    Returns:
        None.

    Raises:
        None.
    """
    print("\nAlarm states")
    print("-" * 80)

    for name in alarm_names:
        try:
            state = get_alarm_state(name)
            reason = str(state.get("StateReason", ""))[:90]
            print(f"{name:<28} {state.get('StateValue'):<20} {reason}")
        except (ClientError, ValueError) as exc:
            print(f"{name:<28} Unable to read state: {exc}")


def main() -> None:
    """
    Run the CloudWatch alarm demo.

    WHY:
        This file demonstrates threshold alarms and composite alarms: the common
        alerting model used to monitor data pipeline health.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS API calls fail unexpectedly.
    """
    dimensions = {
        "PipelineName": "studybook-demo",
        "Environment": "dev",
    }

    alarm_names = [
        "cw-records-low",
        "cw-error-spike",
        "cw-latency-high",
        "cw-pipeline-unhealthy",
    ]

    try:
        emit_synthetic_metrics(CW_NAMESPACE, dimensions)

        create_metric_alarm(
            name="cw-records-low",
            namespace=CW_NAMESPACE,
            metric="records_processed",
            dimensions=dimensions,
            threshold=500,
            comparison="LessThanThreshold",
            evaluation_periods=2,
            period_s=300,
            statistic="Average",
            sns_arn=CW_ALARM_SNS_ARN,
        )

        create_metric_alarm(
            name="cw-error-spike",
            namespace=CW_NAMESPACE,
            metric="error_count",
            dimensions=dimensions,
            threshold=0,
            comparison="GreaterThanThreshold",
            evaluation_periods=1,
            period_s=300,
            statistic="Sum",
            sns_arn=CW_ALARM_SNS_ARN,
        )

        create_metric_alarm(
            name="cw-latency-high",
            namespace=CW_NAMESPACE,
            metric="duration_ms",
            dimensions=dimensions,
            threshold=30000,
            comparison="GreaterThanThreshold",
            evaluation_periods=2,
            period_s=300,
            statistic="p90",
            sns_arn=CW_ALARM_SNS_ARN,
        )

        create_composite_alarm(
            name="cw-pipeline-unhealthy",
            alarm_rule='ALARM("cw-error-spike") OR ALARM("cw-latency-high")',
            sns_arn=CW_ALARM_SNS_ARN,
        )

        print("\nWaiting briefly for alarm states to initialize...")
        time.sleep(10)

        print_alarm_states(alarm_names)

        alarming = list_alarms_in_state("ALARM")
        print("\nCurrent alarms in ALARM state:")
        for alarm in alarming:
            print(f"- {alarm}")

    finally:
        cleanup(alarm_names)


if __name__ == "__main__":
    main()