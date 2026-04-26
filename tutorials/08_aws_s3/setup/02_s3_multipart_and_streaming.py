# ============================================================
# Topic   : AWS S3 for Data Engineers
# File    : 02_s3_multipart_and_streaming.py
# Covers  : Large file uploads/downloads — multipart, streaming, transfer acceleration
# Prereqs : pip install boto3 | AWS credentials | S3 bucket
# Run     : python 02_s3_multipart_and_streaming.py
# ============================================================

import math
import os
from pathlib import Path

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def get_s3_client():
    """
    Create an S3 client without hardcoding credentials.

    WHY:
    Real pipeline code should rely on the AWS credential chain:
    environment vars, AWS profile, SSO, EC2 role, ECS task role, or Lambda role.
    """
    if AWS_PROFILE:
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    else:
        session = boto3.Session(region_name=AWS_REGION)

    return session.client("s3")


def generate_synthetic_large_file(path, size_mb):
    """
    Create a synthetic file for multipart upload testing.

    WHY:
    Multipart upload only matters for larger files. This creates repeatable local
    test data without needing a real production extract.

    COST NOTE:
    Uploading test files to S3 creates PUT request charges and storage charges.
    Always delete tutorial objects when done.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    chunk = (
        "endpoint_id,metric_name,value,timestamp\n"
        "endpoint-001,cpu_usage,42.5,2026-04-25T12:00:00Z\n"
    ).encode("utf-8")

    target_bytes = size_mb * 1024 * 1024
    written = 0

    with path.open("wb") as f:
        while written < target_bytes:
            remaining = target_bytes - written
            data = chunk[:remaining] if remaining < len(chunk) else chunk
            f.write(data)
            written += len(data)

    print(f"Generated file: {path} ({size_mb} MB)")


def calculate_multipart_cost(file_size_gb, part_size_mb):
    """
    Estimate multipart part count.

    WHY:
    S3 multipart upload requires:
    - minimum 5 MB per part, except the final part
    - maximum 10,000 parts per upload

    COST NOTE:
    Each part upload is an API request. Too-small parts increase request count.
    Too-large parts reduce parallelism and retry efficiency.
    """
    file_size_mb = file_size_gb * 1024
    part_count = math.ceil(file_size_mb / part_size_mb)

    return {
        "file_size_gb": file_size_gb,
        "part_size_mb": part_size_mb,
        "estimated_part_count": part_count,
        "within_s3_limit": part_count <= 10_000,
        "note": "S3 allows up to 10,000 parts per multipart upload.",
    }


def upload_large_file(bucket, key, local_path, part_size_mb=100):
    """
    Upload a file using manual multipart upload.

    WHY:
    Manual multipart teaches the mechanics:
    initiate upload -> upload parts -> complete upload.

    GOTCHA:
    If multipart upload fails, you must abort it. Otherwise incomplete parts may
    remain and create storage cost until lifecycle cleanup removes them.
    """
    s3 = get_s3_client()
    local_path = Path(local_path)
    part_size = part_size_mb * 1024 * 1024

    response = s3.create_multipart_upload(Bucket=bucket, Key=key)
    upload_id = response["UploadId"]

    parts = []

    try:
        with local_path.open("rb") as f:
            part_number = 1

            while True:
                data = f.read(part_size)

                if not data:
                    break

                part = s3.upload_part(
                    Bucket=bucket,
                    Key=key,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=data,
                )

                parts.append(
                    {
                        "PartNumber": part_number,
                        "ETag": part["ETag"],
                    }
                )

                print(f"Uploaded part {part_number}")
                part_number += 1

        s3.complete_multipart_upload(
            Bucket=bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )

        print(f"Completed multipart upload: s3://{bucket}/{key}")

    except Exception:
        s3.abort_multipart_upload(
            Bucket=bucket,
            Key=key,
            UploadId=upload_id,
        )
        print(f"Aborted multipart upload: s3://{bucket}/{key}")
        raise


def upload_with_transfer_config(bucket, key, local_path):
    """
    Upload using boto3 TransferConfig.

    WHY:
    This is the production-friendly approach for most DE pipelines.
    boto3 handles multipart threshold, part sizing, retries, and concurrency.

    GOTCHA:
    Multipart ETags are not simple MD5 hashes. Use explicit checksums if your
    pipeline requires strong file integrity validation.
    """
    s3 = get_s3_client()

    config = TransferConfig(
        multipart_threshold=100 * 1024 * 1024,
        multipart_chunksize=100 * 1024 * 1024,
        max_concurrency=4,
        use_threads=True,
    )

    s3.upload_file(
        Filename=str(local_path),
        Bucket=bucket,
        Key=key,
        Config=config,
    )

    print(f"Uploaded with TransferConfig: s3://{bucket}/{key}")


def stream_object_lines(bucket, key, max_lines=None):
    """
    Stream an S3 object line-by-line without downloading the full object.

    WHY:
    Streaming is safer for large files because it avoids loading the whole object
    into memory or writing it to local disk.

    GOTCHA:
    This is still a GET request and data transfer still applies.
    """
    s3 = get_s3_client()

    response = s3.get_object(Bucket=bucket, Key=key)

    count = 0
    for raw_line in response["Body"].iter_lines():
        line = raw_line.decode("utf-8")

        yield line

        count += 1
        if max_lines and count >= max_lines:
            break


def download_range(bucket, key, byte_start, byte_end):
    """
    Download a byte range from an S3 object.

    WHY:
    Range reads are useful for inspecting headers, footers, file signatures,
    partial CSV samples, or splittable file formats.

    GOTCHA:
    byte_end is inclusive in the HTTP Range header.
    """
    s3 = get_s3_client()

    response = s3.get_object(
        Bucket=bucket,
        Key=key,
        Range=f"bytes={byte_start}-{byte_end}",
    )

    return response["Body"].read()


def delete_object_if_exists(bucket, key):
    """
    Best-effort cleanup for tutorial objects.
    """
    s3 = get_s3_client()

    try:
        s3.delete_object(Bucket=bucket, Key=key)
        print(f"Deleted: s3://{bucket}/{key}")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code not in ("NoSuchKey", "404"):
            raise


def main():
    if not S3_BUCKET_NAME:
        raise RuntimeError(
            "Missing S3_BUCKET_NAME environment variable. "
            "Example: set S3_BUCKET_NAME=my-unique-bucket-name"
        )

    bucket = S3_BUCKET_NAME
    local_path = Path("tmp_s3_demo/large_metrics.csv")

    manual_key = "tutorial/s3-multipart/manual-large-metrics.csv"
    auto_key = "tutorial/s3-multipart/auto-large-metrics.csv"

    generate_synthetic_large_file(local_path, size_mb=150)

    estimate = calculate_multipart_cost(file_size_gb=0.15, part_size_mb=100)
    print("\nMultipart estimate:")
    for key, value in estimate.items():
        print(f"{key}: {value}")

    print("\nManual multipart upload:")
    upload_large_file(
        bucket=bucket,
        key=manual_key,
        local_path=local_path,
        part_size_mb=100,
    )

    print("\nTransferConfig upload:")
    upload_with_transfer_config(
        bucket=bucket,
        key=auto_key,
        local_path=local_path,
    )

    print("\nFirst 100 streamed lines:")
    for line in stream_object_lines(bucket, manual_key, max_lines=100):
        print(line)

    print("\nRange read sample:")
    sample = download_range(bucket, manual_key, 0, 300)
    print(sample.decode("utf-8", errors="replace"))

    print("\nCleanup:")
    delete_object_if_exists(bucket, manual_key)
    delete_object_if_exists(bucket, auto_key)

    print("\nNOTE:")
    print("For production, prefer TransferConfig unless you need custom multipart control.")
    print("Also configure lifecycle cleanup for incomplete multipart uploads.")


if __name__ == "__main__":
    main()