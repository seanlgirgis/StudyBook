# 01 — What Docker Is

[⬅️ Back to Start](00_START_HERE.md) | [Next ➡️ Run Your First Container](02_run_first_container.md)

## Goal

Understand Docker in one simple mental model.

## Docker in plain English

Docker packages your application with everything it needs to run:

- code
- Python version
- system dependencies
- runtime settings

That package becomes an **image**.

When the image runs, it becomes a **container**.

## Mental model

```text
Dockerfile  →  Image  →  Container
recipe         box       running box
```

## Why this matters

Without Docker:

```text
It works on my machine.
```

With Docker:

```text
It works in the same environment everywhere.
```

## Tiny vocabulary

| Term | Meaning |
|---|---|
| Dockerfile | Recipe for building an image |
| Image | Packaged app environment |
| Container | Running instance of an image |
| Volume | Folder shared with a container |
| Compose | Tool for running multiple containers |

## Your takeaway

Docker is not magic. It is a repeatable way to run software in isolated boxes.

---

[⬅️ Back to Start](00_START_HERE.md) | [Next ➡️ Run Your First Container](02_run_first_container.md)
