import boto3
import os

BUCKET = os.getenv("S3_BUCKET_NAME")

PRICING = {
    "STANDARD": 0.023,
    "STANDARD_IA": 0.0125,
    "GLACIER_IR": 0.004,
}


s3 = boto3.client("s3")


def get_size():
    total = 0
    resp = s3.list_objects_v2(Bucket=BUCKET)

    for obj in resp.get("Contents", []):
        total += obj["Size"]

    return total / (1024 ** 3)


def estimate():
    size = get_size()

    standard_cost = size * PRICING["STANDARD"]

    lifecycle_cost = (
        size * 0.5 * PRICING["STANDARD"]
        + size * 0.3 * PRICING["STANDARD_IA"]
        + size * 0.2 * PRICING["GLACIER_IR"]
    )

    print("Size GB:", size)
    print("All STANDARD:", standard_cost)
    print("Lifecycle cost:", lifecycle_cost)


if __name__ == "__main__":
    estimate()