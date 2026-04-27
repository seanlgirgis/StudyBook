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
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

case class Salary(dep: String, emp: String, salary: Int)

object SparkWindowFunctions {
  def main(args: Array[String]): Unit = {
    
    // FIREWALL NOTE: 
    // Spark by default tries to connect to your network card.
    // Setting "spark.driver.bindAddress" to "127.0.0.1" forces it to stay local.
    // This helps security and might reduce some firewall prompts (though Java itself still needs permission).

    val spark = SparkSession.builder()
      .appName("Window Functions Demo")
      .master("local[*]")
      .config("spark.driver.bindAddress", "127.0.0.1") // <--- STRICT LOCAL BINDING
      .config("spark.ui.enabled", "false")             // <--- DISABLING UI (Optional, speeds up local runs)
      .getOrCreate()

    import spark.implicits._

    val data = Seq(
      Salary("Sales",     "Alice",  5000),
      Salary("Sales",     "Bob",    4200),
      Salary("Sales",     "Charlie", 5000), // Trie with Alice
      Salary("Sales",     "David",  3000),
      Salary("Engineering", "Eve",    6000),
      Salary("Engineering", "Frank",  6000), // Tie with Eve
      Salary("Engineering", "Grace",  4500)
    ).toDF()

    println("--- Original Data ---")
    data.show()

    // GOAL: Rank employees by salary WITHIN each department.

    // 1. DEFINE WINDOW spec
    // "Partition by Department, Order by Salary Descending"
    val windowSpec = Window
      .partitionBy("dep")
      .orderBy(col("salary").desc)

    // 2. APPLY FUNCTIONS
    val ranked = data
      .withColumn("row_number", row_number().over(windowSpec)) // 1, 2, 3, 4 (Unique)
      .withColumn("rank",       rank().over(windowSpec))       // 1, 2, 2, 4 (Skips 3)
      .withColumn("dense_rank", dense_rank().over(windowSpec)) // 1, 2, 2, 3 (No skips)

    println("--- Ranked Employees ---")
    ranked.show()

    spark.stop()
  }
}
