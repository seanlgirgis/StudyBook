# Story:
# This file shows a transfer that fails mid-flight and gets rolled back.
# It matters because partial updates are how systems go broke.
# Expect Alice to stay the same because the transaction is canceled.

from common.demo_output import print_accounts
from common.db_session import open_writer_session


def run_transfer_rollback_demo():
    # Step 1:
    # Define the actors and the transfer amount.
    sender_account_name = "Alice"
    receiver_account_name = "Bob"
    transfer_amount = 100
    simulated_failure_message = "Simulated failure after debiting sender"

    # Step 2:
    # Show the world before the transfer.
    print_accounts("Before transfer")

    # Step 3:
    # Start a transaction that will intentionally fail.
    rollback_writer_session = open_writer_session()
    try:
        with rollback_writer_session.cursor() as cur:
            # Step 4:
            # Debit the sender.
            cur.execute(
                "UPDATE accounts SET balance = balance - %s WHERE name = %s;",
                (transfer_amount, sender_account_name),
            )
            # Step 5:
            # Blow up before crediting the receiver.
            raise RuntimeError(simulated_failure_message)
            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE name = %s;",
                (transfer_amount, receiver_account_name),
            )
        # Step 6:
        # This commit should never happen because we raised an error.
        rollback_writer_session.commit()
    except Exception as exc:
        # Step 7:
        # Roll back so the partial change is erased.
        rollback_writer_session.rollback()
        print(f"Rollback executed: {exc}")
    finally:
        # Step 8:
        # Close the session.
        rollback_writer_session.close()

    # Step 9:
    # Show the world after rollback.
    print_accounts("After rollback")


if __name__ == "__main__":
    # Step 10:
    # Run the rollback demo directly.
    run_transfer_rollback_demo()

# Takeaway:
# Rollback protects you from half-done work.

