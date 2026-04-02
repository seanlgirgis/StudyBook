# Story:
# This file shows how a failed transaction can be retried safely.
# It matters because real systems fail all the time.
# Expect first attempt to fail, second to succeed cleanly.

from common.demo_output import print_accounts
from common.db_session import open_writer_session


def run_retry_demo():
    # Step 1:
    # Define who is moving money and how much so the retry is repeatable.
    sender_account_name = "Alice"
    receiver_account_name = "Bob"
    transfer_amount = 100
    simulated_failure_message = "Simulated failure after debiting sender"
    max_attempts = 2

    # Step 2:
    # Show the starting balances to prove we begin from a clean state.
    print_accounts("Before transfer")

    for attempt in range(1, max_attempts + 1):
        # Step 3:
        # Announce the attempt so the retry flow is visible.
        print(f"Attempt {attempt}...")

        writer_session = open_writer_session()
        try:
            with writer_session.cursor() as cur:
                # Step 4:
                # Debit first to simulate the risky halfway point.
                cur.execute(
                    "UPDATE accounts SET balance = balance - %s WHERE name = %s;",
                    (transfer_amount, sender_account_name),
                )

                if attempt == 1:
                    # Step 5:
                    # Force a crash after the debit to trigger a rollback.
                    raise RuntimeError(simulated_failure_message)

                # Step 6:
                # Credit the receiver on the successful retry.
                cur.execute(
                    "UPDATE accounts SET balance = balance + %s WHERE name = %s;",
                    (transfer_amount, receiver_account_name),
                )

            # Step 7:
            # Commit only after the full transfer succeeds.
            writer_session.commit()
            print("Success")
            break
        except Exception as exc:
            # Step 8:
            # Roll back so the failed attempt leaves no partial state.
            writer_session.rollback()
            print(f"Failure: {exc}")
            if attempt < max_attempts:
                print("Retrying...")
        finally:
            # Step 9:
            # Close the session to avoid leaking connections.
            writer_session.close()

    # Step 10:
    # Show the balances after the retry to confirm a clean outcome.
    print_accounts("After transfer")


if __name__ == "__main__":
    # Step 11:
    # Run the retry demo directly.
    run_retry_demo()

# Takeaway:
# Retry is safe only because rollback erased the failed attempt.
