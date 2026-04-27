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
import org.apache.spark.sql.SaveMode
import java.nio.file.{Files, Paths}
import java.nio.charset.StandardCharsets

// 1. DATA MODEL
case class Transaction(
  id:       String,
  amount:   Double,
  category: String,
  country:  String,
  status:   String
)

object SparkReadWrite {
  def main(args: Array[String]): Unit = {
    
    val spark = SparkSession.builder()
      .appName("CapitalOne IO Demo")
      .master("local[*]")
      .getOrCreate()

    import spark.implicits._

    // --- WINDOWS WORKAROUND ---
    // Normally we would do: transactions.write.csv(...)
    // But on Windows without 'winutils.exe' installed, Spark Writing crashes.
    // So for this example, we will CREATE the files manually using Java IO,
    // and then demonstrate how Spark READS them (which works fine!).

    println("--- Creating Mock Data Files ---")
    val csvContent = 
      """id,amount,category,country,status
        |T001,5000.0,retail,US,approved
        |T002,75000.0,wire,UK,approved
        |T003,200.0,gambling,US,approved
        |""".stripMargin
    
    val jsonContent = 
      """{"id":"T004","amount":1200.0,"category":"retail","country":"CA","status":"declined"}
        |{"id":"T005","amount":450.0,"category":"grocery","country":"US","status":"approved"}
        |""".stripMargin

    // Create a 'data' folder
    Files.createDirectories(Paths.get("data_input"))
    
    // Write the files
    Files.write(Paths.get("data_input/transactions.csv"), csvContent.getBytes(StandardCharsets.UTF_8))
    Files.write(Paths.get("data_input/transactions.json"), jsonContent.getBytes(StandardCharsets.UTF_8))
    
    println("Created data_input/transactions.csv")
    println("Created data_input/transactions.json")

    // 4. READING DATA (The "Sources")
    // This is the standard Spark API.
    
    println("\n--- Reading from CSV ---")
    val dfCsv = spark.read
      .option("header", "true")       // Use first line as columns
      .option("inferSchema", "true")  // Guess types (Double vs String)
      .csv("data_input/transactions.csv")
    
    dfCsv.show()
    dfCsv.printSchema() // Verify schema inference

    println("--- Reading from JSON ---")
    val dfJson = spark.read
      .json("data_input/transactions.json")
    
    dfJson.show()

    // 5. WRITING (Commented out for Windows compatibility)
    // If you had Hadoop/Winutils set up, you would do:
    /*
    dfCsv.write
      .mode("overwrite")
      .parquet("data_output/transactions_parquet")
    */
    println("\n(Skipping 'write' demo as it requires winutils.exe on Windows)")

    spark.stop()
  }
}
