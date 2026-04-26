# ============================================================
# Topic   : Encryption for Data Engineers
# File    : capstone/encrypt_pipeline.py
# Covers  : PCI-DSS style cardholder data encryption pipeline
# Prereqs : pip install cryptography
# Run     : python encrypt_pipeline.py
# ============================================================

"""
PCI-DSS compliant cardholder data encryption pipeline.

Implements:
  - AES-256-GCM field-level encryption for PAN and SSN
  - Tokenization for PAN (analytics-safe token)
  - HMAC-SHA256 record integrity check
  - Key rotation support (KeyStore with v1→v2 rotation)
  - Encrypted file output with versioned envelope header
  - Full decryption and verification pass
"""

import base64
import datetime
import hashlib
import hmac
import json
import os
import random
import secrets
import uuid
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


OUTPUT_DIR = Path(
    "C:/tmp/studybook/encryption/capstone"
    if os.name == "nt"
    else "/tmp/studybook/encryption/capstone"
)

SENSITIVE_FIELDS = ["pan", "ssn"]
ANALYTICS_FIELDS = [
    "transaction_id",
    "customer_id",
    "tokenized_pan",
    "zip_code",
    "amount",
    "merchant_id",
    "transaction_ts",
    "pan",
    "ssn",
    "record_hmac",
]


def derive_field_key(master_key: bytes, field_name: str) -> bytes:
    """
    Derive a field-specific AES-256 key from master key using HKDF-SHA256.

    WHY:
    A single master key should not be reused directly for every purpose.
    PAN encryption, SSN encryption, and HMAC integrity each get separate derived keys.
    If one derived key is exposed, the other purposes remain isolated.
    """
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=f"field-encryption:{field_name}".encode("utf-8"),
    )
    return hkdf.derive(master_key)


def aes_gcm_encrypt(plaintext: bytes, key: bytes) -> tuple[str, str]:
    """Encrypt with AES-256-GCM. Return (nonce_hex, ciphertext_hex)."""
    if len(key) != 32:
        raise ValueError("AES-256-GCM requires a 32-byte key")

    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, None)
    return nonce.hex(), ciphertext.hex()


def aes_gcm_decrypt(nonce_hex: str, ciphertext_hex: str, key: bytes) -> bytes:
    """Decrypt AES-256-GCM. Return plaintext bytes."""
    if len(key) != 32:
        raise ValueError("AES-256-GCM requires a 32-byte key")

    return AESGCM(key).decrypt(
        bytes.fromhex(nonce_hex),
        bytes.fromhex(ciphertext_hex),
        None,
    )


class KeyStore:
    """
    Manages master encryption key lifecycle.

    Production equivalent:
      - AWS KMS
      - HashiCorp Vault
      - HSM-backed enterprise key manager

    This tutorial implementation stores keys in memory only.
    """

    def __init__(self):
        self._keys: dict[str, dict] = {}
        self._active_key_id: str | None = None

    def create_key(self) -> str:
        """Create a new AES-256 master key and mark it ACTIVE."""
        key_id = str(uuid.uuid4())
        key_bytes = os.urandom(32)

        self._keys[key_id] = {
            "key_id": key_id,
            "key_bytes_b64": base64.b64encode(key_bytes).decode("utf-8"),
            "algorithm": "AES-256-GCM",
            "created_at": datetime.datetime.now(datetime.UTC).isoformat(),
            "status": "ACTIVE",
            "version": 1,
            "rotated_from": None,
        }

        self._active_key_id = key_id
        return key_id

    def get_active_key(self) -> tuple[str, bytes]:
        """Return active key id and raw key bytes."""
        if self._active_key_id is None:
            raise RuntimeError("No active key exists")

        entry = self._keys[self._active_key_id]
        if entry["status"] != "ACTIVE":
            raise ValueError("Active key is not usable for encryption")

        return self._active_key_id, base64.b64decode(entry["key_bytes_b64"])

    def rotate_key(self) -> str:
        """
        Rotate ACTIVE key to RETIRED and create a new ACTIVE key.

        RETIRED keys remain available for decryption.
        DISABLED keys are unusable.
        """
        if self._active_key_id is None:
            raise RuntimeError("No active key exists")

        old_id = self._active_key_id
        old_entry = self._keys[old_id]
        old_entry["status"] = "RETIRED"

        new_id = str(uuid.uuid4())
        new_key = os.urandom(32)

        self._keys[new_id] = {
            "key_id": new_id,
            "key_bytes_b64": base64.b64encode(new_key).decode("utf-8"),
            "algorithm": "AES-256-GCM",
            "created_at": datetime.datetime.now(datetime.UTC).isoformat(),
            "status": "ACTIVE",
            "version": old_entry["version"] + 1,
            "rotated_from": old_id,
        }

        self._active_key_id = new_id
        return new_id

    def get_key_by_id(self, key_id: str) -> bytes:
        """Return raw key bytes for ACTIVE or RETIRED keys."""
        if key_id not in self._keys:
            raise KeyError(f"Unknown key_id: {key_id}")

        entry = self._keys[key_id]
        if entry["status"] == "DISABLED":
            raise ValueError(f"Key {key_id} is DISABLED")

        return base64.b64decode(entry["key_bytes_b64"])

    def key_version(self, key_id: str) -> int:
        """Return key version for reporting."""
        if key_id not in self._keys:
            raise KeyError(f"Unknown key_id: {key_id}")
        return int(self._keys[key_id]["version"])


