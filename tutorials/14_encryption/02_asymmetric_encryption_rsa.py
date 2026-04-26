# ============================================================
# Topic   : Encryption for Data Engineers
# File    : 02_asymmetric_encryption_rsa.py
# Covers  : RSA-OAEP, RSA-PSS, envelope encryption, ECDSA, RSA vs EC
# Prereqs : pip install cryptography
# Run     : python 02_asymmetric_encryption_rsa.py
# ============================================================

import os
import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_rsa_key_pair(key_size: int = 2048) -> tuple:
    """
    Generate RSA private/public key pair.
    """
    if key_size not in {2048, 4096}:
        raise ValueError("key_size must be 2048 or 4096")

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()

    numbers = public_key.public_numbers()
    print(f"RSA key generated: {key_size} bits")
    print(f"Public exponent:   {numbers.e}")

    return private_key, public_key


def encrypt_rsa_oaep(plaintext: bytes, public_key) -> bytes:
    """
    Encrypt with RSA-OAEP.
    """
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    print(f"RSA-OAEP ciphertext: {ciphertext.hex()[:40]}... ({len(ciphertext)} bytes)")
    return ciphertext


def decrypt_rsa_oaep(ciphertext: bytes, private_key) -> bytes:
    """Decrypt RSA-OAEP ciphertext. Return plaintext bytes."""
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def sign_rsa_pss(message: bytes, private_key) -> bytes:
    """
    Sign message with RSA-PSS.
    """
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    print(f"RSA-PSS signature: {signature.hex()[:40]}... ({len(signature)} bytes)")
    return signature


def verify_rsa_pss(message: bytes, signature: bytes, public_key) -> bool:
    """
    Verify RSA-PSS signature. Return True if valid.
    """
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False


def demonstrate_envelope_encryption(plaintext: bytes) -> dict:
    """
    Envelope encryption using AES-256-GCM for data and RSA-OAEP for the DEK.
    """
    print("Step 1: Generate RSA-2048 master key pair")
    private_key, public_key = generate_rsa_key_pair(2048)

    print("Step 2: Generate fresh AES-256 data encryption key (DEK)")
    dek = os.urandom(32)
    print(f"DEK generated in memory: {dek.hex()[:16]}... ({len(dek)} bytes)")

    print("Step 3: Encrypt plaintext with AES-256-GCM using the DEK")
    nonce = os.urandom(12)
    aesgcm = AESGCM(dek)
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    print(f"AES-GCM ciphertext: {ciphertext.hex()[:40]}...")

    print("Step 4: Encrypt the DEK with RSA-OAEP public key")
    encrypted_dek = encrypt_rsa_oaep(dek, public_key)

    envelope = {
        "encrypted_dek_hex": encrypted_dek.hex(),
        "nonce_hex": nonce.hex(),
        "ciphertext_hex": ciphertext.hex(),
    }

    print("Step 5: Decrypt encrypted DEK with RSA private key")
    recovered_dek = decrypt_rsa_oaep(
        bytes.fromhex(envelope["encrypted_dek_hex"]),
        private_key,
    )
    assert recovered_dek == dek

    print("Step 6: Decrypt ciphertext with recovered DEK")
    recovered_plaintext = AESGCM(recovered_dek).decrypt(
        bytes.fromhex(envelope["nonce_hex"]),
        bytes.fromhex(envelope["ciphertext_hex"]),
        associated_data=None,
    )

    assert recovered_plaintext == plaintext
    print("Envelope encryption roundtrip verified ✓")

    return {
        "encrypted_dek_hex": envelope["encrypted_dek_hex"],
        "nonce_hex": envelope["nonce_hex"],
        "ciphertext_hex": envelope["ciphertext_hex"],
        "decrypted_plaintext": recovered_plaintext,
    }


