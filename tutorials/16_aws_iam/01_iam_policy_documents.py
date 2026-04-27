"""
FILE: 01_iam_policy_documents.py
TOPIC: AWS IAM for Data Engineers
PURPOSE: Build and validate IAM policy documents as Python dictionaries.
COVERS: least privilege, IAM JSON, actions/resources/conditions
INTERVIEW FOCUS: Explain how IAM policy shape, scoped resources, and conditions reduce blast radius in data pipelines.
"""

from __future__ import annotations

import json
from typing import Any


POLICY_VERSION = "2012-10-17"


def build_s3_read_only_policy(bucket_name: str, prefix: str) -> dict:
    """
    Build a least-privilege S3 read-only IAM policy for a specific bucket prefix.

    This policy allows:
    - Listing only the requested prefix
    - Reading objects only under that prefix

    Args:
        bucket_name: S3 bucket name without s3://.
        prefix: Folder-style prefix, such as raw/events/.

    Returns:
        IAM policy document as a Python dictionary.
    """
    clean_prefix = prefix.strip("/")

    if not bucket_name.strip():
        raise ValueError("bucket_name must not be empty")

    if not clean_prefix:
        raise ValueError("prefix must not be empty")

    bucket_arn = f"arn:aws:s3:::{bucket_name}"
    object_arn = f"{bucket_arn}/{clean_prefix}/*"

    # INTERVIEW TIP:
    # For S3, ListBucket applies to the bucket ARN, while GetObject applies to
    # object ARNs. Mixing these up is a common interview and production mistake.
    policy = {
        "Version": POLICY_VERSION,
        "Statement": [
            {
                "Sid": "AllowListOnlySpecificPrefix",
                "Effect": "Allow",
                "Action": ["s3:ListBucket"],
                "Resource": bucket_arn,
                "Condition": {
                    "StringLike": {
                        "s3:prefix": [
                            clean_prefix,
                            f"{clean_prefix}/*",
                        ]
                    }
                },
            },
            {
                "Sid": "AllowReadObjectsOnlyWithinPrefix",
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion",
                ],
                "Resource": object_arn,
            },
        ],
    }

    return policy


def build_cloudwatch_logs_policy(log_group_arn: str) -> dict:
    """
    Build a CloudWatch Logs policy for writing logs to a specific log group.

    Args:
        log_group_arn: ARN of the CloudWatch log group.

    Returns:
        IAM policy document as a Python dictionary.
    """
    if not log_group_arn.strip():
        raise ValueError("log_group_arn must not be empty")

    stream_arn = f"{log_group_arn}:*"

    # CloudWatch Logs commonly needs stream-level permissions for writes.
    # We avoid Resource="*" because data pipeline roles should only write
    # to the log group owned by the workload.
    policy = {
        "Version": POLICY_VERSION,
        "Statement": [
            {
                "Sid": "AllowCreateLogStreamsInPipelineLogGroup",
                "Effect": "Allow",
                "Action": ["logs:CreateLogStream"],
                "Resource": stream_arn,
            },
            {
                "Sid": "AllowWriteLogEventsToPipelineLogGroup",
                "Effect": "Allow",
                "Action": ["logs:PutLogEvents"],
                "Resource": stream_arn,
            },
            {
                "Sid": "AllowDescribeSpecificLogGroup",
                "Effect": "Allow",
                "Action": ["logs:DescribeLogStreams"],
                "Resource": log_group_arn,
            },
        ],
    }

    return policy


def validate_policy_structure(policy: dict) -> bool:
    """
    Validate the minimum structure expected in an IAM policy document.

    This is not a full AWS policy simulator. It checks whether the policy has
    the required IAM document shape and avoids obviously unsafe omissions.

    Args:
        policy: IAM policy document.

    Returns:
        True if the policy has a valid basic structure, otherwise False.
    """
    if not isinstance(policy, dict):
        return False

    if policy.get("Version") != POLICY_VERSION:
        return False

    statements = policy.get("Statement")
    if not isinstance(statements, list) or not statements:
        return False

    required_keys = {"Effect", "Action", "Resource"}

    for statement in statements:
        if not isinstance(statement, dict):
            return False

        if not required_keys.issubset(statement.keys()):
            return False

        if statement["Effect"] not in {"Allow", "Deny"}:
            return False

        action = statement["Action"]
        resource = statement["Resource"]

        if not _is_non_empty_string_or_list(action):
            return False

        if not _is_non_empty_string_or_list(resource):
            return False

    return True


def _is_non_empty_string_or_list(value: Any) -> bool:
    """
    Check whether a value is a non-empty string or a non-empty list of strings.

    IAM allows Action and Resource to be either strings or arrays. Supporting
    both makes the validator realistic while still simple enough to teach.
    """
    if isinstance(value, str):
        return bool(value.strip())

    if isinstance(value, list):
        return bool(value) and all(isinstance(item, str) and item.strip() for item in value)

    return False


def _pretty_print_policy(title: str, policy: dict) -> None:
    """
    Print a policy in readable JSON format.
    """
    print(f"\n{'=' * 80}")
    print(title)
    print(f"{'=' * 80}")
    print(json.dumps(policy, indent=2, sort_keys=False))


def main() -> None:
    """
    Demonstrate policy construction and basic validation.
    """
    print("AWS IAM for Data Engineers - File 01")
    print("Building least-privilege IAM policy documents locally.")
    print("No AWS resources are created by this script.")

    bucket_name = "studybook-data-lake-demo"
    prefix = "raw/events"
    log_group_arn = "arn:aws:logs:us-east-1:123456789012:log-group:/studybook/data-pipeline"

    print("\n[Step 1] Build an S3 read-only policy scoped to one bucket prefix.")
    print("Why it matters: data pipelines should not receive full-bucket access unless required.")
    s3_policy = build_s3_read_only_policy(bucket_name=bucket_name, prefix=prefix)
    _pretty_print_policy("S3 Read-Only Prefix Policy", s3_policy)

    print("\n[Step 2] Validate the S3 policy structure.")
    print("Interview concept: IAM JSON must be valid before it can enforce least privilege.")
    print(f"S3 policy structure valid: {validate_policy_structure(s3_policy)}")

    print("\n[Step 3] Build a CloudWatch Logs write policy scoped to one log group.")
    print("Why it matters: logging permissions should not allow writing everywhere in the account.")
    logs_policy = build_cloudwatch_logs_policy(log_group_arn=log_group_arn)
    _pretty_print_policy("CloudWatch Logs Policy", logs_policy)

    print("\n[Step 4] Validate the CloudWatch Logs policy structure.")
    print(f"CloudWatch Logs policy structure valid: {validate_policy_structure(logs_policy)}")

    # INTERVIEW TIP:
    # When discussing IAM, do not only say "least privilege." Explain exactly
    # which actions, resources, and conditions narrow the permission boundary.
    print("\nInterview takeaway:")
    print(
        "A strong data engineering IAM answer names the actions needed, "
        "scopes resources to exact ARNs, and uses conditions when the service supports them."
    )


if __name__ == "__main__":
    main()