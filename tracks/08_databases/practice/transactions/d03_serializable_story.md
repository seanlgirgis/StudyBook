# Serializable Isolation — Story Map

## Story
Two doctors are on call. Each doctor is allowed to go off-call only if **someone else** is still on call.

## Scenario
Both doctors check the on-call list at the same time.
They both see “2 doctors are on-call,” so both decide to go off.

## Failure (Weaker Isolation)
Under REPEATABLE READ, both transactions can commit.
Result: **0 doctors on-call** — the rule is broken.

## Fix (Serializable)
Under SERIALIZABLE, one transaction is aborted.
Result: **1 doctor stays on-call** — the rule holds.

## Why This Matters
This is a classic “write skew” bug:
- each transaction is locally correct
- global rule still breaks

Serializable prevents this by forcing a retry.

## Mental Model
Serializable = “as if transactions ran one-by-one.”
If the database cannot make the interleaving safe,
it forces one transaction to abort so you can retry.

## Run Order
1. c045_serializable_write_skew_repeatable_read.py
2. c046_serializable_retry_pattern.py
