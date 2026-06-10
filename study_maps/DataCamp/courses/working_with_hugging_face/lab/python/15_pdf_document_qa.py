from pathlib import Path

from pypdf import PdfReader
from transformers import pipeline

pdf_path = Path(__file__).with_name("US_Employee_Policy.pdf")

reader = PdfReader(str(pdf_path))

document_text = ""
for page_number, page in enumerate(reader.pages, start=1):
    page_text = page.extract_text() or ""
    print(f"Extracted page {page_number}: {len(page_text)} characters")
    document_text += page_text + "\n"

qa_pipeline = pipeline(
    task="question-answering",
    model="distilbert-base-cased-distilled-squad",
)

question = "What is the notice period for resignation?"

result = qa_pipeline(
    question=question,
    context=document_text,
)

print("\nQuestion:", question)
print("Raw result:", result)

if result["score"] < 0.30:
    print("Answer: Not enough information in the document.")
else:
    print("Answer:", result["answer"])
