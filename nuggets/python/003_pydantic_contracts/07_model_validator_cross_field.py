from datetime import date

from pydantic import BaseModel, ValidationError, model_validator


class DateRange(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_order(self):
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        return self


def build_valid_range() -> DateRange:
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
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
