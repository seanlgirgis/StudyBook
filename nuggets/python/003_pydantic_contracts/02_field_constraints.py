from __future__ import annotations

from pydantic import BaseModel, Field, ValidationError


class Profile(BaseModel):
    age: int = Field(ge=18)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    score: float = Field(ge=0, le=100)


def build_valid_profile() -> Profile:
    return Profile.model_validate({"age": 28, "email": "sean@example.com", "score": 88.5})


def build_invalid_profile() -> Profile:
    return Profile.model_validate({"age": 16, "email": "bad-email", "score": 150})


def main() -> None:
    print("VALID CASE")
    print(build_valid_profile())

    print("\nINVALID CASE")
    try:
        build_invalid_profile()
    except ValidationError as exc:
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
