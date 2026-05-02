from __future__ import annotations

from pydantic import BaseModel, ValidationError


class Product(BaseModel):
    sku: str
    price: float
    in_stock: bool


def build_valid_product() -> Product:
    return Product.model_validate({"sku": "BK-001", "price": 19.99, "in_stock": True})


def build_invalid_product() -> Product:
    return Product.model_validate({"sku": "BK-002", "price": "free", "in_stock": "yes"})


def main() -> None:
    print("VALID CASE")
    product = build_valid_product()
    print("model_dump():")
    print(product.model_dump())
    print("\nmodel_dump_json():")
    print(product.model_dump_json(indent=2))
    print("\nmodel_json_schema():")
    print(Product.model_json_schema())

    print("\nINVALID CASE")
    try:
        build_invalid_product()
    except ValidationError as exc:
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
