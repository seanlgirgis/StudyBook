# Story:
# This file is a quick X-ray of the accounts table.
# It matters because you need to see reality before and after each demo.
# Expect a simple list of Alice and Bob balances.

from common.demo_output import print_accounts


def show_current_state():
    # Step 1:
    # Print the current balances so you know the baseline.
    print_accounts("Current state")


if __name__ == "__main__":
    # Step 2:
    # Run the snapshot directly when executed.
    show_current_state()

# Takeaway:
# Always check the state before you trust a story about it.

