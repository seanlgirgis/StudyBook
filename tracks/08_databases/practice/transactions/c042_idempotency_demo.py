# Story:
# This file shows how to prevent duplicate processing.
# It matters because retries and duplicate requests happen in real systems.
# Expect second run to skip the transfer.

from common.demo_output import print_accounts
from common.db_session import open_writer_session


def _process_transfer(request_id, sender_account_name, receiver_account_name, transfer_amount):
    # Step 3:
    # Open a transaction so the check and transfer stay atomic.
    writer_session = open_writer_session()
    try:
        with writer_session.cursor() as cur:
            # Step 4:
            # Ensure the idempotency table exists for tracking processed requests.
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_requests (
                    request_id TEXT PRIMARY KEY
                );
                """
            )

            # Step 5:
            # Try to claim this request id first.
            # If we succeed, we are the only worker allowed to process it.
            # If we fail, someone else already processed it.
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
                # Step 6:
                # Skip the transfer if another worker already claimed it.
                print("Already processed")
                writer_session.commit()
                return

            # Step 7:
            # Execute the transfer only once when the request is newly claimed.
            cur.execute(
                "UPDATE accounts SET balance = balance - %s WHERE name = %s;",
                (transfer_amount, sender_account_name),
            )
            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE name = %s;",
                (transfer_amount, receiver_account_name),
            )

        # Step 9:
        # Commit the transfer and the idempotency marker together.
        writer_session.commit()
        print("Success")
    except Exception:
        # Step 10:
        # Roll back if anything fails to keep the state consistent.
        writer_session.rollback()
        raise
    finally:
        # Step 11:
        # Close the session after each attempt.
        writer_session.close()


def run_idempotency_demo():
    # Step 1:
    # Define the request and transfer details once so we can replay them.
    request_id = "transfer-001"
    sender_account_name = "Alice"
    receiver_account_name = "Bob"
    transfer_amount = 100

    # Step 2:
    # Teaching demos must reset their world because stale state misleads learners.
    reset_session = open_writer_session()
    try:
        with reset_session.cursor() as cur:
            # Step 3:
            # Clear old request ids so retries are evaluated fairly.
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_requests (
                    request_id TEXT PRIMARY KEY
                );
                """
            )
            cur.execute("DELETE FROM processed_requests;")

            # Step 4:
            # Reset balances so the demo starts from a deterministic baseline.
            cur.execute(
                "UPDATE accounts SET balance = %s WHERE name = %s;",
                (1000, sender_account_name),
            )
            cur.execute(
                "UPDATE accounts SET balance = %s WHERE name = %s;",
                (1000, receiver_account_name),
            )
            cur.execute("DELETE FROM accounts WHERE name = 'Charlie';")
        reset_session.commit()
    finally:
        reset_session.close()

    # Step 5:
    # Show balances before any processing to establish the baseline.
    print_accounts("Before transfer")

    print(f"Processing request {request_id}")
    _process_transfer(
        request_id,
        sender_account_name,
        receiver_account_name,
        transfer_amount,
    )

    # Step 12:
    # Replay the same request id to prove the operation is idempotent.
    print(f"Processing request {request_id} again")
    _process_transfer(
        request_id,
        sender_account_name,
        receiver_account_name,
        transfer_amount,
    )

    # Step 13:
    # Show balances after both attempts to confirm no double-apply.
    print_accounts("After transfer")


if __name__ == "__main__":
    # Step 14:
    # Run the idempotency demo directly.
    run_idempotency_demo()

# Takeaway:
# Idempotency ensures retries do not apply the same change twice.
