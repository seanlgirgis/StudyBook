# NumPy — ChatGPT Project Prompts

Priority: 🟠 Important — underpins Pandas, scikit-learn, and all numerical computing

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: NumPy for Data Engineers
Slug: numpy
Extra coverage required: ndarray — the core object, why it's faster than a Python list (contiguous memory, fixed dtype, C implementation),
dtypes — float32 vs float64 vs int32 vs int64 — choosing the right dtype for memory and performance,
array creation — zeros, ones, arange, linspace, random — when each is used,
indexing and slicing — 1D, 2D, and 3D arrays, boolean indexing, fancy indexing,
broadcasting — the rules that allow operations between arrays of different shapes, practical examples,
vectorized operations — why numpy.sum(arr) is 100x faster than sum(arr) for large arrays,
universal functions (ufuncs) — the underlying mechanism, np.add, np.multiply, np.where,
np.where — the vectorized conditional, replacing apply with np.where for speed,
aggregation — sum, mean, std, min, max along axes — the axis parameter explained,
reshaping — reshape, flatten, ravel, transpose — when each is appropriate,
stacking and splitting — vstack, hstack, concatenate, split — combining arrays,
NumPy in data pipelines — calculating safety factors across 65,000 rows, ceiling thresholds, percentile calculations,
np.percentile and np.nanpercentile — calculating P95 at scale,
NumPy and Pandas — how Pandas is built on NumPy, accessing the underlying array with .values vs .to_numpy(),
memory views and copies — when operations produce a view vs a copy and why it matters,
when to reach for NumPy vs Pandas vs pure Python — the decision logic.
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
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\numpy.html
