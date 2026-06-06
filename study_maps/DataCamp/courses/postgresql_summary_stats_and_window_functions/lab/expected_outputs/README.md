# Expected Outputs and Validation Targets

## Dataset validation

After loading `summer.csv`, the validation query should report:

```text
row_count             31165
distinct_years            27
first_year              1896
last_year               2012
distinct_countries       147
distinct_athletes      22762
distinct_events          666
distinct_disciplines      67
distinct_sports           43
distinct_cities           22
```

## Behavioral checks

### Window functions versus GROUP BY

- `GROUP BY country` returns one row per country.
- `COUNT(*) OVER (PARTITION BY country)` preserves medal-level rows.

### ROW_NUMBER

- Every returned row receives a unique sequence.
- With `PARTITION BY`, numbering restarts at each partition boundary.

### LEAD and LAG

- Boundary rows without a corresponding future or prior row return `NULL`.

### LAST_VALUE

- With a full frame ending at `UNBOUNDED FOLLOWING`, every row should show the same true final value within the partition.

### Ranking

For values:

```text
27, 26, 26, 25
```

Expected ranks:

```text
ROW_NUMBER: 1, 2, 3, 4
RANK:       1, 2, 2, 4
DENSE_RANK: 1, 2, 2, 3
```

### NTILE

- `NTILE(3)` produces bucket numbers 1, 2, and 3.
- Bucket row counts should be approximately equal.
- Equal medal values may be split across bucket boundaries.

### Frames

```text
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
```

contains up to three physical rows.

### ROLLUP and CUBE

- `ROLLUP(country, medal)` includes detail, country subtotals, and a grand total.
- `CUBE(country, medal)` also includes medal-only subtotals.

### CROSSTAB

The basic pivot should produce one row for each of:

```text
CHN
RUS
USA
```

with separate `"2008"` and `"2012"` columns.
