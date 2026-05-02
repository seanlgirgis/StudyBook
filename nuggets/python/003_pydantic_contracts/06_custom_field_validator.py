from __future__ import annotations

from pydantic import BaseModel, ValidationError, field_validator


class DeploymentTarget(BaseModel):
    environment: str

    @field_validator("environment")
    @classmethod
    def normalize_and_validate_environment(cls, value: str) -> str:
        normalized = value.strip().lower()
        allowed = {"dev", "test", "prod"}
        if normalized not in allowed:
            raise ValueError(f"unsupported environment: {value}")
        return normalized


def build_valid_target() -> DeploymentTarget:
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
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