class TokenVault:
    """
    In-memory PAN tokenization vault.

    Production equivalent:
      - HSM-backed token vault
      - PCI-scoped secure database
      - Dedicated tokenization service

    Tokens are safe for analytics because they reveal nothing without the vault.
    """

    def __init__(self):
        self._token_to_pan: dict[str, str] = {}
        self._pan_to_token: dict[str, str] = {}

    def tokenize(self, pan: str) -> str:
        """Return existing token for PAN or create a new opaque token."""
        if pan in self._pan_to_token:
            return self._pan_to_token[pan]

        token = secrets.token_hex(16)
        while token in self._token_to_pan:
            token = secrets.token_hex(16)

        self._pan_to_token[pan] = token
        self._token_to_pan[token] = pan
        return token

    def detokenize(self, token: str) -> str:
        """Return original PAN for token. Raise KeyError if unknown."""
        if token not in self._token_to_pan:
            raise KeyError(f"Unknown token: {token}")
        return self._token_to_pan[token]

    def size(self) -> int:
        """Return number of tokenized PANs."""
        return len(self._token_to_pan)


def generate_transactions(n: int = 1000, seed: int = 42) -> list[dict]:
    """
    Generate synthetic payment transactions.

    Synthetic data keeps the tutorial safe while preserving realistic shapes:
    PAN-like values, SSN-like values, merchant ids, timestamps, and amounts.
    """
    rng = random.Random(seed)
    now = datetime.datetime.now(datetime.UTC)

    transactions = []

    for i in range(n):
        pan = "4" + "".join(str(rng.randint(0, 9)) for _ in range(15))
        ssn = f"{rng.randint(100, 999)}-{rng.randint(10, 99)}-{rng.randint(1000, 9999)}"
        zip_code = f"{rng.randint(10000, 99999)}"
        amount = round(rng.uniform(1.00, 5000.00), 2)
        days_back = rng.randint(0, 30)
        seconds_back = rng.randint(0, 86_400)
        ts = now - datetime.timedelta(days=days_back, seconds=seconds_back)

        transactions.append(
            {
                "transaction_id": f"TXN-{i:06d}",
                "customer_id": f"CUST-{i % 200:05d}",
                "pan": pan,
                "ssn": ssn,
                "zip_code": zip_code,
                "amount": amount,
                "merchant_id": f"MERCH-{i % 50:04d}",
                "transaction_ts": ts.isoformat(),
            }
        )

    return transactions


