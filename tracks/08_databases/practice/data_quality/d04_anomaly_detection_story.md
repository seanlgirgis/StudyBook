# Anomaly Detection Basics - Story Map

## 1. Story (store receipts)
A manager expects daily sales around the usual range. A huge spike triggers a review.

## 2. Core Concepts (street version)
- Baseline = normal expected range.
- Outlier = value far outside the range.
- Detection = flag outliers before dashboards update.

## 3. Failing Case
A revenue spike exceeds the baseline range and fails the check.

## 4. Passing Case
A normal day stays within the range and passes.

## 5. Final Mental Model
Simple baselines are enough to catch obvious anomalies.

## 6. Run Order
1. c005_anomaly_detection_demo.py
