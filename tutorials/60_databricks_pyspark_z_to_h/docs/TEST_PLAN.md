# Test Plan

## Validation Gate 1 (Local Only)

### Script Checks
- Python active
- Java active
- JAVA_HOME present
- `pyspark` import
- `pytest` import
- SparkSession local[*] smoke (if PySpark is available)

### Execution Targets
- `scripts/check_wsl_env.sh`
- `scripts/check_windows_env.ps1`
- `src/00_environment_smoke_test.py`
- `python -m pytest -q -o cache_dir=/home/shareuser/.cache/pytest/60_databricks_pyspark_z_to_h` (WSL)
- `python -m pytest -q` (Windows PowerShell)

## Pass Criteria
- Scripts execute successfully and print status for each required check.
- Spark local smoke succeeds when PySpark is available.
- No cloud dependencies are required.
