from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")

tokens = tokenizer("I like to visit the park on sunny days.", return_tensors="pt")

print(tokens)