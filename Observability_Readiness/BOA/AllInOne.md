




## 1.0 Walk me through how you built the capacity forecasting workflow.
Initially, a lot of the capacity forecast reporting relied on Excel-based
CBFR reports and BMC TrueSight capacity data. That worked, but it was not
efficient or repeatable enough as the reporting demand grew.

We already had a monthly capacity data pipeline, so the next step was to
evolve it into a more telemetry-focused forecasting workflow for the
applications and servers of interest.

The process started with telemetry extraction. We used extraction scripts,
including PL/SQL, to pull monthly capacity data from a mirror Oracle
database for BMC TrueSight. We also interfaced with CMDB data to bring in
application-related fields and ownership context.

Then I cleaned and normalized the data so joins were reliable and the time
series could be bucketed properly. That included timestamp normalization,
hourly and daily buckets, and grouping by host, application, and service.

After that, I engineered capacity features such as rolling averages,
rolling peaks, P95 values where useful, headroom to threshold, breach flags,
risk bands, and growth slope.

For forecasting, I used a time-based validation pattern. Train on an older
history window, such as 18 months, test against a more recent holdout window,
such as 6 months, compare forecasted values or risk bands against actual
outcomes, and adjust only when the backtest showed a real need.

Once the forecast looked reasonable, we used the full history to forecast
the next 3 to 6 month planning window.

The final output was not just a model. It became exception lists,
management summaries, dashboards, and CBFR-style planning outputs that
helped teams understand which applications or servers needed attention.


### Spine
1. Start with telemetry extraction.
2. Clean and normalize the data.
3. Bucket by time: hourly / daily.
4. Group by host, application, service.
5. Engineer capacity features.
6. Forecast and validate.
7. Publish dashboards, exception lists, and management summaries.

### Memory Line
It started as Excel/CBFR and TrueSight reporting, then evolved into a
repeatable telemetry pipeline with forecasting, validation, exception
lists, dashboards, and planning summaries.


## 1.0 Walk me through how you built the capacity forecasting workflow.