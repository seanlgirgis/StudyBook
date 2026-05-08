# Environment

## Supported Paths
- WSL project: `/mnt/d/Workarea/StudyBook/tutorials/60_databricks_pyspark_z_to_h`
- Windows project: `D:\Workarea\StudyBook\tutorials\60_databricks_pyspark_z_to_h`
- WSL venv: `/home/shareuser/venvs/databricks_pyspark`

## Confirmed WSL Runtime
- Python 3.14.4
- OpenJDK 17.0.18
- JAVA_HOME `/usr/lib/jvm/java-17-openjdk-amd64`
- PySpark 4.1.1
- Spark local[*] smoke PASS

## Notes
- Use StudyBook `env_setter.ps1` for Windows sessions.
- Keep Databricks cloud and AWS out of phase 1.
- For WSL pytest runs on `/mnt/d/...`, use a home-directory cache path to avoid `.pytest_cache` permission warnings:
  `python -m pytest -q -o cache_dir=/home/shareuser/.cache/pytest/60_databricks_pyspark_z_to_h`
