"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-01 · Seed Lab Environment                                         ║
║  Creates all tables, indexes, and sample data for every nugget.              ║
║  IDEMPOTENT — safe to run multiple times.                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Creates the pg_lab schema with realistic DE data:
  - customers      (10 rows)
  - products       (8 rows)
  - orders         (50 rows with realistic patterns)
  - order_items    (120 rows)
  - events         (200 rows — clickstream-style)
  - employees      (15 rows — for SCD Type 2 demo)
  - employees_hist (SCD Type 2 history table)
  - transactions   (100 rows — for concurrency demo)

USAGE
─────
    python 01_seed_lab.py          # Create + seed
    python 01_seed_lab.py --reset   # Drop everything + recreate
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema


def drop_all(conn):
    """Drop all lab objects in dependency order."""
    with conn.cursor() as cur:
        cur.execute(f"SET search_path TO {LAB_SCHEMA}")
        # Drop in reverse dependency order
        for name in [
            "order_items", "orders", "events", "employees_hist",
            "employees", "transactions", "products", "customers",
            "gold_daily_metrics", "gold_customer_lifetime_value",
            "silver_orders", "silver_customers",
        ]:
            cur.execute(f"DROP TABLE IF EXISTS {name} CASCADE")
        for name in ["gold_customer_summary"]:
            cur.execute(f"DROP MATERIALIZED VIEW IF EXISTS {name} CASCADE")
        conn.commit()
    print("    Dropped all lab objects.")


