# Story:
# This file shows a frozen snapshot under REPEATABLE READ.
# It matters because stability can beat freshness when correctness is king.
# Expect the reader to see the old value even after another session commits.

from common.demo_output import print_accounts
from common.demo_reset import reset_accounts
from common.db_session import open_reader_session, open_writer_session


def run_repeatable_read_snapshot_demo():
    # Step 1:
    # Reset the world and show the starting balances.
    reset_accounts()
    print_accounts("Starting state")

    # Step 2:
    # Open sessions: one frozen reader, one writer, one fresh verifier.
    reader_session = open_reader_session()
    writer_session = open_writer_session()
    verification_session = open_reader_session()

    try:
        # Step 3:
        # Lock the reader into a REPEATABLE READ snapshot.
        reader_session.set_session(isolation_level="REPEATABLE READ")

        # Step 4:
        # Reader takes the first look at Alice.
        with reader_session.cursor() as reader_cur:
            reader_cur.execute(
                "SELECT balance FROM accounts WHERE name = 'Alice';"
            )
            frozen_snapshot_balance = reader_cur.fetchone()[0]
            print("Reader first read:", frozen_snapshot_balance)

        # Step 5:
        # Writer changes Alice and commits.
        with writer_session.cursor() as writer_cur:
            writer_cur.execute(
                "UPDATE accounts SET balance = 700 WHERE name = 'Alice';"
            )
        writer_session.commit()
        print("Writer committed change")

        # Step 6:
        # Reader looks again and still sees the old snapshot value.
        with reader_session.cursor() as reader_cur:
            reader_cur.execute(
                "SELECT balance FROM accounts WHERE name = 'Alice';"
            )
            frozen_snapshot_balance = reader_cur.fetchone()[0]
            print("Reader second read:", frozen_snapshot_balance)

        # Step 7:
        # A fresh session sees the new committed value.
        with verification_session.cursor() as verify_cur:
            verify_cur.execute(
                "SELECT balance FROM accounts WHERE name = 'Alice';"
            )
            committed_new_balance = verify_cur.fetchone()[0]
            print("Fresh session reads Alice balance:", committed_new_balance)
    finally:
        # Step 8:
        # Close all sessions.
        verification_session.close()
        writer_session.close()
        reader_session.close()

    # Step 9:
    # Show the final balances.
    print_accounts("Final state")


if __name__ == "__main__":
    # Step 10:
    # Run the repeatable read demo directly.
    run_repeatable_read_snapshot_demo()

# Takeaway:
# REPEATABLE READ gives you consistency even when the world changes.

