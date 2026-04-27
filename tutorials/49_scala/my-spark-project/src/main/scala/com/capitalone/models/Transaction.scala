package com.capitalone.models

case class Transaction(
  id:         String,
  customerId: String,
  amount:     Double,
  category:   String,
  country:    String,
  status:     String
)

case class Customer(
  id:   String,
  name: String,
  tier: String
)
