# ChatGPT Prompt — Pandas Tutorial (READY TO PASTE)
# Paste everything between the triple-backtick fences into ChatGPT

```
TOPIC: Pandas for Data Engineers
SLUG: 24_pandas
PRIORITY: DE Fundamentals
INFRASTRUCTURE: Pure Python — no cloud, no Docker

===== CODING STANDARDS =====

FILE HEADER (every file must start with this exact block):
# ============================================================
# Topic   : Pandas for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install pandas pyarrow faker
# Run     : python NN_filename.py
# ============================================================

STYLE RULES:
- Comments explain WHY, especially performance trade-offs
- Always show memory usage before and after optimizations
- Use method chaining style (df.pipe().assign().query())
- Type hints on all function signatures
- All data is synthetic — no external files required; generate inline
- No placeholder comments, no TODO, no pass, no NotImplementedError
- Print section separators: print("\n" + "="*60 + "\n  SECTION NAME\n" + "="*60)

===== FILE 01: 01_dataframe_fundamentals.py =====

PURPOSE: DataFrame creation, indexing, dtypes, memory optimization
COVERS: constructors, .loc/.iloc/.at, dtype selection, memory_usage()

EXACT FUNCTION SIGNATURES:

def create_sample_orders(n: int = 10_000) -> pd.DataFrame:
    """
    Generate synthetic orders DataFrame with these columns:
      order_id (str, UUID4 prefix first 8 chars),
      customer_id (str, "CUST-" + 4-digit zero-padded int),
      product_sku (str, "SKU-" + random choice of 20 SKUs),
      quantity (int, 1-10),
      unit_price (float, 5.99 to 999.99, 2 dp),
      status (str, one of: PENDING/CONFIRMED/SHIPPED/DELIVERED/CANCELLED),
      region (str, one of: NORTH/SOUTH/EAST/WEST/CENTRAL),
      order_date (datetime64[ns], random within last 90 days)
    Do NOT use numpy for generation — use random.choices, random.randint, etc.
    """

def demonstrate_indexing(df: pd.DataFrame) -> None:
    """
    Show all indexing methods with commentary on when to use each:
    1. df.loc[row_label, col_label] — label-based, safe for slices
    2. df.iloc[row_int, col_int] — position-based
    3. df.at[row_label, col_label] — single scalar, fastest
    4. df.iat[row_int, col_int] — single scalar by position
    5. Boolean mask: df[df["status"] == "SHIPPED"]
    6. .query(): df.query("unit_price > 100 and region == 'NORTH'")
    Print the result of each and its use-case comment.
    """

def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return memory-optimized copy of df.
    Optimizations to apply:
    - status, region, product_sku → pd.Categorical (huge savings for low-cardinality strings)
    - quantity → np.int8 (values 1-10 fit in int8)
    - unit_price → np.float32 (2dp precision, halves memory)
    - customer_id → pd.Categorical (repeated values)
    Print before/after memory usage:
      Before: 2.1 MB
      After:  0.4 MB  (81% reduction)
    Use df.memory_usage(deep=True).sum() for accurate measurement.
    """

def demonstrate_copy_vs_view(df: pd.DataFrame) -> None:
    """
    Explain the SettingWithCopyWarning trap.
    Show three cases:
    Case 1 (bug): subset = df[df["status"] == "PENDING"]
                  subset["quantity"] = 99  # SettingWithCopyWarning
    Case 2 (fix): subset = df[df["status"] == "PENDING"].copy()
                  subset["quantity"] = 99  # safe
    Case 3 (pandas 2.0 CoW): df.loc[df["status"] == "PENDING", "quantity"] = 99  # preferred
    Print explanation and the difference between each approach.
    """

MAIN BLOCK:
  df = create_sample_orders(10_000)
  demonstrate_indexing(df)
  optimized = optimize_dtypes(df)
  demonstrate_copy_vs_view(df)
  Print final summary table of dtypes, non-null counts, memory per column.

===== FILE 02: 02_groupby_and_reshape.py =====

PURPOSE: GroupBy, aggregations, pivot_table, melt/stack/unstack
COVERS: split-apply-combine, multi-level groupby, named aggregations, reshaping

EXACT FUNCTION SIGNATURES:

def groupby_basics(df: pd.DataFrame) -> None:
    """
    Demonstrate groupby patterns (use orders DataFrame from file 01):
    1. Single key: df.groupby("region")["unit_price"].agg(["mean", "min", "max", "count"])
    2. Named aggregations (pandas >= 1.1):
         df.groupby("region").agg(
             avg_price=("unit_price", "mean"),
             total_revenue=("unit_price", lambda x: (x * df.loc[x.index, "quantity"]).sum()),
             order_count=("order_id", "count"),
         )
    3. Multi-key groupby: df.groupby(["region", "status"])["quantity"].sum().unstack()
    4. transform() — add column without collapsing:
         df["region_avg_price"] = df.groupby("region")["unit_price"].transform("mean")
    Print result of each with explanation of when to use it.
    """

def advanced_aggregations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a sales summary DataFrame:
      group by product_sku + region
      compute:
        - total_revenue = (unit_price * quantity).sum()
        - order_count = count of order_ids
        - avg_order_value = total_revenue / order_count
        - cancellation_rate = (status == 'CANCELLED').sum() / count
        - latest_order = order_date.max()
    Return the summary sorted by total_revenue descending.
    """

def pivot_table_demo(df: pd.DataFrame) -> None:
    """
    Show pivot_table vs crosstab vs groupby.unstack():
    1. pd.pivot_table(df, values="unit_price", index="region", columns="status",
                      aggfunc="mean", fill_value=0, margins=True)
    2. pd.crosstab(df["region"], df["status"], values=df["quantity"],
                   aggfunc="sum", margins=True)
    3. df.groupby(["region", "status"])["unit_price"].mean().unstack(fill_value=0)
    Print all three and explain when each is appropriate.
    """

def melt_and_stack(df: pd.DataFrame) -> None:
    """
    Demonstrate wide-to-long and long-to-wide transforms:
    1. Create a wide summary first:
         wide = df.groupby("region").agg(
             total_revenue=("unit_price", "sum"),
             total_quantity=("quantity", "sum"),
             order_count=("order_id", "count"),
         ).reset_index()
    2. pd.melt(wide, id_vars=["region"], var_name="metric", value_name="value")
    3. pivot back: melted.pivot(index="region", columns="metric", values="value")
    4. stack/unstack on multi-index: build region × status summary, stack(), unstack()
    Print each transformation with shape changes noted.
    """

MAIN BLOCK:
  df = create_sample_orders(50_000)  # import from file 01 or redefine inline
  groupby_basics(df)
  summary = advanced_aggregations(df)
  print(summary.head(10).to_string())
  pivot_table_demo(df)
  melt_and_stack(df)

===== FILE 03: 03_merge_and_clean.py =====

PURPOSE: Merge/join, concat, deduplication, null handling
COVERS: merge types, concat axis, fillna strategies, duplicate detection

EXACT FUNCTION SIGNATURES:

def create_customers(n: int = 1_000) -> pd.DataFrame:
    """
    Return customers DataFrame:
      customer_id (str, "CUST-XXXX"), name (str, first+last), email (str),
      tier (str: BRONZE/SILVER/GOLD/PLATINUM), signup_date (datetime)
    Use Faker or random to generate — no external files.
    """

def create_products(n_skus: int = 20) -> pd.DataFrame:
    """
    Return products DataFrame:
      product_sku (str, "SKU-XXXXX"), product_name (str), category (str),
      cost_price (float), list_price (float), in_stock (bool)
    """

def demonstrate_merge_types(orders: pd.DataFrame, customers: pd.DataFrame) -> None:
    """
    Show all 4 merge types with row counts and practical meaning:
    1. INNER: df.merge(customers, on="customer_id", how="inner")
       → only orders with known customer
    2. LEFT:  df.merge(customers, on="customer_id", how="left")
       → all orders, customer nulls for unknown
    3. RIGHT: df.merge(customers, on="customer_id", how="right")
       → all customers even with no orders (useful for churn analysis)
    4. OUTER: df.merge(customers, on="customer_id", how="outer")
       → all rows from both, identify gaps
    Print: f"INNER: {len(inner):,} rows | LEFT: {len(left):,} | ..."
    Also show: indicator=True with how="outer" to flag _merge column.
    """

def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Demonstrate null handling strategies on the orders + customers merged df:
    1. Detection: df.isnull().sum(), df.isnull().mean() (proportion)
    2. Drop: df.dropna(subset=["customer_id"])
    3. Fill with constant: df["tier"].fillna("UNKNOWN")
    4. Fill with group median: df["unit_price"].fillna(df.groupby("region")["unit_price"].transform("median"))
    5. Forward fill (time series): df.sort_values("order_date").ffill()
    6. Interpolate: df["unit_price"].interpolate(method="linear")
    Print null counts before and after each strategy.
    Return cleaned DataFrame (drop rows missing critical fields).
    """

def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Demonstrate deduplication patterns:
    1. Find exact duplicates: df.duplicated().sum()
    2. Find duplicates on subset: df.duplicated(subset=["order_id"]).sum()
    3. Keep latest: df.sort_values("order_date").drop_duplicates(subset=["order_id"], keep="last")
    4. Custom: identify order_ids appearing >1 time, flag them in a new column "is_duplicate"
    Print counts at each step. Return deduplicated DataFrame.
    """

def concat_patterns(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Show pd.concat patterns:
    1. Stack DataFrames vertically: pd.concat(dfs, ignore_index=True)
    2. Add source label: pd.concat(dfs, keys=["jan", "feb", "mar"])
    3. Side-by-side (axis=1) with alignment on index
    4. concat vs append (append deprecated in 2.0 — always use concat)
    Print shape of each result.
    """

MAIN BLOCK:
  orders = create_sample_orders(20_000)
  customers = create_customers(1_000)
  products = create_products(20)
  demonstrate_merge_types(orders, customers)
  cleaned = handle_nulls(orders.merge(customers, on="customer_id", how="left"))
  deduped = deduplicate(orders)
  monthly = [create_sample_orders(1_000) for _ in range(3)]
  concat_patterns(monthly)

===== FILE 04: 04_string_datetime_apply.py =====

PURPOSE: String operations, datetime processing, apply vs vectorized
COVERS: .str accessor, .dt accessor, vectorized vs apply performance

EXACT FUNCTION SIGNATURES:

def string_operations(df: pd.DataFrame) -> None:
    """
    Demonstrate .str accessor on the orders DataFrame:
    1. Case: df["region"].str.lower(), .str.upper(), .str.title()
    2. Pad/strip: df["customer_id"].str.strip(), .str.zfill(10)
    3. Extract: df["customer_id"].str.extract(r"CUST-(\d+)").astype(int)
    4. Split: df["product_sku"].str.split("-", expand=True)
    5. Contains/match: df[df["status"].str.contains("ED$", regex=True)]
    6. Replace: df["region"].str.replace("NORTH", "NORTHEAST", regex=False)
    7. Cat: df["customer_id"].str.cat(df["region"], sep="|")
    Print examples of each.
    """

def datetime_operations(df: pd.DataFrame) -> None:
    """
    Demonstrate .dt accessor and datetime math:
    1. Extract: df["order_date"].dt.year, .dt.month, .dt.day_name(), .dt.quarter
    2. Truncate: df["order_date"].dt.to_period("M")  # "2024-01"
    3. Timedelta: df["days_since_order"] = (pd.Timestamp.now() - df["order_date"]).dt.days
    4. Floor/ceil: df["order_date"].dt.floor("D")
    5. Resample pattern (show concept — use a time-indexed series):
         ts = df.set_index("order_date")["unit_price"]
         ts.resample("W").agg(["mean", "sum", "count"])
    6. Business day offset: df["order_date"] + pd.offsets.BDay(3)  # 3 business days later
    Print each result with dtype shown.
    """

def apply_vs_vectorized(df: pd.DataFrame) -> None:
    """
    Benchmark apply vs vectorized for the same operation.
    Operation: compute revenue = unit_price * quantity, then bucket into:
      LOW (<50), MEDIUM (50-500), HIGH (>500)

    Method 1 (slowest — never use for column ops):
      df.apply(lambda row: row["unit_price"] * row["quantity"], axis=1)

    Method 2 (element-wise apply — slow):
      df["unit_price"].apply(lambda x: x * 1.1)

    Method 3 (vectorized — always prefer):
      df["unit_price"] * df["quantity"]

    Method 4 (np.where for if/else):
      np.where(df["revenue"] < 50, "LOW", np.where(df["revenue"] < 500, "MEDIUM", "HIGH"))

    Method 5 (pd.cut for bucketing):
      pd.cut(df["revenue"], bins=[0, 50, 500, float("inf")], labels=["LOW", "MEDIUM", "HIGH"])

    Use timeit to benchmark methods 1 vs 3. Print speedup factor.
    Rule printed: "apply(axis=1) is 100-1000x slower than vectorized ops. Only use for complex logic that cannot be vectorized."
    """

def pipe_method_chaining(df: pd.DataFrame) -> pd.DataFrame:
    """
    Demonstrate clean method chaining with .pipe():
    def add_revenue(df):
        return df.assign(revenue=df["unit_price"] * df["quantity"])
    def add_revenue_bucket(df):
        return df.assign(revenue_bucket=pd.cut(df["revenue"], bins=3, labels=["LOW","MED","HIGH"]))
    def filter_active(df):
        return df.query("status != 'CANCELLED'")

    result = (
        df
        .pipe(add_revenue)
        .pipe(add_revenue_bucket)
        .pipe(filter_active)
        .groupby(["region", "revenue_bucket"])
        .agg(total=("revenue", "sum"), count=("order_id", "count"))
        .reset_index()
        .sort_values("total", ascending=False)
    )
    Print result. Explain .pipe() vs method chaining directly.
    """

MAIN BLOCK:
  df = create_sample_orders(100_000)
  string_operations(df)
  datetime_operations(df)
  apply_vs_vectorized(df)
  pipe_method_chaining(df)

===== FILE 05: 05_io_and_large_files.py =====

PURPOSE: I/O patterns, chunking large files, Parquet, SQL
COVERS: read_csv options, chunking, Parquet with pyarrow, read_sql

EXACT FUNCTION SIGNATURES:

def write_sample_csv(path: str, n_rows: int = 1_000_000) -> str:
    """
    Write 1M row CSV to path using chunked generation (write in chunks of 100K to avoid memory spike).
    Return path. Print file size after write.
    Columns: same as create_sample_orders() schema.
    Use csv.DictWriter directly (faster than pandas for write-only).
    """

def read_csv_options_demo(path: str) -> None:
    """
    Demonstrate read_csv power options:
    1. dtype specification upfront — avoid pandas inferring wrong types
    2. parse_dates=["order_date"]
    3. usecols=["order_id", "unit_price", "region"] — read only needed cols
    4. na_values=["N/A", "null", ""] — explicit null markers
    5. chunksize — read 100K rows at a time
    Show memory and time savings with/without usecols.
    """

def process_large_file_in_chunks(path: str, chunk_size: int = 100_000) -> pd.DataFrame:
    """
    Read 1M row CSV in chunks, compute revenue per chunk, concat partial results.
    Pattern:
      results = []
      for chunk in pd.read_csv(path, chunksize=chunk_size):
          chunk["revenue"] = chunk["unit_price"] * chunk["quantity"]
          partial = chunk.groupby("region")["revenue"].sum()
          results.append(partial)
      final = pd.concat(results).groupby(level=0).sum()
    Print: "Processed {n} chunks, {total_rows:,} total rows"
    Return final aggregated DataFrame.
    """

def parquet_workflow(df: pd.DataFrame, output_dir: str) -> None:
    """
    Demonstrate Parquet patterns with pyarrow engine:
    1. Write: df.to_parquet(path, engine="pyarrow", compression="snappy", index=False)
    2. Read: pd.read_parquet(path, engine="pyarrow", columns=["region", "unit_price"])
    3. Partition by region:
         for region, group in df.groupby("region"):
             group.to_parquet(f"{output_dir}/region={region}/data.parquet")
    4. Read partitioned: pd.read_parquet(output_dir)  # reads all partitions
    5. Show file size CSV vs Parquet vs Parquet+snappy
    Print size comparison table.
    """

def read_sql_demo() -> None:
    """
    Demonstrate pd.read_sql patterns (uses SQLite in-memory — no external DB needed):
    import sqlite3
    conn = sqlite3.connect(":memory:")
    df.to_sql("orders", conn, index=False, if_exists="replace")

    1. Basic: pd.read_sql("SELECT * FROM orders WHERE region = 'NORTH'", conn)
    2. Parameterized: pd.read_sql("SELECT * FROM orders WHERE region = ?", conn, params=["NORTH"])
    3. Chunked: pd.read_sql("SELECT * FROM orders", conn, chunksize=10_000)
    4. With aggregation: complex GROUP BY query → DataFrame
    Show that pd.read_sql returns a DataFrame directly.
    Close connection in finally block.
    """

MAIN BLOCK:
  import tempfile, os
  with tempfile.TemporaryDirectory() as tmp:
      csv_path = os.path.join(tmp, "orders.csv")
      write_sample_csv(csv_path, n_rows=500_000)
      read_csv_options_demo(csv_path)
      result = process_large_file_in_chunks(csv_path)
      print(result)
      df = pd.read_csv(csv_path)
      parquet_workflow(df, tmp)
      read_sql_demo()

===== CAPSTONE =====

Generate these files (all COMPLETE and FULLY RUNNABLE):

--- capstone/brief.md ---
Title: Sales Intelligence Pipeline
Scenario: A Toyota manufacturing division receives daily sales exports as CSV files
(one per region, ~200K rows each). Build a Pandas pipeline that: ingests all 5 region
files, cleans and validates, enriches with product catalog and customer tiers, computes
KPIs (revenue, YoY growth proxied by week-over-week, top 10 SKUs per region), and
writes the final report as Parquet.

--- capstone/pipeline.py ---

CONSTANTS:
  REGIONS = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]
  ROWS_PER_REGION = 200_000

EXACT FUNCTION SIGNATURES:

def generate_region_csv(region: str, output_dir: str, n_rows: int = ROWS_PER_REGION) -> str:
    """Write region CSV to output_dir/orders_{region}.csv. Return path."""

def load_all_regions(input_dir: str) -> pd.DataFrame:
    """
    Read all 5 region CSVs using pd.concat.
    Add source_file column.
    Optimize dtypes immediately after load.
    Print: "Loaded {total_rows:,} rows from {n_files} files | Memory: {mb:.1f} MB"
    """

def validate_and_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validation rules (print count of rows failing each):
    - Drop rows where order_id is null
    - Drop rows where unit_price <= 0
    - Drop rows where quantity not in 1-10
    - Drop exact duplicates on order_id (keep first)
    - Coerce order_date to datetime, drop unparseable
    Print: "Removed {n:,} invalid rows ({pct:.1f}%)"
    Return cleaned DataFrame.
    """

def enrich(df: pd.DataFrame, products: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """
    LEFT JOIN orders → products on product_sku (add category, cost_price)
    LEFT JOIN orders → customers on customer_id (add tier, region_home)
    Add computed columns:
      revenue = unit_price * quantity
      gross_profit = (unit_price - cost_price) * quantity
      is_premium = tier.isin(["GOLD", "PLATINUM"])
    """

def compute_kpis(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Return dict with these DataFrames:
    "region_summary": groupby region → total_revenue, total_profit, order_count, avg_order_value
    "top_skus": top 10 SKUs per region by revenue (use groupby + nlargest)
    "weekly_trend": resample by week → total_revenue, order_count
    "tier_breakdown": groupby tier → revenue, order_count, avg_order_value
    "cancellation_by_region": groupby region → cancellation_rate
    """

def write_report(kpis: dict[str, pd.DataFrame], output_dir: str) -> None:
    """
    Write each KPI DataFrame as a Parquet file:
      output_dir/region_summary.parquet
      output_dir/top_skus.parquet
      output_dir/weekly_trend.parquet
      output_dir/tier_breakdown.parquet
      output_dir/cancellation_by_region.parquet
    Print file sizes. Print total pipeline runtime.
    """

def main() -> None:
    """
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        # Generate all region CSVs
        for region in REGIONS:
            generate_region_csv(region, tmp)
        # Run pipeline
        df = load_all_regions(tmp)
        cleaned = validate_and_clean(df)
        products = create_products(20)
        customers = create_customers(5_000)
        enriched = enrich(cleaned, products, customers)
        kpis = compute_kpis(enriched)
        write_report(kpis, tmp)
        # Print KPI summary
        print("\n=== REGION SUMMARY ===")
        print(kpis["region_summary"].to_string())
    """

--- capstone/test_capstone.py ---

EXACT TEST FUNCTIONS (use pytest):

def test_validate_removes_null_order_ids():
    df = pd.DataFrame({"order_id": ["A1", None, "A3"], "unit_price": [10.0, 5.0, 8.0], "quantity": [1, 1, 1], "order_date": pd.to_datetime(["2024-01-01"]*3)})
    result = validate_and_clean(df)
    assert len(result) == 2
    assert result["order_id"].notna().all()

def test_validate_removes_negative_prices():
    df = pd.DataFrame({"order_id": ["A1","A2","A3"], "unit_price": [10.0, -5.0, 0.0], "quantity": [1,1,1], "order_date": pd.to_datetime(["2024-01-01"]*3)})
    result = validate_and_clean(df)
    assert len(result) == 1
    assert result.iloc[0]["order_id"] == "A1"

def test_validate_removes_duplicate_order_ids():
    df = pd.DataFrame({"order_id": ["A1","A1","A2"], "unit_price": [10.0,10.0,5.0], "quantity": [1,1,1], "order_date": pd.to_datetime(["2024-01-01"]*3)})
    result = validate_and_clean(df)
    assert len(result) == 2

def test_enrich_adds_revenue_column():
    orders = pd.DataFrame({"order_id": ["A1"], "product_sku": ["SKU-001"], "customer_id": ["CUST-0001"], "unit_price": [100.0], "quantity": [3]})
    products = pd.DataFrame({"product_sku": ["SKU-001"], "category": ["Electronics"], "cost_price": [60.0]})
    customers = pd.DataFrame({"customer_id": ["CUST-0001"], "tier": ["GOLD"], "region_home": ["NORTH"]})
    result = enrich(orders, products, customers)
    assert "revenue" in result.columns
    assert result.iloc[0]["revenue"] == 300.0
    assert result.iloc[0]["gross_profit"] == 120.0

def test_enrich_flags_premium_tiers():
    orders = pd.DataFrame({"order_id": ["A1","A2"], "product_sku": ["SKU-001","SKU-001"], "customer_id": ["CUST-0001","CUST-0002"], "unit_price": [100.0,100.0], "quantity": [1,1]})
    products = pd.DataFrame({"product_sku": ["SKU-001"], "category": ["X"], "cost_price": [50.0]})
    customers = pd.DataFrame({"customer_id": ["CUST-0001","CUST-0002"], "tier": ["GOLD","BRONZE"], "region_home": ["N","S"]})
    result = enrich(orders, products, customers)
    assert result[result["customer_id"]=="CUST-0001"]["is_premium"].iloc[0] == True
    assert result[result["customer_id"]=="CUST-0002"]["is_premium"].iloc[0] == False

def test_compute_kpis_returns_all_keys():
    df = enrich(create_sample_orders(1_000), create_products(20), create_customers(200))
    kpis = compute_kpis(df)
    assert set(kpis.keys()) == {"region_summary", "top_skus", "weekly_trend", "tier_breakdown", "cancellation_by_region"}

def test_region_summary_has_all_regions():
    df = enrich(create_sample_orders(5_000), create_products(20), create_customers(500))
    df = validate_and_clean(df)
    kpis = compute_kpis(df)
    assert set(kpis["region_summary"].index) == {"NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"}

===== GENERATION INSTRUCTIONS =====

Generate files ONE AT A TIME in this order:
  01_dataframe_fundamentals.py
  02_groupby_and_reshape.py
  03_merge_and_clean.py
  04_string_datetime_apply.py
  05_io_and_large_files.py
  capstone/brief.md
  capstone/pipeline.py
  capstone/test_capstone.py

Each file must be COMPLETE and FULLY RUNNABLE — no placeholders, no TODO comments, no pass statements.
Use exact function signatures shown above.
After each file, wait for me to say "next".

Acknowledge these instructions, then wait for me to say "generate file 01".
```
