"""Stage 1, Brick 68: Validate application startup settings.

Functionality studied:
    Build one validated non-secret settings object from application
    constants and the current environment.

This brick does not call the AI provider.
"""

from decimal import Decimal
import json
import os

from rag_foundation import (
    ApplicationSettings,
)
from rag_foundation.costs import (
    TokenRates,
)


MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.4-nano",
)

MODEL_RATES = TokenRates(
    input_per_million=Decimal("0.20"),
    output_per_million=Decimal("1.25"),
)


def main() -> None:
    """Validate startup settings without exposing the API key."""

    settings = ApplicationSettings.from_environment(
        model=MODEL,
        rates=MODEL_RATES,
        budget_limit=Decimal("0.001000"),
        projected_request_cost=Decimal("0.000100"),
        warning_threshold_percentage=Decimal("80"),
        max_attempts=3,
        retry_delay_seconds=0,
    )

    safe_settings = settings.to_json_dict()

    print("APPLICATION SETTINGS")
    print("--------------------")
    print(
        json.dumps(
            safe_settings,
            indent=2,
        )
    )

    print("\nSTARTUP CHECK")
    print("-------------")
    print(
        f"API-key variable: "
        f"{settings.api_key_environment_variable}"
    )
    print("API-key value stored in settings: False")
    print(f"Model: {settings.model}")
    print(f"Maximum attempts: {settings.max_attempts}")
    print(
        f"Projected request cost: "
        f"${settings.projected_request_cost}"
    )
    print(
        f"Application budget: "
        f"${settings.budget_limit}"
    )

    key_available = bool(
        os.getenv(
            settings.api_key_environment_variable
        )
    )

    print(
        f"Required API-key variable available: "
        f"{key_available}"
    )

    print("\nFINAL CHECK")
    print("-----------")

    if (
        key_available
        and "api_key" not in safe_settings
        and settings.model != ""
    ):
        print(
            "PASS: startup settings are valid and "
            "the API-key value was not stored."
        )
    else:
        print(
            "FAIL: startup settings did not meet "
            "the expected safety rules."
        )


if __name__ == "__main__":
    main()
