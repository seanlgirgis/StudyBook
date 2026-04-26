# ChatGPT Prompt — Encryption for Data Engineers
# READY TO PASTE — fully specified, no placeholders
# Paste everything between the === markers into ChatGPT

===

TOPIC: Encryption for Data Engineers
SLUG: encryption
PRIORITY: Capital One Interview Prep
INFRASTRUCTURE: Pure Python — cryptography, hashlib, secrets, base64 (stdlib + one third-party lib)
NO AWS, NO DOCKER, NO CLEANUP RULES NEEDED.

Capital One context: encryption is front-and-centre in every Capital One data engineering
interview. They handle cardholder data (PAN, CVV, SSN) and operate under PCI-DSS.
Expect questions on: symmetric vs asymmetric, AES-GCM, key management, envelope
encryption, hashing vs encryption, salted hashes, and when to use what.

===== CODING STANDARDS =====

FILE HEADER (every file must start with this block):
# ============================================================
# Topic   : Encryption for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install cryptography
# Run     : python NN_filename.py
# ============================================================

CRITICAL — CODE QUALITY:
- Every function must be COMPLETE and FULLY RUNNABLE — no placeholders, no TODO
  comments, no pass statements, no "add logic here" stubs.
- Generate the ENTIRE file contents each time. Never truncate with "..." or "rest is same".
- Comments explain WHY — interviewers care about tradeoffs, not just syntax.
  Every choice (AES-GCM over CBC, Argon2 over MD5, etc.) must be justified.
- Use the `cryptography` library (PyCA). Do NOT use PyCryptodome or pycrypto.
- Never hardcode keys or secrets — always generate them in the demo and discard.
- Print real output: ciphertext hex, decrypted plaintext, hash digests, timing numbers.
- No env vars required. All output is in-memory or to /tmp/studybook/encryption/
  (Windows: C:/tmp/studybook/encryption/). Detect with os.name.

===== FILE 01: 01_symmetric_encryption_aes.py =====

Purpose: AES encryption — the workhorse of data-at-rest encryption.
Capital One encrypts PAN data (card numbers) with AES-256. Know it cold.

Implement these functions in this exact order:

def get_output_dir() -> Path:
    """Return platform-specific output dir. Create if missing."""

def generate_aes_key(key_size_bits: int = 256) -> bytes:
    """
    Generate a random AES key.
    key_size_bits: 128, 192, or 256. Default 256 (strongest, no performance penalty).
    Use os.urandom(key_size_bits // 8).
    Validate key_size_bits in {128, 192, 256} — raise ValueError otherwise.
    Print: "AES-{key_size_bits} key generated: {key.hex()[:16]}...  ({len(key)} bytes)"
    WHY 256: AES-256 is required by PCI-DSS for cardholder data. No performance
    penalty vs AES-128 on modern hardware with AES-NI instruction sets.
    """

def encrypt_aes_gcm(plaintext: bytes, key: bytes) -> dict:
    """
    Encrypt with AES-256-GCM (Galois/Counter Mode).
    Use cryptography.hazmat.primitives.ciphers.aead.AESGCM.
    Generate a fresh 12-byte nonce with os.urandom(12) for every encryption.
    Return:
      { nonce_hex: str, ciphertext_hex: str, tag_hex: str (last 16 bytes),
        plaintext_len: int, ciphertext_len: int }
    WHY GCM: GCM provides BOTH confidentiality AND integrity (AEAD).
    The 16-byte authentication tag detects any tampering with the ciphertext.
    AES-CBC provides only confidentiality — an attacker can flip bits without detection.
    WHY fresh nonce: reusing a nonce with the same key under GCM is catastrophic —
    it reveals the keystream XOR and breaks both confidentiality and integrity.
    Print nonce_hex, first 32 chars of ciphertext_hex.
    """

def decrypt_aes_gcm(nonce_hex: str, ciphertext_hex: str, key: bytes) -> bytes:
    """
    Decrypt AES-256-GCM ciphertext. The tag is appended to the ciphertext by AESGCM.
    On tampering (wrong key or modified ciphertext), cryptography raises InvalidTag.
    Catch InvalidTag and raise ValueError("Decryption failed: ciphertext was tampered")
    Return plaintext bytes.
    """

def demonstrate_tamper_detection(key: bytes) -> None:
    """
    Show AES-GCM tamper detection in action:
    1. Encrypt "Cardholder Name: John Smith | PAN: 4111111111111111"
    2. Flip one bit in the ciphertext (ciphertext[5] ^= 0x01)
    3. Try to decrypt → must raise ValueError("Decryption failed: ciphertext was tampered")
    4. Print: "Tamper detected ✓ — AES-GCM authentication tag caught the modification"
    """

