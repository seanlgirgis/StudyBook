# QAuth - Alibaba Cloud Qwen Setup

## Setup Complete ✅

Your Alibaba Cloud Qwen API is configured and working.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  D:\StudyBook\poc\qauth_alibaba_demo.py                     │
│  - Uses OpenAI SDK (compatible with DashScope)              │
│  - International endpoint: Singapore region                 │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ API call
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  https://dashscope-intl.aliyuncs.com/compatible-mode/v1     │
│  (Alibaba Cloud Model Studio - International)               │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ Billed to
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Your Alibaba Cloud Trial Credits                           │
│  https://bailian.console.aliyun.com/                        │
└─────────────────────────────────────────────────────────────┘
```

## Credentials

| Item | Value |
|------|-------|
| **API Key Storage** | `config/secrets/asuspc.secrets.enc.json` (encrypted) |
| **Passphrase** | Stored in DPAPI seed file (`.local/studybook.secret.seed.dpapi.json`) |
| **Endpoint** | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| **Models Available** | `qwen-turbo`, `qwen-plus`, `qwen-max`, `qwen3.5` |

## Run the Demo

```powershell
# Using env_setter (loads passphrase automatically)
.\env_setter.ps1
C:\py_venv\proj_educate\Scripts\python.exe D:\StudyBook\poc\qauth_alibaba_demo.py

# Or one-liner with passphrase
powershell "$env:STUDYBOOK_SECRET_PASSPHRASE = 'YOUR_PASSPHRASE'; C:\py_venv\proj_educate\Scripts\python.exe D:\StudyBook\poc\qauth_alibaba_demo.py"
```

## Use in Your Code

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-e0619e62a69e43e88c7912441d27cb6c",  # or from env var
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

print(completion.choices[0].message.content)
```

## Models & Pricing (2026)

| Model | Input (per 1K tokens) | Output (per 1K tokens) | Best For |
|-------|----------------------|------------------------|----------|
| qwen-turbo | $0.002 | $0.006 | Fast, cheap tasks |
| qwen-plus | $0.004 | $0.012 | Balanced performance |
| qwen-max | $0.04 | $0.12 | Complex reasoning |
| qwen3.5 | $0.02 | $0.06 | Latest capabilities |

*Prices for international endpoint. Check current pricing at https://www.alibabacloud.com/en/product/model-studio*

## Check Usage

1. Go to: https://bailian.console.aliyun.com/
2. Navigate to **Usage Statistics** or **Billing**
3. Monitor your trial credit consumption

## Troubleshooting

| Error | Solution |
|-------|----------|
| `401 Unauthorized` | Check API key is correct |
| `403 Forbidden` | Account may need activation |
| `429 Rate Limited` | Slow down requests |
| `Connection timeout` | Check firewall/network |

## Files Created

- `D:\StudyBook\poc\qauth_alibaba_demo.py` - Demo script
- `D:\StudyBook\scripts\env\add_dashscope_secret.py` - Secret management utility
- `D:\StudyBook\config\secrets\asuspc.secrets.enc.json` - Updated with DASHSCOPE_API_KEY

---

**Next Steps:**
- Integrate Qwen API calls into your applications
- Monitor usage at https://bailian.console.aliyun.com/
- Consider upgrading from trial to paid when needed
