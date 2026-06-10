import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

inputs = tokenizer(
    "I really enjoy learning Hugging Face.",
    return_tensors="pt"
)

with torch.no_grad():
    outputs = model(**inputs)

predicted_id = outputs.logits.argmax(dim=-1).item()
label = model.config.id2label[predicted_id]

print("Predicted ID:", predicted_id)
print("Label:", label)