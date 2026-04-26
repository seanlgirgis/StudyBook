# ============================================================
# Topic   : Encryption for Data Engineers
# File    : 05_encryption_in_data_pipelines.py
# Covers  : Field-level encryption, tokenization, encrypted file I/O, pipeline patterns
# Prereqs : pip install cryptography
# Run     : python 05_encryption_in_data_pipelines.py
# ============================================================

import json
import os
import secrets
import struct
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def get_output_dir() -> Path:
    """Return platform-specific output dir. Create if missing."""
    out = Path("C:/tmp/studybook/encryption" if os.name == "nt" else "/tmp/studybook/encryption")
    out.mkdir(parents=True, exist_ok=True)
    return out


def encrypt_field_level(record: dict, fields_to_encrypt: list[str], key: bytes) -> dict:
    """
    Encrypt only sensitive fields while leaving queryable fields in plaintext.
    """
    encrypted = dict(record)
    aesgcm = AESGCM(key)

    for field in fields_to_encrypt:
        if field not in encrypted:
            continue

        nonce = os.urandom(12)
        plaintext = str(encrypted[field]).encode("utf-8")
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)

        encrypted[field] = {
            "_encrypted": True,
            "nonce": nonce.hex(),
            "ct": ciphertext.hex(),
        }

    return encrypted


def decrypt_field_level(record: dict, fields_to_decrypt: list[str], key: bytes) -> dict:
    """
    Decrypt fields encrypted by encrypt_field_level.
    """
    decrypted = dict(record)
    aesgcm = AESGCM(key)

    for field in fields_to_decrypt:
        value = decrypted.get(field)

        if not isinstance(value, dict) or not value.get("_encrypted"):
            continue

        plaintext = aesgcm.decrypt(
            bytes.fromhex(value["nonce"]),
            bytes.fromhex(value["ct"]),
            None,
        )

        decrypted[field] = plaintext.decode("utf-8")

    return decrypted


def tokenize(value: str, token_map: dict) -> str:
    """
    Replace sensitive value with an opaque random token.

    token_map stores token -> original_value.
    This function is idempotent: same value returns same token.
    """
    for token, original in token_map.items():
        if original == value:
            return token

    token = secrets.token_hex(16)
    token_map[token] = value
    return token


def detokenize(token: str, token_map: dict) -> str:
    """Reverse tokenization. Raise KeyError if token not in map."""
    if token not in token_map:
        raise KeyError(f"Unknown token: {token}")
    return token_map[token]


