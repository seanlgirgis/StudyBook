import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError


# BaseModel turns this class into a Pydantic validation contract.
class Customer(BaseModel):
    customer_id: int
    name: str = Field(min_length=1)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class OrderItem(BaseModel):
    # Field adds value rules beyond the basic type hint.
    sku: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class ShippingAddress(BaseModel):
    line1: str = Field(min_length=1)
    city: str = Field(min_length=1)
    state: str = Field(min_length=2, max_length=2)
    postal_code: str = Field(pattern=r"^\d{5}$")


class Order(BaseModel):
    order_id: int
    # Because these child models inherit BaseModel, Pydantic validates nested contracts too.
    customer: Customer
    items: list[OrderItem] = Field(min_length=1)
    shipping_address: ShippingAddress
    status: str = Field(pattern=r"^(NEW|PAID|SHIPPED|CANCELLED)$")


# Resolve paths from this script so file loading stays local and predictable.
SCRIPT_DIR = Path(__file__).resolve().parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_order(path: Path) -> Order:
    payload = load_json(path)
    # model_validate builds the model if valid, or raises ValidationError if invalid.
    return Order.model_validate(payload)


def main() -> None:
    valid_path = SCRIPT_DIR / "sample_order_valid.json"
    invalid_path = SCRIPT_DIR / "sample_order_invalid.json"

    print("VALID CASE")
    valid_order = load_order(valid_path)
    print(valid_order)

    print("\nINVALID CASE")
    try:
        load_order(invalid_path)
    except ValidationError as exc:
        # Invalid input raises ValidationError, so we catch it to show nested failure paths.
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
