import os
import boto3

BUCKET = os.getenv("S3_BUCKET_NAME")
REGION = os.getenv("AWS_REGION", "us-east-1")

s3 = boto3.client("s3")


def create_bucket():
    if REGION == "us-east-1":
        s3.create_bucket(Bucket=BUCKET)
    else:
        s3.create_bucket(
            Bucket=BUCKET,
            CreateBucketConfiguration={"LocationConstraint": REGION},
        )


def enable_security():
    s3.put_public_access_block(
        Bucket=BUCKET,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )

    s3.put_bucket_versioning(
        Bucket=BUCKET,
        VersioningConfiguration={"Status": "Enabled"},
    )

    s3.put_bucket_encryption(
        Bucket=BUCKET,
        ServerSideEncryptionConfiguration={
            "Rules": [{
                "ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}
            }]
        },
    )


def create_lifecycle():
    s3.put_bucket_lifecycle_configuration(
        Bucket=BUCKET,
        LifecycleConfiguration={
            "Rules": [
                {
                    "ID": "raw-lifecycle",
                    "Prefix": "raw/",
                    "Status": "Enabled",
                    "Transitions": [
                        {"Days": 30, "StorageClass": "STANDARD_IA"},
                        {"Days": 180, "StorageClass": "GLACIER_IR"},
                    ],
                    "Expiration": {"Days": 730},
                }
            ]
        },
    )


if __name__ == "__main__":
    create_bucket()
    enable_security()
    create_lifecycle()
    print("Setup complete")