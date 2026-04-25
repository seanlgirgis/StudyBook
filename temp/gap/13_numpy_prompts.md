# NumPy — ChatGPT Project Prompts

Priority: 🟠 Important — underpins Pandas, scikit-learn, and all numerical computing

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: NumPy for Data Engineers
Slug: numpy

Extra coverage required:
- ndarray — contiguous block of typed memory in C; why it's 10–100x faster than a Python list for numerical operations
- dtypes — float32 vs float64, int32 vs int64; choosing the right dtype cuts memory in half; uint8 for percentages, float32 for ML features
- Array creation — np.zeros, np.ones, np.arange, np.linspace, np.random.default_rng(); when each is used in pipeline code
- Indexing and slicing — 1D, 2D, and 3D arrays; boolean indexing to filter rows; fancy indexing with integer arrays
- Broadcasting — the rules that allow operations between arrays of different shapes; shape (N,) vs (N,1) vs (1,N) and what each does
- Vectorized operations — np.sum, np.mean, np.std applied to the whole array in C; why replacing a Python loop with a ufunc matters at 65K rows
- Universal functions (ufuncs) — np.add, np.multiply, np.exp, np.log; element-wise operations with broadcasting support
- np.where — vectorized conditional: np.where(condition, value_if_true, value_if_false); replaces apply for simple conditionals
- Aggregation along axes — axis=0 (collapse rows, result per column), axis=1 (collapse columns, result per row); the axis parameter explained clearly
- Reshaping — reshape, flatten, ravel, transpose; when each is appropriate; the difference between a view and a copy
- np.percentile and np.nanpercentile — calculating P95 across 65,000 rows; why nanpercentile is required when nulls exist
- NumPy and Pandas — Pandas is built on NumPy; .to_numpy() returns the underlying array; when to drop to NumPy for speed-critical calculations

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug numpy -ChunkSize 750
```

Upload final_numpy.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_numpy.mp3` is live on R2.

```
Topic: NumPy for Data Engineers
Slug: numpy
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_numpy.mp3
Today's date: 2026-04-25

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. ndarray & Why It's Fast
  2. dtypes — choosing the right type
  3. Array Creation & Indexing
  4. Broadcasting — the rules
  5. Vectorized Ops & ufuncs
  6. np.where & Conditionals
  7. Aggregation Along Axes
  8. Reshaping, np.percentile & Pipeline Use Cases
  9. NumPy & Pandas — when to drop down
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\numpy.html
