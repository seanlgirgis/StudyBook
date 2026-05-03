from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError


# BaseModel turns this class into a Pydantic validation contract.
class AppConfig(BaseModel):
    # Field adds value rules beyond the basic type hint.
    app_name: str = Field(min_length=1)
    port: int = Field(ge=1, le=65535)
    debug: bool


# Resolve paths from this script so file loading stays local and predictable.
SCRIPT_DIR = Path(__file__).resolve().parent


def load_config_from_file(filename: str) -> AppConfig:
    file_path = SCRIPT_DIR / filename
    raw_data = json.loads(file_path.read_text(encoding="utf-8"))
    # model_validate builds the model if valid, or raises ValidationError if invalid.
    return AppConfig.model_validate(raw_data)


def main() -> None:
    print("VALID CASE")
    valid_config = load_config_from_file("sample_valid.json")
    print(valid_config)

    print("\nINVALID CASE")
    try:
        load_config_from_file("sample_invalid.json")
    except ValidationError as exc:
        # Invalid input raises ValidationError, so we catch it to show the failure clearly.
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
