from transformers import AutoTokenizer

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)

text = "AI: Making robots smarter and humans lazier!"

token_pieces = tokenizer.tokenize(text)
encoded = tokenizer(text, return_tensors="pt")

print("Token pieces:")
print(token_pieces)
print()
print("Input IDs:")
print(encoded["input_ids"])
print()
print("Attention mask:")
print(encoded["attention_mask"])
