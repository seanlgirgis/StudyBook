# ============================================================
# Topic   : Encryption for Data Engineers
# File    : capstone/test_encryption.py
# Covers  : pytest validation for PCI-DSS encryption pipeline
# Prereqs : pip install cryptography pytest
# Run     : pytest test_encryption.py -v
# ============================================================

"""
pytest — 7 tests validating the encryption pipeline.
Run: pytest test_encryption.py -v
"""

import os
from pathlib import Path

import pytest
from cryptography.exceptions import InvalidTag

import sys

sys.path.insert(0, str(Path(__file__).parent))

from encrypt_pipeline import (
    KeyStore,
    TokenVault,
    derive_field_key,
    aes_gcm_encrypt,
    aes_gcm_decrypt,
    generate_transactions,
    encrypt_record,
    decrypt_record,
    run_pipeline,
)


@pytest.fixture(scope="session")
def pipeline_stats():
    """Run full pipeline once for the session."""
    return run_pipeline(n_transactions=100)


@pytest.fixture(scope="session")
def key_store():
    ks = KeyStore()
    ks.create_key()
    return ks


@pytest.fixture(scope="session")
def vault():
    return TokenVault()


def test_aes_gcm_roundtrip():
    """Encrypt then decrypt must recover the exact original plaintext."""
    key = os.urandom(32)
    plaintext = b"PAN: 4111111111111111"

    nonce_hex, ct_hex = aes_gcm_encrypt(plaintext, key)
    recovered = aes_gcm_decrypt(nonce_hex, ct_hex, key)

    assert recovered == plaintext


def test_aes_gcm_tamper_raises():
    """Flipping a byte in ciphertext must fail authentication."""
    key = os.urandom(32)
    nonce_hex, ct_hex = aes_gcm_encrypt(b"sensitive data", key)

    ct_bytes = bytearray(bytes.fromhex(ct_hex))
    ct_bytes[0] ^= 0xFF

    with pytest.raises((InvalidTag, ValueError)):
        aes_gcm_decrypt(nonce_hex, ct_bytes.hex(), key)


def test_field_keys_are_unique():
    """HKDF must produce different field keys from the same master."""
    master = os.urandom(32)

    pan_key = derive_field_key(master, "pan")
    ssn_key = derive_field_key(master, "ssn")

    assert pan_key != ssn_key
    assert len(pan_key) == 32
    assert len(ssn_key) == 32


def test_tokenization_idempotent(vault):
    """Tokenizing the same PAN twice must return the same token."""
    pan = "4111111111111111"

    t1 = vault.tokenize(pan)
    t2 = vault.tokenize(pan)

    assert t1 == t2


def test_detokenize_roundtrip(vault):
    """Detokenize must return the original PAN."""
    pan = "5500005555555559"

    token = vault.tokenize(pan)

    assert vault.detokenize(token) == pan


def test_hmac_tamper_detected(key_store, vault):
    """Modifying amount after encryption must cause HMAC verification failure."""
    raw = generate_transactions(1)[0]
    enc = encrypt_record(raw, key_store, vault)

    enc["amount"] = 99999.99

    with pytest.raises(ValueError, match="HMAC"):
        decrypt_record(enc, key_store, vault)


def test_pipeline_all_records_hmac_verified(pipeline_stats):
    """All records in the pipeline run must pass HMAC verification."""
    assert pipeline_stats["hmac_verified"] == pipeline_stats["total"]