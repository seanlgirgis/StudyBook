# ============================================================
# Topic   : Python Concurrency for Data Engineers
# File    : pipeline.py
# Covers  : capstone concurrent IoT ingestion pipeline
# Prereqs : pip install aiohttp aiofiles pyarrow pandas
# Run     : python pipeline.py
# ============================================================

from __future__ import annotations

import datetime as dt
import functools
import logging
import os
import random
import threading
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from simulate_sources import ENDPOINTS, RANGES, fetch_sensor


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def default_output_dir() -> Path:
    """Return platform-appropriate default output dir."""
    if os.name == "nt":
        return Path("C:/tmp/studybook/concurrency")
    return Path("/tmp/studybook/concurrency")


OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", str(default_output_dir())))


class TokenBucketRateLimiter:
    """
    Thread-safe token bucket rate limiter.

    Token bucket: tokens accumulate at max_rps/sec up to a burst cap.
    Each request consumes one token. If empty, block until refilled.
    This allows short bursts while enforcing average rate.
    """

    def __init__(self, max_rps: float):
        if max_rps <= 0:
            raise ValueError("max_rps must be > 0")

        self.max_rps = max_rps
        self.tokens = 0.0
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.max_rps, self.tokens + elapsed * self.max_rps)
        self.last_refill = now

    def acquire(self) -> None:
        while True:
            with self.lock:
                self._refill()

                if self.tokens >= 1.0:
                    self.tokens -= 1.0
                    return

                missing_tokens = 1.0 - self.tokens
                sleep_s = missing_tokens / self.max_rps

            time.sleep(sleep_s)


def retry_with_jitter(max_attempts: int = 3, base_delay_s: float = 0.5):
    """
    Decorator factory.

    Retries the decorated function up to max_attempts times.
    Delay uses exponential backoff plus jitter:
      base_delay_s * (2 ** attempt) + random.uniform(0, 0.5)
    """

    if max_attempts <= 0:
        raise ValueError("max_attempts must be > 0")

    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    if attempt == max_attempts:
                        raise

                    delay_s = base_delay_s * (2 ** (attempt - 1)) + random.uniform(0, 0.5)
                    log.info(
                        "Attempt %s/%s failed: %s. Retrying in %.2fs...",
                        attempt,
                        max_attempts,
                        exc,
                        delay_s,
                    )
                    time.sleep(delay_s)

            raise RuntimeError("unreachable retry state")

        return wrapper

    return decorator


ANOMALY_THRESHOLDS = {
    "temperature": 85.0,
    "pressure": 8.5,
    "vibration": 42.0,
    "humidity": 88.0,
}


def enrich_record(record: dict) -> dict:
    """
    Module-level CPU enrichment function (picklable).
    - Compute normalised_value (0.0–1.0)
    - Set anomaly_flag (bool) based on ANOMALY_THRESHOLDS
    - Add processed_at (ISO timestamp)
    - Add pipeline_run_id (passed in via record["_run_id"])
    Return enriched record (remove _run_id before return).
    """
    sensor_type = record["sensor_type"]
    min_value, max_value = RANGES[sensor_type]
    value = float(record["value"])

    normalised_value = (value - min_value) / (max_value - min_value)
    anomaly_flag = value > ANOMALY_THRESHOLDS[sensor_type]
    run_id = record["_run_id"]

    enriched = {
        "endpoint_id": record["endpoint_id"],
        "plant": record["plant"],
        "sensor_type": sensor_type,
        "value": value,
        "unit": record["unit"],
        "normalised_value": normalised_value,
        "anomaly_flag": anomaly_flag,
        "ts": record["ts"],
        "latency_ms": float(record["latency_ms"]),
        "processed_at": dt.datetime.now(dt.UTC).isoformat(),
        "pipeline_run_id": run_id,
    }

    return enriched


def stage1_fetch(
    endpoints: list[dict],
    max_rps: float = 20.0,
    max_workers: int = 20,
) -> tuple[list[dict], list[dict]]:
    """
    ThreadPoolExecutor + TokenBucketRateLimiter.
    Wrap fetch_sensor with @retry_with_jitter(max_attempts=3).
    Return (successful_records, failed_endpoints).
    Log each failure: log.warning("FETCH FAILED: %s — %s", ep["id"], str(e))
    """
    limiter = TokenBucketRateLimiter(max_rps=max_rps)
    successful_records: list[dict] = []
    failed_endpoints: list[dict] = []

    @retry_with_jitter(max_attempts=3, base_delay_s=0.2)
    def fetch_with_retry(endpoint: dict) -> dict:
        limiter.acquire()
        return fetch_sensor(endpoint)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(fetch_with_retry, endpoint): endpoint
            for endpoint in endpoints
        }

        for future in as_completed(futures):
            endpoint = futures[future]

            try:
                record = future.result()
                successful_records.append(record)
                log.info(
                    "FETCH OK: %s latency=%.0fms",
                    record["endpoint_id"],
                    record["latency_ms"],
                )
            except Exception as exc:
                failed_endpoints.append(endpoint)
                log.warning("FETCH FAILED: %s — %s", endpoint["id"], str(exc))

    return successful_records, failed_endpoints


