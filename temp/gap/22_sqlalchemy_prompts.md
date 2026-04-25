# SQLAlchemy for Data Engineers — ChatGPT Project Prompts

Priority: 🟠 Important — the standard Python database abstraction layer, used in Citi pipeline

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: SQLAlchemy for Data Engineers
Slug: sqlalchemy

Extra coverage required:
- What SQLAlchemy is — two layers: Core (SQL expression language) and ORM (object-relational mapper); data engineers primarily use Core for query execution and connection management
- Engine and connection — create_engine() is the entry point; connection string format: dialect+driver://user:password@host:port/dbname; engine is lazy, connection pool is managed automatically
- Native drivers — cx_Oracle for Oracle, pyodbc for SQL Server, psycopg2 for PostgreSQL; SQLAlchemy wraps these; must be installed separately
- Connection pooling — pool_size (persistent connections), max_overflow (burst connections), pool_recycle (prevents stale connections); critical for pipelines running many queries
- Executing SQL safely — text() for parameterized queries; conn.execute(text("SELECT :val"), {"val": x}); never string-format SQL (SQL injection risk)
- Reading results — fetchall(), fetchmany(n), fetchone(); CursorResult rows map to tuples or dicts; converting to DataFrames with pd.DataFrame(result)
- pandas read_sql — pd.read_sql_query(sql, engine) reads directly into a DataFrame; pd.read_sql_table() for full table reads; engine is passed directly
- pandas to_sql — df.to_sql(name, engine, if_exists='replace'|'append'|'fail', chunksize=1000); chunksize prevents OOM on large writes
- Transactions — with conn.begin() as txn: groups multiple statements; explicit commit/rollback; essential for ETL stages that must succeed or fail atomically
- Upsert patterns — INSERT ... ON CONFLICT DO UPDATE in PostgreSQL; MERGE in Oracle; SQLAlchemy Core dialect-specific constructs for each
- Connection context manager — with engine.connect() as conn: ensures connection is always returned to pool; with engine.begin() also commits/rolls back automatically
- Credentials from environment — never hardcode passwords; os.environ or python-dotenv; connection string assembled at runtime from env vars
- Large result sets — server-side cursors with yield_per() for streaming Oracle queries without loading all rows into memory

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. Core vs ORM — what data engineers actually use
  2. Engine, Connection Strings & Native Drivers
  3. Connection Pooling — sizing for pipelines
  4. Executing SQL Safely — text() & parameterized queries
  5. Reading Results & pandas read_sql
  6. pandas to_sql — writing DataFrames to databases
  7. Transactions & Context Managers
  8. Upsert Patterns (PostgreSQL / Oracle / SQL Server)
  9. Secrets, Credentials & Large Result Sets
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs; include a code block where it adds value (20 lines max)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\sqlalchemy.html
