# Course 11 Navigation Repair Audit

## What Was Wrong
- Home page acted mostly as links, not a full review cockpit.
- Linked review topics were not all visibly present on the home page.
- QA and Motherload lacked stable anchors for direct section jumps.

## What Was Fixed
- Course 11 `index.html` redesigned as review cockpit with visible sections and anchor ids.
- Required top navigation links added.
- QA HTML anchor ids added for deep-link sections.
- Motherload HTML anchor ids added and table of contents added.
- Review plan updated with cockpit note and raw URL examples.

## Anchors Added To Course 11 Home
course-status, review-path, mental-model, spark-entry, reading-and-schemas,
dataframe-operations, joins-unions-udfs, rdds-spark-sql, aggregations-scale,
production-support, safe-claims, deep-reference.

## Anchors Added To QA HTML
production-support-mindset, orchestration-and-internals-touchpoints,
dataframes-and-basic-analytics, rdds-and-spark-foundations,
spark-sql-and-temporary-views, aggregations-and-summary-metrics,
pyspark-at-scale-and-optimization, course-11-final-review.

## Anchors Added To Motherload HTML
pyspark-mental-model, sparksession, dataframe-basics, schemas,
dataframe-operations, udfs, rdds-vs-dataframes, spark-sql, aggregations,
pyspark-at-scale, production-support, final-summary.

## Final Course 11 Review Cockpit Path
- study_pages/11_intro_pyspark/index.html

## Remaining Known Issues
- Local PySpark runnable labs are still deferred until environment cleanup.
