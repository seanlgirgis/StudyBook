"""Stage 1, Brick 66: Find an audit record by correlation ID.

Functionality studied:
    Read the existing operation audit summary, obtain its latest
    correlation ID, and retrieve the exact matching JSON Lines record.

This brick does not call the AI provider.

It searches existing audit evidence only.
"""

import json
from pathlib import Path

from rag_foundation import (
    find_operation_audit_record,
    summarize_operation_audit,
)


AUDIT_FILE = (
    Path(__file__).resolve().parent
    / "output"
    / "64_operation_audit.jsonl"
)


def main() -> None:
    """Find and display the latest operation audit record."""

    summary = summarize_operation_audit(
        AUDIT_FILE
    )

    correlation_id = (
        summary.latest_correlation_id
    )

    print("AUDIT LOOKUP")
    print("------------")
    print(f"Audit file: {AUDIT_FILE}")
    print(
        f"Latest correlation ID: "
        f"{correlation_id}"
    )

    if correlation_id is None:
        print("\nLOOKUP RESULT")
        print("-------------")
        print("No audit records are available.")

        return

    record = find_operation_audit_record(
        AUDIT_FILE,
        correlation_id,
    )

    print("\nLOOKUP RESULT")
    print("-------------")

    if record is None:
        print(
            "No record matched the correlation ID."
        )

        return

    print(
        json.dumps(
            record,
            indent=2,
            ensure_ascii=False,
        )
    )

    print("\nFINAL CHECK")
    print("-----------")

    if (
        record["correlation_id"]
        == correlation_id
    ):
        print(
            "PASS: the audit record was found using "
            "its correlation ID."
        )
    else:
        print(
            "FAIL: the returned audit record did not "
            "match the requested correlation ID."
        )


if __name__ == "__main__":
    main()
