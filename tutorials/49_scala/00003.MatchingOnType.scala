object Example {
	def main(args: Array[String]): Unit = {
        def describe(x: Any): String = x match {
        case i: Int     => s"Integer: $i"
        case s: String  => s"String: $s"
        case d: Double  => s"Double: $d"
        case b: Boolean => s"Boolean: $b"
        case _          => "Unknown type"
        }

        println(describe(42))       // Integer: 42
        println(describe("Scala"))  // String: Scala
        println(describe(3.14))     // Double: 3.14
        println(describe(true))     // Boolean: true
    }
}