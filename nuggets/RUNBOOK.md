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
python -m pytest .\python\001_example\
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
