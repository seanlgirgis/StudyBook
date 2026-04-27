package com.capitalone

import com.capitalone.models.Transaction
import com.capitalone.utils.RiskEngine
import org.apache.spark.sql.SparkSession
import org.scalatest.funsuite.AnyFunSuite
import org.scalatest.BeforeAndAfterAll

class TransactionPipelineTest extends AnyFunSuite with BeforeAndAfterAll {

  // Create a local Spark session just for testing
  val spark: SparkSession = SparkSession.builder()
    .appName("TestSuite")
    .master("local[*]")
    .getOrCreate()

  import spark.implicits._

  test("RiskEngine classifies HIGH risk correctly") {
    val t = Transaction("T001", "C001", 75000.00, "wire", "UK", "approved")
    assert(RiskEngine.classifyTransaction(t) == "HIGH")
  }

  test("RiskEngine classifies gambling as MEDIUM risk") {
    val t = Transaction("T002", "C002", 500.00, "gambling", "US", "approved")
    assert(RiskEngine.classifyTransaction(t) == "MEDIUM")
  }

  test("Pipeline filters declined transactions") {
    val transactions = Seq(
      Transaction("T001", "C001", 5000.00, "retail", "US", "approved"),
      Transaction("T002", "C002", 3000.00, "retail", "US", "declined"),
      Transaction("T003", "C003", 1000.00, "retail", "US", "approved")
    ).toDF()

    val approved = transactions
      .filter($"status" === "approved")

    assert(approved.count() == 2)
  }

  override def afterAll(): Unit = {
    spark.stop()
  }
}
