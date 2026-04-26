# AWS Tutorial Development Guidelines & Lessons Learned

When generating new AWS tutorials (especially for S3), please incorporate the following constraints and lessons learned to ensure the provided code runs reliably in our local testing environments.

## 1. S3 Select Deprecation
**Context:** AWS deprecated S3 Select in mid-2024. For newly created buckets, attempting to use `select_object_content` will result in a `MethodNotAllowed` exception.
**Rule:** Avoid relying on S3 Select as a core pipeline mechanism. If you must demonstrate it for legacy purposes, **always** wrap the call in a `try/except ClientError` block. Catch `MethodNotAllowed` and degrade gracefully (e.g., print a warning) so the rest of the tutorial can continue executing.

## 2. Bucket Versioning & Cleanup Scripts
**Context:** If a setup script enables bucket versioning (`Status: Enabled`), a standard `list_objects_v2` and `delete_object` loop will only create delete markers, leaving the underlying object versions intact. Subsequent attempts to call `delete_bucket` will fail with a `BucketNotEmpty` exception.
**Rule:** When writing `cleanup.py` scripts for buckets that may have versioning enabled, you **must** forcefully delete all object versions and markers using the `boto3.resource` API:
```python
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket(BUCKET_NAME)
bucket.object_versions.delete()
s3_client.delete_bucket(Bucket=BUCKET_NAME)
```

## 3. Realistic Multipart Upload Constraints
**Context:** Demonstrating multipart uploads by generating excessively large synthetic files (e.g., 150MB) causes execution to hang or time out during automated testing on standard or constrained network connections.
**Rule:** To demonstrate multipart uploads and `TransferConfig`, use smaller synthetic files (e.g., 15MB) and manually lower the `TransferConfig` thresholds so the multipart logic is still triggered:
```python
config = TransferConfig(
    multipart_threshold=5 * 1024 * 1024,  # 5 MB
    multipart_chunksize=5 * 1024 * 1024,  # 5 MB
)
```

## 4. Resource Name Collisions
**Context:** Hardcoding bucket names or IAM roles leads to `BucketAlreadyExists` or `EntityAlreadyExists` exceptions if the tutorial is run multiple times or run across different environments.
**Rule:** Always instruct the user to pass globally unique names via environment variables (e.g., `S3_BUCKET_NAME`), and provide fallback logic using `uuid` or random integers to generate unique names dynamically if the environment variable is not provided.
