"""
FILE: 05_iam_audit_report.py
TOPIC: AWS IAM for Data Engineers
PURPOSE: Generate a local IAM audit-style report from sample policies.
COVERS: audit findings, wildcard detection, over-permissioned policies
INTERVIEW FOCUS: Explain how to identify risky IAM policies (wildcards, broad resources, excessive privilege) and communicate findings clearly.
"""

from __future__ import annotations

import json
from typing import Any


POLICY_VERSION = "2012-10-17"


def find_wildcard_actions(policy: dict) -> list[str]:
    """
    Find actions in the policy that use broad wildcards.

    Examples:
    - "*" is risky because it allows all actions.
    - "s3:*" is risky because it allows every S3 action.
    """
    wildcard_actions: list[str] = []

    for statement in policy.get("Statement", []):
        actions = statement.get("Action", [])

        if isinstance(actions, str):
            actions = [actions]

        for action in actions:
            if action == "*" or action.endswith(":*"):
                wildcard_actions.append(action)

    return wildcard_actions


def find_wildcard_resources(policy: dict) -> list[str]:
    """
    Find resources that are broadly wildcarded.

    Important teaching point:
    - Resource "*" is broad and risky.
    - An ARN ending in /* can be least-privilege for S3 object-prefix access.
    """
    wildcard_resources: list[str] = []

    for statement in policy.get("Statement", []):
        resources = statement.get("Resource", [])

        if isinstance(resources, str):
            resources = [resources]

        for resource in resources:
            if resource == "*":
                wildcard_resources.append(resource)

    return wildcard_resources


def score_policy_risk(policy: dict) -> dict[str, int | str]:
    """
    Score policy risk based on simple audit heuristics.
    """
    wildcard_actions = find_wildcard_actions(policy)
    wildcard_resources = find_wildcard_resources(policy)

    score = 0

    if "*" in wildcard_actions:
        score += 75
    elif wildcard_actions:
        score += 50

    if "*" in wildcard_resources:
        score += 50

    if score == 0:
        level = "LOW"
    elif score <= 50:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return {
        "risk_score": score,
        "risk_level": level,
        "wildcard_actions": wildcard_actions,
        "wildcard_resources": wildcard_resources,
    }


def _pretty_print(title: str, data: Any) -> None:
    print(f"\n{'=' * 80}")
    print(title)
    print(f"{'=' * 80}")
    print(json.dumps(data, indent=2))


def main() -> None:
    """
    Demonstrate IAM policy audit analysis locally.
    """
    print("AWS IAM for Data Engineers - File 05")
    print("Generating a local IAM audit-style report.")
    print("No AWS resources are used.")

    print("\n[Step 1] Define sample policies for auditing.")

    safe_policy = {
        "Version": POLICY_VERSION,
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": "arn:aws:s3:::studybook-data/raw/events/*",
            }
        ],
    }

    risky_policy = {
        "Version": POLICY_VERSION,
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:*"],
                "Resource": "*",
            }
        ],
    }

    admin_policy = {
        "Version": POLICY_VERSION,
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "*",
                "Resource": "*",
            }
        ],
    }

    policies = {
        "SAFE_POLICY": safe_policy,
        "RISKY_POLICY": risky_policy,
        "ADMIN_POLICY": admin_policy,
    }

    print("\n[Step 2] Scan for wildcard actions and broad wildcard resources.")

    for name, policy in policies.items():
        actions = find_wildcard_actions(policy)
        resources = find_wildcard_resources(policy)

        print(f"\nPolicy: {name}")
        print(f"- Wildcard actions: {actions}")
        print(f"- Broad wildcard resources: {resources}")

    print("\n[Step 3] Score policy risk.")

    for name, policy in policies.items():
        result = score_policy_risk(policy)
        _pretty_print(f"Risk Report: {name}", result)

    # INTERVIEW TIP:
    # Do not automatically call every wildcard bad. S3 prefix ARNs commonly end
    # with /* because that is how object-level access is scoped.
    #
    # INTERVIEW TIP:
    # The riskiest pattern is Action "*" with Resource "*", because it creates
    # account-wide administrative blast radius.
    print("\nInterview takeaway:")
    print(
        "Strong candidates separate acceptable scoped wildcards, like S3 prefix ARNs, "
        "from dangerous account-wide wildcards like Action '*' and Resource '*'."
    )


if __name__ == "__main__":
    main()