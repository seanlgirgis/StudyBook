#!/usr/bin/env bash
set -u

# Beginner-friendly WSL environment checker.
# Reports what exists and what is missing without installing anything.

echo "== Databricks + PySpark Zero-to-Hero: WSL Environment Check =="
echo "Working directory: $(pwd)"
echo

if command -v python3 >/dev/null 2>&1; then
  echo "[OK] Python active: $(python3 --version 2>&1)"
else
  echo "[MISSING] Python active: python3 command not found"
fi

if command -v java >/dev/null 2>&1; then
  echo "[OK] Java active:"
  java -version 2>&1 | head -n 2
else
  echo "[MISSING] Java active: java command not found"
fi

if [ -n "${JAVA_HOME:-}" ]; then
  echo "[OK] JAVA_HOME=$JAVA_HOME"
else
  echo "[MISSING] JAVA_HOME is not set"
fi

echo
python3 - <<'PY'
import importlib.util

def mod(name: str) -> bool:
    return importlib.util.find_spec(name) is not None

print("[OK] pyspark import" if mod("pyspark") else "[MISSING] pyspark import")
print("[OK] pytest import" if mod("pytest") else "[MISSING] pytest import")

if not mod("pyspark"):
    print("[SKIP] SparkSession local[*] smoke test: pyspark missing")
else:
    try:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.master("local[*]").appName("sb-wsl-smoke").getOrCreate()
        print(f"[OK] SparkSession local[*] smoke PASS: Spark {spark.version}")
        spark.stop()
    except Exception as exc:
        print(f"[FAIL] SparkSession local[*] smoke test: {exc}")
PY
