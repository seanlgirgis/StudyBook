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
import org.apache.spark.sql.functions._ // Import 'udf' and 'col'

// 1. DATA MODEL
// "Transaction": A single row of data representing a financial event.
// In Spark, this Case Class defines the columns (id, amount, etc.) automatically.
case class Transaction(
  id:       String,
  amount:   Double,
  category: String,
  country:  String,
  status:   String
)

object SparkUDFs {
  def main(args: Array[String]): Unit = {
    
    val spark = SparkSession.builder()
      .appName("CapitalOne UDF Demo")
      .master("local[*]")
      .getOrCreate()

    import spark.implicits._

    // 2. INPUT DATA
    val transactions = Seq(
      Transaction("T001", 5000.00,  "retail",   "US", "approved"),
      Transaction("T002", 75000.00, "wire",     "UK", "approved"),
      Transaction("T003", 200.00,   "gambling", "US", "approved"),
      Transaction("T004", 1200.00,  "retail",   "CA", "declined"),
      Transaction("T005", 450.00,   "grocery",  "US", "approved")
    ).toDF()

    println("--- Original Data ---")
    transactions.show()

    // 3. DEFINE THE UDF (User Defined Function)
    // Sometimes built-in functions (like sum, avg) aren't enough.
    // We want custom logic:
    // - High Risk: > 50,000 AND Foreign (not US)
    // - Medium Risk: > 10,000
    // - Low Risk: Everything else
    
    // We write a normal Scala function, and wrap it in 'udf(...)'.
    val riskScoreUDF = udf((amount: Double, country: String) => {
      (amount, country) match {
        // Pattern Matching is perfect for this!
        case (a, c) if a > 50000 && c != "US" => "HIGH"
        case (a, _) if a > 10000              => "MEDIUM"
        case _                                => "LOW"
      }
    })

    // 4. APPLY THE UDF
    // use .withColumn to create the new "risk_score" column.
    // We pass the *columns* into our UDF using col("name").
    
    val result = transactions
      .withColumn("risk_score", riskScoreUDF(col("amount"), col("country")))

    println("--- With Risk Scores (Calculated via UDF) ---")
    result.show()

    spark.stop()
  }
}
