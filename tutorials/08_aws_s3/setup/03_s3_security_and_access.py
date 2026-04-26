# ============================================================
# Topic   : AWS S3 for Data Engineers
# File    : 03_s3_security_and_access.py
# Covers  : S3 security — bucket policies, ACLs, presigned URLs, encryption, Block Public Access
# Prereqs : pip install boto3 | AWS credentials | S3 bucket
# Run     : python 03_s3_security_and_access.py
# ============================================================

import json
import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
KMS_KEY_ID = os.getenv("KMS_KEY_ID")


def get_s3_client():
    """
    Create an S3 client using the AWS credential chain.

    WHY:
    Never hardcode access keys in pipeline code. Use AWS_PROFILE locally and IAM
    roles in production.
    """
    if AWS_PROFILE:
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    else:
        session = boto3.Session(region_name=AWS_REGION)

    return session.client("s3")


def block_all_public_access(bucket):
    """
    Enable S3 Block Public Access.

    WHY:
    This is the first safety rail. It blocks public ACLs and public bucket
    policies even if someone accidentally tries to add one later.
    """
    s3 = get_s3_client()

    s3.put_public_access_block(
        Bucket=bucket,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )

    print(f"Enabled Block Public Access on: {bucket}")


def apply_bucket_policy(bucket, policy_dict):
    """
    Apply a resource-based bucket policy.

    WHY:
    Bucket policies are useful for cross-account access, enforcing TLS,
    restricting prefixes, and denying insecure requests.

    GOTCHA:
    If BlockPublicPolicy is enabled, AWS rejects public bucket policies.
    That is usually exactly what you want.
    """
    s3 = get_s3_client()

    s3.put_bucket_policy(
        Bucket=bucket,
        Policy=json.dumps(policy_dict),
    )

    print(f"Applied bucket policy to: {bucket}")


def generate_presigned_url(bucket, key, expiry_seconds=3600):
    """
    Generate a time-limited URL for downloading an object.

    WHY:
    Presigned URLs let external users access one object without receiving AWS
    credentials.

    GOTCHA:
    The URL is bearer-token style. Anyone with the URL can use it until expiry.
    Keep expiry short and avoid logging URLs.
    """
    s3 = get_s3_client()

    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket,
            "Key": key,
        },
        ExpiresIn=expiry_seconds,
    )


def generate_presigned_post(bucket, key_prefix, max_size_bytes, expiry_seconds):
    """
    Generate a browser-friendly presigned POST for uploads.

    WHY:
    Useful when vendors, partners, or browser apps need to upload directly to S3
    without proxying large files through your backend.

    SECURITY:
    Restrict both key prefix and content length. Otherwise users may upload
    unexpected objects or huge files that increase cost.
    """
    s3 = get_s3_client()

    return s3.generate_presigned_post(
        Bucket=bucket,
        Key=f"{key_prefix}/${{filename}}",
        Fields={},
        Conditions=[
            ["starts-with", "$key", key_prefix],
            ["content-length-range", 1, max_size_bytes],
        ],
        ExpiresIn=expiry_seconds,
    )


def enable_sse_s3(bucket):
    """
    Enable default server-side encryption with S3-managed keys.

    WHY:
    SSE-S3 is simple and low-friction. AWS manages the keys.

    USE WHEN:
    You need encryption at rest but do not need customer-managed KMS audit,
    rotation controls, or key-level access policies.
    """
    s3 = get_s3_client()

    s3.put_bucket_encryption(
        Bucket=bucket,
        ServerSideEncryptionConfiguration={
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256",
                    },
                    "BucketKeyEnabled": False,
                }
            ]
        },
    )

    print(f"Enabled SSE-S3 default encryption on: {bucket}")


def enable_sse_kms(bucket, kms_key_id):
    """
    Enable default server-side encryption with KMS.

    WHY:
    SSE-KMS gives stronger governance: KMS key policies, CloudTrail audit events,
    explicit key ownership, and access separation.

    COST NOTE:
    SSE-KMS can add KMS request cost. For very high-volume pipelines, consider
    Bucket Keys to reduce KMS request volume.
    """
    if not kms_key_id:
        raise ValueError("kms_key_id is required for SSE-KMS")

    s3 = get_s3_client()

    s3.put_bucket_encryption(
        Bucket=bucket,
        ServerSideEncryptionConfiguration={
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "aws:kms",
                        "KMSMasterKeyID": kms_key_id,
                    },
                    "BucketKeyEnabled": True,
                }
            ]
        },
    )

    print(f"Enabled SSE-KMS default encryption on: {bucket}")


