# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

# Request/Response schema
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

app = FastAPI(title="Phase2 7B Mini LLM API")

# Load model and tokenizer
MODEL_PATH = "./llm_model"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        device_map="auto",
        torch_dtype=torch.float16
    )
    model.eval()
except Exception as e:
    print(f"Error loading model: {e}")
    raise

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/infer", response_model=QueryResponse)
def infer(request: QueryRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    prompt = (
        "You are a concise, helpful home-services assistant.\n"
        "Answer the user's question in one short paragraph.\n"
        "Do not repeat the question.\n\n"
        f"User question: {query}\n"
        "Answer:"
    )

    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=120,
                do_sample=True,
                temperature=0.4,
                repetition_penalty=1.15,
                pad_token_id=tokenizer.eos_token_id,
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
        answer = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

        return QueryResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))