def compare_aes_modes() -> None:
    """
    Print a formatted comparison table of AES modes:

    Mode    | Auth? | Nonce required? | Parallelisable? | Use case
    --------|-------|-----------------|-----------------|----------------------------
    ECB     | No    | No              | Yes             | ❌ Never — deterministic
    CBC     | No    | Yes (IV)        | Decrypt only    | Legacy systems only
    CTR     | No    | Yes             | Yes             | Streaming (no auth)
    GCM     | Yes   | Yes (12 bytes)  | Yes             | ✅ Default choice for DE
    SIV     | Yes   | No              | No              | Deterministic encryption

    Also explain why ECB should never be used: identical plaintext blocks produce
    identical ciphertext blocks, revealing patterns (famous ECB penguin image).
    """

def benchmark_aes_gcm(plaintext_size_mb: float = 10.0) -> dict:
    """
    Benchmark AES-256-GCM throughput.
    Generate plaintext_size_mb megabytes of random data.
    Encrypt it. Decrypt it. Measure each.
    Return: { plaintext_mb: float, encrypt_ms: float, decrypt_ms: float,
              encrypt_mbps: float, decrypt_mbps: float }
    Print: "AES-256-GCM: 10 MB encrypted in 12 ms (833 MB/s)"
    WHY matters: interviewers ask if encryption is a bottleneck. It is not on modern
    hardware — AES-NI handles ~1-5 GB/s. The bottleneck is always I/O or key fetch.
    """

def main():
    out = get_output_dir()

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
    print(f"Encrypt: {stats['encrypt_mbps']:.0f} MB/s  |  "
          f"Decrypt: {stats['decrypt_mbps']:.0f} MB/s")

if __name__ == "__main__":
    main()

===== FILE 02: 02_asymmetric_encryption_rsa.py =====

Purpose: RSA and elliptic curve cryptography — used for key exchange, digital signatures,
and TLS. Capital One uses asymmetric crypto for API signing and certificate management.

from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.primitives import hashes, serialization

def generate_rsa_key_pair(key_size: int = 2048) -> tuple:
    """
    Generate RSA private/public key pair.
    key_size: 2048 (minimum acceptable) or 4096 (high-security).
    Use rsa.generate_private_key(public_exponent=65537, key_size=key_size).
    WHY 65537: it's the standard RSA public exponent — prime, efficient in binary,
    resistant to small-exponent attacks.
    Return (private_key, public_key).
    Print key size, public exponent.
    """

def encrypt_rsa_oaep(plaintext: bytes, public_key) -> bytes:
    """
    Encrypt with RSA-OAEP (Optimal Asymmetric Encryption Padding).
    Use padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None).
    WHY OAEP not PKCS1v15: PKCS#1 v1.5 is vulnerable to Bleichenbacher's attack (1998).
    OAEP is the modern standard. Never use raw RSA or PKCS1v15 padding for new code.
    RSA-2048 can encrypt at most 214 bytes — only use it for small data (keys/tokens).
    Return ciphertext bytes.
    """

def decrypt_rsa_oaep(ciphertext: bytes, private_key) -> bytes:
    """Decrypt RSA-OAEP ciphertext. Return plaintext bytes."""

def sign_rsa_pss(message: bytes, private_key) -> bytes:
    """
    Sign message with RSA-PSS (Probabilistic Signature Scheme).
    Use padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH).
    WHY PSS not PKCS1v15 for signing: PSS is provably secure. PKCS1v15 signing
    is still widely used but has known weaknesses under certain conditions.
    Return signature bytes.
    """

def verify_rsa_pss(message: bytes, signature: bytes, public_key) -> bool:
    """
    Verify RSA-PSS signature. Return True if valid.
    Catch InvalidSignature → return False (do not raise).
    """

def demonstrate_envelope_encryption(plaintext: bytes) -> dict:
    """
    Envelope encryption — the pattern used in AWS KMS, HashiCorp Vault, and Capital One HSMs.

    Algorithm:
      1. Generate a fresh AES-256 data encryption key (DEK) with os.urandom(32)
      2. Encrypt plaintext with AES-256-GCM using the DEK
      3. Encrypt the DEK with the RSA-2048 public key (RSA-OAEP)
      4. Store: { encrypted_dek_hex, nonce_hex, ciphertext_hex }

    Decryption:
      1. Decrypt the DEK using the RSA private key
      2. Decrypt ciphertext with the recovered DEK

    WHY envelope encryption:
      - RSA can only encrypt ~214 bytes (for 2048-bit key). Plaintext is unbounded.
      - Rotating the master key only requires re-encrypting the DEK, not all data.
      - The DEK lives only in memory during processing — never persisted in plaintext.
      - This is exactly how AWS KMS works: your CMK encrypts DEKs, DEKs encrypt data.

    Return: { encrypted_dek_hex, nonce_hex, ciphertext_hex, decrypted_plaintext }
    Print step-by-step narrative showing each stage.
    """

