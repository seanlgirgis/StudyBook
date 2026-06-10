from transformers import pipeline

classifier = pipeline("sentiment-analysis")

result = classifier("I love learning about AI.")
print(result)