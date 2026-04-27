object ClassesWithMethods {
  def main(args: Array[String]): Unit = {
    
    // 1. Case Class with a Method
    // Even though it's just data, you CAN add logic!
    case class Transaction(id: String, amount: Double) {
        
        // A method to calculate tax
        def tax(): Double = amount * 0.10
        
        // A method to print a receipt
        def printReceipt(): Unit = {
            println(s"Receipt for transaction $id")
            println(s"Subtotal: $$${amount}")
            println(s"Tax:      $$${tax()}")
            println(s"Total:    $$${amount + tax()}")
            println("-------------------")
        }
    }

    val t1 = Transaction("T100", 200.0)
    println("--- Case Class Method ---")
    t1.printReceipt() // Calling the method defined inside


    // 2. Regular Class (The "Java Style")
    // Use 'class' (no 'case') when you want Mutable state and behavior.
    class BankAccount(initialBalance: Double) {
        // 'private var' means only this class can change it
        private var balance: Double = initialBalance

        def deposit(amount: Double): Unit = {
            balance += amount
            println(s"Deposited $$${amount}. New Balance: $$${balance}")
        }

        def withdraw(amount: Double): Unit = {
            if (amount <= balance) {
                balance -= amount
                println(s"Withdrew $$${amount}. New Balance: $$${balance}")
            } else {
                println(s"Insufficient funds to withdraw $$${amount}")
            }
        }
    }

    println("\n--- Regular Class Method ---")
    val myAccount = new BankAccount(100.0) // Note: 'new' keyword is usually used for regular classes
    myAccount.deposit(50.0)
    myAccount.withdraw(30.0)
  }
}
