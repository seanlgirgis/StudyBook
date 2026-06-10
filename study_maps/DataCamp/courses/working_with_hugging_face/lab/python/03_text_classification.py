from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)

result = classifier(
    "The course was difficult at first, but now I understand it and feel very happy."
)

print(result)