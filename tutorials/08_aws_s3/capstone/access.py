import boto3
import os

BUCKET = os.getenv("S3_BUCKET_NAME")
s3 = boto3.client("s3")


def get_last_5():
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix="bronze/")
    objs = sorted(resp.get("Contents", []), key=lambda x: x["LastModified"], reverse=True)
    return objs[:5]


def generate_urls():
    for obj in get_last_5():
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET, "Key": obj["Key"]},
            ExpiresIn=3600,
        )
        print(obj["Key"], url)


if __name__ == "__main__":
    generate_urls()