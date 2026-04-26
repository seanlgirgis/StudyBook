# StudyBook — Quick Reference
# Last updated: 2026-04-25
# One page. Everything you need to remember.

---

## KEY PATHS

| What | Path |
|---|---|
| Repo root | `D:\Workarea\StudyBook\` |
| Manager (this folder) | `D:\Workarea\StudyBook\tutorials\_manager\` |
| Tutorials | `D:\Workarea\StudyBook\tutorials\` |
| Tutorial standards | `D:\Workarea\StudyBook\tutorials\_meta\TUTORIAL_STANDARDS.md` |
| Shared helpers | `D:\Workarea\StudyBook\tutorials\_shared\` |
| Gap prompt files | `D:\Workarea\StudyBook\temp\gap\done\` |
| Website source | `D:\Workarea\seanlgirgis.github.io\learning\` |
| Audio MP3s | `D:\temp\studybook_audio\{slug}\final_{slug}.mp3` |
| Phone music | `C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\StudyBook\` |
| Codex missions | `D:\Workarea\StudyBook\prompts\codex_missions\` |
| ChatGPT P1 prompt | `D:\Workarea\StudyBook\prompts\codex_missions\WebsitePagesAndAudioBYCodexChatgpt\Project-1-Audioscript-Maker.txt` |
| ChatGPT P2 prompt | `D:\Workarea\StudyBook\prompts\codex_missions\WebsitePagesAndAudioBYCodexChatgpt\Project2_HTMl_Maker.txt` |

---

## KEY URLS

| What | URL |
|---|---|
| Live website | https://seanlgirgis.github.io/learning/ |
| R2 CDN (audio) | https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/ |
| Kafka UI | http://localhost:8080 |
| Airflow | http://localhost:8082 |
| Spark Master | http://localhost:8081 |
| Elasticsearch | http://localhost:9200 |
| Kibana | http://localhost:5601 |
| InfluxDB | http://localhost:8086 |
| MLflow | http://localhost:5000 |
| Splunk | http://localhost:8000 |

---

## KEY SCRIPTS

```powershell
# Sync MP3s + playlists to Pixel 8 Pro
.\scripts\sync_studybook_to_phone.ps1
.\scripts\sync_studybook_to_phone.ps1 -DryRun    # preview
.\scripts\sync_studybook_to_phone.ps1 -Force      # force re-copy all

# Generate MP3 audio (full pipeline)
.\scripts\run_mission_audio.ps1 -Slug {slug} -ChunkSize 750

# Docker
docker compose up -d       # start everything
docker compose stop        # stop (keep volumes)
docker compose down        # stop + remove containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## CHATGPT PROJECTS

| Project | File | Purpose |
|---|---|---|
| Project 1 — Audio Script Writer | Project-1-Audioscript-Maker.txt | Writes HOST/SEAN dialogue scripts |
| Project 2 — HTML Page Generator | Project2_HTML_MAKER.txt | Generates learning HTML pages |
| Project 3 — Tutorial Generator | (use prompt.md per topic) | Generates tutorial .py files |

### Audio Script → MP3 Flow
1. ChatGPT Project 1: paste gap prompt → generates script chunks
2. Copy script to codex_missions prompt file
3. Run: `.\scripts\run_mission_audio.ps1 -Slug {slug} -ChunkSize 750`
4. Upload final MP3 to R2 CDN
5. Wire audio src into HTML page
6. Commit + push website

### Tutorial .py Generation Flow
1. Open `tutorials/NN_topic/prompt.md`
2. Paste into ChatGPT (new chat or Project 3)
3. ChatGPT acknowledges → say "generate file 01"
4. Save output to `tutorials/NN_topic/setup/01_name.py`
5. Repeat for 02-05, then "generate capstone"
6. Run locally, fix, mark ROADMAP.md

---

## DOCKER CONNECTION STRINGS

```python
POSTGRES  = "postgresql://studybook:studybook@localhost:5432/studybook"
KAFKA     = "localhost:29092"                    # external listener
REDIS     = "redis://localhost:6380/0"
ES        = "http://localhost:9200"
CASSANDRA = "localhost:9042"
NEO4J     = "bolt://localhost:7687"              # auth: neo4j/studybook
INFLUX    = "http://localhost:8086"
SPARK     = "spark://localhost:7077"             # or local[*]
```

---

## AUDIO SLUGS (54 MP3s)

aws-kinesis | pyspark | apache-airflow | aws-step-functions | delta-lake | aws-emr |
aws-glue | aws-s3 | aws-cloudwatch | python-logging | dbt | parquet |
python-concurrency | encryption | data-anonymization-pii | aws-iam | postgresql |
sql-patterns | python-testing | pydantic | aws-redshift | aws-athena | sqlalchemy |
pandas | numpy | polars | duckdb | data-stubbing | streamlit | fastapi |
aws-lambda | aws-dynamodb | aws-msk-kafka | aws-bedrock | terraform | docker |
cicd | aws-ecs | aws-cloudformation | opensearch | snowflake-pyiceberg |
(+ remaining 13 audio slugs from original 54-topic set)

---

## PHONE PLAYLISTS (12 M3U)

| # | Playlist | Tracks |
|---|---|---|
| PL-01 | Toyota Interview Prep | 18 |
| PL-02 | Capital One Interview Prep | 18 |
| PL-03 | AWS Foundations | 9 |
| PL-04 | AWS Data Stack | 9 |
| PL-05 | Streaming & Real-Time | 6 |
| PL-06 | Python Engineering | 11 |
| PL-07 | Data Engineering Fundamentals | 10 |
| PL-08 | Engineering Discipline | 8 |
| PL-09 | Security & Compliance | 6 |
| PL-10 | My Story | 5 |
| PL-11 | Commute Starter | 10 |
| PL-12 | Local Analytics Stack | 5 |

---

## INTERVIEW TARGETS

**Toyota** — IoT/streaming, real-time pipelines, AWS, Kinesis, Glue, EMR, Airflow
**Capital One** — Financial services, compliance, PII/encryption, IAM, SQL, testing, Redshift

---

## WEBSITE — 49 Learning Pages

All live at https://seanlgirgis.github.io/learning/
Source: `D:\Workarea\seanlgirgis.github.io\learning\*.html`
Push: `git add . && git commit -m "msg" && git push` (from D:\Workarea\seanlgirgis.github.io)
