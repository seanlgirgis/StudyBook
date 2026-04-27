# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : capstone/generate_logs.py
# Covers  : Generate synthetic web logs and upload raw CSV to S3
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket
# Run     : python capstone/generate_logs.py
# ============================================================

from __future__ import annotations

import csv
import os
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import boto3


# Environment variables used by this file:
# - AWS_REGION: AWS region for S3 access.
# - AWS_PROFILE: Optional named AWS CLI profile.
# - EMR_S3_BUCKET: Existing S3 bucket where raw logs will be uploaded.
# - EMR_SUBNET_ID: Required by tutorial standard; not used by this generator.
#
# Cost note:
# This file uploads data to S3. S3 storage and requests have small costs.
# Keep data under raw/weblogs/ so capstone/cleanup.py can remove it safely.

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_PROFILE = os.environ.get("AWS_PROFILE")
EMR_S3_BUCKET = os.environ.get("EMR_S3_BUCKET")
EMR_SUBNET_ID = os.environ.get("EMR_SUBNET_ID")

N_RECORDS = 1_000_000
ENDPOINTS = [
    "/api/users",
    "/api/orders",
    "/api/products",
    "/health",
    "/api/payments",
    "/api/reports",
    "/api/auth/login",
    "/api/auth/logout",
]
STATUS_CODES = [200] * 70 + [201] * 10 + [400] * 8 + [404] * 5 + [500] * 5 + [503] * 2

METHODS = ["GET"] * 60 + ["POST"] * 25 + ["PUT"] * 10 + ["DELETE"] * 5
USER_AGENTS = [
    "Mozilla/5.0 Chrome/120.0",
    "Mozilla/5.0 Safari/17.0",
    "Mozilla/5.0 Firefox/121.0",
    "curl/8.0",
    "PostmanRuntime/7.36",
    "StudyBookSyntheticClient/1.0",
]


def get_boto3_session() -> boto3.session.Session:
    if AWS_PROFILE:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return boto3.Session(region_name=AWS_REGION)


def get_s3_client() -> Any:
    return get_boto3_session().client("s3")


def generate_ip_address() -> str:
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def generate_log_record(ts: datetime) -> dict:
    """
    Return dict with keys:
      timestamp (ISO 8601), endpoint, method (GET/POST/PUT/DELETE weighted),
      status_code, response_time_ms (50-2000, higher for 5xx),
      bytes_sent (100-50000), user_agent, ip_address
    """
    status_code = random.choice(STATUS_CODES)

    if status_code >= 500:
        response_time_ms = random.randint(600, 2000)
    elif status_code >= 400:
        response_time_ms = random.randint(80, 900)
    else:
        response_time_ms = random.randint(50, 500)

    return {
        "timestamp": ts.isoformat(),
        "endpoint": random.choice(ENDPOINTS),
        "method": random.choice(METHODS),
        "status_code": status_code,
        "response_time_ms": response_time_ms,
        "bytes_sent": random.randint(100, 50_000),
        "user_agent": random.choice(USER_AGENTS),
        "ip_address": generate_ip_address(),
    }


def generate_log_batch(n: int = N_RECORDS) -> list[dict]:
    """Generate n records spread across 7 days ending today."""
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=7)
    total_seconds = int((end_time - start_time).total_seconds())

    records: list[dict] = []

    for _ in range(n):
        offset_seconds = random.randint(0, total_seconds)
        ts = start_time + timedelta(seconds=offset_seconds)
        records.append(generate_log_record(ts))

    return records


def save_to_csv(records: list[dict], path: str) -> None:
    """Write records to CSV using csv.DictWriter."""
    if not records:
        raise ValueError("records must not be empty")

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "timestamp",
        "endpoint",
        "method",
        "status_code",
        "response_time_ms",
        "bytes_sent",
        "user_agent",
        "ip_address",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def upload_to_s3(local_path: str, bucket: str, key: str) -> str:
    """Upload file to S3. Return s3:// URI. Print progress."""
    s3 = get_s3_client()

    print(f"Uploading {local_path} to s3://{bucket}/{key}")
    s3.upload_file(local_path, bucket, key)

    uri = f"s3://{bucket}/{key}"
    print(f"Upload complete: {uri}")
    return uri


def main() -> None:
    """Generate logs, save, upload. Print record count and S3 location."""
    local_path = Path("capstone") / "data" / "weblogs.csv"

    try:
        print("Generating synthetic web logs")
        print("=" * 72)
        print(f"Record count: {N_RECORDS:,}")

        records = generate_log_batch(N_RECORDS)
        save_to_csv(records, str(local_path))

        print(f"Saved local CSV: {local_path}")
        print(f"Local file size MB: {local_path.stat().st_size / 1024 / 1024:.2f}")

        if not EMR_S3_BUCKET:
            print("\nSet EMR_S3_BUCKET to upload logs to S3.")
            print("No S3 upload was performed, so no AWS resources were modified.")
            return

        s3_uri = upload_to_s3(
            local_path=str(local_path),
            bucket=EMR_S3_BUCKET,
            key="raw/weblogs/weblogs.csv",
        )

        print("\nGeneration Summary")
        print("=" * 72)
        print(f"Records generated: {len(records):,}")
        print(f"S3 location      : {s3_uri}")
        print("⚠️  COST WARNING: Raw log data is now stored in S3 and may accrue storage charges.")
    finally:
        print("Generator finished. Use capstone/cleanup.py after the capstone to remove S3 data.")


if __name__ == "__main__":
    main()