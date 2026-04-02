import psycopg2
from psycopg2 import extensions

from .env_loader import load_env_config

_ISOLATION_LEVELS = {
    "READ COMMITTED": extensions.ISOLATION_LEVEL_READ_COMMITTED,
    "REPEATABLE READ": extensions.ISOLATION_LEVEL_REPEATABLE_READ,
    "SERIALIZABLE": extensions.ISOLATION_LEVEL_SERIALIZABLE,
}


def open_connection(isolation_level=None):
    config = load_env_config()
    conn = psycopg2.connect(
        host="localhost",
        port=config["POSTGRES_PORT"],
        database=config["POSTGRES_DB"],
        user=config["POSTGRES_USER"],
        password=config["POSTGRES_PASSWORD"],
    )
    conn.autocommit = False

    if isolation_level:
        level = _ISOLATION_LEVELS.get(isolation_level)
        if level is None:
            raise ValueError(f"Unsupported isolation_level: {isolation_level}")
        conn.set_isolation_level(level)

    return conn


def open_reader_session():
    reader_session = open_connection()
    return reader_session


def open_writer_session():
    writer_session = open_connection()
    return writer_session
