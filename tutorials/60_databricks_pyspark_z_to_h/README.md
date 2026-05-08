# Databricks + PySpark Zero to Hero (Design-First Starter)

This lane is the starter foundation for learning Databricks + PySpark from zero to hero.

## Current Scope (Phase 1)
- Design-first project docs
- Local environment checks (WSL + Windows)
- Local PySpark smoke testing only
- No package installation automation

## Out of Scope (Phase 1)
- Databricks cloud execution
- AWS resource setup
- Paid cloud resources
- Full lesson implementations

## Known Paths
- Windows: `D:\Workarea\StudyBook\tutorials\60_databricks_pyspark_z_to_h`
- WSL project path: `/mnt/d/Workarea/StudyBook/tutorials/60_databricks_pyspark_z_to_h`
- WSL venv path: `/home/shareuser/venvs/databricks_pyspark`

## Confirmed Environment Baseline
- Python: 3.14.4
- Java: OpenJDK 17.0.18
- JAVA_HOME: `/usr/lib/jvm/java-17-openjdk-amd64`
- PySpark: 4.1.1
- Spark local smoke: PASS (Spark 4.1.1)

## First Validation Gate Checks
- Python active
- Java active
- JAVA_HOME present
- `pyspark` import
- `pytest` import
- `SparkSession` local[*] smoke test

## Quick Start (WSL)
```bash
cd /mnt/d/Workarea/StudyBook/tutorials/60_databricks_pyspark_z_to_h
chmod +x activate_wsl.sh scripts/check_wsl_env.sh
./activate_wsl.sh
./scripts/check_wsl_env.sh
python3 src/00_environment_smoke_test.py
python3 -m pytest -q -o cache_dir=/home/shareuser/.cache/pytest/60_databricks_pyspark_z_to_h
```

## Quick Start (Windows PowerShell)
```powershell
cd D:\Workarea\StudyBook
.\env_setter.ps1
cd .\tutorials\60_databricks_pyspark_z_to_h
.\scripts\check_windows_env.ps1
python .\src\00_environment_smoke_test.py
python -m pytest -q
```
