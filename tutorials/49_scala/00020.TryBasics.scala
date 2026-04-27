import scala.util.{Try, Success, Failure}

object TryBasics {
  def main(args: Array[String]): Unit = {
    
    // --- WHAT IS 'Transaction'? ---
    // You asked: "What the word Transaction mean?"
    // In this specific code, we are parsing a simple Double (Amount).
    // BUT, imagine if you were parsing a Line from a CSV file into a Transaction object.
    // val t = Try(parseLine("T001,500.00,US")) 
    // This could fail if the CSV line is bad. 
    // So 'Try' protects your pipeline from crashing when converting data into Transactions.

    // 1. THE PROBLEM: Exceptions
    // Double.parseDouble("abc") throws an Exception and crashes your program.
    // We want to "catch" that safely.

    // 2. THE SOLUTION: Try
    // It wraps the dangerous code.
    // Returns:
    // - Success(value) -> It worked!
    // - Failure(error) -> It failed (with the exception inside).

    def parseAmount(s: String): Try[Double] = {
      Try(s.toDouble)  // wraps the risky operation
    }

    // 3. TESTING
    val good = parseAmount("5000.00")   // Success(5000.0)
    val bad  = parseAmount("abc")       // Failure(NumberFormatException)

    println(s"Good result: $good")
    println(s"Bad result:  $bad")
    println("-------------------")

    // 4. PATTERN MATCHING ON TRY
    // Just like Option, you match the two possible states.
    
    println("Matching Good:")
    good match {
      case Success(amount) => println(s"Valid amount: $amount")
      case Failure(ex)     => println(s"Parse error: ${ex.getMessage}")
    }
    // Valid amount: 5000.0

    println("\nMatching Bad:")
    bad match {
      case Success(amount) => println(s"Valid amount: $amount")
      case Failure(ex)     => println(s"Parse error: ${ex.getMessage}")
    }
    // Parse error: For input string: "abc"
  }
}