def stage2_enrich(
    records: list[dict],
    run_id: str,
    n_workers: int = None,
) -> list[dict]:
    """
    ProcessPoolExecutor — apply enrich_record to all records.
    Inject run_id into each record as "_run_id" before sending to pool.
    Return enriched records list.
    """
    if not records:
        return []

    if n_workers is None:
        n_workers = os.cpu_count() or 1

    records_with_run_id = [
        {**record, "_run_id": run_id}
        for record in records
    ]

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        return list(executor.map(enrich_record, records_with_run_id))


PARQUET_SCHEMA = pa.schema(
    [
        ("endpoint_id", pa.string()),
        ("plant", pa.string()),
        ("sensor_type", pa.string()),
        ("value", pa.float64()),
        ("unit", pa.string()),
        ("normalised_value", pa.float64()),
        ("anomaly_flag", pa.bool_()),
        ("ts", pa.string()),
        ("latency_ms", pa.float64()),
        ("processed_at", pa.string()),
        ("pipeline_run_id", pa.string()),
    ]
)


def stage3_write(records: list[dict], output_path: Path) -> None:
    """
    Convert records list to pyarrow Table using PARQUET_SCHEMA.
    Write as SNAPPY Parquet to output_path.
    Print: "Written {len(records)} records to {output_path}"
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(records)

    for field in PARQUET_SCHEMA:
        if field.name not in df.columns:
            df[field.name] = None

    df = df[[field.name for field in PARQUET_SCHEMA]]
    table = pa.Table.from_pandas(df, schema=PARQUET_SCHEMA, preserve_index=False)

    pq.write_table(table, output_path, compression="snappy")
    print(f"Written {len(records)} records to {output_path}")


def run_pipeline(max_rps: float = 20.0) -> dict:
    """
    Orchestrate all 3 stages. Measure wall-clock time for each stage and total.
    Return:
      { run_id: str, total_endpoints: int, fetched_ok: int, fetch_errors: int,
        records_written: int, anomalies: int,
        stage1_ms: float, stage2_ms: float, stage3_ms: float, total_ms: float,
        throughput_rec_per_s: float }
    """
    run_id = str(uuid.uuid4())
    output_path = OUTPUT_DIR / "capstone" / "results.parquet"

    total_start = time.perf_counter()

    stage1_start = time.perf_counter()
    fetched_records, failed_endpoints = stage1_fetch(
        ENDPOINTS,
        max_rps=max_rps,
        max_workers=20,
    )
    stage1_ms = (time.perf_counter() - stage1_start) * 1000

    stage2_start = time.perf_counter()
    enriched_records = stage2_enrich(fetched_records, run_id=run_id)
    stage2_ms = (time.perf_counter() - stage2_start) * 1000

    stage3_start = time.perf_counter()
    stage3_write(enriched_records, output_path)
    stage3_ms = (time.perf_counter() - stage3_start) * 1000

    total_ms = (time.perf_counter() - total_start) * 1000
    total_s = total_ms / 1000
    records_written = len(enriched_records)

    return {
        "run_id": run_id,
        "total_endpoints": len(ENDPOINTS),
        "fetched_ok": len(fetched_records),
        "fetch_errors": len(failed_endpoints),
        "records_written": records_written,
        "anomalies": sum(1 for r in enriched_records if r["anomaly_flag"]),
        "stage1_ms": stage1_ms,
        "stage2_ms": stage2_ms,
        "stage3_ms": stage3_ms,
        "total_ms": total_ms,
        "throughput_rec_per_s": records_written / total_s if total_s > 0 else 0.0,
    }


def print_summary(stats: dict) -> None:
    """
    Print the formatted box summary shown in the module docstring.
    """
    total_s = stats["total_ms"] / 1000

    print("╔══════════════════════════════════════╗")
    print("║  IoT Pipeline Run — Summary          ║")
    print("╠══════════════════════════════════════╣")
    print(f"║  Total endpoints      : {stats['total_endpoints']:<12} ║")
    print(f"║  Fetched OK           : {stats['fetched_ok']:<12} ║")
    print(f"║  Fetch errors         : {stats['fetch_errors']:<12} ║")
    print(f"║  Records written      : {stats['records_written']:<12} ║")
    print(f"║  Anomalies flagged    : {stats['anomalies']:<12} ║")
    print(f"║  Total time           : {total_s:<8.2f} s   ║")
    print(f"║  Throughput           : {stats['throughput_rec_per_s']:<8.1f} rec/s║")
    print("╚══════════════════════════════════════╝")


def main() -> None:
    stats = run_pipeline(max_rps=20.0)
    print_summary(stats)


if __name__ == "__main__":
    main()