# Story:
# This file shows how to retry when a deadlock happens.
# It matters because deadlocks are normal under concurrency.
# Expect a deadlock, then a clean retry that succeeds.

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


def _attempt_lock(worker_name, first_id, second_id, barrier, attempt):
    session = open_connection()
    try:
        with session.cursor() as cur:
            # Step 1:
            # Lock the first resource.
            cur.execute(
                "SELECT id FROM deadlock_resources WHERE id = %s FOR UPDATE;",
                (first_id,),
            )
            print(f"{worker_name} attempt {attempt} locked {first_id}")

            # Step 2:
            # Sync on the first attempt to force a deadlock.
            if attempt == 1:
                barrier.wait()

            # Step 3:
            # Try to lock the second resource.
            cur.execute(
                "SELECT id FROM deadlock_resources WHERE id = %s FOR UPDATE;",
                (second_id,),
            )
            print(f"{worker_name} attempt {attempt} locked {second_id}")

        session.commit()
        print(f"{worker_name} attempt {attempt} committed")
        return True
    finally:
        session.close()


def _worker_with_retry(worker_name, first_id, second_id, barrier, max_attempts):
    # Step 4:
    # Retry the transaction if the database reports a deadlock.
    for attempt in range(1, max_attempts + 1):
        try:
            if _attempt_lock(worker_name, first_id, second_id, barrier, attempt):
                return
        except psycopg2.Error as exc:
            if exc.pgcode == "40P01":
                print(f"{worker_name} deadlock detected, retrying")
                continue
            raise


def run_deadlock_retry_demo():
    # Step 0:
    # Reset the world so the demo is deterministic.
    _setup_resources()

    barrier = threading.Barrier(2)
    max_attempts = 3

    # Step 5:
    # Lock in opposite order to trigger a deadlock, then retry.
    t1 = threading.Thread(
        target=_worker_with_retry, args=("T1", 1, 2, barrier, max_attempts)
    )
    t2 = threading.Thread(
        target=_worker_with_retry, args=("T2", 2, 1, barrier, max_attempts)
    )
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    # Step 6:
    # Run the deadlock retry demo directly.
    run_deadlock_retry_demo()

# Takeaway:
# Deadlocks are resolved by aborting one transaction, so retries are mandatory.
