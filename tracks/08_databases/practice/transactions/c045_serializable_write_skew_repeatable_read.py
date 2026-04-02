# Story:
# This file shows a rule that breaks under weaker isolation.
# It matters because two "correct" actions can still corrupt a system.
# Expect both doctors to go off-call under REPEATABLE READ.

import threading

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


def _doctor_turns_off(doctor_name, ready_barrier):
    session = open_connection("REPEATABLE READ")
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
            # Pause so both doctors decide based on the same snapshot.
            ready_barrier.wait()

            if on_call_count > 1:
                # Step 3:
                # Turn off if someone else is still on call.
                cur.execute(
                    "UPDATE on_call_doctors SET on_call = FALSE WHERE doctor_name = %s;",
                    (doctor_name,),
                )
                print(f"{doctor_name} goes off call")
        session.commit()
    finally:
        session.close()


def run_repeatable_read_write_skew_demo():
    # Step 0:
    # Reset the world so the demo is deterministic.
    _setup_on_call_table()

    barrier = threading.Barrier(2)

    # Step 4:
    # Run two concurrent doctors on REPEATABLE READ.
    t1 = threading.Thread(target=_doctor_turns_off, args=("Dr. Alpha", barrier))
    t2 = threading.Thread(target=_doctor_turns_off, args=("Dr. Beta", barrier))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Step 5:
    # Show the broken rule: zero doctors left on call.
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
    # Step 6:
    # Run the repeatable read failure demo directly.
    run_repeatable_read_write_skew_demo()

# Takeaway:
# Weaker isolation can let correct-looking actions create a broken global state.
