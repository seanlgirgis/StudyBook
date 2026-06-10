from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)

model_name = "distilbert-base-uncased-finetuned-sst-2-english"

my_model = AutoModelForSequenceClassification.from_pretrained(model_name)
my_tokenizer = AutoTokenizer.from_pretrained(model_name)

my_pipeline = pipeline(
    task="sentiment-analysis",
    model=my_model,
    tokenizer=my_tokenizer,
)

output = my_pipeline("This course is pretty good, I guess.")

print(output)
print(f"Sentiment using AutoClasses: {output[0]['label']}")