def generate_ec_key_pair(curve=None) -> tuple:
    """
    Generate EC key pair on P-256 by default.
    """
    selected_curve = curve if curve is not None else ec.SECP256R1()
    private_key = ec.generate_private_key(selected_curve)
    public_key = private_key.public_key()

    print(f"EC key generated: {selected_curve.name}")
    return private_key, public_key


def sign_ecdsa(message: bytes, private_key) -> bytes:
    """
    Sign with ECDSA using SHA-256.
    """
    signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
    print(f"ECDSA signature: {signature.hex()[:40]}... ({len(signature)} bytes)")
    return signature


def verify_ecdsa(message: bytes, signature: bytes, public_key) -> bool:
    """Verify ECDSA signature. Return True if valid, False on InvalidSignature."""
    try:
        public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False


def compare_rsa_vs_ec() -> None:
    """
    Print RSA vs EC comparison table and actual local key generation timings.
    """
    rsa_start = time.perf_counter()
    generate_rsa_key_pair(2048)
    rsa_elapsed = time.perf_counter() - rsa_start

    ec_start = time.perf_counter()
    generate_ec_key_pair()
    ec_elapsed = time.perf_counter() - ec_start

    print(
        "\nAlgorithm    | Key size | Security equiv | Key gen time | Sign time | Use case\n"
        "-------------|----------|----------------|--------------|-----------|----------------------\n"
        "RSA-2048     | 2048 bit | ~112-bit       | ~0.1s        | ~1ms      | Legacy, wide support\n"
        "RSA-4096     | 4096 bit | ~140-bit       | ~1s          | ~4ms      | High security legacy\n"
        "EC P-256     | 256 bit  | ~128-bit       | ~0.01s       | ~0.3ms    | TLS, JWT, mobile\n"
        "EC P-384     | 384 bit  | ~192-bit       | ~0.02s       | ~0.5ms    | Government/FIPS"
    )

    print("\nActual measured key generation times on this machine:")
    print(f"RSA-2048: {rsa_elapsed * 1000:.2f} ms")
    print(f"EC P-256: {ec_elapsed * 1000:.2f} ms")

    print(
        "\nInterview takeaway: RSA is still common because it has broad legacy support, "
        "but EC gives equivalent security with much smaller keys and faster handshakes."
    )


def main():
    print("\n=== RSA KEY PAIR ===")
    rsa_priv, rsa_pub = generate_rsa_key_pair(2048)

    print("\n=== RSA-OAEP ENCRYPT / DECRYPT ===")
    secret = b"AES-DEK: " + os.urandom(32).hex().encode()
    ct = encrypt_rsa_oaep(secret, rsa_pub)
    recovered = decrypt_rsa_oaep(ct, rsa_priv)
    assert recovered == secret
    print(f"Recovered: {recovered[:20]}...")

    print("\n=== RSA-PSS SIGN / VERIFY ===")
    msg = b"Payment authorised: $500.00 to merchant 9876"
    sig = sign_rsa_pss(msg, rsa_priv)
    print(f"Valid:   {verify_rsa_pss(msg, sig, rsa_pub)}")
    print(f"Tampered:{verify_rsa_pss(msg + b'X', sig, rsa_pub)}")

    print("\n=== ENVELOPE ENCRYPTION ===")
    result = demonstrate_envelope_encryption(
        "Full cardholder dataset — 10,000 records".encode("utf-8")
    )
    print(f"Decrypted: {result['decrypted_plaintext'].decode('utf-8')}")

    print("\n=== ECDSA ===")
    ec_priv, ec_pub = generate_ec_key_pair()
    ec_sig = sign_ecdsa(msg, ec_priv)
    print(f"ECDSA valid:    {verify_ecdsa(msg, ec_sig, ec_pub)}")
    print(f"ECDSA tampered: {verify_ecdsa(msg + b'X', ec_sig, ec_pub)}")

    print("\n=== RSA vs EC COMPARISON ===")
    compare_rsa_vs_ec()


if __name__ == "__main__":
    main()