# Pydantic Contracts

## Purpose

Learn Pydantic v2 as contracts that can fail loudly. Each mini-program has:

- one valid input case
- one invalid input case
- clear printed failure details (`ValidationError`)

## Contract That Can Fail

A Pydantic model is a contract around data shape and rules. Valid input passes and becomes a typed object. Invalid input fails early with explicit error messages, so broken assumptions are caught at boundaries.

## Install

```powershell
cd D:\Workarea\StudyBook\nuggets
..\env_setter.ps1
pip install -r .\python\003_pydantic_contracts\requirements.txt
```

## Run Lessons

```powershell
python .\python\003_pydantic_contracts\01_basic_model_contract.py
python .\python\003_pydantic_contracts\02_field_constraints.py
python .\python\003_pydantic_contracts\03_nested_models.py
python .\python\003_pydantic_contracts\04_json_file_contract.py
python .\python\003_pydantic_contracts\05_function_signature_contract.py
python .\python\003_pydantic_contracts\06_custom_field_validator.py
python .\python\003_pydantic_contracts\07_model_validator_cross_field.py
python .\python\003_pydantic_contracts\08_strict_vs_coercion.py
python .\python\003_pydantic_contracts\09_serialization_dump_schema.py
python .\python\003_pydantic_contracts\10_nested_json_file_contract.py
```

## Supporting Files

- `sample_valid.json` and `sample_invalid.json` for lesson 04
- `sample_order_valid.json` and `sample_order_invalid.json` for lesson 10

## Test

```powershell
python -m pytest .\python\003_pydantic_contracts\
```

## Lesson Table

| File | Focus | Contract Behavior |
|---|---|---|
| `01_basic_model_contract.py` | Basic model fields | Missing/wrong fields fail |
| `02_field_constraints.py` | `Field(...)` rules | Range/pattern constraints fail loudly |
| `03_nested_models.py` | Nested contracts | Error paths show nested locations |
| `04_json_file_contract.py` | JSON file boundary | File payload validated against model |
| `05_function_signature_contract.py` | `@validate_call` | Bad function arguments fail before logic |
| `06_custom_field_validator.py` | `@field_validator` | Field normalization and allowlist enforcement |
| `07_model_validator_cross_field.py` | `@model_validator` | Cross-field rule failures |
| `08_strict_vs_coercion.py` | Coercion vs strict mode | Demonstrates boundary hardening |
| `09_serialization_dump_schema.py` | Dump + schema | Validate and document contract |
| `10_nested_json_file_contract.py` | Nested JSON file boundary | Validates complex nested payloads and exposes precise nested error paths |

## Lesson 10 Connection

Lesson 10 combines four earlier ideas into one realistic boundary check:

- JSON file loading
- nested models
- `Field(...)` constraints
- nested `ValidationError` paths

## Suggested Study Order

Recommended path:

1. `01_basic_model_contract.py`
2. `02_field_constraints.py`
3. `03_nested_models.py`
4. `04_json_file_contract.py`
5. `10_nested_json_file_contract.py` (integration checkpoint)
6. `05_function_signature_contract.py`
7. `06_custom_field_validator.py`
8. `07_model_validator_cross_field.py`
9. `08_strict_vs_coercion.py`
10. `09_serialization_dump_schema.py`

Capstone-style alternative:

- Study lessons `01` through `09` first, then run `10` last as an end-to-end example.
