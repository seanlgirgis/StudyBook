object TraitsImplementation {
  def main(args: Array[String]): Unit = {
    
    // 1. Define Traits (Capabilities)
    // A trait defines a "contract" of behavior.
    trait Auditable {
      def auditLog(): String // Abstract method (no body)
    }

    trait Serializable {
      def toJson(): String   // Abstract method
    }

    // 2. Define the Case Class 'Transaction'
    // Q: What does 'Transaction' mean here?
    // A: It is a Data Container (Case Class) that holds id, amount, and status.
    //    BUT, by using 'extends', we are saying:
    //    "This Transaction IS AUDITABLE and IS SERIALIZABLE".
    //    It *must* provide the code for auditLog() and toJson().
    case class Transaction(id: String, amount: Double, status: String) 
      extends Auditable with Serializable {
      
      // Implementing the behavior required by 'Auditable'
      def auditLog(): String = 
        s"Transaction $id for $$$amount was $status"
      
      // Implementing the behavior required by 'Serializable'
      def toJson(): String = 
        s"""{"id":"$id","amount":$amount,"status":"$status"}"""
    }

    // 3. Using it
    val t1 = Transaction("T001", 5000.00, "approved")
    
    println(t1.auditLog())  // Output: Transaction T001 for $5000.0 was approved
    println(t1.toJson())    // Output: {"id":"T001","amount":5000.0,"status":"approved"}
  }
}
