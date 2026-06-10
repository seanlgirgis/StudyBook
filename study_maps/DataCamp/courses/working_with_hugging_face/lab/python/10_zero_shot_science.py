from transformers import pipeline

classifier = pipeline(
    task="zero-shot-classification",
    model="facebook/bart-large-mnli",
)

text = "AI-powered robots assist in complex brain surgeries with precision."
categories = ["politics", "science", "sports"]

output = classifier(
    text,
    candidate_labels=categories,
)

print("Sequence:", output["sequence"])
print("Ranked labels:")
for label, score in zip(output["labels"], output["scores"]):
    print(f"  {label}: {score:.4f}")
