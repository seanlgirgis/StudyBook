SAVE AS: dynamodb_guide.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep DynamoDB guide notebook.

TASK: Cover DynamoDB partition design, GSI, LSI, single-table design, and Streams — using the Citi telemetry dataset on AWS.

AWS CONTEXT — do not deviate:
- AWS profile: study
- AWS region: us-east-1
- DynamoDB table prefix: citi-

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id, name, region, status, category
- metrics: 500,000 rows | endpoint_id, metric_name, value, timestamp
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, created_at
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "DynamoDB — Key-Value + Document at Infinite Scale"; explain partition key hash distribution, 10GB partition limit, RCU/WCU capacity model, on-demand vs provisioned; when DynamoDB wins (unpredictable scale, sub-10ms, serverless, global); ASCII diagram of partition routing
2. Imports + boto3 setup (profile=study, region=us-east-1, no pip install); dynamodb = boto3.resource('dynamodb', ...); print "DynamoDB ready"
3. Table Design — CREATE TABLE citi-alerts (PK=endpoint_id string, SK=alert_id string) on-demand; explain composite key design: PK = partition, SK = sort within partition; insert 100 alert items; GetItem by PK+SK; Query by PK (all alerts for one endpoint); print results
4. GSI Design — add GSI: PK=severity, SK=created_at; Query GSI for all CRITICAL alerts in last 24h; explain GSI eventual consistency; compare to LSI (same PK, different SK, strongly consistent); print "GSI query returned X alerts"
5. Single-Table Design — model endpoints + alerts + metrics in ONE table using entity prefix pattern (PK="ENDPOINT#123", SK="ALERT#456" or "METRIC#789"); show 3 access patterns: get endpoint, get all alerts for endpoint, get latest 10 metrics for endpoint — all using single table; explain overloaded key pattern
6. DynamoDB Streams — enable streams on citi-alerts table; write 5 items; read stream records using boto3 DynamoDB Streams client; show NEW_IMAGE records; explain Lambda trigger pattern for real-time alert processing
7. Hot Partition Problem — demonstrate: write 1000 items all with the same PK; check CloudWatch metrics (conceptual cell showing boto3 code to get consumed WCUs); explain how to detect and fix hot partition with write sharding; Citi framing
8. What Just Happened — DynamoDB vs MongoDB vs Cassandra decision table; 4 interview Q&A; cleanup: delete table

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real AWS values from context above
- Every code cell must execute top-to-bottom without error

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

