object RegularClass {
  def main(args: Array[String]): Unit = {
    
    // 1. DATA: Defined as a 'case class'
    // 'Transaction' is just the data container (ID, Amount, Status).
    // It captures "What something IS".
    case class Transaction(id: String, amount: Double, status: String)

    // 2. BEHAVIOR: Defined as a 'regular class'
    // 'TransactionProcessor' contains the Logic/Code to DO things.
    // It captures "What we DO with the data".
    // 'threshold' is a constructor parameter specific to this instance of the processor.
    class TransactionProcessor(threshold: Double) {
      
      // Method to check if risk logic applies
      def isHighRisk(t: Transaction): Boolean = {
        t.amount > threshold
      }
      
      // Main method to process the transaction
      def process(t: Transaction): String = {
        if (isHighRisk(t)) 
          s"${t.id} flagged for review" 
        else 
          s"${t.id} processed normally"
      }
    }

    // 3. USING THEM TOGETHER
    
    // Initialize the Processor logic
    // KEY DIFFERENCE: We use 'new' for regular classes.
    // This creates an instance of the class with a threshold of 10,000.
    val processor = new TransactionProcessor(10000.00)

    // Create some Data
    // No 'new' needed for case classes.
    val t1 = Transaction("T001", 15000.00, "approved")
    val t2 = Transaction("T002", 500.00,   "approved")

    // Apply Logic to Data
    println(processor.process(t1))  // Output: T001 flagged for review
    println(processor.process(t2))  // Output: T002 processed normally
  }
}
