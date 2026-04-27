package com.capitalone.utils

import com.capitalone.models.Transaction
import org.apache.spark.sql.functions.udf

object RiskEngine {

  // Reusable risk scoring UDF
  val riskScoreUDF = udf((amount: Double, country: String, category: String) => {
    (amount, country, category) match {
      case (a, c, _) if a > 50000 && c != "US" => "HIGH"
      case (_, _, cat) if cat == "gambling"     => "MEDIUM"
      case (a, _, _)  if a > 10000              => "MEDIUM"
      case _                                     => "LOW"
    }
  })

  // Pure Scala function — no Spark needed
  def classifyTransaction(t: Transaction): String = t match {
    case Transaction(_, _, a, _, c, _) if a > 50000 && c != "US" => "HIGH"
    case Transaction(_, _, _, "gambling", _, _)                   => "MEDIUM"
    case Transaction(_, _, a, _, _, _) if a > 10000               => "MEDIUM"
    case _                                                         => "LOW"
  }
}
