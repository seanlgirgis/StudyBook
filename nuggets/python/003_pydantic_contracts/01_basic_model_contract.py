from __future__ import annotations

from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name: str
    active: bool


def build_valid_user() -> User:
    return User.model_validate({"id": 1, "name": "Sean", "active": True})


def build_invalid_user() -> User:
    return User.model_validate({"id": "abc", "active": "yes"})


def main() -> None:
    print("VALID CASE")
    valid = build_valid_user()
    print(valid)

    print("\nINVALID CASE")
    try:
        build_invalid_user()
    except ValidationError as exc:
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
