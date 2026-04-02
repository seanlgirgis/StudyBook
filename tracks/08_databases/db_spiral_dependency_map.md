# Database Spiral Dependency Map

## Core Dependencies
- Any hands-on notebook depends on R0 stack being healthy and seeded.
- R2 deep dives depend on R1 first-contact notebooks for baseline context.
- R2 QA and nuggets depend on completed R2 notebooks for accurate content.
- R3 decision frameworks depend on R2 coverage across all families.

## Setup Dependencies
- `_setup/docker-compose.yml` and `_setup/env` required before local notebooks.
- `_setup/master_seed_data.py` required before any query notebooks.
- `_setup/verify_all.py` should be green before starting a new notebook.
- `_setup/cloud_setup.md` required before any cloud notebooks.

## Family Dependencies
- Relational knowledge informs columnar comparisons and time-series on Postgres extensions.
- Columnar concepts inform OLAP cost and query planning in R3.
- Document and key-value concepts inform R3 decision frameworks and polyglot pipeline.
- Graph concepts inform `neo4j_cypher.ipynb` and R3 interview simulation.
- Vector concepts inform R3 decision framework and polyglot pipeline.
- Search concepts inform R3 decision framework and cloud service mapping.

## Theory-Only Path
- Write or review concept MDs first.
- Draft QA files per family.
- Append nuggets after any major study block.
- Use the gap list to keep theory work aligned with missing files.

## Hands-On Path
- Run `_setup/verify_all.py`.
- Complete R1 notebooks in A-I order.
- Complete R2 notebooks in A-I order.
- Complete R3 notebooks in listed order.