def generate_ec_key_pair(curve=None) -> tuple:
    """
    Generate EC key pair on P-256 (NIST curve, FIPS-approved).
    Use ec.generate_private_key(ec.SECP256R1()).
    WHY EC over RSA: EC-256 provides equivalent security to RSA-3072 with much
    smaller keys (256 bits vs 3072 bits). Faster for TLS handshakes and mobile.
    Return (private_key, public_key).
    """

def sign_ecdsa(message: bytes, private_key) -> bytes:
    """
    Sign with ECDSA using SHA-256. Use ec.ECDSA(hashes.SHA256()).
    Return DER-encoded signature bytes.
    """

def verify_ecdsa(message: bytes, signature: bytes, public_key) -> bool:
    """Verify ECDSA signature. Return True if valid, False on InvalidSignature."""

def compare_rsa_vs_ec() -> None:
    """
    Print comparison table:

    Algorithm    | Key size | Security equiv | Key gen time | Sign time | Use case
    -------------|----------|----------------|--------------|-----------|----------
    RSA-2048     | 2048 bit | ~112-bit       | ~0.1s        | ~1ms      | Legacy, wide support
    RSA-4096     | 4096 bit | ~140-bit       | ~1s          | ~4ms      | High security legacy
    EC P-256     | 256 bit  | ~128-bit       | ~0.01s       | ~0.3ms    | TLS, JWT, mobile
    EC P-384     | 384 bit  | ~192-bit       | ~0.02s       | ~0.5ms    | Government/FIPS

    Time RSA-2048 key generation vs EC P-256 key generation in this script.
    Print actual measured times.
    """

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
        b"Full cardholder dataset — 10,000 records"
    )
    print(f"Decrypted: {result['decrypted_plaintext']}")

    print("\n=== ECDSA ===")
    ec_priv, ec_pub = generate_ec_key_pair()
    ec_sig = sign_ecdsa(msg, ec_priv)
    print(f"ECDSA valid:    {verify_ecdsa(msg, ec_sig, ec_pub)}")
    print(f"ECDSA tampered: {verify_ecdsa(msg + b'X', ec_sig, ec_pub)}")

    print("\n=== RSA vs EC COMPARISON ===")
    compare_rsa_vs_ec()

if __name__ == "__main__":
    main()

===== FILE 03: 03_hashing_and_password_storage.py =====

Purpose: Hashing, salting, KDFs — the correct way to store passwords and verify data integrity.
Capital One: passwords must NEVER be encrypted (recoverable), only hashed with a strong KDF.

from cryptography.hazmat.primitives import hashes as crypto_hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import hashlib, hmac, secrets

def sha256_digest(data: bytes) -> str:
    """
    Compute SHA-256 digest. Return hex string.
    Use hashlib.sha256(data).hexdigest().
    WHY SHA-256 not MD5/SHA-1: MD5 and SHA-1 are cryptographically broken —
    collision attacks exist. SHA-256 (SHA-2 family) is collision-resistant.
    """

def sha256_file(path: str) -> str:
    """
    Stream-hash a file in 64KB chunks (handles files larger than RAM).
    Return hex digest.
    Pattern: h = hashlib.sha256(); for chunk in iter(lambda: f.read(65536), b""): h.update(chunk)
    WHY streaming: hashing a 10GB file by loading it fully crashes pipelines.
    This pattern is used in S3 ETags, file integrity checks, and deduplication.
    """

def demonstrate_avalanche_effect() -> None:
    """
    Show the avalanche effect: one bit change → completely different hash.
    Hash "password" and "Password" (capital P). Print both digests.
    Show they share 0 bytes in common.
    WHY matters: proves that hashes reveal nothing about input similarity.
    """

def hmac_sha256(message: bytes, secret_key: bytes) -> str:
    """
    Compute HMAC-SHA256 (keyed hash — proves authenticity AND integrity).
    Use hmac.new(secret_key, message, hashlib.sha256).hexdigest().
    WHY HMAC not plain hash: H(key || message) is vulnerable to length-extension
    attacks. HMAC is provably secure as a MAC when SHA-256 is the underlying hash.
    Return hex string.
    """

def verify_hmac(message: bytes, expected_hmac: str, secret_key: bytes) -> bool:
    """
    Constant-time HMAC verification using hmac.compare_digest.
    WHY constant-time: comparing strings with == short-circuits on first mismatch.
    Timing attacks can recover the expected HMAC byte-by-byte by measuring
    response time differences. hmac.compare_digest takes the same time regardless.
    """

