# 🔐 Encryption for Data Engineers (Capital One Interview Prep)

## 📌 Overview

This tutorial is a **production-grade, interview-focused deep dive** into encryption for data engineering.

It covers:

* Symmetric encryption (AES-GCM)
* Asymmetric encryption (RSA, ECDSA)
* Hashing, salting, and password storage
* Key management and rotation
* Real-world data pipeline encryption patterns

The goal is not just to write code — but to understand **why each choice is made**, exactly how interviewers expect.

---

## 🧠 Core Philosophy

> Encryption is easy.
> Key management is the real problem.

---

## 📂 Project Structure

```
14_encryption/
│
├── 01_symmetric_encryption_aes.py
├── 02_asymmetric_encryption_rsa.py
├── 03_hashing_and_password_storage.py
├── 04_key_management_and_rotation.py
├── 05_encryption_in_data_pipelines.py
│
└── README.md
```

---

# 🔐 FILE 01 — AES (SYMMETRIC ENCRYPTION)

### Key Concepts

* AES-256-GCM (default for data engineers)
* Nonce management (never reuse!)
* Authentication tag (tamper detection)

### Why GCM?

* Provides **confidentiality + integrity**
* Detects any ciphertext modification

### Interview Insight

> “AES-GCM is my default because it provides authenticated encryption (AEAD), unlike CBC.”

---

# 🔑 FILE 02 — RSA, ECDSA, ENVELOPE ENCRYPTION

### Key Concepts

* RSA-OAEP (encryption)
* RSA-PSS (signing)
* ECDSA (modern alternative)
* Envelope encryption

### Envelope Encryption Pattern

```
Data → encrypted with AES (DEK)
DEK  → encrypted with RSA (master key)
```

### Why?

* RSA cannot encrypt large data
* Enables key rotation without re-encrypting everything

### Interview Insight

> “We use envelope encryption so only the DEK needs re-encryption during key rotation.”

---

# 🔒 FILE 03 — HASHING & PASSWORD STORAGE

### Key Concepts

* SHA-256 (integrity, NOT passwords)
* PBKDF2 / scrypt (password hashing)
* Salts
* HMAC

---

## 🔑 Salt vs Encryption Key (CRITICAL)

### ❌ Salt (NOT encryption)

* Used for password hashing
* Public
* Prevents rainbow table attacks

### ✅ Encryption Key

* Used for AES/RSA
* Secret
* Must be protected (KMS, Vault, HSM)

---

### Why NOT SHA-256 for passwords?

* Too fast → easy brute-force

### Why PBKDF2 / scrypt?

* Intentionally slow
* scrypt is memory-hard → GPU resistant

### Interview Insight

> “Passwords are never encrypted — only hashed using a KDF like scrypt or Argon2.”

---

# 🔁 FILE 04 — KEY MANAGEMENT & ROTATION

### Key Concepts

* Key lifecycle (ACTIVE → RETIRED → DISABLED)
* Key rotation
* HKDF (key derivation)
* Crypto agility

---

## 🔁 Key Rotation Model

```
Old key → RETIRED (still decrypts)
New key → ACTIVE (encrypts new data)
```

✔ Old data remains readable
✔ New data uses new key

---

## 🔐 HKDF (Key Derivation)

```
master_key → enc_key
master_key → signing_key
```

✔ Prevents key reuse across purposes

---

## 🔄 Crypto Agility

Store metadata with ciphertext:

```json
{
  "algorithm": "AES-256-GCM",
  "key_id": "...",
  "version": 2
}
```

---

### Interview Insight

> “I store key_id and algorithm with ciphertext to support key rotation and crypto agility.”

---

# 🏗️ FILE 05 — DATA PIPELINE ENCRYPTION

### Real-world patterns:

## 1. Field-Level Encryption

* Encrypt only sensitive fields (PAN, SSN)
* Keep others queryable

## 2. Tokenization

```
PAN → random token
```

✔ Token has no meaning without vault
✔ Used in financial systems (PCI-DSS)

---

## 3. Encrypted File Format

```
[nonce][length][ciphertext]
```

Overhead:

```
12 (nonce) + 4 (length) + 16 (GCM tag) = 32 bytes
```

---

## 4. End-to-End Pipeline

1. Generate records
2. Encrypt sensitive fields
3. Tokenize PAN
4. Write encrypted file
5. Read + decrypt + verify

---

### Interview Insight

> “I use field-level encryption for queryability and tokenization for downstream analytics safety.”

---

# ⚠️ CRITICAL PYTHON ENCODING LESSON

### ❌ This fails:

```python
b"—"
```

### ✅ Correct:

```python
"—".encode("utf-8")
```

### Why?

* Bytes literals must be ASCII
* Encryption operates on bytes

---

### Interview Answer

> “I always encode strings to UTF-8 before encryption and decode after decryption.”

---

# 🔥 DECISION MATRIX (MEMORIZE THIS)

| Requirement           | Solution               |
| --------------------- | ---------------------- |
| Store passwords       | Argon2 / scrypt        |
| Encrypt data at rest  | AES-256-GCM            |
| Encrypt in transit    | TLS 1.3                |
| Key exchange          | RSA-OAEP / ECDH        |
| Sign data             | RSA-PSS / ECDSA        |
| Integrity             | HMAC-SHA256            |
| Large data encryption | Envelope encryption    |
| Store PAN downstream  | Tokenization           |
| Encrypt DB fields     | Field-level encryption |
| Rotate keys           | Versioned keys + HKDF  |

---

# 🧠 THREE RULES (CAPITAL ONE EXPECTS THESE)

### RULE 1

> Never encrypt passwords — hash them.

### RULE 2

> Never roll your own crypto.

### RULE 3

> Key management is harder than encryption.

---

# 🚀 FINAL TAKEAWAYS

You now understand:

* AES-GCM encryption ✔
* RSA & envelope encryption ✔
* Hashing + salting ✔
* Key rotation ✔
* Tokenization ✔
* Real pipeline encryption ✔

---

# 🎯 What This Prepares You For

This tutorial directly prepares you for:

* Capital One interviews
* Fintech / banking systems
* PCI-DSS compliant pipelines
* Real-world data engineering security

---

## Next Steps

* Run all files end-to-end
* Explain each concept out loud
* Practice interview answers

---

## 💬 If asked one question:

> “How do you securely handle sensitive data?”

You now have a complete answer.

---

**End of Tutorial**
