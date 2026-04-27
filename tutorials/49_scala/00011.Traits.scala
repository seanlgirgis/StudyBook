object TraitsExample {
  def main(args: Array[String]): Unit = {
    
    // --- WHAT IS A TRAIT? ---
    // A Trait is like an 'Interface' in Java or an 'Abstract Base Class' in Python.
    // It defines a set of methods (behaviors) that other classes can Share.
    // Use it when you want to say certain classes "CAN DO" something.

    // 1. Define Traits (Capabilities)
    trait Auditable {
      // Any class that extends this MUST define this method
      def auditLog(): String 
    }

    trait JSONSerializable {
      def toJson(): String
    }

    // 2. Use Traits in a Class
    // Here, 'Transaction' is a Case Class that HAS data...
    // BUT it also "Is Auditable" AND "Is JSONSerializable".
    case class Transaction(id: String, amount: Double, status: String) 
      extends Auditable with JSONSerializable {
      
      // Implementing the auditLog behavior
      def auditLog(): String = 
        s"AUDIT: Transaction $id ($status) - Value: $$$amount"
      
      // Implementing the toJson behavior
      def toJson(): String = 
        s"""{"id": "$id", "amount": $amount, "status": "$status"}"""
    }

    // 3. Testing it out
    val t1 = Transaction("T999", 500.0, "approved")

    println(t1.auditLog()) // Prints the audit log
    println(t1.toJson())   // Prints the JSON string
    
    // 4. Polymorphism (Treating different things the same way)
    // Because Transaction "IS" Auditable, we can treat it just as an Auditable thing.
    def logToSecurity(item: Auditable): Unit = {
        println("\n--- Security System ---")
        println(s"Logging: ${item.auditLog()}")
    }

    logToSecurity(t1)
  }
}
