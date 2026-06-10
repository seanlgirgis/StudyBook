from transformers import pipeline

qa = pipeline(
    "question-answering",
    model="distilbert/distilbert-base-cased-distilled-squad"
)

context = """
Hugging Face was founded in 2016.
The company provides models, datasets, and tools for machine learning.
"""

result = qa(
    question="Who is the CEO of Hugging Face?",
    context=context
)

if result["score"] < 0.30:
    print("Not enough information in the context.")
else:
    print(result["answer"])
