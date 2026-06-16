"""Stage 1, Brick 63: Save OperationResult using atomic JSON writing.

Functionality studied:
    Execute one real AI operation, serialize its structured result safely,
    and persist it to a JSON file using atomic replacement.

Workflow:
    1. Create one correlation ID.
    2. Reserve projected application budget.
    3. Retry simulated transient failures.
    4. Make the real provider request.
    5. Reconcile actual estimated cost.
    6. Build safe operation diagnostics.
    7. Return one validated OperationResult.
    8. Convert the result with to_json_dict().
    9. Write it using write_json_atomic().
    10. Read the persisted JSON back.
    11. Validate the saved operation identity and budget representation.

Reusable mechanics:
    - OperationResult
    - OperationDiagnosticContext
    - BudgetReservationScope
    - CostBudgetTracker
    - RetryPolicy
    - run_with_retry()
    - build_success_diagnostic()
    - create_correlation_id()
    - estimate_request_cost()
    - write_json_atomic()
    - OpenAITextProvider
    - TextGenerationRequest

Application-specific behavior:
    - budget size;
    - projected cost;
    - retry count;
    - simulated failures;
    - prompt;
    - target output filename;
    - displayed validation.

Important:
    The writer first creates a complete temporary file in the destination
    directory and then atomically replaces the target.

    A partial write therefore cannot become the official saved result.
"""

from decimal import Decimal
import json
from pathlib import Path
from typing import Any

from rag_foundation import (
    OpenAITextProvider,
    OperationDiagnosticContext,
    OperationResult,
    TextGenerationRequest,
    write_json_atomic,
)
from rag_foundation.budget import (
    BudgetReservationScope,
    CostBudgetTracker,
)
from rag_foundation.correlation import (
    create_correlation_id,
)
from rag_foundation.costs import (
    TokenRates,
    estimate_request_cost,
)
from rag_foundation.diagnostics import (
    build_success_diagnostic,
)
from rag_foundation.retry import (
    RetryPolicy,
    run_with_retry,
)


MODEL = "gpt-5.4-nano"

MODEL_RATES = TokenRates(
    input_per_million=Decimal("0.20"),
    output_per_million=Decimal("1.25"),
)

APPLICATION_BUDGET = Decimal("0.000100")
PROJECTED_COST = Decimal("0.000070")

MAX_ATTEMPTS = 3
SIMULATED_FAILURES = 2

OUTPUT_DIRECTORY = (
    Path(__file__).resolve().parent
    / "output"
)

OUTPUT_FILE = (
    OUTPUT_DIRECTORY
    / "63_operation_result.json"
)


def contains_decimal(
    value: Any,
) -> bool:
    """Return whether a nested value contains a Decimal."""

    if isinstance(value, Decimal):
        return True

    if isinstance(value, dict):
        return any(
            contains_decimal(item)
            for item in value.values()
        )

    if isinstance(
        value,
        (
            list,
            tuple,
        ),
    ):
        return any(
            contains_decimal(item)
            for item in value
        )

    return False


def related_temporary_files(
    destination: Path,
) -> list[Path]:
    """Return leftover temporary files for one destination."""

    return list(
        destination.parent.glob(
            f".{destination.name}.*.tmp"
        )
    )


def execute_operation() -> OperationResult:
    """Execute one guarded request and return OperationResult."""

    provider = OpenAITextProvider()

    tracker = CostBudgetTracker(
        budget_limit=APPLICATION_BUDGET,
        warning_threshold_percentage=Decimal("80"),
    )

    correlation_id = create_correlation_id(
        prefix="rag"
    )

    request = TextGenerationRequest(
        instructions=(
            "Use plain English. "
            "Return exactly one short sentence."
        ),
        prompt=(
            "Explain why atomic file replacement is useful "
            "when saving an AI operation result."
        ),
        model=MODEL,
        temperature=0.0,
    )

    attempts = {
        "count": 0,
    }

    print("WORKFLOW START")
    print("--------------")
    print(f"Correlation ID: {correlation_id}")
    print(f"Budget limit: ${APPLICATION_BUDGET:.10f}")
    print(f"Projected cost: ${PROJECTED_COST:.10f}")

    with BudgetReservationScope(
        tracker,
        PROJECTED_COST,
    ) as scope:
        print("\nBUDGET RESERVATION")
        print("------------------")
        print(f"Allowed: {scope.allowed}")
        print(f"Reason: {scope.decision.reason}")
        print(
            f"Reserved: "
            f"${tracker.amount_reserved:.10f}"
        )

        if not scope.allowed:
            raise RuntimeError(
                "The demonstration budget unexpectedly "
                "blocked the operation."
            )

        def generate_with_temporary_failures():
            """Simulate failures before the real provider request."""

            attempts["count"] += 1

            print(
                f"Attempt {attempts['count']} "
                f"| correlation_id={correlation_id}"
            )

            if attempts["count"] <= SIMULATED_FAILURES:
                raise ConnectionError(
                    "Simulated temporary provider failure."
                )

            return provider.generate(
                request
            )

        provider_result = run_with_retry(
            generate_with_temporary_failures,
            retry_on=(
                ConnectionError,
            ),
            policy=RetryPolicy(
                max_attempts=MAX_ATTEMPTS,
                delay_seconds=0,
            ),
        )

        actual_cost = estimate_request_cost(
            result=provider_result,
            rates=MODEL_RATES,
        )

        budget_status = scope.reconcile(
            actual_cost
        )

        operation_context = OperationDiagnosticContext(
            correlation_id=correlation_id,
            attempt_count=attempts["count"],
        )

        diagnostic = build_success_diagnostic(
            provider_result,
            context=operation_context,
        )

        return OperationResult(
            status="success",
            user_message=provider_result.require_text(),
            correlation_id=correlation_id,
            attempt_count=attempts["count"],
            diagnostic=diagnostic,
            budget_status=budget_status,
        )


