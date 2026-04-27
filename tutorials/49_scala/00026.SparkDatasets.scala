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

// 1. DATA MODEL
// Just like before, the Case Class defines the schema.
case class Transaction(
  id:       String,
  amount:   Double,
  category: String,
  country:  String,
  status:   String
)

object SparkDatasets {
  def main(args: Array[String]): Unit = {
    
    val spark = SparkSession.builder()
      .appName("CapitalOne Type Safety Demo")
      .master("local[*]")
      .getOrCreate()

    import spark.implicits._

    // 2. CREATE DATAFRAME (Untyped)
    // At this point, Spark just knows it has "columns".
    val df = Seq(
      Transaction("T001", 5000.00,  "retail",   "US", "approved"),
      Transaction("T002", 75000.00, "wire",     "UK", "approved"),
      Transaction("T003", 200.00,   "gambling", "US", "approved"),
      Transaction("T004", 1200.00,  "retail",   "CA", "declined"),
      Transaction("T005", 450.00,   "grocery",  "US", "approved")
    ).toDF()

    // 3. CONVERT TO DATASET (Typed)
    // This is the Scala "Secret Weapon".
    // We convert the loose rows into a collection of 'Transaction' objects.
    val ds = df.as[Transaction]

    println("--- Typed Dataset Filtering ---")
    
    // POWER MOVE 1: Compile-Time Safety
    // In Python or SQL, if you write: df.filter("amountt > 1000"), it crashes AT RUNTIME.
    // In Scala Datasets, if you write: ds.filter(t => t.amountt > 1000), it FAILS TO COMPILE.
    // You catch typos instantly.

    // POWER MOVE 2: Object-Oriented Logic
    // We can use standard Scala code inside the filter/map!
    val flagged = ds
      .filter(t => t.amount > 1000 && t.country == "US")
      .map(t => t.copy(status = "flagged")) // We use the .copy() method from the case class!

    flagged.show()
    
    // POWER MOVE 3: Mixing & Matching
    // You can swap back to DataFrame (SQL style) whenever you want, e.g., for aggregation.
    println("--- Aggregation (Back to DataFrame style) ---")
    ds.groupBy("country")
      .count()
      .show()

    spark.stop()
  }
}
