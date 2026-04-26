import boto3
import os

BUCKET = os.getenv("S3_BUCKET_NAME")
s3 = boto3.client("s3")


def cleanup():
    resp = s3.list_objects_v2(Bucket=BUCKET)

    for obj in resp.get("Contents", []):
        s3.delete_object(Bucket=BUCKET, Key=obj["Key"])

    s3.delete_bucket(Bucket=BUCKET)


if __name__ == "__main__":
    cleanup()
    print("Cleanup complete")