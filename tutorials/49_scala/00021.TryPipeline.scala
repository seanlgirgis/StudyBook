import scala.util.{Try, Success, Failure}

object TryPipeline {
  def main(args: Array[String]): Unit = {
    
    // 1. DATA MODELS
    // 'RawRecord' = The Dirty Data (e.g., read from a CSV where everything is a String).
    case class RawRecord(id: String, amountStr: String, country: String)
    
    // 'Transaction' = The Clean Data (Typed and Validated).
    // You asked "What the word Transaction mean?"
    // Here, it represents the *Successful Result* of our parsing logic.
    case class Transaction(id: String, amount: Double, country: String)

    // 2. THE PARSER
    // Attempt to convert Raw -> Clean.
    // We return Try[Transaction] because it might fail.
    def parseRecord(raw: RawRecord): Try[Transaction] = Try {
      Transaction(
        id      = raw.id,
        amount  = raw.amountStr.toDouble,  // <--- THE RISKY PART (might explode)
        country = raw.country
      )
    }

    // 3. INPUT DATA (Mixed good and bad)
    val rawRecords = List(
      RawRecord("T001", "5000.00", "US"),
      RawRecord("T002", "abc",     "UK"),  // Bad: "abc" is not a number
      RawRecord("T003", "1200.00", "CA"),
      RawRecord("T004", "??",      "US")   // Bad: "??" is not a number
    )

    // 4. PROCESSING
    // Apply the parser to every record.
    // Result is a List[Try[Transaction]]
    val results = rawRecords.map(r => parseRecord(r))

    // 5. SEPARATION (The Magic Step)
    // .collect is like a mix of filter + map.
    
    // Extract only the Successes
    val good = results.collect { case Success(t) => t }
    
    // Extract only the Failures (and get their error messages)
    val bad  = results.collect { case Failure(e) => e.getMessage }

    // 6. REPORTING
    println("--- Good Records (Ready for Database) ---")
    good.foreach(println)

    println("\n--- Bad Records (Log for fixing) ---")
    bad.foreach(println)
  }
}
