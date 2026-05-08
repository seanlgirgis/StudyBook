import os
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, text


DB_PORT = 5432
DB_NAME = "studybook"
DB_USER = "sb_user"
DB_PASSWORD = "sb_pass_123"
"""
        here are two read paths and two write paths. `pd.read_sql_query()` reads database query 
        results into a DataFrame. `pd.read_csv()` or `pd.read_excel()` reads file exports like 
        BMC telemetry exports. `df.to_csv()` or `df.to_excel()` writes report files. `df.to_sql()` 
        writes a DataFrame to a database table. For safety, I read raw telemetry as a protected 
        source and write cleaned or summarized outputs to separate report files or 
        staging/gold tables.
"""

def get_database_url() -> str:
    """Build SQLAlchemy DB URL, allowing DB_HOST override via env var."""
    # If running directly on Windows instead of inside a container,
    # DB_HOST may need to be set to "localhost".
    db_host = os.getenv("DB_HOST", "host.docker.internal")
    password_encoded = quote_plus(DB_PASSWORD)
    return (
        f"postgresql+psycopg2://{DB_USER}:{password_encoded}"
        f"@{db_host}:{DB_PORT}/{DB_NAME}"
    )


def get_engine():
    """Create and return a SQLAlchemy engine."""
    return create_engine(get_database_url())


def run_sql(sql: str) -> pd.DataFrame:
    """Run SELECT SQL and return result as DataFrame."""
    """
        I generally keep the source telemetry layer read-only from analysis scripts. 
        The Python code runs SELECT queries, loads data into Pandas, and creates derived
        outputs like flags, summaries, reports, or curated tables. If I need to write 
        results, I prefer writing to a separate output table or report layer rather 
        than mutating the raw telemetry source. That keeps the bronze layer auditable 
        and makes the pipeline safer.
    """
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(text(sql), conn)


def smoke_test() -> pd.DataFrame:
    """Run a minimal DB connectivity test query."""
    sql = "SELECT current_database(), current_user, now();"
    return run_sql(sql)
