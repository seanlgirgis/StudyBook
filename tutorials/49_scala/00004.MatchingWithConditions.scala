object Example {
	def main(args: Array[String]): Unit = {
        def classify(score: Int): String = score match {
            case s if s >= 90 => "A"
            case s if s >= 80 => "B"
            case s if s >= 70 => "C"
            case s if s >= 60 => "D"
            case _            => "F"
            }

        println(classify(95))  // A
        println(classify(72))  // C
        println(classify(45))  // F
    }
}