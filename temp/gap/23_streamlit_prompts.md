# Streamlit for Data Engineers — ChatGPT Project Prompts

Priority: 🟡 Useful — used in both Citi and HorizonScale, fast internal tool pattern

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Streamlit for Data Engineers
Slug: streamlit

Extra coverage required:
- What Streamlit is — Python script that runs top-to-bottom and rerenders on every user interaction; no HTML/JS required; ideal for internal data tools
- The execution model — every widget interaction reruns the entire script from top; understanding this prevents bugs with side effects and expensive computations
- Core display elements — st.write() (universal), st.dataframe() (interactive table), st.metric() (KPI card), st.json() (nested data); when each is appropriate
- Input widgets — st.selectbox, st.multiselect, st.slider, st.text_input, st.date_input; wiring widget values directly to DataFrame filter conditions
- Charts — st.line_chart and st.bar_chart for quick plots; st.plotly_chart for full Plotly Figure control (annotations, dual axes, confidence bands)
- st.cache_data — cache expensive database queries and file reads; TTL parameter controls staleness; clears automatically when function code changes
- st.cache_resource — cache database connections and ML models that should not reload on every run; singleton pattern for shared resources
- Layout — st.sidebar for persistent filters; st.columns for side-by-side panels; st.tabs for section navigation; st.expander for collapsible detail
- st.session_state — persisting values across reruns; implementing multi-step workflows where earlier inputs must survive later interactions
- The standard filtering pattern — sidebar widgets collect filter values; apply filters to cached DataFrame; display filtered result and row count
- Displaying forecast results — Plotly go.Figure with two traces (actuals + forecast) and fill='tonexty' for confidence bands
- st.data_editor — editable DataFrames for accepting user corrections to flagged records; reading back edits as a DataFrame
- Deploying Streamlit — Streamlit Community Cloud for public apps; Docker container on ECS for internal tools with secrets from environment variables
- Security for internal tools — st.secrets for local secrets management; restricting access at the network or reverse proxy layer; never embedding DB credentials in UI

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. What Streamlit Is & The Execution Model
  2. Core Display Elements
  3. Input Widgets & The Standard Filtering Pattern
  4. Charts — st.line_chart vs Plotly
  5. st.cache_data & st.cache_resource
  6. Layout — sidebar, columns, tabs, expander
  7. st.session_state — persisting state across reruns
  8. st.data_editor — editable DataFrames
  9. Deployment & Security
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\streamlit.html
