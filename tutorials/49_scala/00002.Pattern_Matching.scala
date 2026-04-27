object Example {
	def main(args: Array[String]): Unit = {
		val day = "Monday"
		val result = day match {
			case "Monday"  => "Start of the work week"
			case "Friday"  => "Almost weekend!"
			case "Sunday"  => "Rest day"
			case _         => "Just another day"  // default — like else
		}
		println(result)  // Start of the work week
	}
}