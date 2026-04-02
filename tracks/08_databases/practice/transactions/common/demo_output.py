from .db_session import open_reader_session


def fetch_accounts():
    reader_session = open_reader_session()
    try:
        with reader_session.cursor() as cur:
            cur.execute("SELECT id, name, balance FROM accounts ORDER BY id;")
            rows = cur.fetchall()
        return rows
    finally:
        reader_session.close()


def print_accounts(label):
    print(label)
    for row in fetch_accounts():
        print(row)
