object CopyMethod {
  def main(args: Array[String]): Unit = {
    
    // --- WHAT IS 'Transaction'? ---
    // Again, 'Transaction' is a Case Class (Immutable Data Container).
    // Because it is IMMUTABLE, you cannot change its fields after creation.
    // e.g., t1.status = "approved" would throw an ERROR.
    case class Transaction(id: String, amount: Double, status: String)

    // 1. Create the original transaction
    val t1 = Transaction("T001", 5000.00, "pending")

    // 2. The 'copy' Method
    // Since we can't change t1, we use .copy() to create a NEW object (t2).
    // We only specify the field we want to change (status).
    // All other fields (id, amount) are copied over automatically.
    val t2 = t1.copy(status = "approved")

    // 3. Immutability in Action
    // Notice that t1 is EXACTLY the same as it was before. 
    // This safety is crucial for Big Data (Spark) processing.
    println(s"Original t1: $t1")  // Transaction(T001,5000.0,pending)
    println(s"New Copy t2: $t2")  // Transaction(T001,5000.0,approved)
    
    // Verify they are different objects
    println(s"Are they the same object? ${t1 == t2}") // False (different status)
  }
}
