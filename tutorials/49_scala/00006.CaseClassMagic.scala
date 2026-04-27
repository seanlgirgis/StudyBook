object CaseClassMagic {
  def main(args: Array[String]): Unit = {
    
    // YES! This single line IS the full definition.
    // Scala writes the rest of the code for you in the background.
    case class Transaction(id: String, amount: Double, status: String)

    val t1 = Transaction("T001", 5000.0, "approved")
    val t2 = Transaction("T001", 5000.0, "approved")

    // Feature 1: You didn't write a constructor, but it works! (No 'new' keyword needed)
    println(s"1. Auto-toString: $t1") 
    // Output: Transaction(T001,5000.0,approved) -> It prints nicely automatically.

    // Feature 2: All parameters are automatically public 'val's (you can read them)
    println(s"2. Public Fields: ID is ${t1.id}, Amount is ${t1.amount}")

    // Feature 3: Auto-Equality (Compares DATA, not memory address)
    // In Java, t1 == t2 would be false (different objects).
    // In Scala Case Classes, it is TRUE because the data is the same.
    println(s"3. Auto-Equality: Are t1 and t2 equal? ${t1 == t2}")

    // Feature 4: The 'copy' method
    // You can't change t1.amount (it's immutable), but you can copy it with a change.
    val t3 = t1.copy(amount = 9000.0)
    println(s"4. Copy Method: Old: $t1, New: $t3")
  }
}