def hash_password_pbkdf2(password: str, salt: bytes = None) -> dict:
    """
    Hash a password using PBKDF2-HMAC-SHA256.
    iterations = 600_000  (OWASP 2023 recommendation for PBKDF2-SHA256)
    salt = os.urandom(32) if not provided
    Use PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
    Return: { algorithm: "pbkdf2-sha256", iterations: int,
              salt_hex: str, hash_hex: str }
    WHY iterations: each iteration adds ~0.17ms overhead on modern hardware.
    600k iterations ≈ 100ms per hash — slow enough to resist brute force,
    fast enough for login (users don't notice 100ms).
    WHY random salt: without salt, identical passwords produce identical hashes.
    A rainbow table attack precomputes billions of hash→password mappings.
    Salting makes each hash unique, forcing per-password brute force.
    """

def verify_password_pbkdf2(password: str, stored: dict) -> bool:
    """
    Re-hash password with stored salt + iterations, compare in constant time.
    Use hmac.compare_digest(computed_hash, stored["hash_hex"]).
    """

def hash_password_scrypt(password: str, salt: bytes = None) -> dict:
    """
    Hash a password using scrypt (memory-hard KDF).
    Parameters: n=2**14, r=8, p=1  (OWASP minimum; prod uses n=2**17)
    Use cryptography Scrypt(salt=salt, length=32, n=n, r=r, p=p).
    Return: { algorithm: "scrypt", n: int, r: int, p: int,
              salt_hex: str, hash_hex: str }
    WHY scrypt over PBKDF2: scrypt is memory-hard — it requires large amounts
    of RAM, not just CPU cycles. GPUs have high parallelism but limited RAM bandwidth,
    making them inefficient against scrypt. PBKDF2 is GPU-friendly by comparison.
    WHY not bcrypt: bcrypt is limited to 72-byte passwords and was designed in 1999.
    Argon2id (not in stdlib) is the 2015 Password Hashing Competition winner —
    preferred for new systems, but scrypt is a solid choice available in cryptography.
    """

def demonstrate_rainbow_table_attack() -> None:
    """
    Simulate why unsalted hashes are vulnerable to rainbow tables.
    
    Round 1 — No salt (vulnerable):
      Hash "password123" and "qwerty" with SHA-256 (no salt).
      Build a "rainbow table": {hash: plaintext} for 10 common passwords.
      Show that "password123" and "qwerty" are instantly cracked via table lookup.
      Print: "Cracked 'password123' in 0 ms via rainbow table lookup"

    Round 2 — With salt (safe):
      Hash same passwords with random 32-byte salt.
      Show that the same rainbow table finds nothing.
      Print: "Salt defeated rainbow table — attacker must brute-force each password individually"
    """

def main():
    print("\n=== SHA-256 DIGEST ===")
    data = b"PAN: 4111111111111111 | Amount: $1000.00"
    digest = sha256_digest(data)
    print(f"SHA-256: {digest}")

    print("\n=== FILE INTEGRITY (STREAMING) ===")
    # Write a temp file, hash it, show checksum
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
    print(f"Verify correct:   {verify_password_pbkdf2('correct_horse_battery_staple', stored)}")
    print(f"Verify wrong:     {verify_password_pbkdf2('wrong_password', stored)}")

    print("\n=== SCRYPT PASSWORD HASH ===")
    sc_stored = hash_password_scrypt("my_secure_password")
    print(f"scrypt hash: {sc_stored['hash_hex'][:32]}...")

    print("\n=== RAINBOW TABLE ATTACK DEMO ===")
    demonstrate_rainbow_table_attack()

if __name__ == "__main__":
    main()

===== FILE 04: 04_key_management_and_rotation.py =====

Purpose: Key management — the hardest part of encryption in practice.
Capital One uses AWS KMS + HSMs. This module covers the patterns without real AWS.

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import json, base64, datetime

