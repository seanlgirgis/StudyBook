object EmployeePipeline {
  def main(args: Array[String]): Unit = {
    
    // 1. DATA MODEL
    // In this file, 'Employee' is the Case Class (Data Container).
    // (Note: You asked "What does Transaction mean?" - In this code, 
    //  we are using 'Employee' instead of Transaction, but it serves the 
    //  exact same purpose: holding immutable data rows).
    case class Employee(name: String, role: String, salary: Double)

    // 2. INPUT DATA
    val employees = List(
      Employee("Alice", "Engineer",  95000.00),
      Employee("Bob",   "Manager",   120000.00),
      Employee("Carol", "Engineer",  98000.00),
      Employee("Dave",  "Analyst",   75000.00)
    )

    // 3. THE PIPELINE (Functional Programming!)
    // This is a classic "Chain" of operations.
    // Read it top-to-bottom:
    val result = employees
      
      // Step A: FILTER
      // Keep only objects where role is "Engineer".
      // Input: 4 Employees -> Output: 2 Employees (Alice, Carol)
      .filter(e => e.role == "Engineer")
      
      // Step B: MAP (Transform Data)
      // Give them a raise!
      // We use .copy() to create a NEW Employee object with higher salary.
      // Input: 2 Employees -> Output: 2 NEW Employees (with 10% raise)
      .map(e => e.copy(salary = e.salary * 1.10))
      
      // Step C: MAP (Transform to String)
      // Convert the objects into readable Strings for printing.
      // Input: 2 Employees -> Output: 2 Strings
      .map(e => f"${e.name}: $$${e.salary}%.2f")

    // 4. OUTPUT
    // Loop through the final List of Strings and print them.
    result.foreach(println)
  }
}
