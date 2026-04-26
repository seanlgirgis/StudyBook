from __future__ import annotations

from pyspark.sql import functions as F

from common.spark_session import create_spark_session


def main() -> None:
    spark = create_spark_session("03_sql_and_views")

    try:
        print("\n[Step 1] Build synthetic sales DataFrame")
        sales_df = (
            spark.range(1, 200_001)
            .withColumnRenamed("id", "sale_id")
            .withColumn("date", F.expr("date_add(to_date('2026-01-01'), int(sale_id % 120))"))
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
            .withColumn("month", F.date_format("date", "yyyy-MM"))
        )

        print("\n[Step 2] Register temp view")
        sales_df.createOrReplaceTempView("sales")
        print("Temp view created: sales")

        print("\n[Step 3] SQL aggregation (monthly region/model summary)")
        monthly_sql = """
        SELECT
            month,
            region,
            model,
            COUNT(*) AS num_sales,
            SUM(units) AS total_units,
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(AVG(revenue), 2) AS avg_revenue
        FROM sales
        GROUP BY month, region, model
        ORDER BY total_revenue DESC, month, region, model
        """
        monthly_df = spark.sql(monthly_sql)
        monthly_df.show(15, truncate=False)

        print("\n[Step 4] CTE + window RANK() (top models per month by revenue)")
        rank_sql = """
        WITH model_monthly AS (
            SELECT
                month,
                model,
                ROUND(SUM(revenue), 2) AS model_revenue
            FROM sales
            GROUP BY month, model
        )
        SELECT
            month,
            model,
            model_revenue,
            RANK() OVER (
                PARTITION BY month
                ORDER BY model_revenue DESC
            ) AS revenue_rank
        FROM model_monthly
        ORDER BY month, revenue_rank, model
        """
        ranked_df = spark.sql(rank_sql)
        ranked_df.show(20, truncate=False)

        print("\n[Step 5] CTE + LAG() for month-over-month growth by region")
        mom_sql = """
        WITH region_monthly AS (
            SELECT
                month,
                region,
                ROUND(SUM(revenue), 2) AS monthly_revenue
            FROM sales
            GROUP BY month, region
        )
        SELECT
            month,
            region,
            monthly_revenue,
            LAG(monthly_revenue) OVER (
                PARTITION BY region
                ORDER BY month
            ) AS prev_month_revenue,
            ROUND(
                CASE
                    WHEN LAG(monthly_revenue) OVER (PARTITION BY region ORDER BY month) IS NULL THEN NULL
                    WHEN LAG(monthly_revenue) OVER (PARTITION BY region ORDER BY month) = 0 THEN NULL
                    ELSE (
                        (monthly_revenue - LAG(monthly_revenue) OVER (PARTITION BY region ORDER BY month))
                        / LAG(monthly_revenue) OVER (PARTITION BY region ORDER BY month)
                    ) * 100
                END,
                2
            ) AS mom_growth_pct
        FROM region_monthly
        ORDER BY region, month
        """
        mom_df = spark.sql(mom_sql)
        mom_df.show(30, truncate=False)

        print("\n[Step 6] Explain SQL plan (monthly aggregation query)")
        monthly_df.explain(True)

        print("\nConcept recap:")
        print("- Temp views let you mix DataFrame creation with SQL analytics.")
        print("- CTEs make multi-step SQL logic easier to read and maintain.")
        print("- Window functions (RANK/LAG) support ranking and trend analysis.")
        print("- explain(True) helps inspect logical and physical SQL execution plans.")

    finally:
        print("\nStopping Spark session...")
        spark.stop()


if __name__ == "__main__":
    main()