class KeyStore:
    """
    In-memory key store simulating a secrets manager (Vault / AWS KMS local substitute).
    In production this would be an API call to AWS KMS or HashiCorp Vault.

    Attributes:
        _keys: dict[str, dict]  keyed by key_id
          Each entry: { key_id, key_bytes_b64, algorithm, created_at, status,
                        version, rotated_from }

    Methods — implement all fully:
    """

    def __init__(self):
        self._keys: dict[str, dict] = {}
        self._active_key_id: str | None = None

    def create_key(self, algorithm: str = "AES-256-GCM") -> str:
        """
        Generate a new AES-256 key. Assign uuid4 key_id.
        Store as base64. Set status="ACTIVE", version=1.
        Set as the active key. Return key_id.
        """

    def get_key(self, key_id: str) -> bytes:
        """
        Retrieve raw key bytes by key_id.
        Raise KeyError if key_id unknown.
        Raise ValueError if key status is "DISABLED".
        WHY status check: disabled keys must not be used for new encryption.
        They can still decrypt existing data (see rotate_key).
        """

    def rotate_key(self) -> str:
        """
        Key rotation:
          1. Mark current active key as "RETIRED" (not DISABLED — still needed to decrypt old data)
          2. Generate a new key. Set version = old_version + 1.
          3. Set new key as active.
          4. Return new key_id.
        WHY rotation: limits blast radius of a key compromise. If a key leaks,
        only data encrypted with that key is exposed, not all historical data.
        Print: "Key rotated: {old_id[:8]}... → {new_id[:8]}..."
        """

    def list_keys(self) -> list[dict]:
        """Return list of key metadata dicts (without raw key material)."""

    def disable_key(self, key_id: str) -> None:
        """Mark key as DISABLED. Cannot encrypt or decrypt with it."""

    def encrypt_with_active_key(self, plaintext: bytes) -> dict:
        """
        Encrypt plaintext using the current active key (AES-256-GCM).
        Return: { key_id, nonce_hex, ciphertext_hex }
        WHY store key_id alongside ciphertext: when you rotate keys, you need to
        know WHICH key was used to encrypt each record. This is crypto agility.
        """

    def decrypt(self, encrypted_record: dict) -> bytes:
        """
        Decrypt a record created by encrypt_with_active_key.
        Look up key by encrypted_record["key_id"].
        Supports reading records encrypted with old (RETIRED) keys.
        WHY: key rotation doesn't re-encrypt all historical data immediately.
        Old ciphertexts remain readable via retired keys.
        """

def derive_subkey(master_key: bytes, purpose: str, length: int = 32) -> bytes:
    """
    Derive a purpose-specific subkey using HKDF-SHA256.
    info = purpose.encode()  — the "label" that binds the derived key to its purpose.
    Use HKDF(algorithm=hashes.SHA256(), length=length, salt=None, info=info).
    Return derived key bytes.
    WHY HKDF: never use the same key for both encryption and signing.
    Derive separate keys: master → encrypt_key, master → signing_key, master → mac_key.
    This limits damage if one use-case key is compromised.

    Example:
      master = os.urandom(32)
      enc_key  = derive_subkey(master, "aes-gcm-encryption")
      sign_key = derive_subkey(master, "hmac-sha256-signing")
      # enc_key != sign_key even though derived from same master
    """

def demonstrate_key_rotation_workflow() -> None:
    """
    Full key rotation demo:
      1. Create KeyStore, create initial key (v1)
      2. Encrypt 5 records with v1 key — store encrypted records
      3. Rotate to v2 key
      4. Encrypt 5 more records with v2 key
      5. Show that ALL 10 records can still be decrypted (5 via v1, 5 via v2)
      6. Print summary table:
           Record | Encrypted with | Decryptable?
           -------|---------------|-------------
           0      | v1 (RETIRED)  | ✓
           ...
           5      | v2 (ACTIVE)   | ✓
    """

def demonstrate_crypto_agility() -> None:
    """
    Crypto agility: storing algorithm metadata alongside ciphertext so you can
    migrate to a stronger algorithm without re-encrypting everything at once.

    Show a versioned ciphertext envelope:
      {
        "version": 2,
        "algorithm": "AES-256-GCM",
        "key_id": "abc12345",
        "kdf": "HKDF-SHA256",
        "nonce_hex": "...",
        "ciphertext_hex": "..."
      }

    Explain: "When NIST deprecates AES-256, your decryption code checks 'algorithm'
    and routes to the appropriate library. You never need to re-encrypt everything
    on day one of the migration — you read old records with the old algorithm and
    re-encrypt on write (lazy migration)."

    Print the envelope JSON (pretty-printed) with a real AES-256-GCM ciphertext.
    """

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
    print(f"Encrypted 5 more records with key v2")

    print("\n=== DECRYPT ALL RECORDS (ACROSS KEY VERSIONS) ===")
    for i, rec in enumerate(records):
        pt = ks.decrypt(rec)
        print(f"  Record {i}: {pt.decode()[:30]}...  [key={rec['key_id'][:8]}]")

    print("\n=== KEY DERIVATION (HKDF) ===")
    master = os.urandom(32)
    enc_key  = derive_subkey(master, "aes-gcm-encryption")
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

===== FILE 05: 05_encryption_in_data_pipelines.py =====

Purpose: Practical encryption patterns for data engineering — field-level encryption,
tokenization, encrypted S3 files (local simulation), format-preserving encryption.
This is the Capital One capstone file — real production patterns.

def get_output_dir() -> Path: ...

