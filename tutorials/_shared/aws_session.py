# ============================================================
# Shared AWS Session Helper
# _shared/aws_session.py
#
# Provides a consistent boto3 session and client factory for
# all tutorial files. Centralizing this means:
#   - One place to change region or profile
#   - Consistent credential handling across all tutorials
#   - Easy to swap to assumed-role or EC2 instance profile later
# ============================================================

import os
import boto3
from botocore.config import Config
from botocore.exceptions import NoCredentialsError, ProfileNotFound

# ── Configuration from environment ───────────────────────────
# Never hardcode region or profile. These come from the shell
# environment so the same code works across dev/staging/prod.
AWS_REGION  = os.environ.get("AWS_REGION", "us-east-1")
AWS_PROFILE = os.environ.get("AWS_PROFILE")          # None = use default chain

# Standard retry config applied to all clients.
# max_attempts=3 with adaptive mode backs off intelligently
# under throttling — better than fixed exponential for bursty workloads.
RETRY_CONFIG = Config(
    region_name=AWS_REGION,
    retries={"max_attempts": 3, "mode": "adaptive"},
)


def get_session() -> boto3.Session:
    """
    Return a boto3 Session configured from environment variables.

    Uses AWS_PROFILE if set, otherwise falls back to the default
    credential chain (env vars → ~/.aws/credentials → instance profile).
    Centralizing session creation means all tutorials pick up the same
    credentials without each file reimplementing credential logic.

    Returns:
        boto3.Session: configured session

    Raises:
        ProfileNotFound: if AWS_PROFILE is set but does not exist
    """
    try:
        if AWS_PROFILE:
            return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
        return boto3.Session(region_name=AWS_REGION)
    except ProfileNotFound as e:
        raise ProfileNotFound(
            profile=AWS_PROFILE,
        ) from e


def get_client(service: str, **kwargs) -> boto3.client:
    """
    Return a boto3 client for the given AWS service with standard retry config.

    Prefer this over boto3.client() directly because it applies consistent
    retry configuration, region, and credential source across all tutorials.

    Args:
        service: AWS service name (e.g. 's3', 'kinesis', 'glue')
        **kwargs: additional arguments passed to session.client()

    Returns:
        boto3 client for the specified service

    Raises:
        NoCredentialsError: if no AWS credentials are available

    Example:
        s3 = get_client("s3")
        kinesis = get_client("kinesis")
    """
    try:
        session = get_session()
        return session.client(service, config=RETRY_CONFIG, **kwargs)
    except NoCredentialsError:
        raise NoCredentialsError(
        ) from None


def get_resource(service: str, **kwargs):
    """
    Return a boto3 resource for the given AWS service.

    Use get_resource() for higher-level abstractions (e.g. S3 Object,
    DynamoDB Table). Use get_client() when you need raw API access or
    the service does not have a resource interface (e.g. Kinesis, Glue).

    Args:
        service: AWS service name (e.g. 's3', 'dynamodb')
        **kwargs: additional arguments passed to session.resource()

    Returns:
        boto3 resource for the specified service

    Example:
        s3 = get_resource("s3")
        bucket = s3.Bucket("my-bucket")
    """
    session = get_session()
    return session.resource(service, config=RETRY_CONFIG, **kwargs)


def whoami() -> dict:
    """
    Return the current AWS identity — useful for verifying credentials at
    the start of any tutorial that makes real AWS calls.

    Returns:
        dict with UserId, Account, and Arn of the current caller
    """
    sts = get_client("sts")
    return sts.get_caller_identity()


if __name__ == "__main__":
    print("AWS Session Helper — verifying credentials")
    print(f"  Region  : {AWS_REGION}")
    print(f"  Profile : {AWS_PROFILE or '(default)'}")
    try:
        identity = whoami()
        print(f"  Account : {identity['Account']}")
        print(f"  ARN     : {identity['Arn']}")
        print("  Status  : OK")
    except Exception as e:
        print(f"  Status  : FAILED — {e}")
