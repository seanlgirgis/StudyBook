# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : 02_spark_jobs_on_emr.py
# Covers  : Submit PySpark jobs to EMR with steps, S3 scripts, and log inspection
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket
# Run     : python 02_spark_jobs_on_emr.py
# ============================================================

from __future__ import annotations

import os
import tempfile
import time
from pathlib import Path
from typing import Any

import boto3
from botocore.exceptions import ClientError


# Environment variables used by this file:
# - AWS_REGION: AWS region where EMR runs, for example us-east-1.
# - AWS_PROFILE: Optional named AWS CLI profile for local development.
# - EMR_S3_BUCKET: S3 bucket for scripts, input, output, and logs.
# - EMR_SUBNET_ID: Required by the tutorial standard; not directly used in this step file.
# - EMR_CLUSTER_ID: Existing EMR cluster ID where Spark steps will be submitted.
#
# Cost note:
# This file does not create a cluster. It submits work to an existing cluster.
# The existing cluster may continue accruing EC2 and EMR charges until terminated.

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_PROFILE = os.environ.get("AWS_PROFILE")
EMR_S3_BUCKET = os.environ.get("EMR_S3_BUCKET")
EMR_SUBNET_ID = os.environ.get("EMR_SUBNET_ID")
EMR_CLUSTER_ID = os.environ.get("EMR_CLUSTER_ID")


SAMPLE_PYSPARK_SCRIPT = '''\
from __future__ import annotations

import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import count


def main() -> None:
    if len(sys.argv) != 3:
        raise ValueError("Usage: spark-submit sample_spark_job.py <input_csv_s3> <output_parquet_s3>")

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    spark = (
        SparkSession.builder
        .appName("studybook-emr-category-counts")
        .getOrCreate()
    )

    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(input_path)
    )

    result = (
        df.groupBy("category")
        .agg(count("*").alias("row_count"))
        .orderBy("category")
    )

    result.write.mode("overwrite").parquet(output_path)

    print(f"Input path: {input_path}")
    print(f"Output path: {output_path}")
    print(f"Category count rows: {result.count()}")

    spark.stop()


if __name__ == "__main__":
    main()
'''


def get_boto3_session() -> boto3.session.Session:
    if AWS_PROFILE:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return boto3.Session(region_name=AWS_REGION)


def get_emr_client() -> Any:
    return get_boto3_session().client("emr")


def get_s3_client() -> Any:
    return get_boto3_session().client("s3")


def upload_script_to_s3(
    script_path: str,
    bucket: str,
    prefix: str = "emr-scripts",
) -> str:
    """
    Upload local PySpark script to S3. Return full s3:// URI.
    Print: Uploaded {script_path} → s3://{bucket}/{prefix}/{filename}
    """
    s3 = get_s3_client()
    path = Path(script_path)
    key = f"{prefix.rstrip('/')}/{path.name}"

    s3.upload_file(str(path), bucket, key)

    uri = f"s3://{bucket}/{key}"
    print(f"Uploaded {script_path} → {uri}")
    return uri


def submit_spark_step(
    cluster_id: str,
    script_s3_path: str,
    args: list[str],
    step_name: str = "PySpark Step",
    action_on_failure: str = "CONTINUE",
) -> str:
    """
    Submit a Spark step to an existing cluster. Return step_id.
    Jar: command-runner.jar, Args: ["spark-submit", script_s3_path, *args]
    """
    emr = get_emr_client()

    response = emr.add_job_flow_steps(
        JobFlowId=cluster_id,
        Steps=[
            {
                "Name": step_name,
                "ActionOnFailure": action_on_failure,
                "HadoopJarStep": {
                    "Jar": "command-runner.jar",
                    "Args": ["spark-submit", script_s3_path, *args],
                },
            }
        ],
    )

    step_id = response["StepIds"][0]
    print(f"Submitted Spark step: {step_id}")
    return step_id


def wait_for_step(
    cluster_id: str,
    step_id: str,
    poll_interval: int = 15,
    timeout: int = 600,
) -> str:
    """
    Poll step status every poll_interval seconds.
    Print progress dots: Step {step_id}: PENDING... RUNNING... COMPLETED
    Return final state string.
    Raise TimeoutError if not terminal within timeout.
    """
    emr = get_emr_client()
    start = time.time()
    last_state = ""

    print(f"Step {step_id}: ", end="", flush=True)

    while time.time() - start < timeout:
        response = emr.describe_step(ClusterId=cluster_id, StepId=step_id)
        state = response["Step"]["Status"]["State"]

        if state != last_state:
            print(f"{state}...", end="", flush=True)
            last_state = state

        if state in {"COMPLETED", "FAILED", "CANCELLED", "INTERRUPTED"}:
            print()
            if state != "COMPLETED":
                reason = response["Step"]["Status"].get("FailureDetails", {})
                raise RuntimeError(f"Step {step_id} ended in {state}: {reason}")
            return state

        time.sleep(poll_interval)

    print()
    raise TimeoutError(f"Step {step_id} did not finish within {timeout} seconds.")


