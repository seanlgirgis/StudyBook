# How to Run

```powershell
cd <course-path>\lab
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install only the packages required by the active module.

Expected environment variables may include:

```powershell
$env:OPENAI_API_KEY = "..."
```

Never store API keys in committed files.
