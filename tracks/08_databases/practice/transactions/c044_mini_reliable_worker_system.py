# Story:
# This file shows a mini worker system that is reliable under failure.
# It matters because real queues have retries, duplicates, and poison jobs.
# Expect normal jobs to finish, one job to fail into the DLQ, and a duplicate request to skip.

import threading

from common.db_session import open_writer_session


def _print_jobs(label):
    session = open_writer_session()
    try:
        with session.cursor() as cur:
            cur.execute(
                """
                SELECT id, task_name, request_id, status, attempt_count
                FROM jobs
                ORDER BY id;
                """
            )
            rows = cur.fetchall()
        print(label)
        for row in rows:
            print(row)
    finally:
        session.close()


def _print_dead_letter_jobs(label):
    session = open_writer_session()
    try:
        with session.cursor() as cur:
            cur.execute(
                """
                SELECT id, original_job_id, task_name, request_id, final_error, failed_at
                FROM dead_letter_jobs
                ORDER BY id;
                """
            )
            rows = cur.fetchall()
        print(label)
        for row in rows:
            print(row)
    finally:
        session.close()


def _print_processed_requests(label):
    session = open_writer_session()
    try:
        with session.cursor() as cur:
            cur.execute("SELECT request_id FROM processed_requests ORDER BY request_id;")
            rows = cur.fetchall()
        print(label)
        for row in rows:
            print(row)
    finally:
        session.close()


def _worker_loop(worker_name, max_attempts):
    # Step 6:
    # Each worker keeps its own session and claims jobs with row locks.
    worker_session = open_writer_session()
    try:
        while True:
            with worker_session.cursor() as cur:
                # Step 7:
                # Claim the next queued job without blocking other workers.
                cur.execute(
                    """
                    SELECT id, task_name, request_id, attempt_count
                    FROM jobs
                    WHERE status = 'queued'
                    ORDER BY id
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1;
                    """
                )
                row = cur.fetchone()

                if row is None:
                    worker_session.commit()
                    break

                job_id, task_name, request_id, attempt_count = row
                print(f"{worker_name} claiming {task_name}")

                # Step 8:
                # Mark the job in progress inside the same transaction.
                cur.execute(
                    "UPDATE jobs SET status = 'in_progress' WHERE id = %s;",
                    (job_id,),
                )

                try:
                    if task_name == "job_fail":
                        # Step 9:
                        # Force the poison job to fail every time.
                        raise RuntimeError("Poison job failure")

                    if request_id:
                        # Step 10:
                        # Try to claim the request id so duplicates do not process twice.
                        cur.execute(
                            """
                            INSERT INTO processed_requests (request_id)
                            VALUES (%s)
                            ON CONFLICT DO NOTHING
                            RETURNING request_id;
                            """,
                            (request_id,),
                        )
                        claimed_request = cur.fetchone() is not None

                        if not claimed_request:
                            # Step 11:
                            # Skip work when the request id was already processed.
                            cur.execute(
                                "UPDATE jobs SET status = 'skipped' WHERE id = %s;",
                                (job_id,),
                            )
                            worker_session.commit()
                            print(f"{worker_name} duplicate request skipped: {request_id}")
                            continue

                    # Step 12:
                    # Successful jobs are marked done.
                    cur.execute(
                        "UPDATE jobs SET status = 'done' WHERE id = %s;",
                        (job_id,),
                    )
                    worker_session.commit()
                    print(f"{worker_name} {task_name} -> success")
                except Exception as exc:
                    # Step 13:
                    # Roll back so the failed attempt leaves no partial state.
                    worker_session.rollback()

                    with worker_session.cursor() as retry_cur:
                        next_attempt = attempt_count + 1
                        retry_cur.execute(
                            "UPDATE jobs SET attempt_count = %s WHERE id = %s;",
                            (next_attempt, job_id),
                        )

                        print(
                            f"{worker_name} {task_name} -> failure attempt {next_attempt}"
                        )

                        if next_attempt >= max_attempts:
                            # Step 14:
                            # Move the poison job to the DLQ after max attempts.
                            retry_cur.execute(
                                """
                                INSERT INTO dead_letter_jobs (
                                    original_job_id,
                                    task_name,
                                    request_id,
                                    final_error
                                )
                                VALUES (%s, %s, %s, %s);
                                """,
                                (job_id, task_name, request_id, str(exc)),
                            )
                            retry_cur.execute("DELETE FROM jobs WHERE id = %s;", (job_id,))
                            worker_session.commit()
                            print(f"Moved {task_name} to dead letter queue")
                        else:
                            # Step 15:
                            # Put the job back in the queue for another try.
                            retry_cur.execute(
                                "UPDATE jobs SET status = 'queued' WHERE id = %s;",
                                (job_id,),
                            )
                            worker_session.commit()
    finally:
        worker_session.close()


def run_mini_reliable_worker_system():
    # Step 1:
    # Reset the demo tables so stale data does not mislead the lesson.
    setup_session = open_writer_session()
    try:
        with setup_session.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    request_id TEXT UNIQUE,
                    status TEXT NOT NULL,
                    attempt_count INTEGER NOT NULL DEFAULT 0
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_requests (
                    request_id TEXT PRIMARY KEY
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS dead_letter_jobs (
                    id SERIAL PRIMARY KEY,
                    original_job_id INTEGER,
                    task_name TEXT NOT NULL,
                    request_id TEXT,
                    final_error TEXT NOT NULL,
                    failed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            # Step 2:
            # Ensure missing columns exist if a prior demo created the tables.
            cur.execute(
                """
                ALTER TABLE jobs
                ADD COLUMN IF NOT EXISTS request_id TEXT;
                """
            )
            cur.execute(
                """
                ALTER TABLE jobs
                ADD COLUMN IF NOT EXISTS attempt_count INTEGER NOT NULL DEFAULT 0;
                """
            )
            cur.execute(
                """
                ALTER TABLE dead_letter_jobs
                ADD COLUMN IF NOT EXISTS request_id TEXT;
                """
            )

            # Step 3:
            # Clear previous rows so the demo starts from a clean baseline.
            cur.execute("DELETE FROM dead_letter_jobs;")
            cur.execute("DELETE FROM processed_requests;")
            cur.execute("DELETE FROM jobs;")

            # Step 4:
            # Seed the queue and a duplicate request id to prove idempotency.
            cur.execute(
                """
                INSERT INTO jobs (task_name, request_id, status)
                VALUES
                    ('job_1', 'req_1', 'queued'),
                    ('job_2', 'req_dup', 'queued'),
                    ('job_fail', 'req_fail', 'queued'),
                    ('job_4', 'req_4', 'queued');
                """
            )
            cur.execute(
                "INSERT INTO processed_requests (request_id) VALUES (%s);",
                ("req_dup",),
            )
        setup_session.commit()
    finally:
        setup_session.close()

    max_attempts = 3

    # Step 5:
    # Show the initial queue so we can see what workers will process.
    _print_jobs("Initial jobs")

    workers = []
    for index in range(2):
        worker = threading.Thread(
            target=_worker_loop,
            args=(f"Worker-{index + 1}", max_attempts),
        )
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()

    # Step 16:
    # Show the final tables to confirm retries, DLQ, and idempotency.
    _print_jobs("Final jobs")
    _print_dead_letter_jobs("Dead letter jobs")
    _print_processed_requests("Processed requests")


if __name__ == "__main__":
    # Step 17:
    # Run the mini reliable worker system directly.
    run_mini_reliable_worker_system()

# Takeaway:
# Reliable workers claim jobs safely, retry carefully, and isolate poison work.
