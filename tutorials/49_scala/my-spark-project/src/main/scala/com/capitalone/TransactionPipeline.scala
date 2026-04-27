package com.capitalone

import com.capitalone.models.Transaction
import com.capitalone.utils.RiskEngine
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.log4j.{Level, Logger}

object TransactionPipeline {

  def main(args: Array[String]): Unit = {

    // Reduce log noise
    Logger.getLogger("org").setLevel(Level.ERROR)

    val spark = SparkSession.builder()
      .appName("Transaction Risk Pipeline")
      .master("local[*]") // Logic to run locally if no master is set
      .getOrCreate()

    import spark.implicits._

    // Handle args
    val inputPath = if (args.length > 0) args(0) else "data/sample_transactions.csv"
    val outputPath = if (args.length > 1) args(1) else "output/risk_summary"

    println(s"Reading from: $inputPath")
    println(s"Writing to: $outputPath")

    // Read
    val transactions = spark.read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv(inputPath)          // path passed as argument
      .as[Transaction]       // typed Dataset

    // Transform
    val result = transactions
      .filter(col("status") === "approved")
      .withColumn("risk_score",
        RiskEngine.riskScoreUDF(
          col("amount"),
          col("country"),
          col("category")
        )
      )

    result.show()

    // Write
    result.write
      .mode("overwrite")
      .partitionBy("country", "risk_score")
      .parquet(outputPath)      // output path passed as argument

    println("Pipeline completed successfully.")
    spark.stop()
  }
}
