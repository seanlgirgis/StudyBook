object OptionMethods {
  def main(args: Array[String]): Unit = {
    
    // --- WHAT IS 'Transaction'? ---
    // You asked: "What the word Transaction mean" inside this context.
    // In this specific code, we are just looking at raw Double values (Salaries).
    // BUT, this is exactly how you handle optional fields in a Transaction.
    // Example: case class Transaction(id: String, amount: Double, referralCode: Option[String])
    // The 'referralCode' might be Some("REF123") or None.
    
    // 1. SETUP
    val salary: Option[Double] = Some(95000.00) // A value exists
    val noSalary: Option[Double] = None         // Missing value

    // 2. getOrElse (The Safety Net)
    // "Give me the value, OR give me this default if it's missing."
    // This prevents crashes.
    println(s"Salary: ${salary.getOrElse(0.0)}")       // Output: 95000.0
    println(s"No Salary: ${noSalary.getOrElse(0.0)}")  // Output: 0.0

    // 3. map (Safe Transformation)
    // "If there is a value, apply this math. If None, do nothing."
    // This is powerful because you don't need 'if (x != null)' checks.
    
    val bonus = salary.map(s => s * 0.10)
    println(s"Bonus: $bonus")  // Output: Some(9500.0)

    val noBonus = noSalary.map(s => s * 0.10)
    println(s"No Bonus: $noBonus")  // Output: None (It didn't crash!)

    // 4. Checking status (Boolean)
    println(s"Is salary defined? ${salary.isDefined}") // true
    println(s"Is noSalary empty? ${noSalary.isEmpty}") // true
  }
}
