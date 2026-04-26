# ============================================================
# Topic   : AWS S3 for Data Engineers
# File    : 01_s3_fundamentals.py
# Covers  : Core S3 operations — buckets, objects, metadata, tagging, versioning
# Prereqs : pip install boto3 | AWS credentials | S3 bucket
# Run     : python 01_s3_fundamentals.py
# ============================================================

import os
import json
from pathlib import Path
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def get_s3_client():
    """
    Create an S3 client using either the default credential chain or AWS_PROFILE.

    WHY:
    Data engineers should avoid hardcoding credentials. boto3 can read credentials
    from environment variables, AWS profiles, EC2/ECS roles, or SSO-backed profiles.
    """
    if AWS_PROFILE:
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    else:
        session = boto3.Session(region_name=AWS_REGION)

    return session.client("s3")


def create_bucket(name, region):
    """
    Create an S3 bucket.

    GOTCHA:
    us-east-1 is special. CreateBucketConfiguration must NOT be sent for us-east-1.
    For every other region, LocationConstraint is required.
    """
    s3 = get_s3_client()

    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=name)
        else:
            s3.create_bucket(
                Bucket=name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )

        print(f"Created bucket: {name}")

    except ClientError as e:
        code = e.response["Error"]["Code"]

        if code in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
            print(f"Bucket already exists or is already owned by you: {name}")
        else:
            raise


def upload_file(bucket, key, local_path, metadata=None, storage_class="STANDARD"):
    """
    Upload a local file to S3.

    WHY:
    Metadata is useful for data lineage, source tracking, classification, and audit.
    StorageClass controls cost/performance behavior.

    COST NOTE:
    STANDARD is best for frequently accessed data.
    IA/Glacier classes can reduce storage cost but add retrieval fees and minimum
    storage duration charges.
    """
    s3 = get_s3_client()

    extra_args = {
        "StorageClass": storage_class,
    }

    if metadata:
        extra_args["Metadata"] = metadata

    s3.upload_file(
        Filename=str(local_path),
        Bucket=bucket,
        Key=key,
        ExtraArgs=extra_args,
    )

    print(f"Uploaded: {local_path} -> s3://{bucket}/{key}")


def download_file(bucket, key, local_path):
    """
    Download an S3 object to a local file.

    WHY:
    In real pipelines, downloads are usually avoided for large files.
    Prefer streaming or distributed reads when possible.
    """
    s3 = get_s3_client()
    local_path = Path(local_path)
    local_path.parent.mkdir(parents=True, exist_ok=True)

    s3.download_file(bucket, key, str(local_path))

    print(f"Downloaded: s3://{bucket}/{key} -> {local_path}")


def list_objects(bucket, prefix="", page_size=100):
    """
    List objects in a bucket using pagination.

    GOTCHA:
    S3 list_objects_v2 returns a limited page of results.
    Never assume one API call returns all objects.
    """
    s3 = get_s3_client()

    paginator = s3.get_paginator("list_objects_v2")

    objects = []

    for page in paginator.paginate(
        Bucket=bucket,
        Prefix=prefix,
        PaginationConfig={"PageSize": page_size},
    ):
        for item in page.get("Contents", []):
            objects.append(
                {
                    "Key": item["Key"],
                    "Size": item["Size"],
                    "LastModified": item["LastModified"].isoformat(),
                    "StorageClass": item.get("StorageClass", "STANDARD"),
                }
            )

    return objects


def get_object_metadata(bucket, key):
    """
    Read object metadata using head_object.

    GOTCHA:
    ETag is not always an MD5 checksum.
    For multipart uploads, ETag usually includes a dash and part count.
    Do not blindly use ETag as a data integrity checksum.
    """
    s3 = get_s3_client()

    response = s3.head_object(Bucket=bucket, Key=key)

    metadata = {
        "ContentType": response.get("ContentType"),
        "ContentLength": response.get("ContentLength"),
        "ETag": response.get("ETag"),
        "LastModified": response.get("LastModified").isoformat(),
        "StorageClass": response.get("StorageClass", "STANDARD"),
        "UserMetadata": response.get("Metadata", {}),
    }

    return metadata


