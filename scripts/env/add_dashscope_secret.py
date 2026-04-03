"""
Add DASHSCOPE_API_KEY to encrypted secrets file.
Uses the same encryption scheme as the PowerShell scripts.
"""

import json
import sys
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

PROJECT_ROOT = Path(r"D:\StudyBook")
SECRETS_DIR = PROJECT_ROOT / "config" / "secrets"
ENCRYPTED_FILE = SECRETS_DIR / "asuspc.secrets.enc.json"

def get_passphrase():
    """Get passphrase from environment or prompt."""
    if "STUDYBOOK_SECRET_PASSPHRASE" in os.environ:
        return os.environ["STUDYBOOK_SECRET_PASSPHRASE"]
    return input("Enter STUDYBOOK secrets passphrase: ")

def decrypt_secret(enc_path: Path, passphrase: str) -> dict:
    """Decrypt the encrypted secrets file."""
    with open(enc_path, 'r', encoding='utf-8') as f:
        payload = json.load(f)
    
    salt = base64.b64decode(payload['salt'])
    iv = base64.b64decode(payload['iv'])
    ciphertext = base64.b64decode(payload['ciphertext'])
    iterations = int(payload['iterations'])
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode('utf-8'))
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove PKCS7 padding
    padding_len = plaintext[-1]
    plaintext = plaintext[:-padding_len]
    
    return json.loads(plaintext.decode('utf-8'))

def encrypt_secret(data: dict, enc_path: Path, passphrase: str):
    """Encrypt data to the secrets file."""
    plaintext = json.dumps(data, indent=2).encode('utf-8')
    
    # Generate random salt and IV
    salt = os.urandom(16)
    iv = os.urandom(16)
    iterations = 150000
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode('utf-8'))
    
    # Add PKCS7 padding
    padding_len = 16 - (len(plaintext) % 16)
    plaintext += bytes([padding_len]) * padding_len
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    payload = {
        "version": 1,
        "algorithm": "AES-256-CBC/PBKDF2-SHA256",
        "iterations": iterations,
        "salt": base64.b64encode(salt).decode('utf-8'),
        "iv": base64.b64encode(iv).decode('utf-8'),
        "ciphertext": base64.b64encode(ciphertext).decode('utf-8')
    }
    
    enc_path.parent.mkdir(parents=True, exist_ok=True)
    with open(enc_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)

def main():
    import sys
    print("=" * 50)
    print("Add DASHSCOPE_API_KEY to encrypted secrets")
    print("=" * 50)
    
    # Get API key from command line arg or prompt
    if len(sys.argv) > 1:
        api_key = sys.argv[1].strip()
    else:
        api_key = input("Enter your DashScope API key: ").strip()
    
    if not api_key:
        print("API key cannot be empty!")
        return
    
    passphrase = get_passphrase()
    
    # Load existing secrets or start fresh
    secrets = {}
    if ENCRYPTED_FILE.exists():
        print(f"Loading existing secrets: {ENCRYPTED_FILE}")
        secrets = decrypt_secret(ENCRYPTED_FILE, passphrase)
    
    # Update secrets
    secrets["DASHSCOPE_API_KEY"] = api_key
    
    # Encrypt and save
    encrypt_secret(secrets, ENCRYPTED_FILE, passphrase)
    print(f"✓ Updated DASHSCOPE_API_KEY in {ENCRYPTED_FILE}")
    print("=" * 50)

if __name__ == "__main__":
    main()
