# Story:
# This file shows that PostgreSQL blocks dirty reads.
# It matters because seeing uncommitted data is how bugs and fraud happen.
# Expect the reader to see the old committed balance, not the writer's private change.

from common.demo_output import print_accounts
from common.demo_reset import reset_accounts
from common.db_session import open_reader_session, open_writer_session


def run_dirty_read_protection_demo():
    # Step 1:
    # Reset the world so the demo is clean.
    reset_accounts()

    # Step 2:
    # Show the starting balances.
    print_accounts("Starting state")

    # Step 3:
    # Open two sessions: one writer, one reader.
    writer_session = open_writer_session()
    reader_session = open_reader_session()
    uncommitted_balance_value = 500

    try:
        # Step 4:
        # Writer changes Alice but keeps it private by not committing.
        with writer_session.cursor() as writer_cur:
            writer_cur.execute(
                "UPDATE accounts SET balance = %s WHERE name = 'Alice';",
                (uncommitted_balance_value,),
            )
            print(
                "Session A updated Alice to",
                uncommitted_balance_value,
                "but did NOT commit.",
            )

        # Step 5:
        # Reader checks Alice and should still see the old committed value.
        with reader_session.cursor() as reader_cur:
            reader_cur.execute(
                "SELECT balance FROM accounts WHERE name = 'Alice';"
            )
            observed_balance = reader_cur.fetchone()[0]
            print("Session B reads Alice balance:", observed_balance)

        # Step 6:
        # Roll back the writer's private change.
        writer_session.rollback()
        print("Session A rolled back the uncommitted change.")
    finally:
        # Step 7:
        # Close both sessions.
        reader_session.close()
        writer_session.close()

    # Step 8:
    # Show the final balances.
    print_accounts("Final state")


if __name__ == "__main__":
    # Step 9:
    # Run the dirty read protection demo directly.
    run_dirty_read_protection_demo()

# Takeaway:
# Uncommitted work stays private; dirty reads are blocked.

