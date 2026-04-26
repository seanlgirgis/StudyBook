import boto3
import os

BUCKET = os.getenv("S3_BUCKET_NAME")
s3 = boto3.client("s3")


def cleanup():
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(BUCKET)
    bucket.object_versions.delete()
    s3.delete_bucket(Bucket=BUCKET)


if __name__ == "__main__":
    cleanup()
    print("Cleanup complete")