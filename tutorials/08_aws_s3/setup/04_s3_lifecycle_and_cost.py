# ============================================================
# Topic   : AWS S3 for Data Engineers
# File    : 04_s3_lifecycle_and_cost.py
# Covers  : S3 cost optimization — lifecycle rules, storage classes, Intelligent-Tiering, cost calculator
# Prereqs : pip install boto3 | AWS credentials | S3 bucket
# Run     : python 04_s3_lifecycle_and_cost.py
# ============================================================

import json
import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


# Simplified monthly storage pricing examples for us-east-1.
# Always verify current AWS pricing before using this for real forecasting.
STORAGE_PRICING_PER_GB_MONTH = {
    "STANDARD": 0.023,
    "STANDARD_IA": 0.0125,
    "ONEZONE_IA": 0.01,
    "GLACIER_IR": 0.004,
    "DEEP_ARCHIVE": 0.00099,
    "INTELLIGENT_TIERING": 0.023,
}

RETRIEVAL_PRICING_PER_GB = {
    "STANDARD": 0.00,
    "STANDARD_IA": 0.01,
    "ONEZONE_IA": 0.01,
    "GLACIER_IR": 0.03,
    "DEEP_ARCHIVE": 0.02,
    "INTELLIGENT_TIERING": 0.00,
}


def get_s3_client():
    """
    Create an S3 client without hardcoding credentials.

    WHY:
    Local engineers can use AWS_PROFILE. Production pipelines should usually use
    IAM roles from ECS, EC2, Lambda, Glue, or Airflow workers.
    """
    if AWS_PROFILE:
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    else:
        session = boto3.Session(region_name=AWS_REGION)

    return session.client("s3")


def create_lifecycle_rule(bucket, rule_id, prefix, transitions, expiration_days=None):
    """
    Create a lifecycle rule for objects under a prefix.

    WHY:
    Lifecycle rules are one of the easiest ways to reduce S3 cost for aging data.

    GOTCHA:
    Some storage classes have minimum storage durations. Moving/deleting too early
    can create early deletion charges.
    """
    s3 = get_s3_client()

    rule = {
        "ID": rule_id,
        "Status": "Enabled",
        "Filter": {"Prefix": prefix},
        "Transitions": [
            {
                "Days": item["days"],
                "StorageClass": item["storage_class"],
            }
            for item in transitions
        ],
    }

    if expiration_days:
        rule["Expiration"] = {"Days": expiration_days}

    try:
        existing = s3.get_bucket_lifecycle_configuration(Bucket=bucket)
        rules = existing.get("Rules", [])
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "NoSuchLifecycleConfiguration":
            rules = []
        else:
            raise

    rules = [r for r in rules if r.get("ID") != rule_id]
    rules.append(rule)

    s3.put_bucket_lifecycle_configuration(
        Bucket=bucket,
        LifecycleConfiguration={"Rules": rules},
    )

    print(f"Created lifecycle rule '{rule_id}' on prefix '{prefix}'")


def calculate_storage_cost(size_gb, storage_class, region="us-east-1"):
    """
    Estimate monthly storage cost.

    WHY:
    Data engineers should understand storage class tradeoffs, not just push files
    into S3 forever.

    NOTE:
    This uses simplified sample prices. Real AWS pricing varies by region, request
    type, object count, monitoring fees, and retrieval pattern.
    """
    price = STORAGE_PRICING_PER_GB_MONTH.get(storage_class)

    if price is None:
        raise ValueError(f"Unsupported storage class: {storage_class}")

    return {
        "region": region,
        "size_gb": size_gb,
        "storage_class": storage_class,
        "price_per_gb_month": price,
        "estimated_monthly_cost": round(size_gb * price, 4),
    }


def calculate_retrieval_cost(size_gb, storage_class, requests=1000):
    """
    Estimate retrieval cost.

    WHY:
    Lower storage cost can be misleading. Infrequent-access and archive classes
    may charge retrieval fees.
    """
    retrieval_price = RETRIEVAL_PRICING_PER_GB.get(storage_class)

    if retrieval_price is None:
        raise ValueError(f"Unsupported storage class: {storage_class}")

    # Simplified GET request estimate.
    get_request_cost = (requests / 1000) * 0.0004
    data_retrieval_cost = size_gb * retrieval_price

    return {
        "size_gb": size_gb,
        "storage_class": storage_class,
        "requests": requests,
        "retrieval_price_per_gb": retrieval_price,
        "estimated_get_request_cost": round(get_request_cost, 6),
        "estimated_data_retrieval_cost": round(data_retrieval_cost, 4),
        "estimated_total_retrieval_cost": round(
            get_request_cost + data_retrieval_cost, 4
        ),
    }


