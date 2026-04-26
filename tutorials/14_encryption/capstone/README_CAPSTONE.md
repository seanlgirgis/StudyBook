# 🔐 Capstone: End-to-End Encryption Pipeline (PCI-DSS Style)

## 📌 Overview

This capstone implements a **production-style encryption pipeline** for handling sensitive financial data (PAN, SSN) in a data engineering system.

It demonstrates:

* Field-level encryption (AES-256-GCM)
* Tokenization (PAN → token vault)
* Key rotation (v1 → v2)
* HMAC-based integrity verification
* Encrypted file output (JSONL)
* Full decrypt + validation pipeline
* Automated tests (pytest)

---

## 🧠 Core Principle

> Encryption alone is not enough —
> **key management, integrity, and data usability matter equally.**

---

## 🏗️ Architecture

```
Raw Data
   ↓
Encrypt Sensitive Fields (AES-GCM)
   ↓
Tokenize PAN (vault)
   ↓
Add HMAC (integrity)
   ↓
Store with key_id + metadata
   ↓
Write encrypted JSONL
   ↓
Read → Verify → Decrypt
```

---

## 📂 Structure

```
capstone/
├── encrypt_pipeline.py
├── test_encryption.py
└── README_CAPSTONE.md
```

---

## 🔐 Security Features

### 1. Field-Level Encryption

* PAN and SSN encrypted using AES-256-GCM
* Other fields remain queryable

```python
pan → encrypted
ssn → encrypted
amount → plaintext (analytics)
```

---

### 2. Tokenization

```
PAN → random token
```

* Stored in TokenVault
* Enables analytics without exposing real PAN
* Required for PCI-DSS scope reduction

---

### 3. Key Management & Rotation

```
Key v1 → encrypt first half
Rotate
Key v2 → encrypt second half
```

✔ Old data still decrypts
✔ New data uses new key

---

### 4. Key Derivation (HKDF)

```
master_key → pan_key
master_key → ssn_key
master_key → integrity_key
```

✔ Prevents key reuse
✔ Limits blast radius

---

### 5. Integrity (HMAC)

Each record includes:

```
record_hmac = HMAC-SHA256(...)
```

✔ Detects tampering
✔ Verified before decryption

---

### 6. Authenticated Encryption (AES-GCM)

Provides:

* Confidentiality
* Integrity (auth tag)

Tampering → decryption fails

---

## 📊 Pipeline Output Example

```
Records processed   : 1000
PAN encrypted       : 1000
SSN encrypted       : 1000
PANs tokenized      : 1000
Key v1 records      : 500
Key v2 records      : 500
HMAC verified       : 1000 ✓
Decrypt verified    : 10 sampled ✓
```

---

## 🧪 Testing

Run:

```bash
pytest test_encryption.py -v
```

### Tests Covered:

* AES-GCM encryption/decryption
* Tamper detection
* HKDF key uniqueness
* Tokenization correctness
* HMAC tamper detection
* Full pipeline validation

---

## ⚠️ Critical Concepts

### 🔑 Salt vs Encryption Key

| Concept        | Purpose          | Secret? |
| -------------- | ---------------- | ------- |
| Salt           | Password hashing | ❌ No    |
| Encryption key | Data encryption  | ✅ Yes   |

---

### ❌ This is INVALID:

```python
b"—"
```

### ✅ Correct:

```python
"—".encode("utf-8")
```

---

### Why?

* Encryption works on **bytes**
* Python bytes literals are ASCII-only

---

## 🔥 Interview Takeaways

### ❓ How do you encrypt sensitive data?

> “I use AES-256-GCM for field-level encryption, tokenize PAN for analytics, and manage keys with rotation and HKDF-derived subkeys.”

---

### ❓ How do you handle key rotation?

> “I store key_id with each record so old data can be decrypted while new data uses the latest key.”

---

### ❓ How do you detect tampering?

> “I use HMAC-SHA256 on stable fields and verify it before decryption.”

---

### ❓ Why not encrypt everything?

> “Field-level encryption keeps data queryable while protecting sensitive fields.”

---

## 🚀 What This Demonstrates

You now understand:

* Real-world encryption architecture
* PCI-DSS compliant data handling
* Key lifecycle management
* Secure data pipelines
* Integrity + confidentiality together

---

## 🧠 Final Rule

> The hardest part of encryption is not the algorithm —
> it’s **key management and system design**.

---

## ✅ Status

✔ Fully implemented
✔ Fully tested
✔ Interview ready

---

## 🎯 Next Step (Optional)

* Integrate with:

  * Amazon Web Services KMS
  * HashiCorp Vault

* Add streaming (Kafka / Spark)

* Add access control / auditing

---

**End of Capstone**
