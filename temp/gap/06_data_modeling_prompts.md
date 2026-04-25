# Data Modeling for Data Engineers — ChatGPT Project Prompts

Priority: 🟠 Important — Toyota gap #6

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Data Modeling for Data Engineers
Slug: data-modeling
Extra coverage required: why data modeling matters — how the wrong model makes every query slow and every report wrong,
star schema — fact tables, dimension tables, foreign keys, denormalization for query performance,
snowflake schema — normalized dimensions, when normalization helps vs hurts analytics,
fact table types — transaction facts, periodic snapshot facts, accumulating snapshot facts,
grain — what it means to define the grain of a fact table, and why getting it wrong is catastrophic,
dimension table design — surrogate keys vs natural keys, conformed dimensions,
Slowly Changing Dimensions — Type 1 overwrite, Type 2 full history with effective dates, Type 3 current+previous only,
SCD Type 2 implementation — surrogate key pattern, is_current flag, valid_from and valid_to dates,
One Big Table — when denormalizing everything into a single wide table is the right call,
dimensional modeling for manufacturing — modeling production line events, machine telemetry, shift data,
data vault — hubs, links, satellites — when it applies vs Kimball,
wide vs narrow models — impact on query performance, storage, and downstream usability,
data modeling for streaming — modeling events vs modeling state,
common mistakes — fact-to-fact joins, missing grain definition, surrogate key misuse,
dbt for data modeling — how dbt implements dimensional models in practice.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug data-modeling -ChunkSize 750
```

Upload final_data-modeling.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_data-modeling.mp3` is live on R2.

```
Topic: Data Modeling for Data Engineers
Slug: data-modeling
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_data-modeling.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\data-modeling.html
