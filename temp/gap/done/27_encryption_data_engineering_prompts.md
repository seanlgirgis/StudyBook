# Encryption for Data Engineers — ChatGPT Project Prompts

Priority: 🔴 Critical — financial services, cloud storage, and compliance all require this knowledge

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Encryption for Data Engineers
Slug: encryption-data-engineering

Extra coverage required:
- Symmetric vs asymmetric encryption — symmetric uses one key (AES-256) for bulk data; asymmetric uses a key pair (RSA/ECC) for key exchange and signatures; data engineers mostly deal with symmetric
- Encryption at rest vs in transit — two separate concerns: at-rest protects stored data if storage is compromised; in-transit protects data moving over networks; both must be addressed
- TLS — Transport Layer Security for data in transit; certificate-based handshake; TLS 1.2 minimum, TLS 1.3 preferred; HTTP is never acceptable for pipelines handling sensitive data
- S3 encryption options — SSE-S3 (AWS manages keys, enabled by default), SSE-KMS (customer-managed keys via KMS, audit trail), SSE-C (you provide the key per request); when to choose each
- AWS KMS — Customer Master Keys (CMKs) / KMS keys; key policies control access; automatic annual rotation; KMS encrypts data keys, not data directly
- Envelope encryption — generate a data key from KMS, encrypt data locally with data key (fast AES), encrypt the data key with KMS master key, store both alongside the data; the standard cloud pattern
- Database encryption at rest — Oracle TDE, SQL Server TDE, RDS storage encryption; covers data files and backups; does not protect against a compromised application with valid credentials
- Field-level encryption — encrypt specific columns (SSN, account number) at application layer before writing to database; only the application with the decryption key can read plaintext
- Python cryptography library — Fernet symmetric encryption (AES-128-CBC + HMAC); generate_key(), Fernet(key).encrypt(bytes), .decrypt(token); straightforward for pipeline use
- Hashing vs encryption — hashing is one-way (SHA-256 for checksums, bcrypt for passwords); encryption is reversible with the correct key; never use hashing where you need to retrieve the original value
- Secrets management — AWS Secrets Manager for credentials with automatic rotation; Parameter Store for config values; never store secrets in environment variable files committed to git
- Key rotation — rotating master keys without re-encrypting all data: re-encrypt only the data keys; the envelope encryption pattern makes rotation cheap
- PGP for file exchange — encrypting files before S3 upload for partner data exchange; gnupg library in Python; the standard for B2B file transfer with external organizations
- Compliance requirements — PCI-DSS requires encryption of cardholder data at rest and in transit; HIPAA requires encryption of PHI; GDPR treats encrypted data as lower-risk for breach notification

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. Symmetric vs Asymmetric — the decision rule
  2. Encryption at Rest vs In Transit
  3. S3 Encryption — SSE-S3, SSE-KMS, SSE-C
  4. AWS KMS & Envelope Encryption
  5. Database Encryption — TDE & RDS
  6. Field-Level Encryption
  7. Python cryptography Library — Fernet
  8. Hashing vs Encryption
  9. Secrets Management, Key Rotation & Compliance
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs; include a code block where it adds value (20 lines max)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\encryption-data-engineering.html
