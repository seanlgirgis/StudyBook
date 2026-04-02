# Story:
# This file shows how REPEATABLE READ prevents phantom reads in your session.
# It matters because stable ranges stop surprise rows from appearing.
# Expect the reader to see the same result set both times.

from common.demo_reset import reset_accounts
from common.db_session import open_reader_session, open_writer_session


def run_phantom_read_repeatable_read():
    # Step 1:
    # Reset the world to a known baseline.
    reset_accounts()

    # Step 2:
    # Open reader, writer, and fresh verification sessions.
    reader_session = open_reader_session()
    writer_session = open_writer_session()
    verification_session = open_reader_session()

    try:
        # Step 3:
        # Lock the reader into a REPEATABLE READ snapshot.
        reader_session.set_session(isolation_level="REPEATABLE READ")

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
        # Writer inserts a new row that would match the reader's range.
        with writer_session.cursor() as writer_cur:
            writer_cur.execute(
                "INSERT INTO accounts (name, balance) VALUES ('Charlie', 1500);"
            )
        writer_session.commit()
        print("Writer inserted Charlie")

        # Step 7:
        # Reader runs the same query again and should see the same snapshot.
        with reader_session.cursor() as reader_cur:
            reader_cur.execute(
                "SELECT id, name, balance FROM accounts WHERE balance >= 1000 ORDER BY id;"
            )
            second_rows = reader_cur.fetchall()
            print("Reader second query result:", second_rows)

        # Step 8:
        # A fresh session confirms the new row exists outside the snapshot.
        with verification_session.cursor() as verify_cur:
            verify_cur.execute(
                "SELECT id, name, balance FROM accounts WHERE balance >= 1000 ORDER BY id;"
            )
            verify_rows = verify_cur.fetchall()
            print("Fresh session result:", verify_rows)
    finally:
        # Step 9:
        # Close all sessions.
        verification_session.close()
        writer_session.close()
        reader_session.close()


if __name__ == "__main__":
    # Step 10:
    # Run the repeatable read phantom demo directly.
    run_phantom_read_repeatable_read()

# Takeaway:
# REPEATABLE READ keeps your range stable even when new rows appear.