def encrypt_field_level(record: dict, fields_to_encrypt: list[str],
                        key: bytes) -> dict:
    """
    Field-level encryption: encrypt only sensitive columns, leave others in plaintext.
    For each field in fields_to_encrypt:
      - Encrypt record[field] as UTF-8 bytes with AES-256-GCM
      - Replace record[field] with {"_encrypted": True, "nonce": nonce_hex, "ct": ct_hex}
    Return a new dict (do not mutate original).
    WHY field-level: encrypting the entire row makes SQL queries impossible.
    Field-level lets you query on customer_id while encrypting PAN and SSN.
    """

def decrypt_field_level(record: dict, fields_to_decrypt: list[str],
                        key: bytes) -> dict:
    """
    Reverse field-level encryption. Return record with plaintext fields restored.
    Skip fields that are not encrypted ({"_encrypted": True} check).
    """

def tokenize(value: str, token_map: dict) -> str:
    """
    Tokenization: replace sensitive value with a random opaque token.
    token_map: persistent dict { token: original_value } (in prod: Vault/DB)
    If value already tokenized, return existing token (idempotent).
    token = secrets.token_hex(16)
    WHY tokenization vs encryption:
      - Token is useless without the token vault (no key material in token itself)
      - Format can be preserved (16-char token looks like a PAN)
      - Works in systems that cannot handle encrypted blobs (legacy DBs, logs)
      - Capital One uses tokenization for PAN data — card number → token in all
        downstream systems. Only the vault (HSM-backed) knows the mapping.
    """

def detokenize(token: str, token_map: dict) -> str:
    """Reverse tokenization. Raise KeyError if token not in map."""

def write_encrypted_file(data: bytes, path: Path, key: bytes) -> dict:
    """
    Write an AES-256-GCM encrypted file.
    File format (binary):
      [12 bytes nonce][4 bytes length of ciphertext as uint32 big-endian][ciphertext bytes]
    Return: { path, plaintext_bytes, ciphertext_bytes, overhead_bytes }
    WHY prepend nonce: nonce must travel with ciphertext for decryption.
    Embedding it in the file header avoids storing it separately.
    """

def read_encrypted_file(path: Path, key: bytes) -> bytes:
    """
    Read and decrypt a file written by write_encrypted_file.
    Parse header: first 12 bytes = nonce, next 4 = length, rest = ciphertext.
    Return plaintext bytes.
    """

def demonstrate_pipeline_encryption() -> None:
    """
    End-to-end demo: a realistic Capital One data pipeline.

    Scenario: ingest raw cardholder records, apply field-level encryption on
    sensitive fields, tokenize PANs, write encrypted Parquet-like file to disk,
    read back and verify.

    Steps:
      1. Generate 100 raw cardholder records:
           { customer_id, name, pan (card number), ssn, zip_code, amount }
      2. Apply field-level encryption to ["pan", "ssn"] using AES-256-GCM key
      3. Tokenize each customer's PAN (separate token vault)
      4. Add tokenized_pan to the record (used in downstream analytics)
      5. Serialize all 100 encrypted records as JSON, write to encrypted file
      6. Read back the file, decrypt, deserialize, verify record count
      7. For 3 sample records: decrypt pan + ssn fields, compare with originals

    Print at each step:
      "Step 1: Generated 100 raw records"
      "Step 2: Encrypted PAN and SSN fields  (originals no longer in plaintext)"
      "Step 3: Tokenized 100 PANs → token vault has 100 entries"
      "Step 4: Written encrypted file: {path}  ({size} bytes)"
      "Step 5: Read back and decrypted — {n} records verified ✓"
    """

def show_encryption_decision_matrix() -> None:
    """
    Print the decision matrix interviewers expect Capital One candidates to know:

    Requirement                      | Solution
    ---------------------------------|----------------------------------------------
    Store passwords                  | Argon2id (or scrypt/bcrypt) — never encrypt
    Encrypt data at rest             | AES-256-GCM (symmetric)
    Encrypt data in transit          | TLS 1.3 (don't implement yourself)
    Exchange keys between parties    | RSA-OAEP or ECDH key exchange
    Sign data / prove authenticity   | RSA-PSS or ECDSA
    Verify file integrity            | SHA-256 checksum or HMAC-SHA256
    Encrypt large data efficiently   | Envelope encryption (AES DEK + RSA/KMS CMK)
    Store card numbers downstream    | Tokenization (PAN → token via vault)
    Encrypt specific DB columns      | Field-level encryption (AES-GCM per field)
    Rotate encryption keys           | Key versioning + HKDF derived keys
    Prove data not tampered          | HMAC-SHA256 or AES-GCM auth tag
    Compliance (PCI-DSS)             | AES-256 + TLS 1.2+ + key rotation + audit log

    After the table, print the three rules Capital One candidates must know:
      RULE 1: Never encrypt passwords — hash them with a KDF (scrypt/Argon2id).
      RULE 2: Never roll your own crypto — use established libraries (cryptography, libsodium).
      RULE 3: The hardest part is key management, not the algorithm.
    """

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
    plaintext = b"Sensitive pipeline data — " + os.urandom(10_000)
    path = out / "encrypted_payload.bin"
    stats = write_encrypted_file(plaintext, path, key)
    recovered = read_encrypted_file(path, key)
    assert recovered == plaintext
    print(f"File: {stats['path']}  |  {stats['ciphertext_bytes']} bytes  |  "
          f"Overhead: {stats['overhead_bytes']} bytes (nonce + length prefix)")

    print("\n=== END-TO-END PIPELINE ===")
    demonstrate_pipeline_encryption()

    print("\n=== DECISION MATRIX ===")
    show_encryption_decision_matrix()

