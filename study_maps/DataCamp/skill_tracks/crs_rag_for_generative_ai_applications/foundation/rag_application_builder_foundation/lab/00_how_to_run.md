# How to Run the Foundation Labs

## 1. Open PowerShell

```powershell
cd D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\crs_rag_for_generative_ai_applications\foundation\rag_application_builder_foundation\lab
```

## 2. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Create local environment variables

```powershell
Copy-Item .env.example .env
```

Edit `.env` locally. Never commit `.env`.

## 4. Run one tiny script at a time

```powershell
python .\python\stage_01_application_basics\01_first_request.py
```

Do not jump to the complete RAG pipeline before the earlier components are
understood.
