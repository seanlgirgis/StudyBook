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

// 1. DATA MODELS
// We have two "tables" here.
// 'Customer': The Dimension Table (Who they are)
case class Customer(id: String, name: String, tier: String)

// 'Transaction2': The Fact Table (What they did)
// "What does Transaction mean?": It represents a spending event linked to a Customer ID.
case class Transaction2(id: String, customerId: String, amount: Double)

object SparkJoins {
  def main(args: Array[String]): Unit = {
    
    val spark = SparkSession.builder()
      .appName("CapitalOne Join Demo")
      .master("local[*]")
      .getOrCreate()

    import spark.implicits._

    // 2. CREATE DATASETS
    val customers = Seq(
      Customer("C001", "Alice Johnson", "Premium"),
      Customer("C002", "Bob Smith",     "Standard"),
      Customer("C003", "Carol White",   "Premium")
    ).toDF()

    val transactions2 = Seq(
      Transaction2("T001", "C001", 5000.00),
      Transaction2("T002", "C001", 3000.00),
      Transaction2("T003", "C002", 1500.00),
      Transaction2("T004", "C999", 750.00)   // "C999" does not exist in Customers!
    ).toDF()

    println("--- Customers ---")
    customers.show()
    
    println("--- Transactions ---")
    transactions2.show()

    // 3. INNER JOIN
    // ambiguity fix: Both tables have 'id', so we must specify WHICH 'id' we want.
    // We use aliases "t" and "c".
    
    println("--- Inner Join (Matches Only) ---")
    val inner = transactions2.as("t")
      .join(customers.as("c"), $"t.customerId" === $"c.id", "inner")
      .select($"t.id", $"t.customerId", $"t.amount", $"c.name", $"c.tier")

    inner.show()

    // 4. LEFT JOIN
    println("--- Left Join (Keep All Transactions) ---")
    val left = transactions2.as("t")
      .join(customers.as("c"), $"t.customerId" === $"c.id", "left")
      .select($"t.id", $"t.customerId", $"t.amount", $"c.name", $"c.tier")

    left.show()

    spark.stop()
  }
}
