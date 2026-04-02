from .db_session import open_writer_session


def reset_accounts():
    writer_session = open_writer_session()
    try:
        with writer_session.cursor() as cur:
            cur.execute(
                "UPDATE accounts SET balance = 1000 WHERE name IN ('Alice', 'Bob');"
            )
        writer_session.commit()
    finally:
        writer_session.close()
