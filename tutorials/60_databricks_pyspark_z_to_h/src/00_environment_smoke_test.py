"""Local environment smoke test for Databricks + PySpark starter lane."""

from __future__ import annotations

import importlib.util
import os
import platform
import subprocess
import sys


def module_exists(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def cmd_output(command: list[str]) -> str | None:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        out = (result.stdout or "") + (result.stderr or "")
        return out.strip() or None
    except FileNotFoundError:
        return None


print("== StudyBook Databricks + PySpark Local Smoke Test ==")
print(f"Platform: {platform.platform()}")
print(f"Python active: {sys.version.split()[0]}")

java_text = cmd_output(["java", "-version"])
if java_text:
    print("[OK] Java active:")
    print("\n".join(java_text.splitlines()[:2]))
else:
    print("[MISSING] Java active")

java_home = os.environ.get("JAVA_HOME")
print(f"[OK] JAVA_HOME={java_home}" if java_home else "[MISSING] JAVA_HOME")
print("[OK] pyspark import" if module_exists("pyspark") else "[MISSING] pyspark import")
print("[OK] pytest import" if module_exists("pytest") else "[MISSING] pytest import")

if not module_exists("pyspark"):
    print("[SKIP] SparkSession local[*] smoke test: pyspark missing")
else:
    try:
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.master("local[*]").appName("sb-smoke-script").getOrCreate()
        print(f"[OK] SparkSession local[*] smoke PASS: Spark {spark.version}")
        spark.stop()
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] SparkSession local[*] smoke test: {exc}")
