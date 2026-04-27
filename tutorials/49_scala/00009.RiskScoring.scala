object RiskScoring {
  def main(args: Array[String]): Unit = {
    
    // 1. Define the Data Structure
    // 'Transaction' here is a Case Class. 
    // It represents a specific event with 4 fields: ID, Amount, Category, Country.
    case class Transaction(id: String, amount: Double, category: String, country: String)

    // 2. Define the Business Logic
    // This function takes a transaction 't' and returns a risk label.
    def riskScore(t: Transaction): String = t match {
      
      // Case 1: High Risk
      // Pattern: Any ID (_), Any Category (_), but capture 'amount' and 'country'.
      // Guard (if): Amount is over 50k AND Country is NOT "US".
      case Transaction(_, amount, _, country) if amount > 50000 && country != "US" =>
        "HIGH RISK — large foreign transaction"
        
      // Case 2: Medium Risk
      // Pattern: Specific category "gambling".
      // Guard: Amount is over 1000.
      case Transaction(_, amount, "gambling", _) if amount > 1000 =>
        "MEDIUM RISK — large gambling transaction"
        
      // Case 3: Low Risk
      // Pattern: Any transaction where country is NOT "US" (and didn't match Case 1).
      case Transaction(_, _, _, country) if country != "US" =>
        "LOW RISK — foreign transaction"
        
      // Case 4: Everything Else
      // Catches normal, domestic, low-value transactions.
      case _ => 
        "NORMAL"
    }

    // 3. Test Cases
    val t1 = Transaction("T001", 60000, "Equipment", "UK")      // High Amount + Foreign
    val t2 = Transaction("T002", 5000, "gambling", "US")        // Gambling + >1000
    val t3 = Transaction("T003", 50, "Souvenir", "France")      // Small Foreign
    val t4 = Transaction("T004", 150, "Groceries", "US")        // Standard

    println(s"T1 (${t1.amount}, ${t1.country}): ${riskScore(t1)}")
    println(s"T2 (${t2.category}, ${t2.amount}):   ${riskScore(t2)}")
    println(s"T3 (${t3.country}):         ${riskScore(t3)}")
    println(s"T4 (Domestic):        ${riskScore(t4)}")
  }
}
