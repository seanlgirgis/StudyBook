"""
FILE: 04_sts_assume_role_demo.py
TOPIC: AWS IAM for Data Engineers
PURPOSE: Assume a role with STS when environment variables are configured.
COVERS: STS, temporary credentials, safe skipping
INTERVIEW FOCUS: Explain why production data pipelines use temporary credentials from STS instead of long-lived access keys.
"""

from __future__ import annotations

import json
import os
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError, ProfileNotFound


AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ROLE_ARN_ENV = "STUDYBOOK_ASSUME_ROLE_ARN"
EXTERNAL_ID_ENV = "STUDYBOOK_EXTERNAL_ID"


def get_sts_client(profile_name: str | None = None):
    """
    Create an STS client using an optional AWS profile.

    Args:
        profile_name: AWS profile name. If None, boto3 default credential resolution is used.

    Returns:
        boto3 STS client.
    """
    selected_profile = profile_name or AWS_PROFILE

    try:
        session = boto3.Session(profile_name=selected_profile, region_name=AWS_REGION)
        return session.client("sts")
    except ProfileNotFound:
        print(f"Profile '{selected_profile}' was not found. Falling back to default boto3 credentials.")
        session = boto3.Session(region_name=AWS_REGION)
        return session.client("sts")


def assume_role(role_arn: str, session_name: str, external_id: str | None = None) -> dict:
    """
    Assume an IAM role using AWS STS.

    Args:
        role_arn: Role ARN to assume.
        session_name: Human-readable session name for audit logs.
        external_id: Optional external ID for cross-account trust policies.

    Returns:
        STS AssumeRole response.
    """
    if not role_arn.strip():
        raise ValueError("role_arn must not be empty")

    if not session_name.strip():
        raise ValueError("session_name must not be empty")

    client = get_sts_client()

    request: dict[str, Any] = {
        "RoleArn": role_arn,
        "RoleSessionName": session_name,
    }

    if external_id:
        request["ExternalId"] = external_id

    # INTERVIEW TIP:
    # STS returns temporary credentials with an expiration. This reduces the risk
    # compared with static access keys stored on servers or developer laptops.
    return client.assume_role(**request)


def print_caller_identity() -> dict:
    """
    Print the current AWS caller identity.

    Returns:
        STS GetCallerIdentity response.
    """
    client = get_sts_client()
    identity = client.get_caller_identity()

    print("\nCurrent AWS caller identity:")
    print(json.dumps(identity, indent=2, default=str))

    return identity


def _print_assumed_role_summary(response: dict) -> None:
    """
    Print safe metadata from an AssumeRole response without leaking secret keys.
    """
    credentials = response.get("Credentials", {})
    assumed_role_user = response.get("AssumedRoleUser", {})

    safe_summary = {
        "AssumedRoleArn": assumed_role_user.get("Arn"),
        "AssumedRoleId": assumed_role_user.get("AssumedRoleId"),
        "CredentialExpiration": str(credentials.get("Expiration")),
        "HasAccessKeyId": bool(credentials.get("AccessKeyId")),
        "HasSecretAccessKey": bool(credentials.get("SecretAccessKey")),
        "HasSessionToken": bool(credentials.get("SessionToken")),
    }

    print("\nAssumeRole succeeded. Safe summary:")
    print(json.dumps(safe_summary, indent=2))


def main() -> None:
    """
    Demonstrate STS caller identity and optional AssumeRole.
    """
    print("AWS IAM for Data Engineers - File 04")
    print("Demonstrating STS and temporary credentials.")
    print("This script does not create AWS resources.")

    print(f"\nConfigured AWS profile default: {AWS_PROFILE}")
    print(f"Configured AWS region default: {AWS_REGION}")

    print("\n[Step 1] Try to print caller identity.")
    print("Why it matters: this tells you which principal your pipeline is actually running as.")

    try:
        print_caller_identity()
    except (BotoCoreError, ClientError, NoCredentialsError) as exc:
        print("Caller identity could not be retrieved.")
        print(f"Reason: {exc}")
        print("Safe skip: configure AWS_PROFILE or default AWS credentials to run the live STS demo.")

    role_arn = os.getenv(ROLE_ARN_ENV)
    external_id = os.getenv(EXTERNAL_ID_ENV)

    print("\n[Step 2] Optional AssumeRole demo.")
    print(f"Set {ROLE_ARN_ENV} to run this step against a real role.")
    print(f"Set {EXTERNAL_ID_ENV} too if the trust policy requires an external ID.")

    if not role_arn:
        print("Safe skip: no role ARN provided, so no AssumeRole call was attempted.")
    else:
        try:
            response = assume_role(
                role_arn=role_arn,
                session_name="studybook-iam-demo-session",
                external_id=external_id,
            )
            _print_assumed_role_summary(response)
        except (BotoCoreError, ClientError, NoCredentialsError) as exc:
            print("AssumeRole failed safely.")
            print(f"Reason: {exc}")

    # INTERVIEW TIP:
    # In production, temporary credentials should be delivered through IAM roles,
    # instance profiles, ECS task roles, Lambda execution roles, or assumed roles.
    print("\nInterview takeaway:")
    print(
        "Use STS temporary credentials for pipelines so access is time-bound, auditable, "
        "and easier to revoke than long-lived static keys."
    )


if __name__ == "__main__":
    main()