# Story:
# This file compares CSV vs Parquet on the same dataset.
# It matters because columnar storage is faster for analytics-style reads.
# Expect Parquet to be smaller and faster on narrow column reads.

from pathlib import Path
import time


def _try_imports():
    try:
        import pandas as pd
        import pyarrow as pa
        import pyarrow.parquet as pq
    except Exception as exc:
        print("Missing pandas/pyarrow. Install to run this demo.")
        print(f"Import error: {exc}")
        return None, None, None
    return pd, pa, pq


def _build_dataset(row_count):
    event_types = ["page_view", "purchase", "signup", "support_ticket"]
    devices = [
        "mobile-android-v2",
        "mobile-ios-v3",
        "desktop-chrome-v120",
        "desktop-firefox-v118",
    ]
    countries = ["United-States", "United-Kingdom", "Germany", "Brazil", "India"]
    payload_base = "x" * 600

    data = {
        "id": list(range(1, row_count + 1)),
        "user_id": [(i % 5000) + 1 for i in range(row_count)],
        "event_type": [event_types[i % len(event_types)] for i in range(row_count)],
        "device": [devices[i % len(devices)] for i in range(row_count)],
        "country": [countries[i % len(countries)] for i in range(row_count)],
        "ts": [
            f"2024-06-{(i % 28) + 1:02d} {(i % 24):02d}:00:00"
            for i in range(row_count)
        ],
        "value": [(i % 1000) * 3 for i in range(row_count)],
        "payload_text": [f"{payload_base}{i % 1000}" for i in range(row_count)],
    }
    return data


def _write_files(df, csv_path, parquet_path):
    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False, engine="pyarrow")


def _measure_read(label, read_fn):
    start = time.perf_counter()
    df = read_fn()
    elapsed = time.perf_counter() - start
    print(f"{label}: {elapsed:.4f}s (rows={len(df)})")


def run_parquet_demo():
    pd, _, pq = _try_imports()
    if pd is None:
        return

    output_dir = Path(__file__).resolve().parent / "_artifacts"
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "events.csv"
    parquet_path = output_dir / "events.parquet"

    row_count = 120000
    data = _build_dataset(row_count)
    df = pd.DataFrame(data)

    print("Writing files...")
    _write_files(df, csv_path, parquet_path)

    csv_size = csv_path.stat().st_size
    parquet_size = parquet_path.stat().st_size
    print(f"CSV size: {csv_size / (1024 * 1024):.2f} MB")
    print(f"Parquet size: {parquet_size / (1024 * 1024):.2f} MB")

    print("Reading full dataset...")
    _measure_read(
        "CSV full read",
        lambda: pd.read_csv(csv_path),
    )
    _measure_read(
        "Parquet full read",
        lambda: pd.read_parquet(parquet_path),
    )

    print("Reading narrow columns...")
    _measure_read(
        "CSV narrow read",
        lambda: pd.read_csv(csv_path, usecols=["user_id", "value"]),
    )
    _measure_read(
        "Parquet narrow read",
        lambda: pd.read_parquet(parquet_path, columns=["user_id", "value"]),
    )

    try:
        schema = pq.ParquetFile(parquet_path).schema
        print("Parquet schema:")
        print(schema)
    except Exception as exc:
        print(f"Could not read parquet schema: {exc}")

    print(
        "Note: Parquet is columnar. CSV is row-ish text. This demo shows the "
        "column benefit on reads, not a full columnar engine."
    )


if __name__ == "__main__":
    run_parquet_demo()

# Takeaway:
# Parquet is smaller and faster for narrow analytics reads than CSV.
