# ============================================================
# Topic   : Encryption for Data Engineers
# File    : 03_hashing_and_password_storage.py
# Covers  : Hashing, HMAC, PBKDF2, scrypt, salts, rainbow tables
# Prereqs : pip install cryptography
# Run     : python 03_hashing_and_password_storage.py
# ============================================================

import os
import hashlib
import hmac
import secrets
from pathlib import Path

from cryptography.hazmat.primitives import hashes as crypto_hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def sha256_digest(data: bytes) -> str:
    """
    Compute SHA-256 digest.
    WHY: SHA-256 is collision-resistant; MD5/SHA-1 are broken.
    """
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    """
    Stream-hash a file in chunks (memory-safe).
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def demonstrate_avalanche_effect() -> None:
    """
    Show avalanche effect: tiny input change → huge output change.
    """
    h1 = sha256_digest(b"password")
    h2 = sha256_digest(b"Password")

    print(f"password: {h1}")
    print(f"Password: {h2}")

    common_bytes = sum(a == b for a, b in zip(h1, h2))
    print(f"Common hex chars: {common_bytes} / {len(h1)}")
    print("Avalanche effect ✓ — outputs are completely different")


def hmac_sha256(message: bytes, secret_key: bytes) -> str:
    """
    HMAC-SHA256 for integrity + authenticity.
    """
    return hmac.new(secret_key, message, hashlib.sha256).hexdigest()


def verify_hmac(message: bytes, expected_hmac: str, secret_key: bytes) -> bool:
    """
    Constant-time comparison to prevent timing attacks.
    """
    computed = hmac_sha256(message, secret_key)
    return hmac.compare_digest(computed, expected_hmac)


def hash_password_pbkdf2(password: str, salt: bytes = None) -> dict:
    """
    PBKDF2-HMAC-SHA256 password hashing.
    """
    if salt is None:
        salt = os.urandom(32)

    iterations = 600_000

    kdf = PBKDF2HMAC(
        algorithm=crypto_hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )

    hash_bytes = kdf.derive(password.encode("utf-8"))

    return {
        "algorithm": "pbkdf2-sha256",
        "iterations": iterations,
        "salt_hex": salt.hex(),
        "hash_hex": hash_bytes.hex(),
    }


def verify_password_pbkdf2(password: str, stored: dict) -> bool:
    """
    Verify password using stored salt + iterations.
    """
    salt = bytes.fromhex(stored["salt_hex"])
    iterations = stored["iterations"]

    kdf = PBKDF2HMAC(
        algorithm=crypto_hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )

    computed = kdf.derive(password.encode("utf-8")).hex()
    return hmac.compare_digest(computed, stored["hash_hex"])


def hash_password_scrypt(password: str, salt: bytes = None) -> dict:
    """
    scrypt — memory-hard password hashing.
    """
    if salt is None:
        salt = os.urandom(32)

    n, r, p = 2**14, 8, 1

    kdf = Scrypt(
        salt=salt,
        length=32,
        n=n,
        r=r,
        p=p,
    )

    hash_bytes = kdf.derive(password.encode("utf-8"))

    return {
        "algorithm": "scrypt",
        "n": n,
        "r": r,
        "p": p,
        "salt_hex": salt.hex(),
        "hash_hex": hash_bytes.hex(),
    }


def demonstrate_rainbow_table_attack() -> None:
    """
    Demonstrate why unsalted hashes are vulnerable.
    """
    common_passwords = [
        "123456", "password", "qwerty", "abc123",
        "password123", "admin", "letmein"
    ]

    # Build rainbow table (no salt)
    rainbow = {sha256_digest(p.encode()): p for p in common_passwords}

    target = "password123"
    target_hash = sha256_digest(target.encode())

    print("\n--- No Salt (Vulnerable) ---")
    if target_hash in rainbow:
        print(f"Cracked '{target}' instantly via rainbow table ✓")

    print("\n--- With Salt (Safe) ---")
    salt = os.urandom(32)
    salted_hash = sha256_digest(salt + target.encode())

    if salted_hash not in rainbow:
        print("Salt defeated rainbow table — attacker must brute-force each password individually ✓")


def main():
    print("\n=== SHA-256 DIGEST ===")
    data = b"PAN: 4111111111111111 | Amount: $1000.00"
    print(f"SHA-256: {sha256_digest(data)}")

    print("\n=== FILE INTEGRITY (STREAMING) ===")
    tmp = Path("C:/tmp/studybook/encryption" if os.name == "nt"
               else "/tmp/studybook/encryption") / "test_file.bin"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_bytes(os.urandom(1_000_000))
    print(f"File SHA-256: {sha256_file(str(tmp))}")

    print("\n=== AVALANCHE EFFECT ===")
    demonstrate_avalanche_effect()

    print("\n=== HMAC-SHA256 ===")
    key = secrets.token_bytes(32)
    mac = hmac_sha256(b"Transfer $500 to account 98765", key)
    print(f"HMAC: {mac[:32]}...")
    print(f"Valid:   {verify_hmac(b'Transfer $500 to account 98765', mac, key)}")
    print(f"Tampered:{verify_hmac(b'Transfer $500 to account 99999', mac, key)}")

    print("\n=== PBKDF2 PASSWORD HASH ===")
    stored = hash_password_pbkdf2("correct_horse_battery_staple")
    print(f"Hash: {stored['hash_hex'][:32]}...")
    print(f"Verify correct: {verify_password_pbkdf2('correct_horse_battery_staple', stored)}")
    print(f"Verify wrong:   {verify_password_pbkdf2('wrong_password', stored)}")

    print("\n=== SCRYPT PASSWORD HASH ===")
    sc_stored = hash_password_scrypt("my_secure_password")
    print(f"scrypt hash: {sc_stored['hash_hex'][:32]}...")

    print("\n=== RAINBOW TABLE ATTACK DEMO ===")
    demonstrate_rainbow_table_attack()


if __name__ == "__main__":
    main()