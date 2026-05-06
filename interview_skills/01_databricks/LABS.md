# Databricks Labs

## Lab 1: Delta Basics
1. Create a small DataFrame in a notebook.
2. Write to a Delta table using overwrite.
3. Append a new row set.
4. Query with SQL and verify row counts.

## Lab 2: Data Quality Checks
1. Load sample records with nulls and duplicates.
2. Check required fields and uniqueness.
3. Quarantine bad records.
4. Publish clean records to a Silver-style table.

## Lab 3: Entity Resolution Mini Demo
1. Build sample duplicate-ish customer records.
2. Normalize names and emails.
3. Build match keys and similarity score.
4. Deduplicate based on threshold.
5. Save outputs and quality summary.

## Lab 4: Simple Workflow
1. Create two notebook tasks.
2. Task A prepares data.
3. Task B validates and writes Delta output.
4. Configure workflow dependency and retry.
