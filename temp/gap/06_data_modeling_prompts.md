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

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
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

SCOPE FENCE: 8-10 sections maximum. 2-3 tight paragraphs per section.
One code block per section, 20 lines max. Cheat sheet: 12-15 rows.
Reference page only - no step-by-step tutorials or full worked examples.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\data-modeling.html
