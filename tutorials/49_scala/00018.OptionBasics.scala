object OptionBasics {
  def main(args: Array[String]): Unit = {
    
    // --- WHAT IS 'Transaction'? ---
    // You asked "What the word Transaction mean?"
    // In this specific code, we are looking up 'Employees', not Transactions.
    // However, the concept is IDENTICAL.
    // If you were looking for a Transaction by ID (e.g., "T001"), 
    // it might not exist. So you would return Option[Transaction].
    
    // 1. THE FUNCTION
    // Instead of returning null (which causes crashes), return Option.
    // Option has two forms:
    // - Some(value) -> Data exists
    // - None        -> Data is missing
    def findEmployee(id: String, db: Map[String, String]): Option[String] = {
      db.get(id)  // This automatically returns Some(value) or None
    }

    // 2. THE DATA
    val database = Map(
      "E001" -> "Alice",
      "E002" -> "Bob",
      "E003" -> "Carol"
    )

    // 3. TESTING
    val result1 = findEmployee("E001", database)
    val result2 = findEmployee("E999", database)
    
    println(s"Result 1 is: $result1") // Some(Alice)
    println(s"Result 2 is: $result2") // None

    // 4. PATTERN MATCHING ON OPTION
    // This is the safest way to extract the value.
    // You must handle both cases (Some and None).
    
    println("\n--- Checking Result 1 ---")
    result1 match {
      case Some(name) => println(s"Found employee: $name")
      case None       => println("Employee not found")
    }
    // Output: Found employee: Alice

    println("\n--- Checking Result 2 ---")
    result2 match {
      case Some(name) => println(s"Found employee: $name")
      case None       => println("Employee not found")
    }
    // Output: Employee not found
  }
}
