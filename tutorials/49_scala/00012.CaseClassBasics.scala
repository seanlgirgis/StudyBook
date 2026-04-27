object CaseClassBasics {
  def main(args: Array[String]): Unit = {
    
    // --- WHAT IS 'Transaction'? ---
    // Here, 'Transaction' is a Case Class.
    // It is a blueprint for holding data.
    // Unlike a regular Java class, you don't need to write getters, setters, or constructors.
    case class Transaction(id: String, amount: Double, status: String)

    // 1. Creating Instances
    // Notice: No 'new' keyword is needed! 
    // This makes the code cleaner and easier to read.
    val t1 = Transaction("T001", 5000.00, "approved")
    val t2 = Transaction("T002", 15000.00, "flagged")

    // 2. Accessing Fields
    // You can access fields directly using the dot notation.
    // These fields are immutable (read-only) by default.
    println(s"ID: ${t1.id}")         // Output: T001
    println(s"Amount: ${t1.amount}") // Output: 5000.0
    println(s"Status: ${t1.status}") // Output: approved

    // 3. Automatic toString
    // When you print the object, Scala automatically formats it nicely.
    // You don't see a memory address (like 'Transaction@1a2b3c').
    // Instead, you see the actual data inside.
    println(s"Full Object: $t1")  // Output: Transaction(T001,5000.0,approved)
  }
}
