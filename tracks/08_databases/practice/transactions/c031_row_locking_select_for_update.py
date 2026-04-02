# Story:
# This file shows row-level locking with SELECT ... FOR UPDATE.
# It matters because locks prevent two writers from stomping the same row.
# Expect Session B to wait until Session A commits.

import threading
import time

from common.demo_output import print_accounts
from common.demo_reset import reset_accounts
from common.db_session import open_writer_session


def run_row_locking_demo():
    # Step 1:
    # Reset the world so the demo starts clean.
    reset_accounts()

    # Step 2:
    # Open two writer sessions to simulate two actors.
    session_a = open_writer_session()
    session_b = open_writer_session()

    try:
        # Step 3:
        # Session A locks Alice with SELECT ... FOR UPDATE and holds the lock.
        with session_a.cursor() as cur_a:
            cur_a.execute(
                "SELECT id, name, balance FROM accounts WHERE name = 'Alice' FOR UPDATE;"
            )
            print("Session A locked Alice")

        # Step 4:
        # Session B tries to update Alice and should block until the lock is released.
        def session_b_update():
            with session_b.cursor() as cur_b:
                print("Session B attempting update...")
                print("Session B is waiting...")
                start_time = time.time()
                cur_b.execute(
                    "UPDATE accounts SET balance = 500 WHERE name = 'Alice';"
                )
                elapsed = time.time() - start_time
                print(f"Session B update completed after {elapsed:.2f}s")
            session_b.commit()
            print("Session B updated Alice")

        # Step 5:
        # Run Session B in a background thread so the wait is visible.
        thread = threading.Thread(target=session_b_update)
        thread.start()

        # Step 6:
        # Hold the lock for a moment, then commit to release it.
        time.sleep(2.5)
        session_a.commit()
        print("Session A committed")

        # Step 7:
        # Wait for Session B to finish and show final balances.
        thread.join()
        print_accounts("Final state:")
    finally:
        # Step 8:
        # Close both sessions.
        session_b.close()
        session_a.close()


if __name__ == "__main__":
    # Step 9:
    # Run the row locking demo directly.
    run_row_locking_demo()

# Takeaway:
# FOR UPDATE makes one writer wait so two updates don't collide.

