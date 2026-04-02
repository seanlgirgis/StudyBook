# Story:
# This file shows what to do with a job that keeps failing.
# It matters because infinite retries waste resources and jam the system.
# Expect one poison job to be retried, then moved out of the main queue.

from common.db_session import open_writer_session


def _print_jobs(label):
    session = open_writer_session()
    try:
        with session.cursor() as cur:
            cur.execute(
                "SELECT id, task_name, status, attempt_count FROM jobs ORDER BY id;"
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
                SELECT id, original_job_id, task_name, final_error, failed_at
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


def run_dead_letter_queue_demo():
    # Step 1:
    # Reset the demo tables so stale data does not confuse the lesson.
    setup_session = open_writer_session()
    try:
        with setup_session.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    attempt_count INTEGER NOT NULL DEFAULT 0
                );
                """
            )
            # Step 1a:
            # Ensure the attempt_count column exists if the table was created earlier.
            cur.execute(
                """
                ALTER TABLE jobs
                ADD COLUMN IF NOT EXISTS attempt_count INTEGER NOT NULL DEFAULT 0;
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS dead_letter_jobs (
                    id SERIAL PRIMARY KEY,
                    original_job_id INTEGER,
                    task_name TEXT NOT NULL,
                    final_error TEXT NOT NULL,
                    failed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            cur.execute("DELETE FROM dead_letter_jobs;")
            cur.execute("DELETE FROM jobs;")

            # Step 2:
            # Seed a few jobs, including one poison job that always fails.
            cur.execute(
                """
                INSERT INTO jobs (task_name, status)
                VALUES
                    ('job_1', 'queued'),
                    ('job_2', 'queued'),
                    ('job_fail', 'queued'),
                    ('job_4', 'queued');
                """
            )
        setup_session.commit()
    finally:
        setup_session.close()

    max_attempts = 3

    # Step 3:
    # Show the initial queue so we can see what gets processed.
    _print_jobs("Initial jobs")

    worker_session = open_writer_session()
    try:
        while True:
            with worker_session.cursor() as cur:
                # Step 4:
                # Pull the next queued job to process.
                cur.execute(
                    """
                    SELECT id, task_name, attempt_count
                    FROM jobs
                    WHERE status = 'queued'
                    ORDER BY id
                    LIMIT 1;
                    """
                )
                row = cur.fetchone()

                if row is None:
                    break

                job_id, task_name, attempt_count = row
                next_attempt = attempt_count + 1

                try:
                    if task_name == "job_fail":
                        # Step 5:
                        # Force a failure for the poison job every time.
                        raise RuntimeError("Poison job failure")

                    # Step 6:
                    # Mark successful jobs as done.
                    cur.execute(
                        "UPDATE jobs SET status = 'done' WHERE id = %s;",
                        (job_id,),
                    )
                    worker_session.commit()
                    print(f"Worker processing {task_name} -> success")
                except Exception as exc:
                    # Step 7:
                    # Record the failure attempt and decide whether to retry or dead-letter.
                    cur.execute(
                        "UPDATE jobs SET attempt_count = %s WHERE id = %s;",
                        (next_attempt, job_id),
                    )
                    worker_session.commit()
                    print(
                        f"Worker processing {task_name} -> failure attempt {next_attempt}"
                    )

                    if next_attempt >= max_attempts:
                        # Step 8:
                        # Move the poison job to the dead letter queue after max attempts.
                        with worker_session.cursor() as dlq_cur:
                            dlq_cur.execute(
                                """
                                INSERT INTO dead_letter_jobs (
                                    original_job_id,
                                    task_name,
                                    final_error
                                )
                                VALUES (%s, %s, %s);
                                """,
                                (job_id, task_name, str(exc)),
                            )
                            dlq_cur.execute("DELETE FROM jobs WHERE id = %s;", (job_id,))
                        worker_session.commit()
                        print(f"Moved {task_name} to dead letter queue")
    finally:
        worker_session.close()

    # Step 9:
    # Show remaining jobs and the DLQ to confirm the poison job was isolated.
    _print_jobs("Final jobs")
    _print_dead_letter_jobs("Dead letter jobs")


if __name__ == "__main__":
    # Step 10:
    # Run the demo directly.
    run_dead_letter_queue_demo()

# Takeaway:
# Dead letter queues stop poison jobs from clogging the system.