if __name__ == "__main__":
    main()

===== CAPSTONE PROJECT =====

Title: Cardholder Data Encryption Layer (Capital One Style)
Scenario: You are building the encryption layer for a payment processing pipeline
that must meet PCI-DSS requirements. The pipeline ingests raw transaction records
and produces an encrypted dataset safe for analytics teams to query.

Directory layout:
  capstone/
    encrypt_pipeline.py   ← full encryption pipeline
    test_encryption.py    ← pytest, 7 tests

===== CAPSTONE FILE: encrypt_pipeline.py =====

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
import os, json, hmac, hashlib, secrets, base64
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

OUTPUT_DIR = Path("C:/tmp/studybook/encryption/capstone" if os.name == "nt"
                  else "/tmp/studybook/encryption/capstone")

# ── Constants ─────────────────────────────────────────────────────────────────

SENSITIVE_FIELDS = ["pan", "ssn"]
ANALYTICS_FIELDS = ["customer_id", "tokenized_pan", "zip_code", "amount",
                    "merchant_id", "transaction_ts", "record_hmac"]

# ── Helpers ───────────────────────────────────────────────────────────────────

def derive_field_key(master_key: bytes, field_name: str) -> bytes:
    """
    Derive a field-specific AES-256 key from master key using HKDF-SHA256.
    info = f"field-encryption:{field_name}".encode()
    WHY: each field has its own derived key — compromising the PAN key
    does not expose the SSN key. Both derived from master, never stored separately.
    """

def aes_gcm_encrypt(plaintext: bytes, key: bytes) -> tuple[str, str]:
    """Encrypt with AES-256-GCM. Return (nonce_hex, ciphertext_hex)."""

def aes_gcm_decrypt(nonce_hex: str, ciphertext_hex: str, key: bytes) -> bytes:
    """Decrypt AES-256-GCM. Return plaintext bytes."""

# ── Key Store (same pattern as file 04) ──────────────────────────────────────

class KeyStore:
    """
    Manages master encryption key lifecycle.
    Methods: create_key, get_active_key, rotate_key, get_key_by_id.
    """

# ── Token Vault ───────────────────────────────────────────────────────────────

class TokenVault:
    """
    In-memory PAN tokenization vault.
    Methods:
      tokenize(pan: str) → str         — returns existing token if PAN already tokenized
      detokenize(token: str) → str     — raises KeyError if unknown
      size() → int
    """

# ── Record Processing ─────────────────────────────────────────────────────────

def generate_transactions(n: int = 1000, seed: int = 42) -> list[dict]:
    """
    Generate n synthetic payment transactions. Columns:
      transaction_id:  str  "TXN-{i:06d}"
      customer_id:     str  "CUST-{i%200:05d}"  (200 unique customers)
      pan:             str  "4{random 15 digits}"  (Visa-format)
      ssn:             str  "{3d}-{2d}-{4d}"
      zip_code:        str  5-digit string
      amount:          float  1.00–5000.00 (2 dp)
      merchant_id:     str  "MERCH-{i%50:04d}"
      transaction_ts:  str  ISO 8601 datetime (last 30 days, random)
    """

def encrypt_record(record: dict, key_store: KeyStore,
                   token_vault: TokenVault) -> dict:
    """
    Encrypt one transaction record for PCI-DSS compliance.

    Steps:
      1. Derive field keys: pan_key = derive_field_key(master, "pan")
                            ssn_key = derive_field_key(master, "ssn")
      2. Encrypt PAN:  {"_enc": True, "nonce": ..., "ct": ..., "key_id": ...}
      3. Encrypt SSN:  same structure
      4. Tokenize PAN: add tokenized_pan to record (plain, safe for analytics)
      5. Compute HMAC-SHA256 over stable fields (customer_id, amount, merchant_id,
         transaction_ts) using derive_field_key(master, "record-integrity")
      6. Return analytics-safe record with encrypted PAN/SSN + tokenized_pan + HMAC

    Return dict with ALL ANALYTICS_FIELDS present.
    """

