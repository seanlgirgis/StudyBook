# BOA 30 2 5 Minute Forecasting Talk Track

## 30-Second Answer
I built a practical capacity forecasting workflow to turn telemetry trends into early risk visibility for operations and leadership. I used SQL, Python, and Pandas to normalize timestamps, bucket data hourly and daily, compute trend and headroom features, and rank services by near-term capacity risk. The goal was decision support, so teams could act earlier with clear risk language.

## 2-Minute Answer
The core problem was late capacity risk visibility. I built a forecasting workflow around telemetry we already trusted from infrastructure and application monitoring. In the first version, I used SQL extracts and Pandas to clean data, normalize timestamps, bucket by hour and day, and group by host, application, and service.

Then I engineered practical features: rolling averages, rolling peaks, growth slope, headroom to threshold, and breach flags. I used those features to assign risk bands and rank systems by likely near-term risk windows. Output was built for decisions: operations dashboards for daily action, plus concise management summaries showing what was at risk, when, and what action to prioritize.

Validation was disciplined and practical. I ran data quality checks, validated feature math, used time-ordered evaluation, backtested predicted vs actual outcomes, compared against naive baselines, and reviewed results with SMEs to reduce false positives. For scale, I explain the same logic moving from Pandas prototype workflows to PySpark, with Hadoop or cloud data lake storage and scheduled pipeline patterns.

## 5-Minute Deep Buildout Story
If I break it down end to end, I started with telemetry inputs from infrastructure and application layers, plus KPI context and asset metadata. The first step was cleanup and normalization: timestamp format alignment, duplicate handling, missing value checks, and stale record detection. That gave me reliable time-series inputs.

Next I bucketed data into hourly and daily windows so we could separate noise from sustained trend. I grouped by host, application, and service because ownership and action planning happen at those levels. From there I built explainable features: rolling averages for sustained behavior, rolling peaks for stress behavior, growth slope for trajectory, and headroom-to-threshold for operational urgency.

Then I added threshold breach flags and risk bands. This let us move from raw telemetry to ranked risk. Instead of saying only a metric was high, we could say which service was likely to hit a limit soon and which action window mattered first. That ranking fed dashboard and reporting outputs.

Operationally, teams used ranked service views, trend panels, and threshold outlooks. Leadership received concise summaries with assumptions, confidence framing, and recommendation language. The objective was not a research-grade model. The objective was practical, repeatable decision support.

Validation had multiple layers. I checked data quality first: missing timestamps, impossible values, duplicates, stale assets, and bucket integrity. Then I validated feature calculations. For forecast behavior, I used time-ordered testing and backtesting against actual outcomes, and I compared performance against naive baselines. Finally, I reviewed false positives with SMEs so the output stayed trustworthy and actionable.

For scale-up, I present a safe architecture path. Pandas was ideal for fast prototyping and feature iteration. At larger volume, the same logic moves to PySpark for distributed transformation, with Hadoop/HDFS or cloud data lake storage patterns, partitioned time-series datasets, and scheduled ETL. I describe this as an explainable scale pattern and collaborative platform evolution, not solo ownership of every platform layer.

My ownership statement is straightforward: I can clearly explain and defend the forecasting logic, feature design, risk ranking, validation workflow, and reporting outputs. On large platform expansion, I partner with data and platform teams and stay explicit about boundaries.