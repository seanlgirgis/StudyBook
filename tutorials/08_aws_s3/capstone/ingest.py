import csv
import io
import os
import boto3
from datetime import datetime

BUCKET = os.getenv("S3_BUCKET_NAME")
s3 = boto3.client("s3")


def generate_csv(i):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["sensor_id", "value"])
    writer.writerow([f"s{i}", i * 10])
    return buffer.getvalue()


def ingest():
    for i in range(10):
        key = f"raw/sensor_{i}.csv"

        body = generate_csv(i)
        s3.put_object(Bucket=BUCKET, Key=key, Body=body)

        if len(body) == 0:
            continue

        bronze_key = key.replace("raw/", "bronze/")

        s3.copy_object(
            Bucket=BUCKET,
            Key=bronze_key,
            CopySource={"Bucket": BUCKET, "Key": key},
            Tagging="source_system=iot&data_classification=internal",
            TaggingDirective="REPLACE",
        )


if __name__ == "__main__":
    ingest()
    print("Ingestion complete")