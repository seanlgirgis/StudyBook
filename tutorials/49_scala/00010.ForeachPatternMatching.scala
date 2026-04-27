object ForeachPatternMatching {
  def main(args: Array[String]): Unit = {
    
    // 1. Setup the data
    val numbers = List(1, 2, 3, 4, 5)

    // 2. The Loop
    // 'foreach' is a method on the List.
    // It takes a function (a block of code) and runs it for EVERY item 'n'.
    numbers.foreach { n =>
      
      // 3. Pattern Matching as an Expression
      // Here, 'match' returns a value (a String) which gets stored in 'label'.
      val label = n match {
        case 1 => "one"              // Basic match: if n is 1
        case 2 => "two"              // Basic match: if n is 2
        case n if n % 2 == 0 => "even" // Guard: matches any other even number (4, 6...)
        case _ => "odd"              // Default: matches anything else (3, 5...)
      }

      // 4. String Interpolation
      // Prints the number 'n' and the 'label' describing it.
      println(s"$n is $label")
    }

    // --- NOTE ON "Transaction" ---
    // You asked: "What the word Transaction mean?"
    // Answer: In THIS specific file, the word 'Transaction' does NOT appear.
    // It is not used here.
    // We are just matching simple Integers (Int) against rules.
    // However, the *Technique* (Pattern Matching) is exactly the same tool 
    // we would use to analyze a Transaction object.
  }
}
