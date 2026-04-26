# Tutorials Quick Reference
Last updated: 2026-04-26

## Key Paths

- Repo root: `D:\Workarea\StudyBook`
- Tutorials root: `D:\Workarea\StudyBook\tutorials`
- Manager docs: `D:\Workarea\StudyBook\tutorials\_manager`
- Canonical local PySpark track: `D:\Workarea\StudyBook\tutorials\02_pyspark`
- Docker PySpark variant: `D:\Workarea\StudyBook\tutorials\02_PySpark_Docker`

## First Command For New Session

```powershell
cd D:\Workarea\StudyBook
.\env_setter.ps1 -NonInteractive
```

## Current Status Buckets

- User-reported working: `01, 02, 02_PySpark_Docker, 08, 09, 10, 12, 13, 14`
- READY_TO_PASTE only: `03, 04, 05, 06, 07, 11, 24, 26, 27, 33, 36`
- Not started: `15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 28, 29, 30, 31, 32, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47`

## Useful Commands

### Inventory scan

```powershell
cd D:\Workarea\StudyBook\tutorials
Get-ChildItem -Directory | Sort-Object Name
```

### Quick prompt/test file checks

```powershell
cd D:\Workarea\StudyBook\tutorials
Get-ChildItem -Recurse -File -Filter prompt_READY_TO_PASTE.md
Get-ChildItem -Recurse -File -Filter test_*.py
```

### Topic-level test commands (when you want independent verification)

```powershell
cd D:\Workarea\StudyBook\tutorials
pytest 01_aws_kinesis\capstone\test_capstone.py -v
pytest 08_aws_s3\capstone\test_capstone.py -v
pytest 09_aws_cloudwatch\capstone\test_capstone.py -v
pytest 10_python_logging\capstone\test_pipeline_logger.py -v
pytest 12_parquet\test_capstone.py -v
pytest 13_python_concurrency\test_capstone.py -v
pytest 14_encryption\capstone\test_encryption.py -v
```

### PySpark track distinction

```powershell
# Canonical local mode track
cd D:\Workarea\StudyBook\tutorials\02_pyspark

# Docker/Spark-cluster variant track
cd D:\Workarea\StudyBook\tutorials\02_PySpark_Docker
```

## Notes

- Do not collapse the two PySpark folders into one.
- Label outcomes as `user-reported working` unless this session includes direct run evidence.
