from __future__ import annotations

from pydantic import BaseModel, ConfigDict, ValidationError


# BaseModel turns this class into a Pydantic validation contract.
class CoercingPayload(BaseModel):
    quantity: int
    enabled: bool


class StrictPayload(BaseModel):
    # strict=True prevents Pydantic from guessing/converting types.
    model_config = ConfigDict(strict=True)

    quantity: int
    enabled: bool


def main() -> None:
    print("VALID CASE (COERCION)")
    # model_validate can coerce compatible strings in non-strict mode.
    coercing = CoercingPayload.model_validate({"quantity": "3", "enabled": "true"})
    print(coercing)

    print("\nVALID CASE (STRICT)")
    strict_valid = StrictPayload.model_validate({"quantity": 3, "enabled": True})
    print(strict_valid)

    print("\nINVALID CASE (STRICT WITH COERCIBLE STRINGS)")
    try:
        StrictPayload.model_validate({"quantity": "3", "enabled": "true"})
    except ValidationError as exc:
        # Invalid input raises ValidationError, so we catch it to compare strict behavior.
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
