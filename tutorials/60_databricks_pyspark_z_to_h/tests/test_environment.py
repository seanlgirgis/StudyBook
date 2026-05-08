"""Phase-1 environment tests (local-only)."""

from __future__ import annotations

import importlib.util
import os


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def test_python_probe_runs() -> None:
    assert True


def test_java_home_field_exists_or_missing_cleanly() -> None:
    java_home = os.environ.get("JAVA_HOME")
    assert java_home is None or isinstance(java_home, str)


def test_import_probes_run() -> None:
    assert isinstance(has_module("pyspark"), bool)
    assert isinstance(has_module("pytest"), bool)


def test_spark_local_smoke_when_pyspark_available() -> None:
    if not has_module("pyspark"):
        return

    from pyspark.sql import SparkSession

    spark = SparkSession.builder.master("local[*]").appName("sb-test-smoke").getOrCreate()
    try:
        assert isinstance(spark.version, str) and len(spark.version) > 0
    finally:
        spark.stop()
