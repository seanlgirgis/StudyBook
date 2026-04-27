# Splunk vs Elasticsearch - Story Map

## 1. Story (two toolkits)
Two teams solve the same observability problem with different toolkits.

## 2. Core Concepts (street version)
- Splunk = event indexing + SPL pipeline queries.
- Elasticsearch = document index + DSL queries.

## 3. Ingestion & Indexing
Splunk uses forwarders/HEC into indexes; Elastic uses Beats/Logstash into indices.

## 4. Query Language
Splunk uses SPL; Elastic uses DSL with aggregations.

## 5. Storage Model
Splunk organizes buckets by time; Elastic uses indices/data streams with tiers.

## 6. Final Mental Model
Different stacks, similar goals: search, monitoring, and analytics.

## 7. Run Order
1. c005_splunk_vs_elastic_demo.py
