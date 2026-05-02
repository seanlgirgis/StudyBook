from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType

import pytest
from pydantic import ValidationError


BASE_DIR = Path(__file__).resolve().parent


def load_module(file_name: str, module_name: str) -> ModuleType:
    module_path = BASE_DIR / file_name
    spec = spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_valid_basic_model() -> None:
    mod = load_module("01_basic_model_contract.py", "lesson01")
    user = mod.build_valid_user()
    assert user.id == 1
    assert user.name == "Sean"
    assert user.active is True


def test_invalid_basic_model_raises_validation_error() -> None:
    mod = load_module("01_basic_model_contract.py", "lesson01_invalid")
    with pytest.raises(ValidationError):
        mod.build_invalid_user()


def test_validate_call_rejects_bad_input() -> None:
    mod = load_module("05_function_signature_contract.py", "lesson05")
    with pytest.raises(ValidationError):
        mod.calculate_discount("bad", "data")


def test_model_validator_rejects_invalid_date_range() -> None:
    mod = load_module("07_model_validator_cross_field.py", "lesson07")
    with pytest.raises(ValidationError):
        mod.build_invalid_range()


def test_json_contract_loader_rejects_invalid_file() -> None:
    mod = load_module("04_json_file_contract.py", "lesson04")
    with pytest.raises(ValidationError):
        mod.load_config_from_file("sample_invalid.json")
