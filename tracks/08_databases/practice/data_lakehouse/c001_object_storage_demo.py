# Story:
# Object storage keeps files in buckets with prefixes. Objects are immutable;
# updates mean writing a new object version.

BUCKET = "analytics"

OBJECTS = [
    {"key": "raw/orders/2026/03/27/orders_0001.parquet", "bytes": 1200},
    {"key": "raw/orders/2026/03/27/orders_0002.parquet", "bytes": 1400},
    {"key": "curated/orders/2026/03/27/orders_daily.parquet", "bytes": 900},
]


def list_prefix(objects, prefix):
    return [obj for obj in objects if obj["key"].startswith(prefix)]


def put_object(objects, key, bytes_size):
    objects.append({"key": key, "bytes": bytes_size})
    print(f"PUT s3://{BUCKET}/{key} ({bytes_size} bytes)")


def overwrite_object(objects, key, bytes_size):
    # Object storage is immutable; overwrite means writing a new object key.
    new_key = f"{key}.v2"
    put_object(objects, new_key, bytes_size)
    print(f"NOTE: original object remains at {key}")


def run_object_storage_demo():
    print("=" * 72)
    print("Scenario: object storage concepts")
    print(f"Bucket: {BUCKET}")

    print("\nList raw/ prefix")
    raw_objects = list_prefix(OBJECTS, "raw/")
    for obj in raw_objects:
        print(f"  {obj}")

    print("\nWrite a new curated object")
    put_object(OBJECTS, "curated/orders/2026/03/28/orders_daily.parquet", 950)

    print("\nOverwrite by writing a new object")
    overwrite_object(OBJECTS, "curated/orders/2026/03/27/orders_daily.parquet", 980)

    print("\nSummary")
    print("- Buckets + prefixes organize files like folders.")
    print("- Objects are immutable; updates create new files.")
    print("- File-based layout differs from row-level database storage.")


if __name__ == "__main__":
    run_object_storage_demo()

# Takeaway: Object storage is file-based and immutable.
