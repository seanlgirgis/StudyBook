//> using scala 2.13
//> using dep org.apache.spark::spark-sql:3.5.0
//> using javaOpt --add-opens=java.base/sun.nio.ch=ALL-UNNAMED
//> using javaOpt --add-opens=java.base/sun.util.calendar=ALL-UNNAMED
//> using javaOpt --add-opens=java.base/java.lang=ALL-UNNAMED
//> using javaOpt --add-opens=java.base/java.lang.invoke=ALL-UNNAMED
//> using javaOpt --add-opens=java.base/java.lang.reflect=ALL-UNNAMED
//> using javaOpt --add-opens=java.base/java.io=ALL-UNNAMED
//> using javaOpt --add-opens=java.base/java.net=ALL-UNNAMED
//> using javaOpt --add-opens=java.base/java.nio=ALL-UNNAMED
//> using javaOpt --add-opens=java.base/java.util=ALL-UNNAMED
//> using javaOpt --add-opens=java.base/java.util.concurrent=ALL-UNNAMED
//> using javaOpt --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import java.nio.file.{Files, Paths}
import java.nio.charset.StandardCharsets

// --- DATA MODEL ---
// "Transaction": A case class is the blueprint for our data.
// It defines exactly what columns we expect and their types.
case class Transaction(
  id:         String,
  customerId: String,
  amount:     Double,
  category:   String,
  country:    String,
  status:     String
)

object TransactionPipeline {
  def main(args: Array[String]): Unit = {

    val spark = SparkSession.builder()
      .appName("Transaction Risk Pipeline")
      .master("local[*]")
      .config("spark.driver.bindAddress", "127.0.0.1") // Firewall friendly
      .getOrCreate()

    import spark.implicits._

    // 0. GENERATE MOCK DATA (Simulating S3)
    // We create a CSV file locally to mimic reading from an external source.
    val rawCsvData = 
      """id,customerId,amount,category,country,status
        |T001,C100,5000.0,retail,US,approved
        |T002,C101,75000.0,wire,UK,approved
        |T003,C102,200.0,gambling,US,approved
        |T004,C103,1200.0,retail,CA,declined
        |T005,C100,450.0,grocery,US,approved
        |T006,C104,15000.0,wire,US,approved
        |""".stripMargin

    Files.createDirectories(Paths.get("data_input"))
    Files.write(Paths.get("data_input/pipeline_data.csv"), rawCsvData.getBytes(StandardCharsets.UTF_8))
    println("--- Mock Data Created at data_input/pipeline_data.csv ---")


    // --- STEP 1: READ RAW DATA ---
    println("\n--- 1. Reads Raw CSV ---")
    val rawDf = spark.read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv("data_input/pipeline_data.csv")
    
    rawDf.show()

    // --- STEP 2: TYPED DATASET ---
    // Convert generic Rows into strongly-typed Transaction objects.
    // This ensures compile-time safety for downstream logic.
    val transactions = rawDf.as[Transaction]

    // --- STEP 3: DEFINE BUSINESS LOGIC (UDF) ---
    // Custom logic to flag risky transactions.
    val riskUDF = udf((amount: Double, country: String, category: String) => {
      (amount, country, category) match {
        // High amount outside US -> HIGH RISK
        case (a, c, _) if a > 50000 && c != "US" => "HIGH"
        // Gambling is always risky
        case (_, _, cat) if cat == "gambling"     => "MEDIUM"
        // Large domestic transfers
        case (a, _, _)  if a > 10000              => "MEDIUM"
        // Everything else
        case _                                     => "LOW"
      }
    })

    // --- STEP 4: TRANSFORM ---
    // Filter approved transactions, calculate risk, and add processing date.
    val enriched = transactions
      .filter(col("status") === "approved")
      .withColumn("risk_score", riskUDF(col("amount"), col("country"), col("category")))
      .withColumn("processed_date", current_date())

    println("\n--- 4. Transformed & Enriched Data ---")
    enriched.show()

    // --- STEP 5: AGGREGATE ---
    // Summarize risk exposure by Country and Score.
    val summary = enriched
      .groupBy("country", "risk_score")
      .agg(
        count("id").as("transaction_count"),
        sum("amount").as("total_amount"),
        avg("amount").as("avg_amount")
      )
      .orderBy(desc("total_amount"))

    println("\n--- 5. Final Summary Report ---")
    summary.show()

    // --- STEP 6: WRITE OUTPUT ---
    // (Simulated - would be .write.parquet in production)
    println("\n--- 6. Writing Output (Simulated) ---")
    println("Saving summary to: s3://capitalone/processed/risk_summary/ (Parquet)")
    /* 
    summary.write
      .mode("overwrite")
      .partitionBy("country")
      .parquet("s3://capitalone/processed/risk_summary/")
    */

    spark.stop()
  }
}