def recommend_storage_class(access_frequency_per_month, size_gb, min_storage_days):
    """
    Recommend a storage class based on access frequency and retention.

    WHY:
    Storage class choice depends on access pattern, size, and how long the object
    will live.

    DECISION RULE:
    - frequent access: STANDARD
    - unknown access: INTELLIGENT_TIERING
    - rare access but quick retrieval: STANDARD_IA
    - archive access: GLACIER_IR / DEEP_ARCHIVE
    """
    if access_frequency_per_month >= 4:
        return "STANDARD"

    if access_frequency_per_month >= 1:
        if min_storage_days >= 30 and size_gb >= 1:
            return "STANDARD_IA"
        return "STANDARD"

    if access_frequency_per_month == 0:
        if min_storage_days >= 180:
            return "DEEP_ARCHIVE"
        if min_storage_days >= 90:
            return "GLACIER_IR"
        return "STANDARD_IA"

    return "INTELLIGENT_TIERING"


def enable_intelligent_tiering(bucket, prefix):
    """
    Enable Intelligent-Tiering for a prefix.

    WHY:
    Intelligent-Tiering is useful when access patterns are unknown or change over
    time.

    COST NOTE:
    Intelligent-Tiering has monitoring/automation charges per object. It is usually
    better for larger objects, not millions of tiny files.
    """
    create_lifecycle_rule(
        bucket=bucket,
        rule_id=f"intelligent-tiering-{prefix.strip('/').replace('/', '-')}",
        prefix=prefix,
        transitions=[
            {
                "days": 0,
                "storage_class": "INTELLIGENT_TIERING",
            }
        ],
    )


def get_bucket_size_and_cost(bucket):
    """
    Estimate bucket size from object listing and calculate basic Standard cost.

    WHY:
    CloudWatch bucket storage metrics are better for production reporting, but
    object listing is simple for a tutorial bucket.

    GOTCHA:
    Listing very large buckets can be slow and expensive. Prefer S3 Inventory or
    CloudWatch metrics for serious reporting.
    """
    s3 = get_s3_client()
    paginator = s3.get_paginator("list_objects_v2")

    total_bytes = 0
    object_count = 0

    for page in paginator.paginate(Bucket=bucket):
        for obj in page.get("Contents", []):
            total_bytes += obj["Size"]
            object_count += 1

    size_gb = total_bytes / (1024 ** 3)
    cost = calculate_storage_cost(size_gb, "STANDARD", AWS_REGION)

    return {
        "bucket": bucket,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "object_count": object_count,
        "total_bytes": total_bytes,
        "size_gb": round(size_gb, 6),
        "estimated_standard_monthly_cost": cost["estimated_monthly_cost"],
    }


def compare_storage_classes(size_gb):
    """
    Compare simplified monthly storage costs across common classes.
    """
    rows = []

    for storage_class in STORAGE_PRICING_PER_GB_MONTH:
        rows.append(calculate_storage_cost(size_gb, storage_class, AWS_REGION))

    return rows


def main():
    if not S3_BUCKET_NAME:
        raise RuntimeError(
            "Missing S3_BUCKET_NAME environment variable. "
            "Example: set S3_BUCKET_NAME=my-unique-bucket-name"
        )

    bucket = S3_BUCKET_NAME

    print("\nCreate lifecycle rule for log data:")
    create_lifecycle_rule(
        bucket=bucket,
        rule_id="logs-30d-ia-90d-glacier-365d-delete",
        prefix="logs/",
        transitions=[
            {"days": 30, "storage_class": "STANDARD_IA"},
            {"days": 90, "storage_class": "GLACIER_IR"},
        ],
        expiration_days=365,
    )

    print("\nEnable Intelligent-Tiering for unknown-access data:")
    enable_intelligent_tiering(bucket, prefix="unknown-access/")

    print("\nStorage class recommendation examples:")
    examples = [
        {"access_frequency_per_month": 20, "size_gb": 100, "min_storage_days": 30},
        {"access_frequency_per_month": 1, "size_gb": 500, "min_storage_days": 90},
        {"access_frequency_per_month": 0, "size_gb": 1000, "min_storage_days": 365},
    ]

    for item in examples:
        recommendation = recommend_storage_class(**item)
        print({**item, "recommended_storage_class": recommendation})

    print("\nCost comparison for 1,000 GB:")
    print(json.dumps(compare_storage_classes(1000), indent=2))

    print("\nRetrieval cost examples for 1,000 GB:")
    retrieval_examples = [
        calculate_retrieval_cost(1000, "STANDARD", requests=1000),
        calculate_retrieval_cost(1000, "STANDARD_IA", requests=1000),
        calculate_retrieval_cost(1000, "GLACIER_IR", requests=1000),
    ]
    print(json.dumps(retrieval_examples, indent=2))

    print("\nBucket size and simple Standard cost estimate:")
    print(json.dumps(get_bucket_size_and_cost(bucket), indent=2))

    print("\nNOTE:")
    print("This calculator uses simplified sample pricing.")
    print("For production, use current AWS Pricing API, CUR, or Cost Explorer.")
    print("Lifecycle saves money only when access patterns and retention fit the class.")


if __name__ == "__main__":
    main()