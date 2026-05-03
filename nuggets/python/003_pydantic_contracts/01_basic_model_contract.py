from __future__ import annotations

from pydantic import BaseModel, ValidationError


# BaseModel turns this class into a Pydantic validation contract.
class User(BaseModel):
    id: int
    name: str
    active: bool


def build_valid_user() -> User:
    return User(id=1, name="Sean", active="yes")


def build_invalid_user() -> User:
    # model_validate builds the model if valid, or raises ValidationError if invalid.
    return User.model_validate({"id": "abc", "active": "yes"})


def main() -> None:
    print("VALID CASE")
    u1 = build_valid_user()
    print(u1)

    print("\nINVALID CASE")
    try:
        build_invalid_user()
    except ValidationError as exc:
        # Invalid input raises ValidationError, so we catch it to show the failure clearly.
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