def create_tables(conn):
    """Create all lab tables with realistic schema."""
    with conn.cursor() as cur:
        cur.execute(f"SET search_path TO {LAB_SCHEMA}")

        # ── Customers ─────────────────────────────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id   SERIAL PRIMARY KEY,
                first_name    VARCHAR(50)    NOT NULL,
                last_name     VARCHAR(50)    NOT NULL,
                email         VARCHAR(100)   UNIQUE NOT NULL,
                city          VARCHAR(50),
                country       VARCHAR(50)    DEFAULT 'US',
                signup_date   DATE           NOT NULL DEFAULT CURRENT_DATE,
                is_active     BOOLEAN        DEFAULT true,
                created_at    TIMESTAMP      DEFAULT NOW()
            )
        """)

        # ── Products ──────────────────────────────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id    SERIAL PRIMARY KEY,
                name          VARCHAR(100)   NOT NULL,
                category      VARCHAR(50)    NOT NULL,
                price         NUMERIC(10,2)  NOT NULL CHECK (price > 0),
                cost          NUMERIC(10,2)  NOT NULL CHECK (cost > 0),
                is_active     BOOLEAN        DEFAULT true,
                created_at    TIMESTAMP      DEFAULT NOW()
            )
        """)

        # ── Orders ────────────────────────────────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id      SERIAL PRIMARY KEY,
                customer_id   INT            NOT NULL REFERENCES customers(customer_id),
                order_date    DATE           NOT NULL,
                status        VARCHAR(20)    DEFAULT 'pending'
                              CHECK (status IN ('pending','confirmed','shipped','delivered','cancelled')),
                total_amount  NUMERIC(12,2),
                created_at    TIMESTAMP      DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_orders_customer
                ON orders(customer_id)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_orders_date
                ON orders(order_date)
        """)

        # ── Order Items ───────────────────────────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                item_id       SERIAL PRIMARY KEY,
                order_id      INT            NOT NULL REFERENCES orders(order_id),
                product_id    INT            NOT NULL REFERENCES products(product_id),
                quantity      INT            NOT NULL CHECK (quantity > 0),
                unit_price    NUMERIC(10,2)  NOT NULL,
                line_total    NUMERIC(12,2)  GENERATED ALWAYS AS (quantity * unit_price) STORED
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_items_order
                ON order_items(order_id)
        """)

        # ── Events (clickstream-style) ────────────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id      BIGSERIAL PRIMARY KEY,
                customer_id   INT            REFERENCES customers(customer_id),
                event_type    VARCHAR(30)    NOT NULL,
                page_url      VARCHAR(200),
                event_time    TIMESTAMP      NOT NULL DEFAULT NOW(),
                session_id    VARCHAR(50),
                device        VARCHAR(20)    DEFAULT 'desktop'
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_customer
                ON events(customer_id)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_time
                ON events(event_time)
        """)

        # ── Employees (for SCD Type 2 demo) ───────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                emp_id        SERIAL PRIMARY KEY,
                name          VARCHAR(100)   NOT NULL,
                department    VARCHAR(50)    NOT NULL,
                salary        NUMERIC(10,2)  NOT NULL,
                start_date    DATE           NOT NULL DEFAULT CURRENT_DATE,
                is_current    BOOLEAN        DEFAULT true
            )
        """)

        # ── Employees History (SCD Type 2) ────────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees_hist (
                hist_id       SERIAL PRIMARY KEY,
                emp_id        INT            NOT NULL,
                name          VARCHAR(100)   NOT NULL,
                department    VARCHAR(50)    NOT NULL,
                salary        NUMERIC(10,2)  NOT NULL,
                valid_from    DATE           NOT NULL,
                valid_to      DATE,
                is_current    BOOLEAN        DEFAULT true
            )
        """)

        # ── Transactions (for concurrency demo) ───────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                txn_id        SERIAL PRIMARY KEY,
                account_id    INT            NOT NULL,
                amount        NUMERIC(12,2)  NOT NULL,
                txn_type      VARCHAR(10)    CHECK (txn_type IN ('debit','credit')),
                txn_time      TIMESTAMP      DEFAULT NOW(),
                balance_after NUMERIC(12,2)
            )
        """)

        # ── Gold layer tables (for capstone) ──────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS gold_daily_metrics (
                metric_date   DATE           PRIMARY KEY,
                order_count   INT            DEFAULT 0,
                revenue       NUMERIC(14,2)  DEFAULT 0,
                avg_order     NUMERIC(10,2)  DEFAULT 0,
                unique_cust   INT            DEFAULT 0
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS gold_customer_lifetime_value (
                customer_id   INT            PRIMARY KEY REFERENCES customers(customer_id),
                customer_name VARCHAR(101),
                total_orders  INT            DEFAULT 0,
                total_spent   NUMERIC(14,2)  DEFAULT 0,
                avg_order     NUMERIC(10,2)  DEFAULT 0,
                first_order   DATE,
                last_order    DATE
            )
        """)

        conn.commit()
    print("    Created 10 tables + 5 indexes.")


def seed_data(conn):
    """Insert realistic sample data from a clean baseline."""
    with conn.cursor() as cur:
        cur.execute(f"SET search_path TO {LAB_SCHEMA}")

        # Always reseed from a clean baseline so reruns are deterministic.
        # This is what makes the script truly idempotent for a lab setup.
        cur.execute(f"""
            TRUNCATE TABLE
                order_items,
                orders,
                events,
                employees_hist,
                employees,
                transactions,
                products,
                customers
            RESTART IDENTITY CASCADE
        """)
        conn.commit()

        # ── Customers ─────────────────────────────────────────────────────
        customers = [
            ('Alice',   'Johnson',  'alice@example.com',   'Dallas',     'US', '2023-01-15'),
            ('Bob',     'Smith',    'bob@example.com',     'Austin',     'US', '2023-02-20'),
            ('Carol',   'White',    'carol@example.com',   'Houston',    'US', '2023-03-10'),
            ('David',   'Brown',    'david@example.com',   'Chicago',    'US', '2023-04-05'),
            ('Eva',     'Martinez', 'eva@example.com',     'Miami',      'US', '2023-05-12'),
            ('Frank',   'Lee',      'frank@example.com',   'Seattle',    'US', '2023-06-18'),
            ('Grace',   'Kim',      'grace@example.com',   'New York',   'US', '2023-07-22'),
            ('Henry',   'Wilson',   'henry@example.com',   'Denver',     'US', '2023-08-30'),
            ('Iris',    'Chen',     'iris@example.com',    'San Jose',   'US', '2023-09-14'),
            ('Jack',    'Taylor',   'jack@example.com',    'Phoenix',    'US', '2023-10-01'),
        ]
        cur.executemany("""
            INSERT INTO customers (first_name, last_name, email, city, country, signup_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
        """, customers)

        # ── Products ──────────────────────────────────────────────────────
        products = [
            ('Laptop Pro 15',    'Electronics', 1299.99, 800.00),
            ('Wireless Mouse',   'Accessories',   29.99,  12.00),
            ('USB-C Hub',        'Accessories',   49.99,  20.00),
            ('Gaming Keyboard',  'Electronics',   89.99,  45.00),
            ('Monitor 27"',      'Electronics',  349.99, 200.00),
            ('Webcam HD',        'Accessories',   59.99,  25.00),
            ('Desk Lamp',        'Office',        24.99,  10.00),
            ('Standing Desk',    'Office',       499.99, 300.00),
        ]
        cur.executemany("""
            INSERT INTO products (name, category, price, cost)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, products)

        # ── Orders (50 orders over 30 days) ───────────────────────────────
        import random
        random.seed(42)  # Deterministic

        statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        status_weights = [0.1, 0.15, 0.25, 0.4, 0.1]

        orders_data = []
        for i in range(50):
            cust_id = random.randint(1, 10)
            day = random.randint(1, 30)
            order_date = f"2024-01-{day:02d}"
            status = random.choices(statuses, weights=status_weights, k=1)[0]
            orders_data.append((cust_id, order_date, status))

        cur.executemany("""
            INSERT INTO orders (customer_id, order_date, status)
            VALUES (%s, %s, %s)
        """, orders_data)

        # ── Order Items (~120 items) ──────────────────────────────────────
        items_data = []
        # After RESTART IDENTITY, newly inserted orders are 1..50.
        for order_id in range(1, 51):
            n_items = random.randint(1, 4)
            for _ in range(n_items):
                prod_id = random.randint(1, 8)
                qty = random.randint(1, 5)
                # Get the product price
                cur.execute("SELECT price FROM products WHERE product_id = %s", (prod_id,))
                price = cur.fetchone()[0]
                items_data.append((order_id, prod_id, qty, float(price)))

        cur.executemany("""
            INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
        """, items_data)

        # Update order totals
        cur.execute("""
            UPDATE orders o
            SET total_amount = sub.total
            FROM (
                SELECT order_id, SUM(line_total) AS total
                FROM order_items
                GROUP BY order_id
            ) sub
            WHERE o.order_id = sub.order_id
        """)

        # ── Events (200 clickstream events) ───────────────────────────────
        event_types = ['page_view', 'product_view', 'add_to_cart', 'checkout', 'purchase']
        devices = ['desktop', 'mobile', 'tablet']
        pages = ['/home', '/products', '/product/1', '/product/2', '/cart', '/checkout', '/confirm']

        events_data = []
        for i in range(200):
            cust_id = random.randint(1, 10) if random.random() > 0.1 else None
            etype = random.choices(event_types, weights=[0.4, 0.25, 0.15, 0.1, 0.1], k=1)[0]
            page = random.choice(pages)
            day = random.randint(1, 30)
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            event_time = f"2024-01-{day:02d} {hour:02d}:{minute:02d}:00"
            session = f"sess_{random.randint(1, 50):03d}"
            device = random.choice(devices)
            events_data.append((cust_id, etype, page, event_time, session, device))

        cur.executemany("""
            INSERT INTO events (customer_id, event_type, page_url, event_time, session_id, device)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, events_data)

        # ── Employees ─────────────────────────────────────────────────────
        employees = [
            ('Alice Johnson',  'Engineering', 95000, '2022-01-15'),
            ('Bob Smith',      'Engineering', 88000, '2022-03-01'),
            ('Carol White',    'Sales',       72000, '2022-06-10'),
            ('David Brown',    'Marketing',   68000, '2023-01-20'),
            ('Eva Martinez',   'Engineering', 102000, '2021-09-05'),
        ]
        cur.executemany("""
            INSERT INTO employees (name, department, salary, start_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, employees)

        # ── Employees History (SCD Type 2 seed) ───────────────────────────
        hist_data = [
            (1, 'Alice Johnson',  'Engineering', 90000, '2022-01-15', '2023-06-01', False),
            (1, 'Alice Johnson',  'Engineering', 95000, '2023-06-01', None,         True),
            (2, 'Bob Smith',      'Engineering', 88000, '2022-03-01', None,         True),
            (3, 'Carol White',    'Sales',       72000, '2022-06-10', None,         True),
        ]
        cur.executemany("""
            INSERT INTO employees_hist (emp_id, name, department, salary, valid_from, valid_to, is_current)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, hist_data)

        # ── Transactions (100 rows for concurrency demo) ──────────────────
        txn_data = []
        for i in range(100):
            acct = random.randint(1, 10)
            amount = round(random.uniform(10, 500), 2)
            txn_type = random.choice(['debit', 'credit'])
            day = random.randint(1, 30)
            hour = random.randint(0, 23)
            txn_time = f"2024-01-{day:02d} {hour:02d}:{random.randint(0,59):02d}:00"
            txn_data.append((acct, amount, txn_type, txn_time))

        cur.executemany("""
            INSERT INTO transactions (account_id, amount, txn_type, txn_time)
            VALUES (%s, %s, %s, %s)
        """, txn_data)

        conn.commit()

    # Print counts
    with conn.cursor() as cur:
        cur.execute(f"SET search_path TO {LAB_SCHEMA}")
        for table in ['customers', 'products', 'orders', 'order_items',
                       'events', 'employees', 'employees_hist', 'transactions']:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"    {table:<20} {count} rows")


def main():
    parser = argparse.ArgumentParser(description="Seed PostgreSQL lab environment.")
    parser.add_argument("--reset", action="store_true", help="Drop everything and recreate.")
    args = parser.parse_args()

    print("\n── Seed Lab Environment ──────────────────────────")

    conn = get_connection()
    ensure_lab_schema(conn)

    if args.reset:
        print("\n  Resetting lab environment...")
        drop_all(conn)

    print("\n  Creating tables...")
    create_tables(conn)

    print("\n  Seeding data (deterministic reseed)...")
    seed_data(conn)

    conn.close()
    print("\n  Lab environment ready!")
    print(f"  Schema: {LAB_SCHEMA}")
    print()


if __name__ == "__main__":
    main()
