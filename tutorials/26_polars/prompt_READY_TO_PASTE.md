# ChatGPT Prompt — Polars Tutorial (READY TO PASTE)
# Paste everything between the triple-backtick fences into ChatGPT

```
TOPIC: Polars for Data Engineers
SLUG: 26_polars
PRIORITY: DE Fundamentals
INFRASTRUCTURE: Pure Python — no cloud, no Docker

===== CODING STANDARDS =====

FILE HEADER (every file must start with this exact block):
# ============================================================
# Topic   : Polars for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install polars pyarrow faker
# Run     : python NN_filename.py
# ============================================================

STYLE RULES:
- Use polars expression API exclusively (pl.col, pl.lit, pl.when) — never .apply() unless unavoidable
- Show Polars vs Pandas equivalents at least once per major concept
- Print query plans where relevant: lf.explain()
- Include benchmark comparisons (timeit) for operations where Polars shines
- Type hints on all function signatures
- All data synthetic — generate inline, no external files
- No placeholder comments, no TODO, no pass, no NotImplementedError
- Print section separators: print("\n" + "="*60 + "\n  SECTION NAME\n" + "="*60)

===== FILE 01: 01_series_and_dataframe.py =====

PURPOSE: Polars data model, expressions, lazy vs eager
COVERS: Series, DataFrame, pl.col(), pl.lit(), when/then/otherwise, select/with_columns

EXACT FUNCTION SIGNATURES:

def create_transactions(n: int = 50_000) -> pl.DataFrame:
    """
    Generate synthetic transactions DataFrame:
      tx_id (str, "TX-" + zero-padded 8-digit int),
      account_id (str, "ACC-" + random 6-digit int, ~5000 unique accounts),
      amount (float, -500.0 to 5000.0, 2dp — negatives = refunds),
      tx_type (str: PURCHASE/REFUND/TRANSFER/PAYMENT weighted 60/15/15/10),
      merchant_category (str: one of 8 categories),
      tx_date (date type, random within last 180 days),
      status (str: COMPLETED/PENDING/FAILED weighted 90/7/3),
      country (str: US/UK/CA/AU/DE weighted 70/10/8/7/5)
    Use pl.from_dict() with Python lists for generation.
    Print schema with dtypes after creation.
    """

def expression_basics(df: pl.DataFrame) -> None:
    """
    Demonstrate the Polars expression system:
    1. select: df.select([pl.col("tx_id"), pl.col("amount"), pl.col("tx_type")])
    2. with_columns (add/transform without losing existing):
         df.with_columns([
             pl.col("amount").abs().alias("abs_amount"),
             (pl.col("amount") * 1.1).alias("amount_with_fee"),
         ])
    3. filter: df.filter(pl.col("amount") > 0).filter(pl.col("status") == "COMPLETED")
    4. when/then/otherwise:
         df.with_columns(
             pl.when(pl.col("amount") < 0)
               .then(pl.lit("REFUND"))
               .when(pl.col("amount") > 1000)
               .then(pl.lit("HIGH_VALUE"))
               .otherwise(pl.lit("NORMAL"))
               .alias("tx_class")
         )
    5. String expr: pl.col("account_id").str.starts_with("ACC-")
    6. Date expr: pl.col("tx_date").dt.month(), .dt.weekday()
    Print results of each. Show Pandas equivalent inline as a comment.
    """

def polars_vs_pandas_model() -> None:
    """
    Print comparison table:
    | Concept         | Pandas                   | Polars                          |
    | Mutability      | Mutable (SettingWithCopy) | Immutable (always new DataFrame)|
    | Null type       | NaN (float) / None        | null (native for all types)     |
    | Index           | Always present            | No index concept                |
    | Lazy eval       | No (use Dask)             | Built-in (LazyFrame)            |
    | Multi-threading | GIL-limited               | Rust parallel by default        |
    | Memory          | Copies on most ops        | Zero-copy where possible        |
    | String type     | object (slow)             | Categorical / Utf8 (fast)       |
    Show: creating a DataFrame, selecting cols, filtering — Pandas then Polars side by side.
    """

def null_handling(df: pl.DataFrame) -> None:
    """
    Polars null semantics (null ≠ NaN — show the difference):
    1. Check: df.null_count(), pl.col("amount").is_null().sum()
    2. Fill: pl.col("amount").fill_null(0), .fill_null(strategy="mean")
    3. Drop: df.drop_nulls(subset=["account_id"])
    4. Replace NaN (float NaN) with null: pl.col("amount").fill_nan(None)
    5. is_null vs is_nan: show they are different
    Print null counts before/after each operation.
    """

MAIN BLOCK:
  df = create_transactions(100_000)
  expression_basics(df)
  polars_vs_pandas_model()
  null_handling(df)
  print("\nSchema:")
  print(df.schema)
  print("\nSample:")
  print(df.head(5))

===== FILE 02: 02_lazy_frame.py =====

PURPOSE: LazyFrame, query optimization, scan_* functions, collect()
COVERS: scan_csv/scan_parquet, explain(), streaming, predicate pushdown

EXACT FUNCTION SIGNATURES:

def demonstrate_lazy_vs_eager(df: pl.DataFrame, csv_path: str) -> None:
    """
    Show the same query in eager vs lazy mode, compare query plans:
    Eager (DataFrame):
      result = df.filter(pl.col("amount") > 100).groupby("merchant_category").agg(pl.col("amount").sum())
    
    Lazy (LazyFrame):
      result = (
          pl.scan_csv(csv_path)
          .filter(pl.col("amount") > 100)
          .group_by("merchant_category")
          .agg(pl.col("amount").sum())
      )
      print(result.explain())  # show optimized query plan
      df_result = result.collect()
    
    Explain why lazy is better: predicate pushdown, projection pushdown, no intermediate copies.
    Print both plans with explanation of each optimization shown.
    """

def predicate_and_projection_pushdown(csv_path: str) -> None:
    """
    Demonstrate pushdown optimizations:
    
    WITHOUT optimization (eager reads all, then filters):
      df = pd.read_csv(csv_path)  # reads ALL columns
      result = df[df["amount"] > 1000][["account_id", "amount"]]
    
    WITH Polars pushdown (reads only needed rows/cols at scan time):
      result = (
          pl.scan_csv(csv_path)
          .filter(pl.col("amount") > 1000)      # pushed to scan → fewer rows read
          .select(["account_id", "amount"])      # pushed to scan → fewer cols read
          .collect()
      )
    
    Use timeit to benchmark both on a 500K row CSV.
    Print: "Polars LazyFrame: {ms:.0f}ms vs Pandas: {ms:.0f}ms ({speedup:.1f}x faster)"
    """

def streaming_large_file(csv_path: str) -> pl.DataFrame:
    """
    Process a file larger than RAM using streaming=True.
    result = (
        pl.scan_csv(csv_path)
        .filter(pl.col("status") == "COMPLETED")
        .group_by("country")
        .agg([
            pl.col("amount").sum().alias("total_volume"),
            pl.col("tx_id").count().alias("tx_count"),
            pl.col("amount").mean().alias("avg_tx"),
        ])
        .collect(streaming=True)  # processes in batches, constant memory
    )
    Print: "Streaming mode: constant memory regardless of file size"
    Print result sorted by total_volume descending.
    Return result.
    """

def lazy_join_and_sink(txs_path: str, accounts_path: str, output_path: str) -> None:
    """
    Chain multiple scan → join → aggregate → sink in a single lazy plan:
    (
        pl.scan_csv(txs_path)
        .join(pl.scan_csv(accounts_path), on="account_id", how="left")
        .filter(pl.col("status") == "COMPLETED")
        .group_by(["country", "account_tier"])
        .agg(pl.col("amount").sum().alias("total_spend"))
        .sort("total_spend", descending=True)
        .sink_parquet(output_path)  # writes without materializing full result in RAM
    )
    Print: "Sunk results to {output_path} — never materialized full DataFrame in memory"
    """

MAIN BLOCK:
  import tempfile, os
  df = create_transactions(500_000)
  with tempfile.TemporaryDirectory() as tmp:
      csv_path = os.path.join(tmp, "txs.csv")
      df.write_csv(csv_path)
      demonstrate_lazy_vs_eager(df, csv_path)
      predicate_and_projection_pushdown(csv_path)
      streaming_large_file(csv_path)

===== FILE 03: 03_groupby_join_window.py =====

PURPOSE: GroupBy, joins, window functions, list operations
COVERS: group_by().agg(), join strategies, over() for window, list_eval

EXACT FUNCTION SIGNATURES:

def groupby_aggregations(df: pl.DataFrame) -> None:
    """
    Demonstrate group_by patterns:
    1. Basic multi-agg:
         df.group_by("merchant_category").agg([
             pl.col("amount").sum().alias("total"),
             pl.col("amount").mean().alias("avg"),
             pl.col("amount").std().alias("std_dev"),
             pl.col("tx_id").count().alias("tx_count"),
             pl.col("amount").filter(pl.col("amount") > 0).sum().alias("positive_sum"),
         ])
    2. Group by multiple cols with expression in aggregation:
         df.group_by(["country", "tx_type"]).agg(
             pl.col("amount").sum(),
             pl.col("status").filter(pl.col("status")=="FAILED").count().alias("failed_count"),
         )
    3. rolling_mean within group using over() (see window functions below)
    Print shape and first 10 rows of each result.
    """

def join_strategies(df: pl.DataFrame) -> None:
    """
    Build an accounts DataFrame and demonstrate join strategies:
    accounts = pl.DataFrame({
        "account_id": df["account_id"].unique().to_list(),
        "account_tier": [...],   # BASIC/PREMIUM/PRIVATE_BANKING
        "credit_limit": [...],
        "country_home": [...],
    })
    
    Show:
    1. Inner join (default): df.join(accounts, on="account_id", how="inner")
    2. Left join: df.join(accounts, on="account_id", how="left")
    3. Anti join (rows in df with NO match in accounts):
         df.join(accounts, on="account_id", how="anti")
    4. Semi join (rows in df that HAVE a match — no extra cols added):
         df.join(accounts, on="account_id", how="semi")
    
    Polars join note: all joins are hash joins by default — O(n) not O(n log n).
    Print: row counts for each join type.
    """

def window_functions(df: pl.DataFrame) -> None:
    """
    Window functions using .over() — equivalent to SQL PARTITION BY.
    
    1. Running sum per account:
         df.with_columns(
             pl.col("amount").cum_sum().over("account_id").alias("running_balance")
         )
    2. Rank within group:
         df.with_columns(
             pl.col("amount").rank(descending=True).over("merchant_category").alias("rank_in_category")
         )
    3. Lag/lead (shifted value within partition):
         df.sort("tx_date").with_columns(
             pl.col("amount").shift(1).over("account_id").alias("prev_tx_amount")
         )
    4. Percent of group total:
         df.with_columns(
             (pl.col("amount") / pl.col("amount").sum().over("country") * 100).alias("pct_of_country")
         )
    
    Print head(10) of result for each. Show SQL equivalent as comment.
    """

def list_operations(df: pl.DataFrame) -> None:
    """
    Polars native list dtype for nested data:
    1. Create a per-account list of tx amounts:
         account_txs = df.group_by("account_id").agg(
             pl.col("amount").alias("all_amounts"),      # → List[f64]
             pl.col("tx_date").alias("all_dates"),
         )
    2. Operate on list column:
         account_txs.with_columns([
             pl.col("all_amounts").list.sum().alias("total"),
             pl.col("all_amounts").list.max().alias("max_tx"),
             pl.col("all_amounts").list.len().alias("tx_count"),
             pl.col("all_amounts").list.slice(0, 5).alias("first_5_txs"),
         ])
    3. Explode back to flat: account_txs.explode("all_amounts")
    Print each result with dtypes.
    """

MAIN BLOCK:
  df = create_transactions(200_000)
  groupby_aggregations(df)
  join_strategies(df)
  window_functions(df.sort("tx_date").head(50_000))
  list_operations(df)

===== FILE 04: 04_io_and_formats.py =====

PURPOSE: Reading/writing CSV, Parquet, JSON, Arrow, Delta (via deltalake)
COVERS: scan_* vs read_*, write options, schema enforcement, IPC/Arrow format

EXACT FUNCTION SIGNATURES:

def csv_io_demo(df: pl.DataFrame, tmp_dir: str) -> None:
    """
    CSV read/write with Polars:
    WRITE:
      df.write_csv(path, separator=",", null_value="", date_format="%Y-%m-%d")
    
    READ options:
      pl.read_csv(path,
          dtypes={"amount": pl.Float64, "tx_date": pl.Date},
          try_parse_dates=True,
          null_values=["", "N/A"],
          n_rows=10_000,       # read only first N rows
          columns=["tx_id", "amount", "tx_type"],  # projection pushdown
      )
    
    Show: inferred dtypes vs explicit dtypes (wrong inference example with dates as strings).
    Print: "Read {n:,} rows in {ms:.0f}ms"
    """

def parquet_io_demo(df: pl.DataFrame, tmp_dir: str) -> None:
    """
    Parquet write and partitioned read:
    WRITE options:
      df.write_parquet(path,
          compression="snappy",    # vs "zstd", "lz4", "uncompressed"
          row_group_size=100_000,  # affects read performance
          statistics=True,         # min/max stats per column for pushdown
      )
    
    READ with pushdown via scan:
      pl.scan_parquet(path)
        .filter(pl.col("amount") > 0)
        .select(["account_id", "amount", "merchant_category"])
        .collect()
    
    Partitioned write pattern (by country):
      for country, group in df.group_by("country"):
          group.write_parquet(f"{tmp_dir}/country={country[0]}/data.parquet")
    
    Read partitioned with glob:
      pl.scan_parquet(f"{tmp_dir}/country=US/*.parquet").collect()
    
    Print compression comparison table: size + read time for snappy vs zstd vs uncompressed.
    """

def json_and_ndjson(df: pl.DataFrame, tmp_dir: str) -> None:
    """
    JSON and newline-delimited JSON:
    WRITE:
      df.write_ndjson(path)   # preferred for streaming large datasets
      df.write_json(path)     # full JSON array (avoid for large files)
    
    READ:
      pl.read_ndjson(path)
      pl.scan_ndjson(path).filter(...).collect()  # lazy
    
    Show: nested JSON → struct type handling:
      pl.read_ndjson that contains nested objects → .struct.field() accessor
    
    Print: file sizes JSON vs NDJSON vs Parquet for same data.
    """

def arrow_ipc_demo(df: pl.DataFrame, tmp_dir: str) -> None:
    """
    Arrow IPC (Feather v2) format — fastest for in-process handoff:
    WRITE: df.write_ipc(path)                  # ~3x faster than Parquet write
    READ:  pl.read_ipc(path)                   # ~4x faster than CSV read
    SCAN:  pl.scan_ipc(path).filter(...).collect()
    
    Use case: intermediate files within a single pipeline on same machine.
    
    Benchmark all 4 formats (CSV, Parquet, JSON, IPC) on write + read:
    Print table:
      Format  | Write ms | Read ms | File size MB
      CSV     | 1200     | 800     | 45.2
      Parquet | 300      | 150     | 12.1
      NDJSON  | 900      | 700     | 41.3
      IPC     | 80       | 60      | 18.4
    """

MAIN BLOCK:
  import tempfile
  df = create_transactions(200_000)
  with tempfile.TemporaryDirectory() as tmp:
      csv_io_demo(df, tmp)
      parquet_io_demo(df, tmp)
      json_and_ndjson(df, tmp)
      arrow_ipc_demo(df, tmp)

===== FILE 05: 05_polars_vs_pandas.py =====

PURPOSE: Side-by-side comparison, migration patterns, when to choose each
COVERS: benchmark, API translation table, gotchas when migrating

EXACT FUNCTION SIGNATURES:

def benchmark_common_operations(n_rows: int = 1_000_000) -> None:
    """
    Benchmark these operations on n_rows of transactions data:
    Both Pandas and Polars. Use timeit.timeit(number=3).
    
    Operation 1: GroupBy + multiple aggregations
    Operation 2: Filter + join + select
    Operation 3: String operations on a string column
    Operation 4: Read CSV from disk
    Operation 5: Compute window function (running sum per group)
    
    Print results table:
      Operation           | Pandas    | Polars    | Speedup
      GroupBy + agg       | 1250 ms   | 89 ms     | 14.0x
      Filter + join       | 340 ms    | 28 ms     | 12.1x
      String ops          | 890 ms    | 45 ms     | 19.8x
      Read CSV (500K)     | 420 ms    | 110 ms    | 3.8x
      Window function     | 2100 ms   | 95 ms     | 22.1x
    
    Note: actual numbers will vary by machine. Print real measured times.
    """

def api_translation_guide() -> None:
    """
    Print the 20 most common Pandas → Polars API translations:
    | Pandas                              | Polars                                    |
    | df[["a", "b"]]                      | df.select(["a", "b"])                     |
    | df.assign(c=df.a+1)                 | df.with_columns((pl.col("a")+1).alias("c"))|
    | df[df.a > 5]                        | df.filter(pl.col("a") > 5)                |
    | df.groupby("k")["v"].sum()          | df.group_by("k").agg(pl.col("v").sum())   |
    | df.merge(df2, on="k")               | df.join(df2, on="k", how="inner")         |
    | df.sort_values("a")                 | df.sort("a")                              |
    | df.drop_duplicates()                | df.unique()                               |
    | df.rename({"a": "b"})               | df.rename({"a": "b"})                     |
    | df.fillna(0)                        | df.fill_null(0)                           |
    | df.apply(func, axis=1)              | df.map_rows(func)  ← AVOID, very slow     |
    | np.where(cond, a, b)                | pl.when(cond).then(a).otherwise(b)        |
    | df.to_parquet(p)                    | df.write_parquet(p)                       |
    | pd.read_parquet(p)                  | pl.read_parquet(p) or pl.scan_parquet(p)  |
    | df.reset_index()                    | (no index in Polars — not needed)         |
    | df.set_index("k")                   | (not applicable — use group_by or join)   |
    | df.pivot_table(...)                 | df.pivot(...)                             |
    | df.melt(...)                        | df.melt(...)                              |
    | df.str.contains("pat")             | pl.col("c").str.contains("pat")           |
    | df.dt.month                         | pl.col("d").dt.month()                    |
    | pd.concat([a, b])                   | pl.concat([a, b])                         |
    """

def migration_gotchas() -> None:
    """
    Print the 8 most common bugs when migrating Pandas code to Polars:
    
    1. Index assumption — Polars has no index; reset_index() patterns break.
       Fix: use pl.col("row_nr") = df.with_row_index()
    
    2. In-place mutation — Polars DataFrames are immutable.
       df["col"] = value  # FAILS in Polars
       Fix: df = df.with_columns(pl.lit(value).alias("col"))
    
    3. apply(axis=1) — 100x slower than expressions.
       Fix: rewrite as expression; if impossible use map_rows() sparingly.
    
    4. NaN vs null — Polars float columns have both. NaN ≠ null.
       Fix: fill_nan(None) first, then fill_null()
    
    5. groupby key is list not string — Polars group_by returns groups in any order.
       Fix: always .sort() after group_by if order matters.
    
    6. boolean indexing changes type — In Pandas bool series can be ints.
       Fix: use pl.col("flag").cast(pl.Int8) explicitly.
    
    7. String comparison is case-sensitive — same as Pandas but easy to forget.
       Fix: .str.to_lowercase() before comparison.
    
    8. Date vs Datetime — Polars distinguishes pl.Date and pl.Datetime.
       Fix: use .cast(pl.Date) or .cast(pl.Datetime) explicitly.
    
    For each gotcha: show the bug code and the fix code.
    """

def when_to_choose() -> None:
    """
    Print decision guide:
    Choose POLARS when:
      ✓ Data fits on a single machine (< ~50GB)
      ✓ Performance matters (Polars is 5-20x faster than Pandas)
      ✓ Building new pipelines (no legacy Pandas code to maintain)
      ✓ You need lazy evaluation / streaming for large files
      ✓ Multi-threading is important (Polars uses all CPU cores)
    
    Keep PANDAS when:
      ✓ Integrating with sklearn, statsmodels, matplotlib (they expect Pandas)
      ✓ Maintaining existing Pandas codebase (migration cost not worth it for small files)
      ✓ Frequent in-place mutations are needed
      ✓ Team already knows Pandas and file sizes are small (<1M rows)
    
    The bridge (zero-copy conversion):
      pandas_df = polars_df.to_pandas()
      polars_df = pl.from_pandas(pandas_df)
    """

MAIN BLOCK:
  benchmark_common_operations(500_000)
  api_translation_guide()
  migration_gotchas()
  when_to_choose()

===== CAPSTONE =====

Generate these files (all COMPLETE and FULLY RUNNABLE):

--- capstone/brief.md ---
Title: High-Throughput Financial Transaction Processor
Scenario: Capital One-style batch processor for 5M daily card transactions.
Ingest raw CSV, enrich with merchant + account data, detect anomalies
(velocity check: >10 txs in 1 hour from same account, large tx >3x account avg),
produce a risk-scored output Parquet, benchmark entire pipeline against Pandas equivalent.

--- capstone/pipeline.py ---

CONSTANTS:
  N_TRANSACTIONS = 5_000_000
  N_ACCOUNTS = 100_000
  ANOMALY_VELOCITY_WINDOW_HOURS = 1
  ANOMALY_VELOCITY_THRESHOLD = 10     # more than 10 txs in 1 hour = suspicious
  LARGE_TX_MULTIPLIER = 3.0           # tx > 3x account mean = suspicious

EXACT FUNCTION SIGNATURES:

def generate_transactions(n: int = N_TRANSACTIONS) -> pl.DataFrame:
    """Generate in chunks of 500K using pl.concat to avoid peak RAM."""

def generate_accounts(n: int = N_ACCOUNTS) -> pl.DataFrame:
    """account_id, tier, credit_limit, avg_monthly_spend, country_home"""

def generate_merchants(n_merchants: int = 500) -> pl.DataFrame:
    """merchant_id, merchant_name, category, country, risk_score (0.0-1.0)"""

def enrich(
    txs: pl.LazyFrame,
    accounts: pl.LazyFrame,
    merchants: pl.LazyFrame,
) -> pl.LazyFrame:
    """Join all three as LazyFrames. Add computed columns."""

def detect_velocity_anomalies(lf: pl.LazyFrame) -> pl.LazyFrame:
    """
    Add column is_velocity_anomaly (bool):
    Count transactions per account_id within ANOMALY_VELOCITY_WINDOW_HOURS rolling window.
    Use over() window function.
    """

def detect_large_tx_anomalies(lf: pl.LazyFrame) -> pl.LazyFrame:
    """
    Add column is_large_tx_anomaly (bool):
    Compare each tx amount to the account's own average (use over("account_id")).
    Flag if amount > avg_monthly_spend * LARGE_TX_MULTIPLIER.
    """

def score_risk(lf: pl.LazyFrame) -> pl.LazyFrame:
    """
    Add risk_score (float 0.0-1.0):
      base = merchant risk_score
      + 0.3 if is_velocity_anomaly
      + 0.25 if is_large_tx_anomaly
      + 0.1 if country != country_home
      clamped to 1.0
    Add risk_label: HIGH (>0.7) / MEDIUM (0.4-0.7) / LOW (<0.4)
    """

def run_pipeline(output_path: str) -> dict:
    """
    Full pipeline as a single lazy plan:
      generate → enrich → detect anomalies → score → sink_parquet(output_path)
    Return: {
      "total_rows": int, "anomaly_count": int, "high_risk_count": int,
      "elapsed_seconds": float, "rows_per_second": int
    }
    """

def benchmark_vs_pandas(n_rows: int = 500_000) -> None:
    """
    Run the same groupby + window + join pipeline on n_rows using both Polars and Pandas.
    Print timing comparison table with speedup factor.
    """

def main() -> None:
    import tempfile, os
    with tempfile.TemporaryDirectory() as tmp:
        output_path = os.path.join(tmp, "risk_scored.parquet")
        report = run_pipeline(output_path)
        print("\n=== PIPELINE REPORT ===")
        for k, v in report.items():
            print(f"  {k}: {v:,}" if isinstance(v, int) else f"  {k}: {v}")
        benchmark_vs_pandas()

--- capstone/test_capstone.py ---

EXACT TEST FUNCTIONS:

def test_generate_transactions_schema():
    df = generate_transactions(1000)
    assert len(df) == 1000
    assert "tx_id" in df.columns
    assert "amount" in df.columns
    assert df["amount"].dtype == pl.Float64

def test_enrich_adds_merchant_columns():
    txs = generate_transactions(500).lazy()
    accounts = generate_accounts(100).lazy()
    merchants = generate_merchants(50).lazy()
    result = enrich(txs, accounts, merchants).collect()
    assert "risk_score" in result.columns or "merchant_risk_score" in result.columns

def test_velocity_anomaly_flag_exists():
    txs = generate_transactions(1000).lazy()
    accounts = generate_accounts(100).lazy()
    merchants = generate_merchants(50).lazy()
    enriched = enrich(txs, accounts, merchants)
    flagged = detect_velocity_anomalies(enriched).collect()
    assert "is_velocity_anomaly" in flagged.columns
    assert flagged["is_velocity_anomaly"].dtype == pl.Boolean

def test_risk_score_clamped_to_one():
    txs = generate_transactions(1000).lazy()
    accounts = generate_accounts(100).lazy()
    merchants = generate_merchants(50).lazy()
    result = (
        enrich(txs, accounts, merchants)
        .pipe(detect_velocity_anomalies)
        .pipe(detect_large_tx_anomalies)
        .pipe(score_risk)
        .collect()
    )
    assert result["risk_score"].max() <= 1.0
    assert result["risk_score"].min() >= 0.0

def test_risk_labels_are_valid():
    txs = generate_transactions(1000).lazy()
    accounts = generate_accounts(100).lazy()
    merchants = generate_merchants(50).lazy()
    result = (
        enrich(txs, accounts, merchants)
        .pipe(detect_velocity_anomalies)
        .pipe(detect_large_tx_anomalies)
        .pipe(score_risk)
        .collect()
    )
    valid_labels = {"HIGH", "MEDIUM", "LOW"}
    actual_labels = set(result["risk_label"].unique().to_list())
    assert actual_labels.issubset(valid_labels)

def test_polars_faster_than_pandas():
    import timeit, pandas as pd
    n = 100_000
    df_pl = generate_transactions(n)
    df_pd = df_pl.to_pandas()
    t_polars = timeit.timeit(
        lambda: df_pl.group_by("merchant_category").agg(pl.col("amount").sum()),
        number=5
    )
    t_pandas = timeit.timeit(
        lambda: df_pd.groupby("merchant_category")["amount"].sum(),
        number=5
    )
    speedup = t_pandas / t_polars
    assert speedup > 1.5, f"Polars should be at least 1.5x faster, got {speedup:.1f}x"

===== GENERATION INSTRUCTIONS =====

Generate files ONE AT A TIME in this order:
  01_series_and_dataframe.py
  02_lazy_frame.py
  03_groupby_join_window.py
  04_io_and_formats.py
  05_polars_vs_pandas.py
  capstone/brief.md
  capstone/pipeline.py
  capstone/test_capstone.py

Each file must be COMPLETE and FULLY RUNNABLE — no placeholders, no TODO, no pass.
Use exact function signatures shown above.
After each file, wait for me to say "next".

Acknowledge these instructions, then wait for me to say "generate file 01".
```
