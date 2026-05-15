# BOA Friday Capacity Interview Plan

## Priority Context
- Interview: Friday, 12:30 PM Central.
- Primary lane: Horizon Scale Forecasting Story.
- Focus: Capacity forecasting buildout from Pandas prototype to
  PySpark/Hadoop/cloud scale patterns.


## Informal BOA Team Signal
Use as emphasis, not as confirmed role scope.

- Capacity Baseline Forecast Report (CBFR) / quarterly forecast reporting.
- Production critical applications and clusters.
- BMC TrueSight / TSCO are strong alignment points.
- Helix awareness may help, but do not overclaim.
- Excel forecasting may still exist; Python/Pandas repeatability is valuable.
- Dashboarding is important; Power BI and Tableau are useful language.
- Performance testing / UCL / BreakPoint-style TPS feeds may inform capacity limits.
- Safety factors matter; do not forecast right up to hard limits.
- Project assessment may ask whether new volume can be absorbed or whether
  horizontal / vertical scaling is needed.
- AWS/Kubernetes capacity monitoring is useful as secondary awareness.
- Team may need a technical person who can support and extend the process.

Safe emphasis:
- Meet the team where they are.
- Respect Excel/reporting workflows.
- Show how to improve repeatability, validation, dashboarding, and forecasting.
- Keep the core story on production capacity planning and decision support.


## What To Rehearse First
1. 30-second project summary in spoken language.
2. 2-minute build flow from telemetry input to management decision support.
3. 5-minute deep buildout: features, risk scoring, validation, and scale path.
4. Ownership-safe answers: what Sean built directly vs where platform
   collaboration applies.
5. Whiteboard flow from timestamp normalization to risk ranking and dashboards.
6. Review Prophet validation and holdout-testing Q&A only after the
   30-second, 2-minute, and 5-minute stories are stable.

## What Not To Study Now
- Deep OpenTelemetry collector internals.
- Kubernetes cluster operations details.
- GPU monitoring deep dive.
- Terraform/CloudFormation implementation detail.
- Prometheus/Grafana advanced configuration.

These can be supporting examples only if asked.

## FinOps bridge, only if asked
- Do not lead with FinOps.
- Use this bridge only if asked about finance, cost, budgets, management,
  planning, or stakeholder communication.
- Connect it back to capacity forecasting outputs: trend, headroom, risk,
  ownership, and action timing.

## Top Risks To Control
- Overclaiming deep ML/research model ownership.
- Overclaiming full Hadoop or cloud platform build ownership.
- Drifting into side-tool stories instead of capacity forecasting.
- Giving theoretical answers without operational decision context.
- Using precision metrics not backed by known facts.

## Truth Anchors To Repeat
- Enterprise capacity and APM background across large environments.
- Telemetry workflows across 6,000+ infrastructure endpoints.
- Practical forecasting for risk visibility, KPI reporting, and executive
  summaries.
- Strong Python/SQL/Pandas/PySpark operator workflow understanding.

## Friday Rehearsal Sequence
1. Say the 30-second answer out loud five times.
2. Run the 2-minute answer with a timer and remove extra wording.
3. Walk the 5-minute story at whiteboard pace.
4. Practice 12 likely BOA questions with safe/unsafe contrast.
5. End with one-minute ownership statement and collaboration statement.

## Final Pre-Interview Checklist
- Can explain end-to-end build flow without notes.
- Can define each major feature: rolling average, rolling peak, growth slope,
  headroom, breach flag, risk band.
- Can explain data quality and validation steps in order.
- Can explain backtesting predicted vs actual and simple baseline comparison.
- Can explain Pandas-to-PySpark/Hadoop/cloud scale-up as architecture path,
  not hype.
- Can describe dashboard and executive reporting outputs.
- Can state personal ownership clearly and avoid overclaiming.
- Can redirect side topics back to capacity decision support.

- Can explain UCL/BreakPoint/TPS project assessment: baseline, threshold,
  safety factor, capacity pool, and horizontal/vertical scaling decision.
