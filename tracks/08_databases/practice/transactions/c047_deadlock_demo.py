# Story:
# This file shows a real deadlock between two transactions.
# It matters because deadlocks stop progress even when data is correct.
# Expect one transaction to be aborted by the database.

import threading

import psycopg2

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


def _lock_in_opposite_order(worker_name, first_id, second_id, barrier):
    session = open_connection()
    try:
        with session.cursor() as cur:
            # Step 1:
            # Lock the first resource.
            cur.execute(
                "SELECT id FROM deadlock_resources WHERE id = %s FOR UPDATE;",
                (first_id,),
            )
            print(f"{worker_name} locked {first_id}")

            # Step 2:
            # Wait so both workers hold one lock each.
            barrier.wait()

            # Step 3:
            # Try to lock the second resource (this creates the deadlock).
            cur.execute(
                "SELECT id FROM deadlock_resources WHERE id = %s FOR UPDATE;",
                (second_id,),
            )
            print(f"{worker_name} locked {second_id}")

        session.commit()
        print(f"{worker_name} committed")
    except psycopg2.Error as exc:
        session.rollback()
        print(f"{worker_name} failed with deadlock: {exc.pgcode}")
    finally:
        session.close()


def run_deadlock_demo():
    # Step 0:
    # Reset the world so the demo is deterministic.
    _setup_resources()

    barrier = threading.Barrier(2)

    # Step 4:
    # Lock resources in opposite order to force a deadlock.
    t1 = threading.Thread(
        target=_lock_in_opposite_order, args=("T1", 1, 2, barrier)
    )
    t2 = threading.Thread(
        target=_lock_in_opposite_order, args=("T2", 2, 1, barrier)
    )
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    # Step 5:
    # Run the deadlock demo directly.
    run_deadlock_demo()

# Takeaway:
# A deadlock is a circular wait, so the database kills one transaction to move on.