def enable_versioning(bucket):
    """
    Enable bucket versioning.

    WHY:
    Versioning protects against accidental overwrite/delete.

    GOTCHA:
    Deleting an object in a versioned bucket creates a delete marker.
    Old versions still exist and still cost money until permanently deleted.
    """
    s3 = get_s3_client()

    s3.put_bucket_versioning(
        Bucket=bucket,
        VersioningConfiguration={"Status": "Enabled"},
    )

    print(f"Enabled versioning on bucket: {bucket}")


def tag_object(bucket, key, tags):
    """
    Add or replace object tags.

    WHY:
    Tags are useful for cost allocation, governance, lifecycle rules, and ownership.
    """
    s3 = get_s3_client()

    tag_set = [{"Key": k, "Value": v} for k, v in tags.items()]

    s3.put_object_tagging(
        Bucket=bucket,
        Key=key,
        Tagging={"TagSet": tag_set},
    )

    print(f"Tagged object: s3://{bucket}/{key}")


def delete_object(bucket, key, version_id=None):
    """
    Delete an object.

    GOTCHA:
    With versioning enabled:
    - deleting without version_id creates a delete marker
    - deleting with version_id removes that specific version
    """
    s3 = get_s3_client()

    args = {
        "Bucket": bucket,
        "Key": key,
    }

    if version_id:
        args["VersionId"] = version_id

    s3.delete_object(**args)

    if version_id:
        print(f"Deleted version: s3://{bucket}/{key} version={version_id}")
    else:
        print(f"Deleted object or created delete marker: s3://{bucket}/{key}")


def create_sample_files(base_dir):
    """
    Create small local files for upload demo.
    """
    base_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "customers.csv": "customer_id,name,region\n1,Alice,TX\n2,Bob,CA\n",
        "orders.csv": "order_id,customer_id,amount\n101,1,250.50\n102,2,99.99\n",
        "readme.txt": "S3 fundamentals demo file.\n",
    }

    created = []

    for filename, content in files.items():
        path = base_dir / filename
        path.write_text(content, encoding="utf-8")
        created.append(path)

    return created


def main():
    if not S3_BUCKET_NAME:
        raise RuntimeError(
            "Missing S3_BUCKET_NAME environment variable. "
            "Example: set S3_BUCKET_NAME=my-unique-bucket-name"
        )

    bucket = S3_BUCKET_NAME
    demo_prefix = "tutorial/s3-fundamentals"
    local_dir = Path("tmp_s3_demo")

    create_bucket(bucket, AWS_REGION)
    enable_versioning(bucket)

    sample_files = create_sample_files(local_dir)

    upload_plan = [
        {
            "path": sample_files[0],
            "key": f"{demo_prefix}/customers.csv",
            "metadata": {
                "source_system": "crm",
                "data_classification": "internal",
                "created_by": "s3_tutorial",
            },
        },
        {
            "path": sample_files[1],
            "key": f"{demo_prefix}/orders.csv",
            "metadata": {
                "source_system": "orders",
                "data_classification": "internal",
                "created_by": "s3_tutorial",
            },
        },
        {
            "path": sample_files[2],
            "key": f"{demo_prefix}/readme.txt",
            "metadata": {
                "source_system": "manual",
                "data_classification": "public",
                "created_by": "s3_tutorial",
            },
        },
    ]

    for item in upload_plan:
        upload_file(
            bucket=bucket,
            key=item["key"],
            local_path=item["path"],
            metadata=item["metadata"],
        )

        tag_object(
            bucket=bucket,
            key=item["key"],
            tags={
                "project": "aws-s3-tutorial",
                "environment": "dev",
                "created_date": datetime.now(timezone.utc).date().isoformat(),
            },
        )

    print("\nObjects in demo prefix:")
    objects = list_objects(bucket, prefix=demo_prefix)

    print(json.dumps(objects, indent=2))

    print("\nMetadata for uploaded objects:")
    for item in upload_plan:
        metadata = get_object_metadata(bucket, item["key"])
        print(f"\n{item['key']}")
        print(json.dumps(metadata, indent=2))

    download_target = local_dir / "downloaded_customers.csv"
    download_file(
        bucket=bucket,
        key=f"{demo_prefix}/customers.csv",
        local_path=download_target,
    )

    print("\nCleanup demo objects:")
    for item in upload_plan:
        delete_object(bucket, item["key"])

    print("\nNOTE:")
    print("If versioning is enabled, delete markers may remain.")
    print("For a full cleanup, list object versions and delete each version explicitly.")


if __name__ == "__main__":
    main()