def save_operation_result(
    result: OperationResult,
    destination: Path,
) -> Path:
    """Serialize and atomically save one OperationResult."""

    json_safe_result = result.to_json_dict()

    return write_json_atomic(
        json_safe_result,
        destination,
        indent=2,
        ensure_ascii=False,
    )


def load_saved_result(
    destination: Path,
) -> dict[str, Any]:
    """Load one saved JSON operation result."""

    with destination.open(
        mode="r",
        encoding="utf-8",
    ) as input_file:
        loaded = json.load(
            input_file
        )

    if not isinstance(loaded, dict):
        raise RuntimeError(
            "Saved operation result must be a JSON object."
        )

    return loaded


def main() -> None:
    """Execute, save, reload, and validate the operation result."""

    result = execute_operation()

    saved_path = save_operation_result(
        result,
        OUTPUT_FILE,
    )

    loaded_result = load_saved_result(
        saved_path
    )

    temporary_files = related_temporary_files(
        saved_path
    )

    json_safe_result = result.to_json_dict()

    print("\nMODEL RESULT")
    print("------------")
    print(result.user_message)

    print("\nATOMIC FILE WRITE")
    print("-----------------")
    print(f"Saved path: {saved_path}")
    print(f"File exists: {saved_path.exists()}")
    print(f"File size: {saved_path.stat().st_size} bytes")
    print(
        f"Temporary files remaining: "
        f"{len(temporary_files)}"
    )

    print("\nPERSISTED RESULT")
    print("----------------")
    print(
        json.dumps(
            loaded_result,
            indent=2,
            ensure_ascii=False,
        )
    )

    correlation_matches = (
        result.correlation_id
        == result.diagnostic.correlation_id
        == json_safe_result["correlation_id"]
        == loaded_result["correlation_id"]
        == loaded_result["diagnostic"]["correlation_id"]
    )

    attempts_match = (
        result.attempt_count
        == result.diagnostic.attempt_count
        == json_safe_result["attempt_count"]
        == loaded_result["attempt_count"]
        == loaded_result["diagnostic"]["attempt_count"]
    )

    persisted_has_decimal = contains_decimal(
        loaded_result
    )

    amount_spent_is_string = isinstance(
        loaded_result["budget_status"]["amount_spent"],
        str,
    )

    print("\nPERSISTENCE CHECKS")
    print("------------------")
    print(
        f"Correlation IDs aligned: "
        f"{correlation_matches}"
    )
    print(
        f"Attempt counts aligned: "
        f"{attempts_match}"
    )
    print(
        f"Persisted result contains Decimal: "
        f"{persisted_has_decimal}"
    )
    print(
        f"Persisted amount_spent type: "
        f"{type(loaded_result['budget_status']['amount_spent']).__name__}"
    )
    print(
        f"Temporary files remaining: "
        f"{len(temporary_files)}"
    )

    print("\nFINAL CHECK")
    print("-----------")

    if (
        result.status == "success"
        and saved_path.exists()
        and saved_path == OUTPUT_FILE
        and correlation_matches
        and attempts_match
        and not persisted_has_decimal
        and amount_spent_is_string
        and len(temporary_files) == 0
    ):
        print(
            "PASS: the structured OperationResult was saved "
            "as complete JSON using atomic file replacement."
        )
    else:
        print(
            "FAIL: the persisted operation result did not "
            "meet the expected atomic-write guarantees."
        )


if __name__ == "__main__":
    main()
