import os
import boto3

BUCKET = os.getenv("S3_BUCKET_NAME")
s3 = boto3.client("s3")

def test_bucket_security():
    print("Testing bucket security and versioning...")
    
    # Check versioning
    versioning = s3.get_bucket_versioning(Bucket=BUCKET)
    assert versioning.get("Status") == "Enabled", "Versioning is not enabled"
    
    # Check Public Access Block
    pab = s3.get_public_access_block(Bucket=BUCKET)
    assert pab["PublicAccessBlockConfiguration"]["BlockPublicAcls"] == True, "Public access not blocked"
    print("✓ Bucket security verified")


def test_ingestion():
    print("Testing data ingestion...")
    
    # Check raw objects
    raw_objs = s3.list_objects_v2(Bucket=BUCKET, Prefix="raw/")
    assert "Contents" in raw_objs and len(raw_objs["Contents"]) == 10, "Expected 10 files in raw/"
    
    # Check bronze objects
    bronze_objs = s3.list_objects_v2(Bucket=BUCKET, Prefix="bronze/")
    assert "Contents" in bronze_objs and len(bronze_objs["Contents"]) == 10, "Expected 10 files in bronze/"
    
    # Verify tags on the first bronze object
    first_bronze = bronze_objs["Contents"][0]["Key"]
    tags = s3.get_object_tagging(Bucket=BUCKET, Key=first_bronze)
    tag_dict = {t["Key"]: t["Value"] for t in tags.get("TagSet", [])}
    
    assert tag_dict.get("source_system") == "iot", "Missing or incorrect source_system tag"
    assert tag_dict.get("data_classification") == "internal", "Missing or incorrect data_classification tag"
    
    print(f"✓ Ingestion verified (10 raw, 10 bronze, tags correctly applied to bronze)")


if __name__ == "__main__":
    print(f"Running integration tests against {BUCKET}...")
    try:
        test_bucket_security()
        test_ingestion()
        print("\nAll Capstone tests passed successfully! 🚀")
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
        exit(1)