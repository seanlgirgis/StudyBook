#!/usr/bin/env bash
set -u

# Activate the known WSL virtual environment for this tutorial lane.
# This file does not install anything.

VENV_PATH="/home/shareuser/venvs/databricks_pyspark"

if [ ! -d "$VENV_PATH" ]; then
  echo "[FAIL] Venv path not found: $VENV_PATH"
  return 1 2>/dev/null || exit 1
fi

# shellcheck disable=SC1090
source "$VENV_PATH/bin/activate"

# Keep pytest cache in WSL home to avoid permission warnings on /mnt/d mounts.
export PYTEST_ADDOPTS="-o cache_dir=/home/shareuser/.cache/pytest/60_databricks_pyspark_z_to_h"

echo "[OK] Activated venv: $VENV_PATH"
echo "[OK] Python: $(python3 --version 2>&1)"
echo "[OK] PYTEST_ADDOPTS=$PYTEST_ADDOPTS"
