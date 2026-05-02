from __future__ import annotations

from pydantic import BaseModel, ConfigDict, ValidationError


class CoercingPayload(BaseModel):
    quantity: int
    enabled: bool


class StrictPayload(BaseModel):
    model_config = ConfigDict(strict=True)

    quantity: int
    enabled: bool


def main() -> None:
    print("VALID CASE (COERCION)")
    coercing = CoercingPayload.model_validate({"quantity": "3", "enabled": "true"})
    print(coercing)

    print("\nVALID CASE (STRICT)")
    strict_valid = StrictPayload.model_validate({"quantity": 3, "enabled": True})
    print(strict_valid)

    print("\nINVALID CASE (STRICT WITH COERCIBLE STRINGS)")
    try:
        StrictPayload.model_validate({"quantity": "3", "enabled": "true"})
    except ValidationError as exc:
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
