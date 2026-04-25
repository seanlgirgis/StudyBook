# Encryption for Data Engineers — ChatGPT Project Prompts

Priority: 🔴 Critical — financial services, cloud storage, and compliance all require this knowledge

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Encryption for Data Engineers
Slug: encryption-data-engineering
Extra coverage required: encryption fundamentals — symmetric vs asymmetric encryption, the distinction and when each applies,
encryption at rest vs encryption in transit — two separate concerns that must both be addressed,
TLS — what it is, how it works for data in transit, why HTTP is never acceptable for data pipelines,
S3 encryption — SSE-S3 (Amazon managed keys), SSE-KMS (customer managed keys via KMS), SSE-C (customer-provided keys) — which to choose and why,
AWS KMS — Customer Master Keys, key policies, key rotation, envelope encryption pattern — how KMS encrypts the data key not the data directly,
envelope encryption — the pattern: generate a data key from KMS, encrypt data with the data key locally, encrypt the data key with KMS, store both,
database encryption at rest — Oracle TDE, SQL Server TDE, RDS encryption — what's covered and what isn't,
field-level encryption — encrypting specific columns (SSN, account number) rather than the entire database, application-layer vs database-layer,
Python cryptography library — Fernet symmetric encryption, generating keys, encrypting and decrypting bytes,
hashing vs encryption — hashing is one-way (for passwords, deduplication, checksums), encryption is reversible (for data that must be retrieved),
secrets management — AWS Secrets Manager vs Parameter Store vs environment variables vs .env files — the right tool for each use case,
key rotation — rotating encryption keys without decrypting and re-encrypting all data, the data key vs master key pattern,
data in motion — encrypting files before uploading to S3, PGP for file exchange with external partners,
certificate management — TLS certificates for internal services, ACM, certificate renewal automation,
compliance requirements — what PCI-DSS requires for cardholder data encryption, what HIPAA requires, what GDPR says about encryption,
real scenario: encrypting sensitive endpoint ownership data in the Citi pipeline — field-level masking vs full dataset encryption.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug encryption-data-engineering -ChunkSize 750
```

Upload final_encryption-data-engineering.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_encryption-data-engineering.mp3` is live on R2.

```
Topic: Encryption for Data Engineers
Slug: encryption-data-engineering
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_encryption-data-engineering.mp3
Today's date: 2026-04-25

SCOPE FENCE: 8-10 sections maximum. 2-3 tight paragraphs per section.
One code block per section, 20 lines max. Cheat sheet: 12-15 rows.
Reference page only - no step-by-step tutorials or full worked examples.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\encryption-data-engineering.html
