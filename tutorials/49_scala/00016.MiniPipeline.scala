object MiniPipeline {
  def main(args: Array[String]): Unit = {
    
    // 1. DATA MODEL (The "Schema")
    // Q: What does 'Transaction' mean here?
    // A: It represents the SHAPE of your data. 
    //    In a big data pipeline, this would map to a row in a database or a line in a CSV.
    //    It holds 4 pieces of information immutably.
    case class Transaction(
      id: String, 
      amount: Double, 
      category: String, 
      country: String
    )

    // 2. PROCESSOR (The "Logic")
    // This regular class holds the *rules* for processing data.
    // It takes a 'threshold' as a setting (constructor argument).
    class RiskEngine(highAmountThreshold: Double) {

      // Determine risk based on patterns
      def classify(t: Transaction): String = t match {
        
        // High Risk: Amount > Threshold AND Foreign Country
        case Transaction(_, amount, _, country) 
          if amount > highAmountThreshold && country != "US" =>
            "HIGH RISK"
        
        // Medium Risk: Gambling category
        case Transaction(_, _, "gambling", _) =>
            "MEDIUM RISK"
        
        // Low Risk: Any other foreign transaction
        case Transaction(_, _, _, country) if country != "US" =>
            "LOW RISK"
        
        // Normal: Everything else
        case _ => 
            "NORMAL"
      }

      // Batch Processing Method
      // Takes a List of Transactions -> Returns a List of Strings (Reports)
      def processAll(transactions: List[Transaction]): List[String] = {
        // .map transforms every transaction 't' into a String report
        transactions.map(t => s"${t.id}: ${classify(t)}")
      }
    }

    // 3. EXECUTION (Running the Pipeline)
    
    // Create the input data (Batch of transactions)
    val transactions = List(
      Transaction("T001", 75000.00, "wire",     "UK"),
      Transaction("T002", 500.00,   "gambling", "US"),
      Transaction("T003", 1200.00,  "retail",   "CA"),
      Transaction("T004", 45.00,    "grocery",  "US")
    )

    // Initialize the Engine with a $50,000 threshold
    val engine = new RiskEngine(50000.00)

    // Run the processor and print results
    println("--- Risk Report ---")
    engine.processAll(transactions).foreach(println)
  }
}
