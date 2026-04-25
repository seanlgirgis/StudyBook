# Data Modeling for Data Engineers — ChatGPT Project Prompts

Priority: 🟠 Important — Toyota gap #6

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Data Modeling for Data Engineers
Slug: data-modeling

Extra coverage required:
- Why data modeling matters — the wrong model makes every query slow and every report wrong; it is not a cosmetic choice
- Star schema — fact tables, dimension tables, foreign keys; why denormalization exists and what it trades
- Snowflake schema — normalized dimensions; when the extra joins are worth the storage savings
- Fact table types — transaction facts (one row per event), periodic snapshot (one row per period), accumulating snapshot (one row per process lifecycle)
- Grain — defining the grain of a fact table is the single most important decision; getting it wrong breaks downstream reports permanently
- Dimension design — surrogate keys vs natural keys; conformed dimensions shared across fact tables
- Slowly Changing Dimensions — Type 1 (overwrite, no history), Type 2 (new row per change with valid_from/valid_to), Type 3 (current and previous columns only)
- SCD Type 2 implementation — surrogate key pattern, is_current flag, MERGE statement to detect changes
- One Big Table — when fully denormalizing into a single wide table is the right call; the query performance vs flexibility tradeoff
- Data vault — hubs (unique business keys), links (relationships), satellites (descriptive attributes); when it applies vs Kimball star schema
- Modeling for streaming — events vs state; append-only event tables vs mutable state tables
- Common mistakes — fact-to-fact joins (always wrong), missing grain definition, surrogate key misuse, late-arriving dimensions

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. Why Data Modeling Matters
  2. Star Schema — facts, dimensions, grain
  3. Snowflake Schema — when normalization helps
  4. Fact Table Types — transaction, snapshot, accumulating
  5. Dimension Design — surrogate keys, conformed dimensions
  6. Slowly Changing Dimensions (Type 1, 2, 3)
  7. One Big Table vs Normalized
  8. Data Vault — hubs, links, satellites
  9. Streaming & Event Modeling — events vs state
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\data-modeling.html
