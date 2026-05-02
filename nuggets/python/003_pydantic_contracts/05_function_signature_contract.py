from __future__ import annotations

from pydantic import ValidationError, validate_call


@validate_call
def calculate_discount(price: float, discount_percent: float) -> float:
    return round(price * (1 - discount_percent / 100), 2)


def main() -> None:
    print("VALID CASE")
    print(calculate_discount(100.0, 15.0))

    print("\nINVALID CASE")
    try:
        calculate_discount("oops", "bad")
    except ValidationError as exc:
        print("ValidationError raised before function logic:")
        print(exc)


if __name__ == "__main__":
    main()
