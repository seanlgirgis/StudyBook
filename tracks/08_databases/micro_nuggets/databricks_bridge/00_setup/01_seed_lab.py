"""
NUGGET 00-01 (Bridge) -- Seed Lab
==================================
Create the bridge_lab schema and seed all baseline Delta tables used
by subsequent nuggets.  Safe to rerun (idempotent).

Tables created in nugget_lab.bridge_lab:
  customers      -- dimension: 20 rows
  products       -- dimension: 15 rows
  sales_orders   -- fact:      50 rows
  events_stream  -- raw events: 30 rows (for DE pattern demos)

Why Delta by default?
  Databricks Runtime 8.0+ uses Delta Lake as the default table format.
  Every CREATE TABLE statement gets Delta unless you specify USING CSV, etc.
  Delta = Parquet files + transaction log (_delta_log/) for ACID guarantees.

PostgreSQL analogy:
  CREATE SCHEMA bridge_lab  =>  CREATE SCHEMA bridge_lab
  CREATE TABLE (Delta)      =>  CREATE TABLE (heap storage)
  DESCRIBE HISTORY          =>  No direct equivalent -- closest is pg_stat_user_tables

Usage:
    python 01_seed_lab.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_bridge_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

DIVIDER = "-" * 60


def run(cur, label: str, sql: str) -> None:
    """Execute SQL and print a one-line status."""
    try:
        cur.execute(sql)
        print(f"  [OK]   {label}")
    except Exception as exc:
        # Surface the error but keep going where safe
        msg = str(exc).splitlines()[0][:80]
        print(f"  [WARN] {label}  =>  {msg}")


def table_row_count(cur, table: str) -> int:
    """Return row count for a fully-qualified table, -1 on failure."""
    try:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        row = cur.fetchone()
        return int(row[0]) if row else 0
    except Exception:
        return -1


def main():
    print()
    print("=" * 60)
    print("  Databricks Bridge -- Seed Lab")
    print("=" * 60)

    # Bootstrap connection: no catalog/schema enforced so we can CREATE them
    conn = get_connection(_bootstrap=True)

    with conn.cursor() as cur:

        # ─── Step 1: Ensure catalog exists ────────────────────────────────
        # nugget_lab is already created by the baseline databricks/ nuggets.
        # If starting fresh, create it here.  Unity Catalog requires:
        #   USE CATALOG or CREATE CATALOG privilege.
        print()
        print("  [Step 1] Catalog")
        run(cur, f"CREATE CATALOG IF NOT EXISTS {LAB_CATALOG}",
            f"CREATE CATALOG IF NOT EXISTS {LAB_CATALOG}")

        # ─── Step 2: Ensure schema exists ─────────────────────────────────
        # A schema in Databricks = a namespace within a catalog.
        # In PostgreSQL this is also called a schema; in Snowflake it is
        # a schema inside a database.
        # bridge_lab is separate from 'default' to namespace bridge work.
        print()
        print("  [Step 2] Schema")
        run(cur, f"CREATE SCHEMA IF NOT EXISTS {LAB_CATALOG}.{LAB_SCHEMA}",
            f"CREATE SCHEMA IF NOT EXISTS {LAB_CATALOG}.{LAB_SCHEMA}")

        # ─── Step 3: Create tables ─────────────────────────────────────────
        # All tables default to USING DELTA in Databricks Runtime 8+.
        # COMMENT adds metadata visible via DESCRIBE EXTENDED and
        # Unity Catalog lineage tools.
        print()
        print("  [Step 3] Table DDL")

        run(cur, "CREATE TABLE customers",
            f"""
            CREATE TABLE IF NOT EXISTS {LAB_CATALOG}.{LAB_SCHEMA}.customers (
                customer_id   INT          COMMENT 'Surrogate key',
                customer_name STRING       COMMENT 'Full name',
                email         STRING       COMMENT 'Contact email',
                region        STRING       COMMENT 'Sales region: North/South/East/West',
                segment       STRING       COMMENT 'Market segment: Consumer/Corporate/SMB',
                created_at    DATE         COMMENT 'Account creation date'
            )
            USING DELTA
            COMMENT 'Customer dimension table -- bridge lab'
            """)

        run(cur, "CREATE TABLE products",
            f"""
            CREATE TABLE IF NOT EXISTS {LAB_CATALOG}.{LAB_SCHEMA}.products (
                product_id    INT          COMMENT 'Surrogate key',
                product_name  STRING       COMMENT 'Display name',
                category      STRING       COMMENT 'Electronics/Apparel/Food/Tools/Books',
                unit_price    DECIMAL(10,2) COMMENT 'List price in USD',
                supplier      STRING       COMMENT 'Vendor name'
            )
            USING DELTA
            COMMENT 'Product dimension table -- bridge lab'
            """)

        run(cur, "CREATE TABLE sales_orders",
            f"""
            CREATE TABLE IF NOT EXISTS {LAB_CATALOG}.{LAB_SCHEMA}.sales_orders (
                order_id      INT          COMMENT 'Surrogate key',
                customer_id   INT          COMMENT 'FK to customers',
                product_id    INT          COMMENT 'FK to products',
                order_date    DATE         COMMENT 'Order placement date',
                quantity      INT          COMMENT 'Units ordered',
                unit_price    DECIMAL(10,2) COMMENT 'Price at time of order',
                total_amount  DECIMAL(12,2) COMMENT 'quantity * unit_price',
                status        STRING       COMMENT 'Pending/Shipped/Cancelled/Returned',
                region        STRING       COMMENT 'Fulfillment region'
            )
            USING DELTA
            COMMENT 'Sales orders fact table -- bridge lab'
            """)

        run(cur, "CREATE TABLE events_stream",
            f"""
            CREATE TABLE IF NOT EXISTS {LAB_CATALOG}.{LAB_SCHEMA}.events_stream (
                event_id      STRING       COMMENT 'UUID event identifier',
                event_type    STRING       COMMENT 'page_view/add_to_cart/purchase/return',
                user_id       INT          COMMENT 'User who triggered event',
                event_ts      TIMESTAMP    COMMENT 'Event occurrence time (source clock)',
                payload       STRING       COMMENT 'JSON payload string',
                source        STRING       COMMENT 'web/mobile/api',
                _ingest_ts    TIMESTAMP    COMMENT 'Ingestion watermark (processing time)'
            )
            USING DELTA
            COMMENT 'Raw event stream -- bridge lab (for DE pattern demos)'
            """)

        # ─── Step 4: Seed data (skip if already seeded) ───────────────────
        # Check row count before inserting -- makes this fully idempotent.
        # In production pipelines, you would use a watermark control table
        # instead of a simple count check.
        print()
        print("  [Step 4] Seed data")

        cust_count = table_row_count(cur, f"{LAB_CATALOG}.{LAB_SCHEMA}.customers")
        if cust_count > 0:
            print(f"  [SKIP] customers already has {cust_count} rows")
        else:
            run(cur, "INSERT customers (20 rows)",
                f"""
                INSERT INTO {LAB_CATALOG}.{LAB_SCHEMA}.customers VALUES
                (1,  'Alice Nguyen',    'alice@acme.com',    'North', 'Corporate', '2022-01-15'),
                (2,  'Bob Kimura',      'bob@beta.io',       'South', 'SMB',       '2022-03-08'),
                (3,  'Carol Diaz',      'carol@gamma.co',    'East',  'Consumer',  '2022-04-22'),
                (4,  'David Osei',      'david@delta.net',   'West',  'Corporate', '2022-06-11'),
                (5,  'Eva Petrov',      'eva@epsilon.org',   'North', 'Consumer',  '2022-07-30'),
                (6,  'Frank Mueller',   'frank@zeta.de',     'South', 'SMB',       '2022-09-14'),
                (7,  'Grace Tanaka',    'grace@eta.jp',      'East',  'Corporate', '2022-11-02'),
                (8,  'Henry Okonkwo',   'henry@theta.ng',    'West',  'Consumer',  '2023-01-19'),
                (9,  'Irene Volkov',    'irene@iota.ru',     'North', 'SMB',       '2023-03-07'),
                (10, 'James Park',      'james@kappa.kr',    'South', 'Corporate', '2023-05-23'),
                (11, 'Karen Singh',     'karen@lambda.in',   'East',  'Consumer',  '2023-07-10'),
                (12, 'Leo Martins',     'leo@mu.br',         'West',  'SMB',       '2023-08-28'),
                (13, 'Mia Chen',        'mia@nu.cn',         'North', 'Corporate', '2023-10-15'),
                (14, 'Noah Johansson',  'noah@xi.se',        'South', 'Consumer',  '2023-12-01'),
                (15, 'Olivia Rossi',    'olivia@omicron.it', 'East',  'SMB',       '2024-01-20'),
                (16, 'Paul Dubois',     'paul@pi.fr',        'West',  'Corporate', '2024-03-08'),
                (17, 'Quinn O Brien',   'quinn@rho.ie',      'North', 'Consumer',  '2024-04-25'),
                (18, 'Rosa Fernandez',  'rosa@sigma.es',     'South', 'SMB',       '2024-06-12'),
                (19, 'Sam Goldberg',    'sam@tau.il',        'East',  'Corporate', '2024-08-01'),
                (20, 'Tina Ramos',      'tina@upsilon.mx',   'West',  'Consumer',  '2024-09-18')
                """)

        prod_count = table_row_count(cur, f"{LAB_CATALOG}.{LAB_SCHEMA}.products")
        if prod_count > 0:
            print(f"  [SKIP] products already has {prod_count} rows")
        else:
            run(cur, "INSERT products (15 rows)",
                f"""
                INSERT INTO {LAB_CATALOG}.{LAB_SCHEMA}.products VALUES
                (101, 'Laptop Pro 15',    'Electronics', 1299.99, 'TechCorp'),
                (102, 'Wireless Mouse',   'Electronics',   29.99, 'PeriphCo'),
                (103, 'USB-C Hub 7-port', 'Electronics',   49.99, 'PeriphCo'),
                (104, 'Standing Desk',    'Tools',        399.00, 'FurnishX'),
                (105, 'Ergonomic Chair',  'Tools',        599.00, 'FurnishX'),
                (106, 'Python Cookbook',  'Books',         44.95, 'OReilly'),
                (107, 'Data Engineering', 'Books',         54.95, 'OReilly'),
                (108, 'Winter Jacket',    'Apparel',      129.00, 'OutdoorGear'),
                (109, 'Running Shoes',    'Apparel',       89.99, 'SportMax'),
                (110, 'Organic Coffee',   'Food',          18.50, 'BeanFarm'),
                (111, 'Protein Powder',   'Food',          39.99, 'NutriLab'),
                (112, 'Smart Watch',      'Electronics',  249.00, 'TechCorp'),
                (113, 'Mechanical KB',    'Electronics',   89.00, 'PeriphCo'),
                (114, 'Monitor 27inch',   'Electronics',  329.99, 'TechCorp'),
                (115, 'Cable Organizer',  'Tools',         12.99, 'DeskPro')
                """)

        order_count = table_row_count(cur, f"{LAB_CATALOG}.{LAB_SCHEMA}.sales_orders")
        if order_count > 0:
            print(f"  [SKIP] sales_orders already has {order_count} rows")
        else:
            run(cur, "INSERT sales_orders (50 rows)",
                f"""
                INSERT INTO {LAB_CATALOG}.{LAB_SCHEMA}.sales_orders VALUES
                (1001, 1, 101, '2024-01-05', 1, 1299.99, 1299.99, 'Shipped',   'North'),
                (1002, 2, 110, '2024-01-06', 3,   18.50,   55.50, 'Shipped',   'South'),
                (1003, 3, 106, '2024-01-08', 2,   44.95,   89.90, 'Shipped',   'East'),
                (1004, 4, 112, '2024-01-10', 1,  249.00,  249.00, 'Pending',   'West'),
                (1005, 5, 109, '2024-01-12', 2,   89.99,  179.98, 'Shipped',   'North'),
                (1006, 6, 104, '2024-01-15', 1,  399.00,  399.00, 'Shipped',   'South'),
                (1007, 7, 107, '2024-01-18', 1,   54.95,   54.95, 'Shipped',   'East'),
                (1008, 8, 102, '2024-01-20', 2,   29.99,   59.98, 'Shipped',   'West'),
                (1009, 9, 113, '2024-01-22', 1,   89.00,   89.00, 'Cancelled', 'North'),
                (1010,10, 114, '2024-01-25', 1,  329.99,  329.99, 'Shipped',   'South'),
                (1011, 1, 103, '2024-02-02', 1,   49.99,   49.99, 'Shipped',   'North'),
                (1012, 2, 111, '2024-02-05', 2,   39.99,   79.98, 'Returned',  'South'),
                (1013, 3, 108, '2024-02-08', 1,  129.00,  129.00, 'Shipped',   'East'),
                (1014, 4, 115, '2024-02-10', 3,   12.99,   38.97, 'Shipped',   'West'),
                (1015, 5, 101, '2024-02-12', 1, 1299.99, 1299.99, 'Shipped',   'North'),
                (1016, 6, 106, '2024-02-14', 2,   44.95,   89.90, 'Shipped',   'South'),
                (1017, 7, 112, '2024-02-18', 1,  249.00,  249.00, 'Shipped',   'East'),
                (1018, 8, 109, '2024-02-20', 1,   89.99,   89.99, 'Pending',   'West'),
                (1019, 9, 104, '2024-02-22', 1,  399.00,  399.00, 'Shipped',   'North'),
                (1020,10, 110, '2024-02-25', 4,   18.50,   74.00, 'Shipped',   'South'),
                (1021,11, 107, '2024-03-01', 1,   54.95,   54.95, 'Shipped',   'East'),
                (1022,12, 102, '2024-03-04', 3,   29.99,   89.97, 'Shipped',   'West'),
                (1023,13, 105, '2024-03-08', 1,  599.00,  599.00, 'Shipped',   'North'),
                (1024,14, 113, '2024-03-11', 2,   89.00,  178.00, 'Shipped',   'South'),
                (1025,15, 103, '2024-03-14', 2,   49.99,   99.98, 'Cancelled', 'East'),
                (1026,16, 111, '2024-03-18', 1,   39.99,   39.99, 'Shipped',   'West'),
                (1027,17, 114, '2024-03-20', 1,  329.99,  329.99, 'Shipped',   'North'),
                (1028,18, 108, '2024-03-22', 2,  129.00,  258.00, 'Shipped',   'South'),
                (1029,19, 101, '2024-03-25', 1, 1299.99, 1299.99, 'Returned',  'East'),
                (1030,20, 110, '2024-03-28', 5,   18.50,   92.50, 'Shipped',   'West'),
                (1031, 1, 112, '2024-04-01', 2,  249.00,  498.00, 'Shipped',   'North'),
                (1032, 3, 109, '2024-04-04', 1,   89.99,   89.99, 'Shipped',   'East'),
                (1033, 5, 106, '2024-04-07', 3,   44.95,  134.85, 'Shipped',   'North'),
                (1034, 7, 104, '2024-04-10', 1,  399.00,  399.00, 'Shipped',   'East'),
                (1035, 9, 115, '2024-04-13', 4,   12.99,   51.96, 'Shipped',   'North'),
                (1036,11, 102, '2024-04-16', 2,   29.99,   59.98, 'Pending',   'East'),
                (1037,13, 113, '2024-04-19', 1,   89.00,   89.00, 'Shipped',   'North'),
                (1038,15, 107, '2024-04-22', 2,   54.95,  109.90, 'Shipped',   'East'),
                (1039,17, 111, '2024-04-25', 1,   39.99,   39.99, 'Cancelled', 'North'),
                (1040,19, 114, '2024-04-28', 1,  329.99,  329.99, 'Shipped',   'East'),
                (1041, 2, 105, '2024-05-01', 1,  599.00,  599.00, 'Shipped',   'South'),
                (1042, 4, 103, '2024-05-04', 3,   49.99,  149.97, 'Shipped',   'West'),
                (1043, 6, 108, '2024-05-07', 1,  129.00,  129.00, 'Shipped',   'South'),
                (1044, 8, 110, '2024-05-10', 6,   18.50,  111.00, 'Shipped',   'West'),
                (1045,10, 112, '2024-05-13', 1,  249.00,  249.00, 'Shipped',   'South'),
                (1046,12, 101, '2024-05-16', 1, 1299.99, 1299.99, 'Pending',   'West'),
                (1047,14, 106, '2024-05-19', 2,   44.95,   89.90, 'Shipped',   'South'),
                (1048,16, 109, '2024-05-22', 2,   89.99,  179.98, 'Returned',  'West'),
                (1049,18, 113, '2024-05-25', 1,   89.00,   89.00, 'Shipped',   'South'),
                (1050,20, 115, '2024-05-28', 5,   12.99,   64.95, 'Shipped',   'West')
                """)

        event_count = table_row_count(cur, f"{LAB_CATALOG}.{LAB_SCHEMA}.events_stream")
        if event_count > 0:
            print(f"  [SKIP] events_stream already has {event_count} rows")
        else:
            run(cur, "INSERT events_stream (30 rows)",
                f"""
                INSERT INTO {LAB_CATALOG}.{LAB_SCHEMA}.events_stream VALUES
                ('evt-001','page_view',   1,'2024-05-01 08:00:00','{{\"page\":\"/home\"}}',          'web',    '2024-05-01 08:00:05'),
                ('evt-002','add_to_cart', 1,'2024-05-01 08:02:00','{{\"product_id\":101}}',           'web',    '2024-05-01 08:02:03'),
                ('evt-003','purchase',    1,'2024-05-01 08:05:00','{{\"order_id\":1046}}',             'web',    '2024-05-01 08:05:10'),
                ('evt-004','page_view',   2,'2024-05-01 09:00:00','{{\"page\":\"/products\"}}',       'mobile', '2024-05-01 09:00:07'),
                ('evt-005','add_to_cart', 2,'2024-05-01 09:03:00','{{\"product_id\":105}}',           'mobile', '2024-05-01 09:03:04'),
                ('evt-006','purchase',    2,'2024-05-01 09:08:00','{{\"order_id\":1041}}',             'mobile', '2024-05-01 09:08:12'),
                ('evt-007','page_view',   3,'2024-05-01 10:00:00','{{\"page\":\"/search\"}}',         'web',    '2024-05-01 10:00:02'),
                ('evt-008','page_view',   4,'2024-05-01 10:15:00','{{\"page\":\"/home\"}}',           'api',    '2024-05-01 10:15:01'),
                ('evt-009','add_to_cart', 4,'2024-05-01 10:18:00','{{\"product_id\":103}}',           'api',    '2024-05-01 10:18:05'),
                ('evt-010','purchase',    4,'2024-05-01 10:22:00','{{\"order_id\":1042}}',             'api',    '2024-05-01 10:22:08'),
                ('evt-011','page_view',   5,'2024-05-01 11:00:00','{{\"page\":\"/deals\"}}',          'web',    '2024-05-01 11:00:03'),
                ('evt-012','add_to_cart', 5,'2024-05-01 11:05:00','{{\"product_id\":106}}',           'web',    '2024-05-01 11:05:06'),
                ('evt-013','purchase',    5,'2024-05-01 11:09:00','{{\"order_id\":1047}}',             'web',    '2024-05-01 11:09:14'),
                ('evt-014','page_view',   6,'2024-05-01 12:00:00','{{\"page\":\"/home\"}}',           'mobile', '2024-05-01 12:00:04'),
                ('evt-015','return',      6,'2024-05-01 12:10:00','{{\"order_id\":1012,\"reason\":\"defect\"}}','mobile','2024-05-01 12:10:09'),
                ('evt-016','page_view',   7,'2024-05-02 08:00:00','{{\"page\":\"/search\"}}',         'web',    '2024-05-02 08:00:06'),
                ('evt-017','add_to_cart', 7,'2024-05-02 08:04:00','{{\"product_id\":109}}',           'web',    '2024-05-02 08:04:07'),
                ('evt-018','page_view',   8,'2024-05-02 09:00:00','{{\"page\":\"/products\"}}',       'mobile', '2024-05-02 09:00:02'),
                ('evt-019','add_to_cart', 8,'2024-05-02 09:05:00','{{\"product_id\":110}}',           'mobile', '2024-05-02 09:05:05'),
                ('evt-020','purchase',    8,'2024-05-02 09:12:00','{{\"order_id\":1044}}',             'mobile', '2024-05-02 09:12:11'),
                ('evt-021','page_view',   9,'2024-05-02 10:00:00','{{\"page\":\"/home\"}}',           'api',    '2024-05-02 10:00:01'),
                ('evt-022','page_view',  10,'2024-05-02 11:00:00','{{\"page\":\"/home\"}}',           'web',    '2024-05-02 11:00:03'),
                ('evt-023','add_to_cart',10,'2024-05-02 11:03:00','{{\"product_id\":112}}',           'web',    '2024-05-02 11:03:05'),
                ('evt-024','purchase',   10,'2024-05-02 11:08:00','{{\"order_id\":1045}}',             'web',    '2024-05-02 11:08:09'),
                ('evt-025','page_view',  11,'2024-05-03 08:00:00','{{\"page\":\"/deals\"}}',          'mobile', '2024-05-03 08:00:04'),
                ('evt-026','add_to_cart',11,'2024-05-03 08:06:00','{{\"product_id\":102}}',           'mobile', '2024-05-03 08:06:07'),
                ('evt-027','purchase',   11,'2024-05-03 08:11:00','{{\"order_id\":1036}}',             'mobile', '2024-05-03 08:11:12'),
                ('evt-028','page_view',  12,'2024-05-03 09:00:00','{{\"page\":\"/home\"}}',           'web',    '2024-05-03 09:00:02'),
                ('evt-029','page_view',  13,'2024-05-03 10:00:00','{{\"page\":\"/search\"}}',         'api',    '2024-05-03 10:00:03'),
                ('evt-030','add_to_cart',13,'2024-05-03 10:05:00','{{\"product_id\":113}}',           'api',    '2024-05-03 10:05:06')
                """)

        # ─── Validation ───────────────────────────────────────────────────
        print()
        print("  [Step 5] Validation")
        tables = ["customers", "products", "sales_orders", "events_stream"]
        expected = [20, 15, 50, 30]
        all_pass = True
        for tbl, exp in zip(tables, expected):
            fqn = f"{LAB_CATALOG}.{LAB_SCHEMA}.{tbl}"
            count = table_row_count(cur, fqn)
            status = "PASS" if count >= exp else "FAIL"
            if status == "FAIL":
                all_pass = False
            print(f"      {status}  {tbl:<20} rows={count}  (expected >= {exp})")

    conn.close()

    print()
    print(DIVIDER)
    if all_pass:
        print("  Seed complete. All tables ready. [PASS]")
    else:
        print("  Seed finished with warnings. Check output above.")
    print(f"  Target: {LAB_CATALOG}.{LAB_SCHEMA}")
    print(DIVIDER)
    print()

    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
