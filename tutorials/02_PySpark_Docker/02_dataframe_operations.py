from __future__ import annotations

from pyspark.sql import functions as F

from common.spark_session import create_spark_session


def main() -> None:
    spark = create_spark_session("02_dataframe_operations")

    try:
        print("\n[Step 1] Build synthetic sales DataFrame with spark.range")
        sales_df = (
            spark.range(1, 200_001)
            .withColumnRenamed("id", "sale_id")
            .withColumn("date", F.expr("date_add(to_date('2026-01-01'), int(sale_id % 90))"))
            .withColumn(
                "region",
                F.when((F.col("sale_id") % 5) == 0, F.lit("North"))
                .when((F.col("sale_id") % 5) == 1, F.lit("South"))
                .when((F.col("sale_id") % 5) == 2, F.lit("East"))
                .when((F.col("sale_id") % 5) == 3, F.lit("West"))
                .otherwise(F.lit("Central")),
            )
            .withColumn(
                "model",
                F.when((F.col("sale_id") % 4) == 0, F.lit("Camry"))
                .when((F.col("sale_id") % 4) == 1, F.lit("Corolla"))
                .when((F.col("sale_id") % 4) == 2, F.lit("RAV4"))
                .otherwise(F.lit("Prius")),
            )
            .withColumn("units", (F.col("sale_id") % 6 + F.lit(1)).cast("int"))
            .withColumn(
                "unit_price",
                F.when(F.col("model") == "Camry", F.lit(32000.0))
                .when(F.col("model") == "Corolla", F.lit(24000.0))
                .when(F.col("model") == "RAV4", F.lit(35000.0))
                .otherwise(F.lit(29000.0)),
            )
            .withColumn("revenue", (F.col("units") * F.col("unit_price")).cast("double"))
            .withColumn("salesperson", F.concat(F.lit("SP_"), F.format_string("%04d", (F.col("sale_id") % 75))))
        )

        print("\nSchema:")
        sales_df.printSchema()

        print("\n[Step 2] select() only needed columns")
        selected = sales_df.select("sale_id", "date", "region", "model", "units", "revenue")
        selected.show(5, truncate=False)

        print("\n[Step 3] filter() high-value transactions")
        high_value = selected.filter((F.col("region") == "North") & (F.col("revenue") >= 120000.0))
        print(f"High-value count: {high_value.count()}")
        high_value.show(5, truncate=False)

        print("\n[Step 4] withColumn() business features")
        enriched = (
            sales_df.withColumn("month", F.date_format("date", "yyyy-MM"))
            .withColumn("is_high_ticket", F.col("unit_price") >= 30000.0)
            .withColumn(
                "discount_band",
                F.when(F.col("units") >= 5, F.lit("bulk"))
                .when(F.col("units") >= 3, F.lit("standard"))
                .otherwise(F.lit("small")),
            )
        )
        enriched.select("sale_id", "region", "model", "units", "unit_price", "is_high_ticket", "discount_band").show(
            8, truncate=False
        )

        print("\n[Step 5] groupBy() + agg() monthly sales by region/model")
        monthly_summary = (
            enriched.groupBy("month", "region", "model")
            .agg(
                F.count("*").alias("num_sales"),
                F.sum("units").alias("total_units"),
                F.round(F.sum("revenue"), 2).alias("total_revenue"),
                F.round(F.avg("revenue"), 2).alias("avg_revenue"),
            )
            .orderBy(F.col("total_revenue").desc(), F.col("month"), F.col("region"), F.col("model"))
        )
        monthly_summary.show(15, truncate=False)

        print("\n[Step 6] orderBy() top salespeople by revenue")
        top_salespeople = (
            enriched.groupBy("salesperson")
            .agg(F.round(F.sum("revenue"), 2).alias("salesperson_revenue"))
            .orderBy(F.col("salesperson_revenue").desc())
        )
        top_salespeople.show(10, truncate=False)

        print("\n[Step 7] explain(True) on aggregated pipeline")
        monthly_summary.explain(True)

        print("\nConcept recap:")
        print("- Transformations (select/filter/withColumn/groupBy/orderBy) are lazy.")
        print("- Actions (count/show) trigger execution across partitions.")
        print("- explain(True) reveals logical and physical execution plans.")

    finally:
        print("\nStopping Spark session...")
        spark.stop()


if __name__ == "__main__":
    main()
