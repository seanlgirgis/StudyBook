# Scala Tutorial — Agent Context

## What this folder is
Hands-on Scala learning materials migrated from the Study/DataMajor repo (Capital One interview prep, 2026).
38 `.scala` example files covering core Scala concepts, plus a full SBT Spark project template.

## Topics covered
- Pattern matching (basic, on type, with conditions, on case classes, on lists)
- Case classes (basics, copy method, magic methods)
- Classes, traits, and OOP
- Functional programming (Option, Try, Either, higher-order functions)
- Collections (map, filter, flatMap, fold)
- Spark with Scala (SparkProject/ subfolder — full SBT project)

## Companion conceptual guide
`StudyBook/docs/concepts/data_engineering_guides/00001.Scala.FS.md` — full explanation guide
`StudyBook/docs/concepts/data_engineering_guides/00002.Scala.Q.md` — interview Q&A

## How to run
Requires Scala + SBT installed. For the Spark project:
```bash
cd SparkProject
sbt compile
sbt run
```

Individual `.scala` files can be run with:
```bash
scala <filename>.scala
```

## Environment
No venv needed — JVM-based. Ensure Java 11+ is installed.
