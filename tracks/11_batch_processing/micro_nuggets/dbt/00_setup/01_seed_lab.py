"""
01_seed_lab.py — Seed the dbt lab with realistic CSV data.

Steps:
  1. Write profiles.yml (auto-detects backend)
  2. Run `dbt deps` (install packages)
  3. Run `dbt seed` to load CSVs into the raw schema
  4. Verify seed tables exist by querying row counts

This script is idempotent — safe to run multiple times.

Run:
    python 00_setup/01_seed_lab.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from _dbt_lane_connect import (
    DBT_PROJECT_DIR,
    detect_backend,
    run_dbt,
    write_profiles_yml,
)

# ── Seed data ─────────────────────────────────────────────────────────────────
# These CSVs are embedded here and written to lab_dbt_project/seeds/ so the
# script is self-contained.  Later you can edit the CSV files directly.

RAW_CUSTOMERS = """\
id,name,email,country,created_at,is_active,tier
1,Alice Johnson,alice@example.com,US,2023-01-15,true,gold
2,Bob Smith,bob@example.com,UK,2023-02-01,true,silver
3,Carol White,carol@example.com,CA,2023-02-14,true,bronze
4,David Lee,david@example.com,US,2023-03-05,true,platinum
5,Eva Martinez,eva@example.com,MX,2023-03-20,false,bronze
6,Frank Brown,frank@example.com,US,2023-04-01,true,silver
7,Grace Kim,grace@example.com,KR,2023-04-15,true,gold
8,Henry Davis,henry@example.com,UK,2023-05-01,true,silver
9,Iris Chen,iris@example.com,CN,2023-05-10,true,bronze
10,Jack Wilson,jack@example.com,AU,2023-05-20,false,bronze
11,Karen Moore,karen@example.com,US,2023-06-01,true,gold
12,Leo Taylor,leo@example.com,US,2023-06-15,true,silver
13,Mia Anderson,mia@example.com,DE,2023-07-01,true,platinum
14,Noah Thomas,noah@example.com,FR,2023-07-10,true,bronze
15,Olivia Jackson,olivia@example.com,US,2023-07-20,true,silver
16,Paul Harris,paul@example.com,UK,2023-08-01,false,bronze
17,Quinn Martin,quinn@example.com,CA,2023-08-10,true,gold
18,Rachel Garcia,rachel@example.com,MX,2023-08-20,true,silver
19,Sam Robinson,alice@example.com,US,2023-09-01,true,silver
20,Tina Clark,tina@example.com,AU,2023-09-15,true,platinum
"""
# Note: row 19 has same email as row 1 (alice@example.com) — intentional for
# unique test demonstration.  Row 19 tier changed from gold→silver for SCD demo.

RAW_PRODUCTS = """\
product_id,name,category,price_cents,is_active
P001,Laptop Pro 15,Electronics,149999,true
P002,Wireless Mouse,Electronics,2999,true
P003,USB-C Hub,Electronics,4999,true
P004,Standing Desk,Furniture,59999,true
P005,Ergonomic Chair,Furniture,89999,true
P006,Notebook Pack,Stationery,999,true
P007,Pen Set,Stationery,499,true
P008,Monitor 27in,Electronics,39999,true
P009,Keyboard Mech,Electronics,12999,false
P010,Webcam HD,Electronics,7999,true
"""

RAW_ORDERS = """\
order_id,customer_id,product_id,amount_cents,status,order_date,updated_at
O001,1,P001,149999,completed,2023-03-01,2023-03-05
O002,2,P002,2999,completed,2023-03-02,2023-03-03
O003,3,P003,4999,completed,2023-03-10,2023-03-11
O004,4,P004,59999,completed,2023-03-15,2023-03-20
O005,5,P005,89999,cancelled,2023-03-20,2023-03-21
O006,1,P006,999,completed,2023-04-01,2023-04-02
O007,6,P001,149999,completed,2023-04-05,2023-04-10
O008,7,P007,499,completed,2023-04-10,2023-04-11
O009,8,P008,39999,pending,2023-04-15,2023-04-15
O010,9,P009,12999,cancelled,2023-04-20,2023-04-21
O011,10,P010,7999,completed,2023-05-01,2023-05-03
O012,11,P001,149999,completed,2023-05-05,2023-05-10
O013,12,P002,2999,pending,2023-05-10,2023-05-10
O014,13,P003,4999,completed,2023-05-15,2023-05-16
O015,14,P004,59999,completed,2023-05-20,2023-05-25
O016,15,P005,89999,completed,2023-06-01,2023-06-06
O017,16,P006,999,cancelled,2023-06-05,2023-06-06
O018,17,P007,499,completed,2023-06-10,2023-06-11
O019,18,P008,39999,completed,2023-06-15,2023-06-17
O020,19,P009,12999,completed,2023-06-20,2023-06-25
O021,20,P010,7999,completed,2023-07-01,2023-07-03
O022,1,P001,149999,pending,2023-07-05,2023-07-05
O023,2,P003,4999,completed,2023-07-10,2023-07-11
O024,3,P005,89999,cancelled,2023-07-15,2023-07-16
O025,4,P007,499,completed,2022-12-01,2022-12-02
O026,5,P001,149999,completed,2022-11-15,2022-11-20
O027,6,P002,2999,completed,2023-08-01,2023-08-02
O028,7,P004,59999,completed,2023-08-05,2023-08-10
O029,8,P010,7999,pending,2023-08-10,2023-08-10
O030,9,P006,999,completed,2023-08-15,2023-08-16
"""
# Note: O025 and O026 have late-arriving 2022 order_dates (historical records).

RAW_EVENTS = """\
event_id,customer_id,event_type,event_ts,page,session_id
E001,1,page_view,2023-04-01 09:00:00,/home,S001
E002,1,click,2023-04-01 09:01:30,/home,S001
E003,1,page_view,2023-04-01 09:02:00,/products,S001
E004,1,purchase,2023-04-01 09:15:00,/checkout,S001
E005,2,page_view,2023-04-01 10:00:00,/home,S002
E006,2,signup,2023-04-01 10:05:00,/register,S002
E007,3,page_view,2023-04-02 08:30:00,/products,S003
E008,3,click,2023-04-02 08:35:00,/products/P001,S003
E009,4,page_view,2023-04-02 11:00:00,/home,S004
E010,4,purchase,2023-04-02 11:20:00,/checkout,S004
E011,5,page_view,2023-04-03 09:00:00,/home,S005
E012,5,click,2023-04-03 09:05:00,/products,S005
E013,6,signup,2023-04-03 10:00:00,/register,S006
E014,6,page_view,2023-04-03 10:01:00,/home,S006
E015,7,page_view,2023-04-04 09:00:00,/products,S007
E016,7,purchase,2023-04-04 09:30:00,/checkout,S007
E017,8,page_view,2023-04-04 14:00:00,/home,S008
E018,8,click,2023-04-04 14:05:00,/products/P002,S008
E019,9,page_view,2023-04-05 09:00:00,/home,S009
E020,9,click,2023-04-05 09:10:00,/products,S009
E021,10,page_view,2023-04-05 11:00:00,/home,S010
E022,10,signup,2023-04-05 11:05:00,/register,S010
E023,11,page_view,2023-04-06 09:00:00,/home,S011
E024,11,purchase,2023-04-06 09:45:00,/checkout,S011
E025,12,page_view,2023-04-06 13:00:00,/products,S012
E026,12,click,2023-04-06 13:10:00,/products/P005,S012
E027,13,page_view,2023-04-07 09:00:00,/home,S013
E028,13,click,2023-04-07 09:05:00,/products,S013
E029,14,signup,2023-04-07 10:00:00,/register,S014
E030,14,page_view,2023-04-07 10:01:00,/home,S014
E031,15,page_view,2023-04-08 09:00:00,/products,S015
E032,15,purchase,2023-04-08 09:20:00,/checkout,S015
E033,16,page_view,2023-04-08 14:00:00,/home,S016
E034,16,click,2023-04-08 14:15:00,/products/P003,S016
E035,17,page_view,2023-04-09 09:00:00,/home,S017
E036,17,purchase,2023-04-09 09:40:00,/checkout,S017
E037,18,page_view,2023-04-09 11:00:00,/home,S018
E038,18,click,2023-04-09 11:10:00,/products,S018
E039,19,page_view,2023-04-10 09:00:00,/home,S019
E040,20,purchase,2023-04-10 10:00:00,/checkout,S020
"""

RAW_PAYMENTS = """\
payment_id,order_id,amount_cents,payment_method,paid_at,status
PAY001,O001,149999,credit_card,2023-03-05 10:00:00,completed
PAY002,O002,2999,paypal,2023-03-03 11:00:00,completed
PAY003,O003,4999,credit_card,2023-03-11 09:00:00,completed
PAY004,O004,59999,bank_transfer,2023-03-20 14:00:00,completed
PAY005,O006,999,credit_card,2023-04-02 10:00:00,completed
PAY006,O007,149999,credit_card,2023-04-10 11:00:00,completed
PAY007,O008,499,paypal,2023-04-11 09:00:00,completed
PAY008,O011,7999,credit_card,2023-05-03 10:00:00,completed
PAY009,O012,149999,bank_transfer,2023-05-10 14:00:00,completed
PAY010,O014,4999,credit_card,2023-05-16 09:00:00,completed
PAY011,O015,59999,credit_card,2023-05-25 10:00:00,completed
PAY012,O016,89999,bank_transfer,2023-06-06 14:00:00,completed
PAY013,O018,499,paypal,2023-06-11 09:00:00,completed
PAY014,O019,39999,credit_card,2023-06-17 11:00:00,completed
PAY015,O020,12999,credit_card,2023-06-25 10:00:00,completed
PAY016,O021,7999,paypal,2023-07-03 09:00:00,completed
PAY017,O023,4999,credit_card,2023-07-11 10:00:00,completed
PAY018,O025,499,bank_transfer,2022-12-02 09:00:00,completed
PAY019,O026,149999,credit_card,2022-11-20 14:00:00,completed
PAY020,O027,2999,paypal,2023-08-02 10:00:00,completed
PAY021,O028,59999,bank_transfer,2023-08-10 14:00:00,completed
PAY022,O030,999,credit_card,2023-08-16 09:00:00,completed
PAY023,O001,0,refund,2023-03-10 10:00:00,refunded
PAY024,O007,0,refund,2023-04-12 11:00:00,refunded
PAY025,O012,149999,credit_card,2023-05-11 10:00:00,completed
"""
# Note: PAY023 and PAY024 have amount_cents=0 — the assert_positive_amounts
# singular test will catch these.  Intentional teaching material.


# ── Seed writer ────────────────────────────────────────────────────────────────

def write_seed_files() -> None:
    """Write CSV seed files to lab_dbt_project/seeds/ if they don't exist."""
    seeds_dir = DBT_PROJECT_DIR / "seeds"
    seeds_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "raw_customers.csv": RAW_CUSTOMERS,
        "raw_products.csv":  RAW_PRODUCTS,
        "raw_orders.csv":    RAW_ORDERS,
        "raw_events.csv":    RAW_EVENTS,
        "raw_payments.csv":  RAW_PAYMENTS,
    }
    for fname, content in files.items():
        path = seeds_dir / fname
        path.write_text(content, encoding="utf-8")
        print(f"  Wrote: {path}")


