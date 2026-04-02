# Story:
# This file builds the tiny world for every scenario: a simple accounts table.
# It matters because every concurrency lesson is garbage if the schema is wrong.
# Expect to see a clean table with Alice and Bob ready for the next scripts.

from common.db_session import open_writer_session


def setup_schema():
    # Step 1:
    # Open a writer session so we can build tables and seed data.
    writer_session = open_writer_session()
    try:
        # Step 2:
        # Create the accounts table from scratch (drop + create) to avoid leftovers.
        with writer_session.cursor() as cur:
            cur.execute(
                """
                DROP TABLE IF EXISTS accounts;
                CREATE TABLE IF NOT EXISTS accounts (
                    id SERIAL PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    balance INTEGER NOT NULL
                );
                """
            )
            # Step 3:
            # Seed the two accounts so every demo starts from the same reality.
            cur.execute(
                """
                INSERT INTO accounts (name, balance)
                VALUES ('Alice', 1000), ('Bob', 1000)
                ON CONFLICT (name) DO NOTHING;
                """
            )
        # Step 4:
        # Commit so the table and seed data become real for everyone.
        writer_session.commit()
    finally:
        # Step 5:
        # Always close the session so connections don't leak.
        writer_session.close()


if __name__ == "__main__":
    # Step 6:
    # Run the schema setup directly when this file is executed.
    setup_schema()

# Takeaway:
# Clean schema + known seed data makes every concurrency demo trustworthy.


