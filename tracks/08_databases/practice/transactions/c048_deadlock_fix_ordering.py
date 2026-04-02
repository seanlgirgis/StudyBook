# Story:
# This file shows how consistent lock ordering prevents deadlocks.
# It matters because the simplest fix is often the best fix.
# Expect both transactions to succeed without deadlock.

import threading

from common.db_session import open_connection


def _setup_resources():
    session = open_connection()
    try:
        with session.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS deadlock_resources (
                    id INTEGER PRIMARY KEY,
                    resource_name TEXT NOT NULL
                );
                """
            )
            cur.execute("DELETE FROM deadlock_resources;")
            cur.execute(
                """
                INSERT INTO deadlock_resources (id, resource_name)
                VALUES (1, 'Resource A'), (2, 'Resource B');
                """
            )
        session.commit()
    finally:
        session.close()


def _lock_in_order(worker_name, first_id, second_id, barrier):
    session = open_connection()
    try:
        with session.cursor() as cur:
            # Step 1:
            # Wait so both workers start together.
            barrier.wait()

            # Step 2:
            # Lock resources in the same order for everyone.
            cur.execute(
                "SELECT id FROM deadlock_resources WHERE id = %s FOR UPDATE;",
                (first_id,),
            )
            print(f"{worker_name} locked {first_id}")
            cur.execute(
                "SELECT id FROM deadlock_resources WHERE id = %s FOR UPDATE;",
                (second_id,),
            )
            print(f"{worker_name} locked {second_id}")

        session.commit()
        print(f"{worker_name} committed")
    finally:
        session.close()


def run_deadlock_fix_demo():
    # Step 0:
    # Reset the world so the demo is deterministic.
    _setup_resources()

    barrier = threading.Barrier(2)

    # Step 3:
    # Both workers lock A then B, so there is no deadlock.
    t1 = threading.Thread(target=_lock_in_order, args=("T1", 1, 2, barrier))
    t2 = threading.Thread(target=_lock_in_order, args=("T2", 1, 2, barrier))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    # Step 4:
    # Run the deadlock fix demo directly.
    run_deadlock_fix_demo()

# Takeaway:
# Consistent lock ordering turns deadlocks into simple blocking.
