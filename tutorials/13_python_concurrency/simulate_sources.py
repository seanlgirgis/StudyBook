# ============================================================
# Topic   : Python Concurrency for Data Engineers
# File    : simulate_sources.py
# Covers  : simulated IoT sensor endpoints for capstone pipeline
# Prereqs : pip install aiohttp aiofiles pyarrow pandas
# Run     : python simulate_sources.py
# ============================================================

from __future__ import annotations

import datetime as dt
import random
import time


PLANTS = ["plant_A", "plant_B", "plant_C"]
SENSORS = ["temperature", "pressure", "vibration", "humidity"]

RANGES = {
    "temperature": (15.0, 95.0),
    "pressure": (1.0, 10.0),
    "vibration": (0.0, 50.0),
    "humidity": (20.0, 100.0),
}

UNITS = {
    "temperature": "C",
    "pressure": "bar",
    "vibration": "mm/s",
    "humidity": "%",
}


ENDPOINTS: list[dict] = [
    {
        "id": f"sensor_{i:03d}",
        "plant": PLANTS[i % len(PLANTS)],
        "sensor_type": SENSORS[i % len(SENSORS)],
        "base_value": random.uniform(*RANGES[SENSORS[i % len(SENSORS)]]),
    }
    for i in range(50)
]


def fetch_sensor(endpoint: dict, seed: int = None) -> dict:
    """
    Simulate fetching one sensor reading:
      - Sleep random 0.1–2.0s (network latency)
      - 10% chance: raise ConnectionError("Simulated network failure")
      - Return:
          { endpoint_id: str, plant: str, sensor_type: str,
            value: float (base_value + gaussian noise σ=2),
            unit: str, ts: str (ISO 8601),
            latency_ms: float }
    seed parameter sets random seed for reproducibility in tests.
    """
    rng = random.Random(seed) if seed is not None else random

    start = time.perf_counter()
    time.sleep(rng.uniform(0.1, 2.0))

    if rng.random() < 0.10:
        raise ConnectionError("Simulated network failure")

    sensor_type = endpoint["sensor_type"]
    value = float(endpoint["base_value"] + rng.gauss(0.0, 2.0))
    latency_ms = (time.perf_counter() - start) * 1000

    return {
        "endpoint_id": endpoint["id"],
        "plant": endpoint["plant"],
        "sensor_type": sensor_type,
        "value": value,
        "unit": UNITS[sensor_type],
        "ts": dt.datetime.now(dt.UTC).isoformat(),
        "latency_ms": latency_ms,
    }


def fetch_all_sequential() -> list[dict]:
    """Fetch all 50 endpoints one at a time. For benchmarking baseline."""
    results = []

    for endpoint in ENDPOINTS:
        try:
            results.append(fetch_sensor(endpoint))
        except ConnectionError as exc:
            print(f"FETCH FAILED: {endpoint['id']} — {exc}")

    return results


def main() -> None:
    print("\n=== SIMULATED IOT SOURCES ===")
    print(f"Total endpoints: {len(ENDPOINTS)}")

    start = time.perf_counter()
    results = fetch_all_sequential()
    elapsed = time.perf_counter() - start

    print(f"Fetched OK : {len(results)}")
    print(f"Errors     : {len(ENDPOINTS) - len(results)}")
    print(f"Total time : {elapsed:.2f}s")


if __name__ == "__main__":
    main()