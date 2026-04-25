# SQLAlchemy for Data Engineers — ChatGPT Project Prompts

Priority: 🟠 Important — the standard Python database abstraction layer, used in Citi pipeline

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: SQLAlchemy for Data Engineers
Slug: sqlalchemy
Extra coverage required: what SQLAlchemy is — two layers: Core (SQL expression language) and ORM (object-relational mapper) — data engineers primarily use Core,
engine and connection — create_engine, connection string formats for Oracle, SQL Server, PostgreSQL, SQLite,
cx_Oracle and pyodbc — native drivers that SQLAlchemy wraps, when you need them installed separately,
connection string patterns — dialect+driver://user:password@host:port/dbname — Oracle, SQL Server, PostgreSQL variants,
connection pooling — why it matters for pipelines that run many queries, pool_size, max_overflow, pool_recycle,
executing SQL — text(), conn.execute(), parameterized queries — never string-formatting SQL (SQL injection),
reading results — fetchall, fetchmany, fetchone, CursorResult — mapping to dicts and DataFrames,
pandas read_sql — using an engine directly with pd.read_sql_query() and pd.read_sql_table(),
pandas to_sql — writing DataFrames to a database table, if_exists parameter (replace/append/fail), chunksize,
transactions — conn.begin(), commit, rollback — when to use explicit transaction control in ETL,
metadata and table reflection — Table, MetaData, autoload_with — inspecting existing database schemas,
upsert patterns — INSERT OR REPLACE in SQLite, ON CONFLICT DO UPDATE in PostgreSQL, merge in Oracle,
connection context manager — with engine.connect() as conn — ensuring connections are closed,
environment variables for credentials — never hardcoding passwords, os.environ, .env files with python-dotenv,
handling large result sets — server-side cursors, yield_per, streaming large Oracle query results,
real scenario: extracting P95 telemetry from Oracle and enrichment data from SQL Server in the Citi pipeline.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug sqlalchemy -ChunkSize 750
```

Upload final_sqlalchemy.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_sqlalchemy.mp3` is live on R2.

```
Topic: SQLAlchemy for Data Engineers
Slug: sqlalchemy
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_sqlalchemy.mp3
Today's date: 2026-04-25

Content sections — create exactly these, in this order:
Engine & Connection | Connection Strings (Oracle / SQL Server / PostgreSQL) | Connection Pooling | Executing SQL Safely | Pandas Integration (read_sql & to_sql) | Transactions | Upsert Patterns | Secrets & Credentials | Large Result Sets
Then add: Interview Q&A (6 pairs) | Quick Reference (12-15 rows)
Size per section: 2-3 tight paragraphs, one code block max (20 lines). No tutorials.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\sqlalchemy.html
