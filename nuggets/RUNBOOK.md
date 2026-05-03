# Nuggets Runbook

## Start environment

```powershell
..\env_setter.ps1
```

## Run a Python script

```powershell
python .\relative\path\to\script.py
```

## Run all tests

```powershell
python -m pytest
```

## Run tests for one nugget

```powershell
python -m pytest .\python\001_environment_check\
```

## Current Nuggets

### 1) Environment check

```powershell
python .\python\001_environment_check\demo.py
python -m pytest .\python\001_environment_check\
```

### 2) Argparse CLI

```powershell
python .\python\002_argparse_cli\demo.py
python .\python\002_argparse_cli\demo.py --name Sean --repeat 3 --uppercase
python -m pytest .\python\002_argparse_cli\
```

### 3) Pydantic contracts

```powershell
pip install -r .\python\003_pydantic_contracts\requirements.txt
python .\python\003_pydantic_contracts\01_basic_model_contract.py
python .\python\003_pydantic_contracts\10_nested_json_file_contract.py
python -m pytest .\python\003_pydantic_contracts\
```

## Add dependencies

Prefer updating a local `requirements.txt` only when needed.

```powershell
pip install package-name
pip freeze > requirements.txt
```

## Rules

- Run commands from the repository root.
- Use relative paths.
- Keep experiments small.
