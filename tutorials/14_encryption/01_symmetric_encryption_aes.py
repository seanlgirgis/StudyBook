# ============================================================
# Topic   : Encryption for Data Engineers
# File    : 01_symmetric_encryption_aes.py
# Covers  : AES-256-GCM encryption, tamper detection, modes, benchmark
# Prereqs : pip install cryptography
# Run     : python 01_symmetric_encryption_aes.py
# ============================================================

import os
import time
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def get_output_dir() -> Path:
    """Return platform-specific output dir. Create if missing."""
    out = Path("C:/tmp/studybook/encryption" if os.name == "nt" else "/tmp/studybook/encryption")
    out.mkdir(parents=True, exist_ok=True)
    return out


def generate_aes_key(key_size_bits: int = 256) -> bytes:
    """
    Generate a random AES key.
    """
    valid_sizes = {128, 192, 256}
    if key_size_bits not in valid_sizes:
        raise ValueError(f"key_size_bits must be one of {valid_sizes}")

    key = os.urandom(key_size_bits // 8)

    # AES-256 is the default for PCI-DSS-style cardholder data protection.
    # Modern CPUs provide AES-NI, so AES-256 usually has no meaningful pipeline
    # bottleneck compared with AES-128; storage, network, or key retrieval dominate.
    print(f"AES-{key_size_bits} key generated: {key.hex()[:16]}...  ({len(key)} bytes)")
    return key


def encrypt_aes_gcm(plaintext: bytes, key: bytes) -> dict:
    """
    Encrypt with AES-256-GCM.

    AESGCM.encrypt returns ciphertext with the 16-byte authentication tag appended.
    """
    if len(key) not in {16, 24, 32}:
        raise ValueError("AES key must be 16, 24, or 32 bytes")

    aesgcm = AESGCM(key)

    # GCM requires a unique nonce per key. 12 bytes is the recommended size because
    # GCM can process it directly without extra GHASH work.
    nonce = os.urandom(12)
    ciphertext_with_tag = aesgcm.encrypt(nonce, plaintext, associated_data=None)

    tag = ciphertext_with_tag[-16:]

    print(f"Nonce:      {nonce.hex()}")
    print(f"Ciphertext: {ciphertext_with_tag.hex()[:32]}...")

    return {
        "nonce_hex": nonce.hex(),
        "ciphertext_hex": ciphertext_with_tag.hex(),
        "tag_hex": tag.hex(),
        "plaintext_len": len(plaintext),
        "ciphertext_len": len(ciphertext_with_tag),
    }


def decrypt_aes_gcm(nonce_hex: str, ciphertext_hex: str, key: bytes) -> bytes:
    """
    Decrypt AES-GCM ciphertext. Raises ValueError on tampering.
    """
    try:
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(
            bytes.fromhex(nonce_hex),
            bytes.fromhex(ciphertext_hex),
            associated_data=None,
        )
    except InvalidTag as exc:
        raise ValueError("Decryption failed: ciphertext was tampered") from exc


def demonstrate_tamper_detection(key: bytes) -> None:
    """
    Show AES-GCM tamper detection in action.
    """
    plaintext = b"Cardholder Name: John Smith | PAN: 4111111111111111"
    result = encrypt_aes_gcm(plaintext, key)

    tampered = bytearray(bytes.fromhex(result["ciphertext_hex"]))
    tampered[5] ^= 0x01

    try:
        decrypt_aes_gcm(result["nonce_hex"], tampered.hex(), key)
    except ValueError as exc:
        if str(exc) == "Decryption failed: ciphertext was tampered":
            print("Tamper detected ✓ — AES-GCM authentication tag caught the modification")
            return
        raise

    raise RuntimeError("Tampering was not detected, which should never happen with AES-GCM")


def compare_aes_modes() -> None:
    """
    Print a comparison table of AES modes.
    """
    print(
        "Mode    | Auth? | Nonce required? | Parallelisable? | Use case\n"
        "--------|-------|-----------------|-----------------|----------------------------\n"
        "ECB     | No    | No              | Yes             | ❌ Never — deterministic\n"
        "CBC     | No    | Yes (IV)        | Decrypt only    | Legacy systems only\n"
        "CTR     | No    | Yes             | Yes             | Streaming (no auth)\n"
        "GCM     | Yes   | Yes (12 bytes)  | Yes             | ✅ Default choice for DE\n"
        "SIV     | Yes   | No              | No              | Deterministic encryption"
    )

    print(
        "\nWhy ECB should never be used: identical plaintext blocks produce identical "
        "ciphertext blocks. That leaks structure and patterns, which is why the "
        "famous ECB penguin image remains visibly penguin-shaped after encryption."
    )


def benchmark_aes_gcm(plaintext_size_mb: float = 10.0) -> dict:
    """
    Benchmark AES-256-GCM throughput.
    """
    if plaintext_size_mb <= 0:
        raise ValueError("plaintext_size_mb must be positive")

    key = os.urandom(32)
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)

    plaintext_bytes = int(plaintext_size_mb * 1024 * 1024)
    plaintext = os.urandom(plaintext_bytes)

    enc_start = time.perf_counter()
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    enc_elapsed = time.perf_counter() - enc_start

    dec_start = time.perf_counter()
    decrypted = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    dec_elapsed = time.perf_counter() - dec_start

    assert decrypted == plaintext

    encrypt_ms = enc_elapsed * 1000
    decrypt_ms = dec_elapsed * 1000
    encrypt_mbps = plaintext_size_mb / enc_elapsed
    decrypt_mbps = plaintext_size_mb / dec_elapsed

    print(
        f"AES-256-GCM: {plaintext_size_mb:g} MB encrypted in "
        f"{encrypt_ms:.0f} ms ({encrypt_mbps:.0f} MB/s)"
    )

    return {
        "plaintext_mb": plaintext_size_mb,
        "encrypt_ms": encrypt_ms,
        "decrypt_ms": decrypt_ms,
        "encrypt_mbps": encrypt_mbps,
        "decrypt_mbps": decrypt_mbps,
    }


def main():
    out = get_output_dir()
    print(f"Output directory: {out}")

    print("\n=== KEY GENERATION ===")
    key = generate_aes_key(256)

    print("\n=== AES-256-GCM ENCRYPT / DECRYPT ===")
    plaintext = b"Cardholder Name: Jane Doe | PAN: 4111111111111111 | CVV: 123"
    result = encrypt_aes_gcm(plaintext, key)
    decrypted = decrypt_aes_gcm(result["nonce_hex"], result["ciphertext_hex"], key)
    assert decrypted == plaintext
    print(f"Decrypted: {decrypted.decode()}")

    print("\n=== TAMPER DETECTION ===")
    demonstrate_tamper_detection(key)

    print("\n=== AES MODE COMPARISON ===")
    compare_aes_modes()

    print("\n=== THROUGHPUT BENCHMARK ===")
    stats = benchmark_aes_gcm(plaintext_size_mb=10.0)
    print(
        f"Encrypt: {stats['encrypt_mbps']:.0f} MB/s  |  "
        f"Decrypt: {stats['decrypt_mbps']:.0f} MB/s"
    )


if __name__ == "__main__":
    main()