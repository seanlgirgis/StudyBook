# Story:
# This file shows a non-repeatable read under READ COMMITTED.
# It matters because your view can change inside one transaction.
# Expect the reader to see Alice change between two reads.

from common.demo_reset import reset_accounts
from common.db_session import open_reader_session, open_writer_session


def run_non_repeatable_read_demo():
    # Step 1:
    # Reset the world to a known baseline.
    reset_accounts()

    # Step 2:
    # Open reader and writer sessions.
    reader_session = open_reader_session()
    writer_session = open_writer_session()

    try:
        # Step 3:
        # Use READ COMMITTED so each query sees the latest committed data.
        reader_session.set_session(isolation_level="READ COMMITTED")

        # Step 4:
        # Reader takes the first look at Alice.
        with reader_session.cursor() as reader_cur:
            reader_cur.execute(
                "SELECT balance FROM accounts WHERE name = 'Alice';"
            )
            first_balance = reader_cur.fetchone()[0]
            print("Reader first read:", first_balance)

        # Step 5:
        # Writer changes Alice and commits.
        with writer_session.cursor() as writer_cur:
            writer_cur.execute(
                "UPDATE accounts SET balance = 700 WHERE name = 'Alice';"
            )
        writer_session.commit()
        print("Writer committed change")

        # Step 6:
        # Reader looks again and sees a different value.
        with reader_session.cursor() as reader_cur:
            reader_cur.execute(
                "SELECT balance FROM accounts WHERE name = 'Alice';"
            )
            second_balance = reader_cur.fetchone()[0]
            print("Reader second read:", second_balance)
    finally:
        # Step 7:
        # Close both sessions.
        writer_session.close()
        reader_session.close()


if __name__ == "__main__":
    # Step 8:
    # Run the non-repeatable read demo directly.
    run_non_repeatable_read_demo()

# Takeaway:
# READ COMMITTED allows the world to change between reads.

