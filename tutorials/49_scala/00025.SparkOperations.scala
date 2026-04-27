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
import org.apache.spark.sql.functions._ // Import standard functions like col, count, sum, avg

// 1. DEFINE SCHEMA (Must be outside main)
case class Transaction(
  id:       String,
  amount:   Double,
  category: String,
  country:  String,
  status:   String
)

object SparkOperations {
  def main(args: Array[String]): Unit = {
    
    // 2. SETUP SPARK
    val spark = SparkSession.builder()
      .appName("CapitalOne Transaction Pipeline")
      .master("local[*]")
      .getOrCreate()

    import spark.implicits._

    // 3. CREATE DATA
    val transactions = Seq(
      Transaction("T001", 5000.00,  "retail",   "US", "approved"),
      Transaction("T002", 75000.00, "wire",     "UK", "approved"),
      Transaction("T003", 200.00,   "gambling", "US", "approved"),
      Transaction("T004", 1200.00,  "retail",   "CA", "declined"),
      Transaction("T005", 450.00,   "grocery",  "US", "approved")
    ).toDF()

    println("--- 1. Original Data ---")
    transactions.show()

    // 4. PERFORM OPERATIONS
    
    // A. SELECT
    // Pick specific columns to view.
    println("--- 2. Select Specific Columns (id, amount, country) ---")
    transactions.select("id", "amount", "country").show()

    // B. FILTER
    // Keep rows matching a condition.
    println("--- 3. Filter High Amounts (> 1000) ---")
    transactions.filter(col("amount") > 1000).show()

    // C. FILTER WITH 'AND'
    // Combine multiple conditions.
    println("--- 4. Filter High Amount AND US --")
    transactions
      .filter(col("amount") > 1000 && col("country") === "US")
      .show()

    // D. WITHCOLUMN (Transformation)
    // Add a new column or modify an existing one.
    // Here we convert Amount to GBP (approx 0.79 rate).
    println("--- 5. Add Column (amountInGBP) ---")
    transactions
      .withColumn("amountInGBP", col("amount") * 0.79)
      .show()

    // E. AGGREGATION (GroupBy)
    // Summary statistics by group.
    println("--- 6. Aggregation by Country ---")
    transactions
      .groupBy("country")
      .agg(
        count("id").as("total_transactions"),
        sum("amount").as("total_amount"),
        avg("amount").as("avg_amount")
      )
      .show()

    spark.stop()
  }
}