def check_bucket_security_posture(bucket):
    """
    Report important S3 bucket security settings.

    Checks:
    - Block Public Access
    - Default encryption
    - Versioning
    - Server access logging

    WHY:
    Data engineers are often responsible for proving that pipeline storage is
    not public, encrypted, recoverable, and auditable.
    """
    s3 = get_s3_client()

    report = {
        "bucket": bucket,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "public_access_block": None,
        "default_encryption": None,
        "versioning": None,
        "logging": None,
        "findings": [],
    }

    try:
        response = s3.get_public_access_block(Bucket=bucket)
        report["public_access_block"] = response["PublicAccessBlockConfiguration"]
    except ClientError as e:
        report["public_access_block"] = "NOT_CONFIGURED"
        report["findings"].append("Block Public Access is not configured.")

    try:
        response = s3.get_bucket_encryption(Bucket=bucket)
        report["default_encryption"] = response["ServerSideEncryptionConfiguration"]
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "ServerSideEncryptionConfigurationNotFoundError":
            report["default_encryption"] = "NOT_CONFIGURED"
            report["findings"].append("Default bucket encryption is not configured.")
        else:
            raise

    response = s3.get_bucket_versioning(Bucket=bucket)
    report["versioning"] = response.get("Status", "Disabled")

    if report["versioning"] != "Enabled":
        report["findings"].append("Versioning is not enabled.")

    response = s3.get_bucket_logging(Bucket=bucket)
    report["logging"] = response.get("LoggingEnabled", "NOT_CONFIGURED")

    if report["logging"] == "NOT_CONFIGURED":
        report["findings"].append("Server access logging is not configured.")

    if not report["findings"]:
        report["findings"].append("No major findings from this basic posture check.")

    return report


def enable_versioning(bucket):
    """
    Enable bucket versioning.

    WHY:
    Versioning helps recover from accidental overwrites and deletes.

    GOTCHA:
    Versioning increases storage usage because old versions remain billable.
    """
    s3 = get_s3_client()

    s3.put_bucket_versioning(
        Bucket=bucket,
        VersioningConfiguration={"Status": "Enabled"},
    )

    print(f"Enabled versioning on: {bucket}")


def upload_demo_object(bucket, key):
    """
    Upload a small object used for presigned URL testing.
    """
    s3 = get_s3_client()

    body = "sensor_id,value,timestamp\ns-001,42.5,2026-04-25T12:00:00Z\n"

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=body.encode("utf-8"),
        ContentType="text/csv",
        Metadata={
            "source_system": "iot_demo",
            "data_classification": "internal",
        },
    )

    print(f"Uploaded demo object: s3://{bucket}/{key}")


def build_tls_only_policy(bucket):
    """
    Build a bucket policy that denies non-TLS access.

    WHY:
    Sensitive pipeline data should never move over plain HTTP.
    This deny policy enforces HTTPS/TLS at the bucket layer.
    """
    bucket_arn = f"arn:aws:s3:::{bucket}"
    object_arn = f"arn:aws:s3:::{bucket}/*"

    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "DenyInsecureTransport",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": [bucket_arn, object_arn],
                "Condition": {
                    "Bool": {
                        "aws:SecureTransport": "false"
                    }
                },
            }
        ],
    }


def main():
    if not S3_BUCKET_NAME:
        raise RuntimeError(
            "Missing S3_BUCKET_NAME environment variable. "
            "Example: set S3_BUCKET_NAME=my-unique-bucket-name"
        )

    bucket = S3_BUCKET_NAME
    demo_key = "tutorial/s3-security/demo_sensor.csv"

    print("\nInitial security posture:")
    initial_report = check_bucket_security_posture(bucket)
    print(json.dumps(initial_report, indent=2, default=str))

    print("\nApplying security controls:")
    block_all_public_access(bucket)
    enable_versioning(bucket)

    if KMS_KEY_ID:
        enable_sse_kms(bucket, KMS_KEY_ID)
    else:
        enable_sse_s3(bucket)

    tls_policy = build_tls_only_policy(bucket)
    apply_bucket_policy(bucket, tls_policy)

    upload_demo_object(bucket, demo_key)

    print("\nPresigned GET URL:")
    url = generate_presigned_url(bucket, demo_key, expiry_seconds=3600)
    print(url)

    print("\nPresigned POST policy:")
    post = generate_presigned_post(
        bucket=bucket,
        key_prefix="tutorial/s3-security/uploads/",
        max_size_bytes=10 * 1024 * 1024,
        expiry_seconds=3600,
    )
    print(json.dumps(post, indent=2))

    print("\nFinal security posture:")
    final_report = check_bucket_security_posture(bucket)
    print(json.dumps(final_report, indent=2, default=str))

    print("\nNOTE:")
    print("Presigned URLs are sensitive. Do not paste real URLs into logs or tickets.")
    print("For high-volume SSE-KMS pipelines, review KMS request cost and Bucket Keys.")


if __name__ == "__main__":
    main()