def main() -> int:
    print("=" * 60)
    print("  dbt Lab — Seed Setup")
    print("=" * 60)

    # Step 1: Write CSV seed files
    print("\n[1/4] Writing seed CSV files...")
    write_seed_files()

    # Step 2: Write profiles.yml
    print("\n[2/4] Writing profiles.yml...")
    try:
        write_profiles_yml()
    except Exception as e:
        print(f"  ERROR: {e}")
        print("FAIL")
        return 1

    # Step 3: dbt deps (install packages — empty packages.yml so this is fast)
    print("\n[3/4] Running dbt deps...")
    rc, stdout, stderr = run_dbt(["deps"], timeout=120)
    output = (stdout + "\n" + stderr).strip()
    for line in output.splitlines()[-5:]:
        print(f"  {line}")
    if rc != 0:
        print(f"  WARNING: dbt deps returned rc={rc} — continuing anyway (may be OK with empty packages.yml)")

    # Step 4: dbt seed
    print("\n[4/4] Running dbt seed...")
    rc, stdout, stderr = run_dbt(["seed", "--full-refresh"], timeout=180)
    output = (stdout + "\n" + stderr).strip()
    for line in output.splitlines()[-20:]:
        print(f"  {line}")

    if rc != 0:
        print(f"\n  ERROR: dbt seed failed (rc={rc})")
        print("FAIL")
        return 1

    # Verify: print row counts using DuckDB / backend
    print("\n--- Seed Row Counts ---")
    backend, _ = detect_backend()
    if backend == "duckdb":
        try:
            import duckdb
            from _dbt_lane_connect import _duckdb_path
            db_path = _duckdb_path()
            con = duckdb.connect(db_path, read_only=True)
            tables = [
                "raw_customers", "raw_orders", "raw_events",
                "raw_products", "raw_payments"
            ]
            # dbt seeds into schema named by +schema: raw → dbt_lab_raw
            for t in tables:
                for schema in ("dbt_lab_raw", "raw", "main"):
                    try:
                        row = con.execute(
                            f"SELECT COUNT(*) FROM {schema}.{t}"
                        ).fetchone()
                        print(f"  {schema}.{t}: {row[0]} rows")
                        break
                    except Exception:
                        continue
            con.close()
        except Exception as e:
            print(f"  (Could not query row counts: {e})")
    else:
        print("  (Row count verification skipped for non-DuckDB backend)")

    print()
    print("PASS — dbt lab seeded successfully")
    print("Next: python 01_dbt_basics/01_project_init_and_profiles.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
