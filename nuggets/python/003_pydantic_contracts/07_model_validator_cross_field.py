from datetime import date

from pydantic import BaseModel, ValidationError, model_validator


# BaseModel turns this class into a Pydantic validation contract.
class DateRange(BaseModel):
    start_date: date
    end_date: date

    # mode="after" runs after fields are parsed into their Python types.
    @model_validator(mode="after")
    def validate_order(self):
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        return self


def build_valid_range() -> DateRange:
    # model_validate builds the model if valid, or raises ValidationError if invalid.
    return DateRange.model_validate({"start_date": "2026-01-01", "end_date": "2026-01-31"})


def build_invalid_range() -> DateRange:
    return DateRange.model_validate({"start_date": "2026-02-01", "end_date": "2026-01-31"})


def main() -> None:
    print("VALID CASE")
    print(build_valid_range())

    print("\nINVALID CASE")
    try:
        build_invalid_range()
    except ValidationError as exc:
        # Invalid input raises ValidationError, so we catch it to show the failure clearly.
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
