import scala.util.{Try, Success, Failure}

object TryChaining {
  def main(args: Array[String]): Unit = {
    
    // --- WHAT IS 'Transaction'? ---
    // In this specific code, we aren't using a 'Transaction' class.
    // We are working with raw data (List of Strings).
    // HOWEVER: Imagine these are "Transaction Amounts" coming from a messy text file.
    // This pipeline cleans them up and processes them in one go.

    // 1. INPUT DATA (Mix of good numbers and garbage)
    val inputs = List("100.0", "200.0", "oops", "400.0", "??")

    // 2. THE PIPELINE
    // Watch how the data transforms step-by-step:
    
    val results = inputs
      
      // Step A: SAFE PARSING
      // "100.0" -> Success(100.0)
      // "oops"  -> Failure(...)
      .map(s => Try(s.toDouble))
      
      // Step B: CLEANING (collect)
      // Throw away Failures, keep only Success values.
      // List(Success(100.0), Failure, ...) -> List(100.0, 200.0, 400.0)
      // Note: This extracts the value *out* of the Success box.
      .collect { case Success(v) => v }
      
      // Step C: FILTERING
      // Keep only amounts greater than 150.0
      // List(100.0, 200.0, 400.0) -> List(200.0, 400.0)
      .filter(v => v > 150.0)
      
      // Step D: TRANSFORMATION
      // Double the value.
      // List(200.0, 400.0) -> List(400.0, 800.0)
      .map(v => v * 2)

    // 3. OUTPUT
    println(results) // List(400.0, 800.0)
  }
}
