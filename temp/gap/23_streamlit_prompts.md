# Streamlit for Data Engineers — ChatGPT Project Prompts

Priority: 🟡 Useful — used in both Citi and HorizonScale, fast internal tool pattern

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Streamlit for Data Engineers
Slug: streamlit
Extra coverage required: what Streamlit is — Python script that runs top-to-bottom and rerenders on interaction, no HTML/JS needed,
the execution model — every interaction reruns the script, why this is different from a web app,
core display elements — st.write, st.dataframe, st.table, st.metric, st.json — when each is appropriate,
input widgets — st.selectbox, st.multiselect, st.slider, st.text_input, st.date_input — wiring inputs to DataFrame filters,
charts — st.line_chart, st.bar_chart, st.plotly_chart, st.altair_chart — when to use Plotly for custom charts,
st.cache_data — caching expensive database queries and file reads, TTL, cache invalidation,
st.cache_resource — caching database connections and ML models that shouldn't reload on every run,
layout — st.sidebar, st.columns, st.tabs, st.expander — organizing a multi-section dashboard,
st.session_state — persisting state across reruns, implementing multi-step workflows,
filtering patterns — filtering a DataFrame based on sidebar inputs, the standard pattern every DE uses,
displaying forecast results — line charts with confidence bands, plotly go.Figure with fill='tonexty',
st.data_editor — editable DataFrames, accepting user corrections to flagged records,
deploying Streamlit — Streamlit Community Cloud, Docker container on ECS, environment variables for secrets,
security for internal tools — st.secrets, restricting access, not exposing database credentials in the UI,
real scenario: the internal capacity planning dashboard at Citi — month-over-month progression, under-utilization list, near-capacity alerts.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug streamlit -ChunkSize 750
```

Upload final_streamlit.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_streamlit.mp3` is live on R2.

```
Topic: Streamlit for Data Engineers
Slug: streamlit
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_streamlit.mp3
Today's date: 2026-04-25

SCOPE FENCE: 8-10 sections maximum. 2-3 tight paragraphs per section.
One code block per section, 20 lines max. Cheat sheet: 12-15 rows.
Reference page only - no step-by-step tutorials or full worked examples.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\streamlit.html
