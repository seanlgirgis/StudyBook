from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

text = "The company reported record quarterly revenue."

labels = ["business", "sports", "technology"]

result = classifier(
    text,
    candidate_labels=labels
)

print(result)