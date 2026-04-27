"""
FILE: 02_roles_and_trust_policies.py
TOPIC: AWS IAM for Data Engineers
PURPOSE: Create trust policies and explain role assumption.
COVERS: trust policy principals, sts:AssumeRole, external IDs
INTERVIEW FOCUS: Explain the difference between permissions policies and trust policies, and how secure role assumption works.
"""

from __future__ import annotations

import json
import re
from typing import Any


POLICY_VERSION = "2012-10-17"


def build_assume_role_trust_policy(service_principal: str) -> dict:
    """
    Build a trust policy that allows an AWS service to assume a role.

    Args:
        service_principal: AWS service principal, such as glue.amazonaws.com.

    Returns:
        IAM trust policy document as a dictionary.
    """
    if not service_principal.strip():
        raise ValueError("service_principal must not be empty")

    if not service_principal.endswith(".amazonaws.com"):
        raise ValueError("service_principal should look like glue.amazonaws.com")

    return {
        "Version": POLICY_VERSION,
        "Statement": [
            {
                "Sid": "AllowServiceToAssumeRole",
                "Effect": "Allow",
                "Principal": {
                    "Service": service_principal,
                },
                "Action": "sts:AssumeRole",
            }
        ],
    }


def build_cross_account_trust_policy(account_id: str, external_id: str) -> dict:
    """
    Build a cross-account trust policy using an external ID.

    Args:
        account_id: Trusted AWS account ID.
        external_id: Shared external ID used to reduce confused-deputy risk.

    Returns:
        IAM trust policy document as a dictionary.
    """
    if not re.fullmatch(r"\d{12}", account_id):
        raise ValueError("account_id must be a 12-digit AWS account ID")

    if not external_id.strip():
        raise ValueError("external_id must not be empty")

    trusted_root_arn = f"arn:aws:iam::{account_id}:root"

    # INTERVIEW TIP:
    # A trust policy answers "who can assume this role?" A permissions policy
    # answers "what can the role do after it is assumed?"
    return {
        "Version": POLICY_VERSION,
        "Statement": [
            {
                "Sid": "AllowTrustedAccountWithExternalId",
                "Effect": "Allow",
                "Principal": {
                    "AWS": trusted_root_arn,
                },
                "Action": "sts:AssumeRole",
                "Condition": {
                    "StringEquals": {
                        "sts:ExternalId": external_id,
                    }
                },
            }
        ],
    }


def explain_trust_policy(policy: dict) -> list[str]:
    """
    Convert a trust policy into plain-English explanation lines.

    Args:
        policy: IAM trust policy document.

    Returns:
        List of explanation strings.
    """
    if not isinstance(policy, dict):
        raise ValueError("policy must be a dictionary")

    statements = policy.get("Statement")
    if not isinstance(statements, list) or not statements:
        raise ValueError("policy must contain a non-empty Statement list")

    explanations: list[str] = []

    for index, statement in enumerate(statements, start=1):
        if not isinstance(statement, dict):
            raise ValueError("each statement must be a dictionary")

        effect = statement.get("Effect", "Unknown")
        principal = statement.get("Principal", {})
        action = statement.get("Action", "Unknown")
        condition = statement.get("Condition")

        principal_text = _format_principal(principal)
        explanation = (
            f"Statement {index}: {effect} lets {principal_text} call {action} "
            "against this role."
        )
        explanations.append(explanation)

        if condition:
            explanations.append(
                f"Statement {index}: The assumption is further restricted by condition "
                f"{json.dumps(condition, sort_keys=True)}."
            )
        else:
            explanations.append(
                f"Statement {index}: No condition is present, so access relies entirely "
                "on the principal and AWS-side authorization checks."
            )

    return explanations


def _format_principal(principal: Any) -> str:
    """
    Format an IAM Principal block for teaching output.
    """
    if isinstance(principal, dict):
        if "Service" in principal:
            return f"the AWS service principal {principal['Service']}"
        if "AWS" in principal:
            return f"the AWS principal {principal['AWS']}"
        return f"the principal block {json.dumps(principal, sort_keys=True)}"

    return str(principal)


def _pretty_print_policy(title: str, policy: dict) -> None:
    """
    Print policy JSON in a readable format.
    """
    print(f"\n{'=' * 80}")
    print(title)
    print(f"{'=' * 80}")
    print(json.dumps(policy, indent=2, sort_keys=False))


def main() -> None:
    """
    Demonstrate service and cross-account trust policies.
    """
    print("AWS IAM for Data Engineers - File 02")
    print("Building trust policies locally.")
    print("No AWS resources are created by this script.")

    service_principal = "glue.amazonaws.com"
    trusted_account_id = "123456789012"
    external_id = "studybook-data-platform-external-id"

    print("\n[Step 1] Build a service trust policy.")
    print("Why it matters: AWS services like Glue, EMR, Lambda, and Step Functions assume roles to run workloads.")
    service_policy = build_assume_role_trust_policy(service_principal)
    _pretty_print_policy("Service AssumeRole Trust Policy", service_policy)

    print("\n[Step 2] Explain the service trust policy.")
    for line in explain_trust_policy(service_policy):
        print(f"- {line}")

    print("\n[Step 3] Build a cross-account trust policy with an external ID.")
    print("Why it matters: cross-account access is common in centralized data platforms and vendor integrations.")
    cross_account_policy = build_cross_account_trust_policy(
        account_id=trusted_account_id,
        external_id=external_id,
    )
    _pretty_print_policy("Cross-Account Trust Policy", cross_account_policy)

    print("\n[Step 4] Explain the cross-account trust policy.")
    for line in explain_trust_policy(cross_account_policy):
        print(f"- {line}")

    # INTERVIEW TIP:
    # Senior candidates should mention the confused deputy problem when discussing
    # third-party or cross-account role assumption.
    print("\nInterview takeaway:")
    print(
        "A role needs both sides correct: the trust policy must allow assumption, "
        "and the permissions policy must allow useful actions after assumption."
    )


if __name__ == "__main__":
    main()