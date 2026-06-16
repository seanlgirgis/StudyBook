"""Stage 1, Brick 65: Read and summarize a JSON Lines audit file.

Functionality studied:
    Read the compact JSON Lines audit records created by Brick 64 and
    calculate simple totals.

This brick does not call the AI provider.

It summarizes existing audit evidence only.
"""

import json
from pathlib import Path

from rag_foundation import (
    summarize_operation_audit,
)


AUDIT_FILE = (
    Path(__file__).resolve().parent
    / "output"
    / "64_operation_audit.jsonl"
)


def main() -> None:
    """Read the audit file and print one compact summary."""

    summary = summarize_operation_audit(
        AUDIT_FILE
    )

    print("OPERATION AUDIT SUMMARY")
    print("-----------------------")
    print(f"Audit file: {AUDIT_FILE}")
    print(f"Total records: {summary.total_records}")
    print(f"Success: {summary.success_count}")
    print(f"Fallback: {summary.fallback_count}")
    print(f"Blocked: {summary.blocked_count}")
    print(
        f"Input tokens: "
        f"{summary.total_input_tokens}"
    )
    print(
        f"Output tokens: "
        f"{summary.total_output_tokens}"
    )
    print(
        f"Total tokens: "
        f"{summary.total_tokens}"
    )
    print(
        f"Total amount spent: "
        f"${summary.total_amount_spent}"
    )
    print(
        f"Latest correlation ID: "
        f"{summary.latest_correlation_id}"
    )

    print("\nJSON-SAFE SUMMARY")
    print("-----------------")
    print(
        json.dumps(
            summary.to_json_dict(),
            indent=2,
        )
    )

    print("\nFINAL CHECK")
    print("-----------")

    status_count = (
        summary.success_count
        + summary.fallback_count
        + summary.blocked_count
    )

    if (
        status_count == summary.total_records
        and summary.total_tokens
        == (
            summary.total_input_tokens
            + summary.total_output_tokens
        )
    ):
        print(
            "PASS: the JSON Lines audit file was "
            "read and summarized correctly."
        )
    else:
        print(
            "FAIL: the audit summary totals are inconsistent."
        )


if __name__ == "__main__":
    main()
