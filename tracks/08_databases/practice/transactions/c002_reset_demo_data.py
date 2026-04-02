# Story:
# This file resets the world so every demo starts from the same balances.
# It matters because stale data makes you chase the wrong bug.
# Expect Alice and Bob to be set back to 1000 every time.

from common.demo_reset import reset_accounts


def reset_demo_data():
    # Step 1:
    # Reset the accounts to a clean baseline.
    reset_accounts()


if __name__ == "__main__":
    # Step 2:
    # Run the reset directly when executed.
    reset_demo_data()

# Takeaway:
# A clean starting state makes every result trustworthy.

