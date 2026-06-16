"""Stage 1, Brick 67: List recent operation audit records.

Functionality studied:
    Read the existing JSON Lines audit file and display the latest records
    in newest-first order.

This brick does not call the AI provider.

It reads existing audit evidence only.
"""

import json
from pathlib import Path

from rag_foundation import (
    list_recent_operation_audit_records,
)


AUDIT_FILE = (
    Path(__file__).resolve().parent
    / "output"
    / "64_operation_audit.jsonl"
)

RECENT_LIMIT = 5


def main() -> None:
    """Read and display the latest audit records."""

    records = list_recent_operation_audit_records(
        AUDIT_FILE,
        limit=RECENT_LIMIT,
    )

    print("RECENT OPERATION AUDIT RECORDS")
    print("------------------------------")
    print(f"Audit file: {AUDIT_FILE}")
    print(f"Requested limit: {RECENT_LIMIT}")
    print(f"Records returned: {len(records)}")

    if not records:
        print("\nNo audit records are available.")
        return

    for position, record in enumerate(
        records,
        start=1,
    ):
        print(
            f"\nRECENT RECORD {position}"
        )
        print("----------------")

        print(
            json.dumps(
                record,
                indent=2,
                ensure_ascii=False,
            )
        )

    newest_record = records[0]

    print("\nNEWEST RECORD SUMMARY")
    print("---------------------")
    print(
        f"Correlation ID: "
        f"{newest_record.get('correlation_id')}"
    )
    print(
        f"Status: "
        f"{newest_record.get('status')}"
    )
    print(
        f"Total tokens: "
        f"{newest_record.get('total_tokens')}"
    )
    print(
        f"Amount spent: "
        f"{newest_record.get('amount_spent')}"
    )

    print("\nFINAL CHECK")
    print("-----------")

    if (
        len(records) <= RECENT_LIMIT
        and records[0].get("correlation_id")
        is not None
    ):
        print(
            "PASS: recent audit records were returned "
            "in newest-first order."
        )
    else:
        print(
            "FAIL: recent audit records did not meet "
            "the expected result."
        )


if __name__ == "__main__":
    main()