def decrypt_record(enc_record: dict, key_store: KeyStore,
                   token_vault: TokenVault) -> dict:
    """
    Reverse encrypt_record. Verify HMAC before decrypting.
    Raise ValueError("HMAC verification failed") if record was tampered.
    Return record with plaintext pan and ssn restored.
    """

def run_pipeline(n_transactions: int = 1000) -> dict:
    """
    Full pipeline:
      1. Generate n_transactions raw records
      2. Create KeyStore (v1 key), TokenVault
      3. Encrypt all records
      4. Rotate key to v2 mid-pipeline:
           records 0-499 encrypted with v1, 500-999 with v2
      5. Write all encrypted records as newline-delimited JSON to
           OUTPUT_DIR / "encrypted_transactions.jsonl"
      6. Read back all records
      7. Decrypt all records — verify HMAC for each
      8. Assert: decrypted PAN and SSN match originals for 10 sampled records
      9. Print summary:
           ╔═══════════════════════════════════════════╗
           ║  Encryption Pipeline — Summary             ║
           ╠═══════════════════════════════════════════╣
           ║  Records processed   : 1000               ║
           ║  PAN encrypted       : 1000               ║
           ║  SSN encrypted       : 1000               ║
           ║  PANs tokenized      : 1000               ║
           ║  Unique customers    : 200                 ║
           ║  Key v1 records      : 500                 ║
           ║  Key v2 records      : 500                 ║
           ║  HMAC verified       : 1000 ✓              ║
           ║  Decrypt verified    : 10 sampled ✓        ║
           ╚═══════════════════════════════════════════╝
    Return: { total, pan_encrypted, ssn_encrypted, tokenized, hmac_verified,
              key_v1_records, key_v2_records, decrypt_sampled_ok }
    """

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stats = run_pipeline(n_transactions=1000)
    print(f"\nDone. Output: {OUTPUT_DIR / 'encrypted_transactions.jsonl'}")

if __name__ == "__main__":
    main()

===== CAPSTONE FILE: test_encryption.py =====

"""
pytest — 7 tests validating the encryption pipeline.
Run: pytest test_encryption.py -v
"""
import json, os, secrets, pytest
from pathlib import Path
from cryptography.exceptions import InvalidTag

import sys
sys.path.insert(0, str(Path(__file__).parent))
from encrypt_pipeline import (
    KeyStore, TokenVault, derive_field_key, aes_gcm_encrypt, aes_gcm_decrypt,
    generate_transactions, encrypt_record, decrypt_record, run_pipeline,
    OUTPUT_DIR, SENSITIVE_FIELDS
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
    """Flipping a byte in the ciphertext must raise InvalidTag or ValueError."""
    key = os.urandom(32)
    nonce_hex, ct_hex = aes_gcm_encrypt(b"sensitive data", key)
    ct_bytes = bytearray(bytes.fromhex(ct_hex))
    ct_bytes[0] ^= 0xFF
    tampered_hex = bytes(ct_bytes).hex()
    with pytest.raises((InvalidTag, ValueError)):
        aes_gcm_decrypt(nonce_hex, tampered_hex, key)

def test_field_keys_are_unique():
    """HKDF must produce different keys for different field names from the same master."""
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
    """
    Modifying amount after encryption must cause HMAC verification to fail.
    """
    raw = generate_transactions(1)[0]
    enc = encrypt_record(raw, key_store, vault)
    enc["amount"] = 99999.99   # tamper with amount after HMAC was computed
    with pytest.raises(ValueError, match="HMAC"):
        decrypt_record(enc, key_store, vault)

def test_pipeline_all_records_hmac_verified(pipeline_stats):
    """All records in the pipeline run must pass HMAC verification."""
    assert pipeline_stats["hmac_verified"] == pipeline_stats["total"]

===== GENERATION SEQUENCE =====

Acknowledge these instructions, then wait for me to say "generate file 01".

Generation order:
  "generate file 01"  → 01_symmetric_encryption_aes.py
  "generate file 02"  → 02_asymmetric_encryption_rsa.py
  "generate file 03"  → 03_hashing_and_password_storage.py
  "generate file 04"  → 04_key_management_and_rotation.py
  "generate file 05"  → 05_encryption_in_data_pipelines.py
  "generate readme"   → README.md
  "generate pipeline" → capstone/encrypt_pipeline.py
  "generate tests"    → capstone/test_encryption.py

Each file must be COMPLETE and FULLY RUNNABLE.
No placeholders. No TODO comments. No pass statements.
Generate the ENTIRE file contents every time.

===
