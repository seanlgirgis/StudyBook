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

// 3. DEFINE SCHEMA (Case Class)
case class Transaction(
  id:       String,
  amount:   Double,
  category: String,
  country:  String,
  status:   String
)

object SparkBasics {
  def main(args: Array[String]): Unit = {
    
    // 1. SETUP SPARK SESSION
    val spark = SparkSession.builder()
      .appName("CapitalOne Transaction Pipeline")
      .master("local[*]")  
      .getOrCreate()

    // 2. IMPORT IMPLICITS
    import spark.implicits._

    // 4. CREATE DATAFRAME
    val transactions = Seq(
      Transaction("T001", 5000.00,  "retail",   "US", "approved"),
      Transaction("T002", 75000.00, "wire",     "UK", "approved"),
      Transaction("T003", 200.00,   "gambling", "US", "approved"),
      Transaction("T004", 1200.00,  "retail",   "CA", "declined"),
      Transaction("T005", 450.00,   "grocery",  "US", "approved")
    ).toDF()  // .toDF() works because of the import spark.implicits._

    // 5. SHOW RESULTS
    println("--- Transactions DataFrame ---")
    transactions.show()

    // 6. STOP SPARK
    spark.stop()
  }
}
