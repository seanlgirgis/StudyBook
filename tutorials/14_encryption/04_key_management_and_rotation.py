# ============================================================
# Topic   : Encryption for Data Engineers
# File    : 04_key_management_and_rotation.py
# Covers  : KeyStore, key rotation, HKDF, crypto agility
# Prereqs : pip install cryptography
# Run     : python 04_key_management_and_rotation.py
# ============================================================

import os
import json
import base64
import uuid
import datetime
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


# ─────────────────────────────────────────────────────────────
# KeyStore — simulates KMS / Vault
# ─────────────────────────────────────────────────────────────

class KeyStore:
    """
    In-memory key store simulating AWS KMS / Vault.

    IMPORTANT DESIGN:
    - Keys are NEVER stored in plaintext externally
    - Metadata is separate from key material
    - Rotation does NOT break decryption of old data
    """

    def __init__(self):
        self._keys: dict[str, dict] = {}
        self._active_key_id: str | None = None

    def create_key(self, algorithm: str = "AES-256-GCM") -> str:
        """
        Create new AES-256 key and set as active.
        """
        key_id = str(uuid.uuid4())
        key_bytes = os.urandom(32)

        entry = {
            "key_id": key_id,
            "key_bytes_b64": base64.b64encode(key_bytes).decode(),
            "algorithm": algorithm,
            "created_at": datetime.datetime.now(datetime.UTC).isoformat(),
            "status": "ACTIVE",
            "version": 1,
            "rotated_from": None,
        }

        self._keys[key_id] = entry
        self._active_key_id = key_id

        print(f"Key created: {key_id[:8]}... (v1 ACTIVE)")
        return key_id

    def get_key(self, key_id: str) -> bytes:
        """
        Retrieve key bytes. Reject DISABLED keys.
        """
        if key_id not in self._keys:
            raise KeyError(f"Unknown key_id: {key_id}")

        entry = self._keys[key_id]

        if entry["status"] == "DISABLED":
            raise ValueError(f"Key {key_id} is DISABLED")

        return base64.b64decode(entry["key_bytes_b64"])

    def rotate_key(self) -> str:
        """
        Rotate active key:
        - old ACTIVE → RETIRED
        - new key becomes ACTIVE
        """
        if not self._active_key_id:
            raise RuntimeError("No active key to rotate")

        old_id = self._active_key_id
        old_entry = self._keys[old_id]
        old_entry["status"] = "RETIRED"

        new_id = str(uuid.uuid4())
        new_key = os.urandom(32)

        new_entry = {
            "key_id": new_id,
            "key_bytes_b64": base64.b64encode(new_key).decode(),
            "algorithm": "AES-256-GCM",
            "created_at": datetime.datetime.now(datetime.UTC).isoformat(),
            "status": "ACTIVE",
            "version": old_entry["version"] + 1,
            "rotated_from": old_id,
        }

        self._keys[new_id] = new_entry
        self._active_key_id = new_id

        print(f"Key rotated: {old_id[:8]}... → {new_id[:8]}...")
        return new_id

    def list_keys(self) -> list[dict]:
        """
        Return metadata only (no raw key material).
        """
        return [
            {
                "key_id": k["key_id"],
                "algorithm": k["algorithm"],
                "created_at": k["created_at"],
                "status": k["status"],
                "version": k["version"],
                "rotated_from": k["rotated_from"],
            }
            for k in self._keys.values()
        ]

    def disable_key(self, key_id: str) -> None:
        """
        Disable key permanently.
        """
        if key_id not in self._keys:
            raise KeyError(key_id)

        self._keys[key_id]["status"] = "DISABLED"
        print(f"Key disabled: {key_id[:8]}...")

    def encrypt_with_active_key(self, plaintext: bytes) -> dict:
        """
        Encrypt using current active key.
        """
        if not self._active_key_id:
            raise RuntimeError("No active key")

        key = self.get_key(self._active_key_id)

        nonce = os.urandom(12)
        ct = AESGCM(key).encrypt(nonce, plaintext, None)

        return {
            "key_id": self._active_key_id,
            "nonce_hex": nonce.hex(),
            "ciphertext_hex": ct.hex(),
        }

    def decrypt(self, encrypted_record: dict) -> bytes:
        """
        Decrypt using key referenced in record.
        """
        key = self.get_key(encrypted_record["key_id"])

        return AESGCM(key).decrypt(
            bytes.fromhex(encrypted_record["nonce_hex"]),
            bytes.fromhex(encrypted_record["ciphertext_hex"]),
            None,
        )


