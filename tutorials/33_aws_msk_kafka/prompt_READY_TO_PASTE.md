# ChatGPT Prompt — Kafka / AWS MSK Tutorial (READY TO PASTE)
# Paste everything between the triple-backtick fences into ChatGPT

```
TOPIC: Apache Kafka & AWS MSK for Data Engineers
SLUG: 33_aws_msk_kafka
PRIORITY: DE Fundamentals — Event Streaming
INFRASTRUCTURE: Kafka via Docker (self-hosted) + optional AWS MSK

===== CODING STANDARDS =====

FILE HEADER (every file must start with this exact block):
# ============================================================
# Topic   : Apache Kafka & AWS MSK
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install confluent-kafka | Docker + docker-compose.yml for local Kafka
# Run     : 1) docker compose up -d  2) python NN_filename.py
# ============================================================

STYLE RULES:
- Use confluent-kafka (librdkafka-based) — NOT kafka-python. It's the industry standard.
- Local Kafka via Docker Compose (provided below). Never assume a running cluster.
- All connection config in a dict — never scattered around the code.
- Show error handling: KafkaError, KafkaException, delivery callbacks
- Type hints on all function signatures
- Print section separators and progress for long-running consumers
- No placeholder comments, no TODO, no pass, no NotImplementedError
- For AWS MSK: gate on env vars (MSK_BOOTSTRAP_SERVERS, MSK_REGION) — never crash if not set

GENERATE docker-compose.kafka.yml FIRST (used by all files):

--- docker-compose.kafka.yml ---
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.6.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    healthcheck:
      test: echo srvr | nc localhost 2181 | grep Mode
      interval: 10s
      timeout: 5s
      retries: 5

  kafka:
    image: confluentinc/cp-kafka:7.6.0
    depends_on:
      zookeeper:
        condition: service_healthy
    ports:
      - "29092:29092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: "zookeeper:2181"
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
      KAFKA_LOG_RETENTION_HOURS: 24
    healthcheck:
      test: kafka-broker-api-versions --bootstrap-server localhost:9092
      interval: 10s
      timeout: 10s
      retries: 10
      start_period: 30s

  schema-registry:
    image: confluentinc/cp-schema-registry:7.6.0
    depends_on:
      kafka:
        condition: service_healthy
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: "kafka:9092"
    healthcheck:
      test: curl -f http://localhost:8081/subjects || exit 1
      interval: 10s
      timeout: 5s
      retries: 10

volumes: {}

===== FILE 01: 01_producer_basics.py =====

PURPOSE: Kafka producers — sync/async, delivery reports, batch tuning
COVERS: Producer config, produce(), flush(), poll(), delivery callbacks, error handling

CONSTANTS:
  BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
  TOPIC = "studybook-orders"
  N_MESSAGES = 1_000

EXACT FUNCTION SIGNATURES:

def get_producer_config(
    bootstrap_servers: str = BOOTSTRAP_SERVERS,
    acks: str = "all",
    retries: int = 5,
    batch_size: int = 16384,
    linger_ms: int = 5,
) -> dict:
    """
    Return confluent-kafka Producer config dict.
    Key settings explained with inline comments:
      'bootstrap.servers': bootstrap_servers,
      'acks': acks,              # 'all' = wait for all replicas (safest, slower)
      'retries': retries,        # retry on transient failures
      'retry.backoff.ms': 100,
      'batch.size': batch_size,  # bytes per batch — larger = higher throughput
      'linger.ms': linger_ms,    # wait up to Nms for more messages to batch
      'compression.type': 'snappy',  # compress batches
      'enable.idempotence': True,    # exactly-once delivery guarantee
    """

def delivery_callback(err, msg) -> None:
    """
    Delivery report callback for async produce.
    Print on success: f"✓ Delivered: {msg.topic()}[{msg.partition()}]@{msg.offset()} key={msg.key()}"
    Print on error:   f"✗ Failed:    {msg.topic()} key={msg.key()} error={err}"
    """

def create_topic_if_not_exists(
    bootstrap_servers: str,
    topic: str,
    num_partitions: int = 3,
    replication_factor: int = 1,
) -> None:
    """
    Use AdminClient to create topic.
    from confluent_kafka.admin import AdminClient, NewTopic
    Catch TopicAlreadyExistsException silently.
    Print: "Topic {topic} ready (partitions={num_partitions})"
    """

def produce_sync(producer: Producer, messages: list[dict]) -> int:
    """
    Produce messages synchronously — call flush() after each or after N messages.
    Each message: key=str(msg["order_id"]).encode(), value=json.dumps(msg).encode()
    Call producer.poll(0) between produces to trigger delivery callbacks.
    Call producer.flush() at the end.
    Return count of successfully delivered messages.
    """

def produce_async_with_callback(producer: Producer, messages: list[dict]) -> None:
    """
    Produce all messages async with delivery_callback.
    DO NOT flush between messages — let librdkafka batch them.
    Call producer.flush() once at the end.
    Print: "Produced {len(messages):,} messages — awaiting delivery reports..."
    """

def benchmark_producer(
    n_messages: int = 10_000,
    batch_sizes: list[int] | None = None,
) -> None:
    """
    Benchmark producer throughput with different batch sizes:
    batch_sizes = [1, 100, 1000, 16384]  (bytes)
    For each: produce n_messages, measure msg/sec.
    Print comparison table:
      batch.size | linger.ms | throughput (msg/s) | latency (ms/msg)
    """

MAIN BLOCK:
  create_topic_if_not_exists(BOOTSTRAP_SERVERS, TOPIC, num_partitions=3)
  producer = Producer(get_producer_config())
  orders = [generate_order(i) for i in range(N_MESSAGES)]  # define generate_order inline
  produce_async_with_callback(producer, orders)
  benchmark_producer(5_000)

===== FILE 02: 02_consumer_basics.py =====

PURPOSE: Kafka consumers — poll loop, consumer groups, offset management, rebalancing
COVERS: Consumer config, subscribe(), poll(), commit(), partition assignment, at-least-once

EXACT FUNCTION SIGNATURES:

def get_consumer_config(
    bootstrap_servers: str = BOOTSTRAP_SERVERS,
    group_id: str = "studybook-consumer-group",
    auto_offset_reset: str = "earliest",
    enable_auto_commit: bool = False,
) -> dict:
    """
    Return confluent-kafka Consumer config dict.
    Key settings explained:
      'bootstrap.servers': bootstrap_servers,
      'group.id': group_id,             # consumers with same group.id share partitions
      'auto.offset.reset': auto_offset_reset,   # 'earliest' = read from start, 'latest' = new only
      'enable.auto.commit': enable_auto_commit, # False = manual commit (at-least-once control)
      'max.poll.interval.ms': 300_000,          # max time between polls before kicked from group
      'session.timeout.ms': 45_000,             # heartbeat timeout
    """

def on_assign(consumer: Consumer, partitions: list) -> None:
    """
    Rebalance callback — called when partitions assigned.
    Print: "Assigned partitions: {[f'{p.topic}[{p.partition}]' for p in partitions]}"
    """

def on_revoke(consumer: Consumer, partitions: list) -> None:
    """
    Rebalance callback — called when partitions revoked (graceful rebalance).
    Commit offsets before losing partitions (manual commit pattern).
    Print: "Revoked partitions: {[f'{p.topic}[{p.partition}]' for p in partitions]}"
    """

def consume_with_manual_commit(
    consumer: Consumer,
    topic: str,
    max_messages: int = 1_000,
    poll_timeout: float = 1.0,
) -> list[dict]:
    """
    Poll loop with manual offset commit.
    Pattern:
      consumer.subscribe([topic], on_assign=on_assign, on_revoke=on_revoke)
      messages_consumed = 0
      while messages_consumed < max_messages:
          msg = consumer.poll(poll_timeout)
          if msg is None: continue
          if msg.error():
              if msg.error().code() == KafkaError._PARTITION_EOF: continue
              raise KafkaException(msg.error())
          data = json.loads(msg.value().decode("utf-8"))
          # process...
          consumer.commit(message=msg, asynchronous=False)  # commit after processing
          messages_consumed += 1
    Print progress every 100 messages: "Consumed {n}/1000"
    Return list of deserialized message dicts.
    """

def consume_batch_commit(
    consumer: Consumer,
    topic: str,
    batch_size: int = 100,
    max_messages: int = 1_000,
) -> list[dict]:
    """
    Accumulate messages in a batch, commit once per batch.
    This pattern: 1 commit per 100 messages vs 1 commit per message = 100x fewer commits.
    On error mid-batch: log and commit what was processed (at-least-once).
    """

def read_from_specific_offset(
    bootstrap_servers: str,
    topic: str,
    partition: int,
    offset: int,
    n_messages: int = 10,
) -> list[dict]:
    """
    Assign specific partition + offset (bypass consumer group entirely).
    Use consumer.assign([TopicPartition(topic, partition, offset)])
    Read exactly n_messages. Useful for replay and debugging.
    """

MAIN BLOCK:
  consumer = Consumer(get_consumer_config())
  messages = consume_with_manual_commit(consumer, TOPIC, max_messages=500)
  print(f"Consumed {len(messages):,} messages")
  consumer.close()
  # Show single-partition replay
  replayed = read_from_specific_offset(BOOTSTRAP_SERVERS, TOPIC, partition=0, offset=0, n_messages=5)
  print("Replayed messages:", replayed[:2])

===== FILE 03: 03_serialization.py =====

PURPOSE: Message serialization — JSON, Avro with Schema Registry, struct validation
COVERS: JSON, Avro schemas, confluent Schema Registry, schema evolution rules

EXACT FUNCTION SIGNATURES:

def json_producer_consumer_demo(bootstrap_servers: str) -> None:
    """
    Simplest pattern: JSON bytes.
    Producer: json.dumps(msg).encode("utf-8") as value
    Consumer: json.loads(msg.value().decode("utf-8"))
    
    Pros: human readable, no schema registration
    Cons: no schema enforcement, large message size, no versioning
    Print: pros/cons table and a round-trip example.
    """

def define_order_avro_schema() -> dict:
    """
    Return Avro schema dict for an Order:
    {
      "type": "record",
      "name": "Order",
      "namespace": "com.studybook.orders",
      "fields": [
        {"name": "order_id", "type": "string"},
        {"name": "customer_id", "type": "string"},
        {"name": "amount", "type": "double"},
        {"name": "status", "type": {"type": "enum", "name": "OrderStatus",
                                     "symbols": ["PENDING","CONFIRMED","SHIPPED","DELIVERED","CANCELLED"]}},
        {"name": "order_date", "type": "long", "logicalType": "timestamp-millis"},
        {"name": "metadata", "type": ["null", {"type": "map", "values": "string"}], "default": None},
      ]
    }
    """

def avro_producer(
    bootstrap_servers: str,
    schema_registry_url: str,
    topic: str,
    messages: list[dict],
) -> None:
    """
    Produce Avro-serialized messages using confluent_kafka.schema_registry.avro.AvroSerializer.
    from confluent_kafka.schema_registry import SchemaRegistryClient
    from confluent_kafka.schema_registry.avro import AvroSerializer
    from confluent_kafka.serialization import SerializationContext, MessageField
    
    Steps:
    1. schema_registry_client = SchemaRegistryClient({"url": schema_registry_url})
    2. avro_serializer = AvroSerializer(schema_registry_client, json.dumps(schema), to_dict)
    3. producer = SerializingProducer({"bootstrap.servers": ..., "value.serializer": avro_serializer})
    4. producer.produce(topic, value=msg, ...)
    
    to_dict: convert Python dict → dict compatible with Avro schema (e.g., convert datetime to millis)
    """

def avro_consumer(
    bootstrap_servers: str,
    schema_registry_url: str,
    topic: str,
    max_messages: int = 100,
) -> list[dict]:
    """
    Consume Avro messages using AvroDeserializer.
    The Schema Registry serves the schema — consumer doesn't need to know it upfront.
    Return list of deserialized Python dicts.
    """

def schema_evolution_demo(schema_registry_url: str) -> None:
    """
    Show what schema changes are COMPATIBLE vs BREAKING:
    
    BACKWARD COMPATIBLE (safe to deploy consumer first):
      ✓ Add optional field with default
      ✓ Remove a field
      ✗ Add required field without default
      ✗ Change field type (int → string)
      ✗ Rename a field
    
    FORWARD COMPATIBLE (safe to deploy producer first):
      ✓ Add a field (consumer ignores unknown fields)
      ✗ Remove a required field the consumer reads
    
    Show: register two schema versions, check compatibility via Schema Registry API.
    GET /compatibility/subjects/{subject}/versions/latest
    Print: which version is registered, compatibility check result.
    """

MAIN BLOCK:
  json_producer_consumer_demo(BOOTSTRAP_SERVERS)
  schema = define_order_avro_schema()
  print("Avro Schema:", json.dumps(schema, indent=2))
  schema_evolution_demo("http://localhost:8081")
  # Live avro producer/consumer if schema registry is up:
  import requests
  try:
      requests.get("http://localhost:8081/subjects", timeout=2)
      # run avro demo
  except Exception:
      print("Schema Registry not available — showing code only")

===== FILE 04: 04_kafka_patterns.py =====

PURPOSE: Real-world Kafka patterns for data engineers
COVERS: partitioning strategy, dead letter queue, idempotent consumer, compacted topics

EXACT FUNCTION SIGNATURES:

def partitioning_strategy_demo(producer: Producer, topic: str) -> None:
    """
    Show 3 partitioning strategies:
    
    1. Default (round-robin when no key):
         producer.produce(topic, value=msg_bytes)  # key=None → round-robin
         Use case: uniform load distribution, order doesn't matter
    
    2. Key-based (same key → same partition):
         producer.produce(topic, key=account_id.encode(), value=msg_bytes)
         Use case: ALL events for account_id go to same partition → ordering guaranteed
    
    3. Custom partitioner:
         def my_partitioner(key, all_partitions, available_partitions):
             # hash by first 2 chars of key → sticky partitioning for small keyspace
             return ord(key.decode()[0]) % len(all_partitions)
    
    Show: produce 100 messages with key=account_id, verify they go to same partition.
    Print partition distribution.
    """

def dead_letter_queue_pattern(
    consumer: Consumer,
    main_topic: str,
    dlq_topic: str,
    max_retries: int = 3,
) -> None:
    """
    DLQ pattern: if processing fails after max_retries, send to DLQ.
    
    For each message:
      retry_count = 0
      while retry_count < max_retries:
          try:
              process(msg)
              consumer.commit(message=msg)
              break
          except Exception as e:
              retry_count += 1
              time.sleep(2 ** retry_count)  # exponential backoff
      else:
          # All retries exhausted — send to DLQ with metadata
          dlq_msg = {
              "original_topic": msg.topic(),
              "original_partition": msg.partition(),
              "original_offset": msg.offset(),
              "original_key": msg.key().decode() if msg.key() else None,
              "original_value": msg.value().decode(),
              "error": str(last_error),
              "retry_count": max_retries,
              "failed_at": datetime.utcnow().isoformat(),
          }
          producer.produce(dlq_topic, key=msg.key(), value=json.dumps(dlq_msg).encode())
          consumer.commit(message=msg)
    
    Print: "DLQ pattern protects the pipeline from poison pill messages"
    """

def idempotent_consumer_demo(con: sqlite3.Connection) -> None:
    """
    Show idempotent consumer pattern using a processed_offsets table.
    Before processing each message: check if offset already processed (dedup).
    After processing: record offset.
    
    This handles at-least-once delivery → effectively-once processing.
    
    CREATE TABLE IF NOT EXISTS processed_offsets (
        topic TEXT, partition INTEGER, offset INTEGER, processed_at TEXT,
        PRIMARY KEY (topic, partition, offset)
    );
    
    def is_already_processed(topic, partition, offset) → bool
    def mark_as_processed(topic, partition, offset) → None
    
    Print: "Idempotent consumer: process safely even if message delivered twice"
    """

def compacted_topic_demo(bootstrap_servers: str) -> None:
    """
    Explain log compaction (key → latest value survives compaction):
    Use case: maintaining latest state per key (customer profile, product catalog)
    
    Create a compacted topic via AdminClient:
      NewTopic("customer-profiles", num_partitions=3, replication_factor=1,
               config={"cleanup.policy": "compact", "retention.ms": "-1",
                       "min.compaction.lag.ms": "0"})
    
    Show:
    - Produce 3 updates for customer_id "CUST-001" (different addresses)
    - After compaction: only the latest survives
    - This is Kafka as a distributed key-value store
    
    Print: comparison table: regular topic vs compacted topic
    """

MAIN BLOCK:
  create_topic_if_not_exists(BOOTSTRAP_SERVERS, "studybook-dlq")
  producer = Producer(get_producer_config())
  consumer = Consumer(get_consumer_config(group_id="pattern-demo"))
  partitioning_strategy_demo(producer, TOPIC)
  compacted_topic_demo(BOOTSTRAP_SERVERS)

===== FILE 05: 05_aws_msk.py =====

PURPOSE: AWS MSK — managed Kafka, IAM auth, MSK vs self-hosted
COVERS: MSK cluster creation, IAM auth, SASL/SCRAM, MSK Serverless, cost comparison

CONSTANTS:
  MSK_BOOTSTRAP = os.environ.get("MSK_BOOTSTRAP_SERVERS", "")
  MSK_REGION = os.environ.get("MSK_REGION", "us-east-1")

EXACT FUNCTION SIGNATURES:

def create_msk_cluster_config(
    cluster_name: str,
    vpc_id: str,
    subnet_ids: list[str],
    broker_count: int = 3,
    broker_type: str = "kafka.m5.large",
) -> dict:
    """
    Return boto3-ready create_cluster_v2() config dict.
    Key settings:
    - ClientAuthentication: IAM enabled + SASL/SCRAM enabled
    - EncryptionInfo: TLS_PLAINTEXT (in transit), KMS key (at rest)
    - BrokerNodeGroupInfo: 3 brokers, 1 per AZ
    - Logging: CloudWatch + S3 broker logs enabled
    Print the dict as JSON. Explain cost: m5.large = ~$0.096/hr per broker = ~$206/mo for 3 brokers.
    """

def get_msk_iam_producer_config(bootstrap_servers: str) -> dict:
    """
    Return Producer config for MSK with IAM authentication:
    {
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'OAUTHBEARER',
        'sasl.oauthbearer.method': 'oidc',  # MSK IAM uses OAUTHBEARER
        # confluent-kafka MSK IAM plugin config:
        'plugin.library.paths': 'msk-iam-auth',
    }
    Note: requires aws-msk-iam-sasl-signer-python:
      pip install aws-msk-iam-sasl-signer-python
    """

def get_msk_sasl_scram_config(
    bootstrap_servers: str,
    username: str,
    password: str,
) -> dict:
    """
    Return Producer config for MSK with SASL/SCRAM auth:
    {
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'SCRAM-SHA-512',
        'sasl.username': username,
        'sasl.password': password,
    }
    Explain: SCRAM stored in AWS Secrets Manager — never hardcode credentials.
    """

def msk_serverless_vs_provisioned() -> None:
    """
    Print comparison table:
    
    | Dimension          | MSK Serverless              | MSK Provisioned          |
    | Capacity           | Auto-scales                 | Fixed broker count       |
    | Pricing            | Per-partition-hour + GB     | Per-broker-hour          |
    | Best for           | Variable workloads          | Predictable high-volume  |
    | Throughput limit   | 200 MB/s per cluster        | Depends on broker type   |
    | Partitions         | Up to 120                   | Up to 45,000             |
    | Cost (1 partition) | ~$0.016/hr                  | ~$0.29/hr (m5.large x3) |
    | Auth options       | IAM only                    | IAM + SASL/SCRAM + mTLS  |
    | Replication config | Managed (cannot change)     | Configurable (1-3)       |
    
    When to choose each — 3 concrete scenarios.
    """

def msk_vs_self_hosted_kafka() -> None:
    """
    Print decision matrix:
    
    Choose MSK when:
      ✓ Don't want to manage Zookeeper/KRaft, broker upgrades, disk scaling
      ✓ Team is small — ops burden matters
      ✓ AWS-native stack (VPC integration, IAM, CloudWatch built-in)
      ✓ Compliance requires managed service
    
    Choose self-hosted when:
      ✓ Need full control (custom configs, Kafka plugins, specific versions)
      ✓ Multi-cloud or on-prem requirement
      ✓ Cost optimization at large scale (MSK premium ~30%)
      ✓ Need Kafka features MSK doesn't support (e.g., tiered storage on older versions)
    
    Middle ground: MSK Serverless for dev/test, provisioned for prod.
    """

MAIN BLOCK:
  msk_serverless_vs_provisioned()
  msk_vs_self_hosted_kafka()
  if MSK_BOOTSTRAP:
      print("MSK bootstrap found — showing auth config examples")
      print(json.dumps(get_msk_iam_producer_config(MSK_BOOTSTRAP), indent=2))
  else:
      print("Set MSK_BOOTSTRAP_SERVERS to connect to a real MSK cluster.")
      print("Running local Kafka demo instead (localhost:29092)")

===== CAPSTONE =====

Generate these files (all COMPLETE and FULLY RUNNABLE):

--- capstone/brief.md ---
Title: Real-Time Transaction Processing Pipeline
Scenario: Capital One-style real-time pipeline. A producer simulates 10,000 card
transactions from 500 accounts. A consumer reads, detects 3 anomaly types
(velocity: >5 txs/min from same account; large: >3x account average; geo-mismatch:
different country than account home), tags each transaction with anomaly flags,
writes clean transactions to Parquet and suspicious ones to a dead letter topic.

--- capstone/producer.py ---

CONSTANTS:
  TOPIC = "transactions"
  DLQ_TOPIC = "transactions-dlq"
  N_TRANSACTIONS = 10_000
  N_ACCOUNTS = 500

EXACT FUNCTION SIGNATURES:

def generate_transaction(account_id: str, account_home_country: str, seq: int) -> dict:
    """
    Generate one transaction dict. 5% chance of anomalous behavior:
    - 2% velocity burst: 10 transactions in rapid succession (same account, same second)
    - 2% large amount: amount = account_avg * 4
    - 1% geo mismatch: country != account_home_country
    Include: tx_id, account_id, amount, merchant, country, ts (epoch ms), seq
    """

def run_producer() -> None:
    """
    Produce all transactions with key=account_id (ensures ordering per account).
    Print throughput: msgs/sec every 1000 messages.
    """

--- capstone/consumer.py ---

EXACT FUNCTION SIGNATURES:

def detect_anomalies(
    tx: dict,
    account_history: dict[str, list[dict]],
    account_profiles: dict[str, dict],
) -> list[str]:
    """
    Return list of anomaly type strings (empty = clean).
    Check:
    1. velocity: count txs for account in last 60 seconds > 5 → "VELOCITY"
    2. large_tx: amount > account_profiles[account_id]["avg_amount"] * 3 → "LARGE_TX"
    3. geo_mismatch: tx["country"] != account_profiles[account_id]["home_country"] → "GEO_MISMATCH"
    account_history: {account_id: [last N tx dicts]} — updated by caller
    """

def run_consumer(output_parquet_path: str) -> dict:
    """
    Consume until all 10K messages processed or 30s of no new messages.
    For each message:
      - detect_anomalies()
      - if anomalies: send to DLQ with anomaly_flags field
      - else: append to clean_txs list
    After all consumed:
      - write clean_txs as Parquet
      - print summary report
    Return: {total: int, clean: int, anomalous: int, by_type: dict}
    """

--- capstone/test_capstone.py ---

EXACT TEST FUNCTIONS:

def test_generate_transaction_schema():
    tx = generate_transaction("ACC-001", "US", 1)
    required = ["tx_id", "account_id", "amount", "merchant", "country", "ts", "seq"]
    assert all(k in tx for k in required)
    assert tx["account_id"] == "ACC-001"

def test_detect_no_anomaly_for_normal_tx():
    tx = {"tx_id": "T1", "account_id": "ACC-001", "amount": 50.0, "country": "US", "ts": time.time()}
    profiles = {"ACC-001": {"avg_amount": 100.0, "home_country": "US"}}
    history = {"ACC-001": []}
    result = detect_anomalies(tx, history, profiles)
    assert result == []

def test_detect_velocity_anomaly():
    now = time.time()
    recent_txs = [{"ts": now - i * 5} for i in range(6)]  # 6 txs in last 30s
    tx = {"tx_id": "T7", "account_id": "ACC-001", "amount": 50.0, "country": "US", "ts": now}
    profiles = {"ACC-001": {"avg_amount": 100.0, "home_country": "US"}}
    history = {"ACC-001": recent_txs}
    result = detect_anomalies(tx, history, profiles)
    assert "VELOCITY" in result

def test_detect_large_tx_anomaly():
    tx = {"tx_id": "T1", "account_id": "ACC-001", "amount": 500.0, "country": "US", "ts": time.time()}
    profiles = {"ACC-001": {"avg_amount": 100.0, "home_country": "US"}}
    result = detect_anomalies(tx, {}, profiles)
    assert "LARGE_TX" in result

def test_detect_geo_mismatch():
    tx = {"tx_id": "T1", "account_id": "ACC-001", "amount": 50.0, "country": "UK", "ts": time.time()}
    profiles = {"ACC-001": {"avg_amount": 100.0, "home_country": "US"}}
    result = detect_anomalies(tx, {}, profiles)
    assert "GEO_MISMATCH" in result

def test_multiple_anomalies_detected():
    now = time.time()
    tx = {"tx_id": "T7", "account_id": "ACC-001", "amount": 500.0, "country": "UK", "ts": now}
    profiles = {"ACC-001": {"avg_amount": 100.0, "home_country": "US"}}
    recent_txs = [{"ts": now - i * 5} for i in range(6)]
    result = detect_anomalies(tx, {"ACC-001": recent_txs}, profiles)
    assert "VELOCITY" in result
    assert "LARGE_TX" in result
    assert "GEO_MISMATCH" in result

===== GENERATION INSTRUCTIONS =====

Generate files ONE AT A TIME in this order:
  docker-compose.kafka.yml
  01_producer_basics.py
  02_consumer_basics.py
  03_serialization.py
  04_kafka_patterns.py
  05_aws_msk.py
  capstone/brief.md
  capstone/producer.py
  capstone/consumer.py
  capstone/test_capstone.py

Each file must be COMPLETE and FULLY RUNNABLE — no placeholders, no TODO, no pass.
Use exact function signatures shown above.
After each file, wait for me to say "next".

Acknowledge these instructions, then wait for me to say "generate file 01".
```
