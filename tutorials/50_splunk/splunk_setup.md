<!-- File: splunk_setup.md -->

SAVE AS: splunk_setup.md
PLACE IN: D:\Workspace\Technologies\_setup\

---

ROLE: You are a senior Data Engineer writing a precise operational runbook.
Every command is copy-paste ready. No vague steps. No "see documentation".
Target: someone who has never used Splunk but knows Docker and Python.

TASK: Generate splunk_setup.md — a complete setup guide for running Splunk Free via Docker
and ingesting Citi telemetry alert data.

IMPORTANT ARCHITECTURE NOTE — embed this clearly at the top of the generated guide:
Splunk runs as a STANDALONE Docker container separate from docker-compose.technologies.yml.
Start it with `docker run` (provided below). Do NOT add it to the main docker-compose stack.
Reason: Splunk is optional and its license model is independent of the learning stack.

DATASET CONTEXT — do not deviate:
- PostgreSQL: localhost:5432, db=citi_telemetry, user=de_user, password=de_password
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Goal: forward recent alerts to Splunk and query them with SPL

PORT AWARENESS: Splunk web UI runs on 8000. Verify no conflict before starting.
Check with: `docker ps --format "table {{.Ports}}" | grep 8000`
The main docker-compose stack does NOT use port 8000, so this is safe.

STRUCTURE — include all 8 sections in this order:

## 1. What Splunk Free gives you
- 500 MB/day ingestion limit — sufficient for 25K alert rows
- Web UI: port 8000
- REST API: port 8089
- HEC (HTTP Event Collector): port 8088
- Suitable for: local dev, SPL learning, dashboards
- NOT suitable for: production, multi-instance, forwarding at scale

## 2. Start Splunk (standalone docker run)
Provide the exact docker run command:
- Image: splunk/splunk:9.2.0
- Container name: citi_splunk
- Detached (-d)
- Ports: -p 8000:8000 -p 8088:8088 -p 8089:8089
- SPLUNK_START_ARGS: --accept-license
- SPLUNK_PASSWORD: SplunkAdmin123! (meets 8-char complexity requirement)
- Volume: -v splunk_var:/opt/splunk/var (named Docker volume)
- Volume: -v splunk_etc:/opt/splunk/etc (named Docker volume)
- Restart: --restart unless-stopped
- Then: the exact docker command to wait for Splunk to be ready (tail logs until "Ansible playbook complete")

## 3. First login and health check
- URL: http://localhost:8000 | Username: admin | Password: SplunkAdmin123!
- Exact curl command to verify REST API health:
  curl -k -u admin:SplunkAdmin123! https://localhost:8089/services/server/info -o /dev/null -w "%{http_code}"
  Expected: 200

## 4. Enable HEC (HTTP Event Collector)
Step-by-step via Splunk Web UI:
1. Settings → Data Inputs → HTTP Event Collector → Global Settings → Enable: On → Save
2. New Token → Name: citi_telemetry_hec → Source type: _json → Index: main → Review → Submit
3. Copy the token value — you will need it in step 5

Test HEC immediately with curl (replace YOUR_TOKEN with the copied value):
```
curl http://localhost:8088/services/collector/event \
  -H "Authorization: Splunk YOUR_TOKEN" \
  -d '{"event": {"test": "hec_working"}, "sourcetype": "_json"}'
```
Expected response: {"text":"Success","code":0}

## 5. Python forwarder script (send_to_splunk.py)
Provide a complete, runnable Python script as a code block.
The script must:
- Import: psycopg2, requests, json, time
- Connect to PostgreSQL with the connection params above
- Query: SELECT alert_id, endpoint_id, severity, message, created_at FROM alerts ORDER BY created_at DESC LIMIT 100
- For each row, build a Splunk HEC event dict:
  {"time": unix_timestamp_of_created_at, "event": {all row fields as dict}, "source": "citi_telemetry_postgres", "sourcetype": "citi_alert"}
- Batch 10 events per POST to http://localhost:8088/services/collector/event
  Use the batch endpoint format: newline-separated JSON objects in one POST body
- Header: Authorization: Splunk YOUR_TOKEN (hardcode as the string "YOUR_TOKEN" — user replaces after generating)
- Print "Sent {n} events to Splunk" on completion
- No external libraries beyond psycopg2 and requests

## 6. SPL queries — copy-paste ready
Provide exactly 5 SPL queries (each as a code block):
1. Count all events: `index=main | stats count by sourcetype`
2. Last 10 alerts: `index=main sourcetype=citi_alert | table created_at severity message endpoint_id | sort -created_at | head 10`
3. Alerts by severity: `index=main sourcetype=citi_alert | stats count by severity | sort -count`
4. Alert trend by hour: `index=main sourcetype=citi_alert | timechart span=1h count by severity`
5. Top 10 endpoints by alert count: `index=main sourcetype=citi_alert | stats count by endpoint_id | sort -count | head 10`

## 7. Splunk concepts — one paragraph each (3-4 sentences)
Define these 5 terms in plain language:
- Index
- Sourcetype
- Forwarder (Universal Forwarder vs Heavy Forwarder)
- Search Head
- HEC (HTTP Event Collector)

## 8. Troubleshooting
Exactly 4 issues, each with: **Symptom** / **Cause** / **Fix** (one line each):
1. Container starts but http://localhost:8000 returns connection refused
2. HEC POST returns 403 Forbidden
3. Events arrive in Splunk but _time is wrong / shows current time instead of created_at
4. "License quota exceeded" warning — ingestion stopped

CONSTRAINTS:
- Every command is copy-paste ready
- No "refer to Splunk docs" — all steps inline
- The only placeholder is YOUR_TOKEN in the curl test and Python script, which is explained in context
- Named Docker volumes (splunk_var, splunk_etc) — no bind-mount paths

ACCEPTANCE: Following this guide, user has Splunk running, 100 alerts ingested, all 5 SPL queries returning results in under 30 minutes.

OUTPUT: Return ONLY the raw markdown. No preamble, no explanation outside the guide.