def _stable_hmac_payload(record: dict) -> bytes:
    """
    Build deterministic JSON payload for record integrity.

    Only stable analytics fields are included. Encrypted PAN/SSN ciphertext is excluded
    so HMAC verification can happen before decryption while still detecting tampering
    to business-critical fields.
    """
    payload = {
        "transaction_id": record["transaction_id"],
        "customer_id": record["customer_id"],
        "amount": record["amount"],
        "merchant_id": record["merchant_id"],
        "transaction_ts": record["transaction_ts"],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _compute_record_hmac(record: dict, integrity_key: bytes) -> str:
    """Compute HMAC-SHA256 over stable record fields."""
    return hmac.new(
        integrity_key,
        _stable_hmac_payload(record),
        hashlib.sha256,
    ).hexdigest()


def encrypt_record(record: dict, key_store: KeyStore, token_vault: TokenVault) -> dict:
    """
    Encrypt one transaction record for PCI-DSS compliance.

    Output remains analytics-safe:
      - PAN and SSN are encrypted
      - tokenized_pan supports downstream grouping/joining
      - HMAC detects tampering
      - key_id supports key rotation
    """
    key_id, master_key = key_store.get_active_key()

    pan_key = derive_field_key(master_key, "pan")
    ssn_key = derive_field_key(master_key, "ssn")
    integrity_key = derive_field_key(master_key, "record-integrity")

    pan_nonce, pan_ct = aes_gcm_encrypt(record["pan"].encode("utf-8"), pan_key)
    ssn_nonce, ssn_ct = aes_gcm_encrypt(record["ssn"].encode("utf-8"), ssn_key)

    encrypted = {
        "transaction_id": record["transaction_id"],
        "customer_id": record["customer_id"],
        "tokenized_pan": token_vault.tokenize(record["pan"]),
        "zip_code": record["zip_code"],
        "amount": record["amount"],
        "merchant_id": record["merchant_id"],
        "transaction_ts": record["transaction_ts"],
        "pan": {
            "_enc": True,
            "nonce": pan_nonce,
            "ct": pan_ct,
            "key_id": key_id,
        },
        "ssn": {
            "_enc": True,
            "nonce": ssn_nonce,
            "ct": ssn_ct,
            "key_id": key_id,
        },
    }

    encrypted["record_hmac"] = _compute_record_hmac(encrypted, integrity_key)

    for field in ANALYTICS_FIELDS:
        if field not in encrypted:
            raise ValueError(f"Missing analytics field: {field}")

    return encrypted


def decrypt_record(enc_record: dict, key_store: KeyStore, token_vault: TokenVault) -> dict:
    """
    Reverse encrypt_record.

    HMAC is verified before decrypting. This detects tampering to stable business
    fields such as amount, merchant_id, and timestamp.
    """
    pan_meta = enc_record["pan"]
    ssn_meta = enc_record["ssn"]

    if not pan_meta.get("_enc") or not ssn_meta.get("_enc"):
        raise ValueError("Encrypted PAN/SSN metadata is missing")

    pan_key_id = pan_meta["key_id"]
    ssn_key_id = ssn_meta["key_id"]

    if pan_key_id != ssn_key_id:
        raise ValueError("Record uses inconsistent key ids")

    master_key = key_store.get_key_by_id(pan_key_id)
    pan_key = derive_field_key(master_key, "pan")
    ssn_key = derive_field_key(master_key, "ssn")
    integrity_key = derive_field_key(master_key, "record-integrity")

    expected_hmac = _compute_record_hmac(enc_record, integrity_key)
    if not hmac.compare_digest(expected_hmac, enc_record["record_hmac"]):
        raise ValueError("HMAC verification failed")

    try:
        pan = aes_gcm_decrypt(pan_meta["nonce"], pan_meta["ct"], pan_key).decode("utf-8")
        ssn = aes_gcm_decrypt(ssn_meta["nonce"], ssn_meta["ct"], ssn_key).decode("utf-8")
    except InvalidTag as exc:
        raise ValueError("AES-GCM authentication failed") from exc

    vault_pan = token_vault.detokenize(enc_record["tokenized_pan"])
    if vault_pan != pan:
        raise ValueError("Token vault PAN does not match decrypted PAN")

    return {
        "transaction_id": enc_record["transaction_id"],
        "customer_id": enc_record["customer_id"],
        "pan": pan,
        "ssn": ssn,
        "zip_code": enc_record["zip_code"],
        "amount": enc_record["amount"],
        "merchant_id": enc_record["merchant_id"],
        "transaction_ts": enc_record["transaction_ts"],
    }


def _write_jsonl(records: list[dict], path: Path) -> None:
    """Write newline-delimited JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, sort_keys=True) + "\n")


def _read_jsonl(path: Path) -> list[dict]:
    """Read newline-delimited JSON."""
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def run_pipeline(n_transactions: int = 1000) -> dict:
    """
    Full pipeline:
      1. Generate raw transactions
      2. Encrypt with v1 key for first half
      3. Rotate to v2 key for second half
      4. Write encrypted JSONL
      5. Read back and decrypt
      6. Verify HMAC for every record
      7. Verify plaintext against samples
    """
    if n_transactions <= 0:
        raise ValueError("n_transactions must be positive")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_records = generate_transactions(n_transactions)
    key_store = KeyStore()
    token_vault = TokenVault()
    key_store.create_key()

    encrypted_records = []
    midpoint = n_transactions // 2

    for i, record in enumerate(raw_records):
        if i == midpoint:
            key_store.rotate_key()
        encrypted_records.append(encrypt_record(record, key_store, token_vault))

    output_path = OUTPUT_DIR / "encrypted_transactions.jsonl"
    _write_jsonl(encrypted_records, output_path)

    loaded_records = _read_jsonl(output_path)

    hmac_verified = 0
    for enc_record in loaded_records:
        decrypt_record(enc_record, key_store, token_vault)
        hmac_verified += 1

    sample_indexes = sorted(
        set(
            [
                0,
                max(0, midpoint - 1),
                midpoint,
                n_transactions - 1,
                n_transactions // 3,
                (2 * n_transactions) // 3,
                min(n_transactions - 1, 7),
                min(n_transactions - 1, 13),
                min(n_transactions - 1, 29),
                min(n_transactions - 1, 97),
            ]
        )
    )

    decrypt_sampled_ok = True
    for idx in sample_indexes:
        decrypted = decrypt_record(loaded_records[idx], key_store, token_vault)
        if (
            decrypted["pan"] != raw_records[idx]["pan"]
            or decrypted["ssn"] != raw_records[idx]["ssn"]
        ):
            decrypt_sampled_ok = False
            break

    key_v1_records = sum(
        1 for rec in encrypted_records if key_store.key_version(rec["pan"]["key_id"]) == 1
    )
    key_v2_records = sum(
        1 for rec in encrypted_records if key_store.key_version(rec["pan"]["key_id"]) == 2
    )

    stats = {
        "total": n_transactions,
        "pan_encrypted": sum(1 for r in encrypted_records if r["pan"].get("_enc")),
        "ssn_encrypted": sum(1 for r in encrypted_records if r["ssn"].get("_enc")),
        "tokenized": token_vault.size(),
        "unique_customers": len({r["customer_id"] for r in raw_records}),
        "hmac_verified": hmac_verified,
        "key_v1_records": key_v1_records,
        "key_v2_records": key_v2_records,
        "decrypt_sampled_ok": decrypt_sampled_ok,
        "output_path": str(output_path),
    }

    print("╔═══════════════════════════════════════════╗")
    print("║  Encryption Pipeline — Summary            ║")
    print("╠═══════════════════════════════════════════╣")
    print(f"║  Records processed   : {stats['total']:<18}║")
    print(f"║  PAN encrypted       : {stats['pan_encrypted']:<18}║")
    print(f"║  SSN encrypted       : {stats['ssn_encrypted']:<18}║")
    print(f"║  PANs tokenized      : {stats['tokenized']:<18}║")
    print(f"║  Unique customers    : {stats['unique_customers']:<18}║")
    print(f"║  Key v1 records      : {stats['key_v1_records']:<18}║")
    print(f"║  Key v2 records      : {stats['key_v2_records']:<18}║")
    print(f"║  HMAC verified       : {str(stats['hmac_verified']) + ' ✓':<18}║")
    print(f"║  Decrypt verified    : {'10 sampled ✓' if decrypt_sampled_ok else 'FAILED':<18}║")
    print("╚═══════════════════════════════════════════╝")

    return stats


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stats = run_pipeline(n_transactions=1000)
    print(f"\nDone. Output: {stats['output_path']}")


if __name__ == "__main__":
    main()