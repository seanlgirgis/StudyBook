object EitherBasics {
  def main(args: Array[String]): Unit = {
    
    // 1. DATA MODEL
    // 'Transaction' again acts as our valid data container.
    // We define it here so the code below works.
    case class Transaction(id: String, amount: Double, country: String)

    // 2. THE CONCEPT: Either
    // Try is for Exceptions (crashes).
    // Either is for Logical Errors (validation rules).
    // It returns:
    // - Right(value) -> Valid Data (Success)
    // - Left(error)  -> Invalid Data (Failure with a custom message)

    // 3. THE VALIDATOR
    def validateTransaction(id: String, amount: Double): Either[String, Transaction] = {
      if (amount <= 0)
        Left(s"$id: Amount must be positive, got $amount") // Custom "Business" Error
      else if (amount > 1000000)
        Left(s"$id: Amount exceeds maximum limit: $amount") // Another Custom Rule
      else
        Right(Transaction(id, amount, "US")) // Success!
    }

    // 4. TEST CASES
    val r1 = validateTransaction("T001", 5000.00)     // Valid
    val r2 = validateTransaction("T002", -100.00)     // Logically Invalid (Negative)
    val r3 = validateTransaction("T003", 2000000.00)  // Logically Invalid (Too High)

    // 5. PROCESSING
    // We can handle the list of results just like Option or Try.
    
    val allResults = List(r1, r2, r3)
    
    println("--- Processing Results ---")
    allResults.foreach {
      case Right(t)    => println(s"Valid: ${t.id} — $$${t.amount}")
      case Left(error) => println(s"Invalid: $error")
    }
  }
}
