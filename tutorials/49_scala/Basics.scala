object Basics {
  def main(args: Array[String]): Unit = {
    // 1. Variables: val (immutable) vs var (mutable)
    val name = "Data Engineer" // Immutable, preferred in Scala
    var age = 25              // Mutable
    age = 26                  // Allowed
    // name = "Architect"     // Error: Reassignment to val
    println(s"1. Variables: Name is $name (fixed), Age became $age")

    // 2. Functions & Type Inference
    def greet(n: String): String = s"Hello, $n"
    println("\n2. Functions: " + greet("Future Scala Expert"))

    // 3. Collections (Lists are immutable by default)
    val fruits = List("apple", "banana", "cherry")
    println(s"\n3. Collections: My fruit list: $fruits")

    // 4. Higher-Order Functions (Map, Filter)
    val nums = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    
    // Pipeline: Filter evens -> Multiply by 10 -> Sum them up
    val result = nums
      .filter(_ % 2 == 0)   // Keep evens (2, 4, 6...)
      .map(_ * 10)          // Multiply by 10 (20, 40, 60...)
      .reduce(_ + _)        // Sum (300)

    println(s"\n4. Pipeline Result (Sum of evens * 10): $result")

    // 5. Maps (Key-Value)
    val skills = Map("Java" -> "Intermediate", "Scala" -> "Beginner")
    println(s"\n5. Maps: Current Scala Level: ${skills("Scala")}")
  }
}
