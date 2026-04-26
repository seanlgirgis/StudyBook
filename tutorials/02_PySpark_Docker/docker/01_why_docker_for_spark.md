# 01 - Why Docker For Spark?

Back to [Docker Pack Index](./README.md)

## Why we need Docker here

Running Spark directly on Windows can fail due to:

- Java path conflicts
- Hadoop/winutils edge cases
- Python runtime drift across tools
- hidden local-machine state

Docker solves this by shipping a repeatable runtime image.

## What Docker gives us

- Consistent Spark binaries and dependencies
- Same behavior across teammates
- Fast restart/rebuild workflow
- Easier CI/CD and cloud portability

## Mental model

- Your Python script is the driver client.
- Spark master coordinates jobs.
- Spark workers execute tasks.

With Docker, we control the Spark side cleanly and point the driver to it.

Next: [How To Build Images And Compose](./02_build_images.md)
