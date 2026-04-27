#!/usr/bin/env python3
"""Sample pipeline: reads a CSV from /data/input, counts rows, writes summary to /data/output."""
import csv
import json
import pathlib

def main():
    input_path = pathlib.Path("/data/input/records.csv")
    output_path = pathlib.Path("/data/output/summary.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print("No input file - generating synthetic data")
        records = [{"id": i, "value": i * 1.5} for i in range(1000)]
        input_path.parent.mkdir(parents=True, exist_ok=True)
        with open(input_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "value"])
            writer.writeheader()
            writer.writerows(records)

    with open(input_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    summary = {"row_count": len(rows), "source": str(input_path)}
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Processed {len(rows):,} rows -> {output_path}")

if __name__ == "__main__":
    main()
