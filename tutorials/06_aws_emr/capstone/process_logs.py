# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : capstone/process_logs.py
# Covers  : PySpark EMR Serverless log processing job
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket
# Run     : spark-submit capstone/process_logs.py <input_s3_uri> <output_s3_uri>
# ============================================================

from __future__ import annotations

import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, count, date_format, hour, sum as spark_sum, to_timestamp


def main() -> None:
    if len(sys.argv) != 3:
        raise ValueError(
            "Usage: spark-submit process_logs.py "
            "<input_csv_s3_uri> <output_parquet_s3_uri>"
        )

    input_uri = sys.argv[1]
    output_uri = sys.argv[2]

    spark = (
        SparkSession.builder
        .appName("studybook-emr-serverless-log-processing")
        .getOrCreate()
    )

    raw_df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(input_uri)
    )

    input_count = raw_df.count()

    parsed_df = raw_df.withColumn(
        "parsed_timestamp",
        to_timestamp(col("timestamp"))
    )

    errors_df = (
        parsed_df
        .filter(col("status_code") >= 400)
        .withColumn("hour", hour(col("parsed_timestamp")))
        .withColumn("date", date_format(col("parsed_timestamp"), "yyyy-MM-dd"))
    )

    aggregated_df = (
        errors_df
        .groupBy("date", "endpoint", "status_code", "hour")
        .agg(
            count("*").alias("request_count"),
            avg("response_time_ms").alias("avg_response_ms"),
            spark_sum("bytes_sent").alias("total_bytes"),
        )
    )

    output_count = aggregated_df.count()

    (
        aggregated_df.write
        .mode("overwrite")
        .partitionBy("date", "status_code")
        .parquet(output_uri)
    )

    print("=" * 72)
    print("EMR Serverless Log Processing Complete")
    print("=" * 72)
    print(f"Input URI    : {input_uri}")
    print(f"Output URI   : {output_uri}")
    print(f"Input rows   : {input_count:,}")
    print(f"Output groups: {output_count:,}")
    print("Filtered rule: status_code >= 400")
    print("Partitions   : date, status_code")

    spark.stop()


if __name__ == "__main__":
    main()
