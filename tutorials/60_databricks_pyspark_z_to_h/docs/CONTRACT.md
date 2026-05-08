# Contract

## Scope Contract
- Build only the starter design-first foundation.
- Keep all checks local and dependency-observational.
- Do not auto-install packages.

## Platform Contract
- Support WSL Ubuntu and Windows PowerShell.
- WSL venv is fixed at `/home/shareuser/venvs/databricks_pyspark`.
- Spark smoke uses `local[*]` only.

## Teaching Contract
- Scripts remain readable for beginners.
- Java is discussed as JVM dependency awareness only.
- Error outputs should guide, not overwhelm.
