object Example {
  def main(args: Array[String]): Unit = {
    val words = List("spark", "scala", "kafka", "hadoop", "hive")

    val result = words
      .filter(w => w.length > 4)
      .map(w => w.toUpperCase)

    println(result)
  }
}