# Story:
# This file shows a phantom read under READ COMMITTED.
# It matters because new rows can appear mid-transaction.
# Expect the reader's second query to include an extra row.

from common.demo_reset import reset_accounts
from common.db_session import open_reader_session, open_writer_session


def run_phantom_read_read_committed():
    # Step 1:
    # Reset the world to a known baseline.
    reset_accounts()

    # Step 2:
    # Open reader and writer sessions.
    reader_session = open_reader_session()
    writer_session = open_writer_session()

    try:
        # Step 3:
        # Use READ COMMITTED so each query sees fresh committed data.
        reader_session.set_session(isolation_level="READ COMMITTED")

        # Step 4:
        # Ensure Charlie is not already in the table.
        with writer_session.cursor() as writer_cur:
            writer_cur.execute("DELETE FROM accounts WHERE name = 'Charlie';")
        writer_session.commit()

        # Step 5:
        # Reader runs a range query and captures the first result set.
        with reader_session.cursor() as reader_cur:
            reader_cur.execute(
                "SELECT id, name, balance FROM accounts WHERE balance >= 1000 ORDER BY id;"
            )
            first_rows = reader_cur.fetchall()
            print("Reader first query result:", first_rows)

        # Step 6:
        # Writer inserts a new row that matches the reader's range.
        with writer_session.cursor() as writer_cur:
            writer_cur.execute(
                "INSERT INTO accounts (name, balance) VALUES ('Charlie', 1500);"
            )
        writer_session.commit()
        print("Writer inserted Charlie")

        # Step 7:
        # Reader runs the same range query again and sees the phantom row.
        with reader_session.cursor() as reader_cur:
            reader_cur.execute(
                "SELECT id, name, balance FROM accounts WHERE balance >= 1000 ORDER BY id;"
            )
            second_rows = reader_cur.fetchall()
            print("Reader second query result:", second_rows)
    finally:
        # Step 8:
        # Close both sessions.
        writer_session.close()
        reader_session.close()


if __name__ == "__main__":
    # Step 9:
    # Run the phantom read demo directly.
    run_phantom_read_read_committed()

# Takeaway:
# READ COMMITTED can show new rows between queries in the same transaction.

