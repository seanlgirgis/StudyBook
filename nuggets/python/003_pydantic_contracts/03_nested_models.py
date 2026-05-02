from __future__ import annotations

from pydantic import BaseModel, Field, ValidationError


class Customer(BaseModel):
    customer_id: int
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Order(BaseModel):
    order_id: int
    customer: Customer
    items: list[str] = Field(min_length=1)


def build_valid_order() -> Order:
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
        print("ValidationError raised (note nested paths):")
        print(exc)


if __name__ == "__main__":
    main()
