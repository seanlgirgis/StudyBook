"""
FILE: 03_permission_boundaries.py
TOPIC: AWS IAM for Data Engineers
PURPOSE: Demonstrate permission boundaries and guardrails.
COVERS: permission boundaries, explicit deny, blast radius
INTERVIEW FOCUS: Explain how permission boundaries and explicit denies limit what roles *can ever do*, even if policies are misconfigured.
"""

from __future__ import annotations

import json
from typing import List, Dict


POLICY_VERSION = "2012-10-17"


def build_permission_boundary(allowed_services: List[str]) -> dict:
    """
    Build a permission boundary that allows actions only within specified AWS services.

    Args:
        allowed_services: List like ["s3", "logs"]

    Returns:
        IAM permission boundary policy.
    """
    if not allowed_services:
        raise ValueError("allowed_services must not be empty")

    actions: List[str] = []

    for svc in allowed_services:
        clean = svc.strip().lower()
        if not clean:
            continue
        actions.append(f"{clean}:*")

    if not actions:
        raise ValueError("No valid services provided")

    # INTERVIEW TIP:
    # Permission boundaries do NOT grant permissions by themselves.
    # They define the MAXIMUM permissions a role can have.
    return {
        "Version": POLICY_VERSION,
        "Statement": [
            {
                "Sid": "BoundaryAllowOnlySpecificServices",
                "Effect": "Allow",
                "Action": actions,
                "Resource": "*",
            }
        ],
    }


def build_explicit_deny_policy(denied_actions: List[str]) -> dict:
    """
    Build an explicit deny policy.

    Args:
        denied_actions: List of actions to deny, e.g. ["s3:DeleteObject"]

    Returns:
        IAM deny policy.
    """
    if not denied_actions:
        raise ValueError("denied_actions must not be empty")

    clean_actions = [a.strip() for a in denied_actions if a.strip()]

    if not clean_actions:
        raise ValueError("No valid denied actions provided")

    # INTERVIEW TIP:
    # Explicit Deny ALWAYS overrides Allow in IAM evaluation.
    return {
        "Version": POLICY_VERSION,
        "Statement": [
            {
                "Sid": "ExplicitDenyCriticalActions",
                "Effect": "Deny",
                "Action": clean_actions,
                "Resource": "*",
            }
        ],
    }


def evaluate_action_against_policy(action: str, policy: dict) -> str:
    """
    Evaluate whether an action is allowed or denied by a simple policy.

    This is a simplified evaluator (not AWS-complete).
    It demonstrates key interview concepts:
    - Explicit Deny overrides Allow
    - Wildcard matching
    - Default Deny

    Args:
        action: Action like "s3:GetObject"
        policy: IAM policy

    Returns:
        "ALLOW", "DENY", or "IMPLICIT_DENY"
    """
    if not action.strip():
        raise ValueError("action must not be empty")

    if not isinstance(policy, dict):
        raise ValueError("policy must be a dictionary")

    statements = policy.get("Statement", [])
    if not isinstance(statements, list):
        raise ValueError("policy Statement must be a list")

    matched_allow = False

    for stmt in statements:
        effect = stmt.get("Effect")
        actions = stmt.get("Action")

        if not _action_matches(action, actions):
            continue

        if effect == "Deny":
            return "DENY"

        if effect == "Allow":
            matched_allow = True

    if matched_allow:
        return "ALLOW"

    return "IMPLICIT_DENY"


def _action_matches(action: str, policy_actions) -> bool:
    """
    Check if an action matches a policy action list or string.
    Supports:
    - exact match
    - wildcard like "s3:*"
    """
    if isinstance(policy_actions, str):
        policy_actions = [policy_actions]

    if not isinstance(policy_actions, list):
        return False

    for pa in policy_actions:
        if pa == "*":
            return True

        if pa.endswith(":*"):
            service = pa.split(":")[0]
            if action.startswith(f"{service}:"):
                return True

        if pa.lower() == action.lower():
            return True

    return False


def _pretty_print_policy(title: str, policy: dict) -> None:
    print(f"\n{'=' * 80}")
    print(title)
    print(f"{'=' * 80}")
    print(json.dumps(policy, indent=2))


def main() -> None:
    print("AWS IAM for Data Engineers - File 03")
    print("Demonstrating permission boundaries and explicit deny.")
    print("No AWS resources are created by this script.")

    print("\n[Step 1] Build a permission boundary allowing only S3 and Logs.")
    boundary = build_permission_boundary(["s3", "logs"])
    _pretty_print_policy("Permission Boundary Policy", boundary)

    print("\n[Step 2] Build an explicit deny policy for dangerous actions.")
    deny_policy = build_explicit_deny_policy(["s3:DeleteObject"])
    _pretty_print_policy("Explicit Deny Policy", deny_policy)

    print("\n[Step 3] Evaluate actions against the boundary.")
    test_actions = [
        "s3:GetObject",
        "s3:DeleteObject",
        "ec2:StartInstances",
        "logs:PutLogEvents",
    ]

    for act in test_actions:
        result = evaluate_action_against_policy(act, boundary)
        print(f"Boundary evaluation for {act}: {result}")

    print("\n[Step 4] Evaluate actions against explicit deny policy.")
    for act in test_actions:
        result = evaluate_action_against_policy(act, deny_policy)
        print(f"Deny policy evaluation for {act}: {result}")

    print("\n[Step 5] Combined reasoning (conceptual).")
    print("In real AWS evaluation:")
    print("- Explicit DENY wins first")
    print("- Then ALLOW if within boundary")
    print("- Otherwise IMPLICIT DENY")

    # INTERVIEW TIP:
    # A strong answer: "We use permission boundaries to prevent privilege escalation
    # even if someone attaches an overly broad policy later."
    print("\nInterview takeaway:")
    print(
        "Permission boundaries cap maximum access, while explicit deny policies enforce hard guardrails."
    )


if __name__ == "__main__":
    main()