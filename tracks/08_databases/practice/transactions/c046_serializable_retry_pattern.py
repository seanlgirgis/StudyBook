# Story:
# This file shows how SERIALIZABLE prevents write skew by forcing a retry.
# It matters because correctness sometimes requires aborting a transaction.
# Expect one doctor to retry and the rule to hold.

import threading

import psycopg2

from common.db_session import open_connection


def _setup_on_call_table():
    session = open_connection()
    try:
        with session.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS on_call_doctors (
                    doctor_name TEXT PRIMARY KEY,
                    on_call BOOLEAN NOT NULL
                );
                """
            )
            cur.execute("DELETE FROM on_call_doctors;")
            cur.execute(
                """
                INSERT INTO on_call_doctors (doctor_name, on_call)
                VALUES
                    ('Dr. Alpha', TRUE),
                    ('Dr. Beta', TRUE);
                """
            )
        session.commit()
    finally:
        session.close()


def _serializable_attempt(doctor_name, barrier, attempt):
    session = open_connection("SERIALIZABLE")
    try:
        with session.cursor() as cur:
            # Step 1:
            # Each doctor checks how many people are on call.
            cur.execute(
                "SELECT COUNT(*) FROM on_call_doctors WHERE on_call = TRUE;"
            )
            (on_call_count,) = cur.fetchone()
            print(f"{doctor_name} sees {on_call_count} doctors on call")

            # Step 2:
            # Sync only on the first attempt so we hit the conflict.
            if attempt == 1:
                barrier.wait()

            if on_call_count > 1:
                # Step 3:
                # Try to go off-call if someone else is still on call.
                cur.execute(
                    "UPDATE on_call_doctors SET on_call = FALSE WHERE doctor_name = %s;",
                    (doctor_name,),
                )
                print(f"{doctor_name} attempts to go off call")

        session.commit()
        return True
    finally:
        session.close()


def _doctor_with_retry(doctor_name, barrier, max_attempts):
    # Step 4:
    # SERIALIZABLE may abort, so we retry with a clean transaction.
    for attempt in range(1, max_attempts + 1):
        try:
            success = _serializable_attempt(doctor_name, barrier, attempt)
            if success:
                print(f"{doctor_name} commit success on attempt {attempt}")
                return
        except psycopg2.Error as exc:
            if exc.pgcode == "40001":
                print(f"{doctor_name} serialization failure, retrying")
                continue
            raise


def run_serializable_retry_demo():
    # Step 0:
    # Reset the world so the demo is deterministic.
    _setup_on_call_table()

    barrier = threading.Barrier(2)
    max_attempts = 3

    # Step 5:
    # Run two concurrent doctors on SERIALIZABLE with retries.
    t1 = threading.Thread(
        target=_doctor_with_retry, args=("Dr. Alpha", barrier, max_attempts)
    )
    t2 = threading.Thread(
        target=_doctor_with_retry, args=("Dr. Beta", barrier, max_attempts)
    )
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Step 6:
    # Show the rule holds: at least one doctor stays on call.
    session = open_connection()
    try:
        with session.cursor() as cur:
            cur.execute(
                "SELECT doctor_name, on_call FROM on_call_doctors ORDER BY doctor_name;"
            )
            rows = cur.fetchall()
        print("Final on-call status")
        for row in rows:
            print(row)
    finally:
        session.close()


if __name__ == "__main__":
    # Step 7:
    # Run the serializable retry demo directly.
    run_serializable_retry_demo()

# Takeaway:
# Serializable isolation preserves the rule by aborting unsafe interleavings.
