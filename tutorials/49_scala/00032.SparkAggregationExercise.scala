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

// --- DATA MODEL ---
// In this example, "Sale" is the Transaction.
// A "Transaction" generally means a single unit of work or a single event record.
// Here, every time someone buys something, we record one 'Sale' object.
case class Sale(region: String, product: String, amount: Double)

object SparkAggregationExercise {
  def main(args: Array[String]): Unit = {
    
    val spark = SparkSession.builder()
      .appName("Sales Aggregation")
      .master("local[*]")
      .config("spark.driver.bindAddress", "127.0.0.1")
      .getOrCreate()

    import spark.implicits._

    // 1. CREATE DATA
    // We have 5 transactions (Sales).
    val sales = Seq(
      Sale("North", "Laptop",  1200.00),
      Sale("South", "Phone",    800.00),
      Sale("North", "Tablet",   600.00),
      Sale("South", "Laptop",  1100.00),
      Sale("North", "Phone",    750.00)
    ).toDF()

    println("--- Raw Sales Data ---")
    sales.show()

    // 2. THE LOGIC
    // We want to know: How is each Region performing?
    val result = sales
      .groupBy("region")
      .agg(
        count("product").as("total_sales"), // How many items sold?
        sum("amount").as("total_revenue")   // How much money total?
      )
      .withColumn("avg_sale", col("total_revenue") / col("total_sales")) // Derived metric
      .orderBy(desc("total_revenue")) // Highest revenue first

    // 3. THE OUTPUT
    // What does it look like?
    // North: Sold 3 items (1200 + 600 + 750 = 2550). Avg = 2550 / 3 = 850.
    // South: Sold 2 items (800 + 1100 = 1900). Avg = 1900 / 2 = 950.
    
    println("--- Regional Performance Report ---")
    result.show()

    spark.stop()
  }
}
