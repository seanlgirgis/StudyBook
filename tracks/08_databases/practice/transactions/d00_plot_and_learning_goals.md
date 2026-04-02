# PostgreSQL Transactions Training Plot

# PostgreSQL Transactions Training Plot

## Purpose

This folder is not about memorizing definitions.

This is about **seeing how things break… and why they don’t have to**.

You’re not here to learn “what is a transaction.”
You’re here to understand:

what happens when two things hit the same data at the same time

Because that’s where real systems either:

* behave correctly
* or quietly corrupt your data

---

## Scenario Story (The Real Way to Think About It)

We’re running a tiny system.

Nothing fancy. Just:

* Alice
* Bob
* Money moving between them

Looks simple, right?

Now add reality:

* two sessions
* two users
* same data
* same time

Now things get interesting.

---

### Scene 1 — Happy Path

Alice sends money to Bob.

All good.

Nobody else is touching anything.

Life is easy.

---

### Scene 2 — Something breaks mid-transfer

Money leaves Alice…

Then boom 💥
Process dies.

Now:

* Alice lost money
* Bob didn’t get it

That’s how systems go bankrupt.

---

### Scene 3 — Someone is watching while you work

You update Alice…

But you didn’t commit yet.

Another session reads:

Should they see it?

If yes → chaos
If no → isolation

---

### Scene 4 — World changes under your feet

You read Alice = 1000

Someone commits a change.

You read again:

Now it’s 700

Same transaction. Different reality.

That’s where bugs hide.

---

### Scene 5 — Frozen reality

You say:

"I want stability"

Now:

* you keep seeing 1000
* even though the real world is now 700

You’re consistent… but maybe outdated.

Trade-offs begin here.

---

### Scene 6 — Direct conflict

Two people try to update Alice.

Now the database says:

"Hold on… one at a time"

That’s locking.

---

### Scene 7 — Scaling workers

Now imagine:

* 3 workers
* 10 jobs
* same table

If they wait → slow system
If they collide → duplicate work

So we do:

SKIP LOCKED

Now:

* no waiting
* no duplicates
* real system behavior

---

## What You Should Walk Away With

Not definitions.

But instincts.

You should feel:

* when data is safe
* when it is not

---

## Core Concepts (Street Version)

### Transaction

"Do these steps together or don’t do them at all"

---

### Commit

"This is final. Everyone can see it now"

---

### Rollback

"Forget everything I just did"

---

### Isolation

"What am I allowed to see while others are working?"

---

### READ COMMITTED

"Show me only real data… but keep it fresh every time I look"

👉 Same transaction
👉 Different answers possible

---

### REPEATABLE READ

"Freeze my world when I start"

👉 stable
👉 but possibly outdated

---

### Lock

"I’m working on this — nobody else touch it"

---

### SKIP LOCKED

"If someone is working on it… skip it and keep going"

👉 this is how real systems scale

---

### Serializable

"Make everything behave like it ran one by one"

👉 safest
👉 but expensive
👉 sometimes you must retry

---

## Learning Order

practice/transactions/
d00_plot_and_learning_goals.md
d01_domain_setup.md

c001_setup_schema.py
c002_reset_demo_data.py
c003_show_current_state.py

c011_transfer_happy_path.py
c012_transfer_rollback_demo.py

c021_dirty_read_protection_demo.py
c022_read_committed_non_repeatable_read_demo.py
c023_repeatable_read_snapshot_demo.py

c031_row_locking_select_for_update.py
c032_job_queue_skip_locked.py

common/

---

## Study Rule (Do Not Skip This)

For each script:

1. Read the story (md)
2. Run the code
3. Watch the output
4. Say out loud what happened
5. Write 3–5 nuggets

If you skip step 4 → you didn’t learn it.

---

## Why This Matters (Real Talk)

### In real systems

Without this:

* money disappears
* orders duplicate
* inventory lies
* data corrupts silently

---

### In data engineering

This explains:

* why your batch is inconsistent
* why upserts collide
* why duplicates appear
* why snapshots matter

---

## Final Outcome

Two years from now…

You open this folder…

And instantly remember:

* what breaks
* why it breaks
* how to fix it

---

## Final line

Transactions are not about SQL.

They are about controlling reality under concurrency.


---

