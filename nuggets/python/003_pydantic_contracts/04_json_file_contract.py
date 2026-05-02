from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError


class AppConfig(BaseModel):
    app_name: str = Field(min_length=1)
    port: int = Field(ge=1, le=65535)
    debug: bool


SCRIPT_DIR = Path(__file__).resolve().parent


def load_config_from_file(filename: str) -> AppConfig:
    file_path = SCRIPT_DIR / filename
    raw_data = json.loads(file_path.read_text(encoding="utf-8"))
    return AppConfig.model_validate(raw_data)


def main() -> None:
    print("VALID CASE")
    valid_config = load_config_from_file("sample_valid.json")
    print(valid_config)

    print("\nINVALID CASE")
    try:
        load_config_from_file("sample_invalid.json")
    except ValidationError as exc:
        print("ValidationError raised:")
        print(exc)


if __name__ == "__main__":
    main()
