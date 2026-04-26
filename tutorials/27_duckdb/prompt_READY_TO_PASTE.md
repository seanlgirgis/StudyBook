# ChatGPT Prompt — DuckDB Tutorial (READY TO PASTE)
# Paste everything between the triple-backtick fences into ChatGPT

```
TOPIC: DuckDB for Data Engineers
SLUG: 27_duckdb
PRIORITY: DE Fundamentals
INFRASTRUCTURE: Pure Python — no cloud, no Docker

===== CODING STANDARDS =====

FILE HEADER (every file must start with this exact block):
# ============================================================
# Topic   : DuckDB for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install duckdb pandas pyarrow polars faker
# Run     : python NN_filename.py
# ============================================================

STYLE RULES:
- Use duckdb.connect() context manager (with duckdb.connect() as con:) where appropriate
- Show both SQL string approach and Relational API (.table(), .filter(), .project())
- Always explain WHY DuckDB beats SQLite for analytics (vectorized execution, columnar)
- Include benchmark comparisons where relevant
- Type hints on all function signatures
- All data synthetic — generate inline, no external files required
- No placeholder comments, no TODO, no pass, no NotImplementedError
- Print section separators: print("\n" + "="*60 + "\n  SECTION NAME\n" + "="*60)

===== FILE 01: 01_duckdb_basics.py =====

PURPOSE: DuckDB connection modes, basic SQL, DataFrame integration
COVERS: in-memory vs persistent, execute(), fetchdf(), fetchall(), register()

EXACT FUNCTION SIGNATURES:

def in_memory_demo() -> duckdb.DuckDBPyConnection:
    """
    Show two connection modes:
    1. In-memory (default): con = duckdb.connect()
       Use case: ad-hoc analysis, no persistence needed, fastest
    2. Persistent: con = duckdb.connect("analytics.duckdb")
       Use case: repeated queries on same dataset, survives process restart
    
    Create a sample table in-memory:
      con.execute('''
          CREATE TABLE orders AS
          SELECT * FROM range(100000) t(id)
          CROSS JOIN (SELECT 'NORTH' AS region UNION ALL SELECT 'SOUTH') r
      ''')
    Show: con.execute("SHOW TABLES").fetchall()
    Show: con.execute("DESCRIBE orders").fetchdf()
    Return the in-memory connection for use in subsequent demos.
    """

def create_and_query_from_python(con: duckdb.DuckDBPyConnection) -> None:
    """
    Generate a pandas DataFrame of 100K rows and query it WITHOUT copying into DuckDB:
    
    df = pd.DataFrame({...})  # 100K orders
    
    # DuckDB can directly query a Python variable — no INSERT needed
    result = con.execute("SELECT region, SUM(amount) FROM df GROUP BY region").fetchdf()
    
    # Register for reuse (still no copy — just a named reference)
    con.register("orders_view", df)
    result2 = con.execute("SELECT * FROM orders_view WHERE amount > 500 LIMIT 10").fetchdf()
    
    # Or use the relational API
    rel = con.table("orders_view").filter("amount > 500").project("region, amount")
    
    Print schema, first 5 rows, and query results.
    Explain: "DuckDB scans DataFrames in-place via Arrow. Zero copy overhead."
    """

def fetch_methods(con: duckdb.DuckDBPyConnection) -> None:
    """
    Show all result fetch methods and when to use each:
    
    res = con.execute("SELECT region, COUNT(*) AS cnt FROM orders_view GROUP BY region")
    
    1. .fetchall()      → list of tuples — good for simple checks
    2. .fetchone()      → first row as tuple — good for scalar results
    3. .fetchdf()       → pandas DataFrame — integrate with matplotlib/sklearn
    4. .fetchnumpy()    → dict of numpy arrays — fastest for numerical processing
    5. .pl()            → polars DataFrame — fastest if using Polars downstream
    6. .arrow()         → pyarrow Table — zero-copy to Arrow ecosystem
    
    Print result of each fetch method with type annotation.
    Print when to use each in a comment table.
    """

def parameterized_queries(con: duckdb.DuckDBPyConnection) -> None:
    """
    Show safe parameterized queries (prevents SQL injection):
    
    # Positional parameters
    result = con.execute(
        "SELECT * FROM orders_view WHERE region = ? AND amount > ?",
        ["NORTH", 100.0]
    ).fetchdf()
    
    # Named parameters (DuckDB 0.9+)
    result = con.execute(
        "SELECT * FROM orders_view WHERE region = $region AND amount > $min_amount",
        {"region": "SOUTH", "min_amount": 50.0}
    ).fetchdf()
    
    # NEVER do this:
    # f"SELECT * FROM orders WHERE region = '{user_input}'"  # SQL injection risk
    
    Print results and the SQL injection warning.
    """

MAIN BLOCK:
  con = in_memory_demo()
  create_and_query_from_python(con)
  fetch_methods(con)
  parameterized_queries(con)
  con.close()

===== FILE 02: 02_analytical_sql.py =====

PURPOSE: Analytical SQL patterns — window functions, CTEs, QUALIFY, PIVOT
COVERS: All the SQL features SQLite lacks that DuckDB supports natively

EXACT FUNCTION SIGNATURES:

def setup_database(con: duckdb.DuckDBPyConnection) -> None:
    """
    Create 3 tables in DuckDB using Python-generated data:
    
    orders: order_id, customer_id, product_id, amount, order_date, region, status
    customers: customer_id, name, tier, signup_date, country
    products: product_id, name, category, cost_price, list_price
    
    Each 100K, 10K, 200 rows respectively. Use con.execute("CREATE TABLE AS SELECT ...").
    Show how to insert from a pandas DataFrame:
      con.execute("INSERT INTO orders SELECT * FROM df")
    """

def window_functions_demo(con: duckdb.DuckDBPyConnection) -> None:
    """
    Show 5 window function patterns:
    
    1. Running total:
       SELECT order_id, order_date, amount,
              SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total
       FROM orders
    
    2. Rank within group:
       SELECT *, RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS rank_in_region
       FROM orders
    
    3. Lag/Lead (compare to previous row):
       SELECT *, amount - LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS delta
       FROM orders
    
    4. Moving average (7-day):
       SELECT order_date, AVG(amount) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
       FROM orders
    
    5. Percentile rank:
       SELECT *, PERCENT_RANK() OVER (PARTITION BY region ORDER BY amount) AS percentile
       FROM orders
    
    Execute each and print first 5 rows with column names.
    """

def cte_patterns(con: duckdb.DuckDBPyConnection) -> None:
    """
    Demonstrate CTEs for readable complex queries:
    
    1. Simple CTE:
       WITH high_value AS (SELECT * FROM orders WHERE amount > 500)
       SELECT region, COUNT(*), SUM(amount) FROM high_value GROUP BY region
    
    2. Chained CTEs (multi-step pipeline):
       WITH
         active_customers AS (SELECT customer_id FROM orders GROUP BY 1 HAVING COUNT(*) > 5),
         customer_revenue AS (SELECT o.customer_id, SUM(o.amount) AS total FROM orders o
                              JOIN active_customers ac ON o.customer_id = ac.customer_id GROUP BY 1),
         tier_joined AS (SELECT cr.*, c.tier FROM customer_revenue cr JOIN customers c USING (customer_id))
       SELECT tier, AVG(total) AS avg_revenue, COUNT(*) AS customer_count FROM tier_joined GROUP BY tier
    
    3. Recursive CTE (date spine — generate every date in a range):
       WITH RECURSIVE date_spine AS (
         SELECT DATE '2024-01-01' AS dt
         UNION ALL
         SELECT dt + INTERVAL '1 day' FROM date_spine WHERE dt < DATE '2024-12-31'
       )
       SELECT ds.dt, COALESCE(SUM(o.amount), 0) AS daily_revenue
       FROM date_spine ds LEFT JOIN orders o ON o.order_date = ds.dt
       GROUP BY ds.dt ORDER BY ds.dt
    
    Execute each and print results.
    """

def qualify_and_pivot(con: duckdb.DuckDBPyConnection) -> None:
    """
    QUALIFY — filter on window function results (not possible in standard SQL):
    
    -- Get only the top 1 order per customer (by amount) WITHOUT a subquery:
    SELECT customer_id, order_id, amount, order_date
    FROM orders
    QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) = 1
    
    Without QUALIFY: needs subquery + WHERE rank = 1 (ugly and slower).
    Print: "QUALIFY eliminates the need for subquery/CTE just to filter on window result."
    
    PIVOT — reshape rows to columns:
    PIVOT orders ON region USING SUM(amount) GROUP BY product_id
    → product_id | NORTH | SOUTH | EAST | WEST | CENTRAL
    
    UNPIVOT the result back:
    UNPIVOT pivoted ON (NORTH, SOUTH, EAST, WEST, CENTRAL) INTO NAME region VALUE total_revenue
    
    Execute both and print.
    """

def advanced_aggregations(con: duckdb.DuckDBPyConnection) -> None:
    """
    DuckDB aggregations that are rare in SQLite/Postgres:
    
    1. FILTER clause (conditional aggregation without CASE):
       SELECT region,
              COUNT(*) FILTER (WHERE status = 'COMPLETED') AS completed,
              COUNT(*) FILTER (WHERE status = 'CANCELLED') AS cancelled,
              SUM(amount) FILTER (WHERE amount > 0) AS positive_revenue
       FROM orders GROUP BY region
    
    2. Approximate count distinct (HyperLogLog — fast for billions of rows):
       SELECT region, APPROX_COUNT_DISTINCT(customer_id) AS approx_unique_customers FROM orders GROUP BY region
    
    3. LIST aggregate (group values into array):
       SELECT customer_id, LIST(product_id ORDER BY order_date) AS product_sequence FROM orders GROUP BY 1
    
    4. PERCENTILE_CONT:
       SELECT region, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) AS median_order FROM orders GROUP BY region
    
    5. GROUPING SETS / ROLLUP:
       SELECT region, status, SUM(amount) FROM orders
       GROUP BY ROLLUP(region, status)  -- totals at each level
    
    Execute each and print.
    """

MAIN BLOCK:
  con = duckdb.connect()
  setup_database(con)
  window_functions_demo(con)
  cte_patterns(con)
  qualify_and_pivot(con)
  advanced_aggregations(con)
  con.close()

===== FILE 03: 03_files_and_formats.py =====

PURPOSE: Reading CSV/Parquet/JSON directly — DuckDB's superpower for DE
COVERS: read_csv(), read_parquet(), read_json(), glob patterns, S3 httpfs

EXACT FUNCTION SIGNATURES:

def read_csv_demo(tmp_dir: str) -> None:
    """
    DuckDB can query CSV files directly — no loading required:
    
    # Create sample CSVs
    df.to_csv(f"{tmp_dir}/orders_2024_01.csv")
    df.to_csv(f"{tmp_dir}/orders_2024_02.csv")
    
    # Query ONE file directly
    con.execute(f"SELECT * FROM read_csv_auto('{tmp_dir}/orders_2024_01.csv') LIMIT 5").fetchdf()
    
    # Query ALL matching files with glob
    con.execute(f"SELECT COUNT(*), SUM(amount) FROM read_csv_auto('{tmp_dir}/orders_2024_*.csv')").fetchdf()
    
    # With explicit schema
    con.execute(f'''
        SELECT region, SUM(amount) FROM read_csv(
            '{tmp_dir}/orders_2024_01.csv',
            columns={{'order_id': 'VARCHAR', 'amount': 'DOUBLE', 'region': 'VARCHAR', 'order_date': 'DATE'}},
            dateformat='%Y-%m-%d'
        ) GROUP BY region
    ''').fetchdf()
    
    Print all results.
    """

def read_parquet_demo(tmp_dir: str) -> None:
    """
    DuckDB + Parquet = the DE power combo:
    
    # Write partitioned Parquet
    for region in ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]:
        df[df["region"] == region].to_parquet(f"{tmp_dir}/region={region}/data.parquet")
    
    # Query single file
    con.execute(f"SELECT * FROM read_parquet('{tmp_dir}/region=NORTH/data.parquet') LIMIT 5").fetchdf()
    
    # Query ALL partitions with glob (hive partitioning awareness)
    con.execute(f'''
        SELECT region, SUM(amount) AS total
        FROM read_parquet('{tmp_dir}/region=*/data.parquet', hive_partitioning=true)
        GROUP BY region
    ''').fetchdf()
    
    # Persistent table from Parquet (zero copy — metadata only):
    con.execute(f"CREATE VIEW orders_parquet AS SELECT * FROM read_parquet('{tmp_dir}/region=*/data.parquet')")
    
    Print results and explain: "DuckDB pushes filters into Parquet row groups — reads only matching data"
    """

def read_json_demo(tmp_dir: str) -> None:
    """
    Read JSON and NDJSON:
    
    # NDJSON (one record per line — preferred for large files)
    con.execute(f"SELECT * FROM read_ndjson_auto('{tmp_dir}/events.ndjson') LIMIT 5").fetchdf()
    
    # Nested JSON — auto-unnests struct columns
    # Show a JSON with nested field: {"id": 1, "user": {"name": "Alice", "tier": "GOLD"}}
    # DuckDB auto-creates: user.name, user.tier
    
    # read_json for JSON arrays
    con.execute(f"SELECT * FROM read_json('{tmp_dir}/batch.json') LIMIT 5").fetchdf()
    
    Print results with schema.
    """

def s3_and_httpfs_demo() -> None:
    """
    Explain S3 access pattern (no live AWS call — show the code with explanation):
    
    # Load extension (built-in, no install needed for DuckDB >= 0.9)
    con.execute("INSTALL httpfs; LOAD httpfs;")
    
    # Configure AWS credentials
    con.execute('''
        SET s3_region = 'us-east-1';
        SET s3_access_key_id = 'YOUR_KEY';
        SET s3_secret_access_key = 'YOUR_SECRET';
    ''')
    
    # Or use AWS profile (preferred)
    con.execute("SET s3_profile = 'default';")
    
    # Query S3 directly (Parquet or CSV)
    # con.execute("SELECT COUNT(*) FROM read_parquet('s3://my-bucket/data/*.parquet')")
    
    # Use credential_chain for EC2/ECS/Lambda (picks up IAM role automatically)
    con.execute("SET s3_use_credential_chain = true;")
    
    Print the full pattern with comments. Add note about cost: "Each scan reads from S3 — 
    cache results locally with CREATE TABLE ... AS SELECT if querying multiple times."
    """

def create_persistent_db(db_path: str, data_dir: str) -> None:
    """
    Pattern for analyst-friendly persistent DuckDB workflow:
    
    with duckdb.connect(db_path) as con:
        # One-time setup: load Parquet into persistent tables
        con.execute(f"CREATE TABLE IF NOT EXISTS orders AS SELECT * FROM read_parquet('{data_dir}/*.parquet')")
        con.execute("CREATE INDEX IF NOT EXISTS idx_orders_region ON orders(region)")
        
        # Subsequent queries are instant (no re-reading files)
        result = con.execute("SELECT region, SUM(amount) FROM orders GROUP BY region").fetchdf()
        print(result)
    
    Print file size of the DuckDB file vs original Parquet files.
    """

MAIN BLOCK:
  import tempfile
  with tempfile.TemporaryDirectory() as tmp:
      df = create_orders(100_000)  # defined inline or imported
      df.to_csv(f"{tmp}/orders_2024_01.csv", index=False)
      df.to_csv(f"{tmp}/orders_2024_02.csv", index=False)
      read_csv_demo(tmp)
      read_parquet_demo(tmp)
      read_json_demo(tmp)
      s3_and_httpfs_demo()

===== FILE 04: 04_duckdb_integrations.py =====

PURPOSE: DuckDB with Pandas, Polars, PyArrow, SQLAlchemy, Jupyter
COVERS: zero-copy Arrow protocol, relation API, pandas/polars interop

EXACT FUNCTION SIGNATURES:

def pandas_integration(con: duckdb.DuckDBPyConnection, df: pd.DataFrame) -> None:
    """
    DuckDB ↔ Pandas zero-copy bridge:
    
    # Query pandas DataFrame directly (no copy, uses Arrow internally)
    result = con.execute("SELECT region, AVG(amount) FROM df GROUP BY region ORDER BY 2 DESC").fetchdf()
    
    # Register for multi-query reuse
    con.register("orders", df)
    
    # Use pandas for viz/sklearn, DuckDB for aggregation
    summary = con.execute("SELECT * FROM orders WHERE amount > 1000").fetchdf()
    # → feed summary to matplotlib, sklearn, etc.
    
    # Write DuckDB query result back to pandas in one line
    df_result: pd.DataFrame = duckdb.query("SELECT * FROM df LIMIT 100").df()
    
    Print: "DuckDB → Pandas: zero copy via Apache Arrow. No serialization overhead."
    """

def polars_integration(con: duckdb.DuckDBPyConnection, df_pl: pl.DataFrame) -> None:
    """
    DuckDB ↔ Polars zero-copy bridge:
    
    # Query Polars DataFrame directly
    result = con.execute("SELECT region, COUNT(*) FROM df_pl GROUP BY region").pl()
    
    # Polars → DuckDB → Polars pipeline
    result = (
        duckdb.query("SELECT * FROM df_pl WHERE amount > 500")
        .pl()                          # result is a Polars DataFrame
        .group_by("merchant_category")
        .agg(pl.col("amount").sum())
    )
    
    # When to use DuckDB vs Polars:
    # DuckDB: complex SQL (window funcs, QUALIFY, CTEs, PIVOT, joins across files)
    # Polars: Python-native transforms, streaming, expression chaining
    # Both: mix freely — zero copy means no performance penalty
    
    Print: "DuckDB + Polars: SQL for complex queries, Polars for Python transforms."
    """

def arrow_integration(con: duckdb.DuckDBPyConnection) -> None:
    """
    DuckDB natively speaks Apache Arrow:
    
    # Fetch as Arrow Table (zero copy)
    arrow_table = con.execute("SELECT * FROM orders LIMIT 1000").arrow()
    
    # Convert Arrow → Pandas (zero copy if no nulls in int columns)
    df = arrow_table.to_pandas()
    
    # Convert Arrow → Polars (always zero copy)
    df_pl = pl.from_arrow(arrow_table)
    
    # Register Arrow Table in DuckDB
    con.register("arrow_data", arrow_table)
    
    # Use PyArrow for Parquet write, DuckDB for read
    import pyarrow.parquet as pq
    pq.write_table(arrow_table, "output.parquet", compression="snappy")
    result = con.execute("SELECT * FROM read_parquet('output.parquet')").arrow()
    
    Print: "Arrow is the universal zero-copy bridge between DuckDB, Pandas, and Polars."
    """

def relational_api_demo(con: duckdb.DuckDBPyConnection) -> None:
    """
    DuckDB Relational API (Python-native, no SQL strings):
    
    rel = (
        con.table("orders")          # DuckDBPyRelation
          .filter("amount > 100")
          .project("region, amount, status")
          .aggregate("region, SUM(amount) AS total, COUNT(*) AS cnt", "region")
          .order("total DESC")
          .limit(10)
    )
    print(rel.fetchdf())
    
    # Can also use Python operators
    rel2 = con.sql("SELECT * FROM orders")
    filtered = rel2.filter("status = 'COMPLETED'")
    joined = filtered.join(con.table("customers"), "orders.customer_id = customers.customer_id")
    
    Print: "Relational API avoids string manipulation — safer for programmatic query building."
    """

MAIN BLOCK:
  con = duckdb.connect()
  df = pd.DataFrame(...)  # 50K rows
  df_pl = pl.from_pandas(df)
  pandas_integration(con, df)
  polars_integration(con, df_pl)
  arrow_integration(con)
  relational_api_demo(con)
  con.close()

===== FILE 05: 05_duckdb_vs_alternatives.py =====

PURPOSE: DuckDB vs SQLite vs Spark vs Pandas for analytics — decision guide
COVERS: benchmark, use-case matrix, migration patterns

EXACT FUNCTION SIGNATURES:

def benchmark_group_by(n_rows: int = 2_000_000) -> None:
    """
    Run the same GROUP BY + multiple aggregations on the same data using:
    1. DuckDB (in-memory)
    2. Pandas
    3. Polars
    4. SQLite
    
    Query: GROUP BY region → SUM(amount), COUNT(*), AVG(amount), MAX(amount)
    
    Print table:
      Engine      | Time (ms) | Memory (MB) | Notes
      DuckDB      | 45        | 120         | Vectorized, columnar, multi-threaded
      Polars      | 89        | 180         | Expression API, multi-threaded Rust
      Pandas      | 890       | 650         | Single-threaded, row-oriented
      SQLite      | 4200      | 380         | Row-oriented, single-threaded, B-tree
    
    Note: actual numbers from your machine.
    """

def duckdb_for_files_benchmark(tmp_dir: str) -> None:
    """
    Benchmark querying a 1M row Parquet file:
    1. DuckDB scan_parquet() with predicate pushdown
    2. pd.read_parquet() then filter in Pandas
    3. pl.scan_parquet() with Polars lazy
    
    Show: DuckDB only reads matching row groups (predicate pushdown in Parquet metadata).
    Print: rows read vs rows in file, and time comparison.
    """

def print_decision_matrix() -> None:
    """
    Print decision matrix:
    
    ╔══════════════════╦══════════╦══════════╦══════════╦══════════╗
    ║ Dimension        ║ DuckDB   ║ SQLite   ║ Pandas   ║ Spark    ║
    ╠══════════════════╬══════════╬══════════╬══════════╬══════════╣
    ║ Data size        ║ < 1TB    ║ < 1GB    ║ < 50GB   ║ > 100GB  ║
    ║ SQL support      ║ Full     ║ Limited  ║ Via conn ║ SparkSQL ║
    ║ Setup            ║ pip only ║ built-in ║ pip only ║ JVM + cfg║
    ║ Multi-threading  ║ Yes      ║ No       ║ No       ║ Yes      ║
    ║ Parquet/CSV      ║ Native   ║ No       ║ Library  ║ Native   ║
    ║ S3 support       ║ httpfs   ║ No       ║ Via s3fs ║ Native   ║
    ║ ACID / txns      ║ Yes      ║ Yes      ║ No       ║ No       ║
    ║ Window funcs     ║ Full     ║ Partial  ║ Partial  ║ Full     ║
    ║ Python API       ║ Excel.   ║ Good     ║ Native   ║ PySpark  ║
    ║ Best for         ║ Analytics║ OLTP/emb ║ Wrangling║ Cluster  ║
    ╚══════════════════╩══════════╩══════════╩══════════╩══════════╝
    """

def recommend_tool(
    data_size_gb: float,
    needs_sql: bool,
    distributed: bool,
    file_query: bool,
) -> dict:
    """
    Return recommendation:
      {
        "primary": str,
        "rationale": str,
        "avoid": str,
        "avoid_reason": str,
      }
    Rules:
    - distributed=True → Spark (or EMR)
    - data_size_gb > 100 → Spark
    - file_query=True and data_size_gb < 100 → DuckDB ("queries files directly — no ETL needed")
    - needs_sql=True and data_size_gb < 10 → DuckDB
    - needs_sql=False and data_size_gb < 50 → Polars
    - data_size_gb < 1 → Pandas or DuckDB
    """

MAIN BLOCK:
  benchmark_group_by(1_000_000)
  with tempfile.TemporaryDirectory() as tmp:
      duckdb_for_files_benchmark(tmp)
  print_decision_matrix()
  scenarios = [
      (0.5, True, False, False),    # Small, SQL needed → DuckDB
      (200.0, True, True, False),   # Large, distributed → Spark
      (5.0, False, False, True),    # File query, medium → DuckDB
      (30.0, False, False, False),  # Medium, no SQL → Polars
  ]
  for args in scenarios:
      rec = recommend_tool(*args)
      print(f"\nData: {args[0]}GB | SQL: {args[1]} | Distributed: {args[2]} | File: {args[3]}")
      print(f"  → {rec['primary']}: {rec['rationale']}")

===== CAPSTONE =====

Generate these files (all COMPLETE and FULLY RUNNABLE):

--- capstone/brief.md ---
Title: Analytical Data Platform with DuckDB
Scenario: A Capital One analyst team needs to run ad-hoc analytical queries on 3 months
of transaction data stored as Parquet files (partitioned by month and region). Build a
DuckDB-based analytics platform that: ingests all Parquet files into a persistent DuckDB
database, exposes 5 pre-built analytical queries (top merchants, fraud velocity, regional
trends, customer cohort analysis, daily P&L), and provides a simple query runner CLI.

--- capstone/setup.py ---

CONSTANTS:
  N_TRANSACTIONS = 500_000
  MONTHS = ["2024-01", "2024-02", "2024-03"]
  REGIONS = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]

EXACT FUNCTION SIGNATURES:

def generate_monthly_transactions(month: str, region: str, n: int) -> pd.DataFrame:
    """Generate n transactions for given month and region."""

def write_partitioned_parquet(output_dir: str) -> list[str]:
    """
    Write Parquet files partitioned by month and region:
      output_dir/month=2024-01/region=NORTH/data.parquet
    Return list of all file paths written.
    """

def build_analytics_db(parquet_dir: str, db_path: str) -> None:
    """
    Create persistent DuckDB with:
    - transactions table (from all Parquet files)
    - customers table
    - merchants table
    - Pre-computed materialized views for each analytical query
    Print: "Loaded {n:,} rows | DB size: {mb:.1f} MB"
    """

--- capstone/analytics.py ---

EXACT FUNCTION SIGNATURES (each returns a DataFrame and also prints formatted output):

def top_merchants_by_volume(con: duckdb.DuckDBPyConnection, top_n: int = 10) -> pd.DataFrame:
    """Top N merchants by transaction volume and count. Uses window rank."""

def velocity_fraud_candidates(con: duckdb.DuckDBPyConnection, min_txs_per_hour: int = 8) -> pd.DataFrame:
    """Accounts with >min_txs_per_hour in any rolling 60-minute window. Uses window COUNT."""

def regional_weekly_trends(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Week-over-week revenue change per region. Uses LAG() window function."""

def customer_cohort_analysis(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """
    Cohort = month of first transaction. For each cohort, show:
    retention by month (% of cohort that transacted in each subsequent month).
    Uses CTEs + PIVOT.
    """

def daily_pnl(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """
    Daily: total revenue, total cost (from products), gross profit, running total.
    Uses window SUM() OVER (ORDER BY date).
    """

--- capstone/query_runner.py ---

def run_query(db_path: str, sql: str) -> pd.DataFrame:
    """Open persistent DB, run query, return DataFrame, close."""

def cli() -> None:
    """
    Simple CLI: if run as main, accept SQL from sys.argv[1] or stdin.
    If no argument, print available pre-built queries and let user choose 1-5.
    """

--- capstone/test_capstone.py ---

EXACT TEST FUNCTIONS:

def test_write_partitioned_parquet_creates_expected_dirs():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        paths = write_partitioned_parquet(tmp)
        assert len(paths) == len(MONTHS) * len(REGIONS)
        for path in paths:
            assert os.path.exists(path)

def test_build_analytics_db_has_transactions_table():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        write_partitioned_parquet(tmp)
        db = os.path.join(tmp, "analytics.duckdb")
        build_analytics_db(tmp, db)
        con = duckdb.connect(db)
        tables = con.execute("SHOW TABLES").fetchdf()
        assert "transactions" in tables["name"].values
        count = con.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
        assert count > 0
        con.close()

def test_top_merchants_returns_correct_shape():
    con = duckdb.connect()
    # inline test data
    con.execute("CREATE TABLE transactions AS SELECT ...")
    result = top_merchants_by_volume(con, top_n=5)
    assert len(result) == 5
    assert "total_volume" in result.columns
    con.close()

def test_velocity_fraud_candidates_threshold():
    con = duckdb.connect()
    # Create data with one account having exactly 9 txs in 30 min
    # → should appear with min_txs_per_hour=8
    result = velocity_fraud_candidates(con, min_txs_per_hour=8)
    assert len(result) >= 1
    con.close()

def test_daily_pnl_has_running_total():
    con = duckdb.connect()
    con.execute("CREATE TABLE transactions AS ...")
    result = daily_pnl(con)
    assert "running_total" in result.columns
    # Running total should be monotonically increasing (all positive amounts)
    assert (result["running_total"].diff().dropna() >= 0).all()
    con.close()

def test_recommend_tool_large_distributed():
    result = recommend_tool(data_size_gb=500, needs_sql=True, distributed=True, file_query=False)
    assert result["primary"] == "Spark"

def test_recommend_tool_file_query():
    result = recommend_tool(data_size_gb=5, needs_sql=True, distributed=False, file_query=True)
    assert result["primary"] == "DuckDB"

===== GENERATION INSTRUCTIONS =====

Generate files ONE AT A TIME in this order:
  01_duckdb_basics.py
  02_analytical_sql.py
  03_files_and_formats.py
  04_duckdb_integrations.py
  05_duckdb_vs_alternatives.py
  capstone/brief.md
  capstone/setup.py
  capstone/analytics.py
  capstone/query_runner.py
  capstone/test_capstone.py

Each file must be COMPLETE and FULLY RUNNABLE — no placeholders, no TODO, no pass.
Use exact function signatures shown above.
After each file, wait for me to say "next".

Acknowledge these instructions, then wait for me to say "generate file 01".
```
