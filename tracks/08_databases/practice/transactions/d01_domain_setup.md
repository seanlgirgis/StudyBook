# Domain Setup

## What We Are Modeling
A tiny bank ledger with two accounts: Alice and Bob. Each scenario moves money between them and checks the results. The goal is to see how transaction isolation changes what different sessions can observe.

## Data Model
We use a single table, `accounts`:
- `id`: surrogate primary key
- `name`: unique account name
- `balance`: integer balance

## Why This Matters
When two sessions run at the same time, the isolation level determines:
- what data is visible before a transaction commits
- whether repeated reads see the same values
- whether new rows can appear mid-transaction

This folder builds a reusable set of scripts to demonstrate those behaviors in a controlled, repeatable way.

