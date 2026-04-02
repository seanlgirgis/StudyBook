# Dashboards and Alerting Patterns - Story Map

## 1. Story (control room)
A control room shows key gauges on a wall. Alarms ring only when a gauge crosses a limit.

## 2. Core Concepts (street version)
- Dashboard = summary of key signals.
- Alert = trigger when a threshold or spike happens.
- Signal = latency, error rate, backlog, etc.

## 3. Dashboard View
Aggregate metrics like total events, error count, and average latency.

## 4. Alert Patterns
Threshold alerts (error count) and spike alerts (latency spikes).

## 5. Final Mental Model
Dashboards show the state; alerts wake you up when it changes.

## 6. Run Order
1. c003_dashboards_alerts_demo.py