def get_step_logs(
    cluster_id: str,
    step_id: str,
    bucket: str,
) -> str:
    """
    Construct S3 log path: s3://{bucket}/emr-logs/{cluster_id}/steps/{step_id}/
    Attempt to read stderr and stdout from S3.
    Return concatenated log content or "Logs not yet available" if key missing.
    """
    s3 = get_s3_client()
    base_key = f"emr-logs/{cluster_id}/steps/{step_id}"
    log_keys = [
        f"{base_key}/stdout.gz",
        f"{base_key}/stderr.gz",
        f"{base_key}/stdout",
        f"{base_key}/stderr",
    ]

    chunks: list[str] = []

    for key in log_keys:
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            body = response["Body"].read()

            if key.endswith(".gz"):
                import gzip

                content = gzip.decompress(body).decode("utf-8", errors="replace")
            else:
                content = body.decode("utf-8", errors="replace")

            chunks.append(f"\n--- s3://{bucket}/{key} ---\n{content}")
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code in {"NoSuchKey", "404", "NoSuchBucket"}:
                continue
            raise

    if not chunks:
        return "Logs not yet available"

    return "\n".join(chunks)


def build_spark_submit_args(
    conf_overrides: dict[str, str] | None = None,
    py_files: list[str] | None = None,
    jars: list[str] | None = None,
) -> list[str]:
    """
    Build list of spark-submit CLI arguments.
    conf_overrides: {"spark.executor.memory": "4g"} → ["--conf", "spark.executor.memory=4g", ...]
    py_files: ["s3://bucket/lib.py"] → ["--py-files", "s3://bucket/lib.py"]
    jars: ["s3://bucket/dep.jar"] → ["--jars", "s3://bucket/dep.jar"]
    """
    spark_args: list[str] = []

    if conf_overrides:
        for key, value in conf_overrides.items():
            spark_args.extend(["--conf", f"{key}={value}"])

    if py_files:
        spark_args.extend(["--py-files", ",".join(py_files)])

    if jars:
        spark_args.extend(["--jars", ",".join(jars)])

    return spark_args


def generate_script_content() -> str:
    return SAMPLE_PYSPARK_SCRIPT


def print_submit_arg_examples() -> None:
    examples = [
        (
            "Small job",
            build_spark_submit_args(
                conf_overrides={
                    "spark.executor.instances": "2",
                    "spark.executor.memory": "2g",
                }
            ),
        ),
        (
            "Memory-heavy job",
            build_spark_submit_args(
                conf_overrides={
                    "spark.executor.instances": "8",
                    "spark.executor.memory": "8g",
                    "spark.driver.memory": "4g",
                }
            ),
        ),
        (
            "Job with dependencies",
            build_spark_submit_args(
                conf_overrides={"spark.sql.shuffle.partitions": "200"},
                py_files=["s3://example-bucket/libs/shared_transforms.py"],
                jars=["s3://example-bucket/jars/custom-connector.jar"],
            ),
        ),
    ]

    print("\nSpark Submit Argument Examples")
    print("=" * 88)
    for name, args in examples:
        print(f"{name:24}: {args}")


def main() -> None:
    print("AWS EMR Spark Jobs")
    print("=" * 72)
    print_submit_arg_examples()

    if not EMR_S3_BUCKET:
        print("\nSet EMR_S3_BUCKET to upload scripts and inspect logs.")

    if EMR_CLUSTER_ID and EMR_S3_BUCKET:
        step_id: str | None = None

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                script_path = str(Path(temp_dir) / "sample_spark_job.py")
                Path(script_path).write_text(generate_script_content(), encoding="utf-8")

                script_s3 = upload_script_to_s3(script_path, EMR_S3_BUCKET)

                input_path = f"s3://{EMR_S3_BUCKET}/sample/category_input/"
                output_path = f"s3://{EMR_S3_BUCKET}/sample/category_output/"

                spark_args = build_spark_submit_args(
                    conf_overrides={
                        "spark.executor.instances": "2",
                        "spark.executor.memory": "2g",
                    }
                )

                step_id = submit_spark_step(
                    cluster_id=EMR_CLUSTER_ID,
                    script_s3_path=script_s3,
                    args=[*spark_args, input_path, output_path],
                    step_name="Studybook category count",
                    action_on_failure="CONTINUE",
                )

                final_state = wait_for_step(EMR_CLUSTER_ID, step_id)
                print(f"Final step state: {final_state}")

                logs = get_step_logs(EMR_CLUSTER_ID, step_id, EMR_S3_BUCKET)
                print("\nStep Logs")
                print("=" * 72)
                print(logs[:4000])
        finally:
            print(
                "\nThis file submitted work to an existing EMR cluster. "
                "Terminate the cluster when finished to stop EC2 and EMR charges."
            )
    else:
        print(
            "\nSet EMR_CLUSTER_ID and EMR_S3_BUCKET to run live step submission.\n"
            "No Spark step was submitted, and this script created no billable EMR resources."
        )
        print("\nGenerated PySpark Script")
        print("=" * 72)
        print(generate_script_content())


if __name__ == "__main__":
    main()