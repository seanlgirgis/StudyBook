from __future__ import annotations

from pydantic import BaseModel, Field, ValidationError


# BaseModel turns this class into a Pydantic validation contract.
class Customer(BaseModel):
    customer_id: int
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Order(BaseModel):
    order_id: int
    # Because Customer inherits BaseModel, Pydantic validates it as a nested contract.
    customer: Customer
    items: list[str] = Field(min_length=1)


def build_valid_order() -> Order:
    # model_validate validates every nested level, not just top-level fields.
    return Order.model_validate(
        {
            "order_id": 101,
            "customer": {"customer_id": 7, "email": "buyer@example.com"},
            "items": ["book", "pen"],
        }
    )


def build_invalid_order() -> Order:
    return Order.model_validate(
        {
            "order_id": 101,
            "customer": {"customer_id": "x", "email": "broken"},
            "items": [],
        }
    )


def main() -> None:
    print("VALID CASE")
    print(build_valid_order())

    print("\nINVALID CASE")
    try:
        build_invalid_order()
    except ValidationError as exc:
        # Invalid input raises ValidationError, so we catch it to show nested failure paths.
        print("ValidationError raised (note nested paths):")
        print(exc)


if __name__ == "__main__":
    main()
