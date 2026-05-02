# Job Search RAG

> Match job descriptions against your resume and prep interview questions automatically.

## Problem it solves

When applying to 20+ jobs, it's hard to quickly assess fit or prep targeted questions. This ingests your resume + job descriptions and lets you query across all of them.

## Architecture

```
Resume (PDF/Word) + Job Description texts
      ↓
  [ingest/]  chunk + embed → ChromaDB
      ↓
  [retrieval/]  query → ranked matches + gap analysis
      ↓
  [app/]  FastAPI or Streamlit
```

## Example queries

- "Which of these 10 JDs best match my background?"
- "What skills am I missing for the Staff Engineer role at Stripe?"
- "Generate 5 interview questions based on this job description."

## Run it

```bash
pip install -r requirements.txt
python ingest/load_docs.py
streamlit run app/app.py
```
