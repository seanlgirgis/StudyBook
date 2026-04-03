"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-00 · Prerequisite Check                                           ║
║  Verify Python, PySpark, Kafka, and Java before running any nugget.          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Checks everything you need is in place:
  1. Python version (≥ 3.8)
  2. Required packages (pyspark, kafka-python, requests)
  3. Java / JAVA_HOME (required by PySpark)
  4. Spark session creation
  5. Kafka broker reachability

USAGE
─────
    python 00_prereq_check.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _spark_stream_connect import check_kafka_broker, KAFKA_BOOTSTRAP

print("\n── Spark Structured Streaming Prerequisite Check ───")

# 1. Python version
py_ok = sys.version_info >= (3, 8)
status = "✓" if py_ok else "✗"
print(f"\n  [{status}] Python {sys.version.split()[0]}  (requires ≥ 3.8)")

# 2. Package checks
for pkg_name, import_name in [
    ("pyspark", "pyspark"),
    ("kafka-python", "kafka"),
    ("requests", "requests"),
]:
    try:
        mod = __import__(import_name.replace("-", "_"))
        version = getattr(mod, "__version__", "unknown")
        print(f"  [✓] {pkg_name} {version}")
    except ImportError:
        print(f"  [✗] {pkg_name} — NOT INSTALLED")
        print(f"      Fix: pip install {pkg_name}")
        sys.exit(1)

# 3. Java check
java_home = os.getenv("JAVA_HOME")
if java_home:
    print(f"\n  [✓] JAVA_HOME = {java_home}")
else:
    # PySpark can find Java on its own sometimes
    print(f"\n  [!] JAVA_HOME not set (PySpark may auto-detect)")

# 4. Spark session creation
print("\n  Testing Spark session...")
try:
    from _spark_stream_connect import get_spark, ensure_lab_dirs
    ensure_lab_dirs()
    spark = get_spark("prereq-check")
    version = spark.version
    print(f"  [✓] Spark {version}")
    spark.stop()
except Exception as e:
    print(f"  [✗] Spark session failed: {e}")
    print("\n  Common causes:")
    print("    - Java not installed → install JDK 11 or 17")
    print("    - JAVA_HOME not set → setx JAVA_HOME 'C:\\path\\to\\jdk'")
    sys.exit(1)

# 5. Kafka broker check
print("\n  Testing Kafka broker...")
if check_kafka_broker():
    print(f"  [✓] Kafka reachable at {KAFKA_BOOTSTRAP}")
else:
    print(f"  [✗] Kafka NOT reachable at {KAFKA_BOOTSTRAP}")
    print("\n  Fix: start Docker services:")
    print("    pwsh D:\\StudyBook\\_infra\\scripts\\infra_up.ps1 -Group streaming")
    print("    pwsh D:\\StudyBook\\_infra\\scripts\\infra_up.ps1 -Group pipeline")

print("\n  All prerequisites met. Ready to run nuggets!")
print()
