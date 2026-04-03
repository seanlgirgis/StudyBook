"""
QAuth - Alibaba Cloud DashScope Qwen Model Demo

Uses your Alibaba Cloud trial credits with the international endpoint.
"""

import os
import json
from pathlib import Path
from openai import OpenAI


def load_dashscope_api_key():
    """Load DashScope API key from encrypted secrets or environment."""
    # Try encrypted secrets file first
    secrets_path = Path(__file__).parent.parent / "config" / "secrets" / "asuspc.secrets.enc.json"
    
    if secrets_path.exists():
        # For encrypted files, we need the passphrase from env
        passphrase = os.getenv("STUDYBOOK_SECRET_PASSPHRASE")
        if passphrase:
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.backends import default_backend
            import base64
            
            with open(secrets_path, 'r', encoding='utf-8') as f:
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
            
            padding_len = plaintext[-1]
            plaintext = plaintext[:-padding_len]
            
            secrets = json.loads(plaintext.decode('utf-8'))
            return secrets.get("DASHSCOPE_API_KEY")
    
    # Fallback to environment variable
    return os.getenv("DASHSCOPE_API_KEY")


def create_client():
    """Create OpenAI-compatible client for DashScope international."""
    api_key = load_dashscope_api_key()
    
    if not api_key:
        raise ValueError(
            "No DashScope API key found.\n\n"
            "Setup steps:\n"
            "1. Get your API key from: https://bailian.console.aliyun.com/\n"
            "2. The key is stored in config/secrets/asuspc.secrets.enc.json\n"
            "   OR set DASHSCOPE_API_KEY environment variable"
        )
    
    # International endpoint (Singapore region)
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )
    return client


def chat_with_qwen(messages, model="qwen-plus"):
    """
    Chat with Qwen model via OpenAI-compatible API.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model name (qwen-turbo, qwen-plus, qwen-max, qwen3.5)
    
    Returns:
        Model response text
    """
    try:
        client = create_client()
        
        completion = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        return completion.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Demo: Chat with Qwen."""
    print("=" * 50)
    print("QAuth - Alibaba Cloud Qwen Demo (International)")
    print("=" * 50)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! What can you help me with?"}
    ]
    
    print(f"\nUsing model: qwen-plus")
    print(f"Endpoint: https://dashscope-intl.aliyuncs.com")
    print(f"User: {messages[-1]['content']}")
    print("\nAssistant: ", end="", flush=True)
    
    response = chat_with_qwen(messages)
    print(response)
    
    print("\n" + "=" * 50)
    print("Billed to your Alibaba Cloud trial credits")
    print("Check usage: https://bailian.console.aliyun.com/")
    print("=" * 50)


if __name__ == "__main__":
    main()
