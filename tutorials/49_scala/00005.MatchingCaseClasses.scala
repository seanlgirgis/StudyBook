object MatchingCaseClasses {
  def main(args: Array[String]): Unit = {
    
    // --- WHAT IS 'Transaction'? ---
    // Here, Transaction is a 'case class'. 
    // Think of a Case Class as a "Data Container" (like a Python @dataclass or a Struct).
    // It is designed to hold data immutably (values cannot change).
    // Scala automatically gives it superpowers like:
    // 1. Easy to print (toString is auto-generated)
    // 2. Easy to compare (compares values, not memory addresses)
    // 3. Perfect for Pattern Matching (as seen below)
    case class Transaction(id: String, amount: Double, status: String)

    // The function takes a Transaction object 't' and matches it against patterns
    def processTransaction(t: Transaction): String = t match {
      
      // Pattern 1: Deconstructs the object.
      // Matches specific status "approved" PLUS a condition (Guard) 'if amount > 10000'
      // It extracts 'id' and 'amount' variables to use in the return string.
      case Transaction(id, amount, "approved") if amount > 10000 =>
        s"$id: Large approved transaction — flag for review"

      // Pattern 2: Matches status "approved" (implicitly, amount is <= 10000 here)
      case Transaction(id, amount, "approved") =>
        s"$id: Normal approved transaction of $$$amount"

      // Pattern 3: Matches status "flagged". 
      // Uses '_' (Wildcard) for amount because we don't care what the amount is.
      case Transaction(id, _, "flagged") =>
        s"$id: ALERT — flagged transaction!"

      // Pattern 4: Matches status "declined". 
      case Transaction(id, _, "declined") =>
        s"$id: Declined — notify customer"

      // Default Case: Matches anything else preventing a "MatchError"
      case _ =>
        "Unknown transaction state"
    }
    // Creating instances of the Case Class
    val t1 = Transaction("T001", 5000.00, "approved")
    val t2 = Transaction("T002", 15000.00, "flagged")
    val t3 = Transaction("T003", 200.00, "declined")
    // Testing the function
    println(processTransaction(t1))  // Output: T001: Normal approved transaction...
    println(processTransaction(t2))  // Output: T002: Large approved transaction... wait, t2 amount is 15000, so it matches the HIGH RISK logic? 
                                     // Actually t2 is "flagged", so it matches Pattern 3 first? 
                                     // (Correction: t2 status is "flagged", so it matches Pattern 3)
    println(processTransaction(t3))  // Output: T003: Declined...
  }
}
