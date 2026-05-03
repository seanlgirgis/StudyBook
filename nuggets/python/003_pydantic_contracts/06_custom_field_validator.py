from __future__ import annotations

from pydantic import BaseModel, ValidationError, field_validator


# BaseModel turns this class into a Pydantic validation contract.
class DeploymentTarget(BaseModel):
    environment: str

    # This validator normalizes and validates one field.
    @field_validator("environment")
    @classmethod
    def normalize_and_validate_environment(cls, value: str) -> str:
        normalized = value.strip().lower()
        allowed = {"dev", "test", "prod"}
        if normalized not in allowed:
            raise ValueError(f"unsupported environment: {value}")
        return normalized


def build_valid_target() -> DeploymentTarget:
    # model_validate applies field validators as part of model creation.
    return DeploymentTarget.model_validate({"environment": "  PROD  "})


def build_invalid_target() -> DeploymentTarget:
    return DeploymentTarget.model_validate({"environment": "stage"})


def main() -> None:
    print("VALID CASE")
    print(build_valid_target())

    print("\nINVALID CASE")
    try:
        build_invalid_target()
    except ValidationError as exc:
        # Invalid input raises ValidationError, so we catch it to show the failure clearly.
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
