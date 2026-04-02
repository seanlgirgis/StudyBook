# Story:
# This file shows a clean, successful money transfer inside one transaction.
# It matters because this is the baseline behavior everything else is compared to.
# Expect Alice to go down, Bob to go up, and both changes to land together.

from common.demo_output import print_accounts
from common.db_session import open_writer_session


def run_transfer_happy_path():
    # Step 1:
    # Define the actors and the transfer amount so the intent is explicit.
    sender_account_name = "Alice"
    receiver_account_name = "Bob"
    transfer_amount = 100

    # Step 2:
    # Show the world before the transfer so the change is obvious.
    print_accounts("Before transfer")

    # Step 3:
    # Open a writer session and do both updates inside one transaction.
    transfer_writer_session = open_writer_session()
    try:
        with transfer_writer_session.cursor() as cur:
            # Step 4:
            # Subtract from the sender.
            cur.execute(
                "UPDATE accounts SET balance = balance - %s WHERE name = %s;",
                (transfer_amount, sender_account_name),
            )
            # Step 5:
            # Add to the receiver.
            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE name = %s;",
                (transfer_amount, receiver_account_name),
            )
        # Step 6:
        # Commit so both updates become real at the same time.
        transfer_writer_session.commit()
    finally:
        # Step 7:
        # Close the session cleanly.
        transfer_writer_session.close()

    # Step 8:
    # Show the world after the transfer.
    print_accounts("After transfer")


if __name__ == "__main__":
    # Step 9:
    # Run the happy path demo directly.
    run_transfer_happy_path()

# Takeaway:
# A transaction keeps the transfer atomic: both sides move together or not at all.