# ─────────────────────────────────────────────────────────────
# HKDF — Key derivation
# ─────────────────────────────────────────────────────────────

def derive_subkey(master_key: bytes, purpose: str, length: int = 32) -> bytes:
    """
    Derive purpose-specific key from master using HKDF.
    """
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=None,
        info=purpose.encode(),
    )
    return hkdf.derive(master_key)


# ─────────────────────────────────────────────────────────────
# Demonstrations
# ─────────────────────────────────────────────────────────────

def demonstrate_key_rotation_workflow() -> None:
    """
    Full rotation workflow demo.
    """
    ks = KeyStore()
    ks.create_key()

    records = []

    # Encrypt with v1
    for i in range(5):
        rec = ks.encrypt_with_active_key(f"Record {i}".encode())
        records.append(rec)

    # Rotate to v2
    ks.rotate_key()

    for i in range(5, 10):
        rec = ks.encrypt_with_active_key(f"Record {i}".encode())
        records.append(rec)

    print("\nRecord | Encrypted with | Decryptable?")
    print("-------|----------------|-------------")

    for i, rec in enumerate(records):
        pt = ks.decrypt(rec)
        status = "✓" if pt else "✗"
        version = ks._keys[rec["key_id"]]["version"]
        state = ks._keys[rec["key_id"]]["status"]
        print(f"{i:<6} | v{version} ({state}) | {status}")


def demonstrate_crypto_agility() -> None:
    """
    Show versioned encryption envelope.
    """
    ks = KeyStore()
    kid = ks.create_key()

    record = ks.encrypt_with_active_key(b"Sensitive record")

    envelope = {
        "version": 2,
        "algorithm": "AES-256-GCM",
        "key_id": record["key_id"],
        "kdf": "HKDF-SHA256",
        "nonce_hex": record["nonce_hex"],
        "ciphertext_hex": record["ciphertext_hex"],
    }

    print("\nCrypto agility envelope:")
    print(json.dumps(envelope, indent=2))


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────

def main():
    print("\n=== KEY STORE — CREATE & ENCRYPT ===")
    ks = KeyStore()
    kid1 = ks.create_key()
    print(f"Active key: {kid1[:8]}...")

    records = []
    for i in range(5):
        enc = ks.encrypt_with_active_key(f"Record {i}: PAN=4111...{i:04d}".encode())
        records.append(enc)

    print(f"Encrypted {len(records)} records with key v1")

    print("\n=== KEY ROTATION ===")
    kid2 = ks.rotate_key()

    for i in range(5, 10):
        enc = ks.encrypt_with_active_key(f"Record {i}: PAN=4111...{i:04d}".encode())
        records.append(enc)

    print("Encrypted 5 more records with key v2")

    print("\n=== DECRYPT ALL RECORDS (ACROSS KEY VERSIONS) ===")
    for i, rec in enumerate(records):
        pt = ks.decrypt(rec)
        print(f"  Record {i}: {pt.decode()}  [key={rec['key_id'][:8]}]")

    print("\n=== KEY DERIVATION (HKDF) ===")
    master = os.urandom(32)
    enc_key = derive_subkey(master, "aes-gcm-encryption")
    sign_key = derive_subkey(master, "hmac-sha256-signing")

    print(f"Enc key:  {enc_key.hex()[:32]}...")
    print(f"Sign key: {sign_key.hex()[:32]}...")
    print(f"Different: {enc_key != sign_key}")

    print("\n=== ROTATION WORKFLOW ===")
    demonstrate_key_rotation_workflow()

    print("\n=== CRYPTO AGILITY ENVELOPE ===")
    demonstrate_crypto_agility()


if __name__ == "__main__":
    main()