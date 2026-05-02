# Environment Check

## Question

Can this nuggets repository run Python correctly from the repository root using the project environment setup?

## Run

```powershell
cd D:\Workarea\StudyBook\nuggets
..\env_setter.ps1
python .\python\001_environment_check\demo.py
python -m pytest .\python\001_environment_check\
```

## Expected Output

- Python version is printed
- Current working directory is printed
- Script directory is printed
- Output directory path is printed
- Output directory creation is confirmed as `True`
- Pytest reports `1 passed`

## Lesson

How to verify environment setup, path handling, and safe relative-directory creation from a nugget script.
