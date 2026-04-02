# Log-Based Anomaly Detection - Story Map

## 1. Story (traffic monitor)
A traffic camera expects a steady flow. If cars suddenly drop or pile up, something is wrong.

## 2. Core Concepts (street version)
- Baseline = normal request and error volume.
- Throughput drop = sudden fall in events.
- Error spike = sudden surge in failures.

## 3. Detection Pattern
Compare each time window to baseline thresholds and flag anomalies.

## 4. Final Mental Model
Watch the volume and error rate; big deviations are the signal.

## 5. Run Order
1. c004_log_anomaly_detection_demo.py
