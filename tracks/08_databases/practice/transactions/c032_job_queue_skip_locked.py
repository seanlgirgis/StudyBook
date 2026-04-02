# Story:
# This file shows a simple job queue using FOR UPDATE SKIP LOCKED.
# It matters because multiple workers can process jobs in parallel without collisions.
# Expect each job to be picked once, with no blocking between workers.

import random
import threading
import time

from common.db_session import open_reader_session, open_writer_session


TOTAL_JOBS = 10
WORKER_COUNT = 3


def setup_jobs():
    # Step 1:
    # Create the jobs table and reset it to a clean set of pending jobs.
    writer_session = open_writer_session()
    try:
        with writer_session.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    status TEXT NOT NULL
                );
                """
            )
            cur.execute("DELETE FROM jobs;")
            for i in range(1, TOTAL_JOBS + 1):
                cur.execute(
                    "INSERT INTO jobs (task_name, status) VALUES (%s, 'pending');",
                    (f"job_{i}",),
                )
        # Step 2:
        # Commit the seed data so workers see the same queue.
        writer_session.commit()
    finally:
        # Step 3:
        # Close the session.
        writer_session.close()


def print_jobs(label):
    # Step 4:
    # Print the current job table state for visibility.
    reader_session = open_reader_session()
    try:
        print(label)
        with reader_session.cursor() as cur:
            cur.execute("SELECT task_name, status FROM jobs ORDER BY id;")
            rows = cur.fetchall()
            for task_name, status in rows:
                print(f"{task_name} {status}")
    finally:
        reader_session.close()


def worker_loop(worker_id):
    # Step 5:
    # Each worker grabs one job at a time and loops until none remain.
    writer_session = open_writer_session()
    try:
        while True:
            with writer_session.cursor() as cur:
                # Step 6:
                # SKIP LOCKED means: don't wait, just skip rows another worker is holding.
                cur.execute(
                    """
                    SELECT id, task_name
                    FROM jobs
                    WHERE status = 'pending'
                    ORDER BY id
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1;
                    """
                )
                row = cur.fetchone()
                if not row:
                    # Step 7:
                    # No jobs left for this worker.
                    writer_session.commit()
                    print(f"Worker {worker_id} No jobs left")
                    break

                # Step 8:
                # Claim the job by marking it processing.
                job_id, task_name = row
                print(f"Worker {worker_id} picked {task_name}")
                cur.execute(
                    "UPDATE jobs SET status = 'processing' WHERE id = %s;",
                    (job_id,),
                )

            # Step 9:
            # Simulate doing the work.
            time.sleep(random.uniform(1.0, 2.0))

            with writer_session.cursor() as cur:
                # Step 10:
                # Mark the job done and commit.
                cur.execute(
                    "UPDATE jobs SET status = 'done' WHERE id = %s;",
                    (job_id,),
                )
            writer_session.commit()
    finally:
        # Step 11:
        # Close the worker session.
        writer_session.close()


def run_skip_locked_demo():
    # Step 12:
    # Set up jobs and show the starting queue.
    setup_jobs()
    print_jobs("Initial jobs:")

    # Step 13:
    # Start multiple workers in parallel.
    threads = []
    for worker_id in range(1, WORKER_COUNT + 1):
        thread = threading.Thread(target=worker_loop, args=(worker_id,))
        thread.start()
        threads.append(thread)

    # Step 14:
    # Wait for all workers to finish.
    for thread in threads:
        thread.join()

    # Step 15:
    # Show the final queue state.
    print_jobs("Final jobs:")


if __name__ == "__main__":
    # Step 16:
    # Run the skip locked demo directly.
    run_skip_locked_demo()

# Takeaway:
# SKIP LOCKED lets workers move fast without stepping on each other.

