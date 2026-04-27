#!/usr/bin/env python3
"""Pipeline: connect to Postgres, create table, insert one run record, print rows."""

import os
import socket
import psycopg2

def main():
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pipeline_runs (
                    id SERIAL PRIMARY KEY,
                    run_name TEXT NOT NULL,
                    container_name TEXT NOT NULL DEFAULT 'unknown',
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            cur.execute("""
                ALTER TABLE pipeline_runs
                ADD COLUMN IF NOT EXISTS container_name TEXT DEFAULT 'unknown';
            """)
            cur.execute(
                """
                INSERT INTO pipeline_runs (run_name, container_name)
                VALUES (%s, %s)
                RETURNING id, run_name, container_name, created_at;
                """,
                ("pipeline_wrote_to_postgres", socket.gethostname()),
            )
            print(f"Inserted row: {cur.fetchone()}")

            cur.execute("""
                SELECT id, run_name, container_name, created_at
                FROM pipeline_runs
                ORDER BY id DESC
                LIMIT 5;
            """)
            print("Latest pipeline rows:")
            for row in cur.fetchall():
                print(row)

    conn.close()

if __name__ == "__main__":
    main()