def write_encrypted_file(data: bytes, path: Path, key: bytes) -> dict:
    """
    Write AES-256-GCM encrypted data to disk.

    File format:
      [12-byte nonce][4-byte ciphertext length][ciphertext bytes]
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, data, None)

    length_prefix = struct.pack(">I", len(ciphertext))
    path.write_bytes(nonce + length_prefix + ciphertext)

    return {
        "path": str(path),
        "plaintext_bytes": len(data),
        "ciphertext_bytes": len(ciphertext),
        "overhead_bytes": 12 + 4 + 16,
    }


def read_encrypted_file(path: Path, key: bytes) -> bytes:
    """
    Read and decrypt file written by write_encrypted_file.
    """
    raw = path.read_bytes()

    if len(raw) < 16:
        raise ValueError("Encrypted file is too short")

    nonce = raw[:12]
    ciphertext_len = struct.unpack(">I", raw[12:16])[0]
    ciphertext = raw[16:16 + ciphertext_len]

    if len(ciphertext) != ciphertext_len:
        raise ValueError("Encrypted file is truncated or corrupted")

    return AESGCM(key).decrypt(nonce, ciphertext, None)


def demonstrate_pipeline_encryption() -> None:
    """
    End-to-end Capital One-style data pipeline demo.
    """
    out = get_output_dir()
    key = os.urandom(32)
    file_key = os.urandom(32)
    token_vault = {}

    raw_records = []
    for i in range(100):
        raw_records.append({
            "customer_id": f"CUST-{i:05d}",
            "name": f"Customer {i}",
            "pan": f"411111111111{i:04d}",
            "ssn": f"123-45-{i:04d}",
            "zip_code": f"{10000 + i}",
            "amount": round(100 + i * 7.25, 2),
        })

    print("Step 1: Generated 100 raw records")

    encrypted_records = []
    for record in raw_records:
        encrypted = encrypt_field_level(record, ["pan", "ssn"], key)
        encrypted["tokenized_pan"] = tokenize(record["pan"], token_vault)
        encrypted_records.append(encrypted)

    print("Step 2: Encrypted PAN and SSN fields  (originals no longer in plaintext)")
    print(f"Step 3: Tokenized 100 PANs → token vault has {len(token_vault)} entries")

    payload = json.dumps(encrypted_records, indent=2).encode("utf-8")
    path = out / "pipeline_encrypted_records.bin"
    stats = write_encrypted_file(payload, path, file_key)

    print(f"Step 4: Written encrypted file: {path}  ({stats['ciphertext_bytes']} bytes)")

    recovered_payload = read_encrypted_file(path, file_key)
    recovered_records = json.loads(recovered_payload.decode("utf-8"))

    assert len(recovered_records) == 100

    for i in range(3):
        decrypted = decrypt_field_level(recovered_records[i], ["pan", "ssn"], key)
        assert decrypted["pan"] == raw_records[i]["pan"]
        assert decrypted["ssn"] == raw_records[i]["ssn"]

    print(f"Step 5: Read back and decrypted — {len(recovered_records)} records verified ✓")


def show_encryption_decision_matrix() -> None:
    """
    Print interview decision matrix.
    """
    print(
        "Requirement                      | Solution\n"
        "---------------------------------|----------------------------------------------\n"
        "Store passwords                  | Argon2id (or scrypt/bcrypt) — never encrypt\n"
        "Encrypt data at rest             | AES-256-GCM (symmetric)\n"
        "Encrypt data in transit          | TLS 1.3 (don't implement yourself)\n"
        "Exchange keys between parties    | RSA-OAEP or ECDH key exchange\n"
        "Sign data / prove authenticity   | RSA-PSS or ECDSA\n"
        "Verify file integrity            | SHA-256 checksum or HMAC-SHA256\n"
        "Encrypt large data efficiently   | Envelope encryption (AES DEK + RSA/KMS CMK)\n"
        "Store card numbers downstream    | Tokenization (PAN → token via vault)\n"
        "Encrypt specific DB columns      | Field-level encryption (AES-GCM per field)\n"
        "Rotate encryption keys           | Key versioning + HKDF derived keys\n"
        "Prove data not tampered          | HMAC-SHA256 or AES-GCM auth tag\n"
        "Compliance (PCI-DSS)             | AES-256 + TLS 1.2+ + key rotation + audit log"
    )

    print("\nRULE 1: Never encrypt passwords — hash them with a KDF (scrypt/Argon2id).")
    print("RULE 2: Never roll your own crypto — use established libraries (cryptography, libsodium).")
    print("RULE 3: The hardest part is key management, not the algorithm.")


def main():
    out = get_output_dir()
    key = os.urandom(32)

    print("\n=== FIELD-LEVEL ENCRYPTION ===")
    record = {
        "customer_id": "C-12345",
        "name": "Jane Smith",
        "pan": "4111111111111111",
        "ssn": "123-45-6789",
        "zip_code": "10001",
        "amount": 1500.00,
    }

    encrypted_record = encrypt_field_level(record, ["pan", "ssn"], key)
    print(f"customer_id: {encrypted_record['customer_id']} (plaintext — queryable)")
    print(f"pan:         {str(encrypted_record['pan'])[:40]}... (encrypted)")

    decrypted_record = decrypt_field_level(encrypted_record, ["pan", "ssn"], key)
    assert decrypted_record["pan"] == record["pan"]
    print(f"pan decrypted: {decrypted_record['pan']} ✓")

    print("\n=== TOKENIZATION ===")
    vault = {}
    token = tokenize("4111111111111111", vault)
    print(f"Token:       {token}")
    print(f"Vault size:  {len(vault)} entry")
    original = detokenize(token, vault)
    print(f"Detokenized: {original}")

    print("\n=== ENCRYPTED FILE I/O ===")
    plaintext = b"Sensitive pipeline data - " + os.urandom(10_000)
    path = out / "encrypted_payload.bin"
    stats = write_encrypted_file(plaintext, path, key)
    recovered = read_encrypted_file(path, key)
    assert recovered == plaintext

    print(
        f"File: {stats['path']}  |  {stats['ciphertext_bytes']} bytes  |  "
        f"Overhead: {stats['overhead_bytes']} bytes (nonce + length prefix + GCM tag)"
    )

    print("\n=== END-TO-END PIPELINE ===")
    demonstrate_pipeline_encryption()

    print("\n=== DECISION MATRIX ===")
    show_encryption_decision_matrix()


if __name__ == "__main__":
    main()